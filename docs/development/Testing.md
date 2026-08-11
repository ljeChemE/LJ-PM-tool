> Status: adopted | Audience: anyone writing or reviewing a
> change | See also: [Getting-Started.md](Getting-Started.md)

# Testing

## The three tiers

```text
tests/unit/          Fast, isolated, no I/O — the fewest of the three tiers
tests/integration/   Real request/response cycles against the real datastore
tests/e2e/           Full stack, driven like a user would drive it
```

The suite is weighted deliberately toward **integration**: a real
request/response cycle against a real datastore catches the most failures
for the least fragility. Unit tests earn their place on logic with enough
branches to matter; e2e tests earn theirs on the workflows a stakeholder
actually walks through.

## Acceptance-first workflow

Outside-in, in this order:

1. Write the acceptance test from the requirement itself. Watch it fail
   honestly — a green test at this step means it isn't testing anything.
2. Write the integration test for the slice underneath.
3. Write unit tests for logic with real edge cases.
4. Write code until everything is green.
5. Run the schema-drift check — models and migrations must still agree.

## Never mock the datastore

Tests run against the real engine, at the production major version — never a
lighter substitute, never an in-memory stand-in. A substitute lets schema
changes lie and engine-specific behavior go untested. Container tooling makes
this cheap; there's no longer a good excuse to skip it.

## Guardian suites

Logic whose silent failure would be expensive — money math, scheduling,
anything feeding a report someone trusts — gets a **named guardian suite**: a
dedicated, edge-case-heavy test module for that one computation.

**Standing rule: change the computation, update its guardian in the same
change.** A crash is cheap to notice; a wrong number is not.

| Suite | What it protects |
| --- | --- |
| [FILL: list your guardian suites here] | [FILL: the computation it guards] |

## Determinism

Freeze time; seed randomness. A test that passes sometimes is a test that
tells you nothing.

## No silent skips

No test is skipped without a reason string linking the issue that will
unskip it. A skip with no reason is a failure with a snooze button.

## Coverage is a ratchet

CI enforces a coverage floor that only ever rises. Nobody chases the number
up for its own sake, and nobody lets it fall — the floor moves in one
direction.

## Accessibility gate

If there is a UI, an accessibility check (axe or equivalent) runs against the
real built stylesheet as a gate, not a suggestion.

## Running the suite

```bash
just test   # all tiers
just e2e    # end-to-end only
```

See `docs/development/Getting-Started.md` for environment setup if either
command fails to find a running stack.
