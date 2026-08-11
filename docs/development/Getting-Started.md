> Status: adopted | Audience: new contributors and agents
> bootstrapping a checkout | See also: [Testing.md](Testing.md),
> [../README.md](../README.md)

# Getting started

## Prerequisites

Install on the host: Docker Desktop (container runtime), `just` (task
runner) — `brew install --cask docker && brew install just` on a Mac.
Nothing else touches the host; the backend's actual toolchain (Python,
FastAPI, Postgres client libs) lives in the `api` container.

## Quick start

```bash
# No GitHub remote yet — this is currently a local-only project (solo, no
# hosting). Replace this with the real clone URL once Pillar VI stands up a
# repo for it.
cd project-seed-kit
just dev
```

The first run creates `.env` from `.env.example` and stops, asking you to
fill in `POSTGRES_PASSWORD`:

```bash
openssl rand -hex 16
# paste the result into .env, then:
just dev
just health
```

`just health` should report `{"status": "ok"}`. If it doesn't, see
Troubleshooting below before doing anything else.

## What `just dev` does

Idempotent — safe to re-run at any time, including on an already-running
stack:

1. Creates `.env` from `.env.example` on first run (and stops — you must fill
   in the generated secret yourself; see Quick start above).
2. Starts services: the FastAPI backend (`api`) and Postgres (`db`), via
   `docker-compose.yml`.
3. Waits for `/health` to report ok, then prints it.

Schema migrations and seed data aren't part of this yet — there's no schema
to migrate until the first feature (the daily to-do list) needs one. This
section will grow a step 3 (migrate) and step 4 (seed) at that point.

## Install the commit hooks

One-time, per clone:

```bash
pre-commit install
```

Without this, `just lint` still catches everything CI catches — but you'll
find out at push time instead of commit time.

## Resetting

```bash
just reset
```

Destructive: drops all local data and rebuilds from scratch. Asks for typed
confirmation before it does anything — the friction is deliberate, not a
bug. Use it whenever local state feels wrong; the environment is disposable
by design, so there's no state worth protecting here.

## Troubleshooting

- **`just: command not found`.** `just` isn't installed yet —
  `brew install just`.
- **`just up`/`just dev` hangs or errors talking to Docker.** Docker Desktop
  is installed but not running. `open -a Docker`, wait for it to finish
  starting, then retry.
- **Port already in use (5432 or 8000).** Something else on your machine is
  already listening there. Change `POSTGRES_PORT`/`API_PORT` in `.env`, or
  stop the other process.

## Where to go next

- Running and writing tests: [Testing.md](Testing.md).
- The full documentation map: [../README.md](../README.md).
- Agent-facing conventions and gotchas: `../../CLAUDE.md` at the repository
  root.
