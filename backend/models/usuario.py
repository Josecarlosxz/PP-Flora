from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    # ============================================================
    # ID
    # ============================================================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # ============================================================
    # NOME
    # ============================================================

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # ============================================================
    # EMAIL
    # ============================================================

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # ============================================================
    # SENHA
    # ============================================================

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # ============================================================
    # PERFIL
    #
    # Valores esperados:
    #
    # usuario
    # professor
    # administrador
    #
    # IMPORTANTE:
    # O usuário comum não poderá escolher "administrador"
    # no cadastro.
    # ============================================================

    perfil: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="usuario"
    )

    # ============================================================
    # RELACIONAMENTO COM ESPÉCIES
    # ============================================================

    especies = relationship(
        "Especie",
        back_populates="usuario"
    )

    # ============================================================
    # RELACIONAMENTO COM TOKENS
    # ============================================================

    tokens = relationship(
        "Token",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )