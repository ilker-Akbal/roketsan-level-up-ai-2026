# OpenRAG Bench on the existing FAISS retriever (first-party integration)

This repository now uses the **published** OpenRAG Bench v0.6.0 wheel in a
separate integration exercise. It evaluates the existing local Sentence
Transformers + FAISS retriever in `practice/llm/local-rag/` and produces
real ranked chunk IDs (not labels copied into retrieval results).

**Scope:** This is a reproducible *first-party* integration on six original,
tiny educational text snippets, not an independent external adoption, a
production integration, a general RAG benchmark, or a measurement of LLM
answer quality. The author assigned six relevance labels by hand; they have
not been independently annotated or validated. The PDF-looking file names
in the snippets are illustrative metadata; no PDF content is loaded.

## Why this particular RAG implementation

The Day-1 workshop agent loads Google embedding and Gemini API clients.
Instead, the local RAG practice uses a **real multilingual MiniLM embedding
model** with a **FAISS IndexFlatIP cosine similarity index**; it does not need
a cloud API key and has stable source chunk IDs `chunk_01` through
`chunk_06`. It can be evaluated without calling Ollama or generating text.

Refactoring `faiss_search.py` placed the same original educational
documents and embedding/FAISS logic in `retrieval_core.py`. Both the
interactive Ollama example and the evaluation runner now call
`build_retriever()`. The retriever's scoring and ranked FAISS indices
determine the actual observed documents.

## Reproduce on Windows or Linux

From the repository root, in a Python 3.11 environment (a CPU is sufficient):

~~~bash
python -m pip install "sentence-transformers==5.1.1" "transformers==4.57.1" "faiss-cpu==1.12.0"
python -m pip install https://github.com/ilker-Akbal/openrag-bench/releases/download/v0.6.0/openrag_bench-0.6.0-py3-none-any.whl
python -m unittest discover -s tests -v
python practice/llm/local-rag/openrag_bench_eval.py --output-dir reports/my-first-faiss-test
~~~

The model weights are downloaded from Hugging Face **on the first run** and
cached; subsequent retrieval runs can use cached weights. The package
installation also needs network access. **The evaluation and Guard operate
offline once dependencies and model weights are available.**

On Windows PowerShell, open the resulting HTML report with:

~~~powershell
Start-Process .\reports\my-first-faiss-test\guard.html
~~~

Use a **new output directory** for each run. Evidence is intentionally not
overwritten; generated `reports/` are gitignored. No OpenAI or Ollama API
credentials are needed for this evaluation.

## Exactly what gets evaluated

- **Retriever:** `retrieval_core.build_retriever()` — same actual
  Sentence Transformers model and FAISS cosine ranking used by the original
  local RAG script.
- **Ground truth:** six author-assigned synthetic judgments in
  `practice/llm/local-rag/openrag_golden.json`. These labels are not passed
  to FAISS or used to construct rankings.
- **Baseline configuration:** top-k 3, minimum cosine similarity 0.35.
- **Candidate configuration:** same actual index and top-k 3, minimum
  similarity 0.20. This tests a genuine configuration change; it is not a
  comparison of two independently trained embedding models.
- **Capture:** OpenRAG Bench saves two sets of observed, ranked chunk IDs,
  binds them to the separate author labels and writes hash-only manifests.
- **Replay/Guard:** v0.6.0 evaluates NDCG@3 non-regression overall and
  no regression in hit@3 for the marked navigation query.
- **Results:** `summary.json`, `guard.json` and `guard.html`.
  The exact scores and pass/fail result **must come from the run**; do not
  assume an improvement just because the threshold is lower.

On default thresholds, lowering the score filter cannot discard a result
previously retained, but it may or may not improve the benchmark metrics.
To explore a potentially harmful threshold, use for example
`--candidate-min-score 0.85`. A Guard failure returns **exit code 2**,
and a passed Guard returns **0**. Do not claim the stricter policy always
fails unless a real observed run demonstrates it.

The full captured `baseline.json`/`candidate.json` include question text
and ranked chunk IDs and remain **local**. Do not upload private RAG
captured datasets to issues, public CI artifacts, or releases.

## GitHub Actions evidence

The path-scoped workflow
[`.github/workflows/openrag-bench-faiss.yml`](../.github/workflows/openrag-bench-faiss.yml)
also has **Run workflow** enabled for manual verification.

It installs a CPU runtime, downloads the real Sentence Transformers
model, creates the FAISS index, calls OpenRAG Bench v0.6.0 from its
**public release wheel** (not from a local copy), verifies real
observed rankings and checks Guard exit behavior.

When successfully run, the public workflow's job log and short-lived
artifact `openrag-faiss-firstparty-summary` provide independently
inspectable **CI execution evidence for our own integration**.
The artifact includes **only aggregate summary and redacted Guard reports**;
raw query texts, complete captured rows, corpus documents, model weights
and observed raw ranking files are excluded.

Workflow success is not asserted here without a passing run URL. A
passing job demonstrates the first-party integration actually executed;
it is **not** a claim that someone outside this project uses OpenRAG
Bench.

## Limitations and next step

- The corpus has only six intentionally simple English educational snippets.
  These do not establish retrieval quality on actual workshop manuals.
- Labels were assigned by the same author, not independent human assessors.
- The Hugging Face model repository's revision is not pinned here;
  dependency version pins alone do not prove bitwise repeatability.
- Real-world validation requires a separate developer to integrate
  OpenRAG Bench into an independent retriever, consent to share a
  minimal public reproduction, and provide factual feedback.
- The optional interactive Ollama answer script is unchanged in purpose,
  but it now only loads and calls Ollama when explicitly executed.

See the [upstream OpenRAG Bench integration guide](https://github.com/ilker-Akbal/openrag-bench/blob/main/docs/OWN_RAG_QUICKSTART.md).
