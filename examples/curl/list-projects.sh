#!/usr/bin/env bash
# List recent projects.
# Usage:  REVID_API_KEY=… ./list-projects.sh [limit]
set -euo pipefail
: "${REVID_API_KEY:?set REVID_API_KEY}"
LIMIT="${1:-10}"

curl -s "https://www.revid.ai/api/public/v3/projects?limit=$LIMIT" \
  -H "key: $REVID_API_KEY" | jq .
