import os

from flask import Flask
from dotenv import load_dotenv

# CARREGA VARIÁVEIS DO .ENV
load_dotenv()


# ============================================================
# BANCO DE DADOS
# ============================================================

from backend.database.database import engine, Base
from backend.database.seed import criar_admin


# ============================================================
# MODELS
# ============================================================

from backend.models.usuario import Usuario
from backend.models.token import Token
from backend.models.participante import Participante
from backend.models.especie import Especie
from backend.models.animal import Animal
from backend.models.planta import Planta
from backend.models.bioma import Bioma
from backend.models.especie_bioma import EspecieBioma


# ============================================================
# FRONTEND
# ============================================================

from frontend.routes import frontend_bp


# ============================================================
# CONTROLLERS
# ============================================================

from backend.controllers.usuario_controller import usuario_bp
from backend.controllers.login_controller import login_bp
from backend.controllers.logout_controller import logout_bp
from backend.controllers.cadastro_controller import cadastro_bp
from backend.controllers.especie_controller import especie_bp
from backend.controllers.animal_controller import animal_bp
from backend.controllers.planta_controller import planta_bp
from backend.controllers.bioma_controller import bioma_bp
from backend.controllers.especie_bioma_controller import especie_bioma_bp
from backend.controllers.token_controller import token_bp
from backend.controllers.participante_controller import participante_bp


def create_app():

    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    app.config["JSON_SORT_KEYS"] = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    if not app.config["SECRET_KEY"]:
        raise RuntimeError(
            "SECRET_KEY não configurada no arquivo .env"
        )


    # ========================================================
    # BANCO DE DADOS
    # ========================================================

    print("====================================")
    print("Verificando banco de dados...")

    try:

        Base.metadata.create_all(bind=engine)

        print("Tabelas verificadas/criadas com sucesso!")

    except Exception as e:

        print("Erro ao criar tabelas:")
        print(e)

        raise


    # ========================================================
    # ADMINISTRADOR
    # ========================================================

    try:

        criar_admin()

    except Exception as e:

        print("Erro ao verificar administrador:")
        print(e)

        raise


    # ========================================================
    # FRONTEND
    # ========================================================

    app.register_blueprint(frontend_bp)


    # ========================================================
    # CONTROLLERS
    # ========================================================

    app.register_blueprint(usuario_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(especie_bp)
    app.register_blueprint(animal_bp)
    app.register_blueprint(planta_bp)
    app.register_blueprint(bioma_bp)
    app.register_blueprint(especie_bioma_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(participante_bp)


    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )