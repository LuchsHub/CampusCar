"""empty message

Revision ID: fbeb3a1e022a
Revises: 1a31ce608336
Create Date: 2025-06-26 06:36:04.888530

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'fbeb3a1e022a'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('postal_code', sqlmodel.sql.sqltypes.AutoString(length=5), nullable=False),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('street', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('house_number', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('n_seats', sa.Integer(), nullable=False),
    sa.Column('model', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('brand', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('rater_id', sa.Uuid(), nullable=False),
    sa.Column('rating_value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stop',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('time_of_arrival', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ride',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('recurring_id', sa.Uuid(), nullable=False),
    sa.Column('driver_id', sa.Uuid(), nullable=False),
    sa.Column('car_id', sa.Uuid(), nullable=False),
    sa.Column('recurring_mon', sa.Boolean(), nullable=False),
    sa.Column('recurring_tue', sa.Boolean(), nullable=False),
    sa.Column('recurring_wed', sa.Boolean(), nullable=False),
    sa.Column('recurring_thu', sa.Boolean(), nullable=False),
    sa.Column('recurring_fri', sa.Boolean(), nullable=False),
    sa.Column('recurring_sat', sa.Boolean(), nullable=False),
    sa.Column('recurring_sun', sa.Boolean(), nullable=False),
    sa.Column('n_co_driver', sa.Integer(), nullable=False),
    sa.Column('starting_time', sa.DateTime(), nullable=False),
    sa.Column('time_of_arrial', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('item')
    op.add_column('user', sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True))
    op.add_column('user', sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True))
    op.add_column('user', sa.Column('user_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False))
    op.add_column('user', sa.Column('rating', sa.Float(), nullable=False))
    op.add_column('user', sa.Column('points', sa.Integer(), nullable=False))
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('user', 'points')
    op.drop_column('user', 'rating')
    op.drop_column('user', 'user_name')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    op.create_table('item',
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='item_owner_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='item_pkey')
    )
    op.drop_table('ride')
    op.drop_table('stop')
    op.drop_table('rating')
    op.drop_table('car')
    op.drop_table('location')
    # ### end Alembic commands ###
