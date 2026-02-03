from typing import Dict, List, Tuple

SEVERITY_WEIGHTS = {
    "HIGH": 45,
    "MEDIUM": 20,
    "LOW": 5,
}


def score_findings(findings: List[Dict[str, object]]) -> Tuple[int, str]:
    score = 0
    for finding in findings:
        score += SEVERITY_WEIGHTS.get(finding["severity"], 0)
    score = min(score, 100)
    if score >= 70:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"
    return score, level
