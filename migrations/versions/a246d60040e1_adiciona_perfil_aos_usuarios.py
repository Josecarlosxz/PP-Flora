"""adiciona perfil aos usuarios

Revision ID: a246d60040e1
Revises: 18211820b0bf
Create Date: 2026-08-25 15:36:18.860321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a246d60040e1'
down_revision: Union[str, Sequence[str], None] = '18211820b0bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Cria a coluna temporariamente permitindo NULL
    op.add_column(
        "usuarios",
        sa.Column(
            "perfil",
            sa.String(length=20),
            nullable=True
        )
    )

    # 2. Define o perfil padrão para usuários existentes
    op.execute(
        "UPDATE usuarios "
        "SET perfil = 'usuario' "
        "WHERE perfil IS NULL"
    )

    # 3. Torna a coluna obrigatória
    op.alter_column(
        "usuarios",
        "perfil",
        existing_type=sa.String(length=20),
        nullable=False
    )


def downgrade() -> None:

    op.drop_column(
        "usuarios",
        "perfil"
    )