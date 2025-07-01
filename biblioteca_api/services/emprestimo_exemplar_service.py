import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.emprestimo import Emprestimo
from ..models.emprestimo_exemplar import EmprestimoExemplar
from ..models.exemplar import Exemplar

logger = logging.getLogger(__name__)


class EmprestimoExemplarService:
    @staticmethod
    def get_all_emprestimo_exemplares(db: Session, skip: int = 0, limit: int = 100) -> List[EmprestimoExemplar]:
        try:
            emprestimo_exemplares = db.query(EmprestimoExemplar).offset(skip).limit(limit).all()
            return emprestimo_exemplares
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar empréstimo exemplares: {e}")
            return []

    @staticmethod
    def get_emprestimo_exemplar_by_ids(
        db: Session, cod_emprestimo: int, tombo_exemplar: int
    ) -> Optional[EmprestimoExemplar]:
        try:
            emprestimo_exemplar = (
                db.query(EmprestimoExemplar)
                .filter_by(cod_emprestimo=cod_emprestimo, tombo_exemplar=tombo_exemplar)
                .first()
            )
            return emprestimo_exemplar
        except SQLAlchemyError as e:
            logger.error(
                f"Erro ao buscar empréstimo exemplar com cod_emprestimo {cod_emprestimo} e tombo_exemplar {tombo_exemplar}: {e}"
            )
            return None

    @staticmethod
    def create_emprestimo_exemplar(
        db: Session, cod_emprestimo: int, tombo_exemplar: int
    ) -> Optional[EmprestimoExemplar]:
        try:
            emprestimo = db.session.get(Emprestimo, cod_emprestimo)
            if not emprestimo:
                logger.warning(f"Empréstimo com código {cod_emprestimo} não encontrado")
                return None

            exemplar = db.session.get(Exemplar, tombo_exemplar)
            if not exemplar:
                logger.warning(f"Exemplar com tombo {tombo_exemplar} não encontrado")
                return None

            new_emprestimo_exemplar = EmprestimoExemplar(
                cod_emprestimo=cod_emprestimo, tombo_exemplar=tombo_exemplar
            )
            db.add(new_emprestimo_exemplar)
            db.commit()
            db.refresh(new_emprestimo_exemplar)
            logger.info(
                f"Empréstimo exemplar criado com sucesso: {new_emprestimo_exemplar.cod_emprestimo}, {new_emprestimo_exemplar.tombo_exemplar}"
            )
            return new_emprestimo_exemplar
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar empréstimo exemplar: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete_emprestimo_exemplar(
        db: Session, cod_emprestimo: int, tombo_exemplar: int
    ) -> bool:
        try:
            emprestimo_exemplar = (
                db.query(EmprestimoExemplar)
                .filter_by(cod_emprestimo=cod_emprestimo, tombo_exemplar=tombo_exemplar)
                .first()
            )
            if not emprestimo_exemplar:
                logger.warning(
                    f"Empréstimo exemplar com cod_emprestimo {cod_emprestimo} e tombo_exemplar {tombo_exemplar} não encontrado"
                )
                return False

            db.delete(emprestimo_exemplar)
            db.commit()
            logger.info(
                f"Empréstimo exemplar {cod_emprestimo}, {tombo_exemplar} deletado com sucesso"
            )
            return True
        except SQLAlchemyError as e:
            logger.error(
                f"Erro ao deletar empréstimo exemplar {cod_emprestimo}, {tombo_exemplar}: {e}"
            )
            db.rollback()
            return False

    @staticmethod
    def get_exemplares_by_emprestimo(db: Session, cod_emprestimo: int) -> List[EmprestimoExemplar]:
        try:
            emprestimo = db.session.get(Emprestimo, cod_emprestimo)
            if not emprestimo:
                logger.warning(f"Empréstimo com código {cod_emprestimo} não encontrado")
                return []
            emprestimo_exemplares = db.query(EmprestimoExemplar).filter(EmprestimoExemplar.cod_emprestimo == cod_emprestimo).all()
            return emprestimo_exemplares
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar exemplares para o empréstimo {cod_emprestimo}: {e}")
            return []

    @staticmethod
    def get_emprestimos_by_exemplar(db: Session, tombo_exemplar: int) -> List[EmprestimoExemplar]:
        try:
            exemplar = db.session.get(Exemplar, tombo_exemplar)
            if not exemplar:
                logger.warning(f"Exemplar com tombo {tombo_exemplar} não encontrado")
                return []
            emprestimo_exemplares = db.query(EmprestimoExemplar).filter(EmprestimoExemplar.tombo_exemplar == tombo_exemplar).all()
            return emprestimo_exemplares
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empréstimos para o exemplar {tombo_exemplar}: {e}")
            return []