"""Initial migration

Revision ID: 4c56ad199fd0
Revises: 
Create Date: 2021-02-19 14:04:30.979435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c56ad199fd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_behaviours',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('endless', sa.Boolean(), nullable=False),
    sa.Column('time_seconds', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_behaviours')
    # ### end Alembic commands ###
