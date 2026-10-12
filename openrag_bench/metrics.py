"""Dependency-free information retrieval metrics."""
import math

def _check_k(k):
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("k must be a positive integer")

def _unique(items):
    return list(dict.fromkeys(items))

def precision_at_k(retrieved, relevant, k):
    _check_k(k)
    return len(set(retrieved[:k]) & set(relevant)) / k

def recall_at_k(retrieved, relevant, k):
    _check_k(k)
    relevant = set(relevant)
    return len(set(retrieved[:k]) & relevant) / len(relevant) if relevant else 0.0

def reciprocal_rank(retrieved, relevant):
    relevant = set(relevant)
    return next((1 / i for i, doc in enumerate(retrieved, 1) if doc in relevant), 0.0)

def hit_at_k(retrieved, relevant, k):
    _check_k(k)
    return float(bool(set(retrieved[:k]) & set(relevant)))

def ndcg_at_k(retrieved, relevant, k):
    """Binary-relevance normalized discounted cumulative gain."""
    _check_k(k)
    relevant = set(relevant)
    dcg = sum(1 / math.log2(i + 2) for i, doc in enumerate(retrieved[:k]) if doc in relevant)
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(relevant), k)))
    return dcg / ideal if ideal else 0.0
