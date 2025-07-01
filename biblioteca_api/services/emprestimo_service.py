import logging
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.aluno import Aluno
from ..models.emprestimo import Emprestimo

logger = logging.getLogger(__name__)


class EmprestimoService:
    @staticmethod
    def get_all_emprestimos(db: Session, skip: int = 0, limit: int = 100) -> List[Emprestimo]:
        try:
            emprestimos = db.query(Emprestimo).offset(skip).limit(limit).all()
            return emprestimos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar empréstimos: {e}")
            return []

    @staticmethod
    def get_emprestimo_by_cod(db: Session, cod: int) -> Optional[Emprestimo]:
        try:
            emprestimo = db.session.get(Emprestimo, cod)
            return emprestimo
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empréstimo por código {cod}: {e}")
            return None

    @staticmethod
    def create_emprestimo(
        db: Session,
        mat_aluno: int,
        data_emprestimo: date,
        data_prevista_dev: date,
    ) -> Optional[Emprestimo]:
        try:
            aluno = db.session.get(Aluno, mat_aluno)
            if not aluno:
                logger.warning(f"Aluno com matrícula {mat_aluno} não encontrado")
                return None

            new_emprestimo = Emprestimo(
                mat_aluno=mat_aluno,
                data_emprestimo=data_emprestimo,
                data_prevista_dev=data_prevista_dev,
            )
            db.add(new_emprestimo)
            db.commit()
            db.refresh(new_emprestimo)
            logger.info(f"Empréstimo criado com sucesso: {new_emprestimo.COD}")
            return new_emprestimo
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar empréstimo: {e}")
            db.rollback()
            return None

    @staticmethod
    def update_emprestimo(
        db: Session,
        cod: int,
        mat_aluno: Optional[int] = None,
        data_emprestimo: Optional[date] = None,
        data_prevista_dev: Optional[date] = None,
        data_devolucao: Optional[date] = None,
        data_atraso: Optional[date] = None,
    ) -> Optional[Emprestimo]:
        try:
            emprestimo = db.session.get(Emprestimo, cod)
            if not emprestimo:
                logger.warning(f"Empréstimo com código {cod} não encontrado")
                return None

            if mat_aluno is not None:
                aluno = db.session.get(Aluno, mat_aluno)
                if not aluno:
                    logger.warning(f"Aluno com matrícula {mat_aluno} não encontrado")
                    return None
                emprestimo.mat_aluno = mat_aluno
            if data_emprestimo is not None:
                emprestimo.data_emprestimo = data_emprestimo
            if data_prevista_dev is not None:
                emprestimo.data_prevista_dev = data_prevista_dev
            if data_devolucao is not None:
                emprestimo.data_devolucao = data_devolucao
            if data_atraso is not None:
                emprestimo.data_atraso = data_atraso

            db.commit()
            db.refresh(emprestimo)
            logger.info(f"Empréstimo {cod} atualizado com sucesso")
            return emprestimo
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar empréstimo {cod}: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete_emprestimo(db: Session, cod: int) -> bool:
        try:
            emprestimo = db.session.get(Emprestimo, cod)
            if not emprestimo:
                logger.warning(f"Empréstimo com código {cod} não encontrado")
                return False

            db.delete(emprestimo)
            db.commit()
            logger.info(f"Empréstimo {cod} deletado com sucesso")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar empréstimo {cod}: {e}")
            db.rollback()
            return False

    @staticmethod
    def return_emprestimo(db: Session, cod: int) -> Optional[Emprestimo]:
        try:
            emprestimo = db.session.get(Emprestimo, cod)
            if not emprestimo:
                logger.warning(f"Empréstimo com código {cod} não encontrado")
                return None

            if emprestimo.DATA_DEVOLUCAO:
                logger.warning(f"Empréstimo {cod} já foi devolvido")
                return None

            emprestimo.DATA_DEVOLUCAO = datetime.now().date()
            if emprestimo.DATA_DEVOLUCAO > emprestimo.DATA_PREVISTA_DEV:
                emprestimo.DATA_ATRASO = emprestimo.DATA_DEVOLUCAO

            db.commit()
            db.refresh(emprestimo)
            logger.info(f"Empréstimo {cod} devolvido com sucesso")
            return emprestimo
        except SQLAlchemyError as e:
            logger.error(f"Erro ao devolver empréstimo {cod}: {e}")
            db.rollback()
            return None

    @staticmethod
    def get_emprestimos_by_aluno(db: Session, mat_aluno: int) -> List[Emprestimo]:
        try:
            aluno = db.session.get(Aluno, mat_aluno)
            if not aluno:
                logger.warning(f"Aluno com matrícula {mat_aluno} não encontrado")
                return []
            emprestimos = db.query(Emprestimo).filter(Emprestimo.MAT_ALUNO == mat_aluno).all()
            return emprestimos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar empréstimos para o aluno {mat_aluno}: {e}")
            return []