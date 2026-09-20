from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash

from backend.database.database import SessionLocal
from backend.models.usuario import Usuario
from backend.utils.auth import login_required, admin_required


usuario_bp = Blueprint(
    "usuario",
    __name__,
    url_prefix="/usuarios"
)


# ============================================================
# CADASTRAR USUÁRIO
# ============================================================

@usuario_bp.route("/", methods=["POST"])
def create():

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")

        if not nome or not email or not senha:
            return jsonify({
                "erro": "Nome, email e senha são obrigatórios"
            }), 400

        nome = nome.strip()
        email = email.strip().lower()

        if len(nome) < 2:
            return jsonify({
                "erro": "Nome inválido"
            }), 400

        if len(email) > 100:
            return jsonify({
                "erro": "Email muito grande"
            }), 400

        if len(senha) < 8:
            return jsonify({
                "erro": "A senha deve possuir pelo menos 8 caracteres"
            }), 400

        # ----------------------------------------------------
        # PERFIL NÃO É ESCOLHIDO NO CADASTRO PÚBLICO
        #
        # Todo novo usuário começa como professor.
        # Administrador deverá ser definido pelo administrador.
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

        senha_hash = generate_password_hash(senha)

        obj = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil="professor"
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return jsonify({
            "id": obj.id,
            "nome": obj.nome,
            "email": obj.email,
            "perfil": obj.perfil
        }), 201

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar usuário"
        }), 500

    finally:

        db.close()


# ============================================================
# LISTAR USUÁRIOS
# ============================================================

@usuario_bp.route("/", methods=["GET"])
@admin_required
def get_all():

    db = SessionLocal()

    try:

        usuarios = db.query(Usuario).all()

        return jsonify([
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil
            }
            for usuario in usuarios
        ]), 200

    finally:

        db.close()

# ============================================================
# USUÁRIO AUTENTICADO
# ============================================================

@usuario_bp.route("/me", methods=["GET"])
@login_required
def get_me():

    return jsonify({
        "id": g.usuario.id,
        "nome": g.usuario.nome,
        "email": g.usuario.email,
        "perfil": g.usuario.perfil
    }), 200
# ============================================================
# BUSCAR USUÁRIO
# ============================================================

@usuario_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_by_id(id):

    db = SessionLocal()

    try:

        if (
            g.usuario.id != id
            and g.usuario.perfil != "administrador"
        ):
            return jsonify({
                "erro": "Você não possui permissão para acessar este usuário"
            }), 403

        usuario = (
            db.query(Usuario)
            .filter(Usuario.id == id)
            .first()
        )

        if not usuario:
            return jsonify({
                "erro": "Usuário não encontrado"
            }), 404

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }), 200

    finally:

        db.close()


# ============================================================
# ATUALIZAR USUÁRIO
# ============================================================

@usuario_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update(id):

    db = SessionLocal()

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Dados não enviados"
            }), 400

        usuario = (
            db.query(Usuario)
            .filter(Usuario.id == id)
            .first()
        )

        if not usuario:
            return jsonify({
                "erro": "Usuário não encontrado"
            }), 404

        # ----------------------------------------------------
        # SOMENTE O PRÓPRIO USUÁRIO OU ADMIN
        # ----------------------------------------------------

        if (
            g.usuario.id != id
            and g.usuario.perfil != "administrador"
        ):
            return jsonify({
                "erro": "Você não possui permissão para alterar este usuário"
            }), 403

        # ----------------------------------------------------
        # NOME
        # ----------------------------------------------------

        if "nome" in data:

            nome = data["nome"]

            if not isinstance(nome, str):
                return jsonify({
                    "erro": "Nome inválido"
                }), 400

            nome = nome.strip()

            if len(nome) < 2:
                return jsonify({
                    "erro": "Nome inválido"
                }), 400

            usuario.nome = nome

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        if "email" in data:

            email = data["email"]

            if not isinstance(email, str):
                return jsonify({
                    "erro": "Email inválido"
                }), 400

            email = email.strip().lower()

            existente = (
                db.query(Usuario)
                .filter(
                    Usuario.email == email,
                    Usuario.id != id
                )
                .first()
            )

            if existente:
                return jsonify({
                    "erro": "Email já cadastrado"
                }), 409

            usuario.email = email

        # ----------------------------------------------------
        # SENHA
        # ----------------------------------------------------

        if "senha" in data:

            senha = data["senha"]

            if not isinstance(senha, str) or len(senha) < 8:
                return jsonify({
                    "erro": "A senha deve possuir pelo menos 8 caracteres"
                }), 400

            usuario.senha_hash = generate_password_hash(senha)

        # ----------------------------------------------------
        # PERFIL
        #
        # Somente administrador pode alterar perfil.
        # ----------------------------------------------------

        if "perfil" in data:

            if g.usuario.perfil != "administrador":
                return jsonify({
                    "erro": "Somente administradores podem alterar perfis"
                }), 403

            if data["perfil"] not in [
                "professor",
                "administrador"
            ]:
                return jsonify({
                    "erro": "Perfil inválido"
                }), 400

            usuario.perfil = data["perfil"]

        db.commit()
        db.refresh(usuario)

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao atualizar usuário"
        }), 500

    finally:

        db.close()


# ============================================================
# DELETAR USUÁRIO
# ============================================================

@usuario_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete(id):

    db = SessionLocal()

    try:

        usuario = (
            db.query(Usuario)
            .filter(Usuario.id == id)
            .first()
        )

        if not usuario:
            return jsonify({
                "erro": "Usuário não encontrado"
            }), 404

        usuario_id = usuario.id

        db.delete(usuario)
        db.commit()

        return jsonify({
            "mensagem": "Usuário deletado com sucesso",
            "id": usuario_id
        }), 200

    except Exception:

        db.rollback()

        return jsonify({
            "erro": "Erro ao deletar usuário"
        }), 500

    finally:

        db.close()