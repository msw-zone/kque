# LangGraph SQL Agent

This project provides a modular agent-based system built with [LangGraph](https://github.com/langchain-ai/langgraph). It retrieves relevant context from a Qdrant vector database, generates SQL with your preferred LLM, executes the query against MySQL and persists the full conversation history. If the agent lacks enough context to answer, it now asks a clarifying question so you can refine the request.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure credentials in `config/config.yaml`.

3. Run the main script:

```bash
python main.py --query "Your question here"
```
4. Launch the Streamlit UI:

```bash
streamlit run ui/app.py
```

5. Start the FastAPI server:

```bash
uvicorn api.app:app --reload
```

See `config/config.yaml` for configuration options.
