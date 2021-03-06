"""empty message

Revision ID: c8c2fea609d4
Revises: 6f690c6fc72c
Create Date: 2020-12-15 11:09:34.732150

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'c8c2fea609d4'
down_revision = '6f690c6fc72c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('date', sa.DateTime(), nullable=False))
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'date')
    # ### end Alembic commands ###
