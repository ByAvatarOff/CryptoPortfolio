"""add constraint unique 

Revision ID: bf739663d859
Revises: 4ca29aa2d379
Create Date: 2024-08-20 16:09:15.427699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf739663d859'
down_revision: Union[str, None] = '4ca29aa2d379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('portfolio_name_key', 'portfolio', type_='unique')
    op.create_unique_constraint(None, 'portfolio', ['name', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'portfolio', type_='unique')
    op.create_unique_constraint('portfolio_name_key', 'portfolio', ['name'])
    # ### end Alembic commands ###
