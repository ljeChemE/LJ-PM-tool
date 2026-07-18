> Status: [FILL: draft / adopted] | Audience: new contributors and agents
> bootstrapping a checkout | See also: [Testing.md](Testing.md),
> [../README.md](../README.md)

# Getting started

## Prerequisites

Install on the host: [FILL: e.g. "brew install docker docker-compose just"] —
a container runtime, the task runner, and a couple of small CLIs. Nothing
else touches the host; the toolchain itself lives in containers.

## Quick start

```bash
git clone [FILL: repo URL]
cd [FILL: repo directory]
cp .env.example .env
# Generate a local secret — never share this value, never commit it:
openssl rand -hex 16
# Paste the generated value into .env where the placeholder says so, then:
just dev
just health
```

`just health` should report every service up. If it doesn't, see
Troubleshooting below before doing anything else.

## What `just dev` does

Idempotent — safe to re-run at any time, including on an already-running
stack:

1. Materializes local config from `.env` (fails loudly if a required variable
   is missing).
2. Starts services (app + datastore + [FILL: cache, proxy, mail-catcher, …]).
3. Applies the schema (migrations run to the latest version).
4. Seeds realistic development data, if the datastore is empty.
5. Prints the URLs and any local credentials it just created.

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

[FILL: the traps that have actually cost someone time on this project —
port conflicts, stale volumes, a service that needs a second start. Add an
entry the day something bites; a missing entry here means the next person
rediscovers it the hard way.]

## Where to go next

- Running and writing tests: [Testing.md](Testing.md).
- The full documentation map: [../README.md](../README.md).
- Agent-facing conventions and gotchas: `../../CLAUDE.md` at the repository
  root.
