def test_login(client, usuario):

    resposta = client.post(
        "/login/",
        json={
            "email": "teste_professor@email.com",
            "senha": "Senha123"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert "token" in dados
    assert dados["tipo"] == "Bearer"
    assert "usuario" in dados


def test_login_email_inexistente(client):

    resposta = client.post(
        "/login/",
        json={
            "email": "naoexiste@email.com",
            "senha": "Senha123"
        }
    )

    assert resposta.status_code == 401


def test_login_senha_incorreta(client, usuario):

    resposta = client.post(
        "/login/",
        json={
            "email": "teste_professor@email.com",
            "senha": "SenhaErrada"
        }
    )

    assert resposta.status_code == 401


def test_login_sem_dados(client):

    resposta = client.post(
        "/login/",
        json={}
    )

    assert resposta.status_code == 400