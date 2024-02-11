"""initial

Revision ID: 00d695e6331f
Revises: 
Create Date: 2024-01-30 12:55:40.396586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00d695e6331f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('login', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('user_history',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid', 'user_id'),
    sa.UniqueConstraint('uuid', 'user_id'),
    postgresql_partition_by='HASH (user_id)'
    )
    #op.execute(
    #    """CREATE TABLE user_history (
    #        uuid uuid DEFAULT gen_random_uuid() NOT NULL,
    #        user_id uuid NOT NULL REFERENCES users,
    #        user_agent VARCHAR(255) NOT NULL,
    #        refresh_token TEXT NOT NULL,
    #        is_active boolean NOT NULL,
    #        created_at DATE NOT NULL,
    #        updated_at DATE,
    #        PRIMARY KEY (uuid)
    #    ) PARTITION BY HASH(user_id);
    #    """
    #)
    op.execute(
        "CREATE TABLE hash_part_0 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 0);"
    )
    op.execute(
        "CREATE TABLE hash_part_1 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 1);"
    )
    op.execute(
        "CREATE TABLE hash_part_2 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 2);"
    )
    op.execute(
        "CREATE TABLE hash_part_3 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 3);"
    )
    op.execute(
        "CREATE TABLE hash_part_4 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 4);"
    )
    op.execute(
        "CREATE TABLE hash_part_5 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 5);"
    )
    op.execute(
        "CREATE TABLE hash_part_6 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 6);"
    )
    op.execute(
        "CREATE TABLE hash_part_7 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 7);"
    )
    op.execute(
        "CREATE TABLE hash_part_8 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 8);"
    )
    op.execute(
        "CREATE TABLE hash_part_9 PARTITION OF user_history "
        "FOR VALUES WITH (MODULUS 10, REMAINDER 9);"
    )
    op.create_table('users_roles',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('role_id', sa.Uuid(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.uuid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('user_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
