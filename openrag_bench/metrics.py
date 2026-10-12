"""Deterministic retrieval evaluation metrics."""
def precision_at_k(retrieved, relevant, k):
    if k <= 0:
        raise ValueError("k must be positive")
    return len(set(retrieved[:k]) & set(relevant)) / k

def recall_at_k(retrieved, relevant, k):
    if k <= 0:
        raise ValueError("k must be positive")
    relevant = set(relevant)
    return len(set(retrieved[:k]) & relevant) / len(relevant) if relevant else 0.0

def reciprocal_rank(retrieved, relevant):
    relevant = set(relevant)
    return next((1 / i for i, doc in enumerate(retrieved, 1) if doc in relevant), 0.0)

def hit_at_k(retrieved, relevant, k):
    if k <= 0:
        raise ValueError("k must be positive")
    return float(bool(set(retrieved[:k]) & set(relevant)))
