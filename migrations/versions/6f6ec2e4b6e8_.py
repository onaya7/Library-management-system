"""empty message

Revision ID: 6f6ec2e4b6e8
Revises: 45d00e7a6657
Create Date: 2023-09-18 13:25:17.808807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f6ec2e4b6e8'
down_revision = '45d00e7a6657'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('librarian', schema=None) as batch_op:
        batch_op.alter_column('alternative_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alternative_i', sa.String(length=36), nullable=False))
        batch_op.drop_column('alternative_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alternative_id', sa.VARCHAR(length=36), nullable=True))
        batch_op.drop_column('alternative_i')

    with op.batch_alter_table('librarian', schema=None) as batch_op:
        batch_op.alter_column('alternative_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)

    # ### end Alembic commands ###