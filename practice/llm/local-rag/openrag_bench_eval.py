"""Evaluate the existing actual FAISS retriever with OpenRAG Bench v0.6.0.

Both observed rankings are computed by the same Sentence Transformers + FAISS
index used in faiss_search.py, at two different similarity cutoffs. Relevance
labels are a separate, author-assigned synthetic fixture, never retrieval input.

Requires: sentence-transformers, faiss-cpu, numpy, openrag-bench==0.6.0.
No LLM API, Ollama, GPU or raw PDF dataset is needed.
"""
import argparse
import contextlib
import io
import json
import math
from pathlib import Path

from openrag_bench.capture import capture, replay
from retrieval_core import DOCUMENTS, MODEL_ID, build_retriever


HERE = Path(__file__).resolve().parent
GOLDEN_PATH = HERE / "openrag_golden.json"
POLICY_PATH = HERE / "openrag_guard_policy.json"


class OpenRagFaissAdapter:
    """OpenRAG Bench synchronous retriever protocol backed by actual FAISS search."""

    def __init__(self, faiss_retriever, min_score):
        self.faiss_retriever = faiss_retriever
        self.min_score = min_score

    def retrieve(self, question: str, k: int):
        matches = self.faiss_retriever.retrieve(
            question, top_k=k, min_score=self.min_score
        )
        return [match["chunk_id"] for match in matches]


def _write_json_new(path, payload):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def run_evaluation(output_dir, *, k=3, baseline_min_score=0.35, candidate_min_score=0.20):
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    if any(type(value) not in (int, float) or not math.isfinite(value)
           for value in (baseline_min_score, candidate_min_score)):
        raise ValueError("Similarity thresholds must be finite numbers")

    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    corpus_ids = {doc["chunk_id"] for doc in DOCUMENTS}
    if len(corpus_ids) != len(DOCUMENTS) or any(
        not set(item["relevant_ids"]) <= corpus_ids for item in golden
    ):
        raise ValueError("Golden labels must reference stable IDs in the actual corpus")

    # Creating vectors/FAISS and executing searches happens before capture;
    # golden judgments never enter the vector index or retrieval ranking.
    faiss_retriever = build_retriever()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)

    for name, cutoff in (("baseline", baseline_min_score), ("candidate", candidate_min_score)):
        adapter = OpenRagFaissAdapter(faiss_retriever, cutoff)
        observed = [
            {"query_id": item["query_id"],
             "retrieved_ids": adapter.retrieve(item["question"], k)}
            for item in golden
        ]
        _write_json_new(output_dir / f"{name}-observed.json", observed)

        # Use OpenRAG Bench's actual versioned CLI capture and manifest,
        # rather than copying a baseline/candidate JSON template.
        with contextlib.redirect_stdout(io.StringIO()):
            status = capture([
                str(GOLDEN_PATH),
                "--rankings", str(output_dir / f"{name}-observed.json"),
                "--output", str(output_dir / f"{name}.json"),
                "--manifest", str(output_dir / f"{name}.manifest.json"),
            ])
        if status != 0:
            raise RuntimeError(f"OpenRAG capture of {name} did not succeed")

    with contextlib.redirect_stdout(io.StringIO()):
        status = replay([
            str(output_dir / "candidate.json"),
            "--baseline", str(output_dir / "baseline.json"),
            "--policy", str(POLICY_PATH),
            "--k", str(k),
            "--output", str(output_dir / "guard.json"),
            "--html", str(output_dir / "guard.html"),
        ])
    report = json.loads((output_dir / "guard.json").read_text(encoding="utf-8"))
    if status not in (0, 2) or report["guard"]["passed"] != (status == 0):
        raise RuntimeError("OpenRAG Guard result disagrees with replay exit status")

    summary = {
        "evidence_type": "first-party actual FAISS retriever integration on a small synthetic corpus",
        "embedding_model": MODEL_ID,
        "corpus_document_count": len(DOCUMENTS),
        "query_count": len(golden),
        "k": k,
        "baseline_min_score": baseline_min_score,
        "candidate_min_score": candidate_min_score,
        "baseline_ndcg_at_k": report["baseline"]["metrics"]["ndcg_at_k"],
        "candidate_ndcg_at_k": report["candidate"]["metrics"]["ndcg_at_k"],
        "delta_ndcg_at_k": report["delta"]["ndcg_at_k"],
        "guard_passed": report["guard"]["passed"],
        "failed_rules": report["guard"]["failed_rules"],
        "replay_exit_code": status,
    }
    _write_json_new(output_dir / "summary.json", summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/openrag-faiss"))
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--baseline-min-score", type=float, default=0.35)
    parser.add_argument("--candidate-min-score", type=float, default=0.20)
    args = parser.parse_args(argv)
    try:
        summary = run_evaluation(
            args.output_dir, k=args.k,
            baseline_min_score=args.baseline_min_score,
            candidate_min_score=args.candidate_min_score,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False))
    return summary["replay_exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
