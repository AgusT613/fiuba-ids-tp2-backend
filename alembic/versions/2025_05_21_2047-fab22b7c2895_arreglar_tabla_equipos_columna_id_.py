"""arreglar tabla equipos columna id_generacion_del_equipo

Revision ID: fab22b7c2895
Revises: 05612f9677b2
Create Date: 2025-05-21 20:47:14.893798

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fab22b7c2895"
down_revision: Union[str, None] = "05612f9677b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("equipos") as batch_op:
        batch_op.drop_column("id_generacion_del_equipo")
        batch_op.add_column(sa.Column("id_generacion_del_equipo", sa.Integer))
    pass


def downgrade() -> None:
    with op.batch_alter_table("equipos") as batch_op:
        batch_op.drop_column("id_generacion_del_equipo")
        batch_op.add_column(sa.Column("id_generacion_del_equipo", sa.Text))
    pass
