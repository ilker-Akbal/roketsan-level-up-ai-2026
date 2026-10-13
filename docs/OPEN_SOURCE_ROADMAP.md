# OpenRAG Bench: release and community roadmap

## Completed in the draft PR
- [x] Offline ranked-retrieval metrics and macro-averaged JSON reports
- [x] JSON schema validation and duplicate-document-ID rejection
- [x] Distinct truncated MRR@k and legacy uncut reciprocal rank
- [x] Candidate-versus-baseline paired comparisons with stable query IDs
- [x] Reproducible paired bootstrap intervals and a CLI regression threshold
- [x] Escaped, standalone HTML reports; synthetic comparison fixtures
- [x] Unit tests and Python 3.10–3.13 GitHub Actions matrix
- [x] Optional FAISS adapter with mocked integration tests and runnable example
- [x] Documented provenance boundary and preliminary security policy

## Required before claiming a publicly maintained open-source release
- [ ] Audit inherited files and sample data for provenance and permissions
- [ ] Extract independently authored evaluation package into its own public repo
- [ ] Review and adopt an explicit license for the extracted package
- [ ] Publish tagged version(s) and public installation documentation
- [ ] Run independently reproducible comparisons on a properly licensed dataset
- [ ] Publish a multilingual dataset with documented provenance and annotation
- [ ] Invite genuine outside use; triage issues, review contributions and maintain releases
- [ ] Track authentic downloads, external users and downstream integrations
- [ ] Configure dedicated security advisories and release provenance

## Codex for Open Source readiness

OpenAI evaluates meaningful project usage, ecosystem importance and ongoing
maintainer responsibilities. This roadmap is **not** a promise of eligibility or
selection. Never manufacture stars, downloads, contributions or benchmark wins.
Keep application claims verifiable, and clearly distinguish experimental
features from released functionality.
