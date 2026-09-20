from flask import Blueprint, request, jsonify

from backend.database.database import SessionLocal
from backend.models.bioma import Bioma
from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


bioma_bp = Blueprint(
    "bioma",
    __name__,
    url_prefix="/biomas"
)


# ============================================================
# CRIAR BIOMA
# ============================================================

@bioma_bp.route("/", methods=["POST"])
@professor_or_admin_required
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        campos = [
            "nome",
            "clima",
            "vegetacao"
        ]

        for campo in campos:

            if not data.get(campo):
                return jsonify({
                    "erro": f"{campo} é obrigatório"
                }), 400

        obj = Bioma(
            nome=data["nome"].strip(),
            descricao=data.get("descricao"),
            clima=data["clima"].strip(),
            vegetacao=data["vegetacao"].strip()
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "descricao": obj.descricao,
            "clima": obj.clima,
            "vegetacao": obj.vegetacao
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar bioma"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR BIOMAS
# ============================================================

@bioma_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Bioma).all()

        return jsonify([
            {
                "id": b.id,
                "nome": b.nome,
                "descricao": b.descricao,
                "clima": b.clima,
                "vegetacao": b.vegetacao
            }
            for b in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR BIOMA
# ============================================================

@bioma_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Bioma)
            .filter(Bioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Bioma não encontrado"
            }), 404

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "descricao": obj.descricao,
            "clima": obj.clima,
            "vegetacao": obj.vegetacao
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR BIOMA
# ============================================================

@bioma_bp.route("/<int:id>", methods=["PUT"])
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
            db.query(Bioma)
            .filter(Bioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Bioma não encontrado"
            }), 404

        if "nome" in data:
            obj.nome = data["nome"].strip()

        if "descricao" in data:
            obj.descricao = data["descricao"]

        if "clima" in data:
            obj.clima = data["clima"].strip()

        if "vegetacao" in data:
            obj.vegetacao = data["vegetacao"].strip()

        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "descricao": obj.descricao,
            "clima": obj.clima,
            "vegetacao": obj.vegetacao
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar bioma"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR BIOMA
# ============================================================

@bioma_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Bioma)
            .filter(Bioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Bioma não encontrado"
            }), 404

        bioma_id = obj.id

        db.delete(obj)
        db.commit()

        return jsonify({
            "mensagem": "Bioma deletado com sucesso",
            "id": bioma_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar bioma"
        }), 500

    finally:

        db.close()