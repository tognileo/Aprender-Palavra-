"""
usuario_logado.py: descobre quem é a pessoa logada a partir do token.
As rotas protegidas usam: usuario = Depends(get_usuario_atual)
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.banco_de_dados import get_db
from backend.modelos import Usuario
from backend.seguranca import ler_token

# Lê o cabeçalho "Authorization: Bearer <token>" enviado pelo navegador
esquema_bearer = HTTPBearer(auto_error=False)


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    erro = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Sessão inválida ou expirada. Faça login novamente.",
    )
    if credenciais is None:
        raise erro

    usuario_id = ler_token(credenciais.credentials)
    if usuario_id is None:
        raise erro

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise erro
    return usuario
