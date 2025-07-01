#!/bin/bash

# Script para inicializar o banco de dados da biblioteca
# Este script verifica se o Docker está rodando, inicia o PostgreSQL e inicializa o banco

echo "🚀 Inicializando o sistema da biblioteca..."

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verifica se o docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não encontrado. Por favor, instale o docker-compose primeiro."
    exit 1
fi

echo "🐳 Iniciando o PostgreSQL com Docker..."

# Inicia o PostgreSQL
docker-compose up -d

echo "⏳ Aguardando o PostgreSQL inicializar..."
sleep 10

# Verifica se o Python está instalado
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python não encontrado. Por favor, instale o Python primeiro."
        exit 1
    else
        PYTHON_CMD="python3"
    fi
else
    PYTHON_CMD="python"
fi

echo "📦 Instalando dependências Python..."

# Instala as dependências se o requirements.txt existir
if [ -f "requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r requirements.txt
else
    echo "⚠️  Arquivo requirements.txt não encontrado. Instalando dependências manualmente..."
    $PYTHON_CMD -m pip install psycopg2-binary sqlalchemy
fi

echo "🔧 Inicializando o banco de dados..."

# Executa o script de inicialização
$PYTHON_CMD init_database.py

echo "✅ Setup completo!"
echo "💡 Para parar o PostgreSQL: docker-compose down"
echo "💡 Para ver os logs: docker-compose logs postgres"
