from typing import List
from langchain.embeddings import OllamaEmbeddings

from .base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_id: str = "nomic-embed-text"):
        self.embeddings = OllamaEmbeddings(model=model_id)

    def embed(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
