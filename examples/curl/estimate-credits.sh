#!/usr/bin/env bash
# Estimate credits before rendering. Mirror your /render body.
# Usage:  REVID_API_KEY=… ./estimate-credits.sh path/to/payload.json
set -euo pipefail
: "${REVID_API_KEY:?set REVID_API_KEY}"
PAYLOAD_FILE="${1:?path to render payload json required}"

curl -s https://www.revid.ai/api/public/v3/calculate-credits \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d @"$PAYLOAD_FILE" | jq .
