from textual.screen import Screen
from textual.widgets import Digits
from textual.containers import Grid
from dao.transaction_dao import TransactionDAO


class Dashboard(Screen):
    """Tela principal do dashboard financeiro"""
    CSS_PATH = "dashboard.tcss"

    def compose(self):
        with Grid(id="dashboard-grid"):
            yield Digits("Total Balance", id="total_balance")
            yield Digits("Total Income", id="total_income")
            yield Digits("Total Expenses", id="total_expenses")

    async def on_mount(self) -> None:
        with TransactionDAO() as dao:
            totals = dao.get_totals_by_type()
            self.update_dashboard(
                total_balance=totals["income"] - totals["expense"],
                total_income=totals["income"],
                total_expenses=totals["expense"]
            )

    def update_dashboard(self, total_balance, total_income, total_expenses):
        self.query_one("#total_balance", Digits).update(f"R$ {total_balance:.2f}")
        self.query_one("#total_income", Digits).update(f"R$ {total_income:.2f}")
        self.query_one("#total_expenses", Digits).update(f"R$ {total_expenses:.2f}")
