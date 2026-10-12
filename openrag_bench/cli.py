"""Evaluate retrieval results from a JSON dataset."""
import argparse
import json
from pathlib import Path
from .metrics import precision_at_k, recall_at_k, reciprocal_rank, hit_at_k

def evaluate(rows, k):
    if not rows:
        raise ValueError("Dataset must contain at least one example")
    scores = []
    for row in rows:
        retrieved, relevant = row["retrieved_ids"], row["relevant_ids"]
        scores.append({"precision_at_k": precision_at_k(retrieved, relevant, k),
                       "recall_at_k": recall_at_k(retrieved, relevant, k),
                       "hit_at_k": hit_at_k(retrieved, relevant, k),
                       "reciprocal_rank": reciprocal_rank(retrieved, relevant)})
    return {"count": len(scores), "k": k, "metrics": {key: sum(x[key] for x in scores) / len(scores) for key in scores[0]}}

def main():
    parser = argparse.ArgumentParser(description="Evaluate RAG retrieval results")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(json.loads(args.dataset.read_text(encoding="utf-8")), args.k)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
