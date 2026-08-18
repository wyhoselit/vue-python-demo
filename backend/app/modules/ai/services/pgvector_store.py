from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.modules.ai.services.vector_store import SearchResult, VectorStore
from app.modules.core.config import settings
from app.modules.llm.rag.models import Document


class PGVectorStore(VectorStore):
    def __init__(self):
        async_engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            pool_size=10,
            max_overflow=20,
        )
        self.AsyncSessionLocal = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
        self.engine = async_engine

    async def _ensure_hnsw_index(self, session: AsyncSession) -> None:
        await session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_documents_embedding_hnsw "
                "ON documents USING hnsw (embedding vector_cosine_ops) "
                f"WITH (m = {settings.PGVECTOR_HNSW_M}, ef_construction = {settings.PGVECTOR_HNSW_EF_CONSTRUCTION})"
            )
        )

    async def add_documents(self, documents: list[dict]) -> None:
        async with self.AsyncSessionLocal() as session:
            for doc in documents:
                db_doc = Document(
                    id=int(doc["id"]) if doc["id"].isdigit() else hash(doc["id"]),
                    content=doc["document"],
                    embedding=doc["embedding"],
                    meta_data=doc.get("metadata"),
                )
                session.add(db_doc)
            await session.commit()

    async def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        filter_metadata: dict | None = None,
    ) -> list[SearchResult]:
        async with self.AsyncSessionLocal() as session:
            from pgvector.sqlalchemy import ScalarFunction

            query = (
                select(
                    Document.id,
                    Document.content,
                    Document.meta_data,
                    Document.embedding.cast(
                        ScalarFunction("1 - cosine_distance")
                    ).label("score"),
                )
                .order_by(Document.embedding.cosine_distance(query_embedding))
                .limit(limit)
            )

            if filter_metadata:
                where_clause = text("meta_data @> :filter")
                query = query.where(where_clause)
                results = await session.execute(query, {"filter": filter_metadata})
            else:
                results = await session.execute(query)

            rows = results.fetchall()
            return [
                SearchResult(
                    id=str(row.id),
                    text=row.content,
                    score=float(row.score) if hasattr(row, "score") else 0.0,
                    metadata=row.meta_data or {},
                )
                for row in rows
            ]

    async def delete(self, ids: list[str]) -> None:
        async with self.AsyncSessionLocal() as session:
            int_ids = [int(i) for i in ids if str(i).isdigit()]
            if int_ids:
                await session.execute(
                    text("DELETE FROM documents WHERE id = ANY(:ids)"),
                    {"ids": int_ids},
                )
                await session.commit()

    async def health_check(self) -> bool:
        try:
            async with self.AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
                return True
        except Exception:  # noqa: BLE001
            return False
