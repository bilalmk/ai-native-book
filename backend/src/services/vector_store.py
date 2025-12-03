"""
Qdrant vector store service.

Manages vector search operations using Qdrant Cloud.
"""

import logging
from typing import List, Dict, Any
from uuid import UUID, uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    ScoredPoint,
    Filter,
)
from src.config import settings
from src.models.document import ChunkPayload

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Service for vector search using Qdrant."""

    def __init__(self):
        """Initialize Qdrant client."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.dimension = settings.openai_embedding_dimension

    async def ensure_collection_exists(self) -> None:
        """
        Create collection if it doesn't exist.

        Creates a collection with cosine distance metric and configured dimensions.
        """
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to ensure collection exists: {str(e)}")
            raise

    async def upsert_chunks(
        self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]
    ) -> None:
        """
        Upsert document chunks with embeddings to Qdrant.

        Args:
            chunks: List of chunk metadata dictionaries
            embeddings: List of embedding vectors

        Raises:
            Exception: If upsert fails
        """
        try:
            points = []
            for chunk, embedding in zip(chunks, embeddings):
                point = PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload=chunk,
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Upserted {len(points)} chunks to Qdrant")

        except Exception as e:
            logger.error(f"Failed to upsert chunks: {str(e)}")
            raise

    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar document chunks.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of matching chunks with metadata and scores

        Raises:
            Exception: If search fails
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=score_threshold,
            )

            chunks = []
            for result in results:
                chunk = {
                    "title": result.payload.get("title", "Untitled"),
                    "file_path": result.payload.get("file_path", ""),
                    "chunk_text": result.payload.get("chunk_text", ""),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "total_chunks": result.payload.get("total_chunks", 1),
                    "relevance_score": result.score,
                }
                chunks.append(chunk)

            logger.info(f"Found {len(chunks)} chunks above threshold {score_threshold}")
            return chunks

        except Exception as e:
            logger.error(f"Failed to search vector store: {str(e)}")
            raise

    async def check_health(self) -> bool:
        """
        Check if Qdrant is accessible.

        Returns:
            True if healthy, False otherwise
        """
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get collection statistics.

        Returns:
            Dictionary with collection info (point count, etc.)
        """
        try:
            info = await self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {str(e)}")
            return {}

    async def delete_collection(self) -> bool:
        """
        Delete the collection.

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection: {str(e)}")
            return False
