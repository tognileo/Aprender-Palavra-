from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from backend.banco_de_dados import Base


class Expressao(Base):
    __tablename__ = "expressoes"
    __table_args__ = (UniqueConstraint("grupo_id", "ingles", name="uq_expressoes_grupo_ingles"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    ingles = Column(String(255), nullable=False)
    portugues = Column(String(255), nullable=False)
    pronuncia = Column(String(255), nullable=False)
    ordem = Column(Integer, nullable=False)   # importância dentro do grupo (1 = mais importante)
    audio = Column(String(255), nullable=True)  # começa vazio