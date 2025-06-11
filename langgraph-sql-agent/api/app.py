from fastapi import FastAPI
from pydantic import BaseModel
import time

from agent.graph import build_graph
from config.config import load_config
from chat.history_manager import HistoryManager

config = load_config()
history = HistoryManager(config["history"]["db_uri"])

app = FastAPI(title="LangGraph SQL Agent API")

class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None

class QueryResponse(BaseModel):
    session_id: str
    sql: str | None = None
    results: list | None = None
    context: str | None = None
    clarification: str | None = None
    error: str | None = None
    execution_time: float
    model: str | None = None

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    session_id = req.session_id or history.create_session_id()
    history.add_message(session_id, "user", req.question)

    graph = build_graph(config, session_id=session_id, history_manager=history, debug=True)

    start = time.perf_counter()
    try:
        result = graph.invoke({"query": req.question})
        error = result.get("error")
        sql = result.get("sql")
        results = result.get("results")
        context = result.get("context")
        clarification = result.get("clarification")
    except Exception as e:
        result = {}
        error = str(e)
        sql = None
        results = None
        context = None
        clarification = None
    execution_time = time.perf_counter() - start

    history.add_message(session_id, "assistant", str(result.get("answer")))

    return QueryResponse(
        session_id=session_id,
        sql=sql,
        results=results,
        context=context,
        clarification=clarification,
        error=error,
        execution_time=execution_time,
        model=config.get("llm", {}).get("model_id"),
    )
