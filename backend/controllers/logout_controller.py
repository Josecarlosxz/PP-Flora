from flask import Blueprint, jsonify, g

from backend.database.database import SessionLocal
from backend.models.token import Token
from backend.utils.auth import login_required


logout_bp = Blueprint(
    "logout",
    __name__,
    url_prefix="/logout"
)


# ============================================================
# LOGOUT
# ============================================================

@logout_bp.route("/", methods=["POST"])
@login_required
def logout():

    db = SessionLocal()

    try:

        token = (
            db.query(Token)
            .filter(Token.id == g.token.id)
            .first()
        )

        if not token:
            return jsonify({
                "erro": "Token não encontrado"
            }), 401

        token.ativo = False

        db.commit()

        return jsonify({
            "mensagem": "Logout realizado com sucesso"
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao realizar logout"
        }), 500

    finally:

        db.close()