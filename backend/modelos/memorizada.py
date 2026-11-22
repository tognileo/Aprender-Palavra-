from sqlalchemy import Column, Integer, ForeignKey
from backend.banco_de_dados import Base


class Memorizada(Base):
    __tablename__ = "memorizadas"

    # Existe linha = a expressão está em "Já memorizadas"
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    expressao_id = Column(Integer, ForeignKey("expressoes.id", ondelete="CASCADE"), primary_key=True)