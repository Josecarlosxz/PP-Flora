def test_listar_participantes(client, headers):

    resposta = client.get(
        "/participantes/",
        headers=headers
    )

    assert resposta.status_code == 200

    assert isinstance(
        resposta.get_json(),
        list
    )


def test_buscar_participante_inexistente(client, headers):

    resposta = client.get(
        "/participantes/999999",
        headers=headers
    )

    assert resposta.status_code == 404


def test_criar_participante_sem_login(client):

    resposta = client.post(
        "/participantes/",
        json={
            "nome": "Participante"
        }
    )

    assert resposta.status_code == 401