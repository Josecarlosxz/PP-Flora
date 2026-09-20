from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Token(Base):

    __tablename__ = "tokens"

    # ============================================================
    # ID
    # ============================================================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # ============================================================
    # CÓDIGO DO TOKEN
    #
    # Esse valor é gerado pelo servidor.
    # O usuário nunca escolhe o token.
    # ============================================================

    codigo: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )

    # ============================================================
    # STATUS
    # ============================================================

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # ============================================================
    # EXPIRAÇÃO
    # ============================================================

    expira_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )

    # ============================================================
    # USUÁRIO DONO DO TOKEN
    # ============================================================

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # ============================================================
    # RELACIONAMENTO COM USUÁRIO
    # ============================================================

    usuario = relationship(
        "Usuario",
        back_populates="tokens"
    )

    # ============================================================
    # RELACIONAMENTO COM PARTICIPANTES
    # ============================================================

    participantes = relationship(
        "Participante",
        back_populates="token",
        cascade="all, delete-orphan"
    )