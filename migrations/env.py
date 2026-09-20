from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv


# ============================================================
# ADICIONA A RAIZ DO PROJETO AO PYTHONPATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# CARREGA O .ENV
# ============================================================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


# ============================================================
# IMPORTA O BASE DO SQLALCHEMY
# ============================================================

from backend.database.database import Base


# ============================================================
# IMPORTA TODOS OS MODELS
# ============================================================
# É importante importar todos eles para que o SQLAlchemy
# registre as tabelas em Base.metadata.
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
# CONFIGURAÇÃO DO ALEMBIC
# ============================================================

config = context.config


# ============================================================
# LOGGING
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# METADATA DOS MODELS
# ============================================================

target_metadata = Base.metadata


# ============================================================
# URL DO BANCO
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ============================================================
# MIGRATION OFFLINE
# ============================================================

def run_migrations_offline() -> None:
    """
    Executa as migrations em modo offline.

    Nesse modo o Alembic não cria uma conexão real
    com o banco. Ele apenas gera o SQL.
    """

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# MIGRATION ONLINE
# ============================================================

def run_migrations_online() -> None:
    """
    Executa as migrations conectando diretamente
    ao banco MySQL.
    """

    configuration = config.get_section(
        config.config_ini_section
    )

    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# EXECUÇÃO
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()