from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, MarkdownViewer


class ResponseAIScreen(Screen):
    """Tela para exibir resposta da IA"""

    CSS_PATH = "response_ai.tcss"

    def __init__(self, response_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_text = response_text

    def compose(self):
        yield MarkdownViewer(self.response_text, classes="response-viewer")
        yield Horizontal(
            Button("Close", variant="primary", id="close-btn"),
            Button("Save PDF", variant="success", id="save-btn"),
            id="button-container",
        )

    def on_button_pressed(self, event):
        if event.button.id == "close-btn":
            self.dismiss()
