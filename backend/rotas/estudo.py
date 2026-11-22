from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.controladores import estudo as controlador
from backend.banco_de_dados import get_db
from backend.usuario_logado import get_usuario_atual
from backend.modelos import Usuario
from backend.esquemas.estudo import NichoSaida, GrupoSaida, ExpressaoSaida

router = APIRouter(tags=["Estudo"])


@router.get("/nichos", response_model=List[NichoSaida])
def nichos(db: Session = Depends(get_db)):
    return controlador.listar_nichos(db)


@router.get("/grupos", response_model=List[GrupoSaida])
def grupos(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    return controlador.listar_grupos(db, usuario)


@router.get("/grupos/{grupo_id}/expressoes", response_model=List[ExpressaoSaida])
def expressoes(
    grupo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    return controlador.expressoes_do_grupo(db, usuario, grupo_id)


@router.post("/expressoes/{expressao_id}/memorizar", status_code=status.HTTP_204_NO_CONTENT)
def memorizar(
    expressao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    controlador.memorizar(db, usuario, expressao_id)


@router.delete("/expressoes/{expressao_id}/memorizar", status_code=status.HTTP_204_NO_CONTENT)
def desmemorizar(
    expressao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    controlador.desmemorizar(db, usuario, expressao_id)
