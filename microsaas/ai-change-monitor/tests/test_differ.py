from app.services.differ import build_diff
from app.services.summarizer import summarize_diff


def test_build_diff_returns_unified_diff():
    diff = build_diff("Alpha\nBeta", "Alpha\nGamma")

    assert "--- previous" in diff
    assert "+++ current" in diff
    assert "-Beta" in diff
    assert "+Gamma" in diff


def test_summarize_diff_counts_line_changes():
    diff = "--- previous\n+++ current\n@@ -1 +1 @@\n-Old\n+New"

    assert summarize_diff(diff) == "Detected 1 added line(s) and 1 removed line(s)."

