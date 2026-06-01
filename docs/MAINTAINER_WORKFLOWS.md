# Maintainer Workflows

`oss-maintainer-toolbelt` is designed for small checks that maintainers can run locally or in CI.

## Before opening a release pull request

```bash
omt report .
omt changelog . --since v0.1.0
omt template-lint .github/ISSUE_TEMPLATE
```

Use the report to confirm core project files are present, then paste the changelog draft into release notes.

## Before merging setup-related changes

```bash
omt env-check --example .env.example --actual .env
```

This catches missing environment keys before contributors hit setup failures.

## During contributor experience cleanup

```bash
omt template-lint .github/ISSUE_TEMPLATE --json
```

JSON output is useful for CI annotations, bots, or project dashboards.

