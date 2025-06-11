# kque

This repository contains a LangGraph based SQL agent. The agent retrieves relevant context from a vector database, generates SQL using an LLM and executes it against MySQL. Conversation history is stored for each session.

The latest version supports multi-step reasoning. When the system cannot answer a question due to missing context it will generate a follow-up clarification question so the user can refine their query.
