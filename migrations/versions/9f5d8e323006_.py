"""empty message

Revision ID: 9f5d8e323006
Revises: 34aa55c23b8c
Create Date: 2020-12-10 12:14:49.481424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5d8e323006'
down_revision = '34aa55c23b8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('title', sa.String(100), nullable=False))
    op.drop_column('notification', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('name', sa.BINARY(length=16), nullable=True))
    op.drop_column('notification', 'title')
    # ### end Alembic commands ###
