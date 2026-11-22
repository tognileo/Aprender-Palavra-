from sqlalchemy import Column, Integer, String, ForeignKey
from backend.banco_de_dados import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)  # nunca a senha pura
    nicho_id = Column(Integer, ForeignKey("nichos.id"), nullable=False)