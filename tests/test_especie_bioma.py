# ============================================================
# TESTES DE ESPÉCIE x BIOMA
# ============================================================


# ============================================================
# LISTAR RELAÇÕES
# ============================================================

def test_listar_especies_biomas(client, headers):

    resposta = client.get(
        "/especie_bioma/",
        headers=headers
    )

    assert resposta.status_code == 200


# ============================================================
# LISTAR SEM LOGIN
# ============================================================

def test_listar_especies_biomas_sem_login(client):

    resposta = client.get(
        "/especie_bioma/"
    )

    assert resposta.status_code == 401


# ============================================================
# CRIAR SEM LOGIN
# ============================================================

def test_criar_especie_bioma_sem_login(client):

    resposta = client.post(
        "/especie_bioma/",
        json={}
    )

    assert resposta.status_code == 401


# ============================================================
# BUSCAR RELAÇÃO INEXISTENTE
# ============================================================

def test_buscar_especie_bioma_inexistente(
    client,
    headers
):

    resposta = client.get(
        "/especie_bioma/999999",
        headers=headers
    )

    assert resposta.status_code == 404


# ============================================================
# ATUALIZAR RELAÇÃO INEXISTENTE
# ============================================================

def test_atualizar_especie_bioma_inexistente(
    client,
    headers
):

    resposta = client.put(
        "/especie_bioma/999999",
        headers=headers,
        json={
            "especie_id": 1,
            "bioma_id": 1
        }
    )

    assert resposta.status_code == 404


# ============================================================
# DELETAR SEM LOGIN
# ============================================================

def test_deletar_especie_bioma_sem_login(client):

    resposta = client.delete(
        "/especie_bioma/999999"
    )

    assert resposta.status_code == 401