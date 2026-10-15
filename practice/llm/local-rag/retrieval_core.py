"""Shared genuine FAISS retriever for the local RAG demo and OpenRAG Bench.

The six tiny source passages are original educational examples. Retrieval ranks
the actual vector index, not relevance judgments or precomputed answers.
Heavy optional dependencies and model weights load only when build_retriever()
is called; importing this module neither runs Ollama nor downloads a model.
"""
import math

MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

DOCUMENTS = [
    {"text": "The radar detects airborne targets.",
     "document": "radar_manual.pdf", "page": 12, "chunk_id": "chunk_01"},
    {"text": "The battery supplies 24 V DC power.",
     "document": "power_system.pdf", "page": 7, "chunk_id": "chunk_02"},
    {"text": "GNSS provides vehicle position information.",
     "document": "navigation_manual.pdf", "page": 18, "chunk_id": "chunk_03"},
    {"text": "The camera detects pedestrians.",
     "document": "camera_manual.pdf", "page": 25, "chunk_id": "chunk_04"},
    {"text": "IMU measures acceleration and angular velocity.",
     "document": "navigation_manual.pdf", "page": 19, "chunk_id": "chunk_05"},
    {"text": "Ethernet is used to transmit telemetry data.",
     "document": "communication_manual.pdf", "page": 31, "chunk_id": "chunk_06"},
]


class LocalFaissRetriever:
    """Cosine-similarity FAISS search returning source metadata and stable IDs."""

    def __init__(self, documents, model, index, numpy, faiss):
        self.documents = list(documents)
        self.model = model
        self.index = index
        self.numpy = numpy
        self.faiss = faiss
        ids = [row["chunk_id"] for row in self.documents]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("Documents need unique stable chunk_id values")

    def retrieve(self, query, top_k=3, min_score=0.35):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be nonempty text")
        if type(top_k) is not int or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        if type(min_score) not in (int, float) or not math.isfinite(min_score):
            raise ValueError("min_score must be finite")

        query_vector = self.numpy.asarray(self.model.encode([query]), dtype="float32")
        self.faiss.normalize_L2(query_vector)
        scores, indices = self.index.search(query_vector, min(top_k, len(self.documents)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            idx = int(idx)
            if idx < 0 or idx >= len(self.documents) or float(score) < min_score:
                continue
            row = self.documents[idx].copy()
            row["score"] = float(score)
            results.append(row)
        return results


def build_retriever():
    """Build the same Sentence Transformers + FAISS index used by faiss_search.py."""
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_ID, device="cpu")
    vectors = np.asarray(model.encode([doc["text"] for doc in DOCUMENTS]), dtype="float32")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return LocalFaissRetriever(DOCUMENTS, model, index, np, faiss)
