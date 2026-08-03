"""migrate_trace_configurations_to_system_settings

Revision ID: 3c4351fa93f3
Revises: 739f2db1fc49
Create Date: 2026-08-03 12:43:11.827037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c4351fa93f3'
down_revision: Union[str, Sequence[str], None] = '739f2db1fc49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    results = conn.execute(sa.text("SELECT service_name, enabled FROM trace_configurations")).fetchall()
    
    for row in results:
        conn.execute(
            sa.text("INSERT INTO system_settings (key, settings, updated_at) VALUES (:key, :settings, :updated_at)"),
            {
                "key": f"tracing.{row.service_name}",
                "settings": {"enabled": row.enabled},
                "updated_at": sa.func.now()
            }
        )

def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM system_settings WHERE key LIKE 'tracing.%'"))
