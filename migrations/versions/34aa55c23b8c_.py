"""empty message

Revision ID: 34aa55c23b8c
Revises: fd24d63e4f89
Create Date: 2020-12-10 12:13:05.589932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34aa55c23b8c'
down_revision = 'fd24d63e4f89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('schedule_at', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'schedule_at')
    # ### end Alembic commands ###
