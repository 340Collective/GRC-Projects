#!/usr/bin/env bash
# Signs you in to the AWS CLI with MFA for 12 hours. Anyone can use this one.
#
#   bash infrastructure/scripts/grc-engineer-users/0-mfa-login.sh 123456
#
# Reads your access key from profile BASE (default 340collective-base) and
# writes temporary MFA credentials to profile TARGET (default 340collective).
# Every call in this account without MFA is denied (grc-require-mfa), so run
# this at the start of each work session. Override the names if yours differ:
#
#   BASE=my-keys TARGET=my-mfa bash .../0-mfa-login.sh 123456
set -euo pipefail

BASE="${BASE:-340collective-base}"
TARGET="${TARGET:-340collective}"
CODE="${1:-}"

[[ "$CODE" =~ ^[0-9]{6}$ ]] || { echo "STOP  run it with your 6-digit MFA code, for example: bash $0 123456"; exit 1; }

user_arn=$(aws sts get-caller-identity --profile "$BASE" --query Arn --output text) \
  || { echo "STOP  profile $BASE does not work. Run: aws configure --profile $BASE"; exit 1; }
user_name="${user_arn##*/}"
mfa_arn=$(aws iam list-mfa-devices --user-name "$user_name" --profile "$BASE" --query "MFADevices[0].SerialNumber" --output text)
[ "$mfa_arn" != "None" ] || { echo "STOP  no MFA device on $user_name. Add one in the AWS console first."; exit 1; }

read -r key secret token < <(aws sts get-session-token --serial-number "$mfa_arn" --token-code "$CODE" \
  --duration-seconds 43200 --profile "$BASE" \
  --query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" --output text)

aws configure set aws_access_key_id "$key" --profile "$TARGET"
aws configure set aws_secret_access_key "$secret" --profile "$TARGET"
aws configure set aws_session_token "$token" --profile "$TARGET"
aws configure set region us-east-1 --profile "$TARGET"

acct=$(aws sts get-caller-identity --profile "$TARGET" --query Account --output text)
echo "PASS  signed in as $user_name with MFA, account $acct, profile $TARGET, good for 12 hours"
