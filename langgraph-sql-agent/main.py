import argparse
from agent.graph import build_graph
from config.config import load_config


def main():
    parser = argparse.ArgumentParser(description="LangGraph SQL Agent")
    parser.add_argument("--query", required=True, help="Natural language question")
    parser.add_argument("--debug", action="store_true", help="Return intermediate steps")
    args = parser.parse_args()

    config = load_config()
    graph = build_graph(config, debug=args.debug)
    result = graph.invoke({"query": args.query})
    print(result)


if __name__ == "__main__":
    main()
