"""crear tabla habilidades

Revision ID: b411724a6482
Revises: 294cdee50f83
Create Date: 2025-05-20 22:11:45.652098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b411724a6482"
down_revision: Union[str, None] = "294cdee50f83"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "habilidades",
        sa.Column("id_habilidad", sa.Integer, primary_key=True),
        sa.Column("nombre_habilidad", sa.Text, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("habilidades")
    pass
