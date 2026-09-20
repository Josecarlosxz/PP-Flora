from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Bioma(Base):
    __tablename__ = "biomas"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    clima: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    vegetacao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    especies = relationship(
        "EspecieBioma",
        back_populates="bioma",
        cascade="all, delete-orphan"
    )