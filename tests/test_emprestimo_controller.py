from datetime import datetime, timedelta

import pytest

from biblioteca_api import app, db
from biblioteca_api.models.aluno import Aluno
from biblioteca_api.models.emprestimo import Emprestimo


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            aluno = Aluno(
                MAT_ALUNO=12345,
                NOME="Aluno Teste",
                EMAIL="aluno@teste.com",
                CURSO="Curso Teste",
            )
            db.session.add(aluno)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_criar_emprestimo(client):
    response = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["MAT_ALUNO"] == 12345
    assert "DATA_EMPRESTIMO" in data
    assert "DATA_PREVISTA_DEV" in data


def test_listar_emprestimos(client):
    client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    response = client.get("/Emprestimos/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(emprestimo["MAT_ALUNO"] == 12345 for emprestimo in data)


def test_obter_emprestimo(client):
    resp = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    COD = resp.get_json()["COD"]
    response = client.get(f"/Emprestimos/{COD}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["MAT_ALUNO"] == 12345


def test_atualizar_emprestimo(client):
    resp = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    COD = resp.get_json()["COD"]
    new_data_emprestimo = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    new_data_prevista_dev = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    response = client.put(
        f"/Emprestimos/{COD}",
        json={
            "MAT_ALUNO": 12345,
            "DATA_EMPRESTIMO": new_data_emprestimo,
            "DATA_PREVISTA_DEV": new_data_prevista_dev,
            "DATA_DEVOLUCAO": None,
            "DATA_ATRASO": None,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["DATA_EMPRESTIMO"] == new_data_emprestimo
    assert data["DATA_PREVISTA_DEV"] == new_data_prevista_dev


def test_deletar_emprestimo(client):
    resp = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    COD = resp.get_json()["COD"]
    response = client.delete(f"/Emprestimos/{COD}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Empréstimo deletado com sucesso" in data["message"]
    response = client.get(f"/Emprestimos/{COD}")
    assert response.status_code == 404


def test_devolver_emprestimo(client):
    resp = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    COD = resp.get_json()["COD"]
    response = client.put(f"/Emprestimos/devolver/{COD}")
    assert response.status_code == 200
    data = response.get_json()
    assert "DATA_DEVOLUCAO" in data
    assert data["DATA_DEVOLUCAO"] == datetime.now().strftime("%Y-%m-%d")


def test_listar_emprestimos_por_aluno(client):
    client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    response = client.get("/Emprestimos/aluno/12345")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(emprestimo["MAT_ALUNO"] == 12345 for emprestimo in data)


def test_criar_emprestimo_aluno_inexistente(client):
    data = {"MAT_ALUNO": 99999}
    response = client.post("/Emprestimos/", json=data)
    assert response.status_code == 400
    assert "Aluno não encontrado" in response.get_json()["message"]


def test_obter_emprestimo_inexistente(client):
    response = client.get("/Emprestimos/9999")
    assert response.status_code == 404
    assert "Empréstimo não encontrado" in response.get_json()["message"]


def test_deletar_emprestimo_inexistente(client):
    response = client.delete("/Emprestimos/9999")
    assert response.status_code == 404
    assert "Empréstimo não encontrado" in response.get_json()["message"]


def test_devolver_emprestimo_inexistente(client):
    response = client.put("/Emprestimos/devolver/9999")
    assert response.status_code == 404
    assert "Empréstimo não encontrado" in response.get_json()["message"]


def test_devolver_emprestimo_ja_devolvido(client):
    resp = client.post(
        "/Emprestimos/",
        json={"MAT_ALUNO": 12345},
    )
    COD = resp.get_json()["COD"]
    client.put(f"/Emprestimos/devolver/{COD}")
    response = client.put(f"/Emprestimos/devolver/{COD}")
    assert response.status_code == 400
    assert "Empréstimo já foi devolvido" in response.get_json()["message"]


def test_listar_emprestimos_por_aluno_inexistente(client):
    response = client.get("/Emprestimos/aluno/99999")
    assert response.status_code == 404
    assert "Aluno não encontrado" in response.get_json()["message"]
