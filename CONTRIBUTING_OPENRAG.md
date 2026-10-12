# Contributing to OpenRAG Bench

Thanks for helping make retrieval evaluation reproducible.

## Local setup
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m openrag_bench.cli examples/retrieval_results.json --k 2
```

## Contribution guidelines
- Open an issue describing the problem and expected behavior before large changes.
- Add deterministic tests for new metrics and edge cases.
- Keep the evaluation core usable without network access or GPU.
- Never commit API keys, proprietary datasets, model weights or personal information.
- Benchmark datasets must document provenance, licenses and annotation methods.
- Do not claim evaluation metrics measure answer truthfulness without ground-truth validation.

## License status
This repository contains older workshop practice materials. Licensing and provenance must be reviewed before publishing a project-wide open-source license. Until then, public visibility alone does not grant broad reuse rights.
