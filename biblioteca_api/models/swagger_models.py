from flask_restx import fields

# Importar api do módulo principal
from .. import api

# Modelos para documentação Swagger

# Modelo para Aluno
aluno_model = api.model(
    "Aluno",
    {
        "MAT_ALUNO": fields.String(
            readonly=True, description="Matrícula única do aluno"
        ),
        "NOME": fields.String(required=True, description="Nome completo do aluno"),
        "EMAIL": fields.String(required=True, description="Email do aluno"),
        "CURSO": fields.String(description="Curso do aluno"),
    },
)

aluno_response_model = api.model(
    "AlunoResponse",
    {
        "MAT_ALUNO": fields.String(
            readonly=True, description="Matrícula única do aluno"
        ),
        "NOME": fields.String(description="Nome completo do aluno"),
        "EMAIL": fields.String(description="Email do aluno"),
        "CURSO": fields.String(description="Curso do aluno"),
    },
)

# Modelo para Livro
livro_model = api.model(
    "Livro",
    {
        "COD": fields.Integer(readonly=True, description="Código único do livro"),
        "TITULO": fields.String(required=True, description="Título do livro"),
        "AUTOR": fields.String(required=True, description="Autor do livro"),
        "EDITORA": fields.String(description="Editora do livro"),
        "ANO": fields.Integer(description="Ano de publicação"),
    },
)

# Modelo para Exemplar
exemplar_model = api.model(
    "Exemplar",
    {
        "TOMBO": fields.Integer(
            readonly=True, description="Número do tombo do exemplar"
        ),
        "COD_LIVRO": fields.Integer(required=True, description="Código do livro"),
    },
)

# Modelo para Empréstimo
emprestimo_model = api.model(
    "Emprestimo",
    {
        "COD": fields.Integer(readonly=True, description="Código único do empréstimo"),
        "MAT_ALUNO": fields.Integer(required=True, description="Matrícula do aluno"),
        "DATA_EMPRESTIMO": fields.Date(required=True, description="Data do empréstimo"),
        "DATA_PREVISTA_DEV": fields.Date(
            required=True, description="Data prevista de devolução"
        ),
        "DATA_DEVOLUCAO": fields.Date(description="Data real de devolução"),
        "DATA_ATRASO": fields.Date(description="Data de atraso"),
    },
)

emprestimo_create_model = api.model(
    "EmprestimoCreate",
    {
        "MAT_ALUNO": fields.Integer(required=True, description="Matrícula do aluno"),
    },
)

# Modelo para Empréstimo Exemplar
emprestimo_exemplar_model = api.model(
    "EmprestimoExemplar",
    {
        "COD_EMPRESTIMO": fields.Integer(
            required=True, description="Código do empréstimo"
        ),
        "TOMBO_EXEMPLAR": fields.Integer(
            required=True, description="Tombo do exemplar"
        ),
    },
)

# Modelos para mensagens de erro
error_model = api.model(
    "Error", {"error": fields.String(description="Mensagem de erro")}
)

message_model = api.model(
    "Message", {"message": fields.String(description="Mensagem de sucesso")}
)

# Modelos para listas
alunos_list_model = api.model(
    "AlunosList",
    {
        "alunos": fields.List(
            fields.Nested(aluno_response_model), description="Lista de alunos"
        )
    },
)

livros_list_model = api.model(
    "LivrosList",
    {"livros": fields.List(fields.Nested(livro_model), description="Lista de livros")},
)

exemplares_list_model = api.model(
    "ExemplaresList",
    {
        "exemplares": fields.List(
            fields.Nested(exemplar_model), description="Lista de exemplares"
        )
    },
)

emprestimos_list_model = api.model(
    "EmprestimosList",
    {
        "emprestimos": fields.List(
            fields.Nested(emprestimo_model), description="Lista de empréstimos"
        )
    },
)
