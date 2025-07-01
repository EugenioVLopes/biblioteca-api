from datetime import datetime, timedelta

import pytest

from biblioteca_api import app, db
from biblioteca_api.models.aluno import Aluno
from biblioteca_api.models.emprestimo import Emprestimo
from biblioteca_api.models.exemplar import Exemplar
from biblioteca_api.models.livro import Livro


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.query(Emprestimo).delete()
            db.session.query(Exemplar).delete()
            db.session.query(Livro).delete()
            db.session.query(Aluno).delete()
            db.session.commit()
            aluno = Aluno(
                MAT_ALUNO=1,
                NOME="Aluno Teste",
                EMAIL="aluno@teste.com",
                CURSO="Engenharia",
            )
            db.session.add(aluno)
            db.session.commit()

            livro = Livro(TITULO="Livro Teste", AUTOR="Autor Teste")
            db.session.add(livro)
            db.session.commit()

            exemplar = Exemplar(TOMBO=1, COD_LIVRO=1)
            db.session.add(exemplar)
            db.session.commit()

            emprestimo = Emprestimo(
                COD=1,
                MAT_ALUNO=1,
                DATA_EMPRESTIMO=datetime.now().date(),
                DATA_PREVISTA_DEV=(datetime.now() + timedelta(days=15)).date(),
            )
            db.session.add(emprestimo)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_criar_emprestimo_exemplar(client):
    response = client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["COD_EMPRESTIMO"] == 1
    assert data["TOMBO_EXEMPLAR"] == 1


def test_listar_emprestimo_exemplares(client):
    client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    response = client.get("/Emprestimo-exemplares/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(ee["COD_EMPRESTIMO"] == 1 and ee["TOMBO_EXEMPLAR"] == 1 for ee in data)


def test_obter_emprestimo_exemplar(client):
    client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    response = client.get("/Emprestimo-exemplares/1/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["COD_EMPRESTIMO"] == 1
    assert data["TOMBO_EXEMPLAR"] == 1


def test_deletar_emprestimo_exemplar(client):
    client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    response = client.delete("/Emprestimo-exemplares/1/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "Exemplar removido do empréstimo com sucesso" in data["message"]
    response = client.get("/Emprestimo-exemplares/1/1")
    assert response.status_code == 404


def test_criar_emprestimo_exemplar_emprestimo_inexistente(client):
    response = client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 999,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    assert response.status_code == 400
    assert "Empréstimo não encontrado" in response.get_json()["message"]


def test_criar_emprestimo_exemplar_exemplar_inexistente(client):
    response = client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 999,
        },
    )
    assert response.status_code == 400
    assert "Exemplar não encontrado" in response.get_json()["message"]


def test_obter_emprestimo_exemplar_inexistente(client):
    response = client.get("/Emprestimo-exemplares/999/999")
    assert response.status_code == 404
    assert "Empréstimo exemplar não encontrado" in response.get_json()["message"]


def test_deletar_emprestimo_exemplar_inexistente(client):
    response = client.delete("/Emprestimo-exemplares/999/999")
    assert response.status_code == 404
    assert "Empréstimo exemplar não encontrado" in response.get_json()["message"]


def test_listar_exemplares_por_emprestimo(client):
    client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    response = client.get("/Emprestimo-exemplares/emprestimo/1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(ee["COD_EMPRESTIMO"] == 1 for ee in data)


def test_listar_emprestimos_por_exemplar(client):
    client.post(
        "/Emprestimo-exemplares/",
        json={
            "COD_EMPRESTIMO": 1,
            "TOMBO_EXEMPLAR": 1,
        },
    )
    response = client.get("/Emprestimo-exemplares/exemplar/1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(ee["TOMBO_EXEMPLAR"] == 1 for ee in data)


def test_listar_exemplares_por_emprestimo_inexistente(client):
    response = client.get("/Emprestimo-exemplares/emprestimo/999")
    assert response.status_code == 404
    assert "Empréstimo não encontrado" in response.get_json()["message"]


def test_listar_emprestimos_por_exemplar_inexistente(client):
    response = client.get("/Emprestimo-exemplares/exemplar/999")
    assert response.status_code == 404
    assert "Exemplar não encontrado" in response.get_json()["message"]
