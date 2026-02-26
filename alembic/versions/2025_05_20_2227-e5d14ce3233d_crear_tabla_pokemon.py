"""crear tabla pokemon

Revision ID: e5d14ce3233d
Revises: b411724a6482
Create Date: 2025-05-20 22:27:20.146454

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5d14ce3233d"
down_revision: Union[str, None] = "b411724a6482"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemones",
        sa.Column("id_pokemon", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("altura", sa.Float, nullable=False),
        sa.Column("peso", sa.Float, nullable=False),
        sa.Column("ataque", sa.Integer, nullable=True),
        sa.Column("defensa", sa.Integer, nullable=True),
        sa.Column("ataque_especial", sa.Integer, nullable=True),
        sa.Column("defensa_especial", sa.Integer, nullable=True),
        sa.Column("puntos_de_golpe", sa.Integer, nullable=True),
        sa.Column("velocidad", sa.Integer, nullable=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("pokemones")
    pass
