from __future__ import annotations

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from providers import get_embedding_provider, get_llm_provider

from typing import Dict

from config.config import load_config
from vector.qdrant_client import QdrantVectorClient
from db.mysql_connector import create_mysql_engine

from .nodes.user_query import user_query_node
from .nodes.retriever import retrieval_node
from .nodes.sql_builder import sql_builder_node
from .nodes.sql_validator import sql_validator_node
from .nodes.sql_executor import sql_executor_node
from .nodes.output import output_node
from .nodes.history import history_node
from .nodes.clarification import clarification_node


class AgentState(Dict):
    query: str
    context: str
    sql: str
    valid: bool
    results: list
    error: str


def build_graph(config: dict | None = None, session_id: str | None = None, history_manager=None, debug: bool = False):
    if config is None:
        config = load_config()

    # Initialize external dependencies
    vector_config = config.get("vector", {})
    vector_client = QdrantVectorClient(url=vector_config["host"], collection=vector_config.get("collection", "documents"))

    embedding_cfg = config.get("embedding", {})
    llm_cfg = config.get("llm", {})

    embeddings = get_embedding_provider(embedding_cfg)
    llm = get_llm_provider(llm_cfg)
    engine = create_mysql_engine(config["sql"]["connection_string"])

    # Build graph
    sg = StateGraph(AgentState)
    sg.add_node("user_query", lambda state: user_query_node(state))
    sg.add_node("retrieval", lambda state: retrieval_node(state, vector_client))
    sg.add_node("clarify", lambda state: clarification_node(state, llm))
    sg.add_node("build_sql", lambda state: sql_builder_node(state, llm))
    sg.add_node("validate", lambda state: sql_validator_node(state, engine))
    sg.add_node("execute", lambda state: sql_executor_node(state, engine))
    sg.add_node("output", lambda state: output_node(state, debug=debug))
    if history_manager and session_id:
        sg.add_node("history", lambda state: history_node(state, history_manager, session_id))

    # Edges
    sg.set_entry_point("user_query")
    sg.add_edge("user_query", "retrieval")
    sg.add_conditional_edges(
        "retrieval",
        lambda state: "clarify" if state.get("needs_clarification") else "build_sql",
    )
    sg.add_edge("clarify", "output")
    sg.add_edge("build_sql", "validate")
    sg.add_conditional_edges(
        "validate",
        lambda state: "execute" if state.get("valid") else "output",
    )
    sg.add_edge("execute", "output")
    if history_manager and session_id:
        sg.add_edge("output", "history")
        sg.add_edge("history", END)
    else:
        sg.add_edge("output", END)

    memory = SqliteSaver(".langgraph.db")
    graph = sg.compile(checkpointer=memory)
    return graph
