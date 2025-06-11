from langchain.llms import OpenAI

from .base import LLMProvider


class OpenAILLMProvider(LLMProvider):
    def __init__(self, model_id: str, api_key: str | None = None):
        self.llm = OpenAI(model_name=model_id, openai_api_key=api_key)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)
