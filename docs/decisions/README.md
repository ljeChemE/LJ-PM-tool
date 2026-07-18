<!--
This index does not replace inline decision records — it exists only so a
decision can be found without knowing which design doc holds it. Keep the
table below in the same commit as the inline stamp it points to; a decision
recorded here but not there (or vice versa) is a broken link waiting to be
noticed the hard way.
-->

# Decisions index

This project has no separate decision-log format. Decisions are recorded
**inline, where they're made** — in the design doc discussing the tradeoff,
at the exact point of relevance — stamped like this:

```text
(decision YYYY-MM-DD, #issue)
```

When a later decision replaces an earlier one, the new entry says so
explicitly, in place:

```text
(decision YYYY-MM-DD, #issue) This supersedes the 2024-02-01 decision to
[FILL: what changed and why].
```

The stamp and the reasoning live together, in context, so a reader hits the
decision exactly where they'd otherwise ask "wait, why is it built this
way?" This index exists only to make those stamps *discoverable* without
grepping every design doc.

## Rule

Adding an inline decision stamp means adding a row below, in the same commit.
An index row with no matching stamp, or a stamp with no matching row, means
someone skipped half the rule.

## Index

| Date | Decision (one line) | Recorded in | Status |
| --- | --- | --- | --- |
| 2024-01-01 | *(example, delete me)* Adopt trunk-based branching with `develop` as the integration branch | [../../CLAUDE.md](../../CLAUDE.md) | active |
| [FILL: YYYY-MM-DD] | [FILL: one-line decision] | [FILL: path to doc] | [FILL: active / superseded by YYYY-MM-DD] |
