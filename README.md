# OSS Maintainer Toolbelt

`oss-maintainer-toolbelt` is a small dependency-free CLI for repetitive open source maintainer chores.

It focuses on checks that are useful before releases, during repository cleanup, and while reviewing contributor experience:

- repository maintenance report;
- changelog draft from Conventional Commits;
- `.env` drift check against `.env.example`;
- GitHub issue template linting.

## Install

```bash
python -m pip install .
```

For local development:

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Usage

Generate a repository report:

```bash
omt report .
```

Draft a changelog from commits:

```bash
omt changelog . --since v0.1.0
```

Check local environment keys:

```bash
omt env-check --example .env.example --actual .env
```

Lint GitHub issue templates:

```bash
omt template-lint .github/ISSUE_TEMPLATE
```

Every command supports `--json` for automation.

## Why maintainers might use it

Small projects often miss the lightweight checks that larger maintainership teams automate:

- release notes are written by hand and lose useful context;
- contributors hit missing `.env` keys during setup;
- issue templates drift and collect low-quality reports;
- repository health is hard to summarize before a cleanup pass.

This tool keeps those checks local, transparent, and easy to run in CI.

## Roadmap

- GitHub API mode for open issue and pull request triage summaries.
- Markdown output for repository reports.
- Config file support for project-specific required docs.
- Pre-release checklist generation.

## License

MIT

