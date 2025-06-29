"""empty message

Revision ID: 02c363d7ff92
Revises: faed849ae2c8
Create Date: 2025-06-26 07:10:52.680614

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '02c363d7ff92'
down_revision = 'faed849ae2c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'location_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'location_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
