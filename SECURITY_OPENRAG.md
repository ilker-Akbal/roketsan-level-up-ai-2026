# OpenRAG Bench security policy (experimental)

OpenRAG Bench evaluates local retrieval inputs and generates JSON/HTML reports.
Treat benchmark questions and document IDs as untrusted; reports may contain
sensitive input text. Do not upload proprietary retrieval data to public issues.

## Reporting a vulnerability

Before the standalone project's security-contact setup exists, please use a
private communication channel with the repository maintainer rather than
publishing proof-of-concept secrets or private datasets. A dedicated GitHub
private vulnerability-reporting workflow should be configured at release.

## Supported versions

No stable supported release is published yet. Changes in the draft PR are
experimental and receive no security-response-time guarantee.

## Safe defaults

- No network calls or telemetry from the evaluation core.
- No evaluation of arbitrary Python expressions in JSON inputs.
- HTML output escapes untrusted query text.
- Optional FAISS integration does not download models or write index files.
