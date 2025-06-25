import logging
import os

import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL do banco usando as configurações do docker-compose
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="biblioteca",
            user="postgres",
            password="postgres",
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
    required_tables = ["aluno", "livro", "exemplar", "emprestimo", "emp_exemplar"]
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
            # Divide o arquivo em comandos individuais e executa cada um
            commands = sql_commands.split(";")
            for command in commands:
                command = command.strip()
                if command:  # Ignora comandos vazios
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

    # Verifica conexão
    if not check_database_connection():
        logger.error(
            "Não foi possível conectar ao banco de dados. Verifique se o PostgreSQL está rodando."
        )
        return False

    # Verifica se todas as tabelas existem
    missing_tables = check_all_tables_exist()

    if not missing_tables:
        logger.info("Todas as tabelas já existem no banco de dados!")
        return True

    logger.info(f"Tabelas faltando: {missing_tables}")
    logger.info("Criando tabelas...")

    # Caminho para o arquivo SQL
    sql_file_path = os.path.join(os.path.dirname(__file__), "init_db.sql")

    if not os.path.exists(sql_file_path):
        logger.error(f"Arquivo SQL não encontrado: {sql_file_path}")
        return False

    # Executa o script SQL
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
