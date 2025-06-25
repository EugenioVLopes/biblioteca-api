#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da biblioteca.
Este script verifica se as tabelas existem e as cria caso necessário.
"""

import logging
import os
import sys

import psycopg2

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configurações do banco de dados (conforme docker-compose.yaml)
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "biblioteca",
    "user": "postgres",
    "password": "postgres",
}


def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        connection.close()
        logger.info("✅ Conexão com o banco de dados estabelecida com sucesso!")
        return True
    except psycopg2.Error as e:
        logger.error(f"❌ Erro ao conectar com o banco de dados: {e}")
        logger.error("Verifique se o PostgreSQL está rodando (docker-compose up)")
        return False


def table_exists(cursor, table_name):
    """Verifica se uma tabela existe no banco de dados"""
    try:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """,
            (table_name.lower(),),
        )
        return cursor.fetchone()[0]
    except psycopg2.Error as e:
        logger.error(f"Erro ao verificar se a tabela {table_name} existe: {e}")
        return False


def check_all_tables_exist():
    """Verifica se todas as tabelas necessárias existem"""
    required_tables = ["aluno", "livro", "exemplar", "emprestimo", "emp_exemplar"]
    missing_tables = []

    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for table in required_tables:
            if not table_exists(cursor, table):
                missing_tables.append(table)

        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        logger.error(f"Erro ao verificar tabelas: {e}")
        return required_tables  # Assume que todas estão faltando se der erro

    return missing_tables


def execute_sql_file(file_path):
    """Executa um arquivo SQL"""
    try:
        # Lê o arquivo SQL
        with open(file_path, "r", encoding="utf-8") as file:
            sql_commands = file.read()

        # Conecta ao banco e executa
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Executa o script completo
        cursor.execute(sql_commands)
        connection.commit()

        cursor.close()
        connection.close()

        logger.info(f"✅ Arquivo SQL {file_path} executado com sucesso!")
        return True

    except FileNotFoundError:
        logger.error(f"❌ Arquivo SQL não encontrado: {file_path}")
        return False
    except psycopg2.Error as e:
        logger.error(f"❌ Erro ao executar arquivo SQL {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        return False


def main():
    """Função principal"""
    logger.info("🔍 Iniciando verificação do banco de dados da biblioteca...")

    # Verifica conexão
    if not check_database_connection():
        logger.error("❌ Não foi possível conectar ao banco de dados.")
        logger.info("💡 Dica: Execute 'docker-compose up -d' para iniciar o PostgreSQL")
        sys.exit(1)

    # Verifica se todas as tabelas existem
    missing_tables = check_all_tables_exist()

    if not missing_tables:
        logger.info("✅ Todas as tabelas já existem no banco de dados!")
        logger.info("🎉 O banco de dados está pronto para uso!")
        return

    logger.info(f"⚠️  Tabelas faltando: {missing_tables}")
    logger.info("🔧 Criando tabelas...")

    # Caminho para o arquivo SQL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(script_dir, "init_db.sql")

    # Executa o script SQL
    if execute_sql_file(sql_file_path):
        logger.info("🎉 Banco de dados inicializado com sucesso!")
        logger.info("✅ Todas as tabelas foram criadas!")

        # Verifica novamente para confirmar
        missing_tables_after = check_all_tables_exist()
        if not missing_tables_after:
            logger.info("✅ Verificação final: Todas as tabelas estão presentes!")
        else:
            logger.warning(f"⚠️  Ainda há tabelas faltando: {missing_tables_after}")
    else:
        logger.error("❌ Falha ao inicializar o banco de dados!")
        sys.exit(1)


if __name__ == "__main__":
    main()
