from sqlalchemy import Column, Integer, String
from backend.banco_de_dados import Base


class Nicho(Base):
    __tablename__ = "nichos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)