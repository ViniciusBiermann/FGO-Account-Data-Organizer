"""Start DB

Revision ID: c18712017617
Revises: 
Create Date: 2023-02-05 11:44:21.037588

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c18712017617'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True, autoincrement=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
                    sa.Column('username', sa.String(), nullable=False, unique=True, index=True),
                    sa.Column('password', sa.String()))
    op.create_table('servants',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
                    sa.Column('name', sa.String()),
                    sa.Column('name_jp', sa.String()),
                    sa.Column('servant_class', sa.String()),
                    sa.Column('rarity', sa.Integer())
                    )
    op.create_table('masters',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
                    sa.Column('in_game_id', sa.String(), nullable=False),
                    sa.Column('owner_user_id', sa.Integer()),
                    sa.Column('name', sa.String()),
                    sa.Column('birthday', sa.Date()),
                    sa.Column('gender', sa.String()),
                    sa.Column('device', sa.String()),
                    sa.Column('download_date', sa.Date()),
                    sa.Column('last_access', sa.DateTime()),
                    sa.Column('master_level', sa.Integer()),
                    sa.Column('saint_quartz', sa.Integer()),
                    sa.Column('paid_saint_quartz', sa.Integer()),
                    sa.Column('rare_prisms', sa.Integer()),
                    sa.Column('unregistered_spirit_origin', sa.Integer()),
                    sa.Column('recovery_number', sa.String()),
                    sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], name='user_masters_fk', ondelete='CASCADE')
                    )
    # op.create_foreign_key('user_masters_fk', source_table='masters', referent_table='users',
    #                       local_cols=['owner_user_id'], remote_cols=['id'], ondelete='CASCADE')

    op.create_table('master_servants',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True, autoincrement=True),
                    sa.Column('master_id', sa.Integer()),
                    sa.Column('servant_id', sa.Integer()),
                    sa.Column('level', sa.Integer()),
                    sa.Column('bond_level', sa.Integer()),
                    sa.Column('np_level', sa.Integer()),
                    sa.Column('skill_1_level', sa.Integer()),
                    sa.Column('skill_2_level', sa.Integer()),
                    sa.Column('skill_3_level', sa.Integer()),
                    sa.Column('summon_date', sa.Date()),
                    sa.Column('is_favourite', sa.Boolean()),
                    sa.ForeignKeyConstraint(['master_id'], ['masters.id'], name='master_servants_fk', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['servant_id'], ['servants.id'], name='servant_master_servants_fk', ondelete='CASCADE')
                    )
    # op.create_foreign_key('master_servants_fk', source_table='master_servants', referent_table='masters',
    #                       local_cols=['master_id'], remote_cols=['id'], ondelete='CASCADE')
    # op.create_foreign_key('servant_master_servants_fk', source_table='master_servants', referent_table='servants',
    #                       local_cols=['servant_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_table('master_servants')
    op.drop_table('servants')
    op.drop_table('masters')
    op.drop_table('users')
