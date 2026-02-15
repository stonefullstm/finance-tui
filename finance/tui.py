from textual.app import App
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Static


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

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self):
        yield Header()
        add_button = Button("Add", variant="success", id="add")
        add_button.focus()
        buttons_panel = Vertical(
            add_button,
            Button("Delete", variant="warning", id="delete"),
            Button("Edit", variant="primary", id="edit"),
            Static(classes="separator"),
            Button("Clear All", variant="error", id="clear"),
            classes="buttons-panel",
        )
        transactions_list = DataTable(classes="transactions-list")
        transactions_list.focus()
        transactions_list.add_columns(
            "Description", "Date", "Value", "Type", "Category"
        )
        transactions_list.cursor_type = "row"
        transactions_list.zebra_stripes = True
        yield Horizontal(buttons_panel, transactions_list, classes="main-panel")
        yield Footer()

    def on_mount(self):
        self.title = "Personal Finance Manager"
        self.sub_title = "A Finance Manager App With Textual & Python"
        self.load_transactions()

    def load_transactions(self):
        transactions_list = self.query_one(".transactions-list", DataTable)
        transactions_list.clear()
        for transaction in self.db.get_all_transactions():
            transactions_list.add_row(
                transaction.description,
                transaction.transaction_date,
                f"{transaction.transaction_value:.2f}",
                transaction.type,
                transaction.category.name if transaction.category else "None",
            )

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
