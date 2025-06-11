from langchain.llms import Ollama

from .base import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, model_id: str):
        self.llm = Ollama(model=model_id)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)
