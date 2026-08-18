"""Create documents table with pgvector and HNSW index

Revision ID: a1b2c3d4e5f6_vec
Revises: 8c4783b0e69d
Create Date: 2026-08-18 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "8c4783b0e69d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", sa.Text()),
        sa.Column("meta_data", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_index("ix_documents_id", "documents", ["id"])
    conn.execute(
        sa.text(
            "CREATE INDEX idx_documents_embedding_hnsw "
            "ON documents USING hnsw (embedding vector_cosine_ops) "
            "WITH (m = 16, ef_construction = 64)"
        )
    )


def downgrade() -> None:
    op.drop_index("idx_documents_embedding_hnsw", table_name="documents")
    op.drop_index("ix_documents_id", table_name="documents")
    op.drop_table("documents")