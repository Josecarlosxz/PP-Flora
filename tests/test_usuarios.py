import uuid


# ============================================================
# GERA EMAIL ÚNICO PARA OS TESTES
# ============================================================

def email_unico():

    return f"teste_{uuid.uuid4().hex}@email.com"


# ============================================================
# CADASTRAR USUÁRIO
# ============================================================

def test_cadastrar_usuario(client):

    email = email_unico()

    resposta = client.post(
        "/usuarios/",
        json={
            "nome": "Usuario Teste",
            "email": email,
            "senha": "Senha123"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["nome"] == "Usuario Teste"
    assert dados["email"] == email
    assert dados["perfil"] == "professor"


# ============================================================
# CADASTRAR USUÁRIO COM EMAIL DUPLICADO
# ============================================================

def test_cadastrar_usuario_email_duplicado(client):

    email = email_unico()

    dados = {
        "nome": "Usuario",
        "email": email,
        "senha": "Senha123"
    }

    # --------------------------------------------------------
    # PRIMEIRO CADASTRO
    # --------------------------------------------------------

    primeira = client.post(
        "/usuarios/",
        json=dados
    )

    assert primeira.status_code == 201

    # --------------------------------------------------------
    # SEGUNDO CADASTRO
    # --------------------------------------------------------

    segunda = client.post(
        "/usuarios/",
        json=dados
    )

    assert segunda.status_code == 409

    resposta = segunda.get_json()

    assert resposta["erro"] == "Email já cadastrado"