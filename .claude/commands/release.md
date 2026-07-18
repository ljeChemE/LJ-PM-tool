---
description: Guided release — verify gates, tag vX.Y.Z on main, push, watch CI
argument-hint: <major|minor|patch>
---

You are running the `/release` skill. This tags a release on `main` and
triggers the release workflow. **Refuses on any red precondition** — it does
not push through a failing check.

## Argument

`$ARGUMENTS` must be exactly one of: `major`, `minor`, `patch`. Missing or any
other value — abort with a one-line error before touching anything.

## Preflight — refuse if any of these are red

1. **On `main`.** `git rev-parse --abbrev-ref HEAD` must equal `main`.
   Releases only cut from `main`.
2. **In sync with `origin/main`.** `git fetch origin main`, then compare. If
   local is ahead: abort "Push first." If behind: abort "Pull first."
3. **Working tree clean.** `git status --porcelain` empty.
4. **Local gates green:** `just lint`, `just typecheck`, `just test`. Run all
   three; if any fail, stop and print the failing output verbatim. Do not
   tag.
5. **Changelog has a section for the target version.** See below — this is a
   mechanical check, not a judgment call.

## Compute the target version

- Current version: `just version`.
- Bump it per `$ARGUMENTS` (major/minor/patch) to get the target `X.Y.Z`.
- Mechanically confirm `CHANGELOG.md` contains a `## [X.Y.Z]` section:
  ```bash
  grep -q "^## \[X.Y.Z\]" CHANGELOG.md || { echo "CHANGELOG.md has no section for X.Y.Z"; exit 1; }
  ```
  Abort if it doesn't — do not write the section yourself; the changelog is
  authored by the change that earned it, not by this skill.

## Confirm and tag

State the **exact tag** about to be created: `vX.Y.Z`. Ask verbatim:

> About to tag `vX.Y.Z` and push it. Proceed? (yes/no)

Require an explicit `yes`. Anything else — abort, no changes made.

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Watch CI

```bash
gh run watch --exit-status
```

Watch the release workflow run triggered by the tag push. Report the final
state, and the built artifact reference if the workflow prints one.

## On CI failure

Report exactly which job failed and why (surface the raw log, don't
summarize it away). **Do not auto-delete the tag.** Print the manual-delete
commands so the user can retry deliberately once the fix lands:

```bash
git push --delete origin vX.Y.Z
git tag -d vX.Y.Z
```
