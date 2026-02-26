"""crear tabla tipos

Revision ID: 294cdee50f83
Revises: f6572fe23519
Create Date: 2025-05-20 22:07:06.595224

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "294cdee50f83"
down_revision: Union[str, None] = "f6572fe23519"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tipos",
        sa.Column("id_tipo", sa.Integer, primary_key=True),
        sa.Column("nombre_tipo", sa.Text, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("tipos")
    pass
