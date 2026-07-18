> Status: [FILL: e.g. "Phase 0 in progress"] | Audience: contributors and
> agents planning next work | See also: [docs/README.md](README.md),
> [../CHANGELOG.md](../CHANGELOG.md)

<!--
PLAN-DOC LIFECYCLE — read before editing.

This document holds forward work only. A phase is a slice of capability with
an exit criterion phrased as something observable — a command that succeeds,
a page that loads, a check that passes — never "code complete," which nobody
can verify from outside the author's head.

When a phase ships, CUT it from this file. Git history keeps the detail; this
file is not the historical record, the progress log below is. That log is
intentionally the *only* place the past survives here — one line per
completion, append-only. If you want the full story of a shipped phase, `git
log` the commits that closed it, or check `docs/archive/` if it was a
one-time plan rather than a recurring phase.

Keep exactly one phase "in progress" at a time in the body of this doc; stack
the rest in the Backlog section below, unordered until they're picked up.
-->

# Implementation plan

## Phase 0 — Engineering substrate

<!-- WORKED EXAMPLE — replace with your actual phase 0 slices, or delete this
     phase entirely once it ships (see lifecycle note above). -->

Stand up the scaffolding every later phase depends on, before the first
feature makes it expensive to retrofit.

- **Task runner with core verbs.** Wire `dev`, `test`, `lint`, `reset` (even
  as thin wrappers around one placeholder command each).
  Exit criterion: a new clone runs `[FILL: task-runner] dev` and reaches a
  running stack with no manual step.
- **Env contract + secret scanner.** Commit `.env.example`; add a secret
  scanner as a commit hook and a CI job.
  Exit criterion: committing a fake secret is blocked locally, and a PR that
  slips one past the hook is blocked in CI.
- **CI fast tier.** Lint + unit tests running on every PR.
  Exit criterion: a red PR shows a named, actionable failure within [FILL:
  target minutes] of push.
- **Docs skeleton.** `design/`, `development/`, `decisions/`, `archive/`
  trees exist with index files, even mostly empty.
  Exit criterion: a newcomer finds `docs/README.md` and can name which tree
  answers their question, without asking anyone.

## Verification

Phase 0 complete when:

- [ ] `[FILL: task-runner] dev` brings up a working stack from a clean clone.
- [ ] `[FILL: task-runner] test` and `[FILL: task-runner] lint` both run in CI
      on every pull request.
- [ ] A committed fake secret is caught before it reaches the remote.
- [ ] `docs/README.md` routes a newcomer to the right tree in one hop.

## Backlog

<!-- Unordered, not-yet-scheduled work. Move an item up into its own phase
     section when it's picked up; delete it from here in the same commit. -->

- [FILL: next capability slice]
- [FILL: next capability slice]

## Progress log

<!--
Append-only, reverse-chronological (newest entry at the top). One line per
shipped phase or major slice:

  **YYYY-MM-DD** — one-line note, carrying the commit ref and the numbers
  that matter (tests passing, endpoints live, whatever is checkable).

This is an audit trail, not a diary — no adjectives, no narrative, just what
shipped and the evidence. Delete the example entry below once a real one
replaces it.
-->

- **2024-01-01** — *(example, delete me)* Phase 0 engineering substrate
  shipped: task runner + secret scanner + CI fast tier green (`abc1234`, 12
  tests passing).
