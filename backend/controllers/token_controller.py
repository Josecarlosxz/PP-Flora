from flask import Blueprint, jsonify

from backend.database.database import SessionLocal
from backend.models.token import Token
from backend.utils.auth import admin_required


token_bp = Blueprint(
    "token",
    __name__,
    url_prefix="/tokens"
)


# ============================================================
# LISTAR TOKENS
# ============================================================

@token_bp.route("/", methods=["GET"])
@admin_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Token).all()

        return jsonify([
            {
                "id": token.id,
                "codigo": token.codigo,
                "ativo": token.ativo,
                "expira_em": (
                    token.expira_em.isoformat()
                    if token.expira_em
                    else None
                ),
                "usuario_id": token.usuario_id
            }
            for token in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR TOKEN
# ============================================================

@token_bp.route("/<int:id>", methods=["GET"])
@admin_required
def get_by_id(id):

    db = SessionLocal()

    try:

        token = (
            db.query(Token)
            .filter(Token.id == id)
            .first()
        )

        if not token:
            return jsonify({
                "erro": "Token não encontrado"
            }), 404

        return jsonify({
            "id": token.id,
            "ativo": token.ativo,
            "codigo": token.codigo,
            "expira_em": (
                token.expira_em.isoformat()
                if token.expira_em
                else None
            ),
            "usuario_id": token.usuario_id
        }), 200

    finally:

        db.close()


# ============================================================
# DESATIVAR TOKEN
# ============================================================

@token_bp.route("/<int:id>/desativar", methods=["PUT"])
@admin_required
def deactivate(id):

    db = SessionLocal()

    try:

        token = (
            db.query(Token)
            .filter(Token.id == id)
            .first()
        )

        if not token:
            return jsonify({
                "erro": "Token não encontrado"
            }), 404

        token.ativo = False

        db.commit()
        db.refresh(token)

        return jsonify({
            "mensagem": "Token desativado com sucesso",
            "id": token.id,
            "ativo": token.ativo
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao desativar token"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR TOKEN
# ============================================================

@token_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        token = (
            db.query(Token)
            .filter(Token.id == id)
            .first()
        )

        if not token:
            return jsonify({
                "erro": "Token não encontrado"
            }), 404

        token_id = token.id

        db.delete(token)
        db.commit()

        return jsonify({
            "mensagem": "Token deletado com sucesso",
            "id": token_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar token"
        }), 500

    finally:

        db.close()