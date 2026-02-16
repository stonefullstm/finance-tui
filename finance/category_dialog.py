from textual.screen import Screen
from textual.widgets import Button, Label, Input, Static
from textual.containers import Grid


class CategoryDialog(Screen):
    """Diálogo para adicionar uma nova categoria"""

    def compose(self):
        yield Grid(
            Label("Add Category", id="title"),
            Label("Category Name:", classes="label"),
            Input(
                placeholder="Ex: Alimentação, Transporte, Saúde",
                classes="input",
                id="category_name",
            ),
            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button("Save", variant="success", id="ok"),
            id="category-dialog",
        )

    def on_button_pressed(self, event):
        if event.button.id == "ok":
            category_name = self.query_one("#category_name", Input).value
            if category_name.strip():  # Verifica se não está vazio
                self.dismiss(category_name.strip())
            else:
                # Você pode adicionar uma mensagem de erro aqui
                self.dismiss(None)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event):
        """Permite confirmar com Enter no campo de input"""
        if event.input.id == "category_name":
            category_name = event.input.value
            if category_name.strip():
                self.dismiss(category_name.strip())
