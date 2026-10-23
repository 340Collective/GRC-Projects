#!/usr/bin/env bash
# Checks the grc-engineer-users template. Read-only, changes nothing in AWS.
#   bash infrastructure/scripts/grc-engineer-users/1-check-template.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"

VENV="/tmp/grc_cfnlint"

[ -f "$TEMPLATE" ] || stop "$TEMPLATE not found."
git ls-files --error-unmatch "$TEMPLATE" >/dev/null 2>&1 || stop "$TEMPLATE is not tracked in git."
pass "template present and tracked in git"

require_account
pass "profile $PROFILE is account $ACCOUNT"

size=$(wc -c < "$TEMPLATE" | tr -d ' ')
[ "$size" -lt 51200 ] || stop "template is $size bytes. AWS allows less than 51200."
pass "template size $size bytes (limit 51200)"

if [ ! -x "$VENV/bin/cfn-lint" ]; then
  echo "Installing cfn-lint 1.57.2 into $VENV ..."
  python3 -m venv --clear "$VENV" >/dev/null
  "$VENV/bin/pip" install -q cfn-lint==1.57.2
fi
"$VENV/bin/cfn-lint" "$TEMPLATE" || stop "cfn-lint found problems (above)."
pass "cfn-lint clean"

aws cloudformation validate-template --template-body "file://$TEMPLATE" "${AWS_OPTS[@]}" >/dev/null \
  || stop "AWS rejected the template (error above)."
pass "AWS validate-template OK"

echo
echo "All checks passed. Next: 2-preview-update.sh"
