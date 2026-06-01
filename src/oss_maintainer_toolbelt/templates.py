from __future__ import annotations

from pathlib import Path


REQUIRED_FRONT_MATTER = {"name", "about", "title", "labels"}


def _parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def lint_issue_templates(path: Path) -> dict[str, object]:
    problems: list[str] = []
    checked = 0

    if not path.exists():
        return {
            "checked": checked,
            "problems": [f"Template path does not exist: {path}"],
            "summary": f"Template path does not exist: {path}",
        }

    for template in sorted(path.glob("*.md")):
        checked += 1
        front_matter = _parse_front_matter(template.read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_FRONT_MATTER - set(front_matter))
        if missing:
            problems.append(f"{template.name}: missing front matter keys: {', '.join(missing)}")
        if not any(heading.startswith("## ") for heading in template.read_text(encoding="utf-8").splitlines()):
            problems.append(f"{template.name}: add at least one section heading")

    if checked == 0:
        problems.append(f"No markdown issue templates found in {path}")

    summary = "Issue templates look good." if not problems else "\n".join(problems)
    return {"checked": checked, "problems": problems, "summary": summary}

