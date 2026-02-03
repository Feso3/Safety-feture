from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from hidprompt.utils.hashing import sha256_file
from hidprompt.utils.normalization import normalize_text
from hidprompt.utils.offsets import build_offset_map, OffsetMap


@dataclass(frozen=True)
class ExtractedContent:
    text: str
    offsets: OffsetMap
    metadata: Dict[str, str]


def extract_text(path: Path) -> ExtractedContent:
    raw = path.read_text(encoding="utf-8", errors="replace")
    normalized = normalize_text(raw)
    offsets = build_offset_map(normalized.text)
    metadata = {
        "source": str(path),
        "sha256": sha256_file(path),
        "size": str(path.stat().st_size),
        "newline": normalized.newline,
        "mime": "text/plain",
    }
    return ExtractedContent(text=normalized.text, offsets=offsets, metadata=metadata)
