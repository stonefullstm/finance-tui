from textual import on
from textual.app import App
from textual.containers import Horizontal, Vertical, Container
from textual_plot import PlotWidget
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Static,
    Digits,
)
from dao.transaction_dao import TransactionDAO
from finance.question_dialog import QuestionDialog
from finance.transaction_dialog import TransactionDialog
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Salva no arquivo
        logging.StreamHandler(),  # Mostra no console
    ],
)

# Uso do logger
logger = logging.getLogger(__name__)


class FinanceApp(App):
    CSS_PATH = "finance.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("a", "add", "Add"),
        ("e", "edit", "Edit"),
        ("d", "delete", "Delete"),
        ("c", "clear_all", "Clear All"),
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()

    def compose(self):
        yield Header()
        # Barra de KPIs
        yield Horizontal(
            Vertical(
                Digits("0", id="kpi_income_value"),
                Static("Receitas", classes="kpi-label"),
                classes="kpi-box income",
            ),
            Vertical(
                Digits("0", id="kpi_expense_value"),
                Static("Despesas", classes="kpi-label"),
                classes="kpi-box expense",
            ),
            Vertical(
                Digits("0", id="kpi_balance_value"),
                Static("Saldo", classes="kpi-label"),
                classes="kpi-box balance",
            ),
            classes="kpi-bar",
        )
        add_button = Button("Add", variant="success", id="add")
        add_button.focus()
        buttons_panel = Vertical(
            add_button,
            Button("Edit", variant="primary", id="edit"),
            Button("Delete", variant="warning", id="delete"),
            Static(classes="separator"),
            Button("Clear All", variant="error", id="clear"),
            classes="buttons-panel",
        )
        # Container com DataTable
        transactions_list = DataTable(classes="transactions-list")
        transactions_list.cursor_type = "row"
        transactions_list.zebra_stripes = True
        transactions_list.add_columns(
            "Description", "Date", "Value", "Type", "Category"
        )

        # Container com título definido aqui
        transactions_container = Container(
            transactions_list,
            classes="transactions-container",
        )
        transactions_container.border_title = "Transactions"  # Define o título aqui!

        graphics = Horizontal(
            PlotWidget(id="expense_plot"),
            PlotWidget(id="category_plot"),
            classes="dashboard-graphics",
        )
        dashboard_container = Vertical(
            transactions_container,
            graphics,
            classes="dashboard-container",
        )

        yield Horizontal(
            buttons_panel,
            dashboard_container,
            classes="main-panel",
        )
        yield Footer()

    def on_mount(self):
        self.title = "Personal Finance Manager"
        self.sub_title = "A Finance Manager App With Textual & Python"
        self.load_transactions()
        self.update_kpis()
        self.create_graphic()

    def action_request_quit(self):
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)

    def load_transactions(self):
        transactions_list = self.query_one(".transactions-list", DataTable)
        transactions_list.clear()
        with TransactionDAO() as dao:
            transactions = list(dao.get_all_transactions(order=True))
            for transaction in transactions:
                transactions_list.add_row(
                    transaction.description,
                    transaction.transaction_date,
                    f"{transaction.transaction_value:>10.2f}",
                    transaction.type,
                    transaction.category.name if transaction.category else "None",
                    # Armazena o ID da transação como chave da linha
                    key=transaction.id,
                )
        self._last_transactions = transactions  # guarda para cálculo
        self.update_kpis()

    def handle_transaction_result(self, result):
        """Processa o resultado do diálogo (create ou edit)"""
        if result:  # Se não foi cancelado
            with TransactionDAO() as dao:
                if "id" in result:
                    # Modo edição - atualiza transação existente
                    dao.update_transaction(result)
                else:
                    # Modo criação - cria nova transação
                    dao.create_transaction(result)

            # Atualiza a lista de transações na tela
            self.load_transactions()

    def update_kpis(self):
        income = sum(
            t.transaction_value for t in self._last_transactions if t.type == "Receita"
        )
        expense = sum(
            t.transaction_value for t in self._last_transactions if t.type == "Despesa"
        )
        balance = income - expense

        kpi_income = self.query_one("#kpi_income_value", Digits)
        kpi_expense = self.query_one("#kpi_expense_value", Digits)
        kpi_balance = self.query_one("#kpi_balance_value", Digits)

        kpi_income.update(f"R$ {income:,.2f}")
        kpi_expense.update(f"R$ {expense:,.2f}")
        kpi_balance.update(f"R$ {balance:,.2f}")

    def create_graphic(self):
        with TransactionDAO() as dao:
            totals_by_month = dao.get_totals_by_month()
        months = sorted(totals_by_month.keys())
        # income_values = [totals_by_month[month]["income"] for month in months]
        expense_values = [totals_by_month[month]["expense"] for month in months]
        plot = self.query_one("#expense_plot", PlotWidget)
        # Aqui você pode criar um gráfico usando os dados das transações
        # Exemplo: plot.plot(...)
        plot.clear()
        # Exemplo de gráfico simples (substitua pelos seus dados reais)
        plot.bar(
            months,
            expense_values,
            bar_style=["red", "blue", "green"],
            label="Expense Data",
        )

    @on(Button.Pressed, "#add")
    def action_add(self):
        self.push_screen(TransactionDialog(), self.handle_transaction_result)

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    # Quando clicar no botão Edit
    @on(Button.Pressed, "#edit")
    def action_edit(self):
        transactions_list = self.query_one(".transactions-list", DataTable)
        row_key, _ = transactions_list.coordinate_to_cell_key(
            transactions_list.cursor_coordinate
        )
        logger.info(f"Edit button pressed for transaction ID: {row_key.value}")
        with TransactionDAO() as dao:
            transaction = dao.get_transaction_by_id(row_key.value)
        # Abre o diálogo
        self.app.push_screen(
            TransactionDialog(transaction=transaction), self.handle_transaction_result
        )

    @on(Button.Pressed, "#delete")
    def action_delete(self):
        transactions_list = self.query_one(".transactions-list", DataTable)
        row_key, _ = transactions_list.coordinate_to_cell_key(
            transactions_list.cursor_coordinate
        )
        logger.info(f"Delete button pressed for transaction ID: {row_key.value}")
        with TransactionDAO() as dao:
            transaction = dao.get_transaction_by_id(row_key.value)

        def check_answer(accepted):
            if accepted:
                with TransactionDAO() as dao:
                    dao.delete_transaction(transaction.id)
                self.load_transactions()

        self.push_screen(
            QuestionDialog(f"Do you want to delete '{transaction.description}'?"),
            check_answer,
        )
