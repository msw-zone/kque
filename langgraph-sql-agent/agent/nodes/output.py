from typing import Dict


def output_node(state: Dict, debug: bool = False) -> Dict:
    if state.get("clarification"):
        return {"answer": state.get("clarification")}

    if not debug:
        return {"answer": state.get("results")}
    else:
        return state
