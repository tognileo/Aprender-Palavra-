import os
from pathlib import Path
from dotenv import load_dotenv

# Procura o arquivo .env na raiz do projeto (uma pasta acima de backend)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "15"))

# Se faltar alguma configuração, avisa logo, com o nome da que falta
for nome in ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "JWT_SECRET"):
    if not os.getenv(nome):
        raise RuntimeError(f"Falta a configuração {nome} no arquivo .env")