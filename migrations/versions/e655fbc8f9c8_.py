"""empty message

Revision ID: e655fbc8f9c8
Revises: 02cd17647853
Create Date: 2020-12-08 02:59:28.241440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e655fbc8f9c8'
down_revision = '02cd17647853'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('active', sa.Boolean(), nullable=False))
    op.add_column('ticket', sa.Column('title', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket', 'title')
    op.drop_column('project', 'active')
    # ### end Alembic commands ###
