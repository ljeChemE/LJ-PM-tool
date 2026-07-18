---
description: Environment health check — read-only pass/fail punch list
---

You are running the `/doctor` skill. READ-ONLY. Do not modify anything, even
if a check fails — diagnosis only. If something is broken, the human decides
what to do; you report, you don't repair.

## Checks

Run each. Record OK / FAIL / SKIP + one-line detail. Stop for no single
failure — run the whole list, then report.

1. **Git repo + status.** `git rev-parse --is-inside-work-tree` confirms this
   is a repo. `git status --porcelain` — empty is clean, non-empty is dirty
   (dirty is not a FAIL, just report it).
2. **Task runner present.** `just --version`. FAIL if missing — nothing else
   in this kit works without it.
3. **Container runtime up.**
   <!-- FILL: the liveness check for your container runtime, e.g.
        `docker info >/dev/null 2>&1` or `podman info >/dev/null 2>&1` -->
   SKIP if this project doesn't containerize its services.
4. **`.env` exists and its keys match `.env.example`.** Compare the **key
   names only** — never values — between `.env` and `.env.example`. Report
   any key present in one file and missing from the other, by name only.
   SKIP if `.env.example` doesn't exist yet.
5. **Commit hooks installed.** Check that `.git/hooks/pre-commit` exists.
   FAIL if missing — Pillar VI enforcement isn't wired locally.
6. **`just health` reachable.** Run `just health`. OK only if it exits zero
   and prints a health payload; FAIL otherwise (including "not implemented").

## Output

Print a markdown table:

```markdown
| # | Check | Status | Detail |
| --- | --- | --- | --- |
| 1 | Git repo + status | OK | clean |
```

End with exactly one verdict line: `All green.` or `N issue(s) — see above.`

Never attempt a fix, never suggest a specific fix inline in the table — the
detail column states what's wrong, not what to do about it.
