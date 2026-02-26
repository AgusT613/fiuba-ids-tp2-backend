"""crear tabla debilidades

Revision ID: 9db1eecdc65e
Revises: 5ff2bb5f7c9c
Create Date: 2025-05-22 00:32:58.289124

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9db1eecdc65e"
down_revision: Union[str, None] = "fab22b7c2895"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "debilidades",
        sa.Column("id_debilidad", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.String(50)),
    )


def downgrade() -> None:
    op.drop_table("debilidades")
