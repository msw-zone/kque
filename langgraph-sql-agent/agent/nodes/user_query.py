from typing import Dict


def user_query_node(state: Dict) -> Dict:
    """Pass the user query through the state."""
    # The query is already provided in the state when invoking the graph.
    return state
