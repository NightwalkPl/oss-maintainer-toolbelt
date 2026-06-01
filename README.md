# OSS Maintainer Toolbelt

`oss-maintainer-toolbelt` is a small dependency-free CLI for repetitive open source maintainer chores.

It focuses on checks that are useful before releases, during repository cleanup, and while reviewing contributor experience:

- repository maintenance report;
- configurable required documentation checks;
- changelog draft from Conventional Commits;
- `.env` drift check against `.env.example`;
- GitHub issue template linting;
- pre-release checklist generation.

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
omt report . --markdown
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

Build a pre-release checklist:

```bash
omt preflight . --since v0.1.0
```

Every command supports `--json` for automation.

## Configuration

Create `.omt.json` in the repository root:

```json
{
  "required_docs": ["README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md"],
  "issue_template_path": ".github/ISSUE_TEMPLATE"
}
```

## Maintainer docs

- [Maintainer workflows](docs/MAINTAINER_WORKFLOWS.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Why maintainers might use it

Small projects often miss the lightweight checks that larger maintainership teams automate:

- release notes are written by hand and lose useful context;
- contributors hit missing `.env` keys during setup;
- issue templates drift and collect low-quality reports;
- repository health is hard to summarize before a cleanup pass.

This tool keeps those checks local, transparent, and easy to run in CI.

## Roadmap

The short version:

- configurable repository health checks;
- markdown output for reports;
- pre-release checklist generation;
- optional GitHub API and OpenAI-assisted triage workflows.

See [docs/ROADMAP.md](docs/ROADMAP.md) for the fuller plan.

## License

MIT
