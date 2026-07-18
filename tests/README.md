<!--
Quick orientation for this directory. The full testing philosophy —
acceptance-first workflow, guardian suites, determinism, the coverage
ratchet — lives in docs/development/Testing.md. This file just orients you
inside tests/ itself.
-->

# Tests

Three tiers, weighted deliberately toward the middle one:

- **`unit/`** — fast, pure logic. No datastore, no network, no filesystem.
  Cheap enough to run on every keystroke.
- **`integration/`** — real request/response cycles against the **real**
  datastore engine (same engine, same major version as production). This is
  where most of the suite lives on purpose: integration tests catch the most
  failures for the least fragility.
- **`e2e/`** — drives the real UI. One test per critical stakeholder
  workflow, not one per page or per click.

See [`docs/development/Testing.md`](../docs/development/Testing.md) for the
full philosophy: acceptance-first (behavior test before code), named guardian
suites for load-bearing computations, determinism (frozen time, seeded
randomness), and the coverage ratchet (a floor that only ever rises).

## Two rules, absolute, no exceptions

- **Never mock the datastore.** A lighter substitute lets schema changes and
  engine-specific behavior lie. Container tooling makes the real thing cheap;
  there's no longer a good excuse.
- **No skipped test without a reason string linking an issue.** A skip with
  no paper trail is a silent, permanent hole in the suite.
