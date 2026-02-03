from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional

from hidprompt.utils.hashing import sha256_file
from hidprompt.utils.normalization import normalize_text
from hidprompt.utils.offsets import build_offset_map, OffsetMap


BLOCK_TAGS = {
    "p",
    "div",
    "section",
    "article",
    "header",
    "footer",
    "li",
    "ul",
    "ol",
    "table",
    "tr",
    "td",
    "th",
    "br",
    "hr",
}


@dataclass(frozen=True)
class ExtractedContent:
    text: str
    offsets: OffsetMap
    metadata: Dict[str, str]
    raw_html: Optional[str] = None


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in BLOCK_TAGS:
            self._append_newline()

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in BLOCK_TAGS:
            self._append_newline()

    def handle_data(self, data: str) -> None:
        if data:
            self._chunks.append(data)

    def _append_newline(self) -> None:
        if not self._chunks or not self._chunks[-1].endswith("\n"):
            self._chunks.append("\n")

    def text(self) -> str:
        return "".join(self._chunks)


def extract_html(path: Path) -> ExtractedContent:
    raw_html = path.read_text(encoding="utf-8", errors="replace")
    parser = HTMLTextExtractor()
    parser.feed(raw_html)
    parser.close()
    normalized = normalize_text(parser.text())
    offsets = build_offset_map(normalized.text)
    metadata = {
        "source": str(path),
        "sha256": sha256_file(path),
        "size": str(path.stat().st_size),
        "newline": normalized.newline,
        "mime": "text/html",
    }
    return ExtractedContent(
        text=normalized.text,
        offsets=offsets,
        metadata=metadata,
        raw_html=raw_html,
    )
