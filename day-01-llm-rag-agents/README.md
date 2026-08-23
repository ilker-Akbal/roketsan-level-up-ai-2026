# Day 01 — LLM, RAG and AI Agents

This folder contains the workshop implementation for a small technical-document assistant.

## Flow

1. `mil_std_document.py` defines the fictional training document.
2. `create_vector.py` chunks the document, creates Gemini embeddings, and saves a local FAISS index.
3. `rag.py` retrieves relevant chunks and grounds an LLM response in the retrieved context.
4. `tools.py` exposes general-question and technical-document RAG tools.
5. `agent.py` creates a tool-using agent with in-memory conversation state.

## Run

From the repository root:

```bash
pip install -r requirements/day-01.txt
```

Create `.env` from `.env.example`, set `GOOGLE_API_KEY`, then:

```bash
cd day-01-llm-rag-agents
python create_vector.py
python rag.py
python agent.py
```

`faiss_index/` is generated locally and is not version-controlled.
