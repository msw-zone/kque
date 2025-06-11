from typing import Dict
from langchain.prompts import ChatPromptTemplate
from providers.llms.base import LLMProvider

CLARIFICATION_PROMPT = ChatPromptTemplate.from_template(
    "You are a helpful assistant.\n"
    "The user question is unclear or lacks enough context to answer.\n"
    "User question: {question}\n"
    "Ask a brief clarifying question to gather more details."
)


def clarification_node(state: Dict, llm: LLMProvider) -> Dict:
    prompt = CLARIFICATION_PROMPT.format(question=state.get("query", ""))
    state["clarification"] = llm(prompt).strip()
    return state
