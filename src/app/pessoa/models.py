from sqlalchemy import Column, Integer, String

from src.app.database import Base


class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, primary_key=False, index=True)
    idade = Column(Integer, index=False)

