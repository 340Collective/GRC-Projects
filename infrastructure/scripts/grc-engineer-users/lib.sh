#!/usr/bin/env bash
# Shared settings and helpers for the grc-engineer-users scripts. Sourced, not run.

STACK="grc-engineer-users"
BASE_STACK="grc-access-model"
TEMPLATE="infrastructure/cloudformation/grc-engineer-users.yaml"
CHANGE_SET="add-console-logins"
PROFILE="${PROFILE:-340collective}"
REGION="us-east-1"
ACCOUNT="570814274897"
AWS_OPTS=(--profile "$PROFILE" --region "$REGION")

pass() { echo "PASS  $1"; }
stop() { echo "STOP  $1"; exit 1; }

# Run from the repo root no matter where the script is called from.
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO"

require_account() {
  local acct
  acct=$(aws sts get-caller-identity "${AWS_OPTS[@]}" --query Account --output text) \
    || stop "AWS profile $PROFILE does not work. Run 0-mfa-login.sh first."
  [ "$acct" = "$ACCOUNT" ] || stop "profile $PROFILE is account $acct, expected $ACCOUNT."
}

# Change control: AWS changes only from clean main equal to GitHub.
require_clean_main() {
  git fetch origin --quiet
  [ "$(git branch --show-current)" = "main" ] || stop "not on main. Run: git switch main && git pull"
  [ -z "$(git status --porcelain --untracked-files=no)" ] || stop "main has uncommitted changes. Run: git status"
  [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || stop "local main differs from GitHub. Run: git pull"
  git ls-files --error-unmatch "$TEMPLATE" >/dev/null 2>&1 || stop "$TEMPLATE is not tracked in git."
}

stack_status() {
  aws cloudformation describe-stacks --stack-name "$STACK" "${AWS_OPTS[@]}" \
    --query "Stacks[0].StackStatus" --output text 2>/dev/null || echo "NONE"
}

stack_output() {
  aws cloudformation describe-stacks --stack-name "$STACK" "${AWS_OPTS[@]}" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}

drift_of() {
  local id status
  id=$(aws cloudformation detect-stack-drift --stack-name "$1" "${AWS_OPTS[@]}" --query StackDriftDetectionId --output text)
  while :; do
    status=$(aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id "$id" "${AWS_OPTS[@]}" --query DetectionStatus --output text)
    [ "$status" = "DETECTION_IN_PROGRESS" ] || break
    sleep 5
  done
  aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id "$id" "${AWS_OPTS[@]}" --query StackDriftStatus --output text
}
