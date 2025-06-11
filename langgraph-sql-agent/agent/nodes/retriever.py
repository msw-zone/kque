from typing import Dict
from vector.base import VectorClient


def retrieval_node(state: Dict, vector_client: VectorClient, k: int = 5) -> Dict:
    query = state.get("query")
    docs = vector_client.similarity_search(query, k=k)
    state["context"] = "\n".join(docs)
    return state
