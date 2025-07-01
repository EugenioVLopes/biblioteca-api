import logging
import os

import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_connection_params():
    """Extrai parâmetros de conexão da DATABASE_URL"""
    if DATABASE_URL.startswith("postgresql://"):
        url_parts = DATABASE_URL.replace("postgresql://", "").split("@")
        if len(url_parts) == 2:
            auth_part = url_parts[0]
            host_part = url_parts[1]

            if ":" in auth_part:
                user, password = auth_part.split(":", 1)
            else:
                user, password = auth_part, ""

            if ":" in host_part:
                host_port, database = host_part.split("/", 1)
                if ":" in host_port:
                    host, port = host_port.split(":")
                else:
                    host, port = host_port, "5432"
            else:
                host, port, database = (
                    host_part.split("/", 1)[0],
                    "5432",
                    host_part.split("/", 1)[1],
                )

            return {
                "host": host,
                "port": port,
                "database": database,
                "user": user,
                "password": password,
            }

    return {
        "host": "localhost",
        "port": "5432",
        "database": "biblioteca",
        "user": "postgres",
        "password": "postgres",
    }


def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        params = get_connection_params()
        connection = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            database=params["database"],
            user=params["user"],
            password=params["password"],
        )
        connection.close()
        logger.info("Conexão com o banco de dados estabelecida com sucesso!")
        return True
    except psycopg2.Error as e:
        logger.error(f"Erro ao conectar com o banco de dados: {e}")
        return False


def table_exists(table_name):
    """Verifica se uma tabela existe no banco de dados"""
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = :table_name
                    );
                """
                ),
                {"table_name": table_name.lower()},
            )
            return result.scalar()
    except SQLAlchemyError as e:
        logger.error(f"Erro ao verificar se a tabela {table_name} existe: {e}")
        return False


def check_all_tables_exist():
    """Verifica se todas as tabelas necessárias existem"""
    required_tables = [
        "aluno",
        "livro",
        "exemplar",
        "emprestimo",
        "emprestimo_exemplar",
    ]
    missing_tables = []

    for table in required_tables:
        if not table_exists(table):
            missing_tables.append(table)

    return missing_tables


def execute_sql_file(file_path):
    """Executa um arquivo SQL"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            sql_commands = file.read()

        with engine.connect() as connection:
            commands = sql_commands.split(";")
            for command in commands:
                command = command.strip()
                if command:
                    connection.execute(text(command))
            connection.commit()

        logger.info(f"Arquivo SQL {file_path} executado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao executar arquivo SQL {file_path}: {e}")
        return False


def initialize_database():
    """Inicializa o banco de dados criando as tabelas se necessário"""
    logger.info("Iniciando verificação do banco de dados...")

    if not check_database_connection():
        logger.error(
            "Não foi possível conectar ao banco de dados. Verifique se o PostgreSQL está rodando."
        )
        return False

    missing_tables = check_all_tables_exist()

    if not missing_tables:
        logger.info("Todas as tabelas já existem no banco de dados!")
        return True

    logger.info(f"Tabelas faltando: {missing_tables}")
    logger.info("Criando tabelas...")

    sql_file_path = os.path.join(os.path.dirname(__file__), "..", "init_db.sql")

    if not os.path.exists(sql_file_path):
        logger.error(f"Arquivo SQL não encontrado: {sql_file_path}")
        return False

    if execute_sql_file(sql_file_path):
        logger.info("Banco de dados inicializado com sucesso!")
        return True
    else:
        logger.error("Falha ao inicializar o banco de dados!")
        return False


def get_db():
    """Função para obter uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_connection():
    """Retorna uma conexão direta com o banco de dados"""
    params = get_connection_params()
    return psycopg2.connect(
        host=params["host"],
        port=params["port"],
        database=params["database"],
        user=params["user"],
        password=params["password"],
        cursor_factory=psycopg2.extras.DictCursor,
    )
