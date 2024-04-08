"""add foreign key to posts table

Revision ID: 7b08a06d935b
Revises: 29b0ade60fec
Create Date: 2024-04-01 19:14:29.128689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b08a06d935b'
down_revision: Union[str, None] = '29b0ade60fec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsdatas',sa.Column('user_id' , sa.Integer() , nullable = False))
    op.create_foreign_key('posts_users_fk' , source_table = 'postsdatas' , referent_table = 'userlogininfo',
                          local_cols = ['user_id'] , remote_cols = ['id'] , ondelete="CASCADE")

    pass



def downgrade() -> None:
    op.drop_constraint('posts_users_fk','postsdatas' )
    op.drop_column('postsdatas' , 'user_id')
    pass