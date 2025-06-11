from typing import Dict
from sqlalchemy.exc import SQLAlchemyError
from db.mysql_connector import reflect_schema


def sql_validator_node(state: Dict, engine) -> Dict:
    try:
        # simple validation by running EXPLAIN
        with engine.connect() as conn:
            conn.execute(f"EXPLAIN {state['sql']}")
        state["valid"] = True
    except SQLAlchemyError as e:
        state["valid"] = False
        state["error"] = str(e)
    return state
