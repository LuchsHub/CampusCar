"""Merge branches

Revision ID: b3c1b0ab37f8
Revises: bb65a9e03779, c67f505a24b9
Create Date: 2025-07-01 15:54:40.771434

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'b3c1b0ab37f8'
down_revision = ('bb65a9e03779', 'c67f505a24b9')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
