from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Aluno(Base):
    __tablename__ = "aluno"
    matricula = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    curso = Column(String, nullable=False)
