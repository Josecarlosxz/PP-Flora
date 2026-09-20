from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class EspecieBioma(Base):
    __tablename__ = "especie_bioma"
    
# constraint UNIQUE para impedir duplicação.
    __table_args__ = (
        UniqueConstraint(
            "especie_id",
            "bioma_id",
            name="uq_especie_bioma"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    especie_id: Mapped[int] = mapped_column(
        ForeignKey(
            "especies.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    bioma_id: Mapped[int] = mapped_column(
        ForeignKey(
            "biomas.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    especie = relationship(
        "Especie",
        back_populates="biomas"
    )

    bioma = relationship(
        "Bioma",
        back_populates="especies"
    )