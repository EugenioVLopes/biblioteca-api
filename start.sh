#!/bin/bash

# Script para inicializar o ambiente de desenvolvimento da API da biblioteca
# Este script inicia os contêineres Docker e aguarda a inicialização do banco de dados.

echo "🚀 Inicializando o ambiente de desenvolvimento..."

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

echo "🐳 Iniciando os contêineres Docker (PostgreSQL e API)..."

# Inicia os contêineres em modo detached
docker-compose up -d --build

echo "⏳ Aguardando o PostgreSQL e a API inicializarem..."
sleep 15

echo "🔧 Verificando a inicialização do banco de dados..."

# A inicialização do banco de dados é feita pela aplicação ao iniciar.
# Vamos verificar os logs para confirmar que a API está rodando.
docker-compose logs biblioteca-api

echo "✅ Ambiente de desenvolvimento iniciado com sucesso!"
echo "💡 A API está rodando em http://localhost:5000/docs"
echo "💡 Para ver os logs da API: docker-compose logs -f biblioteca-api"
echo "💡 Para ver os logs do banco de dados: docker-compose logs -f postgres"
echo "💡 Para parar os contêineres: docker-compose down"
