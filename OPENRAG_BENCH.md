# OpenRAG Bench — offline retrieval evaluation (experimental)

OpenRAG Bench is a lightweight, dependency-free Python toolkit for **evaluating
ranked document retrieval in RAG pipelines**, with reproducible, paired
baseline-versus-candidate comparisons. It evaluates *retrieval relevance*, not
LLM answer correctness, hallucinations, or production readiness.

> **Project status:** experimental pre-release, developed in a draft PR.
> The workshop repository includes third-party teaching materials. Do **not**
> assume those materials have an open-source license. A standalone repository
> for independently authored toolkit code is planned after provenance review.

## Quickstart

Python 3.10–3.13:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
openrag-bench examples/retrieval_results.json --k 2 --output report.json --html report.html
```

## Compare two retrieval versions (CI regression gate)

```bash
openrag-bench examples/comparison_candidate.json \
  --baseline examples/comparison_baseline.json \
  --k 2 --metric ndcg_at_k --min-delta 0 \
  --output comparison.json --html comparison.html
```

A positive delta means the candidate scored higher. When the selected delta
falls **below** `--min-delta`, the CLI exits with status **2**, after writing
the requested reports. This is a practical CI threshold, *not* a statistical
significance claim.

## JSON input contract

Provide a non-empty JSON **array**, one object per query:

```json
[
  {
    "query_id": "example-001",
    "question": "What is a retriever?",
    "retrieved_ids": ["doc-7", "doc-2"],
    "relevant_ids": ["doc-2"]
  }
]
```

- `retrieved_ids` is a ranked list of distinct, nonempty document IDs. It may
  be empty. Its order determines rank.
- `relevant_ids` is a set-like list of distinct, nonempty ground-truth document
  IDs. It may be empty; recall and NDCG are defined as zero for that query.
- `query_id` is optional for single-system evaluation, **required and unique**
  for comparisons. The query ID sets and per-query ground truth must match
  between baseline and candidate. Row order does not matter.
- `question` is an optional display string, never sent to an API or LLM.
- All metrics are **macro-averaged** equally across queries. `precision_at_k`
  uses `k` as denominator even when fewer than `k` items are retrieved.
- `mrr_at_k` uses only the first `k` positions. Legacy `reciprocal_rank` is
  an **uncut** reciprocal rank provided for compatibility; don't compare it as
  an at-k metric. NDCG uses binary (not graded) relevance.
- Paired-bootstrap 95% intervals use 1,000 seeded samples over aligned queries.
  On small or unrepresentative datasets, they do **not** justify claims of
  significance or generalization.

## Evaluate a retriever object directly

```python
from openrag_bench.adapters import run_retriever

class MyRetriever:
    def retrieve(self, query: str, k: int):
        return ["doc-7", "doc-2"][:k]

report = run_retriever(
    MyRetriever(),
    [{"question": "What is retrieval?", "relevant_ids": ["doc-2"]}],
    k=2,
)
print(report["metrics"])
```

This protocol can wrap FAISS, BM25 or a vector database without changing the
evaluation core. An **optional FAISS adapter** is included:

```bash
pip install numpy faiss-cpu
python examples/faiss_integration.py
```

The example uses illustrative *handmade* vectors, not learned embeddings.
For a real vector index, the caller must supply matching document IDs and an
embedding function; model downloads and index ownership remain external.
Ollama, direct answer-grounding evaluation and multilingual labeled benchmarks
remain planned, not implemented.

## Limitations and provenance

The bundled examples are **synthetic test fixtures** and are not evidence of
benchmark superiority, accuracy in deployed systems, or project adoption.
Datasets must have documented licenses and annotation methodology before
publishing comparative claims. No API credentials or network services are
required by the evaluation core. See the [roadmap](docs/OPEN_SOURCE_ROADMAP.md),
[provenance policy](docs/PROVENANCE.md), [security policy](SECURITY_OPENRAG.md)
and [contribution guide](CONTRIBUTING_OPENRAG.md).
