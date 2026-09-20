from flask import Blueprint, request, jsonify, g

from backend.database.database import SessionLocal
from backend.models.planta import Planta
from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


planta_bp = Blueprint(
    "planta",
    __name__,
    url_prefix="/plantas"
)


# ============================================================
# CRIAR PLANTA
# ============================================================

@planta_bp.route("/", methods=["POST"])
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
            "nome_popular",
            "nome_cientifico",
            "tipo_folha",
            "medicinal"
        ]

        for campo in campos:

            if campo not in data:
                return jsonify({
                    "erro": f"{campo} é obrigatório"
                }), 400

        if not isinstance(data["medicinal"], bool):
            return jsonify({
                "erro": "medicinal deve ser booleano"
            }), 400

        obj = Planta(
            nome_popular=data["nome_popular"].strip(),
            nome_cientifico=data["nome_cientifico"].strip(),
            descricao=data.get("descricao"),
            usuario_id=g.usuario.id,
            tipo_folha=data["tipo_folha"].strip(),
            medicinal=data["medicinal"],
            tipo="planta"
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
            "tipo": obj.tipo,
            "tipo_folha": obj.tipo_folha,
            "medicinal": obj.medicinal
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar planta"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR PLANTAS
# ============================================================

@planta_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Planta).all()

        return jsonify([
            {
                "id": p.id,
                "nome_popular": p.nome_popular,
                "nome_cientifico": p.nome_cientifico,
                "descricao": p.descricao,
                "usuario_id": p.usuario_id,
                "tipo": p.tipo,
                "tipo_folha": p.tipo_folha,
                "medicinal": p.medicinal
            }
            for p in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR PLANTA
# ============================================================

@planta_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Planta)
            .filter(Planta.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Planta não encontrada"
            }), 404

        return jsonify({
            "id": obj.id,
            "nome_popular": obj.nome_popular,
            "nome_cientifico": obj.nome_cientifico,
            "descricao": obj.descricao,
            "usuario_id": obj.usuario_id,
            "tipo": obj.tipo,
            "tipo_folha": obj.tipo_folha,
            "medicinal": obj.medicinal
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR PLANTA
# ============================================================

@planta_bp.route("/<int:id>", methods=["PUT"])
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
            db.query(Planta)
            .filter(Planta.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Planta não encontrada"
            }), 404

        campos = [
            "nome_popular",
            "nome_cientifico",
            "descricao",
            "tipo_folha"
        ]

        for campo in campos:

            if campo in data:
                setattr(obj, campo, data[campo])

        if "medicinal" in data:

            if not isinstance(data["medicinal"], bool):
                return jsonify({
                    "erro": "medicinal deve ser booleano"
                }), 400

            obj.medicinal = data["medicinal"]

        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome_popular": obj.nome_popular,
            "nome_cientifico": obj.nome_cientifico,
            "descricao": obj.descricao,
            "usuario_id": obj.usuario_id,
            "tipo": obj.tipo,
            "tipo_folha": obj.tipo_folha,
            "medicinal": obj.medicinal
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar planta"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR PLANTA
# ============================================================

@planta_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(Planta)
            .filter(Planta.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Planta não encontrada"
            }), 404

        planta_id = obj.id

        db.delete(obj)
        db.commit()

        return jsonify({
            "mensagem": "Planta deletada com sucesso",
            "id": planta_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar planta"
        }), 500

    finally:

        db.close()