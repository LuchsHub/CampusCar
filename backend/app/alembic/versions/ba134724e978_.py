"""empty message

Revision ID: ba134724e978
Revises: 9add1390d8a6
Create Date: 2025-06-26 06:59:13.786107

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ba134724e978'
down_revision = '9add1390d8a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ride', sa.Column('driver_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'ride', 'user', ['driver_id'], ['id'])
    op.add_column('stop', sa.Column('user_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'stop', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stop', type_='foreignkey')
    op.drop_column('stop', 'user_id')
    op.drop_constraint(None, 'ride', type_='foreignkey')
    op.drop_column('ride', 'driver_id')
    # ### end Alembic commands ###
