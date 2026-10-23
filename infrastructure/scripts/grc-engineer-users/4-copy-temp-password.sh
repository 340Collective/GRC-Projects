#!/usr/bin/env bash
# Copies one seat's one-time console password to the clipboard. Never prints it.
# ISSM only: engineers are denied secretsmanager:GetSecretValue.
#   bash infrastructure/scripts/grc-engineer-users/4-copy-temp-password.sh <user>
#
# Paste it into a private message to that person with the sign-in URL and their
# user name. Never into GitHub, Jira, a log, or a group chat. Then clear the
# clipboard. They must change it at first sign-in, then enroll MFA.
set -euo pipefail
source "$(dirname "$0")/lib.sh"

USER_NAME="${1:-}"
[ -n "$USER_NAME" ] || stop "give the user name, for example: bash $0 <user>"
require_account

secret_id=""
for pair in "AutomationEngineerUserName:AutomationEngineerPasswordSecret" "IssmBuilderUserName:IssmBuilderPasswordSecret"; do
  if [ "$(stack_output "${pair%%:*}")" = "$USER_NAME" ]; then
    secret_id=$(stack_output "${pair##*:}")
  fi
done
[ -n "$secret_id" ] || stop "$USER_NAME is not a seat in stack $STACK."

if command -v pbcopy >/dev/null; then copy=pbcopy
elif command -v clip.exe >/dev/null; then copy=clip.exe
elif command -v clip >/dev/null; then copy=clip
else stop "no clipboard tool found (pbcopy or clip)."
fi

aws secretsmanager get-secret-value --secret-id "$secret_id" "${AWS_OPTS[@]}" \
  --query SecretString --output text | tr -d '\n' | "$copy"
pass "one-time password for $USER_NAME is on the clipboard (not shown)"

url=$(aws cloudformation describe-stacks --stack-name "$BASE_STACK" "${AWS_OPTS[@]}" \
  --query "Stacks[0].Outputs[?OutputKey=='ConsoleSignInUrl'].OutputValue" --output text)
echo "Send privately: sign-in URL $url, user name $USER_NAME, and the password you just copied."
echo "Then clear the clipboard (macOS: pbcopy < /dev/null)."
