from __future__ import annotations

import re
from pathlib import Path


KEY_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def _keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    found: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = KEY_RE.match(line)
        if match:
            found.add(match.group(1))
    return found


def compare_env_files(example: Path, actual: Path) -> dict[str, object]:
    expected = _keys(example)
    current = _keys(actual)
    missing = sorted(expected - current)
    extra = sorted(current - expected)

    if not example.exists():
        summary = f"Example file not found: {example}"
    elif not actual.exists():
        summary = f"Actual file not found: {actual}. Missing keys: {', '.join(missing) or 'none'}"
    elif missing:
        summary = f"Missing keys: {', '.join(missing)}"
    else:
        summary = "Environment files match required keys."
        if extra:
            summary += f" Extra local keys: {', '.join(extra)}"

    return {
        "example": str(example),
        "actual": str(actual),
        "expected": sorted(expected),
        "current": sorted(current),
        "missing": missing,
        "extra": extra,
        "summary": summary,
    }

