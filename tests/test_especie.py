def test_listar_especies(client, headers):

    resposta = client.get(
        "/especies/",
        headers=headers
    )

    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_buscar_especie_inexistente(client, headers):

    resposta = client.get(
        "/especies/999999",
        headers=headers
    )

    assert resposta.status_code == 404


def test_criar_especie_sem_login(client):

    resposta = client.post(
        "/especies/",
        json={}
    )

    assert resposta.status_code == 401