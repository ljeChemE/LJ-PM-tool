<!--
This is the KIT's own README — it explains the kit, not your project. Once
you've worked the Day-one checklist below, replace this file with your actual
project README. (Keep this file around in git history; you won't need it
again, but it costs nothing to keep.)
-->

# Project seed kit

A stack-agnostic starting point for a new software project. It implements the
practices in [`docs/Practices-Playbook.md`](docs/Practices-Playbook.md) as
files, not just advice, so a new repository begins with the scaffolding that
usually gets bolted on — badly, under pressure — six months in.

## How to use it

1. Create a new repository from this template (or copy this tree into an
   empty repository if your platform has no template feature).
2. Run `ops/bootstrap-repo.sh` to apply the platform settings this kit assumes
   (branch protection, required reviewers, merge strategy) — see the script
   for what it changes and what it needs from you first.
3. Work the **Day one checklist** below. It is the fast path through
   `docs/Practices-Playbook.md`'s adoption order.
4. Replace this file with your project's real README. Nothing here describes
   your project — it describes the kit.

## The three-tier model

Every file in this kit falls into one of three tiers:

- **Tier 1 — ready.** Works verbatim, no stack decision required
  (`.gitignore`, `CHANGELOG.md` skeleton, the `cache-cleanup.yml` workflow,
  the real `github-actions` entry in `dependabot.yml`). Commit as-is.
- **Tier 2 — shapes.** Structurally complete but marked with
  `[FILL: description]` where a stack decision belongs — a task-runner verb,
  a CI step, a linter command. The shape encodes the practice; you supply the
  tool.
- **Tier 3 — platform settings.** Not a file at all: settings applied to the
  hosting platform (branch protection, required status checks, merge
  strategy) by `ops/bootstrap-repo.sh`. These can't live in the repository
  because they govern how the repository is written to.

**Deliberately absent:** a `LICENSE` file, seed data, guardian test suites,
philosophy content, and a gotchas list. Each of these must be *decided* or
*earned* by the project it belongs to — a starter kit that pre-fills them
would violate its own rule that policy should be a real decision, not an
inherited default.

## File inventory

| File | Tier | Pillar | Status |
| --- | --- | --- | --- |
| `README.md` | — | III | ready (replace after Day one) |
| `CLAUDE.md` | 2 | V | fill-in (ships as the agent-context template) |
| `CHANGELOG.md` | 1 | VII | ready |
| `CONTRIBUTING.md` | 1 | III, VI | ready |
| `justfile` | 2 | I | fill-in (verb shapes) |
| `.env.example` | 2 | II | fill-in |
| `.gitignore` | 1 | II | ready |
| `.pre-commit-config.yaml` | 2 | II, VI | fill-in (gitleaks real; linter/formatter/drift are placeholders) |
| `GitVersion.yml` | 2 | VII | fill-in (optional) |
| `docs/README.md` | 1 | III | ready |
| `docs/Practices-Playbook.md` | 1 | III | ready |
| `docs/Implementation-Plan.md` | 2 | III | fill-in |
| `docs/design/Philosophy.md` | 2 | III | fill-in |
| `docs/design/Stakeholders/_TEMPLATE.md` | 2 | III | fill-in |
| `docs/decisions/README.md` | 1 | III | ready |
| `docs/archive/README.md` | 1 | III | ready |
| `docs/development/Getting-Started.md` | 2 | I, III | fill-in |
| `docs/development/Testing.md` | 2 | III, IV | fill-in |
| `.github/PULL_REQUEST_TEMPLATE.md` | 1 | VI | ready |
| `.github/CODEOWNERS` | 2 | VI | fill-in (commented stub) |
| `.github/dependabot.yml` | 1 | VII | ready (github-actions); fill-in (package ecosystem) |
| `.github/workflows/ci.yml` | 2 | VI | fill-in (tiered shape) |
| `.github/workflows/release.yml` | 2 | VII | fill-in (shape) |
| `.github/workflows/cache-cleanup.yml` | 1 | VI | ready |
| `.claude/commands/doctor.md` | 2 | V | fill-in |
| `.claude/commands/dev-reset.md` | 2 | I, V | fill-in |
| `.claude/commands/release.md` | 2 | V, VII | fill-in |
| `.claude/commands/hotfix.md` | 2 | V, VII | fill-in |
| `.claude/commands/deps-check.md` | 2 | V, VII | fill-in |
| `.claude/commands/deps-update.md` | 2 | V, VII | fill-in |
| `tests/README.md` | 1 | IV | ready |
| `tests/unit/`, `tests/integration/`, `tests/e2e/` | 2 | IV | fill-in (empty until first test) |
| `ops/bootstrap-repo.sh` | 1 | VI | ready (fill required status checks once CI job names exist) |

## Day one checklist

Straight from the Playbook's adoption path — an afternoon, not a sprint:

1. Pick a license deliberately. Don't inherit one by default.
2. Fill the `justfile` verbs (`dev`, `up`, `down`, `reset`, `test`, `e2e`,
   `lint`, `fmt`, `typecheck`, `migrate`, `health`, `version`) for your stack.
3. Fill the linter and formatter hooks in `.pre-commit-config.yaml`; leave
   gitleaks as-is.
4. Fill the CI steps in `.github/workflows/ci.yml` so the fast tier runs your
   real lint/test/typecheck commands.
5. Fill in `CLAUDE.md` — it ships as the agent-context template; replace every
   `[PLACEHOLDER]` and delete the guidance comments as you go.
6. Commit. Run `ops/bootstrap-repo.sh` if you haven't already.

## Why any of this

Every file here is an instance of a pillar in
[`docs/Practices-Playbook.md`](docs/Practices-Playbook.md). When a convention
in this kit looks arbitrary, that document is the rationale — read it before
changing the shape of anything.
