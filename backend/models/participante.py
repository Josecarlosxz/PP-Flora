from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    token_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tokens.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    token = relationship(
        "Token",
        back_populates="participantes"
    )