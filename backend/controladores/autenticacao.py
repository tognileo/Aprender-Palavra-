from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
#É O CONTROLER:LIGICA DE CADASTRAR E ENTRAR
from backend.modelos import Nicho, Usuario
from backend.esquemas.autenticacao import CadastroEntrada
from backend.seguranca import gerar_hash, verificar_senha, criar_token


def cadastrar(db: Session, dados: CadastroEntrada) -> Usuario:
    """Cria a conta. O nicho escolhido não pode ser trocado depois."""
    if db.query(Nicho).filter(Nicho.id == dados.nicho_id).first() is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Motivo da viagem inválido.")

    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Este e-mail já está cadastrado.")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash(dados.senha),  # guarda só a senha criptografada
        nicho_id=dados.nicho_id,
    )
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:
        # Duas pessoas cadastrando o mesmo e-mail ao mesmo tempo
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Este e-mail já está cadastrado.")
    db.refresh(usuario)
    return usuario


def entrar(db: Session, email: str, senha: str) -> dict:
    """Confere e-mail e senha e devolve o token."""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    # A mesma mensagem para e-mail errado e senha errada (não revela qual foi)
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha incorretos.")

    return {"access_token": criar_token(usuario.id), "token_type": "bearer", "nome": usuario.nome}