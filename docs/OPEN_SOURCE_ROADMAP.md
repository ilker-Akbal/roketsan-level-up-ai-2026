# OpenRAG Bench: release and community roadmap

## Completed in the draft PR
- [x] Offline ranked-retrieval metrics and macro-averaged JSON reports
- [x] JSON schema validation and duplicate-document-ID rejection
- [x] Distinct truncated MRR@k and legacy uncut reciprocal rank
- [x] Candidate-versus-baseline paired comparisons with stable query IDs
- [x] Reproducible paired bootstrap intervals and a CLI regression threshold
- [x] Escaped, standalone HTML reports; synthetic comparison fixtures
- [x] Unit tests and Python 3.10–3.13 GitHub Actions matrix

## Required before claiming a publicly maintained open-source release
- [ ] Audit all inherited workshop material and sample data for provenance and permissions
- [ ] Extract independently authored evaluation package into its own public repo
- [ ] Review and adopt an appropriate explicit license for the extracted package
- [ ] Publish versioned releases and public installation documentation
- [ ] Integrate real RAG retrievers and publish independently reproducible results
- [ ] Publish a multilingual dataset with its own license and annotation methodology
- [ ] Invite *genuine* outside use; triage real issues and maintain releases
- [ ] Track authentic downloads, external users, contributions and downstream integrations
- [ ] Add security policy, automated dependency audit and release provenance

## Codex for Open Source readiness

OpenAI evaluates meaningful project usage, ecosystem importance and ongoing
maintainer responsibilities. This roadmap is **not** a promise of eligibility or
selection. Never manufacture stars, downloads, contributions, benchmark wins,
or other adoption evidence. Keep application claims verifiable, and clearly
distinguish experimental features from released functionality.
