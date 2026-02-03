import re
from typing import Dict, Iterable, List

from hidprompt.utils.offsets import build_offset_map, line_for_offset, snippet_for_offset


PATTERNS = [
    (
        "inline_display_none",
        re.compile(r"style\s*=\s*['\"][^'\"]*display\s*:\s*none[^'\"]*['\"]", re.I),
        "Elements styled with display:none are invisible to users.",
    ),
    (
        "inline_visibility_hidden",
        re.compile(r"style\s*=\s*['\"][^'\"]*visibility\s*:\s*hidden[^'\"]*['\"]", re.I),
        "Elements styled with visibility:hidden are invisible to users.",
    ),
    (
        "inline_opacity_zero",
        re.compile(r"style\s*=\s*['\"][^'\"]*opacity\s*:\s*0(?:\.0+)?[^'\"]*['\"]", re.I),
        "Elements styled with opacity:0 are invisible to users.",
    ),
    (
        "inline_font_size_zero",
        re.compile(r"style\s*=\s*['\"][^'\"]*font-size\s*:\s*0(?:px|em|rem|%)?[^'\"]*['\"]", re.I),
        "Elements styled with font-size:0 hide text.",
    ),
    (
        "inline_zero_size",
        re.compile(
            r"style\s*=\s*['\"][^'\"]*(height\s*:\s*0|width\s*:\s*0)[^'\"]*['\"]",
            re.I,
        ),
        "Zero-sized elements can conceal hidden text.",
    ),
    (
        "hidden_attribute",
        re.compile(r"<[^>]*\bhidden\b[^>]*>", re.I),
        "Elements marked as hidden are not visible to users.",
    ),
    (
        "aria_hidden_true",
        re.compile(r"aria-hidden\s*=\s*['\"]true['\"]", re.I),
        "aria-hidden elements are hidden from assistive technologies.",
    ),
    (
        "input_type_hidden",
        re.compile(r"<input[^>]*type\s*=\s*['\"]hidden['\"][^>]*>", re.I),
        "Hidden inputs can carry unseen instructions or payloads.",
    ),
]


def scan(html: str) -> Iterable[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    offsets = build_offset_map(html)
    for name, regex, rationale in PATTERNS:
        for match in regex.finditer(html):
            snippet, start, end = snippet_for_offset(html, match.start())
            findings.append(
                {
                    "category": "hidden_text_html",
                    "title": f"Hidden HTML pattern: {name}",
                    "severity": "HIGH",
                    "confidence": 0.7,
                    "evidence": match.group(0)[:120],
                    "snippets": [{"text": snippet, "start": start, "end": end}],
                    "offsets": {"start": match.start(), "end": match.end()},
                    "line_numbers": {"start": line_for_offset(offsets, match.start())},
                    "rationale": rationale,
                    "recommendation": "Review the hidden element and remove concealed instructions.",
                    "tags": [name, "html"],
                }
            )
    return findings
