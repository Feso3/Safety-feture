import uuid
from pathlib import Path
from typing import Dict, List

from hidprompt.extractors.text_extractor import extract_text
from hidprompt.renderers.json_renderer import render as render_json
from hidprompt.renderers.markdown_renderer import render as render_markdown
from hidprompt.schema import counts_from_findings, now_timestamp
from hidprompt.scanners.encoded_blob_scanner import scan as scan_encoded
from hidprompt.scanners.injection_phrase_scanner import scan as scan_injection
from hidprompt.scanners.unicode_obfuscation_scanner import scan as scan_unicode
from hidprompt.scoring import score_findings

SUPPORTED_SUFFIXES = {".txt", ".md"}


def run_scan(path: Path, output_dir: Path, output_format: str) -> Dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"Target not found: {path}")
    if path.is_dir():
        raise ValueError("Directory scanning not implemented yet. Provide a file path.")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    extracted = extract_text(path)
    findings: List[Dict[str, object]] = []
    findings.extend(scan_injection(extracted.text, extracted.offsets))
    findings.extend(scan_unicode(extracted.text, extracted.offsets))
    findings.extend(scan_encoded(extracted.text, extracted.offsets))

    risk_score, risk_level = score_findings(findings)
    summary = counts_from_findings(findings)

    report = {
        "tool": "hidprompt",
        "version": "0.1.0",
        "scan_id": str(uuid.uuid4()),
        "timestamp": now_timestamp(),
        "target": str(path),
        "file_info": {
            "size": int(extracted.metadata["size"]),
            "sha256": extracted.metadata["sha256"],
            "mime": extracted.metadata["mime"],
        },
        "summary": {"high": summary.high, "medium": summary.medium, "low": summary.low},
        "risk_score": risk_score,
        "risk_level": risk_level,
        "findings": findings,
        "extraction": {"newline": extracted.metadata["newline"]},
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    if output_format in {"json", "both"}:
        render_json(report, output_dir / "report.json")
    if output_format in {"md", "both"}:
        render_markdown(report, output_dir / "report.md")
    return report
