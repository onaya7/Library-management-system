"""empty message

Revision ID: bc5817e39cc1
Revises: ada88f0b732d
Create Date: 2023-09-30 22:09:15.433930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc5817e39cc1'
down_revision = 'ada88f0b732d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fine', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fine', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###