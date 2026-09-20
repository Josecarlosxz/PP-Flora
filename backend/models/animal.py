from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.especie import Especie


class Animal(Especie):
    __tablename__ = "animais"

    id: Mapped[int] = mapped_column(
        ForeignKey(
            "especies.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    dieta: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    habitat_especifico: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "animal"
    }