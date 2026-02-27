import logging
from pathlib import Path
from typing import Iterable
from markdown_pdf import MarkdownPdf, Section

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree

# Uso do logger
logger = logging.getLogger(__name__)


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]


class DirectoryTreeApp(Screen):
    CSS_PATH = "save_pdf.tcss"

    def __init__(self, text_markdown: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_markdown = text_markdown
        self.selected_directory = None

    def compose(self) -> ComposeResult:
        save_pdf_container = Vertical(
            FilteredDirectoryTree("./", id="directory-tree"),
            Horizontal(
                Button("Save PDF", variant="success", disabled=True, id="save-btn"),
                Button("Close", variant="primary", id="close-btn"),
                id="button-container",
            ),
            id="save-pdf-container",
        )
        save_pdf_container.border_title = "Select Directory to Save PDF"
        yield save_pdf_container

    @on(DirectoryTree.DirectorySelected)
    def handle_directory_selected(self, event: DirectoryTree.DirectorySelected):
        self.selected_directory = event.path
        self.query_one("#save-btn", Button).disabled = False

    def on_button_pressed(self, event):
        if event.button.id == "close-btn":
            self.dismiss()
        elif event.button.id == "save-btn":
            logger.info(f"Selected directory: {self.selected_directory}")
            if self.selected_directory:
                pdf_path = self.selected_directory / "response_ai.pdf"

                pdf = MarkdownPdf()
                pdf.add_section(Section(self.text_markdown))
                pdf.save(pdf_path)
                self.dismiss()
