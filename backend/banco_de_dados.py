from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

import sys
from pathlib import Path

# Põe a pasta raiz do projeto no caminho do Python. Assim o "from backend..." funciona
# em qualquer jeito de rodar (botão Play do VS Code, de dentro da pasta, ou com -m).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.configuracao import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Monta o endereço do banco. O URL.create trata símbolos na senha sozinho.
url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
    query={"charset": "utf8mb4"},
)

# O engine é a conexão com o banco
engine = create_engine(url, pool_pre_ping=True)

# Cada requisição do site vai abrir uma sessão e fechar no final
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Todos os models (as tabelas em Python) vão herdar desta classe
Base = declarative_base()


def get_db():
    """Entrega uma sessão para a rota e fecha ao terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Teste rápido: roda só quando você executa este arquivo diretamente
# (python -m backend.banco_de_dados, na raiz do projeto, ou o botão Play)
if __name__ == "__main__":
    with engine.connect() as conexao:
        tabelas = [linha[0] for linha in conexao.execute(text("SHOW TABLES"))]
        print("Conectou! Tabelas encontradas:", tabelas)