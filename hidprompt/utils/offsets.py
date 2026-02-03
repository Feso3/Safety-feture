from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class OffsetMap:
    line_offsets: List[int]


def build_offset_map(text: str) -> OffsetMap:
    offsets = [0]
    for idx, char in enumerate(text):
        if char == "\n":
            offsets.append(idx + 1)
    return OffsetMap(line_offsets=offsets)


def line_for_offset(offsets: OffsetMap, offset: int) -> int:
    line_no = 1
    for idx, line_offset in enumerate(offsets.line_offsets):
        if line_offset > offset:
            break
        line_no = idx + 1
    return line_no


def snippet_for_offset(text: str, offset: int, radius: int = 40) -> Tuple[str, int, int]:
    start = max(0, offset - radius)
    end = min(len(text), offset + radius)
    return text[start:end], start, end
