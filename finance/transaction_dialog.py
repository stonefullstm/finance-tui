from textual.screen import Screen
from textual.widgets import Button, Label, Input, Select, Static
from textual.containers import Grid
from dao.category_dao import CategoryDAO
from finance.category_dialog import CategoryDialog
import datetime


class TransactionDialog(Screen):
    """Diálogo para adicionar ou editar transação"""
    CSS_PATH = "transaction_dialog.tcss"

    def __init__(self, transaction=None, *args, **kwargs):
        """
        Args:
            transaction: Se None, cria nova transação.
                        Se fornecido, edita transação existente.
        """
        super().__init__(*args, **kwargs)
        self.transaction = transaction
        self.is_edit_mode = transaction is not None

    def compose(self):
        # Define valores padrão para modo criação
        description = ""
        transaction_date = datetime.date.today().strftime("%d-%m-%Y")
        transaction_value = ""
        type_value = Select.BLANK
        category_value = Select.BLANK

        # Se estiver em modo edição, preenche com dados existentes
        if self.is_edit_mode:
            year, month, day = self.transaction.transaction_date.strftime(
                "%Y-%m-%d"
            ).split("-")
            description = self.transaction.description
            transaction_date = f"{day}-{month}-{year}"
            transaction_value = str(self.transaction.transaction_value)
            type_value = self.transaction.type
            category_value = self.transaction.category_id

        # Ajusta textos conforme o modo
        title = "Edit Transaction" if self.is_edit_mode else "Add Transaction"
        button_label = "Save" if self.is_edit_mode else "Ok"

        yield Grid(
            Label(title, id="title"),
            Label("Description:", classes="label"),
            Input(
                placeholder="Transaction Description",
                value=description,
                classes="input",
                id="description",
            ),
            Label("Date:", classes="label"),
            Input(
                placeholder="Transaction Date (DD-MM-YYYY)",
                value=transaction_date,
                classes="input",
                id="transaction_date",
            ),
            Label("Value:", classes="label"),
            Input(
                placeholder="Transaction Value",
                value=transaction_value,
                classes="input",
                id="transaction_value",
            ),
            Label("Type:", classes="label"),
            Select(
                options=[("Receita", "Receita"), ("Despesa", "Despesa")],
                value=type_value,
                classes="input",
                id="type",
            ),
            Label("Category:", classes="label"),
            Select(
                options=self.get_category_options(),
                value=category_value,
                id="category_id",
            ),
            Button("+", variant="primary", id="add_category"),
            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button(button_label, variant="success", id="ok"),
            id="input-dialog",
        )

    def get_category_options(self):
        """Retorna lista de categorias do banco de dados"""
        with CategoryDAO() as dao:
            categories = dao.get_all_categories()
            categories.sort(key=lambda c: c.name)
        return [(c.name, c.id) for c in categories]

    def refresh_categories(self):
        """Atualiza a lista de categorias no Select mantendo a seleção atual"""
        category_select = self.query_one("#category_id", Select)
        current_value = category_select.value
        category_select.set_options(self.get_category_options())
        # Tenta manter a seleção anterior
        try:
            category_select.value = current_value
        except ValueError:
            pass

    def handle_new_category(self, category_name):
        """Callback executado após criar nova categoria"""
        if category_name:
            with CategoryDAO() as dao:
                new_category = dao.create_category(category_name)
            self.refresh_categories()
            # Seleciona automaticamente a categoria recém-criada
            category_select = self.query_one("#category_id", Select)
            category_select.value = new_category.id

    def on_button_pressed(self, event):
        """Manipula cliques nos botões"""
        if event.button.id == "add_category":
            # Abre diálogo para criar nova categoria
            self.app.push_screen(CategoryDialog(), self.handle_new_category)

        elif event.button.id == "ok":
            # Coleta os dados do formulário
            description = self.query_one("#description", Input).value
            transaction_date = self.query_one("#transaction_date", Input).value
            transaction_value = self.query_one("#transaction_value", Input).value
            # Substitui virgula por ponto para conversão float
            transaction_value = transaction_value.replace(",", ".")
            type = self.query_one("#type", Select).value
            category_id = self.query_one("#category_id", Select).value

            # Converte data de DD-MM-YYYY para YYYY-MM-DD
            day, month, year = map(int, transaction_date.split("-"))
            transaction_date = f"{year:04d}-{month:02d}-{day:02d}"

            # Monta o dicionário de resultado
            result = {
                "description": description,
                "transaction_date": transaction_date,
                "transaction_value": float(transaction_value),
                "type": type,
                "category_id": category_id,
            }

            # Adiciona o ID se estiver em modo edição
            if self.is_edit_mode:
                result["id"] = self.transaction.id

            self.dismiss(result)
        else:
            # Cancelar - retorna None
            self.dismiss(None)
