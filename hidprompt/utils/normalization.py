from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedText:
    text: str
    newline: str


def normalize_text(raw: str) -> NormalizedText:
    if "\r\n" in raw:
        return NormalizedText(text=raw.replace("\r\n", "\n"), newline="\r\n")
    return NormalizedText(text=raw.replace("\r", "\n"), newline="\n")
