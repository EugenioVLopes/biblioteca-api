# Sistema de Biblioteca - API

Este projeto implementa uma API para gerenciamento de biblioteca com banco de dados PostgreSQL e documentação automática usando Flask-RESTX/Swagger.

## 📋 Pré-requisitos

- Docker e Docker Compose
- Python 3.8+
- pip (gerenciador de pacotes do Python)

## 🚀 Configuração e Inicialização

### Opção 1: Script Automático (Recomendado)

#### No Linux/Mac:

```bash
chmod +x start.sh
./start.sh
```

### Opção 2: Configuração Manual

1. **Inicie o PostgreSQL:**

   ```bash
   docker-compose up -d
   ```

2. **Instale as dependências Python:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Inicialize o banco de dados:**
   ```bash
   python -c "from db import initialize_database; initialize_database()"
   ```

## 🗄️ Estrutura do Banco de Dados

O sistema cria automaticamente as seguintes tabelas:

### ALUNO

- `MAT_ALUNO` (INTEGER) - Matrícula (PK, Auto-incremento)
- `NOME` (VARCHAR(100)) - Nome do aluno
- `EMAIL` (VARCHAR(100)) - Email
- `CURSO` (VARCHAR(100)) - Curso

### LIVRO

- `COD` (INTEGER) - Código do livro (PK, Auto-incremento)
- `TITULO` (VARCHAR(200)) - Título
- `AUTOR` (VARCHAR(100)) - Autor
- `EDITORA` (VARCHAR(100)) - Editora
- `ANO` (INTEGER) - Ano de publicação

### EXEMPLAR

- `TOMBO` (INTEGER) - Número do tombo (PK, Auto-incremento)
- `COD_LIVRO` (INTEGER) - Código do livro (FK)

### EMPRESTIMO

- `COD` (INTEGER) - Código do empréstimo (PK)
- `MAT_ALUNO` (INTEGER) - Matrícula do aluno (FK)
- `DATA_EMPRESTIMO` (DATE) - Data do empréstimo
- `DATA_PREVISTA_DEV` (DATE) - Data prevista de devolução
- `DATA_DEVOLUCAO` (DATE) - Data real de devolução
- `DATA_ATRASO` (DATE) - Data de atraso

### EMP_EXEMPLAR

- `COD_EMPRESTIMO` (INTEGER) - Código do empréstimo (FK)
- `TOMBO_EXEMPLAR` (INTEGER) - Tombo do exemplar (FK)

## 📚 Documentação da API

A API possui documentação automática gerada pelo Flask-RESTX/Swagger. Após iniciar a aplicação, você pode acessar:

- **Documentação Swagger UI:** `http://localhost:5000/docs`
- **Especificação OpenAPI:** `http://localhost:5000/swagger.json`

### Endpoints Disponíveis

A API está organizada em namespaces:

- **`/alunos`** - Gerenciamento de alunos
- **`/livros`** - Gerenciamento de livros
- **`/exemplares`** - Gerenciamento de exemplares
- **`/emprestimos`** - Gerenciamento de empréstimos
- **`/emprestimo-exemplares`** - Relacionamento entre empréstimos e exemplares

## 🔧 Scripts Disponíveis

### `db.py`

Script Python que:

- Verifica conexão com o banco de dados
- Checa se todas as tabelas existem
- Cria as tabelas faltantes automaticamente
- Fornece logs detalhados do processo

### `init_db.sql`

Arquivo SQL com os comandos CREATE TABLE para todas as tabelas do sistema.

## 🐳 Comandos Docker Úteis

```bash
# Iniciar o PostgreSQL
docker-compose up -d

# Parar o PostgreSQL
docker-compose down

# Ver logs do PostgreSQL
docker-compose logs postgres

# Conectar ao PostgreSQL via psql
docker exec -it biblioteca-db psql -U postgres -d biblioteca
```

## 📊 Configurações do Banco

- **Host:** localhost
- **Porta:** 5432
- **Banco:** biblioteca
- **Usuário:** postgres
- **Senha:** postgres

## ⚡ Verificação Rápida

Para verificar se tudo está funcionando:

1. Execute `python -c "from db import initialize_database; initialize_database()"`
2. Se você ver "✅ Todas as tabelas já existem no banco de dados!", está tudo configurado
3. Se você ver "🎉 Banco de dados inicializado com sucesso!", as tabelas foram criadas
4. Inicie a aplicação: `python run.py`
5. Acesse a documentação: `http://localhost:5000/docs`

## 🔍 Troubleshooting

### Erro de conexão com banco

- Verifique se o Docker está rodando: `docker ps`
- Reinicie o PostgreSQL: `docker-compose restart`

### Erro de dependências Python

- Instale as dependências: `pip install -r requirements.txt`
- Ou instale manualmente: `pip install psycopg2-binary sqlalchemy`

### Tabelas não são criadas

- Verifique as permissões do usuário postgres
- Verifique os logs: `docker-compose logs postgres`
