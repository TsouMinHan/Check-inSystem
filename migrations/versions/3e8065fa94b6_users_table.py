"""users table

Revision ID: 3e8065fa94b6
Revises: 
Create Date: 2020-07-11 13:51:01.690749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e8065fa94b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=4), nullable=True),
    sa.Column('course_name', sa.String(length=10), nullable=True),
    sa.Column('teacher_id', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=4), nullable=True),
    sa.Column('student_id', sa.String(length=9), nullable=True),
    sa.Column('date', sa.String(length=10), nullable=True),
    sa.Column('attend', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('father_name', sa.String(length=10), nullable=True),
    sa.Column('mother_name', sa.String(length=10), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=32), nullable=True),
    sa.Column('class_name', sa.String(length=10), nullable=True),
    sa.Column('student_id', sa.String(length=9), nullable=True),
    sa.Column('date_of_birth', sa.String(length=10), nullable=True),
    sa.Column('line_id', sa.String(length=64), nullable=True),
    sa.Column('face_data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('take_course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=4), nullable=True),
    sa.Column('student_id', sa.String(length=9), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('teacher_id', sa.String(length=6), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher')
    op.drop_table('take_course')
    op.drop_table('student')
    op.drop_table('record')
    op.drop_table('course')
    # ### end Alembic commands ###
