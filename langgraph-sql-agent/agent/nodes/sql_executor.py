from typing import Dict
from db.mysql_connector import execute_sql


def sql_executor_node(state: Dict, engine) -> Dict:
    if not state.get("valid", False):
        return state
    rows = execute_sql(engine, state["sql"])
    state["results"] = [dict(row) for row in rows]
    return state
