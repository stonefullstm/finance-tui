from textual.screen import Screen
from textual.widgets import Button, Label, Input, Select, Static
from textual.containers import Grid
from dao.category_dao import CategoryDAO
from finance.category_dialog import CategoryDialog


class TransactionDialog(Screen):
    def compose(self):
        yield Grid(
            Label("Add Transaction", id="title"),
            Label("Description:", classes="label"),
            Input(
                placeholder="Transaction Description",
                classes="input",
                id="description",
            ),
            Label("Date:", classes="label"),
            Input(
                placeholder="Transaction Date (DD-MM-YYYY)",
                classes="input",
                id="transaction_date",
            ),
            Label("Value:", classes="label"),
            Input(
                placeholder="Transaction Value",
                classes="input",
                id="transaction_value",
            ),
            Label("Type:", classes="label"),
            Select(
                options=[("Receita", "Receita"), ("Despesa", "Despesa")],
                classes="input",
                id="type",
            ),
            Label("Category:", classes="label"),
            Select(
                options=self.get_category_options(),
                id="category_id",
            ),
            Button("+", variant="primary", id="add_category"),
            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button("Ok", variant="success", id="ok"),
            id="input-dialog",
        )

    def get_category_options(self):
        with CategoryDAO() as dao:
            categories = dao.get_all_categories()
        return [(c.name, c.id) for c in categories]

    def refresh_categories(self):
        """Atualiza a lista de categorias no Select"""
        category_select = self.query_one("#category_id", Select)
        category_select.set_options(self.get_category_options())

    def handle_new_category(self, category_name):
        """Callback que recebe o nome da categoria do diálogo"""
        if category_name:
            # Salva a nova categoria no banco
            with CategoryDAO() as dao:
                new_category = dao.create_category(category_name)
            # Atualiza a lista de categorias
            self.refresh_categories()
            # Seleciona a categoria recém-criada
            category_select = self.query_one("#category_id", Select)
            category_select.value = new_category.id

    async def on_button_pressed(self, event):
        if event.button.id == "add_category":
            # Abre o diálogo de categoria
            self.app.push_screen(CategoryDialog(), self.handle_new_category)
        elif event.button.id == "ok":
            description = self.query_one("#description", Input).value
            transaction_date = self.query_one("#transaction_date", Input).value
            transaction_value = self.query_one("#transaction_value", Input).value
            type = self.query_one("#type", Select).value
            category_id = self.query_one("#category_id", Select).value
            day, month, year = map(int, transaction_date.split("-"))
            transaction_date = f"{year:04d}-{month:02d}-{day:02d}"
            self.dismiss(
                {
                    "description": description,
                    "transaction_date": transaction_date,
                    "transaction_value": float(transaction_value),
                    "type": type,
                    "category_id": category_id,
                }
            )
        else:
            self.dismiss(())
