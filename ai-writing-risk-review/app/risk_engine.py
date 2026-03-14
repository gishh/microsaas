from __future__ import annotations

import re
from collections.abc import Iterable


RISK_PATTERNS: dict[str, tuple[Iterable[str], int]] = {
    "urgency": (("urgent", "immediately", "act now", "last chance"), 20),
    "guarantees": (("guaranteed", "risk-free", "no downside", "certain"), 18),
    "manipulation": (("secret", "exclusive", "hidden truth", "they don't want you to know"), 16),
    "pressure": (("must", "only today", "limited time", "before it's gone"), 12),
}


def score_text(text: str) -> dict[str, object]:
    lowered = text.lower()
    findings: list[dict[str, object]] = []
    score = 0

    for category, (phrases, weight) in RISK_PATTERNS.items():
        matches = [phrase for phrase in phrases if phrase in lowered]
        if not matches:
            continue
        score += weight * len(matches)
        findings.append(
            {
                "category": category,
                "matches": matches,
                "weight": weight,
            }
        )

    exclamation_marks = text.count("!")
    if exclamation_marks >= 3:
        score += 10
        findings.append(
            {
                "category": "punctuation",
                "matches": [f"{exclamation_marks} exclamation marks"],
                "weight": 10,
            }
        )

    all_caps_words = re.findall(r"\b[A-Z]{4,}\b", text)
    if all_caps_words:
        score += min(len(all_caps_words) * 5, 15)
        findings.append(
            {
                "category": "tone",
                "matches": all_caps_words,
                "weight": min(len(all_caps_words) * 5, 15),
            }
        )

    score = min(score, 100)
    level = "low"
    if score >= 60:
        level = "high"
    elif score >= 30:
        level = "medium"

    return {
        "score": score,
        "level": level,
        "findings": findings,
    }
