from textual.screen import Screen
from textual.widgets import Button, Label, Input, Select, Static
from textual.containers import Grid


class InputDialog(Screen):
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
                options=[("Saúde", 1), ("Feira", 2), ("Lazer", 3)],
                classes="input",
                id="category_id",
            ),
            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button("Ok", variant="success", id="ok"),
            id="input-dialog",
        )

    def on_button_pressed(self, event):
        if event.button.id == "ok":
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
                    "category_id": category_id
                }
            )
        else:
            self.dismiss(())
