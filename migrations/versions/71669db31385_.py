"""empty message

Revision ID: 71669db31385
Revises: 
Create Date: 2023-09-03 10:35:33.196181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71669db31385'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('img_upload',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Float(precision=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('img_upload',
               existing_type=sa.Float(precision=100),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###