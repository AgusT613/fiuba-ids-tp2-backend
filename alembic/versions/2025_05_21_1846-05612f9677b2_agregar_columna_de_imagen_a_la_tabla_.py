"""agregar columna de imagen a la tabla pokemones

Revision ID: 05612f9677b2
Revises: 563b21b73b69
Create Date: 2025-05-21 18:46:44.108069

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05612f9677b2"
down_revision: Union[str, None] = "563b21b73b69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("pokemones") as batch_op:
        batch_op.add_column(sa.Column("imagen", sa.Text))
    pass


def downgrade() -> None:
    with op.batch_alter_table("pokemones") as batch_op:
        batch_op.drop_column("imagen")
    pass
