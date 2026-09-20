import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# CARREGA VARIÁVEIS DO .ENV
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURAÇÕES DO BANCO
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================
# VALIDA CONFIGURAÇÕES
# ============================================================

variaveis_obrigatorias = {
    "DB_HOST": DB_HOST,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}


for nome, valor in variaveis_obrigatorias.items():

    if not valor:

        raise RuntimeError(
            f"{nome} não configurado no arquivo .env"
        )


# ============================================================
# URL DO BANCO
# ============================================================

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ============================================================
# ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


# ============================================================
# SESSÃO
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# BASE DOS MODELS
# ============================================================

Base = declarative_base()