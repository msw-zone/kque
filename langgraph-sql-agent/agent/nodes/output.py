from typing import Dict


def output_node(state: Dict, debug: bool = False) -> Dict:
    if not debug:
        return {"answer": state.get("results")}
    else:
        return state
