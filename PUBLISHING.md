# Publishing Checklist

This repository is ready to publish as `NightwalkPl/oss-maintainer-toolbelt`.

## Option A: GitHub website

1. Open https://github.com/new
2. Repository name: `oss-maintainer-toolbelt`
3. Visibility: `Public`
4. Do not add README, license, or `.gitignore`; they already exist locally.
5. Create repository.
6. Run:

```powershell
git remote add origin https://github.com/NightwalkPl/oss-maintainer-toolbelt.git
git push -u origin main
```

## Option B: GitHub CLI

Install GitHub CLI, sign in, then run:

```powershell
gh auth login
gh repo create NightwalkPl/oss-maintainer-toolbelt --public --source . --remote origin --push
```

## After publishing

1. Confirm the repository is public.
2. Confirm GitHub Actions runs the CI workflow.
3. Add repository topics:
   - `open-source`
   - `maintainers`
   - `changelog`
   - `github`
   - `cli`
4. Create a first issue named `Roadmap: GitHub API triage summaries`.
5. Consider enabling GitHub private vulnerability reporting.

