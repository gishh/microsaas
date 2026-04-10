from difflib import unified_diff


def build_diff(previous_text: str, current_text: str) -> str:
    previous_lines = previous_text.splitlines()
    current_lines = current_text.splitlines()
    diff = unified_diff(previous_lines, current_lines, fromfile="previous", tofile="current", lineterm="")
    result = "\n".join(diff).strip()
    return result or "No textual changes detected."

