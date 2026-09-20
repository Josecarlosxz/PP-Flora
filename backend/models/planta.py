from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.especie import Especie


class Planta(Especie):
    __tablename__ = "plantas"

    id: Mapped[int] = mapped_column(
        ForeignKey(
            "especies.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    tipo_folha: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    medicinal: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "planta"
    }