# Contributing

This is the human-readable mirror of `CLAUDE.md`. **`CLAUDE.md` is the source
of truth for conventions** — if this file and `CLAUDE.md` ever disagree,
`CLAUDE.md` wins and this file has drifted; fix the drift, don't pick a
favorite. This document points at conventions; it doesn't restate them in
full.

## Branching

- `develop` is the integration branch. `feature/*`, `fix/*`, and `docs/*`
  branch off `develop` and PR back into it.
- `hotfix/*` branches off `main` (production), PRs to `main`, then
  back-merges into `develop` — mandatorily, so the fix isn't silently reverted
  by the next release.
- All changes land via pull request. There is no sanctioned direct push to
  `main` or `develop`.
- Merges use **merge commits, never squash**. The versioning tool reads merge
  history to compute the next version; squashing erases the signal it needs.

## What CI runs where

- **Fast tier** (lint, types, drift check, unit, integration) runs on every
  pull request. It's PR-triggered, not push-triggered, so minutes aren't spent
  twice.
- **Full gate** (end-to-end suite, accessibility, container vulnerability
  scan, deep review) runs only on pull requests into `main` — where a red
  result actually blocks a release.

See `.github/workflows/ci.yml` for the exact steps.

## Commit hooks

Install once per clone:

```text
[FILL: pre-commit install]
```

The hooks run the formatter, the linter, the schema-drift check, and a secret
scanner (gitleaks) before a commit is created — the same checks the fast CI
tier runs, so a hook failure locally means CI would have failed too.

## Definition of Done

A change is done when, mirroring `CLAUDE.md`:

- [ ] Tests pass at every tier the change touches
- [ ] Lint, format, and types are clean
- [ ] Schema-drift check is clean, if models changed
- [ ] Docs are updated, if behavior or structure changed
- [ ] Changelog entry added, if the change is user-facing
- [ ] Decision stamp + decisions index row added, if a decision was made

## Recording decisions

A load-bearing decision gets recorded in the same commit it's made in, two
places at once:

1. An inline stamp at the point of relevance in `docs/design/` — date, issue
   reference, and supersession note if it replaces an earlier decision.
2. A one-line entry in `docs/decisions/README.md` so the decision is
   discoverable without reading every design doc.

A decision recorded in only one place is half-recorded — it either has no
context (index only) or isn't discoverable (inline only).
