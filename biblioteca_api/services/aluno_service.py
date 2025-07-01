import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.aluno import Aluno

logger = logging.getLogger(__name__)


class AlunoService:
    """Serviço para operações CRUD da entidade Aluno"""

    @staticmethod
    def criar_aluno(
        db: Session,
        MAT_ALUNO: int,
        NOME: str,
        EMAIL: Optional[str] = None,
        CURSO: Optional[str] = None,
    ) -> Optional[Aluno]:
        """
        Cria um novo aluno no banco de dados

        Args:
            db: Sessão do banco de dados
            MAT_ALUNO: Matrícula do aluno (chave primária)
            NOME: Nome do aluno
            EMAIL: Email do aluno (opcional)
            CURSO: Curso do aluno (opcional)

        Returns:
            Objeto Aluno criado ou None em caso de erro
        """
        try:
            aluno_existente = AlunoService.buscar_por_matricula(db, MAT_ALUNO)

            if aluno_existente:
                logger.warning(f"Aluno com matrícula {MAT_ALUNO} já existe")
                return None

            novo_aluno = Aluno(MAT_ALUNO=MAT_ALUNO, NOME=NOME, EMAIL=EMAIL, CURSO=CURSO)

            db.add(novo_aluno)
            db.commit()
            db.refresh(novo_aluno)

            logger.info(f"Aluno criado com sucesso: {MAT_ALUNO}")
            return novo_aluno

        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar aluno: {e}")
            db.rollback()
            return None

    @staticmethod
    def buscar_por_matricula(db: Session, MAT_ALUNO: int) -> Optional[Aluno]:
        """
        Busca um aluno pela matrícula

        Args:
            db: Sessão do banco de dados
            MAT_ALUNO: Matrícula do aluno

        Returns:
            Objeto Aluno encontrado ou None
        """
        try:
            aluno = db.query(Aluno).filter(Aluno.MAT_ALUNO == MAT_ALUNO).first()
            return aluno
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar aluno por matrícula {MAT_ALUNO}: {e}")
            return None

    @staticmethod
    def buscar_por_email(db: Session, EMAIL: str) -> Optional[Aluno]:
        """
        Busca um aluno pelo email

        Args:
            db: Sessão do banco de dados
            EMAIL: Email do aluno

        Returns:
            Objeto Aluno encontrado ou None
        """
        try:
            aluno = db.query(Aluno).filter(Aluno.EMAIL == EMAIL).first()
            return aluno
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar aluno por email {EMAIL}: {e}")
            return None

    @staticmethod
    def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """
        Lista todos os alunos com paginação

        Args:
            db: Sessão do banco de dados
            skip: Número de registros para pular (paginação)
            limit: Número máximo de registros para retornar

        Returns:
            Lista de objetos Aluno
        """
        try:
            alunos = db.query(Aluno).offset(skip).limit(limit).all()
            return alunos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar alunos: {e}")
            return []

    @staticmethod
    def buscar_por_nome(db: Session, NOME: str) -> List[Aluno]:
        """
        Busca alunos por nome (busca parcial, case-insensitive)

        Args:
            db: Sessão do banco de dados
            NOME: Nome ou parte do nome para buscar

        Returns:
            Lista de objetos Aluno que correspondem à busca
        """
        try:
            alunos = db.query(Aluno).filter(Aluno.NOME.ilike(f"%{NOME}%")).all()
            return alunos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar alunos por nome {NOME}: {e}")
            return []

    @staticmethod
    def buscar_por_curso(db: Session, CURSO: str) -> List[Aluno]:
        """
        Busca alunos por curso

        Args:
            db: Sessão do banco de dados
            CURSO: Curso para buscar

        Returns:
            Lista de objetos Aluno do curso especificado
        """
        try:
            alunos = db.query(Aluno).filter(Aluno.CURSO == CURSO).all()
            return alunos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar alunos por curso {CURSO}: {e}")
            return []

    @staticmethod
    def atualizar_aluno(
        db: Session,
        MAT_ALUNO: int,
        NOME: Optional[str] = None,
        EMAIL: Optional[str] = None,
        CURSO: Optional[str] = None,
    ) -> Optional[Aluno]:
        """
        Atualiza os dados de um aluno

        Args:
            db: Sessão do banco de dados
            MAT_ALUNO: Matrícula do aluno a ser atualizado
            NOME: Novo nome (opcional)
            EMAIL: Novo email (opcional)
            CURSO: Novo curso (opcional)

        Returns:
            Objeto Aluno atualizado ou None em caso de erro
        """
        try:
            aluno = AlunoService.buscar_por_matricula(db, MAT_ALUNO)
            if not aluno:
                logger.warning(f"Aluno com matrícula {MAT_ALUNO} não encontrado")
                return None

            # Atualiza apenas os campos fornecidos
            if NOME is not None:
                aluno.NOME = NOME
            if EMAIL is not None:
                aluno.EMAIL = EMAIL
            if CURSO is not None:
                aluno.CURSO = CURSO

            db.commit()
            db.refresh(aluno)

            logger.info(f"Aluno {MAT_ALUNO} atualizado com sucesso")
            return aluno

        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar aluno {MAT_ALUNO}: {e}")
            db.rollback()
            return None

    @staticmethod
    def deletar_aluno(db: Session, MAT_ALUNO: int) -> bool:
        """
        Deleta um aluno do banco de dados

        Args:
            db: Sessão do banco de dados
            MAT_ALUNO: Matrícula do aluno a ser deletado

        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            aluno = AlunoService.buscar_por_matricula(db, MAT_ALUNO)
            if not aluno:
                logger.warning(f"Aluno com matrícula {MAT_ALUNO} não encontrado")
                return False

            db.delete(aluno)
            db.commit()

            logger.info(f"Aluno {MAT_ALUNO} deletado com sucesso")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar aluno {MAT_ALUNO}: {e}")
            db.rollback()
            return False

    @staticmethod
    def contar_alunos(db: Session) -> int:
        """
        Conta o número total de alunos no banco de dados

        Args:
            db: Sessão do banco de dados

        Returns:
            Número total de alunos
        """
        try:
            count = db.query(Aluno).count()
            return count
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar alunos: {e}")
            return 0

    @staticmethod
    def aluno_existe(db: Session, MAT_ALUNO: int) -> bool:
        """
        Verifica se um aluno existe pelo matrícula

        Args:
            db: Sessão do banco de dados
            MAT_ALUNO: Matrícula do aluno

        Returns:
            True se o aluno existe, False caso contrário
        """
        try:
            count = db.query(Aluno).filter(Aluno.MAT_ALUNO == MAT_ALUNO).count()
            return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Erro ao verificar se aluno {MAT_ALUNO} existe: {e}")
            return False
