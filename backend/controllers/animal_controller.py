from flask import Blueprint, request, jsonify, g

from backend.database.database import SessionLocal
from backend.models.animal import Animal
from backend.utils.auth import (
    login_required,
    professor_or_admin_required,
    admin_required
)


# ============================================================
# BLUEPRINT DE ANIMAIS
# ============================================================

animal_bp = Blueprint(
    "animal",
    __name__,
    url_prefix="/animais"
)


# ============================================================
# CRIAR ANIMAL
# Professor ou Administrador
# ============================================================

@animal_bp.route("/", methods=["POST"])
@professor_or_admin_required
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        # ----------------------------------------------------
        # CAMPOS OBRIGATÓRIOS
        # ----------------------------------------------------

        campos_obrigatorios = [
            "nome_popular",
            "nome_cientifico",
            "dieta",
            "habitat_especifico"
        ]

        for campo in campos_obrigatorios:

            if campo not in data:
                return jsonify({
                    "erro": f"{campo} é obrigatório"
                }), 400

            if not isinstance(data[campo], str):
                return jsonify({
                    "erro": f"{campo} deve ser texto"
                }), 400

            if not data[campo].strip():
                return jsonify({
                    "erro": f"{campo} não pode estar vazio"
                }), 400

        # ----------------------------------------------------
        # LIMPA OS DADOS
        # ----------------------------------------------------

        nome_popular = data["nome_popular"].strip()
        nome_cientifico = data["nome_cientifico"].strip()
        dieta = data["dieta"].strip()
        habitat_especifico = data["habitat_especifico"].strip()

        descricao = data.get("descricao")

        if descricao is not None:

            if not isinstance(descricao, str):
                return jsonify({
                    "erro": "descricao deve ser texto"
                }), 400

            descricao = descricao.strip()

        # ----------------------------------------------------
        # USUÁRIO VEM DO TOKEN
        #
        # Nunca recebemos usuario_id pelo JSON.
        # ----------------------------------------------------

        usuario_id = g.usuario.id

        # ----------------------------------------------------
        # CRIA ANIMAL
        # ----------------------------------------------------

        obj = Animal(
            nome_popular=nome_popular,
            nome_cientifico=nome_cientifico,
            descricao=descricao,
            usuario_id=usuario_id,
            dieta=dieta,
            habitat_especifico=habitat_especifico,
            tipo="animal"
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
            "dieta": obj.dieta,
            "habitat_especifico": obj.habitat_especifico
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar animal"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR ANIMAIS
# Qualquer usuário autenticado
# ============================================================

@animal_bp.route("/", methods=["GET"])
@login_required
def get_all():

    db = SessionLocal()

    try:

        dados = db.query(Animal).all()

        response = [

            {
                "id": animal.id,
                "nome_popular": animal.nome_popular,
                "nome_cientifico": animal.nome_cientifico,
                "descricao": animal.descricao,
                "usuario_id": animal.usuario_id,
                "tipo": animal.tipo,
                "dieta": animal.dieta,
                "habitat_especifico": animal.habitat_especifico
            }

            for animal in dados
        ]

        return jsonify(response), 200

    finally:

        db.close()


# ============================================================
# BUSCAR ANIMAL POR ID
# Qualquer usuário autenticado
# ============================================================

@animal_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        animal = (
            db.query(Animal)
            .filter(Animal.id == id)
            .first()
        )

        if not animal:
            return jsonify({
                "erro": "Animal não encontrado"
            }), 404

        return jsonify({
            "id": animal.id,
            "nome_popular": animal.nome_popular,
            "nome_cientifico": animal.nome_cientifico,
            "descricao": animal.descricao,
            "usuario_id": animal.usuario_id,
            "tipo": animal.tipo,
            "dieta": animal.dieta,
            "habitat_especifico": animal.habitat_especifico
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR ANIMAL
# Professor ou Administrador
# ============================================================

@animal_bp.route("/<int:id>", methods=["PUT"])
@professor_or_admin_required
def update(id):

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        animal = (
            db.query(Animal)
            .filter(Animal.id == id)
            .first()
        )

        if not animal:
            return jsonify({
                "erro": "Animal não encontrado"
            }), 404

        # ----------------------------------------------------
        # CAMPOS PERMITIDOS
        # ----------------------------------------------------

        if "nome_popular" in data:

            if not isinstance(data["nome_popular"], str):
                return jsonify({
                    "erro": "nome_popular deve ser texto"
                }), 400

            nome = data["nome_popular"].strip()

            if not nome:
                return jsonify({
                    "erro": "nome_popular não pode estar vazio"
                }), 400

            animal.nome_popular = nome

        if "nome_cientifico" in data:

            if not isinstance(data["nome_cientifico"], str):
                return jsonify({
                    "erro": "nome_cientifico deve ser texto"
                }), 400

            nome = data["nome_cientifico"].strip()

            if not nome:
                return jsonify({
                    "erro": "nome_cientifico não pode estar vazio"
                }), 400

            animal.nome_cientifico = nome

        if "descricao" in data:

            if data["descricao"] is not None:

                if not isinstance(data["descricao"], str):
                    return jsonify({
                        "erro": "descricao deve ser texto"
                    }), 400

                animal.descricao = data["descricao"].strip()

            else:

                animal.descricao = None

        if "dieta" in data:

            if not isinstance(data["dieta"], str):
                return jsonify({
                    "erro": "dieta deve ser texto"
                }), 400

            dieta = data["dieta"].strip()

            if not dieta:
                return jsonify({
                    "erro": "dieta não pode estar vazia"
                }), 400

            animal.dieta = dieta

        if "habitat_especifico" in data:

            if not isinstance(data["habitat_especifico"], str):
                return jsonify({
                    "erro": "habitat_especifico deve ser texto"
                }), 400

            habitat = data["habitat_especifico"].strip()

            if not habitat:
                return jsonify({
                    "erro": "habitat_especifico não pode estar vazio"
                }), 400

            animal.habitat_especifico = habitat

        # ----------------------------------------------------
        # NÃO PERMITIMOS ALTERAR:
        #
        # id
        # usuario_id
        # tipo
        #
        # Esses campos são controlados pelo sistema.
        # ----------------------------------------------------

        db.commit()
        db.refresh(animal)

        return jsonify({
            "id": animal.id,
            "nome_popular": animal.nome_popular,
            "nome_cientifico": animal.nome_cientifico,
            "descricao": animal.descricao,
            "usuario_id": animal.usuario_id,
            "tipo": animal.tipo,
            "dieta": animal.dieta,
            "habitat_especifico": animal.habitat_especifico
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar animal"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR ANIMAL
# Somente Administrador
# ============================================================

@animal_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        animal = (
            db.query(Animal)
            .filter(Animal.id == id)
            .first()
        )

        if not animal:
            return jsonify({
                "erro": "Animal não encontrado"
            }), 404

        animal_id = animal.id

        db.delete(animal)
        db.commit()

        return jsonify({
            "mensagem": "Animal deletado com sucesso",
            "id": animal_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar animal"
        }), 500

    finally:

        db.close()

