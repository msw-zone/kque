from typing import List
from qdrant_client import QdrantClient
from .base import VectorClient

from providers.embeddings import get_embedding_provider


class QdrantVectorClient(VectorClient):
    def __init__(self, url: str, collection: str, embedding_cfg: dict | None = None):
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.embedding = get_embedding_provider(embedding_cfg or {})

    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        vector = self.embedding.embed(query)
        results = self.client.search(collection_name=self.collection, query_vector=vector, top=k)
        return [hit.payload.get("text", "") for hit in results]
