from flask import Blueprint, request, jsonify, g

from backend.database.database import SessionLocal
from backend.models.especie import Especie
from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


especie_bp = Blueprint(
    "especie",
    __name__,
    url_prefix="/especies"
)


# ============================================================
# CRIAR ESPÉCIE
# ============================================================

@especie_bp.route("/", methods=["POST"])
@professor_or_admin_required
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        if not data.get("nome_popular"):
            return jsonify({
                "erro": "nome_popular é obrigatório"
            }), 400

        if not data.get("nome_cientifico"):
            return jsonify({
                "erro": "nome_cientifico é obrigatório"
            }), 400

        obj = Especie(
            nome_popular=data["nome_popular"].strip(),
            nome_cientifico=data["nome_cientifico"].strip(),
            descricao=data.get("descricao"),
            tipo="especie",
            usuario_id=g.usuario.id
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome_popular": obj.nome_popular,
            "nome_cientifico": obj.nome_cientifico,
            "descricao": obj.descricao,
            "usuario_id": obj.usuario_id,
            "tipo": obj.tipo
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar espécie"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR ESPÉCIES
# ============================================================

@especie_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Especie).all()

        return jsonify([
            {
                "id": e.id,
                "nome_popular": e.nome_popular,
                "nome_cientifico": e.nome_cientifico,
                "descricao": e.descricao,
                "usuario_id": e.usuario_id,
                "tipo": e.tipo
            }
            for e in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR ESPÉCIE
# ============================================================

@especie_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Especie)
            .filter(Especie.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Espécie não encontrada"
            }), 404

        return jsonify({
            "id": obj.id,
            "nome_popular": obj.nome_popular,
            "nome_cientifico": obj.nome_cientifico,
            "descricao": obj.descricao,
            "usuario_id": obj.usuario_id,
            "tipo": obj.tipo
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR ESPÉCIE
# ============================================================

@especie_bp.route("/<int:id>", methods=["PUT"])
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
            db.query(Especie)
            .filter(Especie.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Espécie não encontrada"
            }), 404

        if "nome_popular" in data:
            obj.nome_popular = data["nome_popular"].strip()

        if "nome_cientifico" in data:
            obj.nome_cientifico = data["nome_cientifico"].strip()

        if "descricao" in data:
            obj.descricao = data["descricao"]

        # NÃO ALTERAMOS:
        # id
        # usuario_id
        # tipo

        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome_popular": obj.nome_popular,
            "nome_cientifico": obj.nome_cientifico,
            "descricao": obj.descricao,
            "usuario_id": obj.usuario_id,
            "tipo": obj.tipo
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar espécie"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR ESPÉCIE
# ============================================================

@especie_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Especie)
            .filter(Especie.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Espécie não encontrada"
            }), 404

        especie_id = obj.id

        db.delete(obj)
        db.commit()

        return jsonify({
            "mensagem": "Espécie deletada com sucesso",
            "id": especie_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar espécie"
        }), 500

    finally:

        db.close()