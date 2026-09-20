from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from backend.database.database import SessionLocal
from backend.models.usuario import Usuario


cadastro_bp = Blueprint(
    "cadastro",
    __name__,
    url_prefix="/cadastro"
)


# ============================================================
# CADASTRO
# ============================================================

@cadastro_bp.route("/", methods=["POST"])
def cadastro():

    db = SessionLocal()

    try:

        data = request.get_json()

        # ----------------------------------------------------
        # VERIFICA DADOS
        # ----------------------------------------------------

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")

        # ----------------------------------------------------
        # CAMPOS OBRIGATÓRIOS
        # ----------------------------------------------------

        if not nome or not email or not senha:
            return jsonify({
                "erro": "Nome, email e senha são obrigatórios"
            }), 400

        nome = nome.strip()
        email = email.strip().lower()

        # ----------------------------------------------------
        # VALIDA NOME
        # ----------------------------------------------------

        if len(nome) < 2:
            return jsonify({
                "erro": "O nome deve possuir pelo menos 2 caracteres"
            }), 400

        # ----------------------------------------------------
        # VALIDA EMAIL
        # ----------------------------------------------------

        if len(email) > 100 or "@" not in email:
            return jsonify({
                "erro": "Email inválido"
            }), 400

        # ----------------------------------------------------
        # VALIDA SENHA
        # ----------------------------------------------------

        if len(senha) < 8:
            return jsonify({
                "erro": "A senha deve possuir pelo menos 8 caracteres"
            }), 400

        # ----------------------------------------------------
        # VERIFICA EMAIL EXISTENTE
        # ----------------------------------------------------

        usuario_existente = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario_existente:
            return jsonify({
                "erro": "Email já cadastrado"
            }), 409

        # ----------------------------------------------------
        # GERA HASH DA SENHA
        # ----------------------------------------------------

        senha_hash = generate_password_hash(senha)

        # ----------------------------------------------------
        # PERFIL PADRÃO
        # ----------------------------------------------------
        #
        # IMPORTANTE:
        # O usuário NÃO pode escolher o próprio perfil.
        #
        # O cadastro público cria professor.
        #
        # Administradores serão criados posteriormente
        # através de uma operação protegida.
        # ----------------------------------------------------

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil="professor"
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # ----------------------------------------------------
        # RESPOSTA
        # ----------------------------------------------------

        return jsonify({
            "mensagem": "Usuário cadastrado com sucesso",
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil
            }
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao realizar cadastro"
        }), 500

    finally:

        db.close()