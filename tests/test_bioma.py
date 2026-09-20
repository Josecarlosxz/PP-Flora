def test_listar_biomas(client, headers):

    resposta = client.get(
        "/biomas/",
        headers=headers
    )

    assert resposta.status_code == 200

    assert isinstance(
        resposta.get_json(),
        list
    )


def test_buscar_bioma_inexistente(client, headers):

    resposta = client.get(
        "/biomas/999999",
        headers=headers
    )

    assert resposta.status_code == 404


def test_criar_bioma_sem_login(client):

    resposta = client.post(
        "/biomas/",
        json={}
    )

    assert resposta.status_code == 401