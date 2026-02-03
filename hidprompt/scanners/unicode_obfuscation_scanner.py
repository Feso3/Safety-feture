from typing import Dict, Iterable, List

from hidprompt.utils.offsets import line_for_offset, snippet_for_offset

BIDI_CONTROLS = {
    "\u202a": "LEFT-TO-RIGHT EMBEDDING",
    "\u202b": "RIGHT-TO-LEFT EMBEDDING",
    "\u202d": "LEFT-TO-RIGHT OVERRIDE",
    "\u202e": "RIGHT-TO-LEFT OVERRIDE",
    "\u2066": "LEFT-TO-RIGHT ISOLATE",
    "\u2067": "RIGHT-TO-LEFT ISOLATE",
    "\u2068": "FIRST STRONG ISOLATE",
    "\u2069": "POP DIRECTIONAL ISOLATE",
}
ZERO_WIDTH = {
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE",
}


def scan(text: str, offsets) -> Iterable[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    for idx, char in enumerate(text):
        if char in BIDI_CONTROLS or char in ZERO_WIDTH:
            name = BIDI_CONTROLS.get(char) or ZERO_WIDTH.get(char)
            snippet, start, end = snippet_for_offset(text, idx)
            findings.append(
                {
                    "category": "unicode_obfuscation",
                    "title": f"Unicode control character: {name}",
                    "severity": "MEDIUM",
                    "confidence": 0.7,
                    "evidence": f"U+{ord(char):04X} {name}",
                    "snippets": [{"text": snippet, "start": start, "end": end}],
                    "offsets": {"start": idx, "end": idx + 1},
                    "line_numbers": {"start": line_for_offset(offsets, idx)},
                    "rationale": "Control characters can hide or reorder text to mislead reviewers.",
                    "recommendation": "Remove or replace the control characters after verifying intent.",
                    "tags": ["unicode", "obfuscation"],
                }
            )
    return findings
