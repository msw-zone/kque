from typing import Dict
from langchain.prompts import ChatPromptTemplate
from providers.llms.base import LLMProvider


SQL_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful assistant that writes SQL queries.\n"""
    "Context:\n{context}\n"  # inserted from retrieval
    "User question: {question}\n"  # query
    "Write a SQL query."
)


def sql_builder_node(state: Dict, llm: LLMProvider) -> Dict:
    prompt = SQL_PROMPT.format(context=state.get("context", ""), question=state.get("query"))
    sql = llm(prompt).strip()
    state["sql"] = sql
    return state
