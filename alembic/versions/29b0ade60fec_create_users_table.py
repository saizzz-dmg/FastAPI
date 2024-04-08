"""create users table 

Revision ID: 29b0ade60fec
Revises: ebd20c9c73d1
Create Date: 2024-04-01 19:07:55.599723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29b0ade60fec'
down_revision: Union[str, None] = 'ebd20c9c73d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('userlogininfo',
                    sa.Column('id' , sa.Integer() , nullable = False),
                    sa.Column('email' , sa.String() , nullable = False) , 
                    sa.Column('password' , sa.String() , nullable = False),
                    sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , 
                              server_default=sa.text('now()') , nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('userlogininfo')
    pass
