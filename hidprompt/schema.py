from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List


@dataclass(frozen=True)
class SummaryCounts:
    high: int
    medium: int
    low: int


@dataclass(frozen=True)
class ReportMetadata:
    tool: str
    version: str
    scan_id: str
    timestamp: str


def now_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def counts_from_findings(findings: List[Dict[str, object]]) -> SummaryCounts:
    high = sum(1 for f in findings if f["severity"] == "HIGH")
    medium = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low = sum(1 for f in findings if f["severity"] == "LOW")
    return SummaryCounts(high=high, medium=medium, low=low)
