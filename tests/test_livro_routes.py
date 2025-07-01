import pytest

from biblioteca_api import app, db
from biblioteca_api.models.livro import Livro


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


def test_criar_livro(client):
    response = client.post(
        "/Livros/",
        json={
            "TITULO": "Livro Teste",
            "AUTOR": "Autor Teste",
            "EDITORA": "Editora Teste",
            "ANO": 2023,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["TITULO"] == "Livro Teste"
    assert data["AUTOR"] == "Autor Teste"
    assert "COD" in data


def test_listar_livros(client):
    client.post(
        "/Livros/",
        json={
            "TITULO": "Livro Teste 2",
            "AUTOR": "Autor Teste 2",
            "EDITORA": "Editora Teste 2",
            "ANO": 2022,
        },
    )
    response = client.get("/Livros/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(livro["TITULO"] == "Livro Teste 2" for livro in data)


def test_obter_livro(client):
    resp = client.post(
        "/Livros/",
        json={
            "TITULO": "Livro Teste 3",
            "AUTOR": "Autor Teste 3",
            "EDITORA": "Editora Teste 3",
            "ANO": 2021,
        },
    )
    cod_livro = resp.get_json()["COD"]
    response = client.get(f"/Livros/{cod_livro}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["TITULO"] == "Livro Teste 3"


def test_atualizar_livro(client):
    resp = client.post(
        "/Livros/",
        json={
            "TITULO": "Livro Teste 4",
            "AUTOR": "Autor Teste 4",
            "EDITORA": "Editora Teste 4",
            "ANO": 2020,
        },
    )
    cod_livro = resp.get_json()["COD"]
    response = client.put(
        f"/Livros/{cod_livro}",
        json={
            "TITULO": "Livro Atualizado",
            "AUTOR": "Autor Atualizado",
            "EDITORA": "Editora Atualizada",
            "ANO": 2019,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["TITULO"] == "Livro Atualizado"
    assert data["AUTOR"] == "Autor Atualizado"


def test_deletar_livro(client):
    resp = client.post(
        "/Livros/",
        json={
            "TITULO": "Livro Teste 5",
            "AUTOR": "Autor Teste 5",
            "EDITORA": "Editora Teste 5",
            "ANO": 2018,
        },
    )
    cod_livro = resp.get_json()["COD"]
    response = client.delete(f"/Livros/{cod_livro}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Livro deletado com sucesso" in data["message"]
    response = client.get(f"/Livros/{cod_livro}")
    assert response.status_code == 404


def test_obter_livro_inexistente(client):
    response = client.get("/Livros/9999")
    assert response.status_code == 404
    assert "Livro não encontrado" in response.get_json()["message"]


def test_atualizar_livro_inexistente(client):
    response = client.put(
        "/Livros/9999",
        json={
            "TITULO": "Livro Atualizado",
            "AUTOR": "Autor Atualizado",
            "EDITORA": "Editora Atualizada",
            "ANO": 2019,
        },
    )
    assert response.status_code == 404
    assert "Livro não encontrado" in response.get_json()["message"]


def test_deletar_livro_inexistente(client):
    response = client.delete("/Livros/9999")
    assert response.status_code == 404
    assert "Livro não encontrado" in response.get_json()["message"]


def test_buscar_livros_por_titulo(client):
    client.post(
        "/Livros/",
        json={
            "TITULO": "Aventuras de Python",
            "AUTOR": "Guido van Rossum",
            "EDITORA": "Tech Books",
            "ANO": 2020,
        },
    )
    client.post(
        "/Livros/",
        json={
            "TITULO": "Python para Iniciantes",
            "AUTOR": "Maria Silva",
            "EDITORA": "Code Press",
            "ANO": 2021,
        },
    )
    response = client.get("/Livros/buscar?TITULO=Python")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all("Python" in livro["TITULO"] for livro in data)


def test_buscar_livros_por_autor(client):
    client.post(
        "/Livros/",
        json={
            "TITULO": "O Grande Livro",
            "AUTOR": "João Autor",
            "EDITORA": "Editora X",
            "ANO": 2015,
        },
    )
    client.post(
        "/Livros/",
        json={
            "TITULO": "Pequenas Histórias",
            "AUTOR": "João Autor",
            "EDITORA": "Editora Y",
            "ANO": 2018,
        },
    )
    response = client.get("/Livros/buscar?AUTOR=João Autor")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(livro["AUTOR"] == "João Autor" for livro in data)


def test_buscar_livros_por_titulo_e_autor(client):
    client.post(
        "/Livros/",
        json={
            "TITULO": "Programação Avançada",
            "AUTOR": "Ana Programadora",
            "EDITORA": "Dev Books",
            "ANO": 2023,
        },
    )
    client.post(
        "/Livros/",
        json={
            "TITULO": "Introdução à Programação",
            "AUTOR": "Ana Programadora",
            "EDITORA": "Dev Books",
            "ANO": 2022,
        },
    )
    response = client.get("/Livros/buscar?TITULO=Introdução&AUTOR=Ana Programadora")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["TITULO"] == "Introdução à Programação"
    assert data[0]["AUTOR"] == "Ana Programadora"
