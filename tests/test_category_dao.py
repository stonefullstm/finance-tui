import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from dao.category_dao import CategoryDAO
from models.models import Category


# ==================== FIXTURES ====================


@pytest.fixture
def mock_session():
    """Cria uma sessão mock do SQLAlchemy"""
    session = MagicMock()
    return session


@pytest.fixture
def category_dao(mock_session):
    """Cria uma instância do CategoryDAO com sessão mockada"""
    with patch("db.config.SessionLocal", return_value=mock_session):
        dao = CategoryDAO()
        dao.session = mock_session
        return dao


@pytest.fixture
def sample_category():
    """Cria uma categoria de exemplo para testes"""
    category = Category(id=1, name="Eletrônicos")
    return category


@pytest.fixture
def sample_categories():
    """Cria uma lista de categorias para testes"""
    return [
        Category(id=1, name="Eletrônicos"),
        Category(id=2, name="Livros"),
        Category(id=3, name="Roupas"),
    ]


# ==================== TESTES: get_all_categories ====================


def test_get_all_categories_success(category_dao, mock_session, sample_categories):
    """Testa busca bem-sucedida de todas as categorias"""
    # Arrange
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = sample_categories
    mock_session.execute.return_value = mock_result

    # Act
    result = category_dao.get_all_categories()

    # Assert
    assert len(result) == 3
    assert result[0].name == "Eletrônicos"
    assert result[1].name == "Livros"
    assert result[2].name == "Roupas"
    mock_session.execute.assert_called_once()


def test_get_all_categories_empty(category_dao, mock_session):
    """Testa busca quando não há categorias"""
    # Arrange
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = []
    mock_session.execute.return_value = mock_result

    # Act
    result = category_dao.get_all_categories()

    # Assert
    assert result == []
    mock_session.execute.assert_called_once()


def test_get_all_categories_database_error(category_dao, mock_session, capsys):
    """Testa comportamento quando ocorre erro no banco"""
    # Arrange
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    # Act
    result = category_dao.get_all_categories()

    # Assert
    assert result == []
    captured = capsys.readouterr()
    assert "Erro ao buscar categorias" in captured.out


# ==================== TESTES: get_category_by_id ====================


def test_get_category_by_id_success(category_dao, mock_session, sample_category):
    """Testa busca bem-sucedida de categoria por ID"""
    # Arrange
    mock_session.get.return_value = sample_category

    # Act
    result = category_dao.get_category_by_id(1)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.name == "Eletrônicos"
    mock_session.get.assert_called_once_with(Category, 1)


def test_get_category_by_id_not_found(category_dao, mock_session):
    """Testa busca de categoria inexistente"""
    # Arrange
    mock_session.get.return_value = None

    # Act
    result = category_dao.get_category_by_id(999)

    # Assert
    assert result is None
    mock_session.get.assert_called_once_with(Category, 999)


def test_get_category_by_id_database_error(category_dao, mock_session, capsys):
    """Testa comportamento quando ocorre erro ao buscar por ID"""
    # Arrange
    mock_session.get.side_effect = SQLAlchemyError("Database error")

    # Act
    result = category_dao.get_category_by_id(1)

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "Erro ao buscar categoria por ID" in captured.out


# ==================== TESTES: create_category ====================


def test_create_category_success(category_dao, mock_session):
    """Testa criação bem-sucedida de categoria"""
    # Arrange
    new_category = Category(id=1, name="Nova Categoria")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Mock para simular o comportamento do refresh
    def mock_refresh(obj):
        obj.id = 1

    mock_session.refresh.side_effect = mock_refresh

    # Act
    with patch("models.models.Category", return_value=new_category):
        result = category_dao.create_category("Nova Categoria")

    # Assert
    assert result is not None
    assert result.name == "Nova Categoria"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_create_category_integrity_error(category_dao, mock_session, capsys):
    """Testa criação de categoria com violação de integridade (ex: nome duplicado)"""
    # Arrange
    mock_session.commit.side_effect = IntegrityError("Duplicate entry", None, None)

    # Act
    result = category_dao.create_category("Categoria Duplicada")

    # Assert
    assert result is None
    mock_session.rollback.assert_called_once()
    captured = capsys.readouterr()
    assert "Erro de integridade ao criar categoria" in captured.out


def test_create_category_database_error(category_dao, mock_session, capsys):
    """Testa criação de categoria com erro genérico do banco"""
    # Arrange
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    # Act
    result = category_dao.create_category("Nova Categoria")

    # Assert
    assert result is None
    mock_session.rollback.assert_called_once()
    captured = capsys.readouterr()
    assert "Erro ao criar categoria" in captured.out


# ==================== TESTES: update_category ====================


def test_update_category_success(category_dao, mock_session, sample_category):
    """Testa atualização bem-sucedida de categoria"""
    # Arrange
    mock_session.get.return_value = sample_category
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Act
    result = category_dao.update_category(1, "Eletrônicos Atualizados")

    # Assert
    assert result is not None
    assert result.name == "Eletrônicos Atualizados"
    mock_session.get.assert_called_once_with(Category, 1)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_update_category_not_found(category_dao, mock_session, capsys):
    """Testa atualização de categoria inexistente"""
    # Arrange
    mock_session.get.return_value = None

    # Act
    result = category_dao.update_category(999, "Nome Novo")

    # Assert
    assert result is None
    captured = capsys.readouterr()
    assert "Categoria não encontrada" in captured.out
    mock_session.commit.assert_not_called()


def test_update_category_database_error(
    category_dao, mock_session, sample_category, capsys
):
    """Testa atualização com erro no banco de dados"""
    # Arrange
    mock_session.get.return_value = sample_category
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    # Act
    result = category_dao.update_category(1, "Nome Novo")

    # Assert
    assert result is None
    mock_session.rollback.assert_called_once()
    captured = capsys.readouterr()
    assert "Erro ao atualizar categoria" in captured.out


# ==================== TESTES: delete_category ====================


def test_delete_category_success(category_dao, mock_session, sample_category):
    """Testa remoção bem-sucedida de categoria"""
    # Arrange
    mock_session.get.return_value = sample_category
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    # Act
    result = category_dao.delete_category(1)

    # Assert
    assert result is True
    mock_session.get.assert_called_once_with(Category, 1)
    mock_session.delete.assert_called_once_with(sample_category)
    mock_session.commit.assert_called_once()


def test_delete_category_not_found(category_dao, mock_session, capsys):
    """Testa remoção de categoria inexistente"""
    # Arrange
    mock_session.get.return_value = None

    # Act
    result = category_dao.delete_category(999)

    # Assert
    assert result is False
    captured = capsys.readouterr()
    assert "Categoria não encontrada" in captured.out
    mock_session.delete.assert_not_called()


def test_delete_category_database_error(
    category_dao, mock_session, sample_category, capsys
):
    """Testa remoção com erro no banco de dados"""
    # Arrange
    mock_session.get.return_value = sample_category
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    # Act
    result = category_dao.delete_category(1)

    # Assert
    assert result is False
    mock_session.rollback.assert_called_once()
    captured = capsys.readouterr()
    assert "Erro ao remover categoria" in captured.out


# ==================== TESTES: close ====================


def test_close_session(category_dao, mock_session):
    """Testa fechamento da sessão"""
    # Act
    category_dao.close()

    # Assert
    mock_session.close.assert_called_once()


def test_close_session_with_none(category_dao):
    """Testa fechamento quando sessão é None"""
    # Arrange
    category_dao.session = None

    # Act & Assert (não deve lançar exceção)
    category_dao.close()


# ==================== TESTES DE INTEGRAÇÃO ====================


@pytest.mark.integration
def test_full_crud_workflow(category_dao, mock_session):
    """Testa fluxo completo de CRUD"""
    # Create
    new_category = Category(id=1, name="Test Category")
    with patch("models.models.Category", return_value=new_category):
        created = category_dao.create_category("Test Category")

    assert created is not None

    # Read
    mock_session.get.return_value = new_category
    found = category_dao.get_category_by_id(1)
    assert found.name == "Test Category"

    # Update
    updated = category_dao.update_category(1, "Updated Category")
    assert updated.name == "Updated Category"

    # Delete
    deleted = category_dao.delete_category(1)
    assert deleted is True


# ==================== TESTES PARAMETRIZADOS ====================


@pytest.mark.parametrize(
    "category_id,expected_calls", [(1, 1), (999, 1), (0, 1), (-1, 1)]
)
def test_get_category_by_id_various_ids(
    category_dao, mock_session, category_id, expected_calls
):
    """Testa busca por ID com diferentes valores"""
    # Arrange
    mock_session.get.return_value = None

    # Act
    category_dao.get_category_by_id(category_id)

    # Assert
    assert mock_session.get.call_count == expected_calls


@pytest.mark.parametrize(
    "name",
    [
        "Categoria Normal",
        "Categoria com Espaços   ",
        "123",
        "Categoria_com_underscore",
        "Catégoria com Açentos",
    ],
)
def test_create_category_various_names(category_dao, mock_session, name):
    """Testa criação de categorias com diferentes tipos de nomes"""
    # Arrange
    new_category = Category(id=1, name=name)

    # Act
    with patch("models.models.Category", return_value=new_category):
        result = category_dao.create_category(name)

    # Assert
    assert result is not None
    mock_session.add.assert_called()
    mock_session.commit.assert_called()
