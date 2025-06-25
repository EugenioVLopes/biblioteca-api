@echo off
echo 🚀 Inicializando o sistema da biblioteca...

REM Verifica se o Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado. Por favor, instale o Docker primeiro.
    pause
    exit /b 1
)

REM Verifica se o docker-compose está instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose não encontrado. Por favor, instale o docker-compose primeiro.
    pause
    exit /b 1
)

echo 🐳 Iniciando o PostgreSQL com Docker...

REM Inicia o PostgreSQL
docker-compose up -d

echo ⏳ Aguardando o PostgreSQL inicializar...
timeout /t 10 /nobreak >nul

REM Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado. Por favor, instale o Python primeiro.
    pause
    exit /b 1
)

echo 📦 Instalando dependências Python...

REM Instala as dependências se o requirements.txt existir
if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo ⚠️  Arquivo requirements.txt não encontrado. Instalando dependências manualmente...
    python -m pip install psycopg2-binary sqlalchemy
)

echo 🔧 Inicializando o banco de dados...

REM Executa o script de inicialização
python init_database.py

echo ✅ Setup completo!
echo 💡 Para parar o PostgreSQL: docker-compose down
echo 💡 Para ver os logs: docker-compose logs postgres
pause
