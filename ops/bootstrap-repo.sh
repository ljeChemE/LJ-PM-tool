#!/usr/bin/env bash
#
# bootstrap-repo.sh — Tier-3 platform settings (Practices Playbook Pillar VI).
#
# Some conventions this kit assumes can't live in a file the repository
# tracks, because they govern how the repository can be written to, not what
# it contains: which branch is the default, whether the trunk can take an
# unreviewed push, whether a squash merge is even offered as an option. This
# script applies those settings through the GitHub API. Branch protection in
# particular is, in the Playbook's own words, "the single highest-leverage
# switch" available — it is what makes every other convention in this kit
# (PR-only changes, merge-commit history for versioning, required checks)
# mechanically true instead of merely agreed-upon.
#
# Run this once, right after creating the repository from this template.
# Re-running it later is safe (see IDEMPOTENCY below) — e.g. after adding
# your first CI run and filling in REQUIRED_STATUS_CHECKS.
#
# Usage:
#   ops/bootstrap-repo.sh                 # repo = current directory's remote
#   ops/bootstrap-repo.sh owner/repo       # repo = explicit owner/repo
#
# IDEMPOTENCY: every mutation below is safe to re-run. Creating `develop` is
# skipped if it already exists; every other call is a PUT/PATCH of the
# desired end state, not an increment, so applying it twice yields the same
# result as applying it once.
#
# FAILURE STANCE: a 403 from a single API call (a feature your plan doesn't
# include, e.g. secret-scanning push protection on some private-repo plans)
# is reported as a warning and does not stop the rest of the script — one
# unavailable setting shouldn't cost you every setting after it. Anything
# else (bad auth, repo not found, malformed input) stops the script
# immediately, per this kit's standing rule: stop at the first real failure,
# surface the raw error, never auto-recover past it.

set -euo pipefail

# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: the GitHub CLI ('gh') is required and was not found on PATH." >&2
  echo "       Install it: https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: gh is not authenticated. Run 'gh auth login' first." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Resolve the target repository
# ---------------------------------------------------------------------------

if [[ $# -ge 1 ]]; then
  REPO="$1"
else
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
fi

if [[ ! "${REPO}" =~ ^[^/[:space:]]+/[^/[:space:]]+$ ]]; then
  echo "ERROR: '${REPO}' doesn't look like an owner/repo (e.g. my-org/my-app)." >&2
  exit 1
fi

MAIN_BRANCH="main"
DEVELOP_BRANCH="develop"

# ---------------------------------------------------------------------------
# FILL: required status checks.
#
# Add your fast-tier job names here once CI has run at least once on this
# repo and you can see the exact check names GitHub reports (they're each
# job's `name:` as shown in the PR checks list, matching this kit's
# .github/workflows/ci.yml fast tier) — e.g.:
#
#   REQUIRED_STATUS_CHECKS=(lint typecheck schema-drift unit-tests integration-tests)
#
# Left empty, branch protection below still requires a PR and a review, but
# does not yet require any specific check to pass — fill this in as soon as
# CI has run once; an unreviewed change is still blockable, but a red CI run
# should be too.
# ---------------------------------------------------------------------------
REQUIRED_STATUS_CHECKS=()

# ---------------------------------------------------------------------------
# Summary — announce every change before making any of them.
# ---------------------------------------------------------------------------

echo "This will apply the following settings to ${REPO}:"
echo
echo "  1. Ensure '${DEVELOP_BRANCH}' exists (branched from '${MAIN_BRANCH}' if missing)"
echo "     and set it as the repository's default branch."
echo "  2. Protect '${MAIN_BRANCH}' and '${DEVELOP_BRANCH}':"
echo "       - require a pull request with >=1 approving review"
echo "       - dismiss stale approvals on new commits"
echo "       - block force pushes and branch deletion"
if [[ ${#REQUIRED_STATUS_CHECKS[@]} -eq 0 ]]; then
  echo "       - required status checks: NONE YET (REQUIRED_STATUS_CHECKS is empty — fill it in)"
else
  echo "       - required status checks: ${REQUIRED_STATUS_CHECKS[*]}"
fi
echo "  3. Set merge strategy: allow merge commits, disable squash and rebase merges"
echo "     (history-computed versioning reads merge history — see GitVersion.yml)."
echo "  4. Enable Dependabot vulnerability alerts and automated security fixes."
echo "  5. Enable secret scanning and push protection (best-effort — some plans"
echo "     don't offer these on private repos; a 403 here is a warning, not a failure)."
echo
echo "This changes how ${REPO} can be written to. It does not touch any code."
echo

read -r -p "Type 'yes' to proceed: " CONFIRMATION
if [[ "${CONFIRMATION}" != "yes" ]]; then
  echo "Aborted. Nothing was changed."
  exit 1
fi
echo

# ---------------------------------------------------------------------------
# Soft-fail wrapper: run a gh api mutation; on failure, warn and continue
# rather than aborting the whole script. Used for every call below so that
# one plan-gated 403 doesn't cost every setting after it.
# ---------------------------------------------------------------------------

GH_API_ERR="$(mktemp)"
trap 'rm -f "${GH_API_ERR}"' EXIT

gh_api_soft() {
  local description="$1"
  shift
  echo "-> ${description}"
  if ! gh api "$@" >/dev/null 2>"${GH_API_ERR}"; then
    echo "   WARNING: failed — ${description}" >&2
    sed 's/^/   /' "${GH_API_ERR}" >&2
  fi
}

# ---------------------------------------------------------------------------
# (a) Ensure develop exists and is the default branch
# ---------------------------------------------------------------------------

if gh api "repos/${REPO}/branches/${DEVELOP_BRANCH}" --silent >/dev/null 2>&1; then
  echo "-> '${DEVELOP_BRANCH}' already exists; not re-creating it"
else
  echo "-> creating '${DEVELOP_BRANCH}' from the tip of '${MAIN_BRANCH}'"
  # Read the current tip of main, then create develop pointing at the same
  # commit — this is the one non-idempotent creation in the script, hence
  # the existence check above rather than a blind create-or-fail.
  MAIN_SHA="$(gh api "repos/${REPO}/git/ref/heads/${MAIN_BRANCH}" -q .object.sha)"
  gh_api_soft "create ref refs/heads/${DEVELOP_BRANCH} at ${MAIN_SHA}" \
    --method POST "repos/${REPO}/git/refs" \
    -f "ref=refs/heads/${DEVELOP_BRANCH}" \
    -f "sha=${MAIN_SHA}"
fi

# Sets the default branch new clones check out and new PRs target. Combined
# with the merge-strategy fields from (c) below into one PATCH per run would
# also work; kept separate here so this step's intent — "develop is where
# work lands" — reads as its own line, not buried in a bigger payload.
gh_api_soft "set '${DEVELOP_BRANCH}' as the default branch" \
  --method PATCH "repos/${REPO}" \
  -f "default_branch=${DEVELOP_BRANCH}"

# ---------------------------------------------------------------------------
# (b) Branch protection on main AND develop
# ---------------------------------------------------------------------------

for branch in "${MAIN_BRANCH}" "${DEVELOP_BRANCH}"; do
  # required_status_checks.contexts must be present even when empty — an
  # absent key and an empty array mean different things to the API, and we
  # want "no checks required yet" to be explicit, not accidental.
  status_check_args=()
  if [[ ${#REQUIRED_STATUS_CHECKS[@]} -eq 0 ]]; then
    status_check_args+=(-F "required_status_checks[contexts][]")
  else
    for check in "${REQUIRED_STATUS_CHECKS[@]}"; do
      status_check_args+=(-F "required_status_checks[contexts][]=${check}")
    done
  fi

  gh_api_soft "protect '${branch}' (PR + review required, no force-push, no deletion)" \
    --method PUT "repos/${REPO}/branches/${branch}/protection" \
    -F "required_status_checks[strict]=true" \
    "${status_check_args[@]}" \
    -F "enforce_admins=true" \
    -F "required_pull_request_reviews[required_approving_review_count]=1" \
    -F "required_pull_request_reviews[dismiss_stale_reviews]=true" \
    -F "restrictions=null" \
    -F "allow_force_pushes=false" \
    -F "allow_deletions=false"
done

# ---------------------------------------------------------------------------
# (c) Merge strategy: merge commits only
# ---------------------------------------------------------------------------

# Disabling squash and rebase isn't a style preference — it's a dependency.
# GitVersion.yml (and any equivalent history-derived version tool) computes
# the next version by reading merge history: which branch merged into which,
# and when. Squash-merging replaces that history with a single flat commit;
# rebase-merging rewrites it entirely. Either one deletes the exact signal
# the versioning tool reads, silently, well after the setting was changed.
gh_api_soft "require merge commits; disable squash and rebase merges" \
  --method PATCH "repos/${REPO}" \
  -F "allow_merge_commit=true" \
  -F "allow_squash_merge=false" \
  -F "allow_rebase_merge=false"

# ---------------------------------------------------------------------------
# (d) Dependency and secret security features
# ---------------------------------------------------------------------------

gh_api_soft "enable Dependabot vulnerability alerts" \
  --method PUT "repos/${REPO}/vulnerability-alerts"

gh_api_soft "enable Dependabot automated security fixes" \
  --method PUT "repos/${REPO}/automated-security-fixes"

# Secret scanning and push protection are GitHub Advanced Security features.
# They're free for public repos but plan-gated for private ones — expect
# (and tolerate) a 403 here on a private repo without GHAS, per this
# script's failure stance.
gh_api_soft "enable secret scanning and push protection" \
  --method PATCH "repos/${REPO}" \
  -F "security_and_analysis[secret_scanning][status]=enabled" \
  -F "security_and_analysis[secret_scanning_push_protection][status]=enabled"

# ---------------------------------------------------------------------------
# Manual checklist — what this script cannot do for you
# ---------------------------------------------------------------------------

cat <<'EOF'

Done with what a script can do. The rest is a manual checklist:

  [ ] Add repo secrets this CI/release pipeline needs for publishing
      (e.g. a registry token) — Settings > Secrets and variables > Actions.
  [ ] Verify branch protection actually took effect on both branches —
      Settings > Branches. Plan limits can silently drop a requested rule
      (the warnings above, if any, are your first clue which one).
  [ ] Schedule the first backup-restore drill, performed by a SECOND
      operator, not whoever set up backups (Playbook Pillar VIII) — a
      backup nobody has restored is a hypothesis, not a plan.
  [ ] Choose a license deliberately (this kit ships without one on purpose)
      — don't let a repo go public with no license by default.
  [ ] If you're using CODEOWNERS (.github/CODEOWNERS), turn on "Require
      review from Code Owners" in the branch protection rule for the
      branches it should apply to — this script does not enable that flag.

EOF
