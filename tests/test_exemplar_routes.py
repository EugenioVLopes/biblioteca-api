import pytest

from biblioteca_api import app, db
from biblioteca_api.models.exemplar import Exemplar
from biblioteca_api.models.livro import Livro


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            livro = Livro(TITULO="Livro Teste", AUTOR="Autor Teste")
            db.session.add(livro)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_criar_exemplar(client):
    response = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["COD_LIVRO"] == 1
    assert "TOMBO" in data


def test_listar_exemplares(client):
    client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    response = client.get("/Exemplares/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(exemplar["COD_LIVRO"] == 1 for exemplar in data)


def test_obter_exemplar(client):
    resp = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    tombo_exemplar = resp.get_json()["TOMBO"]
    response = client.get(f"/Exemplares/{tombo_exemplar}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["COD_LIVRO"] == 1


def test_atualizar_exemplar(client):
    resp = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    tombo_exemplar = resp.get_json()["TOMBO"]
    livro2 = Livro(TITULO="Livro Teste 2", AUTOR="Autor Teste 2")
    with app.app_context():
        db.session.add(livro2)
        db.session.commit()

    response = client.put(
        f"/Exemplares/{tombo_exemplar}",
        json={
            "COD_LIVRO": 2,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["COD_LIVRO"] == 2


def test_deletar_exemplar(client):
    resp = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    tombo_exemplar = resp.get_json()["TOMBO"]
    response = client.delete(f"/Exemplares/{tombo_exemplar}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Exemplar deletado com sucesso" in data["message"]
    response = client.get(f"/Exemplares/{tombo_exemplar}")
    assert response.status_code == 404


def test_criar_exemplar_livro_inexistente(client):
    response = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 999,
        },
    )
    assert response.status_code == 400
    assert "Livro não encontrado" in response.get_json()["error"]


def test_obter_exemplar_inexistente(client):
    response = client.get("/Exemplares/9999")
    assert response.status_code == 404
    assert "Exemplar não encontrado" in response.get_json()["error"]


def test_atualizar_exemplar_inexistente(client):
    response = client.put(
        "/Exemplares/9999",
        json={
            "COD_LIVRO": 1,
        },
    )
    assert response.status_code == 404
    assert "Exemplar não encontrado" in response.get_json()["error"]


def test_deletar_exemplar_inexistente(client):
    response = client.delete("/Exemplares/9999")
    assert response.status_code == 404
    assert "Exemplar não encontrado" in response.get_json()["error"]


def test_listar_exemplares_por_livro(client):
    client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    response = client.get("/Exemplares/livro/1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all(exemplar["COD_LIVRO"] == 1 for exemplar in data)


def test_listar_exemplares_por_livro_inexistente(client):
    response = client.get("/Exemplares/livro/999")
    assert response.status_code == 404
    assert "Livro não encontrado" in response.get_json()["error"]


def test_criar_exemplar_sem_cod_livro(client):
    response = client.post(
        "/Exemplares/",
        json={},
    )
    assert response.status_code == 400
    assert "COD_LIVRO é obrigatório" in response.get_json()["error"]


def test_atualizar_exemplar_sem_cod_livro(client):
    resp = client.post(
        "/Exemplares/",
        json={
            "COD_LIVRO": 1,
        },
    )
    tombo_exemplar = resp.get_json()["TOMBO"]

    response = client.put(
        f"/Exemplares/{tombo_exemplar}",
        json={},
    )
    assert response.status_code == 400
    assert "COD_LIVRO é obrigatório" in response.get_json()["error"]
