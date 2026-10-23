#!/usr/bin/env bash
# Checks every engineer seat is set up correctly. Read-only.
#   bash infrastructure/scripts/grc-engineer-users/5-verify.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"

failed=0
miss() { echo "FAIL  $1"; failed=1; }

require_account

status=$(stack_status)
[[ "$status" == *_COMPLETE && "$status" != *ROLLBACK* ]] && pass "stack $STACK is $status" || miss "stack $STACK status is $status"

# Seats come from the stack outputs, so no names are hard-coded here.
for pair in "AutomationEngineerUserName:Automation-Engineer" "IssmBuilderUserName:ISSM-Builder"; do
  u=$(stack_output "${pair%%:*}")
  [ -n "$u" ] && [ "$u" != "None" ] || continue
  fn="${pair##*:}"
  echo "== $u"

  groups=$(aws iam list-groups-for-user --user-name "$u" "${AWS_OPTS[@]}" --query "Groups[].GroupName" --output text)
  [ "$groups" = "GRC-Engineer" ] && pass "in group GRC-Engineer only" || miss "groups are '$groups', expected GRC-Engineer"

  boundary=$(aws iam get-user --user-name "$u" "${AWS_OPTS[@]}" --query "User.PermissionsBoundary.PermissionsBoundaryArn" --output text)
  [[ "$boundary" == *":policy/grc-permissions-boundary" ]] && pass "boundary grc-permissions-boundary" || miss "boundary is '$boundary'"

  tags=$(aws iam list-user-tags --user-name "$u" "${AWS_OPTS[@]}" --query "Tags[].[Key,Value]" --output text | sort | tr '\t\n' '= ')
  want="grc-function=$fn grc-managed-by=grc-engineer-users grc-role=engineer "
  [ "$tags" = "$want" ] && pass "tags correct" || miss "tags are: $tags"

  keys=$(aws iam list-access-keys --user-name "$u" "${AWS_OPTS[@]}" --query "length(AccessKeyMetadata)" --output text)
  [ "$keys" = "0" ] && pass "no access keys" || echo "NOTE  $keys access key(s). Fine only if the user created them for CLI use."

  if aws iam get-login-profile --user-name "$u" "${AWS_OPTS[@]}" >/dev/null 2>&1; then
    pass "console login exists"
  else
    miss "no console login. Run 2-preview-update.sh and 3-apply-update.sh."
  fi

  mfa=$(aws iam list-mfa-devices --user-name "$u" "${AWS_OPTS[@]}" --query "length(MFADevices)" --output text)
  [ "$mfa" != "0" ] && pass "MFA set up" || echo "WAIT  no MFA yet. Run again after they sign in and enroll."
done

for s in "$STACK" "$BASE_STACK"; do
  echo "Checking drift on $s (about 30 seconds) ..."
  d=$(drift_of "$s")
  [ "$d" = "IN_SYNC" ] && pass "$s IN_SYNC" || miss "$s drift status $d"
done

echo
if [ "$failed" = 0 ]; then
  echo "All checks passed. Tag the release: git tag live-$(date +%F) && git push origin live-$(date +%F)"
else
  echo "Something is not right (FAIL lines above). Do not tag."
  exit 1
fi
