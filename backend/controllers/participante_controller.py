from flask import Blueprint, request, jsonify

from backend.database.database import SessionLocal
from backend.models.participante import Participante
from backend.models.token import Token

from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


participante_bp = Blueprint(
    "participante",
    __name__,
    url_prefix="/participantes"
)


# ============================================================
# CRIAR PARTICIPANTE
# ============================================================

@participante_bp.route("/", methods=["POST"])
@professor_or_admin_required
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        nome = data.get("nome")
        token_id = data.get("token_id")

        if not nome or not token_id:
            return jsonify({
                "erro": "nome e token_id são obrigatórios"
            }), 400

        # ----------------------------------------------------
        # VERIFICA TOKEN
        # ----------------------------------------------------

        token = (
            db.query(Token)
            .filter(Token.id == token_id)
            .first()
        )

        if not token:
            return jsonify({
                "erro": "Token não encontrado"
            }), 404

        if not token.ativo:
            return jsonify({
                "erro": "Token está inativo"
            }), 400

        obj = Participante(
            nome=nome.strip(),
            token_id=token_id
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "token_id": obj.token_id
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar participante"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR PARTICIPANTES
# ============================================================

@participante_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Participante).all()

        return jsonify([
            {
                "id": p.id,
                "nome": p.nome,
                "token_id": p.token_id
            }
            for p in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR PARTICIPANTE
# ============================================================

@participante_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Participante)
            .filter(Participante.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Participante não encontrado"
            }), 404

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "token_id": obj.token_id
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR PARTICIPANTE
# ============================================================

@participante_bp.route("/<int:id>", methods=["PUT"])
@professor_or_admin_required
def update(id):

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        obj = (
            db.query(Participante)
            .filter(Participante.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Participante não encontrado"
            }), 404

        if "nome" in data:

            nome = data["nome"]

            if not isinstance(nome, str) or len(nome.strip()) < 2:
                return jsonify({
                    "erro": "Nome inválido"
                }), 400

            obj.nome = nome.strip()

        # token_id NÃO é alterado por esta rota.

        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "token_id": obj.token_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar participante"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR PARTICIPANTE
# ============================================================

@participante_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Participante)
            .filter(Participante.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Participante não encontrado"
            }), 404

        participante_id = obj.id

        db.delete(obj)
        db.commit()

        return jsonify({
            "mensagem": "Participante deletado com sucesso",
            "id": participante_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar participante"
        }), 500

    finally:

        db.close()