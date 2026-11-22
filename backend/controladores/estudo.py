from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.modelos import Nicho, Grupo, Expressao, Memorizada, Usuario


def listar_nichos(db: Session):
    """Os nichos para a tela de cadastro (motivo da viagem)."""
    return db.query(Nicho).order_by(Nicho.id).all()


def listar_grupos(db: Session, usuario: Usuario):
    """O Básico (nicho vazio) e os grupos do nicho da pessoa, na ordem."""
    return (
        db.query(Grupo)
        .filter(or_(Grupo.nicho_id.is_(None), Grupo.nicho_id == usuario.nicho_id))
        .order_by(Grupo.ordem)
        .all()
    )


def _buscar_grupo_permitido(db: Session, usuario: Usuario, grupo_id: int) -> Grupo:
    """Acha o grupo, mas só se for o Básico ou do nicho da pessoa.
    Grupo de outro nicho responde 'não encontrado', como se não existisse."""
    grupo = (
        db.query(Grupo)
        .filter(
            Grupo.id == grupo_id,
            or_(Grupo.nicho_id.is_(None), Grupo.nicho_id == usuario.nicho_id),
        )
        .first()
    )
    if grupo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Grupo não encontrado.")
    return grupo


def expressoes_do_grupo(db: Session, usuario: Usuario, grupo_id: int):
    """As expressões do grupo, da mais importante para a menos importante,
    com a marca de quais a pessoa já memorizou."""
    _buscar_grupo_permitido(db, usuario, grupo_id)

    linhas = (
        db.query(Expressao, Memorizada.expressao_id)
        .outerjoin(
            Memorizada,
            and_(
                Memorizada.expressao_id == Expressao.id,
                Memorizada.usuario_id == usuario.id,
            ),
        )
        .filter(Expressao.grupo_id == grupo_id)
        .order_by(Expressao.ordem)
        .all()
    )
    return [
        {
            "id": e.id,
            "ingles": e.ingles,
            "portugues": e.portugues,
            "pronuncia": e.pronuncia,
            "ordem": e.ordem,
            "audio": e.audio,
            "memorizada": memorizada_id is not None,
        }
        for e, memorizada_id in linhas
    ]


def _buscar_expressao_permitida(db: Session, usuario: Usuario, expressao_id: int) -> Expressao:
    """Acha a expressão, mas só se o grupo dela for permitido para a pessoa."""
    expressao = db.query(Expressao).filter(Expressao.id == expressao_id).first()
    if expressao is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expressão não encontrada.")
    _buscar_grupo_permitido(db, usuario, expressao.grupo_id)
    return expressao


def memorizar(db: Session, usuario: Usuario, expressao_id: int) -> None:
    """Botão 'Já memorizei': cria a linha em memorizadas (se ainda não existir)."""
    _buscar_expressao_permitida(db, usuario, expressao_id)
    ja_existe = (
        db.query(Memorizada)
        .filter(Memorizada.usuario_id == usuario.id, Memorizada.expressao_id == expressao_id)
        .first()
    )
    if ja_existe:
        return
    db.add(Memorizada(usuario_id=usuario.id, expressao_id=expressao_id))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # clique duplo: a linha já foi criada, está tudo certo


def desmemorizar(db: Session, usuario: Usuario, expressao_id: int) -> None:
    """Devolve a expressão para 'Para estudar': apaga a linha de memorizadas."""
    _buscar_expressao_permitida(db, usuario, expressao_id)
    db.query(Memorizada).filter(
        Memorizada.usuario_id == usuario.id, Memorizada.expressao_id == expressao_id
    ).delete()
    db.commit()
