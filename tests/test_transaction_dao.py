import pytest
from unittest.mock import MagicMock, patch
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from dao.transaction_dao import TransactionDAO
from models.models import Transaction


# ==================== FIXTURES ====================


@pytest.fixture
def mock_session():
    """Cria uma sessão mock do SQLAlchemy"""
    session = MagicMock()
    return session


@pytest.fixture
def transaction_dao(mock_session):
    """Cria uma instância do TransactionDAO com sessão mockada"""
    with patch("db.config.SessionLocal", return_value=mock_session):
        dao = TransactionDAO()
        dao.session = mock_session
        return dao


@pytest.fixture
def sample_transaction():
    """Cria uma transação de exemplo para testes"""
    transaction = Transaction(
        id=1,
        description="Compra de eletrônicos",
        transaction_date="2024-01-01",
        transaction_value=100.0,
        type="Despesa",
        category_id=1,
    )
    return transaction


@pytest.fixture
def sample_transactions():
    """Cria um dicionário de dados de transações de exemplo para testes"""
    return {
        1: Transaction(
            id=1,
            description="Compra de eletrônicos",
            transaction_date="2024-01-01",
            transaction_value=100.0,
            type="Despesa",
            category_id=1,
        ),
        2: Transaction(
            id=2,
            description="Venda de produtos",
            transaction_date="2024-01-02",
            transaction_value=250.0,
            type="Receita",
            category_id=2,
        ),
    }


def test_get_all_transactions(transaction_dao, mock_session, sample_transactions):
    """Testa o método get_all_transactions do TransactionDAO"""
    # Configura o mock
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = list(sample_transactions.values())
    mock_session.execute.return_value = mock_result
    # Chama o método a ser testado
    transactions = transaction_dao.get_all_transactions()
    # Verifica os resultados
    assert len(transactions) == 2
    assert transactions[0].description == "Compra de eletrônicos"
    assert transactions[1].description == "Venda de produtos"
    mock_session.execute.assert_called_once()
