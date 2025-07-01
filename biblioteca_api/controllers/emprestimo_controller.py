from datetime import datetime, timedelta

from flask import request
from flask_restx import Namespace, Resource

from .. import db
from ..models.aluno import Aluno
from ..models.emprestimo import Emprestimo
from ..models.swagger_models import emprestimo_model, error_model, message_model

emprestimos_ns = Namespace(
    "Emprestimos", description="Operações relacionadas a empréstimos"
)


@emprestimos_ns.route("/")
class EmprestimosList(Resource):
    @emprestimos_ns.doc("listar_emprestimos")
    @emprestimos_ns.marshal_list_with(emprestimo_model)
    def get(self):
        """Lista todos os empréstimos"""
        emprestimos = Emprestimo.query.all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]

    @emprestimos_ns.doc("criar_emprestimo")
    @emprestimos_ns.expect(emprestimo_model)
    @emprestimos_ns.marshal_with(emprestimo_model, code=201)
    @emprestimos_ns.response(400, "Aluno não encontrado", error_model)
    @emprestimos_ns.response(500, "Erro interno do servidor", error_model)
    def post(self):
        """Cria um novo empréstimo"""
        data = request.get_json()

        # Verificar se o aluno existe
        aluno = db.session.get(Aluno, data["MAT_ALUNO"])
        if not aluno:
            emprestimos_ns.abort(400, "Aluno não encontrado")

        try:
            data_emprestimo = datetime.now().date()
            data_prevista_dev = data_emprestimo + timedelta(days=15)

            new_emprestimo = Emprestimo(
                MAT_ALUNO=data["MAT_ALUNO"],
                DATA_EMPRESTIMO=data_emprestimo,
                DATA_PREVISTA_DEV=data_prevista_dev,
                DATA_DEVOLUCAO=None,
                DATA_ATRASO=None,
            )
            db.session.add(new_emprestimo)
            db.session.commit()
            db.session.refresh(new_emprestimo)
            return new_emprestimo.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            emprestimos_ns.abort(500, f"Erro ao criar empréstimo: {str(e)}")
        finally:
            db.session.close()


@emprestimos_ns.route("/<int:COD>")
@emprestimos_ns.param("COD", "Código do empréstimo (COD)")
class EmprestimoResource(Resource):
    @emprestimos_ns.doc("obter_emprestimo")
    @emprestimos_ns.marshal_with(emprestimo_model)
    @emprestimos_ns.response(404, "Empréstimo não encontrado", error_model)
    def get(self, COD):
        """Obtém um empréstimo pelo COD"""
        emprestimo = db.session.get(Emprestimo, COD)
        if emprestimo is None:
            emprestimos_ns.abort(404, "Empréstimo não encontrado")
        return emprestimo.to_dict()

    @emprestimos_ns.doc("atualizar_emprestimo")
    @emprestimos_ns.expect(emprestimo_model)
    @emprestimos_ns.marshal_with(emprestimo_model)
    @emprestimos_ns.response(404, "Empréstimo não encontrado", error_model)
    @emprestimos_ns.response(400, "Aluno não encontrado", error_model)
    @emprestimos_ns.response(500, "Erro interno do servidor", error_model)
    def put(self, COD):
        """Atualiza um empréstimo existente pelo COD"""
        emprestimo = db.session.get(Emprestimo, COD)
        if emprestimo is None:
            emprestimos_ns.abort(404, "Empréstimo não encontrado")

        data = request.get_json()

        aluno = db.session.get(Aluno, data["MAT_ALUNO"])
        if not aluno:
            emprestimos_ns.abort(400, "Aluno não encontrado")

        try:
            emprestimo.MAT_ALUNO = data["MAT_ALUNO"]
            emprestimo.DATA_EMPRESTIMO = datetime.strptime(
                data["DATA_EMPRESTIMO"], "%Y-%m-%d"
            ).date()
            emprestimo.DATA_PREVISTA_DEV = datetime.strptime(
                data["DATA_PREVISTA_DEV"], "%Y-%m-%d"
            ).date()
            emprestimo.DATA_DEVOLUCAO = (
                datetime.strptime(data["DATA_DEVOLUCAO"], "%Y-%m-%d").date()
                if data.get("DATA_DEVOLUCAO")
                else None
            )
            emprestimo.DATA_ATRASO = (
                datetime.strptime(data["DATA_ATRASO"], "%Y-%m-%d").date()
                if data.get("DATA_ATRASO")
                else None
            )
            db.session.commit()
            return emprestimo.to_dict()
        except Exception as e:
            db.session.rollback()
            emprestimos_ns.abort(500, f"Erro ao atualizar empréstimo: {str(e)}")
        finally:
            db.session.close()

    @emprestimos_ns.doc("deletar_emprestimo")
    @emprestimos_ns.marshal_with(message_model)
    @emprestimos_ns.response(404, "Empréstimo não encontrado", error_model)
    @emprestimos_ns.response(500, "Erro interno do servidor", error_model)
    def delete(self, COD):
        """Deleta um empréstimo existente pelo COD"""
        emprestimo = db.session.get(Emprestimo, COD)
        if emprestimo is None:
            emprestimos_ns.abort(404, "Empréstimo não encontrado")

        try:
            db.session.delete(emprestimo)
            db.session.commit()
            return {"message": "Empréstimo deletado com sucesso"}
        except Exception as e:
            db.session.rollback()
            emprestimos_ns.abort(500, f"Erro ao deletar empréstimo: {str(e)}")
        finally:
            db.session.close()


@emprestimos_ns.route("/devolver/<int:COD>")
@emprestimos_ns.param("COD", "Código do empréstimo (COD)")
class DevolverEmprestimo(Resource):
    @emprestimos_ns.doc("devolver_emprestimo")
    @emprestimos_ns.marshal_with(emprestimo_model)
    @emprestimos_ns.response(404, "Empréstimo não encontrado", error_model)
    @emprestimos_ns.response(400, "Empréstimo já devolvido", error_model)
    @emprestimos_ns.response(500, "Erro interno do servidor", error_model)
    def put(self, COD):
        """Registra a devolução de um empréstimo pelo COD"""
        emprestimo = db.session.get(Emprestimo, COD)
        if emprestimo is None:
            emprestimos_ns.abort(404, "Empréstimo não encontrado")

        if emprestimo.DATA_DEVOLUCAO:
            emprestimos_ns.abort(400, "Empréstimo já foi devolvido")

        try:
            data_devolucao = datetime.now().date()
            emprestimo.DATA_DEVOLUCAO = data_devolucao

            if data_devolucao > emprestimo.DATA_PREVISTA_DEV:
                emprestimo.DATA_ATRASO = data_devolucao

            db.session.commit()
            return emprestimo.to_dict()
        except Exception as e:
            db.session.rollback()
            emprestimos_ns.abort(500, f"Erro ao registrar devolução: {str(e)}")
        finally:
            db.session.close()


@emprestimos_ns.route("/aluno/<int:MAT_ALUNO>")
@emprestimos_ns.param("MAT_ALUNO", "Matrícula do aluno")
class EmprestimosPorAluno(Resource):
    @emprestimos_ns.doc("listar_emprestimos_por_aluno")
    @emprestimos_ns.marshal_list_with(emprestimo_model)
    @emprestimos_ns.response(404, "Aluno não encontrado", error_model)
    def get(self, MAT_ALUNO):
        """Lista todos os empréstimos de um aluno específico"""
        aluno = db.session.get(Aluno, MAT_ALUNO)
        if not aluno:
            emprestimos_ns.abort(404, "Aluno não encontrado")

        emprestimos = Emprestimo.query.filter_by(MAT_ALUNO=MAT_ALUNO).all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
