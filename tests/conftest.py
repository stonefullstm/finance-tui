"""
Configurações globais do pytest para testes de integração e unitários.
Aqui podemos definir fixtures, marcadores personalizados e outras
configurações que serão usadas em todos os testes.
"""

import pytest

# from unittest.mock import MagicMock


def pytest_configure(config):
    """Registra marcadores customizados"""
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "unit: marca testes unitários")
    config.addinivalue_line("markers", "slow: marca testes que demoram para executar")


@pytest.fixture(scope="session")
def db_config():
    """Configurações de banco de dados para testes"""
    return {"database": "test_db", "echo": False, "pool_size": 5}
