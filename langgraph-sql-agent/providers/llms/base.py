from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for language models."""

    @abstractmethod
    def __call__(self, prompt: str) -> str:
        raise NotImplementedError
