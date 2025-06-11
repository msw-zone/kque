from typing import List
from langchain.embeddings import HuggingFaceEmbeddings

from .base import EmbeddingProvider


class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_id: str):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_id)

    def embed(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
