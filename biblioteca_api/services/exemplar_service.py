import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.exemplar import Exemplar
from ..models.livro import Livro

logger = logging.getLogger(__name__)


class ExemplarService:
    @staticmethod
    def get_all_exemplares(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Exemplar]:
        try:
            exemplares = db.query(Exemplar).offset(skip).limit(limit).all()
            return exemplares
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar exemplares: {e}")
            return []

    @staticmethod
    def get_exemplar_by_tombo(db: Session, tombo: int) -> Optional[Exemplar]:
        try:
            exemplar = db.query(Exemplar).filter(Exemplar.TOMBO == tombo).first()
            return exemplar
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar exemplar por tombo {tombo}: {e}")
            return None

    @staticmethod
    def create_exemplar(db: Session, cod_livro: int) -> Optional[Exemplar]:
        try:
            livro = db.query(Livro).filter(Livro.COD == cod_livro).first()
            if not livro:
                logger.warning(f"Livro com código {cod_livro} não encontrado")
                return None

            new_exemplar = Exemplar(COD_LIVRO=cod_livro)
            db.add(new_exemplar)
            db.commit()
            db.refresh(new_exemplar)
            logger.info(f"Exemplar criado com sucesso: {new_exemplar.TOMBO}")
            return new_exemplar
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar exemplar: {e}")
            db.rollback()
            return None

    @staticmethod
    def update_exemplar(
        db: Session, tombo: int, cod_livro: Optional[int] = None
    ) -> Optional[Exemplar]:
        try:
            exemplar = db.query(Exemplar).filter(Exemplar.TOMBO == tombo).first()
            if not exemplar:
                logger.warning(f"Exemplar com tombo {tombo} não encontrado")
                return None

            if cod_livro is not None:
                livro = db.query(Livro).filter(Livro.COD == cod_livro).first()
                if not livro:
                    logger.warning(f"Livro com código {cod_livro} não encontrado")
                    return None
                exemplar.COD_LIVRO = cod_livro

            db.commit()
            db.refresh(exemplar)
            logger.info(f"Exemplar {tombo} atualizado com sucesso")
            return exemplar
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar exemplar {tombo}: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete_exemplar(db: Session, tombo: int) -> bool:
        try:
            exemplar = db.query(Exemplar).filter(Exemplar.TOMBO == tombo).first()
            if not exemplar:
                logger.warning(f"Exemplar com tombo {tombo} não encontrado")
                return False

            db.delete(exemplar)
            db.commit()
            logger.info(f"Exemplar {tombo} deletado com sucesso")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar exemplar {tombo}: {e}")
            db.rollback()
            return False

    @staticmethod
    def get_exemplares_by_livro(db: Session, cod_livro: int) -> List[Exemplar]:
        try:
            exemplares = (
                db.query(Exemplar).filter(Exemplar.COD_LIVRO == cod_livro).all()
            )
            return exemplares
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar exemplares para o livro {cod_livro}: {e}")
            return []
