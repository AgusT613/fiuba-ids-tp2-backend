"""crear tabla movimiento

Revision ID: 32a849832433
Revises: 35d6b18cdcc0
Create Date: 2025-05-20 23:23:01.333279

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32a849832433"
down_revision: Union[str, None] = "35d6b18cdcc0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movimientos",
        sa.Column("id_movimiento", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("id_generacion_del_movimiento", sa.Integer, nullable=False),
        sa.Column("id_tipo_del_movimiento", sa.Integer, nullable=False),
        sa.Column("poder", sa.Integer, nullable=False),
        sa.Column("PP", sa.Integer, nullable=False),
        sa.Column("precision", sa.Integer, nullable=False),
        sa.Column("clase_de_daño", sa.Integer, nullable=False),
        sa.Column("efecto", sa.Integer, nullable=False),
    )
    op.create_table(
        "pokemones_que_pueden_aprender_un_movimiento",
        sa.Column("id_movimiento", sa.Integer(), primary_key=True),
        sa.Column("id_pokemon", sa.Integer(), primary_key=True),
        sa.Column(
            "metodo_de_aprendizaje", sa.Integer(), primary_key=True, nullable=False
        ),
        sa.ForeignKeyConstraint(["id_movimiento"], ["movimientos.id_movimiento"]),
        sa.ForeignKeyConstraint(["id_pokemon"], ["pokemones.id_pokemon"]),
    )
    pass


def downgrade() -> None:
    op.drop_table("movimientos")
    op.drop_table("pokemones_que_pueden_aprender_un_movimiento")
    pass
