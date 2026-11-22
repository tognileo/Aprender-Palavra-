from typing import Optional

from pydantic import BaseModel


class NichoSaida(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}


class GrupoSaida(BaseModel):
    id: int
    nome: str
    ordem: int

    model_config = {"from_attributes": True}


class ExpressaoSaida(BaseModel):
    id: int
    ingles: str
    portugues: str
    pronuncia: str
    ordem: int
    audio: Optional[str] = None
    memorizada: bool  # True = aba "Já memorizadas", False = aba "Para estudar"
