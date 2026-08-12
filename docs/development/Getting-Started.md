> Status: adopted | Audience: new contributors and agents
> bootstrapping a checkout | See also: [Testing.md](Testing.md),
> [../README.md](../README.md)

# Getting started

## Prerequisites

Install on the host: Docker Desktop (container runtime), `just` (task
runner) — `brew install --cask docker && brew install just` on a Mac.
Nothing else touches the host; the actual toolchains (Python/FastAPI in
`api`, Node/React in `web`) live inside their containers.

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

Once healthy, open **http://localhost:5173** in any browser — that's the
actual app (the daily to-do list). `just health` only checks the API.

## What `just dev` does

Idempotent — safe to re-run at any time, including on an already-running
stack:

1. Creates `.env` from `.env.example` on first run (and stops — you must fill
   in the generated secret yourself; see Quick start above).
2. Starts services: the FastAPI backend (`api`), Postgres (`db`), and the
   React frontend (`web`), via `docker-compose.yml`.
3. Applies pending schema migrations (`just migrate`).
4. Waits for `/health` to report ok, then prints it.

Seed data isn't part of this yet — add a step 5 here the day an empty
database on first clone becomes annoying enough to fix.

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
- **Port already in use (5432, 8000, or 5173).** Something else on your
  machine is already listening there. Change `POSTGRES_PORT`/`API_PORT`/
  `WEB_PORT` in `.env`, or stop the other process.

## Where to go next

- Running and writing tests: [Testing.md](Testing.md).
- The full documentation map: [../README.md](../README.md).
- Agent-facing conventions and gotchas: `../../CLAUDE.md` at the repository
  root.
