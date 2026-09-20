from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Especie(Base):
    __tablename__ = "especies"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome_popular: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    nome_cientifico: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="especie"
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    usuario = relationship(
        "Usuario",
        back_populates="especies"
    )

    biomas = relationship(
        "EspecieBioma",
        back_populates="especie",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "especie",
    }