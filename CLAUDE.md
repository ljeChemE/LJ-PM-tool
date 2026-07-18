<!--
============================================================================
  STARTER CLAUDE.md — an idealized, stack-agnostic agent-context template
============================================================================
  Companion to Practices-Playbook.md (Pillar V explains the philosophy).

  HOW TO USE
  1. Save as CLAUDE.md at your repository root. If you use other agent tools,
     keep their context files (GEMINI.md, AGENTS.md, .cursorrules) identical
     in substance and change them in the same commit.
  2. Replace every [PLACEHOLDER]; delete any section that doesn't apply.
  3. Delete these guidance comments as sections become real — they don't
     render, but they cost agent context forever if left in.

  FOUR GOLDEN RULES
  - Gotchas are gold. The traps an agent cannot infer from the code are the
    highest-value lines in this file. Record each one the day it bites.
  - Every line costs context. This file is read at the start of every agent
    session. It is a map and a rulebook, not the documentation — link out
    rather than inline, and aim for under ~150 lines.
  - Stale is worse than absent. An agent trusts this file completely; if
    "Current State" lies, the agent acts on the lie. Updating it is part of
    shipping, not housekeeping.
  - Write instructions, not descriptions. "Run X before Y" beats "X is
    generally run before Y."
============================================================================
-->

# CLAUDE.md — Project Context

## What This Repository Is

[PROJECT NAME] — [one sentence: what it is and who it serves].

**Status:** [In development | Beta | Live in production at [URL] since [date]].

## Goal & Guiding Principle

[One paragraph: what you are building and the principle behind it — the
sentence every design decision must be defensible against. Link the philosophy
doc if one exists.]

<!-- Shape: "Build <X> following the '<principle>' pattern: <what that means in
     practice>. This replaces <prior approach>, which failed because <why>." -->

## Repository Map

<!-- Annotate the *why* for anything non-obvious. Keep in step with reality. -->

```text
[src/ or app/]          [what lives here]
[tests/]                [test tiers: unit / integration / e2e]
[docs/design/]          The what & why — domain, decisions (implementation-agnostic)
[docs/development/]     The how — setup, testing, daily workflow
[scripts/ or ops/]      [operational glue: deploys, pipelines, runbooks]
[<task-runner file>]    Canonical commands — the entry point for every operation
[<lockfile>]            Locked dependency versions (committed)
```

## Commands

<!-- The canonical verbs an agent will use constantly. Keep this table tiny;
     defer the full list to `<task-runner> --list`. -->

| Task | Command |
| --- | --- |
| Run the app locally | `[cmd]` |
| Run tests (all / one tier) | `[cmd]` / `[cmd <tier>]` |
| Lint + format | `[cmd]` |
| Type check | `[cmd]` |
| Apply schema changes | `[cmd]` |
| Reset the environment | `[cmd]` — destructive; asks for confirmation |

## Key Design Decisions — and Non-Goals

<!-- The load-bearing choices an agent must respect and never "helpfully" undo.
     Each: the decision + the one-line why + a link. Non-goals matter as much
     as goals — they stop well-meant scope creep. -->

- **[Decision]:** [what was decided and the one-line why]. See [link].
- **[Infrastructure parity]:** [e.g. "Tests run against the real [datastore],
  not a substitute — the app uses [specific features], and substitutes let
  schema changes lie."]
- **[Auth / access model]:** [one line + link to the design doc].
- **Non-goals:** [what this project deliberately does not do, and why].

## Current State / Active Work

<!-- Update whenever a milestone lands — this is how the agent knows the
     present and doesn't act on stale assumptions. -->

[What's shipped, what's in flight, the current focus, the current version.
Link the plan/backlog doc.]

## Conventions

<!-- The rules an agent and a new human must follow. Every rule that matters
     should also have an enforcement hook (pre-commit or CI) — name it. -->

- **Branching:** [the full model, spelled out so automation honors it: the
  integration branch, what PRs into what, how releases and hotfixes flow, and
  any sanctioned push exceptions].
- **All changes land via [PRs / your process];** [what CI runs where].
- **Testing:** [the philosophy in one line — e.g. "acceptance-first: behavior
  test → integration → unit → code → schema-drift check. Never mock the
  datastore."]
- **Guardian tests:** [name the invariant suites protecting load-bearing logic,
  and the rule: change the logic → update its guardian in the same change].
- **Format / lint:** [exact commands; the commit hook and its one-time install].
- **Schema changes:** [how they're made; how drift is caught].
- **Changelog:** [format + when it must be updated; note that release gates on it].
- **Docs:** [where what/why vs. how live; the status-header habit; the
  source-of-truth rule: summaries defer and link, never duplicate].
- **Secrets:** never commit or print secrets. Behavior lives in reviewed
  config; secrets live in the machine-local env file; `[.env.example]` is the
  contract; [scanner] blocks the accident at commit time.
- **Agent-file sync:** this file and [GEMINI.md / siblings] change in the same
  commit.
- **License:** [state it — chosen deliberately, not inherited by default].

## Definition of Done

<!-- What must be true before any change is complete. An agent should
     self-check this list before declaring victory. -->

- [ ] Tests pass at every tier the change touches (`[cmd]`)
- [ ] Lint, format, and types clean (`[cmd]`)
- [ ] Schema-drift check clean, if models changed
- [ ] Docs updated, if behavior or structure changed
- [ ] Changelog entry, if user-facing
- [ ] [Accessibility check, if UI changed]

## Boundaries

<!-- Standing rules about consequence-bearing actions. Adjust to your risk
     tolerance, but have them — an agent without boundaries infers its own. -->

Ask before, never assume: pushing or opening PRs, tagging or releasing,
deploying, destructive data operations, anything touching production, and
adding new dependencies. Never print secrets or env-file contents. On failure:
stop, surface the raw error, and do not auto-recover past it.

[Optional standing grants, e.g.: "Commit freely on feature branches at logical
boundaries; never push without an explicit ask."]

## Gotchas — traps that have cost time

<!-- ⭐ The highest-value section: facts an agent cannot infer from the code
     and will otherwise rediscover the hard way. Add each the day it bites.
     The recurring shapes, with the pattern each example should follow: -->

- **[Tooling trap]:** [a syntax or behavior edge that fails *silently* — e.g.
  "the template-comment syntax is single-line only; a wrapped comment renders
  as page text"].
- **[Environment trap]:** [a false signal — e.g. "inspecting the service
  user's files as yourself returns permission-denied: a false negative, not an
  absence — use the privileged path"].
- **[Version-coupling trap]:** [two pins that must move together — e.g. "the
  commit hook's linter version must match the lockfile's; bump both together
  or local and CI disagree about formatting"].
- **[Parity trap]:** [any place dev and prod genuinely differ, and what that
  difference breaks].

## Maintaining This File

| When… | Update… |
| --- | --- |
| A milestone lands | Current State |
| Something non-obvious costs more than 30 minutes | Gotchas — same day |
| The tree or the commands change | Repository Map / Commands |
| A convention changes | Conventions — and its enforcement hook |
| Any of the above | Sibling agent files, in the same commit |
