import json
from pathlib import Path
from typing import Dict


def render(report: Dict[str, object], output_path: Path) -> Path:
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return output_path
