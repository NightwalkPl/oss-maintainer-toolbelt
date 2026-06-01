from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .changelog import build_changelog
from .envcheck import compare_env_files
from .report import build_repo_report
from .templates import lint_issue_templates


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="omt",
        description="Small CLI helpers for open source maintainer chores.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    report = subparsers.add_parser("report", help="Summarize repository maintenance signals.")
    report.add_argument("path", nargs="?", default=".", help="Repository path.")
    report.add_argument("--json", action="store_true", help="Emit JSON.")

    changelog = subparsers.add_parser("changelog", help="Build changelog text from git commits.")
    changelog.add_argument("path", nargs="?", default=".", help="Repository path.")
    changelog.add_argument("--since", help="Oldest git revision to include, for example v1.2.0.")
    changelog.add_argument("--until", default="HEAD", help="Newest git revision to include.")
    changelog.add_argument("--json", action="store_true", help="Emit JSON.")

    env = subparsers.add_parser("env-check", help="Compare .env against .env.example.")
    env.add_argument("--example", default=".env.example", help="Example env file.")
    env.add_argument("--actual", default=".env", help="Actual env file.")
    env.add_argument("--json", action="store_true", help="Emit JSON.")

    templates = subparsers.add_parser("template-lint", help="Lint GitHub issue templates.")
    templates.add_argument("path", nargs="?", default=".github/ISSUE_TEMPLATE", help="Template directory.")
    templates.add_argument("--json", action="store_true", help="Emit JSON.")

    args = parser.parse_args(argv)

    if args.command == "report":
        data = build_repo_report(Path(args.path))
        if args.json:
            _print_json(data)
        else:
            print(data["summary"])
        return 0

    if args.command == "changelog":
        data = build_changelog(Path(args.path), since=args.since, until=args.until)
        if args.json:
            _print_json(data)
        else:
            print(data["markdown"])
        return 0

    if args.command == "env-check":
        data = compare_env_files(Path(args.example), Path(args.actual))
        if args.json:
            _print_json(data)
        else:
            print(data["summary"])
        return 1 if data["missing"] else 0

    if args.command == "template-lint":
        data = lint_issue_templates(Path(args.path))
        if args.json:
            _print_json(data)
        else:
            print(data["summary"])
        return 1 if data["problems"] else 0

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

