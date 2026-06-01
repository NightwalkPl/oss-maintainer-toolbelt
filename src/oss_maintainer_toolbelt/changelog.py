from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


COMMIT_RE = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\([^)]+\))?(?P<breaking>!)?: (?P<text>.+)$")
CATEGORIES = {
    "feat": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "refactor": "Refactors",
    "docs": "Documentation",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Chores",
}


@dataclass(frozen=True)
class CommitEntry:
    sha: str
    subject: str


def _git_log(path: Path, since: str | None, until: str) -> list[CommitEntry]:
    revision = until if since is None else f"{since}..{until}"
    cmd = ["git", "-C", str(path), "log", "--pretty=format:%h%x09%s", revision]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    entries: list[CommitEntry] = []
    for line in result.stdout.splitlines():
        if "\t" not in line:
            continue
        sha, subject = line.split("\t", 1)
        entries.append(CommitEntry(sha=sha.strip(), subject=subject.strip()))
    return entries


def build_changelog(path: Path, since: str | None = None, until: str = "HEAD") -> dict[str, object]:
    grouped: dict[str, list[str]] = {label: [] for label in CATEGORIES.values()}
    grouped["Breaking Changes"] = []
    grouped["Other"] = []

    for entry in _git_log(path, since, until):
        match = COMMIT_RE.match(entry.subject)
        if not match:
            grouped["Other"].append(f"- {entry.subject} ({entry.sha})")
            continue
        label = CATEGORIES.get(match.group("type").lower(), "Other")
        line = f"- {match.group('text')} ({entry.sha})"
        if match.group("breaking"):
            grouped["Breaking Changes"].append(line)
        grouped[label].append(line)

    sections: list[str] = ["# Changelog", ""]
    for label, items in grouped.items():
        if not items:
            continue
        sections.extend([f"## {label}", "", *items, ""])

    if len(sections) == 2:
        sections.append("No commits found.")

    return {"groups": grouped, "markdown": "\n".join(sections).rstrip() + "\n"}

