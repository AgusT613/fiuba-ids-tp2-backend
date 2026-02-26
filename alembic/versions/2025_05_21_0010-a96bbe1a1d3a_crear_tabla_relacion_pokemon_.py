"""crear tabla relacion pokemon-generaciones y agregar relacion movimiento-generacion

Revision ID: a96bbe1a1d3a
Revises: 32a849832433
Create Date: 2025-05-21 00:10:01.448272

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a96bbe1a1d3a"
down_revision: Union[str, None] = "32a849832433"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "relacion_pokemon_generacion",
        sa.Column("id_pokemon", sa.Integer, primary_key=True),
        sa.Column("id_generacion", sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(["id_pokemon"], ["pokemones.id_pokemon"]),
        sa.ForeignKeyConstraint(["id_generacion"], ["generaciones.id_generacion"]),
    )
    with op.batch_alter_table("movimientos") as batch_op:
        batch_op.create_foreign_key(
            "fk_generacion_movimiento",
            "generaciones",
            ["id_generacion_del_movimiento"],
            ["id_generacion"],
        )
    pass


def downgrade() -> None:
    op.drop_table("relacion_pokemon_generacion")
    with op.batch_alter_table("movimientos") as batch_op:
        batch_op.drop_constraint("fk_generacion_movimiento", type_="foreignkey")
    pass
