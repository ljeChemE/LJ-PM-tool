---
description: Nuclear dev reset — drop local services/volumes, rebuild, reseed
---

You are running the `/dev-reset` skill. **DESTRUCTIVE.** This permanently
deletes local services, volumes, and any data they hold. There is no undo.

## 1. Explain, then confirm

Tell the user plainly what is about to be lost: all local database state, any
local service data, anything not committed to git. Then ask verbatim:

> This will destroy your local environment and rebuild it from scratch. All
> local data will be lost. Continue? (yes/no)

Wait for an explicit `yes`. Anything else — abort and report "No changes
made."

## 2. Reset

Run `just reset`.

`just reset` itself prompts for a typed `yes` before it touches anything —
that is the recipe's own last line of defense for a human running it
directly at a terminal. You already obtained that same consent in step 1, so
auto-confirm the recipe's prompt rather than asking the user twice:

```bash
yes | just reset
```

Annotate this in your output: *"Auto-confirming `just reset`'s internal
prompt — consent was already obtained above; this is not a second,
independent authorization."* This is the auditable consent chain the
Playbook requires (Pillar V) — one real human confirmation, not a
rubber-stamped second one.

If `just reset` exits non-zero, stop and surface the raw error. Do not retry,
do not fall back to a manual teardown.

## 3. Rebuild

Run `just dev`. This is the project's idempotent bootstrap — it should bring
services up, apply schema, seed data, and print the URLs and credentials for
what it built.

## On success

Report the URLs/credentials `just dev` printed. If `just health` is
available, run it once as a smoke test and report the result.

## On failure at any step

Stop immediately, print the raw error, and do not attempt to auto-recover.
Report exactly which step failed.
