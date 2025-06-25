from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Aluno(Base):
    __tablename__ = "ALUNO"
    mat = Column(String(20), primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100))
    curso = Column(String(100))
