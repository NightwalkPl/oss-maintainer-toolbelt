from __future__ import annotations

import subprocess
from pathlib import Path

from .config import DEFAULT_CONFIG, load_config, required_docs_from_config

IMPORTANT_FILES = DEFAULT_CONFIG["required_docs"]


def _git_count(path: Path, args: list[str]) -> int:
    result = subprocess.run(["git", "-C", str(path), *args], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def _markdown_report(data: dict[str, object]) -> str:
    present = data["present_docs"]
    missing = data["missing_docs"]
    lines = [
        "# Repository Maintenance Report",
        "",
        f"- Repository: `{data['path']}`",
        f"- Maintenance score: **{data['score']}/100**",
        f"- Commits: {data['commits']}",
        f"- Contributors: {data['contributors']}",
        f"- Tags: {data['tags']}",
        "",
        "## Documentation",
        "",
        f"- Present: {', '.join(present) if present else 'none'}",
        f"- Missing: {', '.join(missing) if missing else 'none'}",
        "",
    ]
    return "\n".join(lines)


def build_repo_report(path: Path, config_path: Path | None = None) -> dict[str, object]:
    path = path.resolve()
    config = load_config(config_path or (path / ".omt.json"))
    important_files = required_docs_from_config(config)
    present = [name for name in important_files if (path / name).exists()]
    missing = [name for name in important_files if name not in present]
    commit_count = _git_count(path, ["log", "--pretty=%H"])
    contributor_count = _git_count(path, ["shortlog", "-sn", "HEAD"])
    tag_count = _git_count(path, ["tag", "--list"])

    score = 0
    score += min(commit_count, 10) * 4
    score += min(contributor_count, 5) * 5
    score += min(tag_count, 5) * 3
    score += len(present) * 8
    score = min(score, 100)

    lines = [
        f"Repository: {path}",
        f"Maintenance score: {score}/100",
        f"Commits: {commit_count}",
        f"Contributors: {contributor_count}",
        f"Tags: {tag_count}",
        f"Present docs: {', '.join(present) or 'none'}",
        f"Missing docs: {', '.join(missing) or 'none'}",
    ]

    data = {
        "path": str(path),
        "score": score,
        "commits": commit_count,
        "contributors": contributor_count,
        "tags": tag_count,
        "present_docs": present,
        "missing_docs": missing,
        "summary": "\n".join(lines),
    }
    data["markdown"] = _markdown_report(data)
    return data
