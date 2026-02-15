from finance.tui import FinanceApp
from dao.transaction_dao import TransactionDAO

transaction_dao = TransactionDAO()


def main():
    app = FinanceApp(db=transaction_dao)
    app.run()


if __name__ == "__main__":
    main()
