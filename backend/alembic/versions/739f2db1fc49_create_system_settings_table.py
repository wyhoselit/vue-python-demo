"""create_system_settings_table

Revision ID: 739f2db1fc49
Revises: f2a7b8c9d0e1
Create Date: 2026-08-03 12:38:13.674359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '739f2db1fc49'
down_revision: Union[str, Sequence[str], None] = 'f2a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('system_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_system_settings_id'), 'system_settings', ['id'], unique=False)
    op.create_index(op.f('ix_system_settings_key'), 'system_settings', ['key'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_system_settings_key'), table_name='system_settings')
    op.drop_index(op.f('ix_system_settings_id'), table_name='system_settings')
    op.drop_table('system_settings')

