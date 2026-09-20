
def test_deletar_animal_existente(client, admin_headers):

    # --------------------------------------------------------
    # CRIAR ANIMAL
    # --------------------------------------------------------

    criar = client.post(
        "/animais/",
        headers=admin_headers,
        json={
            "nome_popular": "Tamanduá-bandeira",
            "nome_cientifico": "Myrmecophaga tridactyla",
            "descricao": "Mamífero brasileiro",
            "dieta": "Insetívora",
            "habitat_especifico": "Cerrado"
        }
    )

    assert criar.status_code == 201

    animal_id = criar.get_json()["id"]

    # --------------------------------------------------------
    # DELETAR
    # --------------------------------------------------------

    resposta = client.delete(
        f"/animais/{animal_id}",
        headers=admin_headers
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["id"] == animal_id
    assert dados["mensagem"] == "Animal deletado com sucesso"


# ============================================================
# PROFESSOR NÃO PODE DELETAR
# ============================================================

def test_professor_nao_pode_deletar_animal(
    client,
    headers
):

    criar = client.post(
        "/animais/",
        headers=headers,
        json={
            "nome_popular": "Capivara",
            "nome_cientifico": "Hydrochoerus hydrochaeris",
            "descricao": "Roedor",
            "dieta": "Herbívora",
            "habitat_especifico": "Áreas próximas à água"
        }
    )

    assert criar.status_code == 201

    animal_id = criar.get_json()["id"]

    resposta = client.delete(
        f"/animais/{animal_id}",
        headers=headers
    )

    assert resposta.status_code == 403


# ============================================================
# ADMIN DELETA ANIMAL INEXISTENTE
# ============================================================

def test_admin_deletar_animal_inexistente(
    client,
    admin_headers
):

    resposta = client.delete(
        "/animais/999999",
        headers=admin_headers
    )

    assert resposta.status_code == 404

