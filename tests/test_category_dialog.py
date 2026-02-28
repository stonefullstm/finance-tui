# tests/test_category_dialog.py

import pytest
from textual.app import App
from textual.widgets import Button, Input, Select
from finance.category_dialog import CategoryDialog


# App auxiliar que serve como "casca" para hospedar a Screen nos testes
class CategoryDialogApp(App):
    def on_mount(self) -> None:
        self.push_screen(CategoryDialog())

# ==================== TESTE: composição de widgets ====================


@pytest.mark.asyncio
async def test_category_dialog_composes_widgets():
    """Verifica se todos os widgets são renderizados corretamente"""
    app = CategoryDialogApp()

    async with app.run_test() as pilot:  # noqa F401
        # Verifica se os widgets existem na tela
        assert app.screen.query_one("#category-name", Input)
        assert app.screen.query_one("#compute-option", Select)
        assert app.screen.query_one("#ok", Button)
        assert app.screen.query_one("#cancel", Button)


# ==================== TESTE: botão Cancel ====================

@pytest.mark.asyncio
async def test_cancel_button_dismisses_with_none():
    """Clicar em Cancel deve fechar com None"""
    dismissed_value = []

    app = CategoryDialogApp()

    async with app.run_test() as pilot:
        # Captura o resultado do dismiss
        app.screen.dismiss = lambda val: dismissed_value.append(val)

        await pilot.click("#cancel")
        await pilot.pause()

        assert dismissed_value == [None]


# ==================== TESTE: botão Save com nome válido ====================

@pytest.mark.asyncio
async def test_save_button_with_valid_name():
    """Clicar em Save com nome válido deve retornar o nome"""
    dismissed_value = []

    app = CategoryDialogApp()

    async with app.run_test() as pilot:
        app.screen.dismiss = lambda val: dismissed_value.append(val)

        # Digita no campo de input
        await pilot.click("#category-name")
        await pilot.press("A", "l", "i", "m", "e", "n", "t", "a", "ç", "ã", "o")

        # Clica em Save
        await pilot.click("#ok")
        await pilot.pause()

        assert dismissed_value == ["Alimentação"]
