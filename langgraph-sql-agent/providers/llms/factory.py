from __future__ import annotations

from .openai import OpenAILLMProvider
from .bedrock import BedrockLLMProvider
from .huggingface import HuggingFaceLLMProvider
from .ollama import OllamaLLMProvider


def get_llm_provider(cfg: dict):
    provider = cfg.get("provider", "openai")
    model_id = cfg.get("model_id")
    if provider == "openai":
        return OpenAILLMProvider(model_id=model_id, api_key=cfg.get("api_key"))
    if provider == "bedrock":
        return BedrockLLMProvider(model_id=model_id, region=cfg.get("region"))
    if provider == "huggingface":
        return HuggingFaceLLMProvider(model_id=model_id, api_token=cfg.get("api_token"))
    if provider == "ollama":
        return OllamaLLMProvider(model_id=model_id)
    raise ValueError(f"Unknown LLM provider: {provider}")
