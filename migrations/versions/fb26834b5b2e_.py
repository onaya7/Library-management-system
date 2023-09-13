"""empty message

Revision ID: fb26834b5b2e
Revises: a54d5ea4820d
Create Date: 2023-09-12 02:06:21.153057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb26834b5b2e'
down_revision = 'a54d5ea4820d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_copies', sa.Integer(), nullable=True))
        batch_op.drop_column('total_copie')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_copie', sa.INTEGER(), nullable=True))
        batch_op.drop_column('total_copies')

    # ### end Alembic commands ###