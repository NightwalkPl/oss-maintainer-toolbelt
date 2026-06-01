from __future__ import annotations

from pathlib import Path

from .changelog import build_changelog
from .config import issue_template_path_from_config, load_config
from .report import build_repo_report
from .templates import lint_issue_templates


def build_preflight_checklist(path: Path, since: str | None = None, config_path: Path | None = None) -> dict[str, object]:
    path = path.resolve()
    config = load_config(config_path or (path / ".omt.json"))
    report = build_repo_report(path, config_path=config_path)
    templates = lint_issue_templates(path / issue_template_path_from_config(config))
    changelog = build_changelog(path, since=since)

    checks = [
        {
            "name": "Required maintainer docs are present",
            "passed": not report["missing_docs"],
            "detail": ", ".join(report["missing_docs"]) if report["missing_docs"] else "all configured docs found",
        },
        {
            "name": "Issue templates are valid",
            "passed": not templates["problems"],
            "detail": "; ".join(templates["problems"]) if templates["problems"] else "templates look good",
        },
        {
            "name": "Changelog draft can be generated",
            "passed": "No commits found." not in changelog["markdown"],
            "detail": "commit history found" if "No commits found." not in changelog["markdown"] else "no commits found",
        },
    ]

    markdown_lines = ["# Pre-release Checklist", ""]
    for check in checks:
        mark = "x" if check["passed"] else " "
        markdown_lines.append(f"- [{mark}] {check['name']} - {check['detail']}")
    markdown_lines.extend(["", "## Changelog Draft", "", changelog["markdown"].strip(), ""])

    return {
        "path": str(path),
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
        "markdown": "\n".join(markdown_lines),
    }
