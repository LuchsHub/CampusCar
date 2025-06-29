"""empty message

Revision ID: fa4ed70c8e13
Revises: b27d541a7d0e
Create Date: 2025-06-26 06:43:04.446483

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'fa4ed70c8e13'
down_revision = 'b27d541a7d0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rating', sa.Column('user_id', sa.Uuid(), nullable=False))
    op.add_column('rating', sa.Column('rater_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'rating', 'user', ['rater_id'], ['id'])
    op.create_foreign_key(None, 'rating', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('rating', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'rating')
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.drop_constraint(None, 'rating', type_='foreignkey')
    op.drop_column('rating', 'rater_id')
    op.drop_column('rating', 'user_id')
    # ### end Alembic commands ###
