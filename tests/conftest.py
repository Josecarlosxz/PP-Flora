import pytest

from main import app
from backend.database.database import SessionLocal
from backend.models.usuario import Usuario
from backend.models.token import Token


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def usuario(client, db):
    """
    Cria um usuário professor para os testes.
    """

    email = "teste_professor@email.com"

    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )

    if usuario:
        return usuario

    resposta = client.post(
        "/usuarios/",
        json={
            "nome": "Professor Teste",
            "email": email,
            "senha": "Senha123"
        }
    )

    assert resposta.status_code == 201

    return (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )


@pytest.fixture
def token(client, usuario):
    """
    Faz login e retorna o token.
    """

    resposta = client.post(
        "/login/",
        json={
            "email": "teste_professor@email.com",
            "senha": "Senha123"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    return dados["token"]


@pytest.fixture
def headers(token):
    """
    Header de autenticação.
    """

    return {
        "Authorization": f"Bearer {token}"
    }