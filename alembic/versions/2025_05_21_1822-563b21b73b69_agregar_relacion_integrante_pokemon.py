"""agregar relacion integrante-pokemon

Revision ID: 563b21b73b69
Revises: 5ff2bb5f7c9c
Create Date: 2025-05-21 18:22:33.621181

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "563b21b73b69"
down_revision: Union[str, None] = "5ff2bb5f7c9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("integrante") as batch_op:
        batch_op.create_foreign_key(
            "fk_pokemon_integrante",
            "pokemones",
            ["id_pokemon"],
            ["id_pokemon"],
        )
    pass


def downgrade() -> None:
    with op.batch_alter_table("integrante") as batch_op:
        batch_op.drop_constraint("fk_pokemon_integrante", type_="foreignkey")
    pass
