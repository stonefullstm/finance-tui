from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, MarkdownViewer

from finance.save_pdf import DirectoryTreeApp


class ResponseAIScreen(Screen):
    """Tela para exibir resposta da IA"""

    CSS_PATH = "response_ai.tcss"

    def __init__(self, response_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_text = response_text

    def compose(self):
        response_container = Container(
            MarkdownViewer(self.response_text, classes="response-viewer"),
            Horizontal(
                Button("Close", variant="primary", id="close-btn"),
                Button("Save PDF", variant="success", id="save-btn"),
                id="response-button-container",
            ),
            id="response-container",
        )
        response_container.border_title = "AI Insights"
        yield response_container

    def on_button_pressed(self, event):
        if event.button.id == "close-btn":
            self.dismiss()
        elif event.button.id == "save-btn":
            # Salva a resposta em PDF
            # pdf_path = "response_ai.pdf"
            # pdf = MarkdownPdf()
            # pdf.add_section(Section(self.response_text))
            # pdf.save(pdf_path)
            self.app.push_screen(DirectoryTreeApp(self.response_text))
            self.dismiss()
