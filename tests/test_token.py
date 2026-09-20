def test_listar_tokens_sem_login(client):

    resposta = client.get(
        "/tokens/"
    )

    assert resposta.status_code == 401


def test_buscar_token_sem_login(client):

    resposta = client.get(
        "/tokens/1"
    )

    assert resposta.status_code == 401


def test_desativar_token_sem_login(client):

    resposta = client.put(
        "/tokens/1/desativar"
    )

    assert resposta.status_code == 401


def test_deletar_token_sem_login(client):

    resposta = client.delete(
        "/tokens/1"
    )

    assert resposta.status_code == 401