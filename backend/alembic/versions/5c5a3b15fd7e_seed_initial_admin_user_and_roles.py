"""seed initial admin user and roles

Revision ID: 5c5a3b15fd7e
Revises: 8c4783b0e69d2
Create Date: 2026-07-27 20:43:29.380502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c5a3b15fd7e'
down_revision: Union[str, Sequence[str], None] = '8c4783b0e69d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa
from app.core.security import hash_password

def upgrade() -> None:
    # Seed roles
    op.bulk_insert(
        sa.table('roles', sa.column('name', sa.String)),
        [
            {'name': 'admin'},
            {'name': 'user'}
        ]
    )

    # Seed admin user
    hashed_pwd = hash_password("admin123")
    op.execute(
        sa.text("INSERT INTO users (email, hashed_password) VALUES (:email, :hashed_password)")
        .bindparams(email="admin@example.com", hashed_password=hashed_pwd)
    )
    
    # Assign admin role
    op.execute(
        sa.text("""
            INSERT INTO user_roles (user_id, role_id)
            SELECT u.id, r.id
            FROM users u, roles r
            WHERE u.email = 'admin@example.com' AND r.name = 'admin'
        """)
    )

def downgrade() -> None:
    op.execute("DELETE FROM user_roles")
    op.execute("DELETE FROM users WHERE email = 'admin@example.com'")
    op.execute("DELETE FROM roles WHERE name IN ('admin', 'user')")

