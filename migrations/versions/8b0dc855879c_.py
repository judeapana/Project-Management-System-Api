"""empty message

Revision ID: 8b0dc855879c
Revises: e655fbc8f9c8
Create Date: 2020-12-08 05:59:32.849581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b0dc855879c'
down_revision = 'e655fbc8f9c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('img', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'img')
    # ### end Alembic commands ###
