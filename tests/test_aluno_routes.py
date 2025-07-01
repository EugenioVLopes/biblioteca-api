import pytest

from biblioteca_api import app, db
from biblioteca_api.models.aluno import Aluno


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_criar_aluno(client):
    response = client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["NOME"] == "Aluno Teste"
    assert data["EMAIL"] == "aluno@teste.com"
    assert data["CURSO"] == "Curso Teste"
    assert "MAT_ALUNO" in data


def test_listar_alunos(client):
    client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    response = client.get("/Alunos/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(aluno["EMAIL"] == "aluno@teste.com" for aluno in data)


def test_obter_aluno(client):
    resp = client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    MAT_ALUNO = resp.get_json()["MAT_ALUNO"]
    response = client.get(f"/Alunos/{MAT_ALUNO}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["EMAIL"] == "aluno@teste.com"


def test_atualizar_aluno(client):
    resp = client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    MAT_ALUNO = resp.get_json()["MAT_ALUNO"]
    response = client.put(
        f"/Alunos/{MAT_ALUNO}",
        json={
            "NOME": "Aluno Atualizado",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Atualizado",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["NOME"] == "Aluno Atualizado"
    assert data["CURSO"] == "Curso Atualizado"


def test_deletar_aluno(client):
    resp = client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    MAT_ALUNO = resp.get_json()["MAT_ALUNO"]
    response = client.delete(f"/Alunos/{MAT_ALUNO}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Aluno deletado com sucesso" in data["message"]
    response = client.get(f"/Alunos/{MAT_ALUNO}")
    assert response.status_code == 404


def test_criar_aluno_email_duplicado(client):
    client.post(
        "/Alunos/",
        json={
            "NOME": "Aluno Teste",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Curso Teste",
        },
    )
    response = client.post(
        "/Alunos/",
        json={
            "NOME": "Outro Aluno",
            "EMAIL": "aluno@teste.com",
            "CURSO": "Outro Curso",
        },
    )
    assert response.status_code == 409
    assert "já está em uso" in response.get_json()["message"]


def test_obter_aluno_inexistente(client):
    response = client.get("/Alunos/9999")
    assert response.status_code == 404
    assert "Aluno não encontrado" in response.get_json()["message"]


def test_deletar_aluno_inexistente(client):
    response = client.delete("/Alunos/9999")
    assert response.status_code == 404
    assert "Aluno não encontrado" in response.get_json()["message"]


def test_atualizar_aluno_inexistente(client):
    response = client.put(
        "/Alunos/9999",
        json={
            "NOME": "Aluno Atualizado",
            "EMAIL": "novo@teste.com",
            "CURSO": "Novo Curso",
        },
    )
    assert response.status_code == 404
    assert "Aluno não encontrado" in response.get_json()["message"]
