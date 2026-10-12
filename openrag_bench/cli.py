"""Validate and evaluate retrieval results from a JSON dataset."""
import argparse
import json
from pathlib import Path
from .metrics import precision_at_k, recall_at_k, reciprocal_rank, hit_at_k, ndcg_at_k

def _validate(rows, k):
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k must be a positive integer")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Dataset must be a non-empty JSON array")
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Row {i} must be an object")
        for field in ("retrieved_ids", "relevant_ids"):
            ids = row.get(field)
            if not isinstance(ids, list) or any(not isinstance(v, str) or not v for v in ids):
                raise ValueError(f"Row {i}: {field} must be a list of non-empty strings")
            if len(ids) != len(set(ids)):
                raise ValueError(f"Row {i}: duplicate document IDs in {field}")

def evaluate(rows, k):
    _validate(rows, k)
    scores = []
    for row in rows:
        retrieved, relevant = row["retrieved_ids"], row["relevant_ids"]
        scores.append({
            "precision_at_k": precision_at_k(retrieved, relevant, k),
            "recall_at_k": recall_at_k(retrieved, relevant, k),
            "hit_at_k": hit_at_k(retrieved, relevant, k),
            "reciprocal_rank": reciprocal_rank(retrieved, relevant),
            "ndcg_at_k": ndcg_at_k(retrieved, relevant, k),
        })
    return {"count": len(scores), "k": k,
            "metrics": {key: sum(x[key] for x in scores) / len(scores) for key in scores[0]},
            "per_query": [{"question": row.get("question"), "metrics": score}
                          for row, score in zip(rows, scores)]}

def main():
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval results")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(args.dataset.read_text(encoding="utf-8")), args.k)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
