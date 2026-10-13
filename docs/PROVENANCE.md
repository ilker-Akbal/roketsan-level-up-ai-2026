# Provenance, permissions and release boundary

This public repository began as a **personal learning/workshop archive**.
It includes teaching-derived source examples, notes, notebook outputs,
a demonstration PDF and other assets whose original ownership and
redistribution permissions have **not yet been independently audited**.

## Proposed boundary for a standalone release

- **Independent toolkit candidate:** `openrag_bench/` and its purpose-built
  unit tests, synthetic fixture JSON and original CLI/HTML/report code.
- **Excluded until permission is verified:** all workshop exercises,
  ROKETSAN-related notes/notebooks, `practice/llm/local-rag/manual.pdf`,
  images, model weights, third-party sample data and output artifacts.
- **External dependencies:** NumPy/FAISS are optional integrations, obtained
  independently by the user under their respective licensing terms.
- **Synthetic examples:** `examples/retrieval_results.json`,
  `examples/comparison_*.json` and adapter demos contain illustrative
  fabricated labels; they do not demonstrate real-world accuracy.

Before licensing and publishing the standalone project:
1. Review each candidate file's actual author and original source.
2. Confirm that all selected source and fixtures are redistributable.
3. Choose an SPDX-recognized license for the independently owned code.
4. Build a fresh repository **without workshop materials or history**,
   then publish a first tagged version, checksums and documentation.
5. Keep original credit where attribution is required.

**No blanket OSS license is asserted for the workshop archive.**
Public visibility alone does not grant redistribution or modification rights.
