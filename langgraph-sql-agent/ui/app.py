import streamlit as st
from agent.graph import build_graph
from config.config import load_config
from chat.history_manager import HistoryManager

cfg = load_config()
manager = HistoryManager(cfg["history"]["db_uri"])

if "session_id" not in st.session_state:
    st.session_state.session_id = manager.create_session_id()

st.sidebar.header("Configuration")
st.sidebar.write(cfg)

st.title("LangGraph SQL Agent")

history = manager.get_messages(st.session_state.session_id)
for msg in history:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input("Ask a question"):
    st.chat_message("user").write(prompt)
    manager.add_message(st.session_state.session_id, "user", prompt)

    graph = build_graph(cfg)
    result = graph.invoke({"query": prompt})
    answer = result.get("answer")
    st.chat_message("assistant").write(answer)
    manager.add_message(st.session_state.session_id, "assistant", str(answer))
    if result.get("clarification"):
        st.info("The assistant requested more details.")
