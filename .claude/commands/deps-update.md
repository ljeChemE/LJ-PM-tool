---
description: Upgrade the lockfile, rebuild, run tests — stops on regression
---

You are running the `/deps-update` skill. WRITES to the lockfile and rebuilds
the environment. **Never commits** — it leaves a reviewable diff for the
human to inspect and commit themselves.

## 1. Require a clean tree

`git status --porcelain` must be empty. Abort otherwise: "Uncommitted
changes — commit or stash before running `/deps-update`." The diff this skill
produces must start from a clean baseline or it can't be reviewed in
isolation.

## 2. Upgrade the lockfile

```bash
# FILL: the per-ecosystem lockfile-upgrade command, e.g.:
#   uv lock --upgrade           (Python, uv)
#   npm update && npm install   (Node)
#   bundle update                (Ruby)
```

Report the set of packages that moved (name, old version to new version).

## 3. Rebuild / reinstall

Run whatever this project uses to rebuild its environment from the new
lockfile (e.g. `just build`, or the ecosystem's install step). **On build
failure:**

```bash
git checkout -- [lockfile]
```

Report the failing package(s) and stop. Roll all the way back — a broken
build means the upgrade itself is not viable yet, so there's nothing to
leave for review.

## 4. Run tests

```bash
just test
```

**On test failure:** do **not** roll back. Leave the lockfile diff in place —
the human needs to see exactly what changed to understand what broke. Print
which tests failed, then stop.

This is a deliberately asymmetric rollback policy: a build failure means the
upgrade doesn't work at all (nothing to inspect); a test failure means it
works differently (everything to inspect).

## On success

Report:

- Number of packages upgraded, with any load-bearing ones called out by name.
- Test result summary.
- A reminder that the lockfile is modified and uncommitted — review the diff,
  then commit it yourself. This skill never commits.
