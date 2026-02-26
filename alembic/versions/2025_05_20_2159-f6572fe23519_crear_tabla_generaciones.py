"""crear tabla generaciones

Revision ID: f6572fe23519
Revises:
Create Date: 2025-05-20 21:59:34.383229

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6572fe23519"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "generaciones",
        sa.Column("id_generacion", sa.Integer, primary_key=True),
        sa.Column("nombre_generacion", sa.Text, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("generaciones")
    pass
