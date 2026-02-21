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
from dao.category_dao import CategoryDAO
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
                Digits("0", id="kpi-income-value"),
                Static("Incomes", classes="kpi-label"),
                classes="kpi-box income",
            ),
            Vertical(
                Digits("0", id="kpi-expense-value"),
                Static("Expenses", classes="kpi-label"),
                classes="kpi-box expense",
            ),
            Vertical(
                Digits("0", id="kpi-balance-value"),
                Static("Balance", classes="kpi-label"),
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
        # DataTable de categorias
        category_list_table = DataTable(id="category-list-table")
        category_list_table.cursor_type = "row"
        category_list_table.zebra_stripes = True
        category_list_table.add_columns(
            "Name",
        )
        # Container para a lista de categorias (ainda sem conteúdo)
        category_list = Container(
            category_list_table,
            id="category-list-container",
        )
        category_list.border_title = "Categories"  # Define o título aqui!
        # Container com título definido aqui
        transactions_container = Container(
            transactions_list,
            classes="transactions-container",
        )
        transactions_container.border_title = "Transactions"  # Define o título aqui!

        data_view = Horizontal(
            transactions_container,
            category_list,
            classes="data-view",
        )

        expense_container = Container(
            PlotWidget(id="expense-plot"),
            classes="expense-container",
        )
        expense_container.border_title = "Expenses by Month"

        category_container = Container(
            PlotWidget(id="category-plot"),
            classes="category-container",
        )
        category_container.border_title = "Expenses by Category"

        graphics = Horizontal(
            expense_container,
            category_container,
            classes="graphics-container",
        )
        dashboard_container = Vertical(
            data_view,
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
        self.load_categories()
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

    def load_categories(self):
        category_list_table = self.query_one("#category-list-table", DataTable)
        category_list_table.clear()
        with CategoryDAO() as dao:
            categories = sorted(list(dao.get_all_categories()), key=lambda c: c.name)
            for category in categories:
                category_list_table.add_row(
                    category.name,
                    key=category.id,
                )

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

        kpi_income = self.query_one("#kpi-income-value", Digits)
        kpi_expense = self.query_one("#kpi-expense-value", Digits)
        kpi_balance = self.query_one("#kpi-balance-value", Digits)

        kpi_income.update(f"R$ {income:,.2f}")
        kpi_expense.update(f"R$ {expense:,.2f}")
        kpi_balance.update(f"R$ {balance:,.2f}")

    def create_graphic(self):
        with TransactionDAO() as dao:
            totals_by_month = dao.get_totals_by_month()
        months = sorted(totals_by_month.keys())
        # income_values = [totals_by_month[month]["income"] for month in months]
        expense_values = [totals_by_month[month]["expense"] for month in months]
        plot = self.query_one("#expense-plot", PlotWidget)
        plot.clear()
        plot.bar(
            months,
            expense_values,
            bar_style=["red", "blue", "green", "yellow", "magenta", "cyan"],
            label="Expense Data",
        )

    def update_category_graphic(self):
        if not hasattr(self, "_totals_category") or not self._totals_category:
            return

        totals_by_month: dict[str, float] = {}
        for transaction in self._totals_category:
            month_key = transaction.transaction_date.strftime("%Y-%m")
            totals_by_month.setdefault(month_key, 0.0)
            totals_by_month[month_key] += transaction.transaction_value

        months = sorted(totals_by_month.keys())
        values = [totals_by_month[month] for month in months]

        # Eixo X numérico: 0, 1, 2, ...
        x = list(range(len(months)))

        plot = self.query_one("#category-plot", PlotWidget)
        plot.clear()

        # Gráfico de linha
        plot.plot(
            x,
            values,
            line_style="green",
            label="Category Expense Data",
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

    @on(DataTable.RowSelected, "#category-list-table")
    def handle_category_selected(self, event: DataTable.RowSelected):
        category_id = int(event.row_key.value)
        with TransactionDAO() as dao:
            self._totals_category = dao.get_transactions_by_category(category_id)
        self.update_category_graphic()
