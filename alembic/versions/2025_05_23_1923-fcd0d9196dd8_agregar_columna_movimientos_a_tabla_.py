"""agregar columna movimientos a tabla integrantes y tabla intermedia integrante-movimiento

Revision ID: fcd0d9196dd8
Revises: d116810d6016
Create Date: 2025-05-23 19:23:50.459433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fcd0d9196dd8"
down_revision: Union[str, None] = "d116810d6016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "relacion_integrante_movimiento",
        sa.Column(
            "id_integrante",
            sa.Integer,
            sa.ForeignKey("integrante.id_integrante"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "id_movimiento",
            sa.Integer,
            sa.ForeignKey("movimientos.id_movimiento"),
            primary_key=True,
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("relacion_integrante_movimiento")
    pass
