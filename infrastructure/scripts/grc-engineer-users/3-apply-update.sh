#!/usr/bin/env bash
# Applies the preview made by 2-preview-update.sh through CloudFormation.
# ISSM only, from clean main. Asks before applying.
#   bash infrastructure/scripts/grc-engineer-users/3-apply-update.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"

require_clean_main
pass "on clean main, equal to origin/main"
require_account

cs_status=$(aws cloudformation describe-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}" \
  --query "[Status,ExecutionStatus]" --output text 2>/dev/null || echo "NONE")
[ "$cs_status" = "$(printf 'CREATE_COMPLETE\tAVAILABLE')" ] || stop "no ready preview named $CHANGE_SET (got: $cs_status). Run 2-preview-update.sh first."

read -r -p "Apply change set $CHANGE_SET to stack $STACK? Type yes: " answer
[ "$answer" = "yes" ] || stop "not applied."

aws cloudformation execute-change-set --stack-name "$STACK" --change-set-name "$CHANGE_SET" "${AWS_OPTS[@]}"
echo "Applying (about 1 minute) ..."
aws cloudformation wait stack-update-complete --stack-name "$STACK" "${AWS_OPTS[@]}" \
  || stop "update did not complete. Status: $(stack_status). Check the stack events in the console."
pass "stack $STACK is $(stack_status)"

echo
echo "Next: 4-copy-temp-password.sh <user>, once per person, then 5-verify.sh"
