import os

from flask import Flask, jsonify
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api(
    version="1.0",
    title="API Biblioteca",
    description="API para gerenciamento de biblioteca com sistema de empréstimos",
    doc="/docs",
    authorizations={
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Digite 'Bearer <jwt_token>'",
        }
    },
    security="apikey",
    mask_swagger=False,
)


def create_app():
    app = Flask(__name__)
    # Definindo configurações diretamente
    app.config["DEBUG"] = os.environ.get("FLASK_DEBUG") == "1"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api.init_app(app)

    # Register namespaces
    from .controllers.aluno_controller import alunos_ns
    from .controllers.emprestimo_controller import emprestimos_ns
    from .controllers.emprestimo_exemplar_controller import emprestimo_exemplares_ns
    from .controllers.exemplar_controller import exemplares_ns
    from .controllers.livro_controller import livros_ns

    api.add_namespace(alunos_ns)
    api.add_namespace(emprestimos_ns)
    api.add_namespace(emprestimo_exemplares_ns)
    api.add_namespace(exemplares_ns)
    api.add_namespace(livros_ns)

    from .models import swagger_models

    with app.app_context():
        db.create_all()

    # Handler para erro 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Rota não encontrada"}), 404

    return app


app = create_app()
