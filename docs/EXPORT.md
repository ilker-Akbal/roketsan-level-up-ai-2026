# Creating a standalone OpenRAG Bench repository

The original repository is a workshop practice archive. It must **not**
be blanket-licensed while ownership of inherited materials is unclear.

## 1. Export only vetted candidate files

```bash
git clone https://github.com/ilker-Akbal/roketsan-level-up-ai-2026.git
cd roketsan-level-up-ai-2026
git switch feature/openrag-bench
python scripts/export_openrag.py ../openrag-bench-export
```

The export tool uses an explicit allowlist, refuses existing destinations,
and excludes workshop notebooks, demo PDFs, notes, images and local secrets.
The exported folder has **no license** until you review source ownership.

## 2. Complete provenance and licensing review

Use [PROVENANCE.md](PROVENANCE.md) as the checklist. Do not distribute files
you cannot license. Choose a specific SPDX license (MIT/Apache-2.0 are
possible examples), include copyright attributions, update pyproject.toml,
and verify applicable third-party requirements. The maintainer, not the
export script, is responsible for confirming these rights.

## 3. Verify and publish, once rights are cleared

```bash
cd ../openrag-bench-export
python -m pip install -e .
python -m unittest discover -s tests -v
python -m openrag_bench.cli examples/comparison_candidate.json --baseline examples/comparison_baseline.json --k 2 --min-delta 0
```

Create a new **public** GitHub repository, initialize source control in the
exported folder and push it. Record the initial commit and tag v0.1.0 only
after testing and licensing are complete. Never carry over the workshop
repository's unrelated history.

## 4. Build authentic external adoption

Use actual maintainers' feedback, documented benchmark datasets with clear
permission, reproducible evaluations, releases and issues. Do not
manufacture stars, usage or contributors. Publishing the repository is
a starting point; it does not guarantee selection by any third-party program.
