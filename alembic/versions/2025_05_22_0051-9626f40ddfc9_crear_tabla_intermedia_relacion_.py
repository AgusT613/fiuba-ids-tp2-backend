"""crear tabla intermedia relacion debilidades del tipo del pokemon

Revision ID: 9626f40ddfc9
Revises: 9db1eecdc65e
Create Date: 2025-05-22 00:51:38.599241

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9626f40ddfc9"
down_revision: Union[str, None] = "9db1eecdc65e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "debilidades_del_tipo",
        sa.Column("id_debilidades_tipo", sa.Integer, primary_key=True),
        sa.Column(
            "fk_id_tipo", sa.Integer, sa.ForeignKey("tipos.id_tipo"), nullable=False
        ),
        sa.Column(
            "fk_id_debilidad",
            sa.Integer,
            sa.ForeignKey("debilidades.id_debilidad"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("debilidades_del_tipo")
