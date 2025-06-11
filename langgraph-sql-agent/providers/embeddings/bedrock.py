from typing import List

from langchain.embeddings import BedrockEmbeddings

from .base import EmbeddingProvider


class BedrockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_id: str, region: str | None = None):
        self.embeddings = BedrockEmbeddings(model_id=model_id, region_name=region)

    def embed(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
