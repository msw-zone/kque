from typing import List
from langchain.embeddings import OpenAIEmbeddings

from .base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str | None = None):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def embed(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
