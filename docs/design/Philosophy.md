> Status: adopted | Audience: anyone designing a feature or a
> stakeholder doc | See also: [Stakeholders/_TEMPLATE.md](Stakeholders/_TEMPLATE.md)

<!--
Write this before the second stakeholder conversation, not after the tenth.
Every stakeholder doc and every non-trivial feature decision should be
defensible against the principle stated here. If a decision can't be
defended against it, either the decision or the principle is wrong — that
tension is the point of writing this down.
-->

# Philosophy

## The guiding principle

> Never lose a task to friction.

Capturing a task, or updating one, must never cost more than a couple of
seconds and one deliberate action. The daily list and the weekly dashboard
both exist to *look at* work that's already been captured cheaply — neither
view is allowed to make capture itself slower or heavier to justify its own
existence.

Every section below, every stakeholder document, and every feature that gets
built should trace back to this sentence. When a decision can't be defended
against it, that's a signal to revisit the decision, not to skip the check.

## The stakeholder contract

Every role in this system — every document under `Stakeholders/` — fills the
same three-part contract:

1. **Domain of awareness** — what this role must stay aware of to do their
   part. Not everything in the system; only what bears on their decisions.
2. **Data this role keeps current** — what this role is the source of truth
   for. If nobody keeps a field current, question why it exists.
3. **Value this role receives** — what this role gets back for the awareness
   and upkeep asked of them. An unbalanced contract is a design defect, not a
   tradeoff to shrug off.

## The design failure test

> If capturing or updating a task ever takes more than a couple of seconds,
> or more than one deliberate action, the design has failed.

Apply this test whenever a feature adds an obligation (a field to fill, a
step to complete, a notification to read) to any role. A feature that serves
no stakeholder's contract — that asks without giving, or gives to nobody in
particular — is questioned by default, not built by default.

## Stakeholder summary matrix

<!-- One row per role once its Stakeholders/ doc exists. Keep this in sync;
     it's a summary, and a summary that drifts from the source docs is worse
     than no summary — link to the full doc rather than duplicate its
     content here. -->

| Role | Expected awareness | Expected action | Not expected to |
| --- | --- | --- | --- |
| [Self](Stakeholders/Self.md) | Today's tasks, anything slipping, the week's overall shape | Capture/update tasks in a couple of seconds | Categorize, tag, or estimate beyond day + status |
