from __future__ import annotations

from .openai import OpenAIEmbeddingProvider
from .bedrock import BedrockEmbeddingProvider
from .huggingface import HuggingFaceEmbeddingProvider
from .ollama import OllamaEmbeddingProvider


def get_embedding_provider(cfg: dict):
    provider = cfg.get("provider", "openai")
    model_id = cfg.get("model_id")
    if provider == "openai":
        return OpenAIEmbeddingProvider(api_key=cfg.get("api_key"))
    if provider == "bedrock":
        return BedrockEmbeddingProvider(model_id=model_id, region=cfg.get("region"))
    if provider == "huggingface":
        return HuggingFaceEmbeddingProvider(model_id=model_id)
    if provider == "ollama":
        return OllamaEmbeddingProvider(model_id=model_id)
    raise ValueError(f"Unknown embedding provider: {provider}")
