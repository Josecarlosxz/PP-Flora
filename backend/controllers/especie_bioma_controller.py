from flask import Blueprint, request, jsonify

from backend.database.database import SessionLocal
from backend.models.especie_bioma import EspecieBioma
from backend.models.especie import Especie
from backend.models.bioma import Bioma

from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


especie_bioma_bp = Blueprint(
    "especie_bioma",
    __name__,
    url_prefix="/especie_bioma"
)


# ============================================================
# CRIAR RELAÇÃO
# ============================================================

@especie_bioma_bp.route("/", methods=["POST"])
@professor_or_admin_required
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        especie_id = data.get("especie_id")
        bioma_id = data.get("bioma_id")

        if not especie_id or not bioma_id:
            return jsonify({
                "erro": "especie_id e bioma_id são obrigatórios"
            }), 400

        especie = (
            db.query(Especie)
            .filter(Especie.id == especie_id)
            .first()
        )

        if not especie:
            return jsonify({
                "erro": "Espécie não encontrada"
            }), 404

        bioma = (
            db.query(Bioma)
            .filter(Bioma.id == bioma_id)
            .first()
        )

        if not bioma:
            return jsonify({
                "erro": "Bioma não encontrado"
            }), 404

        # ----------------------------------------------------
        # EVITA DUPLICIDADE
        # ----------------------------------------------------

        existente = (
            db.query(EspecieBioma)
            .filter(
                EspecieBioma.especie_id == especie_id,
                EspecieBioma.bioma_id == bioma_id
            )
            .first()
        )

        if existente:
            return jsonify({
                "erro": "Esta espécie já está relacionada a este bioma"
            }), 409

        obj = EspecieBioma(
            especie_id=especie_id,
            bioma_id=bioma_id
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "especie_id": obj.especie_id,
            "bioma_id": obj.bioma_id
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao criar relação"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR RELAÇÕES
# ============================================================

@especie_bioma_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(EspecieBioma).all()

        return jsonify([
            {
                "id": d.id,
                "especie_id": d.especie_id,
                "bioma_id": d.bioma_id
            }
            for d in dados
        ]), 200

    finally:

        db.close()


# ============================================================
# BUSCAR RELAÇÃO
# ============================================================

@especie_bioma_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(EspecieBioma)
            .filter(EspecieBioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Relação não encontrada"
            }), 404

        return jsonify({
            "id": obj.id,
            "especie_id": obj.especie_id,
            "bioma_id": obj.bioma_id
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR RELAÇÃO
# ============================================================

@especie_bioma_bp.route("/<int:id>", methods=["PUT"])
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
            db.query(EspecieBioma)
            .filter(EspecieBioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Relação não encontrada"
            }), 404

        if "especie_id" in data:

            especie = (
                db.query(Especie)
                .filter(Especie.id == data["especie_id"])
                .first()
            )

            if not especie:
                return jsonify({
                    "erro": "Espécie não encontrada"
                }), 404

            obj.especie_id = data["especie_id"]

        if "bioma_id" in data:

            bioma = (
                db.query(Bioma)
                .filter(Bioma.id == data["bioma_id"])
                .first()
            )

            if not bioma:
                return jsonify({
                    "erro": "Bioma não encontrado"
                }), 404

            obj.bioma_id = data["bioma_id"]

        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "especie_id": obj.especie_id,
            "bioma_id": obj.bioma_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar relação"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR RELAÇÃO
# ============================================================

@especie_bioma_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        obj = (
            db.query(EspecieBioma)
            .filter(EspecieBioma.id == id)
            .first()
        )

        if not obj:
            return jsonify({
                "erro": "Relação não encontrada"
            }), 404

        relacao_id = obj.id

        db.delete(obj)
        db.commit()

        return jsonify({
            "mensagem": "Relação deletada com sucesso",
            "id": relacao_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar relação"
        }), 500

    finally:

        db.close()