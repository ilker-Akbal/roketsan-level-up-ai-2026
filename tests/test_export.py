import tempfile
import unittest
from pathlib import Path

from scripts.export_openrag import ALLOWLIST, export


class ExportTests(unittest.TestCase):
    def test_export_only_allowlisted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "workshop"
            src.mkdir()
            for filename in ALLOWLIST:
                target = src / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("safe placeholder")
            (src / ".env").write_text("PRIVATE_KEY=should_never_leave_this_directory")
            (src / "day-01-llm-rag-agents").mkdir()
            (src / "day-01-llm-rag-agents" / "workshop.py").write_text("do not export")
            destination = Path(directory) / "standalone"
            self.assertEqual(export(src, destination), len(ALLOWLIST))
            self.assertTrue((destination / "openrag_bench" / "metrics.py").exists())
            self.assertFalse((destination / ".env").exists())
            self.assertFalse((destination / "day-01-llm-rag-agents").exists())
            self.assertFalse((destination / "LICENSE").exists())
            with self.assertRaises(FileExistsError):
                export(src, destination)

    def test_missing_source_fails_without_partial_output(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "source"
            src.mkdir()
            dest = Path(directory) / "output"
            with self.assertRaises(FileNotFoundError):
                export(src, dest)
            self.assertFalse(dest.exists())


if __name__ == "__main__":
    unittest.main()
