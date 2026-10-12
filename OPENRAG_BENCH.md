# OpenRAG Bench (early prototype)

A small, dependency-free foundation for evaluating retrieval quality in RAG pipelines.

## Run
```bash
python -m openrag_bench.cli examples/retrieval_results.json --k 2
python -m unittest discover -s tests -v
```

## Current scope
- Precision@k, Recall@k, Hit@k, Mean Reciprocal Rank (MRR)
- JSON input and machine-readable report
- No LLM judge, FAISS adapter, or Ollama adapter yet

## Dataset schema
A JSON array of objects containing `retrieved_ids` (ordered document IDs) and `relevant_ids` (ground-truth IDs). Optional `question` is for human readability.

## Roadmap
1. Schema validation and duplicate-ID policy
2. FAISS and Ollama integration with optional dependencies
3. Answer grounding evaluation and multilingual fixtures
4. CI, package metadata, license review and contribution guide

This is a prototype developed separately from the original workshop exercises. Before publishing a license, review provenance and third-party licensing of reused materials.
