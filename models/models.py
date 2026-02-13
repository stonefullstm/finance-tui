# models.py
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from db import Base
import datetime


class Category(Base):
    """Model para a tabela Categories"""
    __tablename__ = 'CATEGORIES'

    id = Mapped[int] = mapped_column(primary_key=True)
    name = Mapped[str]
    transactions = Mapped[List['Transaction']] = relationship()

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'transactions': self.transactions,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            transactions=data.get('transactions'),
        )


class Transaction(Base):
    __tablename__ = 'TRANSACTIONS'

    id = Mapped[int] = mapped_column(primary_key=True)
    description = Mapped[Optional[str]]
    transaction_date = Mapped[datetime.datetime]
    transaction_value = Mapped[float]
    type = Mapped[str]
    category_id = Mapped[int] = mapped_column(ForeignKey('CATEGORIES.id'))
    category = Mapped['Category'] = relationship()

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, date={self.transaction_date}, "
            f"value={self.transaction_value}, type={self.type})>"
        )

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'transaction_date': self.transaction_date,
            'transaction_value': self.transaction_value,
            'type': self.type,
            'category': self.category.to_dict() if self.category else None,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            description=data.get('description'),
            transaction_date=data.get('transaction_date'),
            transaction_value=data.get('transaction_value'),
            type=data.get('type'),
            category_id=data.get('category_id'),
        )
