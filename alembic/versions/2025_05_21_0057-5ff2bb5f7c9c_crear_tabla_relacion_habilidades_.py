"""crear tabla relacion habilidades-pokemon y agregar relacion grupo-generacion

Revision ID: 5ff2bb5f7c9c
Revises: 92a137610411
Create Date: 2025-05-21 00:57:22.586739

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5ff2bb5f7c9c"
down_revision: Union[str, None] = "92a137610411"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "relacion_pokemon_habilidad",
        sa.Column("id_pokemon", sa.Integer, primary_key=True),
        sa.Column("id_habilidad", sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(["id_pokemon"], ["pokemones.id_pokemon"]),
        sa.ForeignKeyConstraint(["id_habilidad"], ["habilidades.id_habilidad"]),
    )
    with op.batch_alter_table("equipos") as batch_op:
        batch_op.create_foreign_key(
            "fk_generacion_equipo",
            "generaciones",
            ["id_generacion_del_equipo"],
            ["id_generacion"],
        )
    pass


def downgrade() -> None:
    op.drop_table("relacion_pokemon_habilidad")
    with op.batch_alter_table("equipos") as batch_op:
        batch_op.drop_constraint("fk_generacion_equipo", type_="foreignkey")
    pass
