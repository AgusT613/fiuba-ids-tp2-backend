"""crear tabla evoluciones pokemon y tabla intermedia que relaciona pokemon-evoluciones

Revision ID: d116810d6016
Revises: 9626f40ddfc9
Create Date: 2025-05-22 13:11:55.257284

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d116810d6016"
down_revision: Union[str, None] = "9626f40ddfc9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "evoluciones",
        sa.Column(
            "fk_id_pokemon",
            sa.Integer,
            sa.ForeignKey("pokemones.id_pokemon"),
            nullable=False,
        ),
        sa.Column("id_evolucion", sa.Integer, primary_key=True),
        sa.Column("nombre_evolucion", sa.Text),
        sa.Column("imagen", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("evoluciones")
