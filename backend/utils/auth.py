from datetime import datetime, timezone
from functools import wraps

from flask import request, jsonify, g

from backend.database.database import SessionLocal
from backend.models.token import Token
from backend.models.usuario import Usuario


# ============================================================
# VERIFICA LOGIN
# ============================================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        db = SessionLocal()

        try:

            # ------------------------------------------------
            # PEGA O HEADER
            # ------------------------------------------------

            authorization = request.headers.get("Authorization")

            if not authorization:
                return jsonify({
                    "erro": "Token não informado"
                }), 401

            # ------------------------------------------------
            # VERIFICA BEARER
            # ------------------------------------------------

            partes = authorization.split(" ", 1)

            if len(partes) != 2:
                return jsonify({
                    "erro": "Formato do token inválido"
                }), 401

            tipo, codigo = partes

            if tipo.lower() != "bearer":
                return jsonify({
                    "erro": "Tipo de autenticação inválido"
                }), 401

            codigo = codigo.strip()

            if not codigo:
                return jsonify({
                    "erro": "Token inválido"
                }), 401

            # ------------------------------------------------
            # PROCURA TOKEN
            # ------------------------------------------------

            token = (
                db.query(Token)
                .filter(Token.codigo == codigo)
                .first()
            )

            if not token:
                return jsonify({
                    "erro": "Token inválido"
                }), 401

            # ------------------------------------------------
            # TOKEN ATIVO?
            # ------------------------------------------------

            if not token.ativo:
                return jsonify({
                    "erro": "Token inativo"
                }), 401

            # ------------------------------------------------
            # VERIFICA EXPIRAÇÃO
            # ------------------------------------------------

            agora = datetime.now(timezone.utc)

            expira_em = token.expira_em

            if expira_em.tzinfo is None:
                expira_em = expira_em.replace(
                    tzinfo=timezone.utc
                )

            if expira_em <= agora:

                token.ativo = False

                db.commit()

                return jsonify({
                    "erro": "Token expirado"
                }), 401

            # ------------------------------------------------
            # PROCURA USUÁRIO
            # ------------------------------------------------

            usuario = (
                db.query(Usuario)
                .filter(Usuario.id == token.usuario_id)
                .first()
            )

            if not usuario:
                return jsonify({
                    "erro": "Usuário não encontrado"
                }), 401

            # ------------------------------------------------
            # DISPONIBILIZA PARA AS ROTAS
            # ------------------------------------------------

            g.usuario = usuario
            g.token = token

            return func(*args, **kwargs)

        except Exception:

            db.rollback()

            return jsonify({
                "erro": "Erro ao validar autenticação"
            }), 500

        finally:

            db.close()

    return wrapper


# ============================================================
# SOMENTE ADMINISTRADOR
# ============================================================

def admin_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if g.usuario.perfil != "administrador":
            return jsonify({
                "erro": "Acesso permitido somente para administradores"
            }), 403

        return func(*args, **kwargs)

    return wrapper


# ============================================================
# SOMENTE PROFESSOR
# ============================================================

def professor_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if g.usuario.perfil != "professor":
            return jsonify({
                "erro": "Acesso permitido somente para professores"
            }), 403

        return func(*args, **kwargs)

    return wrapper


# ============================================================
# PROFESSOR OU ADMINISTRADOR
# ============================================================

def professor_or_admin_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if g.usuario.perfil not in [
            "professor",
            "administrador"
        ]:
            return jsonify({
                "erro": "Acesso permitido somente para professores ou administradores"
            }), 403

        return func(*args, **kwargs)

    return wrapper