def test_criar_planta(client, headers):

    resposta = client.post(
        "/plantas/",
        headers=headers,
        json={
            "nome_popular": "Babosa",
            "nome_cientifico": "Aloe vera",
            "descricao": "Planta medicinal",
            "tipo_folha": "Carnosa",
            "medicinal": True
        }
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["nome_popular"] == "Babosa"
    assert dados["tipo"] == "planta"
    assert dados["medicinal"] is True


def test_listar_plantas(client, headers):

    resposta = client.get(
        "/plantas/",
        headers=headers
    )

    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_buscar_planta_inexistente(client, headers):

    resposta = client.get(
        "/plantas/999999",
        headers=headers
    )

    assert resposta.status_code == 404


def test_atualizar_planta_inexistente(client, headers):

    resposta = client.put(
        "/plantas/999999",
        headers=headers,
        json={
            "nome_popular": "Nova planta"
        }
    )

    assert resposta.status_code == 404


def test_deletar_planta_sem_admin(client, headers):

    resposta = client.delete(
        "/plantas/999999",
        headers=headers
    )

    assert resposta.status_code in [403, 404]