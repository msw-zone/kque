from typing import List
from qdrant_client import QdrantClient
from .base import VectorClient


class QdrantVectorClient(VectorClient):
    def __init__(self, url: str, collection: str):
        self.client = QdrantClient(url=url)
        self.collection = collection

    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        # Here we assume embeddings already exist in Qdrant
        results = self.client.search(collection_name=self.collection, query_text=query, top=k)
        return [hit.payload.get("text", "") for hit in results]
