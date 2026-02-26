"""crear tabla seed_db para comprobar seed de datos hecho

Revision ID: 365a5b29c7ff
Revises: fcd0d9196dd8
Create Date: 2025-05-25 20:22:25.423392

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "365a5b29c7ff"
down_revision: Union[str, None] = "fcd0d9196dd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        "seed_db",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("hecho", sa.Integer, default=0, nullable=False),
    )

    op.bulk_insert(table, [{"hecho": 0}])


def downgrade() -> None:
    op.drop_table("seed_db")
