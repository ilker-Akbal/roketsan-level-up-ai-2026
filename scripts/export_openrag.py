"""Safely export only the independently authored toolkit candidate.

Usage (from the checked-out feature branch):
    python scripts/export_openrag.py ../openrag-bench-export

Does NOT create a GitHub repository, assign a license or validate legal
ownership of the source files. A maintainer must review before publication.
"""
import argparse
from pathlib import Path
import shutil

ALLOWLIST = (
    "pyproject.toml",
    "OPENRAG_BENCH.md",
    "CONTRIBUTING_OPENRAG.md",
    "SECURITY_OPENRAG.md",
    "openrag_bench/__init__.py",
    "openrag_bench/adapters.py",
    "openrag_bench/cli.py",
    "openrag_bench/comparison.py",
    "openrag_bench/html_report.py",
    "openrag_bench/metrics.py",
    "openrag_bench/integrations/__init__.py",
    "openrag_bench/integrations/faiss.py",
    "tests/test_metrics.py",
    "tests/test_adapters.py",
    "tests/test_comparison.py",
    "tests/test_faiss_integration.py",
    "examples/custom_retriever.py",
    "examples/faiss_integration.py",
    "examples/retrieval_results.json",
    "examples/comparison_candidate.json",
    "examples/comparison_baseline.json",
    ".github/workflows/openrag-bench-ci.yml",
    "docs/OPEN_SOURCE_ROADMAP.md",
    "docs/PROVENANCE.md",
)


def export(source: Path, destination: Path):
    """Copy a reviewed allowlist, refusing pre-existing targets and symlinks."""
    source = source.resolve()
    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite existing path: {destination}")
    if destination == source or source in destination.parents:
        raise ValueError("Export destination must be outside the source repository")

    # Check everything first to avoid partial exports.
    for rel in ALLOWLIST:
        path = source / rel
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"Expected regular file missing: {rel}")
        for parent in path.parents:
            if parent == source:
                break
            if parent.is_symlink():
                raise ValueError(f"Refusing symlinked source directory: {rel}")

    for rel in ALLOWLIST:
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, target)

    (destination / "README.md").write_text(
        "# OpenRAG Bench\n\n"
        "See [installation, evaluation and limitations](OPENRAG_BENCH.md).\n\n"
        "**Pre-release export.** Copyright and provenance must be reviewed; "
        "no open-source license has been chosen.\n",
        encoding="utf-8",
    )
    (destination / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n*.egg-info/\nbuild/\ndist/\n"
        ".venv/\nreport.json\nreport.html\ncomparison.json\ncomparison.html\n",
        encoding="utf-8",
    )
    return len(ALLOWLIST)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    count = export(Path(__file__).resolve().parents[1], args.destination)
    print(f"Exported {count} explicitly allowed files to {args.destination}")
    print("NEXT: review ownership, choose license, run tests, then create GitHub repo.")


if __name__ == "__main__":
    main()
