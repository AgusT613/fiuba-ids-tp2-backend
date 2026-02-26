"""crear tabla relacion pokemon-tipo y agregar relacion movimento-tipo

Revision ID: 92a137610411
Revises: a96bbe1a1d3a
Create Date: 2025-05-21 00:28:37.231844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "92a137610411"
down_revision: Union[str, None] = "a96bbe1a1d3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "relacion_pokemon_tipo",
        sa.Column("id_pokemon", sa.Integer, primary_key=True),
        sa.Column("id_tipo", sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(["id_pokemon"], ["pokemones.id_pokemon"]),
        sa.ForeignKeyConstraint(["id_tipo"], ["tipos.id_tipo"]),
    )
    with op.batch_alter_table("movimientos") as batch_op:
        batch_op.create_foreign_key(
            "fk_tipo_movimiento",
            "tipos",
            ["id_tipo_del_movimiento"],
            ["id_tipo"],
        )
    pass


def downgrade() -> None:
    op.drop_table("relacion_pokemon_tipo")
    with op.batch_alter_table("movimientos") as batch_op:
        batch_op.drop_constraint("fk_tipo_movimiento", type_="foreignkey")
    pass
