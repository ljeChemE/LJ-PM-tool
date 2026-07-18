# The Practices Playbook

## An idealized operating manual for software projects

> This document describes a project that does not exist — the *idealized* form of
> one that does. It began as a full audit of a production system's practices;
> this version generalizes every practice to its principle (tools appear only in
> parentheses, as examples) and closes every gap the audit found, folding the
> fixes in as if they had always been there. Read it as a portrait of the
> repository you intend to build.
>
> Each pillar paints the ideal in the present tense, then gives **Getting
> there** (the path) and **It's working when** (observable signals — an ideal
> you can't verify is a mood, not a target). A maturity rubric and an adoption
> order close the document. Companion: the **CLAUDE.md template at the repo
> root**, a drop-in agent-context file that implements Pillar V.

---

## The prime directive

**Make the right thing the easy thing — then let a machine hold the line.**

Everything below is an instance of one idea: good intentions decay under
deadline pressure; automation and incentives don't. Three corollaries recur in
every pillar:

1. **If a rule matters, it is an exit code.** A convention that lives only in
   prose is a request. Policy that matters is a hook, a gate, or a script that
   refuses to proceed.
2. **If a document can drift, delete it or generate it.** Every duplicated fact
   is a future lie. Each document names the single source of truth for what it
   describes and defers to it.
3. **Friction is a design tool.** The cost of an action tracks its consequence,
   not its convenience: dangerous operations demand typed confirmation, safe
   ones announce their safety, and irreversible ones are the hardest of all to
   trigger by accident.

---

## Pillar I — Environment: reproducible, disposable, parallel

A new contributor clones the repository, runs one command, and is working
inside five minutes. That command is idempotent — safe to re-run — and does
everything: creates local configuration from the committed example, starts the
services, applies the schema, seeds realistic data, and prints the URLs and
credentials for what it just built. The host machine needs almost nothing (a
container runtime and two or three small CLIs); the toolchain lives in
containers, so nothing is installed into, or depends on, anyone's system
environment.

Development runs the same infrastructure as production — the same datastore at
the same major version, the same cache, the same proxy pattern — because every
substitution ("it's just dev") is a place where testing diverges from reality.
Outbound side effects (email, webhooks, third-party calls) are captured by
local fakes with inspectable UIs, never sent for real.

The environment is disposable: one confirmed command tears it down and rebuilds
it from scratch, so nobody protects a fragile local state or fears
experimentation. And it is parallel: multiple checkouts run side by side, each
deriving an isolated namespace and port set deterministically from its path, so
working on two branches at once costs nothing.

**Getting there.**

- Put a task runner (`just`, `make`, `task`, npm scripts) in front of
  everything, one verb per operation: `dev`, `test`, `lint`, `migrate`, `reset`.
- Containerize the app and its services; keep host prerequisites to a one-line
  install.
- Build the seed early — an empty app teaches nothing.
- Make `reset` real, destructive, and confirmed; make `dev` idempotent.
- Derive per-checkout isolation (project name + port offset) from the checkout
  path.

**It's working when** a new hire ships a reviewed change on day one; "works on
my machine" has left the vocabulary; people reset their environments casually,
without dread.

---

## Pillar II — Configuration: behavior is reviewed, secrets are local, both are guarded

Behavior lives in committed, code-reviewed configuration — settings profiles
that differ between environments in ways anyone can diff. Secrets, and only
secrets, live in a machine-local, ignored env file. The split is absolute, and
it has a consequence worth stating plainly: a developer's convenience toggle
*cannot* reach a deployment, because every behavioral difference between
environments is a reviewed line in the repository, not a value someone once
exported.

A committed example file is the contract: it lists every variable the system
needs, documented, with safe placeholders. Local secrets are generated, never
shared (`openssl rand` or equivalent), and no tool or script ever prints one.
The discipline is mechanical, not aspirational: a secret scanner (gitleaks,
detect-secrets) runs at commit time *and* in CI, so the ignored-file convention
is backed by a gate that blocks the accident the convention alone can't.

**Getting there.**

- Commit the example env file the day the first variable appears; keep it in
  lockstep with reality.
- Split config into per-environment profiles that are reviewed like any code.
- Add the secret scanner as a commit hook and a CI job in the first week — an
  hour of work that removes a whole category of incident.

**It's working when** "how do dev and prod differ?" is answered by diffing two
committed files, and no secret has ever survived long enough to be pushed.

---

## Pillar III — Documentation: a designed system, not a pile

Documentation is split by the question it answers. One tree holds the *what and
why* — the domain model, the lifecycle, the roles, the decisions — written
implementation-agnostically, in the vocabulary of the problem rather than the
framework. A second tree holds the *how* — setup, testing, daily workflow —
which is allowed to be as tool-specific as it needs to be. The payoff is
portability of thought: when the implementation changes, the design tree
doesn't. (*Field evidence: the audited system's entire product design survived
a full re-platform untouched, because none of it was written in terms of the
abandoned platform.*)

Every document opens with a small header — status, audience, where to go next —
and declares what it is **not** authoritative for, linking to the true source.
Content that would need manual synchronization with code is deleted rather than
trusted; a summary that can drift is a lie on a delay. Aspiration is separated
from reality *inline, at the point of relevance*: a "planned, not built" marker
sits exactly where a reader would otherwise assume "built."

Requirements are anchored to people. A short philosophy document states the
principle every decision must be defensible against, with an explicit failure
test. Each stakeholder role gets a document with the same three-part contract:
what this role must stay aware of, what data it keeps current, and what value
it receives in return — and a feature that serves no stakeholder contract is
questioned by default.

Plans are phased, and every phase has an exit criterion phrased as an
observable capability, never as "code complete." Shipped phases are cut from
the plan (history keeps them); the plan holds only forward work plus an
append-only, dated progress log — one line per completion, carrying the date,
the commit, and the numbers that matter. Decisions are recorded where they're
made — an inline stamp of date and issue reference, with supersession noted
when a new decision replaces an old one — and a tiny decisions index makes them
discoverable without ceremony. Finished one-time plans move to an archive whose
manifest opens loudly: *nothing here describes current state* — kept for the
rationale, stripped of authority.

A documentation index gives newcomers a reading order: one path to understand
the product, another to understand the engineering.

**Getting there.**

- Create `design/` and `development/` trees on day one, even nearly empty.
- Add the status/audience header to each doc as you write it, not retroactively.
- Start the progress log with the first shipped slice; write the philosophy doc
  before the second stakeholder conversation, not after the tenth.
- When you catch a doc duplicating a source of truth, delete the copy and link.

**It's working when** a newcomer self-orients without a tour; the rationale for
any decision can be reconstructed from the repository alone; a re-platform
would orphan none of your design.

---

## Pillar IV — Testing: outside-in, on real infrastructure, with named guardians

The suite has three tiers — unit, integration, end-to-end — weighted
deliberately toward integration: real request/response cycles against a real
datastore catch the most failures for the least fragility. New behavior is
built outside-in: the acceptance test comes first, written from the requirement
it implements and failing honestly; then the integration test; then units; then
code until green; then a schema-drift check proving the models and the
migrations still agree.

The datastore in tests is the production datastore — same engine, same major
version. Never a mock, never a lighter substitute, because substitutes let
schema changes lie and engine-specific behavior go untested. Container tooling
makes this cheap; there is no longer a good excuse.

The logic whose silent failure would be expensive — money math, scheduling,
anything feeding a report someone trusts — is protected by **named guardian
suites**: dedicated, edge-case-heavy test modules, one per load-bearing
computation, under a standing rule recorded where every contributor and agent
reads it: *change the computation → update its guardian in the same change.* A
wrong crash is cheap; a wrong number is not.

Tests are deterministic — time is frozen, randomness is seeded — and honest: no
test is skipped without a reason string linking the issue that will unskip it.
Coverage is a ratchet, not a trophy: CI enforces a floor that only ever rises;
nobody chases the number, and nobody lets it fall. If there is a UI,
accessibility checks (axe or equivalent) run against the real built stylesheet
as a gate, not a suggestion.

**Getting there.**

- Stand up the three-tier layout and the real datastore in CI before the first
  feature, while it's cheap.
- Write your first acceptance test from a requirement doc, watch it fail, and
  work inward.
- The day you ship your first load-bearing calculation, give it a guardian
  suite and write the standing rule down.
- Set the coverage floor at whatever today's number is; raise it as it rises.

**It's working when** a failing business rule fails a *named* test whose name
says what broke; releases need no manual QA sweep; coverage has never gone
down.

---

## Pillar V — Automation and agents: one vocabulary, dual-runnable, safety-classified

Every recurring operation is a command with a name. The task runner is the
project's operational vocabulary, and everything else — CI, runbooks, AI-agent
commands — is a thin wrapper over it. Runbooks and agent skills stay under a
screenful and *delegate*: the logic lives in shared scripts, so a human at a
terminal and an agent in a session run the exact same code, and there is no
drift between what the runbook says and what actually happens. Nothing is
agent-only; automation that can't be run by hand can't be debugged by hand.

Every operation is classified by blast radius. Read-only commands declare
themselves read-only in their first line and refuse to fix anything.
Destructive commands demand a typed confirmation. When automation must
auto-confirm a downstream prompt, it does so only after obtaining its own
explicit consent — and annotates why, so the consent chain is auditable. All of
it shares one failure stance: stop at the first failure, surface the raw error,
never auto-recover past it, never print a secret.

At the repository root sits the agent context file (CLAUDE.md, with
synchronized siblings for other tools): the map, the design decisions and
non-goals, the live status of the work, the conventions, the boundaries — and
above all the **gotchas**: every trap that has ever cost someone an afternoon,
recorded the day it bit, because those non-inferable facts are the most
valuable lines in the repository. The file is kept ruthlessly current; a stale
context file is worse than none, because agents act on it with confidence.

**Getting there.**

- Adopt the CLAUDE.md template (at the repo root) on day one — a skeleton
  beats nothing.
- Write your first three runbook wrappers for the operations you already
  repeat by hand.
- Add the safety classification the first time a command deletes data.
- Make "update the context file" part of shipping, with the same-day rule for
  gotchas.

**It's working when** "how do we do X?" is answered with a command name; a
human run and an agent run are indistinguishable in effect; the gotcha list
grows within a day of each new trap — and then stops growing, because the
traps are fenced.

---

## Pillar VI — Enforcement: policy is code

Two layers hold the line. At commit time, hooks run the formatter, the linter,
the schema-drift check, and the secret scanner — cheap, fast, local. Hook
versions are pinned to the same versions the lockfile carries and bumped
together, so local and CI can never disagree about what "formatted" means. In
CI, every convention that matters has a check: models that drift from
migrations fail; a release without a changelog entry fails (a `grep`-cheap
check, absolutely binding); deployment artifacts — compose files, workflow
definitions — are parsed and linted before they can break a deployment.

CI is tiered by risk and cost. The fast tier — lint, types, drift, unit,
integration — runs on every pull request and finishes in minutes. The full
gate — end-to-end suites, accessibility, container vulnerability scanning,
deep review — runs only where it pays: on pull requests into the release
branch. CI triggers on pull requests, not pushes, so no minutes are spent
twice; every job carries least-privilege permissions; quota (cache, minutes)
is managed proactively rather than discovered at the limit. Every non-obvious
cost decision is commented inline where it's made, so the next maintainer
doesn't helpfully undo it.

And the branch model is mechanical, not conventional: branch protection makes
the trunk unable to receive an unreviewed push — even from an admin in a
hurry, even from you. The rules a team keeps under pressure are exactly the
rules a machine keeps for them.

**Getting there.**

- Hooks on day one; pin them to the lockfile the day both exist.
- Tier the pipeline the day CI first feels slow — don't let the full gate
  become the reason people batch changes.
- Turn on branch protection the moment your platform plan allows it. It is the
  single highest-leverage switch in this document.
- Whenever you hear "we always…", write the one-line check for it.

**It's working when** a red gate names its reason; nothing reaches the trunk
unreviewed; CI cost stays flat while the team grows.

---

## Pillar VII — Releases: computed, honest, guided

The version number is computed from git history — tags, branch, distance —
never hand-edited. Integration builds carry a pre-release label that climbs per
commit; release builds are the clean tag. The computed version is stamped into
every build artifact and surfaced at runtime through a health endpoint, so
"what exactly is running in production?" is one request, never an
investigation.

The changelog is a standard, human-readable format (Keep a Changelog), updated
as work merges — and enforced, not requested: the release path fails,
mechanically, if the changelog didn't change. The release itself is a guided
flow that refuses on any red precondition — wrong branch, dirty tree, out of
sync with the remote, any local gate failing — then states the exact tag it is
about to create, requires confirmation, tags, pushes, and watches the pipeline
through to green. On failure it does not silently clean up; it reports what
failed and how to retry deliberately.

Hotfixes have their own guided path: branch from production, make the smallest
root-cause fix plus the regression test that proves it, pass the same gates as
any release — then back-merge into the integration branch, mandatorily, because
an un-back-merged hotfix is a regression scheduled for the next release. The
merge strategy (merge commits vs. squash) is chosen deliberately to serve the
versioning tool, and the choice is written down.

Dependencies stay current on two tracks: automated update PRs (Dependabot,
Renovate) provide the security floor, and a judgment pass — a read-only report
of what's outdated, then an upgrade command that never commits — handles the
rest. The upgrade tooling has one deliberate manner: on a build failure it
rolls the lockfile back, but on a *test* failure it leaves the diff in place —
the human must see what broke.

**Getting there.**

- Adopt a history-derived version tool and a changelog file in the first week;
  wire the changelog gate the first time someone forgets it.
- Script the release preflight as refuse-on-red before the third release, while
  the manual steps are still fresh enough to transcribe.
- Turn on automated dependency PRs for security updates immediately; add the
  judgment-pass tooling when the noise warrants it.

**It's working when** releases are boring; "what version is prod?" takes one
request; a hotfix has never silently reverted.

---

## Pillar VIII — Data stewardship and continuity

Sensitive data moves with deliberate friction. There is no convenience
automation for pulling production data onto a laptop — that copy is a manual,
conscious act, and the *absence* of a script is the design. Every operation
that destroys or exports data requires a typed confirmation of exactly what is
about to happen.

When shareable data is needed — demos, training, development against realistic
shapes — an anonymization pass produces it, held to a higher standard than most
application code: **deterministic** (one real identity maps to one fake
identity everywhere, so the data stays referentially coherent),
**transactional and self-verifying** (the entire scrub runs inside one
transaction that rolls back if a final sweep finds any real value left — it
fails closed), and **honest** (its known coverage gaps are written down next to
the code, so the next field added to the schema gets added to the scrub).

Backups run on a schedule, and — the part most projects skip — they are
*proven*: restore drills happen on a calendar, performed by the second
operator, because a backup nobody has restored is a hypothesis, and a procedure
only one person can perform is a single point of failure with a salary. Every
operational path — deploy, restore, rotate, revoke — has at least two people
who have actually done it. The system is observable from day one: structured
logs, basic metrics, and the version-bearing health endpoint, so the first
production incident is debugged with evidence rather than folklore.

**Getting there.**

- Add the typed-confirmation pattern to your first destructive command and
  never write one without it again.
- Build the anonymizer the first time someone asks for a demo dataset — with
  the fail-closed sweep from the start, because retrofitting verification into
  a scrub is how leaks happen.
- Schedule the first restore drill within a month of the first backup, and put
  a second name on it.

**It's working when** the demo dataset can be handed to anyone without a second
thought; you know your restore time because you've measured it; the project
runs unbothered through any one person's vacation.

---

## The maturity rubric

Rate yourself per pillar; the gold column is this document.

| Pillar | Baseline | Solid | Idealized |
| --- | --- | --- | --- |
| **I. Environment** | README steps that work | One-command bootstrap + confirmed reset | + prod-parity services, seeded data, parallel checkouts |
| **II. Config & secrets** | Example env file committed | Behavior in reviewed profiles; secrets local only | + secret scanner at commit and in CI |
| **III. Documentation** | README + getting-started | What/why vs. how trees; status headers; index | + philosophy & stakeholder contracts, progress log, decision stamps + index, archive discipline |
| **IV. Testing** | Unit tests in CI | Integration on the real datastore; deterministic; no unexplained skips | + acceptance-first, guardian suites, coverage ratchet, a11y gate |
| **V. Automation & agents** | Task-runner verbs | Agent context file; runbooks delegate to shared scripts | + safety taxonomy, vendor-file sync, same-day gotcha discipline |
| **VI. Enforcement** | Format/lint commit hook | Tiered PR-only CI; least privilege; drift gates | + branch protection, changelog gate, hook/lockfile pinning, cost hygiene |
| **VII. Releases** | Manual tags + notes | Computed version; changelog policy | + runtime version endpoint, refuse-on-red release & hotfix flows, dependency automation |
| **VIII. Data & continuity** | Scheduled backups | Typed confirmations; PII friction; structured logs | + self-verifying anonymization, restore drills by a second operator |

---

## The adoption path

Not all at once. This order front-loads leverage:

**Day one — an afternoon.**

1. Task runner with `dev` / `test` / `lint` / `reset` verbs, even thin ones. *(I)*
2. `.env.example`, ignored `.env`, and the secret-scanner hook. *(II)*
3. Formatter + linter in a commit hook. *(VI)*
4. The agent context file from the **CLAUDE.md template** — a skeleton beats nothing. *(V)*
5. Choose a license deliberately — don't inherit one by default.

**Week one.**

1. Integration tests against the real datastore, in CI, PR-triggered, least
   privilege. *(IV, VI)*
2. Branch protection on the trunk. *(VI)*
3. Changelog + history-computed versioning. *(VII)*
4. `docs/design/` + `docs/development/` + the index. *(III)*

**Month one.**

1. Acceptance-first workflow; the seed; the disposable reset. *(I, IV)*
2. Philosophy + stakeholder contracts; the progress log; decision stamps. *(III)*
3. Guided release flow with refuse-on-red preflights. *(VII)*
4. Automated dependency PRs. *(VII)*

**As it matures.**

1. Guardian suites, the day you first ship load-bearing math. *(IV)*
2. Runbooks as dual-runnable wrappers; the safety taxonomy. *(V)*
3. The full-gate CI tier (e2e, accessibility, vulnerability scan) at the
   release boundary. *(VI)*
4. Self-verifying anonymization, the first time someone asks for a demo
   dataset. *(VIII)*
5. Restore drills, a second operator, observability. *(VIII)*

---

## The test of the whole system

Put the project under deadline pressure and watch what happens. In the
idealized project, nothing degrades: the gates still refuse, the documents
still tell the truth, the dangerous commands still ask, and the shortcut isn't
available to take. That is the point of building it this way — not ceremony,
but quality that survives pressure because it was never optional to begin
with.
