"""Empty Init

Revision ID: a814e53218d6
Revises: 
Create Date: 2023-11-07 20:26:03.346965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a814e53218d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade():
    op.create_table(
        'students',
        sa.Column('sn', sa.Integer, primary_key=True),
        sa.Column('firstname', sa.String),
        sa.Column('lastname', sa.String),
        sa.Column('gender', sa.CHAR),
        sa.Column('age', sa.Integer),
    )

    op.create_table(
        'courses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('description', sa.String),
    )

    op.create_table(
        'registrations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('students.sn')),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.id')),
    )

def downgrade():
    op.drop_table('registrations')
    op.drop_table('courses')
    op.drop_table('students')
