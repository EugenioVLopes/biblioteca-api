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
        mat: str,
        nome: str,
        email: Optional[str] = None,
        curso: Optional[str] = None,
    ) -> Optional[Aluno]:
        """
        Cria um novo aluno no banco de dados

        Args:
            db: Sessão do banco de dados
            mat: Matrícula do aluno (chave primária)
            nome: Nome do aluno
            email: Email do aluno (opcional)
            curso: Curso do aluno (opcional)

        Returns:
            Objeto Aluno criado ou None em caso de erro
        """
        try:
            aluno_existente = AlunoService.buscar_por_matricula(db, mat)

            if aluno_existente:
                logger.warning(f"Aluno com matrícula {mat} já existe")
                return None

            novo_aluno = Aluno(mat=mat, nome=nome, email=email, curso=curso)

            db.add(novo_aluno)
            db.commit()
            db.refresh(novo_aluno)

            logger.info(f"Aluno criado com sucesso: {mat}")
            return novo_aluno

        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar aluno: {e}")
            db.rollback()
            return None

    @staticmethod
    def buscar_por_matricula(db: Session, mat: str) -> Optional[Aluno]:
        """
        Busca um aluno pela matrícula

        Args:
            db: Sessão do banco de dados
            mat: Matrícula do aluno

        Returns:
            Objeto Aluno encontrado ou None
        """
        try:
            aluno = db.query(Aluno).filter(Aluno.mat == mat).first()
            return aluno
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar aluno por matrícula {mat}: {e}")
            return None

    @staticmethod
    def buscar_por_email(db: Session, email: str) -> Optional[Aluno]:
        """
        Busca um aluno pelo email

        Args:
            db: Sessão do banco de dados
            email: Email do aluno

        Returns:
            Objeto Aluno encontrado ou None
        """
        try:
            aluno = db.query(Aluno).filter(Aluno.email == email).first()
            return aluno
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar aluno por email {email}: {e}")
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
    def buscar_por_nome(db: Session, nome: str) -> List[Aluno]:
        """
        Busca alunos por nome (busca parcial, case-insensitive)

        Args:
            db: Sessão do banco de dados
            nome: Nome ou parte do nome para buscar

        Returns:
            Lista de objetos Aluno que correspondem à busca
        """
        try:
            alunos = db.query(Aluno).filter(Aluno.nome.ilike(f"%{nome}%")).all()
            return alunos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar alunos por nome {nome}: {e}")
            return []

    @staticmethod
    def buscar_por_curso(db: Session, curso: str) -> List[Aluno]:
        """
        Busca alunos por curso

        Args:
            db: Sessão do banco de dados
            curso: Curso para buscar

        Returns:
            Lista de objetos Aluno do curso especificado
        """
        try:
            alunos = db.query(Aluno).filter(Aluno.curso == curso).all()
            return alunos
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar alunos por curso {curso}: {e}")
            return []

    @staticmethod
    def atualizar_aluno(
        db: Session,
        mat: str,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        curso: Optional[str] = None,
    ) -> Optional[Aluno]:
        """
        Atualiza os dados de um aluno

        Args:
            db: Sessão do banco de dados
            mat: Matrícula do aluno a ser atualizado
            nome: Novo nome (opcional)
            email: Novo email (opcional)
            curso: Novo curso (opcional)

        Returns:
            Objeto Aluno atualizado ou None em caso de erro
        """
        try:
            aluno = AlunoService.buscar_por_matricula(db, mat)
            if not aluno:
                logger.warning(f"Aluno com matrícula {mat} não encontrado")
                return None

            # Atualiza apenas os campos fornecidos
            if nome is not None:
                aluno.nome = nome
            if email is not None:
                aluno.email = email
            if curso is not None:
                aluno.curso = curso

            db.commit()
            db.refresh(aluno)

            logger.info(f"Aluno {mat} atualizado com sucesso")
            return aluno

        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar aluno {mat}: {e}")
            db.rollback()
            return None

    @staticmethod
    def deletar_aluno(db: Session, mat: str) -> bool:
        """
        Deleta um aluno do banco de dados

        Args:
            db: Sessão do banco de dados
            mat: Matrícula do aluno a ser deletado

        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            aluno = AlunoService.buscar_por_matricula(db, mat)
            if not aluno:
                logger.warning(f"Aluno com matrícula {mat} não encontrado")
                return False

            db.delete(aluno)
            db.commit()

            logger.info(f"Aluno {mat} deletado com sucesso")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar aluno {mat}: {e}")
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
    def aluno_existe(db: Session, mat: str) -> bool:
        """
        Verifica se um aluno existe pelo matrícula

        Args:
            db: Sessão do banco de dados
            mat: Matrícula do aluno

        Returns:
            True se o aluno existe, False caso contrário
        """
        try:
            count = db.query(Aluno).filter(Aluno.mat == mat).count()
            return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Erro ao verificar se aluno {mat} existe: {e}")
            return False
