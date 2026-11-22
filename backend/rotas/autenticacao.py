from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
#Liga os endereços da API ao controller.
from backend.banco_de_dados import get_db
from backend.esquemas.autenticacao import CadastroEntrada, LoginEntrada, UsuarioSaida, TokenSaida
from backend.controladores import autenticacao as controlador

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=UsuarioSaida, status_code=status.HTTP_201_CREATED)
def cadastro(dados: CadastroEntrada, db: Session = Depends(get_db)):
    return controlador.cadastrar(db, dados)


@router.post("/login", response_model=TokenSaida)
def login(dados: LoginEntrada, db: Session = Depends(get_db)):
    return controlador.entrar(db, dados.email, dados.senha)