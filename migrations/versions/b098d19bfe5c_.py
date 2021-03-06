"""empty message

Revision ID: b098d19bfe5c
Revises: 7e62dc62da38
Create Date: 2020-12-16 21:56:52.002843

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b098d19bfe5c'
down_revision = '7e62dc62da38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('read', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'read')
    # ### end Alembic commands ###
