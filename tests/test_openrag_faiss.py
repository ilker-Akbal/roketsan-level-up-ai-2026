"""Fast standard-library contract checks; real embedding/FAISS tested in workflow."""
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RAG = ROOT / "practice" / "llm" / "local-rag"
spec = importlib.util.spec_from_file_location("retrieval_core_tested", RAG / "retrieval_core.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class FakeModel:
    def __init__(self):
        self.queries = []

    def encode(self, questions):
        self.queries.extend(questions)
        return [[1.0, 0.0]]


class FakeNumpy:
    def asarray(self, vectors, dtype):
        if dtype != "float32":
            raise ValueError(dtype)
        return vectors


class FakeFaiss:
    @staticmethod
    def normalize_L2(vector):
        return None


class FakeIndex:
    def search(self, vector, k):
        scores = [0.95, 0.30, 0.10]
        indices = [2, 1, 0]
        return [scores[:k]], [indices[:k]]


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.model = FakeModel()
        self.retriever = core.LocalFaissRetriever(
            core.DOCUMENTS, self.model, FakeIndex(), FakeNumpy(), FakeFaiss()
        )

    def test_stable_ordered_ids_are_returned_from_actual_index_indices(self):
        results = self.retriever.retrieve("Where is the vehicle?", 3, min_score=0.20)
        self.assertEqual([row["chunk_id"] for row in results], ["chunk_03", "chunk_02"])
        self.assertEqual(self.model.queries, ["Where is the vehicle?"])
        self.assertEqual(results[0]["score"], 0.95)

    def test_similarity_threshold_can_change_rankings_without_gold_labels(self):
        strict = self.retriever.retrieve("Where is the vehicle?", 3, min_score=0.35)
        relaxed = self.retriever.retrieve("Where is the vehicle?", 3, min_score=0.20)
        self.assertEqual([x["chunk_id"] for x in strict], ["chunk_03"])
        self.assertEqual([x["chunk_id"] for x in relaxed], ["chunk_03", "chunk_02"])

    def test_reject_invalid_search_arguments(self):
        for query, k, threshold in [
            ("", 3, 0.2), ("valid", 0, 0.2), ("valid", True, 0.2),
            ("valid", 3, float("nan")), ("valid", 3, True),
        ]:
            with self.subTest(query=query, k=k, threshold=threshold):
                with self.assertRaises(ValueError):
                    self.retriever.retrieve(query, k, threshold)

    def test_golden_judgments_use_only_known_unique_ids_and_no_rankings(self):
        golden = json.loads((RAG / "openrag_golden.json").read_text(encoding="utf-8"))
        known = {row["chunk_id"] for row in core.DOCUMENTS}
        self.assertEqual(len(known), len(core.DOCUMENTS))
        self.assertEqual(len({row["query_id"] for row in golden}), len(golden))
        self.assertGreaterEqual(len(golden), 5)
        self.assertTrue(any(row["critical"] for row in golden))
        for row in golden:
            self.assertEqual(row["retrieved_ids"], [])
            self.assertTrue(row["relevant_ids"])
            self.assertTrue(set(row["relevant_ids"]) <= known)

    def test_guard_policy_is_explicit_and_versioned(self):
        policy = json.loads((RAG / "openrag_guard_policy.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["version"], 1)
        self.assertEqual(len(policy["rules"]), 2)


if __name__ == "__main__":
    unittest.main()
