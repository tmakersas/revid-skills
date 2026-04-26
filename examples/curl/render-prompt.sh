#!/usr/bin/env bash
# Smallest possible Revid call. Confirms key + auth + render + status.
# Usage:  REVID_API_KEY=… ./render-prompt.sh "Your one-line idea"
set -euo pipefail
: "${REVID_API_KEY:?set REVID_API_KEY}"
PROMPT="${1:-Why honey never spoils.}"

PID=$(curl -fsS https://www.revid.ai/api/public/v3/render \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d "$(jq -n --arg p "$PROMPT" '{
    workflow:"prompt-to-video",
    source:{prompt:$p,durationSeconds:30},
    aspectRatio:"9:16"
  }')" | jq -r .pid)

echo "pid=$PID"

while :; do
  R=$(curl -fsS "https://www.revid.ai/api/public/v3/status?pid=$PID" -H "key: $REVID_API_KEY")
  S=$(echo "$R" | jq -r .status)
  P=$(echo "$R" | jq -r .progress)
  echo "  status=$S progress=$P"
  case "$S" in
    ready)  echo "$R" | jq .; break ;;
    failed) echo "FAILED: $R"; exit 1 ;;
  esac
  sleep 5
done
