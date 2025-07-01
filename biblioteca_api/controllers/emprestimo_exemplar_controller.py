from flask import request
from flask_restx import Namespace, Resource

from .. import db
from ..models.emprestimo import Emprestimo
from ..models.emprestimo_exemplar import EmprestimoExemplar
from ..models.exemplar import Exemplar
from ..models.swagger_models import (
    emprestimo_exemplar_model,
    error_model,
    message_model,
)

emprestimo_exemplares_ns = Namespace(
    "Emprestimo-exemplares",
    description="Operações relacionadas a empréstimo de exemplares",
)


@emprestimo_exemplares_ns.route("/")
class EmprestimoExemplaresList(Resource):
    @emprestimo_exemplares_ns.doc("listar_emprestimo_exemplares")
    @emprestimo_exemplares_ns.marshal_list_with(emprestimo_exemplar_model)
    def get(self):
        """Lista todos os exemplares de empréstimos"""
        emprestimo_exemplares = EmprestimoExemplar.query.all()
        return [ee.to_dict() for ee in emprestimo_exemplares]

    @emprestimo_exemplares_ns.doc("criar_emprestimo_exemplar")
    @emprestimo_exemplares_ns.expect(emprestimo_exemplar_model)
    @emprestimo_exemplares_ns.marshal_with(emprestimo_exemplar_model, code=201)
    @emprestimo_exemplares_ns.response(
        400, "Empréstimo ou exemplar não encontrado", error_model
    )
    @emprestimo_exemplares_ns.response(500, "Erro interno do servidor", error_model)
    def post(self):
        """Adiciona um exemplar a um empréstimo"""
        data = request.get_json()

        # Verificar se o empréstimo existe
        emprestimo = db.session.get(Emprestimo, data["COD_EMPRESTIMO"])
        if not emprestimo:
            emprestimo_exemplares_ns.abort(400, "Empréstimo não encontrado")

        # Verificar se o exemplar existe
        exemplar = db.session.get(Exemplar, data["TOMBO_EXEMPLAR"])
        if not exemplar:
            emprestimo_exemplares_ns.abort(400, "Exemplar não encontrado")

        # Verificar se o exemplar já está em outro empréstimo ativo
        emprestimo_ativo = (
            EmprestimoExemplar.query.filter_by(tombo_exemplar=data["TOMBO_EXEMPLAR"])
            .join(Emprestimo)
            .filter(Emprestimo.DATA_DEVOLUCAO.is_(None))
            .first()
        )

        if emprestimo_ativo:
            emprestimo_exemplares_ns.abort(400, "Exemplar já está emprestado")

        try:
            new_emprestimo_exemplar = EmprestimoExemplar(
                cod_emprestimo=data["COD_EMPRESTIMO"],
                tombo_exemplar=data["TOMBO_EXEMPLAR"],
            )
            db.session.add(new_emprestimo_exemplar)
            db.session.commit()
            return new_emprestimo_exemplar.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            emprestimo_exemplares_ns.abort(
                500, f"Erro ao adicionar exemplar ao empréstimo: {str(e)}"
            )
        finally:
            db.session.close()


@emprestimo_exemplares_ns.route("/<int:COD_EMPRESTIMO>/<int:TOMBO_EXEMPLAR>")
@emprestimo_exemplares_ns.param("COD_EMPRESTIMO", "Código do empréstimo")
@emprestimo_exemplares_ns.param("TOMBO_EXEMPLAR", "Tombo do exemplar")
class EmprestimoExemplarResource(Resource):
    @emprestimo_exemplares_ns.doc("obter_emprestimo_exemplar")
    @emprestimo_exemplares_ns.marshal_with(emprestimo_exemplar_model)
    @emprestimo_exemplares_ns.response(
        404, "Empréstimo exemplar não encontrado", error_model
    )
    def get(self, COD_EMPRESTIMO, TOMBO_EXEMPLAR):
        """Obtém um exemplar de empréstimo específico"""
        emprestimo_exemplar = EmprestimoExemplar.query.filter_by(
            cod_emprestimo=COD_EMPRESTIMO, tombo_exemplar=TOMBO_EXEMPLAR
        ).first()

        if emprestimo_exemplar is None:
            emprestimo_exemplares_ns.abort(404, "Empréstimo exemplar não encontrado")

        return emprestimo_exemplar.to_dict()

    @emprestimo_exemplares_ns.doc("deletar_emprestimo_exemplar")
    @emprestimo_exemplares_ns.marshal_with(message_model)
    @emprestimo_exemplares_ns.response(
        404, "Empréstimo exemplar não encontrado", error_model
    )
    @emprestimo_exemplares_ns.response(500, "Erro interno do servidor", error_model)
    def delete(self, COD_EMPRESTIMO, TOMBO_EXEMPLAR):
        """Remove um exemplar de um empréstimo"""
        emprestimo_exemplar = EmprestimoExemplar.query.filter_by(
            cod_emprestimo=COD_EMPRESTIMO, tombo_exemplar=TOMBO_EXEMPLAR
        ).first()

        if emprestimo_exemplar is None:
            emprestimo_exemplares_ns.abort(404, "Empréstimo exemplar não encontrado")

        try:
            db.session.delete(emprestimo_exemplar)
            db.session.commit()
            return {"message": "Exemplar removido do empréstimo com sucesso"}
        except Exception as e:
            db.session.rollback()
            emprestimo_exemplares_ns.abort(
                500, f"Erro ao remover exemplar do empréstimo: {str(e)}"
            )
        finally:
            db.session.close()


@emprestimo_exemplares_ns.route("/emprestimo/<int:COD_EMPRESTIMO>")
@emprestimo_exemplares_ns.param("COD_EMPRESTIMO", "Código do empréstimo")
class ExemplaresPorEmprestimo(Resource):
    @emprestimo_exemplares_ns.doc("listar_exemplares_por_emprestimo")
    @emprestimo_exemplares_ns.marshal_list_with(emprestimo_exemplar_model)
    @emprestimo_exemplares_ns.response(404, "Empréstimo não encontrado", error_model)
    def get(self, COD_EMPRESTIMO):
        """Lista todos os exemplares de um empréstimo específico"""
        # Verificar se o empréstimo existe
        emprestimo = db.session.get(Emprestimo, COD_EMPRESTIMO)
        if not emprestimo:
            emprestimo_exemplares_ns.abort(404, "Empréstimo não encontrado")

        emprestimo_exemplares = EmprestimoExemplar.query.filter_by(
            cod_emprestimo=COD_EMPRESTIMO
        ).all()

        return [ee.to_dict() for ee in emprestimo_exemplares]


@emprestimo_exemplares_ns.route("/exemplar/<int:TOMBO_EXEMPLAR>")
@emprestimo_exemplares_ns.param("TOMBO_EXEMPLAR", "Tombo do exemplar")
class EmprestimosPorExemplar(Resource):
    @emprestimo_exemplares_ns.doc("listar_emprestimos_por_exemplar")
    @emprestimo_exemplares_ns.marshal_list_with(emprestimo_exemplar_model)
    @emprestimo_exemplares_ns.response(404, "Exemplar não encontrado", error_model)
    def get(self, TOMBO_EXEMPLAR):
        """Lista todos os empréstimos de um exemplar específico"""
        # Verificar se o exemplar existe
        exemplar = db.session.get(Exemplar, TOMBO_EXEMPLAR)
        if not exemplar:
            emprestimo_exemplares_ns.abort(404, "Exemplar não encontrado")

        emprestimo_exemplares = EmprestimoExemplar.query.filter_by(
            tombo_exemplar=TOMBO_EXEMPLAR
        ).all()

        return [ee.to_dict() for ee in emprestimo_exemplares]
