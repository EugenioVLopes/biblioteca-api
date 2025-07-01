from flask import request
from flask_restx import Namespace, Resource

from .. import db
from ..models.livro import Livro
from ..models.swagger_models import error_model, livro_model, message_model
from ..services.livro_service import LivroService

livros_ns = Namespace("Livros", description="Operações relacionadas a livros")


@livros_ns.route("/")
class LivrosList(Resource):
    @livros_ns.doc("listar_livros")
    @livros_ns.marshal_list_with(livro_model)
    def get(self):
        """Lista todos os livros"""
        livros = LivroService.get_all_livros(db.session)
        return [livro.to_dict() for livro in livros]

    @livros_ns.doc("criar_livro")
    @livros_ns.expect(livro_model)
    @livros_ns.marshal_with(livro_model, code=201)
    @livros_ns.response(500, "Erro interno do servidor", error_model)
    def post(self):
        """Cria um novo livro"""
        data = request.get_json()
        try:
            new_livro = LivroService.create_livro(
                db=db.session,
                TITULO=data["TITULO"],
                AUTOR=data["AUTOR"],
                EDITORA=data.get("EDITORA"),
                ANO=data.get("ANO"),
            )
            if new_livro:
                return new_livro.to_dict(), 201
            else:
                livros_ns.abort(500, "Erro ao criar livro")
        except Exception as e:
            livros_ns.abort(500, f"Erro ao criar livro: {str(e)}")


@livros_ns.route("/<int:COD>")
@livros_ns.param("COD", "Código do livro")
class LivroResource(Resource):
    @livros_ns.doc("obter_livro")
    @livros_ns.marshal_with(livro_model)
    @livros_ns.response(404, "Livro não encontrado", error_model)
    def get(self, COD):
        """Obtém um livro pelo código"""
        livro = LivroService.get_livro_by_id(db.session, COD)
        if livro is None:
            livros_ns.abort(404, "Livro não encontrado")
        return livro.to_dict()

    @livros_ns.doc("atualizar_livro")
    @livros_ns.expect(livro_model)
    @livros_ns.marshal_with(livro_model)
    @livros_ns.response(404, "Livro não encontrado", error_model)
    @livros_ns.response(500, "Erro interno do servidor", error_model)
    def put(self, COD):
        """Atualiza um livro existente"""
        data = request.get_json()
        try:
            updated_livro = LivroService.update_livro(
                db=db.session,
                cod=COD,
                TITULO=data.get("TITULO"),
                AUTOR=data.get("AUTOR"),
                EDITORA=data.get("EDITORA"),
                ANO=data.get("ANO"),
            )
            if updated_livro:
                return updated_livro.to_dict()
            else:
                livros_ns.abort(404, "Livro não encontrado")
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise
            livros_ns.abort(500, f"Erro ao atualizar livro: {str(e)}")

    @livros_ns.doc("deletar_livro")
    @livros_ns.marshal_with(message_model)
    @livros_ns.response(404, "Livro não encontrado", error_model)
    @livros_ns.response(500, "Erro interno do servidor", error_model)
    def delete(self, COD):
        """Deleta um livro existente"""
        try:
            success = LivroService.delete_livro(db.session, COD)
            if success:
                return {"message": "Livro deletado com sucesso"}
            else:
                livros_ns.abort(404, "Livro não encontrado")
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise
            livros_ns.abort(500, f"Erro ao deletar livro: {str(e)}")


@livros_ns.route("/buscar")
class LivroBusca(Resource):
    @livros_ns.doc("buscar_livros")
    @livros_ns.marshal_list_with(livro_model)
    def get(self):
        """Busca livros por título ou autor"""
        TITULO = request.args.get("TITULO", "")
        AUTOR = request.args.get("AUTOR", "")

        livros = LivroService.search_livros(
            db=db.session,
            TITULO=TITULO if TITULO else None,
            AUTOR=AUTOR if AUTOR else None,
        )
        return [livro.to_dict() for livro in livros]
