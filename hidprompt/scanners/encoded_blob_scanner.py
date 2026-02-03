import re
from typing import Dict, Iterable, List

from hidprompt.utils.offsets import line_for_offset, snippet_for_offset

BASE64_RE = re.compile(r"(?:[A-Za-z0-9+/]{4}){12,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?")


def scan(text: str, offsets) -> Iterable[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    for match in BASE64_RE.finditer(text):
        snippet, start, end = snippet_for_offset(text, match.start())
        findings.append(
            {
                "category": "encoded_blob",
                "title": "Suspicious encoded blob",
                "severity": "MEDIUM",
                "confidence": 0.55,
                "evidence": match.group(0)[:80],
                "snippets": [{"text": snippet, "start": start, "end": end}],
                "offsets": {"start": match.start(), "end": match.end()},
                "line_numbers": {"start": line_for_offset(offsets, match.start())},
                "rationale": "Large encoded blobs can conceal hidden instructions or payloads.",
                "recommendation": "Inspect the encoded content and validate its purpose.",
                "tags": ["encoded", "base64"],
            }
        )
    return findings
