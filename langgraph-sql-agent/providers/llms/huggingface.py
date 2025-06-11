from langchain.llms import HuggingFaceHub

from .base import LLMProvider


class HuggingFaceLLMProvider(LLMProvider):
    def __init__(self, model_id: str, api_token: str | None = None):
        self.llm = HuggingFaceHub(repo_id=model_id, huggingfacehub_api_token=api_token)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)
