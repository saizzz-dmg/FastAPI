"""add last few columns to postsdatas

Revision ID: 47aa87a5e584
Revises: 7b08a06d935b
Create Date: 2024-04-01 19:22:14.617898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47aa87a5e584'
down_revision: Union[str, None] = '7b08a06d935b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsdatas' , sa.Column('post' , sa.Boolean , nullable = False , server_default='TRUE'))
    op.add_column('postsdatas' , sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , nullable = False,
                                           server_default= sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('postsdatas' , 'post')
    op.drop_column('postsdatas'  , 'created_at')
    pass
