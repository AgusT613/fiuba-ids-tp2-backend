"""crear tabla grupo

Revision ID: 35d6b18cdcc0
Revises: e5d14ce3233d
Create Date: 2025-05-20 23:08:58.314372

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "35d6b18cdcc0"
down_revision: Union[str, None] = "e5d14ce3233d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "equipos",
        sa.Column("id_equipo", sa.Integer, primary_key=True),
        sa.Column("nombre_equipo", sa.Text, nullable=False),
        sa.Column("id_generacion_del_equipo", sa.Text, nullable=False),
    )
    op.create_table(
        "integrante",
        sa.Column("id_integrante", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("id_integrante_dentro_del_grupo", sa.Integer(), nullable=False),
        sa.Column("apodo", sa.String(), nullable=False),
        sa.Column("id_pokemon", sa.Integer(), nullable=False),
        sa.Column("id_equipo", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_equipo"], ["equipos.id_equipo"]),
    )
    pass


def downgrade() -> None:
    op.drop_table("equipos")
    op.drop_table("integrante")
    pass
