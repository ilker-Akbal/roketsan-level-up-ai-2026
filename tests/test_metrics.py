import unittest
from openrag_bench.metrics import precision_at_k, recall_at_k, reciprocal_rank, hit_at_k
from openrag_bench.cli import evaluate

class MetricsTests(unittest.TestCase):
    def test_metrics(self):
        self.assertEqual(precision_at_k(["a", "b"], ["b"], 2), 0.5)
        self.assertEqual(recall_at_k(["a", "b"], ["b", "c"], 2), 0.5)
        self.assertEqual(reciprocal_rank(["a", "b"], ["b"]), 0.5)
        self.assertEqual(hit_at_k(["a"], ["b"], 1), 0.0)
    def test_empty_relevant(self):
        self.assertEqual(recall_at_k(["a"], [], 1), 0.0)
    def test_invalid_k(self):
        with self.assertRaises(ValueError):
            precision_at_k([], [], 0)
    def test_report(self):
        report = evaluate([{"retrieved_ids": ["a"], "relevant_ids": ["a"]}], 1)
        self.assertEqual(report["metrics"]["recall_at_k"], 1.0)

if __name__ == "__main__":
    unittest.main()
