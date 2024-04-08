"""create posts table

Revision ID: 065d2738f266
Revises: 
Create Date: 2024-04-01 18:44:10.629471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '065d2738f266'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('postsdatas' , sa.Column('id' , sa.Integer(),nullable = False , primary_key=True),
                    sa.Column('title' , sa.String() , nullable = False))


def downgrade() -> None:
    op.drop_table('postsdatas')
    pass


