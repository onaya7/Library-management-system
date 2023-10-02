"""empty message

Revision ID: 00d252fd0ccc
Revises: 880386704702
Create Date: 2023-10-02 23:24:48.645051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00d252fd0ccc'
down_revision = '880386704702'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('issue', schema=None) as batch_op:
        batch_op.alter_column('librarian_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('issue', schema=None) as batch_op:
        batch_op.alter_column('librarian_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
