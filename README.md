# Biblioteca API

## Descrição

API RESTful desenvolvida com NestJS para gerenciamento de biblioteca, permitindo operações CRUD para livros, usuários e empréstimos.

Este projeto foi desenvolvido como trabalho para a disciplina de Banco de Dados do Departamento de Computação e Automação (DCA) da Universidade Federal do Rio Grande do Norte (UFRN).

## Tecnologias Utilizadas

- NestJS
- TypeScript
- Node.js
- PostgreSQL (banco de dados)
- Docker

## Configuração do Projeto

```bash
# Instalar dependências
$ npm install

# Configurar variáveis de ambiente
$ cp .env.example .env
```

## Banco de Dados

O projeto utiliza PostgreSQL como banco de dados, que pode ser executado facilmente usando Docker Compose:

```bash
# Iniciar o banco de dados
$ docker-compose up -d

# Parar o banco de dados
$ docker-compose down
```

Configurações do banco de dados:
- Host: localhost
- Porta: 5432
- Usuário: postgres
- Senha: postgres
- Nome do banco: biblioteca

## Executando o Projeto

```bash
# desenvolvimento
$ npm run start

# modo watch
$ npm run start:dev

# modo produção
$ npm run start:prod
```

## Testes

```bash
# testes unitários
$ npm run test

# testes e2e
$ npm run test:e2e

# cobertura de testes
$ npm run test:cov
```

## Estrutura do Projeto

```
src/
├── livros/           # Módulo de livros
├── usuarios/           # Módulo de usuários
├── emprestimos/           # Módulo de empréstimos
├── common/          # Recursos compartilhados
└── main.ts          # Ponto de entrada da aplicação
```

## Documentação da API

A documentação completa da API está disponível através do Swagger UI quando o servidor estiver em execução:

```
http://localhost:3000/api
```