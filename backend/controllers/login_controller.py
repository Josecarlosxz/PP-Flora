from flask import Blueprint, request, jsonify

from werkzeug.security import check_password_hash

from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from backend.database.database import SessionLocal
from backend.models.usuario import Usuario
from backend.models.token import Token


login_bp = Blueprint(
    "login",
    __name__,
    url_prefix="/login"
)


# ============================================================
# LOGIN
# ============================================================

@login_bp.route("/", methods=["POST"])
def login():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return jsonify({
                "erro": "Email e senha são obrigatórios"
            }), 400

        email = email.strip().lower()

        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        # Não revela se o email existe.

        if not usuario:
            return jsonify({
                "erro": "Email ou senha inválidos"
            }), 401

        if not check_password_hash(
            usuario.senha_hash,
            senha
        ):
            return jsonify({
                "erro": "Email ou senha inválidos"
            }), 401

        agora = datetime.now(timezone.utc)

        # ----------------------------------------------------
        # DESATIVA TOKENS ANTIGOS
        # ----------------------------------------------------

        tokens = (
            db.query(Token)
            .filter(
                Token.usuario_id == usuario.id,
                Token.ativo == True
            )
            .all()
        )

        for token in tokens:

            token.ativo = False

        # ----------------------------------------------------
        # NOVO TOKEN
        # ----------------------------------------------------

        codigo = token_urlsafe(32)

        expira_em = agora + timedelta(hours=2)

        token = Token(
            codigo=codigo,
            ativo=True,
            expira_em=expira_em,
            usuario_id=usuario.id
        )

        db.add(token)

        db.commit()
        db.refresh(token)

        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "token": token.codigo,
            "tipo": "Bearer",
            "expira_em": token.expira_em.isoformat(),
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil
            }
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao realizar login"
        }), 500

    finally:

        db.close()