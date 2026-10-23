#!/usr/bin/env bash
# Builds an UPDATE change set (a preview) for grc-engineer-users and checks it
# is exactly the console-login change. Applies nothing. Deletes the preview if
# it does not match.
#   bash infrastructure/scripts/grc-engineer-users/2-preview-update.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"

require_clean_main
pass "on clean main, equal to origin/main"
require_account

status=$(stack_status)
[[ "$status" == *_COMPLETE && "$status" != *ROLLBACK* ]] || stop "stack $STACK status is $status, expected CREATE_COMPLETE or UPDATE_COMPLETE."
pass "stack $STACK is $status"

echo "Checking drift on $STACK and $BASE_STACK (about 30 seconds each) ..."
for s in "$STACK" "$BASE_STACK"; do
  d=$(drift_of "$s")
  [ "$d" = "IN_SYNC" ] || stop "$s drift status is $d. AWS does not match GitHub. Do not continue."
  pass "$s IN_SYNC"
done

# Remove a leftover preview with the same name, if any.
aws cloudformation delete-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" 2>/dev/null || true

# User names stay as deployed (UsePreviousValue), so no names are typed here.
aws cloudformation create-change-set --change-set-type UPDATE \
  --stack-name "$STACK" \
  --change-set-name "$CHANGE_SET" \
  --template-body "file://$TEMPLATE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=AutomationEngineerUserName,UsePreviousValue=true \
    ParameterKey=IssmBuilderUserName,UsePreviousValue=true \
  "${AWS_OPTS[@]}" >/dev/null
echo "Creating the preview ..."
if ! aws cloudformation wait change-set-create-complete --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}"; then
  aws cloudformation describe-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" --query StatusReason --output text || true
  aws cloudformation delete-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" || true
  stop "the preview failed (reason above). It was deleted. Nothing changed."
fi

changes=$(aws cloudformation describe-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" \
  --query "Changes[].ResourceChange.[Action,LogicalResourceId,Replacement]" --output text | sort)
expected=$(printf 'Add\tGrcAutomationEngineerInitialPassword\tNone\nAdd\tGrcIssmBuilderInitialPassword\tNone\nModify\tGrcAutomationEngineerUser\tFalse\nModify\tGrcIssmBuilderUser\tFalse\n' | sort)
echo "Preview shows (Action, Resource, Replacement):"
echo "$changes"
if [ "$changes" != "$expected" ]; then
  aws cloudformation delete-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" || true
  stop "the preview is not exactly 2 new secrets plus 2 in-place user updates. It was deleted. Nothing changed."
fi
pass "preview is exactly 2 Add (secrets) and 2 Modify (users, no replacement), 0 Remove"

echo
echo "Nothing has been applied. Next: 3-apply-update.sh"
