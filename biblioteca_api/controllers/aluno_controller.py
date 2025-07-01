from flask import request
from flask_restx import Namespace, Resource

from .. import db
from ..models.aluno import Aluno
from ..models.swagger_models import (
    aluno_model,
    aluno_response_model,
    error_model,
    message_model,
)

alunos_ns = Namespace("Alunos", description="Operações relacionadas a alunos")


@alunos_ns.route("/")
class AlunosList(Resource):
    @alunos_ns.doc("listar_alunos")
    @alunos_ns.marshal_list_with(aluno_response_model)
    def get(self):
        """Lista todos os alunos"""
        alunos = Aluno.query.all()
        return [aluno.to_dict() for aluno in alunos]

    @alunos_ns.doc("criar_aluno")
    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_response_model, code=201)
    @alunos_ns.response(409, "O e-mail informado já está em uso", error_model)
    @alunos_ns.response(500, "Erro interno do servidor", error_model)
    def post(self):
        """Cria um novo aluno"""
        data = request.get_json()
        if Aluno.query.filter_by(EMAIL=data["EMAIL"]).first():
            alunos_ns.abort(409, f"O e-mail '{data['EMAIL']}' já está em uso.")
        try:
            new_aluno = Aluno(
                NOME=data["NOME"],
                EMAIL=data["EMAIL"],
                CURSO=data.get("CURSO", ""),
            )
            db.session.add(new_aluno)
            db.session.commit()
            return new_aluno.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            alunos_ns.abort(500, f"Erro ao criar aluno: {str(e)}")
        finally:
            db.session.close()


@alunos_ns.route("/<int:MAT_ALUNO>")
@alunos_ns.param("MAT_ALUNO", "Matrícula do aluno")
class AlunoResource(Resource):
    @alunos_ns.doc("obter_aluno")
    @alunos_ns.marshal_with(aluno_response_model)
    @alunos_ns.response(404, "Aluno não encontrado", error_model)
    def get(self, MAT_ALUNO):
        """Obtém um aluno pela matrícula"""
        aluno = db.session.get(Aluno, MAT_ALUNO)
        if aluno is None:
            alunos_ns.abort(404, "Aluno não encontrado")
        return aluno.to_dict()

    @alunos_ns.doc("atualizar_aluno")
    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_response_model)
    @alunos_ns.response(404, "Aluno não encontrado", error_model)
    @alunos_ns.response(409, "O e-mail informado já está em uso", error_model)
    @alunos_ns.response(500, "Erro interno do servidor", error_model)
    def put(self, MAT_ALUNO):
        """Atualiza um aluno existente"""
        aluno = db.session.get(Aluno, MAT_ALUNO)
        if aluno is None:
            alunos_ns.abort(404, "Aluno não encontrado")

        data = request.get_json()

        # Verifica se o e-mail já está em uso por outro aluno
        existing_aluno = Aluno.query.filter(Aluno.EMAIL == data["EMAIL"]).first()
        if existing_aluno and str(existing_aluno.MAT_ALUNO) != str(MAT_ALUNO):
            alunos_ns.abort(409, f"O e-mail '{data['EMAIL']}' já está em uso.")

        try:
            aluno.NOME = data["NOME"]
            aluno.EMAIL = data["EMAIL"]
            aluno.CURSO = data.get("CURSO", "")
            db.session.commit()
            return aluno.to_dict()
        except Exception as e:
            db.session.rollback()
            alunos_ns.abort(500, f"Erro ao atualizar aluno: {str(e)}")
        finally:
            db.session.close()

    @alunos_ns.doc("deletar_aluno")
    @alunos_ns.marshal_with(message_model)
    @alunos_ns.response(404, "Aluno não encontrado", error_model)
    @alunos_ns.response(500, "Erro interno do servidor", error_model)
    def delete(self, MAT_ALUNO):
        """Deleta um aluno existente"""
        aluno = db.session.get(Aluno, MAT_ALUNO)
        if aluno is None:
            alunos_ns.abort(404, "Aluno não encontrado")

        try:
            db.session.delete(aluno)
            db.session.commit()
            return {"message": "Aluno deletado com sucesso"}
        except Exception as e:
            db.session.rollback()
            alunos_ns.abort(500, f"Erro ao deletar aluno: {str(e)}")
        finally:
            db.session.close()
