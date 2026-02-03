from pathlib import Path
from typing import Dict, List


def render(report: Dict[str, object], output_path: Path) -> Path:
    findings: List[Dict[str, object]] = report["findings"]
    summary = report["summary"]
    lines = [
        f"# Hidden Prompt Scan Report",
        "",
        f"**Target:** {report['target']}",
        f"**Scan ID:** {report['scan_id']}",
        f"**Timestamp:** {report['timestamp']}",
        "",
        "## Summary",
        f"- Risk Score: {report['risk_score']} ({report['risk_level']})",
        f"- High: {summary['high']} | Medium: {summary['medium']} | Low: {summary['low']}",
        "",
        "## Findings",
    ]

    if not findings:
        lines.append("No findings detected.")
    else:
        for finding in findings:
            lines.extend(
                [
                    "---",
                    f"### {finding['title']}",
                    f"- Severity: {finding['severity']}",
                    f"- Category: {finding['category']}",
                    f"- Confidence: {finding['confidence']}",
                    f"- Evidence: `{finding['evidence']}`",
                    f"- Location: offset {finding['offsets']['start']} (line {finding['line_numbers']['start']})",
                    f"- Rationale: {finding['rationale']}",
                    f"- Recommendation: {finding['recommendation']}",
                ]
            )
            for snippet in finding["snippets"]:
                lines.append("```text")
                lines.append(snippet["text"])
                lines.append("```")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
