import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.livro import Livro

logger = logging.getLogger(__name__)


class LivroService:
    @staticmethod
    def get_all_livros(db: Session, skip: int = 0, limit: int = 100) -> List[Livro]:
        try:
            livros = db.query(Livro).offset(skip).limit(limit).all()
            return livros
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar livros: {e}")
            return []

    @staticmethod
    def get_livro_by_id(db: Session, cod: int) -> Optional[Livro]:
        try:
            livro = db.get(Livro, cod)
            return livro
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar livro por código {cod}: {e}")
            return None

    @staticmethod
    def create_livro(
        db: Session,
        TITULO: str,
        AUTOR: str,
        EDITORA: Optional[str] = None,
        ANO: Optional[int] = None,
    ) -> Optional[Livro]:
        try:
            new_livro = Livro(TITULO=TITULO, AUTOR=AUTOR, EDITORA=EDITORA, ANO=ANO)
            db.add(new_livro)
            db.commit()
            db.refresh(new_livro)
            logger.info(f"Livro criado com sucesso: {new_livro.COD}")
            return new_livro
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar livro: {e}")
            db.rollback()
            return None

    @staticmethod
    def update_livro(
        db: Session,
        cod: int,
        TITULO: Optional[str] = None,
        AUTOR: Optional[str] = None,
        EDITORA: Optional[str] = None,
        ANO: Optional[int] = None,
    ) -> Optional[Livro]:
        try:
            livro = db.get(Livro, cod)
            if not livro:
                logger.warning(f"Livro com código {cod} não encontrado")
                return None

            if TITULO is not None:
                livro.TITULO = TITULO
            if AUTOR is not None:
                livro.AUTOR = AUTOR
            if EDITORA is not None:
                livro.EDITORA = EDITORA
            if ANO is not None:
                livro.ANO = ANO

            db.commit()
            db.refresh(livro)
            logger.info(f"Livro {cod} atualizado com sucesso")
            return livro
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar livro {cod}: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete_livro(db: Session, cod: int) -> bool:
        try:
            livro = db.get(Livro, cod)
            if not livro:
                logger.warning(f"Livro com código {cod} não encontrado")
                return False

            db.delete(livro)
            db.commit()
            logger.info(f"Livro {cod} deletado com sucesso")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar livro {cod}: {e}")
            db.rollback()
            return False

    @staticmethod
    def search_livros(
        db: Session, TITULO: Optional[str] = None, AUTOR: Optional[str] = None
    ) -> List[Livro]:
        try:
            query = db.query(Livro)
            if TITULO:
                query = query.filter(Livro.TITULO.ilike(f"%{TITULO}%"))
            if AUTOR:
                query = query.filter(Livro.AUTOR.ilike(f"%{AUTOR}%"))
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar livros: {e}")
            return []
