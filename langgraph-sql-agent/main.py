import argparse
from agent.graph import build_graph
from config.config import load_config
from chat import HistoryManager


def main():
    parser = argparse.ArgumentParser(description="LangGraph SQL Agent")
    parser.add_argument("--query", required=True, help="Natural language question")
    parser.add_argument("--debug", action="store_true", help="Return intermediate steps")
    parser.add_argument("--session-id", help="Existing session ID")
    args = parser.parse_args()

    config = load_config()
    history = HistoryManager(config["history"]["db_uri"])
    session_id = args.session_id or history.create_session_id()
    history.add_message(session_id, "user", args.query)
    graph = build_graph(config, session_id=session_id, history_manager=history, debug=args.debug)
    result = graph.invoke({"query": args.query, "session_id": session_id})
    print(result.get("answer"))


if __name__ == "__main__":
    main()
