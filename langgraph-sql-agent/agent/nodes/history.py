from typing import Dict

from chat.history_manager import HistoryManager


def history_node(state: Dict, manager: HistoryManager, session_id: str) -> Dict:
    manager.add_message(session_id, "assistant", str(state.get("answer")))
    return state
