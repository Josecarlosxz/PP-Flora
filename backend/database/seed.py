
from backend.database.database import SessionLocal

# ============================================================
# CARREGA OS MODELS
#
# Importante:
# Participante precisa estar registrado antes que o SQLAlchemy
# inicialize os relacionamentos de Token.
# ============================================================

from backend.models.usuario import Usuario
from backend.models.token import Token
from backend.models.participante import Participante

from werkzeug.security import generate_password_hash


def criar_admin():

    session = SessionLocal()

    try:

        # ====================================================
        # VERIFICA SE O ADMIN JÁ EXISTE
        # ====================================================

        admin = (
            session.query(Usuario)
            .filter(
                Usuario.email == "admin@biosistema.com"
            )
            .first()
        )

        if admin:

            print("Administrador já existe.")

            return

        # ====================================================
        # CRIA ADMINISTRADOR
        # ====================================================

        admin = Usuario(

            nome="Administrador",

            email="admin@biosistema.com",

            senha_hash=generate_password_hash(
                "admin123"
            ),

            perfil="administrador"

        )

        session.add(admin)

        session.commit()

        session.refresh(admin)

        print("====================================")
        print("Administrador criado com sucesso!")
        print("Email : admin@biosistema.com")
        print("Senha : admin123")
        print("====================================")

    except Exception as e:

        session.rollback()

        print("Erro ao criar administrador:")
        print(e)

    finally:

        session.close()


if __name__ == "__main__":

    criar_admin()

