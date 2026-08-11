# ==============================================================================
# justfile — the project's operational vocabulary (Practices Playbook Pillars
# I and V)
#
# This file is the single source of truth for how anyone — human or agent —
# runs this project. Every runbook, every Claude Code skill under
# .claude/commands/, and every CI job delegates to these verbs instead of
# reimplementing the steps behind them. "How do we do X?" is answered with a
# verb name, not a paragraph.
#
# Fill each recipe body for your stack. Keep the verb NAMES stable — anything
# that calls `just <verb>` (a skill, a workflow file, a teammate's habit)
# breaks the moment a name changes. Add stack-specific recipes freely; do not
# rename or remove one of the twelve below.
#
# NOTE: `just --list` shows the LAST comment line above each recipe as its
# doc string — keep that line a one-line summary; contract details go above.
# ==============================================================================

set shell := ["bash", "-euo", "pipefail", "-c"]

# List every recipe with its doc comment (run with no args).
default:
    @just --list

# CONTRACT: idempotent bootstrap. Safe to re-run on a machine that already has
# a working environment. Sequence: write local config from the example if
# missing → start services → apply schema → seed realistic data → print the
# URLs and credentials for what it just built.
#
# Bootstrap a ready-to-use dev environment (idempotent): env, services, schema, seed.
dev:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Created .env from .env.example — fill in POSTGRES_PASSWORD before continuing:" >&2
        echo "  openssl rand -hex 16" >&2
        exit 1
    fi
    just up
    echo "Waiting for the API to become healthy..." >&2
    for i in $(seq 1 30); do
        if just health >/dev/null 2>&1; then
            just health
            exit 0
        fi
        sleep 1
    done
    echo "API never became healthy — check \`docker compose logs\`." >&2
    exit 1

# CONTRACT: start the already-configured services in the background without
# touching schema or seed data. The lighter sibling of `dev` — use after the
# first `dev` bootstrap when you just need the stack running again.
#
# Start the configured services in the background (no schema/seed steps).
up:
    docker compose up -d --build

# CONTRACT: stop the services started by `up`/`dev` without destroying their
# data volumes. Safe, non-destructive — the inverse of `up`, not of `reset`.
#
# Stop services, preserving data volumes.
down:
    docker compose down

# CONTRACT: destructive. Tears down the environment — services, volumes,
# local state — and rebuilds it from scratch via `dev`. Must ask for a typed
# confirmation before doing anything irreversible (Pillar VIII: friction is a
# design tool). The confirmation logic below is real, wired, and a worked
# example for every other destructive recipe you add to this file.
#
# DESTRUCTIVE: tear down and rebuild from scratch (asks for typed confirmation).
reset:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "This will permanently destroy local services, volumes, and data." >&2
    read -p "Type 'yes' to continue: " confirmation
    if [ "$confirmation" != "yes" ]; then
        echo "Aborted — no changes made." >&2
        exit 1
    fi
    docker compose down --volumes
    just dev

# CONTRACT: run the full automated test suite — every tier (unit,
# integration, e2e) unless your stack's test runner supports narrowing to one
# tier as an argument. Deterministic: no flaky retries, no skipped test
# without a reason string (Pillar IV).
#
# Run the automated test suite (all tiers).
test:
    @echo "not implemented — FILL: run unit + integration + e2e tiers" >&2; exit 1

# CONTRACT: run the end-to-end tier only, against a running stack, driving
# the real UI. One scenario per critical stakeholder workflow.
#
# Run the end-to-end tier against a running stack.
e2e:
    @echo "not implemented — FILL: run e2e tier against a running stack" >&2; exit 1

# CONTRACT: static analysis only. Reports problems; never mutates files. A
# non-zero exit means real findings, not a formatting nit `fmt` would fix.
#
# Static analysis, check-only — never mutates files.
lint:
    @echo "not implemented — FILL: run the linter in check-only mode" >&2; exit 1

# CONTRACT: auto-format the codebase in place. Idempotent — running it twice
# in a row produces no further diff. Pairs with the pre-commit hook so local
# and CI never disagree about what "formatted" means.
#
# Auto-format the codebase in place (idempotent).
fmt:
    @echo "not implemented — FILL: run the formatter, writing changes" >&2; exit 1

# CONTRACT: static type checking only. Read-only, like `lint` — reports, does
# not fix.
#
# Static type checking, check-only.
typecheck:
    @echo "not implemented — FILL: run the type checker in check-only mode" >&2; exit 1

# CONTRACT: apply any pending schema migrations to the datastore this
# environment points at. Must be safe to run against a datastore that is
# already up to date (no-op in that case).
#
# Apply pending schema migrations (no-op when already up to date).
migrate:
    @echo "not implemented — FILL: apply pending schema migrations" >&2; exit 1

# CONTRACT: hit the running app's health endpoint and pretty-print the
# response (status, version, dependency checks). Read-only; exits non-zero if
# the endpoint is unreachable or reports unhealthy.
#
# Hit the health endpoint and pretty-print the response.
health:
    #!/usr/bin/env bash
    set -euo pipefail
    source .env
    curl -sf "http://localhost:${API_PORT:-8000}/health" | jq .

# CONTRACT: print the current SemVer, computed from git history (tags,
# branch, distance) — never hand-edited. This is the number every release
# and every build artifact stamps itself with.
#
# Print the SemVer computed from git history.
version:
    @echo "not implemented — FILL: compute SemVer from git history" >&2; exit 1
