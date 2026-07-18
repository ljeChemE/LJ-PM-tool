---
description: Hotfix from a GitHub issue — branch, fix, gate, open a PR to main
argument-hint: [issue# | URL | "problem description"]
---

You are running the `/hotfix` skill. Takes a production bug from a GitHub
issue to an open PR on `main`: establish the issue, branch, fix it
surgically, gate it, open the PR. **Writes** — an issue (maybe), a branch,
commits, a PR.

## Argument

`$ARGUMENTS` is one of:

- An **issue reference** (`123`, `#123`, or a URL) — work that issue.
- **Free text** describing the bug — search open issues for a match; if none,
  create one (`gh issue create --label bug --title ... --body ...`).
- **Empty** — ask the user to describe the bug or give an issue number, then
  stop until they answer.

Capture the issue number either way — it drives the branch name and the PR.

## 1. Branch

Refuse if the tree is dirty (`git status --porcelain` non-empty) — that's the
user's call to resolve first. Otherwise:

```bash
git fetch origin main
git switch -c hotfix/[slug-from-issue-title] origin/main
```

## 2. Fix it

Reproduce the bug first. Then make the **smallest change that fixes the root
cause** — a hotfix is surgical, never a refactor. Add or adjust a regression
test that fails before the fix and passes after; if it's genuinely
untestable, say why in the PR body.

## 3. Changelog — required, never deferred

Compute the predicted next patch version (`just version`, bumped patch) and
author a new `## [X.Y.Z] — YYYY-MM-DD` section in `CHANGELOG.md` now, Keep a
Changelog format, under `### Fixed` (or `### Changed` for a behavior change).
`/release` has final say on the version/date if timing slips. Enforce the
diff touched it — do not skip:

```bash
git diff origin/main --name-only | grep -qx CHANGELOG.md \
  || { echo "CHANGELOG.md not updated — required for every hotfix"; exit 1; }
```

## 4. Commit, gate, push, PR

Commit as `fix([scope]): [imperative subject]`, body explaining what broke
and why the fix works, footer `Closes #[issue]`.

Run `just lint`, `just typecheck`, `just test` — require all green before
opening a PR. Stop and print the failing output if any fail; fix, re-commit,
re-run. Don't push through red.

```bash
git push -u origin hotfix/[slug]
gh pr create --base main --title "fix([scope]): [subject]" --body "..."
```

PR body: what broke, what changed, the regression test added, `Closes
#[issue]`.

## 5. Back-merge to `develop` — mandatory, not optional

After the PR merges and the release that ships it has tagged:

```bash
git checkout develop && git pull --ff-only
git merge origin/main -m "chore: back-merge main ([tag] hotfix) into develop"
git push
```

This is the **single sanctioned direct push** in this branch model —
everything else lands via PR. It's sanctioned because the content was
already CI-gated on the hotfix PR and the release; a PR here would gate
nothing new. Skipping it is not optional: an un-back-merged hotfix is a
regression scheduled for the next release, since `develop` would silently
regain the bug.

**On conflict:** resolve favoring `main`'s hotfixed lines. If the conflict is
broad or unclear, stop and report it rather than guessing.
