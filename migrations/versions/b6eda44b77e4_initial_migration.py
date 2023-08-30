"""initial migration

Revision ID: b6eda44b77e4
Revises: 
Create Date: 2023-08-30 17:14:39.695597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6eda44b77e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('payment')
    op.drop_table('librarycard')
    op.drop_table('reservation')
    op.drop_table('fine')
    op.drop_table('issue')
    op.drop_table('book')
    op.drop_table('student')
    op.drop_table('author')
    op.drop_table('librarian')
    op.drop_table('book_category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_category',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('librarian',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('phone', sa.INTEGER(), nullable=False),
    sa.Column('joined_date', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('is_librarian', sa.BOOLEAN(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('matric_no', sa.VARCHAR(length=20), nullable=False),
    sa.Column('department', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('img_upload', sa.VARCHAR(length=100), nullable=False),
    sa.Column('joined_date', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('student_status', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('book_category_id', sa.INTEGER(), nullable=False),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), nullable=False),
    sa.Column('version', sa.VARCHAR(length=20), nullable=False),
    sa.Column('publisher', sa.VARCHAR(length=100), nullable=False),
    sa.Column('isbn', sa.INTEGER(), nullable=False),
    sa.Column('img_upload', sa.VARCHAR(length=100), nullable=False),
    sa.Column('total_copies', sa.INTEGER(), nullable=True),
    sa.Column('available_copies', sa.INTEGER(), nullable=True),
    sa.Column('created_date', sa.DATETIME(), nullable=True),
    sa.Column('updated_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['book_category_id'], ['book_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('issue',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('book_id', sa.INTEGER(), nullable=False),
    sa.Column('librarian_id', sa.INTEGER(), nullable=False),
    sa.Column('issue_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['librarian_id'], ['librarian.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fine',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('book_id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('reservation_status', sa.BOOLEAN(), nullable=True),
    sa.Column('reservation_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('librarycard',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('issued_date', sa.DATETIME(), nullable=True),
    sa.Column('expiry_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.Column('payment_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('book_id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('fine_id', sa.INTEGER(), nullable=False),
    sa.Column('issued_date', sa.DATETIME(), nullable=True),
    sa.Column('expiry_date', sa.DATETIME(), nullable=True),
    sa.Column('return_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['fine_id'], ['fine.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
