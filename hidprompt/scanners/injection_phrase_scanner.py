import re
from dataclasses import dataclass
from typing import Dict, Iterable, List

from hidprompt.utils.offsets import line_for_offset, snippet_for_offset


@dataclass(frozen=True)
class InjectionPattern:
    name: str
    regex: re.Pattern
    severity: str
    confidence: float


PATTERNS: List[InjectionPattern] = [
    InjectionPattern(
        name="override_previous",
        regex=re.compile(r"\b(ignore|override|forget)\b.{0,40}\b(previous|prior|earlier)\b", re.I | re.S),
        severity="HIGH",
        confidence=0.85,
    ),
    InjectionPattern(
        name="system_prompt_reference",
        regex=re.compile(r"\b(system\s+prompt|developer\s+message)\b", re.I),
        severity="HIGH",
        confidence=0.8,
    ),
    InjectionPattern(
        name="assistant_directive",
        regex=re.compile(r"\b(you are|act as)\b.{0,30}\b(assistant|agent)\b", re.I),
        severity="MEDIUM",
        confidence=0.6,
    ),
    InjectionPattern(
        name="tool_call_bait",
        regex=re.compile(r"\b(call|invoke|run)\b.{0,20}\b(tool|function|api)\b", re.I),
        severity="LOW",
        confidence=0.4,
    ),
]


def scan(text: str, offsets) -> Iterable[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    for pattern in PATTERNS:
        for match in pattern.regex.finditer(text):
            snippet, start, end = snippet_for_offset(text, match.start())
            finding = {
                "category": "prompt_injection_phrase",
                "title": f"Injection phrase pattern: {pattern.name}",
                "severity": pattern.severity,
                "confidence": pattern.confidence,
                "evidence": match.group(0),
                "snippets": [{"text": snippet, "start": start, "end": end}],
                "offsets": {"start": match.start(), "end": match.end()},
                "line_numbers": {"start": line_for_offset(offsets, match.start())},
                "rationale": "Detected language commonly used to override instructions or target agent behavior.",
                "recommendation": "Review the surrounding text and remove or neutralize suspicious directives.",
                "tags": [pattern.name],
            }
            findings.append(finding)
    return findings
