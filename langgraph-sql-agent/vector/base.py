from abc import ABC, abstractmethod
from typing import List


class VectorClient(ABC):
    """Abstract base class for vector database clients."""

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        """Return a list of documents most similar to the query."""
        raise NotImplementedError
