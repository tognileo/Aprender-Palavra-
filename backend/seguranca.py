"""
seguranca.py: senha criptografada (Argon2) e token de login (JWT).
"""
from datetime import datetime, timedelta, timezone
#CUIDA DA SEGURANÇA DO SITE. GUARDAR SENHA PROTEGIDA COM O HASH#TMB CRIA O TOKEN DE LOGIN
import jwt
from pwdlib import PasswordHash

from backend.configuracao import JWT_SECRET, JWT_EXPIRE_MINUTES

ALGORITMO = "HS256"

# Objeto que sabe criptografar e conferir senhas (usa Argon2)
_hasher = PasswordHash.recommended()


def gerar_hash(senha: str) -> str:
    """Transforma a senha em um texto criptografado, para guardar no banco."""
    return _hasher.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere se a senha digitada bate com a criptografada do banco."""
    return _hasher.verify(senha, senha_hash)


def criar_token(usuario_id: int) -> str:
    """Cria o token de login, com o id do usuário e a validade."""
    agora = datetime.now(timezone.utc)
    dados = {
        "sub": str(usuario_id),  # "sub" = de quem é o token (precisa ser texto)
        "iat": agora,  # quando foi criado
        "exp": agora + timedelta(minutes=JWT_EXPIRE_MINUTES),  # quando expira
    }
    return jwt.encode(dados, JWT_SECRET, algorithm=ALGORITMO)


def ler_token(token: str):
    """Devolve o id do usuário se o token for válido. Se for falso, adulterado
    ou expirado, devolve None."""
    try:
        dados = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITMO])
        return int(dados["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None