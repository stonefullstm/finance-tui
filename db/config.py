# config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do banco de dados
DB_PATH = "/var/lib/firebird/3.0/data/dbfinance/dbfinance.fdb"

# String de conexão com firebird-driver
# Formato: firebird+firebird://usuario:senha@host:porta/caminho/banco.fdb
DATABASE_URL = f"firebird+firebird://sysdba:masterkey@localhost:3050/{DB_PATH}"

# Criar engine com firebird-driver
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Mostra SQL no console
    pool_size=5,
    max_overflow=10,
    # Configurações específicas do firebird-driver
    connect_args={"charset": "UTF8"},
)

# Criar sessão
SessionLocal = sessionmaker(bind=engine)

# Base para os modelos declarativos
Base = declarative_base()


def get_db():
    """Função para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def testar_conexao():
    """Testa a conexão com o banco usando firebird-driver"""
    try:
        from firebird.driver import connect

        # Teste direto com firebird-driver
        conn = connect(
            database=f"localhost/3050:{DB_PATH}",
            user="sysdba",
            password="masterkey",
            charset="UTF8",
        )
        conn.close()
        print("✓ Conexão com firebird-driver estabelecida!")
        return True
    except Exception as e:
        print(f"✗ Erro na conexão com firebird-driver: {e}")
        return False
