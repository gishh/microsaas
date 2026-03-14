from __future__ import annotations

from app.risk_engine import score_text


def test_score_text_detects_high_risk_language() -> None:
    result = score_text("ACT NOW!!! This secret offer is guaranteed and available for a limited time.")

    assert result["level"] == "high"
    assert result["score"] >= 60
    assert len(result["findings"]) >= 3
