"""Standalone HTML report generator; no JS or external assets."""
from html import escape

def render_html(report):
    metrics = report["metrics"]
    lines = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             "<title>OpenRAG Bench Report</title>",
             '<style>body{font:16px system-ui;max-width:900px;margin:3rem auto;padding:0 1rem;color:#17202a}table{border-collapse:collapse;width:100%}th,td{padding:.7rem;border-bottom:1px solid #ccc;text-align:left}th{background:#f4f6f7}h1{margin-bottom:.3rem}</style>',
             '</head><body><h1>OpenRAG Bench</h1>',
             f'<p>Evaluated {int(report["count"])} queries at k={int(report["k"])}</p>',
             '<h2>Aggregate metrics</h2><table><thead><tr><th>Metric</th><th>Score</th></tr></thead><tbody>']
    for key, value in metrics.items():
        lines.append(f"<tr><td>{escape(str(key))}</td><td>{float(value):.4f}</td></tr>")
    lines.append("</tbody></table><h2>Per-query results</h2><table><thead><tr><th>Question</th><th>Scores</th></tr></thead><tbody>")
    for row in report.get("per_query", []):
        question = escape(str(row.get("question") or "—"))
        score = ", ".join(f"{escape(str(k))}: {float(v):.3f}" for k, v in row["metrics"].items())
        lines.append(f"<tr><td>{question}</td><td>{score}</td></tr>")
    lines.append("</tbody></table></body></html>")
    return "\n".join(lines)
