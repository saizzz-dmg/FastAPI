"""add content column to postsdatas 

Revision ID: ebd20c9c73d1
Revises: 065d2738f266
Create Date: 2024-04-01 19:03:21.665552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebd20c9c73d1'
down_revision: Union[str, None] = '065d2738f266'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsdatas' , sa.Column('content' , sa.String() , nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('postsdatas' , 'content')
    pass

