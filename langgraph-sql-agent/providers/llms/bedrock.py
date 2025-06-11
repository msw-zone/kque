from langchain.llms.bedrock import Bedrock

from .base import LLMProvider


class BedrockLLMProvider(LLMProvider):
    def __init__(self, model_id: str, region: str | None = None):
        self.llm = Bedrock(model_id=model_id, region_name=region)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)
