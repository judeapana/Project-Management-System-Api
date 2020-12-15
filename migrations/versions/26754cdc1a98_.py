"""empty message

Revision ID: 26754cdc1a98
Revises: 8b0dc855879c
Create Date: 2020-12-08 09:00:28.094920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26754cdc1a98'
down_revision = '8b0dc855879c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing_info',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('ticket_comment', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ticket_comment', 'user', ['admin_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ticket_comment', type_='foreignkey')
    op.drop_column('ticket_comment', 'admin_id')
    op.drop_table('billing_info')
    # ### end Alembic commands ###
