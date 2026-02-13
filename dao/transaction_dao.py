# dao.py
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.models import Transaction
from db.config import SessionLocal
from typing import Any, Dict, List, Optional


class TransactionDAO:
    """Data Access Object para a tabela Transactions"""

    def __init__(self):
        self.session = SessionLocal()

    def get_all_transactions(self) -> List[Transaction]:
        """Retorna todas as transações"""
        try:
            transactions = (
                self.session.execute(select(Transaction))
                .scalars()
                .all()
            )
            return transactions
        except SQLAlchemyError as e:
            print(f"Erro ao buscar transações: {e}")
            return []

    def get_transaction_by_id(
        self, transaction_id: int
    ) -> Optional[Transaction]:
        """Retorna uma transação pelo ID"""
        try:
            transaction = self.session.get(Transaction, transaction_id)
            return transaction
        except SQLAlchemyError as e:
            print(f"Erro ao buscar transação por ID: {e}")
            return None

    def create_transaction(
        self, transaction_data: Dict[str, Any]
    ) -> Optional[Transaction]:
        """Cria uma nova transação"""
        new_transaction = Transaction.from_dict(transaction_data)
        try:
            self.session.add(new_transaction)
            self.session.commit()
            self.session.refresh(new_transaction)
            return new_transaction
        except IntegrityError as e:
            self.session.rollback()
            print(f"Erro de integridade ao criar transação: {e}")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao criar transação: {e}")
            return None

    def update_transaction(
        self, transaction_data: Dict[str, Any]
    ) -> Optional[Transaction]:
        """Atualiza uma transação existente"""
        try:
            transaction_id = transaction_data.get("id")
            transaction = self.session.get(Transaction, transaction_id)
            if transaction:
                for key, value in transaction_data.items():
                    if hasattr(transaction, key) and value is not None:
                        setattr(transaction, key, value)
            self.session.commit()
            self.session.refresh(transaction)
            return transaction
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao atualizar transação: {e}")
            return None
        except IntegrityError as e:
            self.session.rollback()
            print(f"Erro de integridade ao atualizar transação: {e}")
            return None

    def delete_transaction(self, transaction_id: int) -> bool:
        """Remove uma transação pelo ID"""
        try:
            transaction = self.session.get(Transaction, transaction_id)
            if transaction:
                self.session.delete(transaction)
                self.session.commit()
                return True
            else:
                print("Transação não encontrada")
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao remover transação: {e}")
            return False

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()
