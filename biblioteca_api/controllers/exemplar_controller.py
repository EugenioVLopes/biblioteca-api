from flask import make_response, request
from flask_restx import Namespace, Resource

from .. import db
from ..models.exemplar import Exemplar
from ..models.livro import Livro
from ..models.swagger_models import error_model, exemplar_model, message_model
from ..services.exemplar_service import ExemplarService

exemplares_ns = Namespace(
    "Exemplares", description="Operações relacionadas a exemplares"
)


def error_response(msg, code):
    return make_response({"error": msg}, code)


@exemplares_ns.route("/")
class ExemplaresList(Resource):
    @exemplares_ns.doc("listar_exemplares")
    @exemplares_ns.marshal_list_with(exemplar_model)
    def get(self):
        """Lista todos os exemplares"""
        exemplares = ExemplarService.get_all_exemplares(db.session)
        return [exemplar.to_dict() for exemplar in exemplares]

    @exemplares_ns.doc("criar_exemplar")
    @exemplares_ns.expect(exemplar_model)
    @exemplares_ns.response(201, "Exemplar criado", exemplar_model)
    @exemplares_ns.response(400, "Livro não encontrado", error_model)
    @exemplares_ns.response(500, "Erro interno do servidor", error_model)
    def post(self):
        """Cria um novo exemplar"""
        data = request.get_json()

        if not data or "COD_LIVRO" not in data:
            return error_response("COD_LIVRO é obrigatório", 400)

        new_exemplar = ExemplarService.create_exemplar(db.session, data["COD_LIVRO"])
        if not new_exemplar:
            return error_response("Livro não encontrado", 400)

        return new_exemplar.to_dict(), 201


@exemplares_ns.route("/<int:TOMBO>")
@exemplares_ns.param("TOMBO", "Número do tombo do exemplar")
class ExemplarResource(Resource):
    @exemplares_ns.doc("obter_exemplar")
    @exemplares_ns.response(200, "Exemplar encontrado", exemplar_model)
    @exemplares_ns.response(404, "Exemplar não encontrado", error_model)
    def get(self, TOMBO):
        """Obtém um exemplar pelo tombo"""
        exemplar = ExemplarService.get_exemplar_by_tombo(db.session, TOMBO)
        if exemplar is None:
            return error_response("Exemplar não encontrado", 404)
        return exemplar.to_dict(), 200

    @exemplares_ns.doc("atualizar_exemplar")
    @exemplares_ns.expect(exemplar_model)
    @exemplares_ns.response(200, "Exemplar atualizado", exemplar_model)
    @exemplares_ns.response(404, "Exemplar não encontrado", error_model)
    @exemplares_ns.response(400, "Livro não encontrado", error_model)
    @exemplares_ns.response(500, "Erro interno do servidor", error_model)
    def put(self, TOMBO):
        """Atualiza um exemplar existente"""
        data = request.get_json()

        if not data or "COD_LIVRO" not in data:
            return error_response("COD_LIVRO é obrigatório", 400)

        updated_exemplar = ExemplarService.update_exemplar(
            db.session, TOMBO, data["COD_LIVRO"]
        )
        if not updated_exemplar:
            return error_response("Exemplar não encontrado", 404)

        return updated_exemplar.to_dict(), 200

    @exemplares_ns.doc("deletar_exemplar")
    @exemplares_ns.response(200, "Exemplar deletado", message_model)
    @exemplares_ns.response(404, "Exemplar não encontrado", error_model)
    @exemplares_ns.response(500, "Erro interno do servidor", error_model)
    def delete(self, TOMBO):
        """Deleta um exemplar existente"""
        success = ExemplarService.delete_exemplar(db.session, TOMBO)
        if not success:
            return error_response("Exemplar não encontrado", 404)

        return {"message": "Exemplar deletado com sucesso"}, 200


@exemplares_ns.route("/livro/<int:COD_LIVRO>")
@exemplares_ns.param("COD_LIVRO", "Código do livro")
class ExemplaresPorLivro(Resource):
    @exemplares_ns.doc("listar_exemplares_por_livro")
    @exemplares_ns.response(200, "Exemplares encontrados", exemplar_model)
    @exemplares_ns.response(404, "Livro não encontrado", error_model)
    def get(self, COD_LIVRO):
        """Lista todos os exemplares de um livro específico"""
        # Verificar se o livro existe
        livro = db.session.query(Livro).filter(Livro.COD == COD_LIVRO).first()
        if not livro:
            return error_response("Livro não encontrado", 404)

        exemplares = ExemplarService.get_exemplares_by_livro(db.session, COD_LIVRO)
        return [exemplar.to_dict() for exemplar in exemplares], 200
