from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#ONDE LIGA TUDO E INICIA O SERVIDOR
import sys
from pathlib import Path

# Põe a pasta raiz do projeto no caminho do Python. Assim o "from backend..." funciona
# em qualquer jeito de rodar (botão Play do VS Code, de dentro da pasta, ou com -m).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.rotas import autenticacao, estudo

app = FastAPI(title="Aprender Palavras")

# Como o frontend é separado, o navegador só deixa ele falar com a API
# se a API disser quais endereços são permitidos (CORS).
# 5500 é a porta do "Go Live" do VS Code. Quando publicar, acrescente o endereço do site.
ORIGENS_PERMITIDAS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_methods=["*"],
    allow_headers=["*"],  # inclui o cabeçalho Authorization do token
)

app.include_router(autenticacao.router)
app.include_router(estudo.router)
