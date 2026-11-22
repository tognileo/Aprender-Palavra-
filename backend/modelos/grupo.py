from sqlalchemy import Column, Integer, String, ForeignKey
from backend.banco_de_dados import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # nicho_id vazio (None) = grupo Básico, que vale para os dois nichos
    nicho_id = Column(Integer, ForeignKey("nichos.id"), nullable=True)
    nome = Column(String(100), nullable=False)
    ordem = Column(Integer, nullable=False)