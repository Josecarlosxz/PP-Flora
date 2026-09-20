def test_logout(client, headers):

    resposta = client.post(
        "/logout/",
        headers=headers
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["mensagem"] == "Logout realizado com sucesso"


def test_logout_sem_token(client):

    resposta = client.post(
        "/logout/"
    )

    assert resposta.status_code == 401