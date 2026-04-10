def summarize_diff(diff_text: str) -> str:
    added = 0
    removed = 0
    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1

    if added == 0 and removed == 0:
        return "No visible content changes detected."
    if added > 0 and removed == 0:
        return f"Detected {added} added line(s)."
    if removed > 0 and added == 0:
        return f"Detected {removed} removed line(s)."
    return f"Detected {added} added line(s) and {removed} removed line(s)."

