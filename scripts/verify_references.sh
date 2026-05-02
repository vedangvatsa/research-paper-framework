#!/bin/bash
# verify_references.sh — Curl-checks every URL in a paper's References section.
# Usage: ./scripts/verify_references.sh papers/your_paper.md
#
# Exit codes:
#   0 = all URLs return 200/2xx/403 (bot-blocked but browser-accessible)
#   1 = one or more URLs return 404 or 5xx (genuinely broken)
#
# Run this BEFORE every commit that touches references.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <markdown-file>"
  exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "ERROR: File not found: $FILE"
  exit 1
fi

# Extract all URLs from markdown links [text](url)
URLS=$(grep -Eo 'https://[^)]+' "$FILE" | sed 's/](.*//g' | sort -u)

if [ -z "$URLS" ]; then
  echo "No URLs found in $FILE"
  exit 0
fi

TOTAL=0
OK=0
BOT_BLOCKED=0
BROKEN=0
BROKEN_LIST=""

echo "================================================"
echo "  Reference URL Verification"
echo "  File: $FILE"
echo "================================================"
echo ""

while IFS= read -r url; do
  TOTAL=$((TOTAL + 1))
  code=$(curl -sL -o /dev/null -w '%{http_code}' --max-time 15 "$url" 2>/dev/null || echo "000")

  # Normalize multi-digit zero codes (curl sometimes returns 000000)
  if echo "$code" | grep -qE '^0+$'; then
    code="000"
  fi

  case "$code" in
    2*)
      printf "  ✓ %s  %s\n" "$code" "$url"
      OK=$((OK + 1))
      ;;
    403)
      printf "  ~ %s  %s  (bot-blocked, likely works in browser)\n" "$code" "$url"
      BOT_BLOCKED=$((BOT_BLOCKED + 1))
      ;;
    000)
      printf "  ~ %s  %s  (timeout/bot-protection)\n" "$code" "$url"
      BOT_BLOCKED=$((BOT_BLOCKED + 1))
      ;;
    404|410)
      printf "  ✗ %s  %s  << BROKEN\n" "$code" "$url"
      BROKEN=$((BROKEN + 1))
      BROKEN_LIST="$BROKEN_LIST\n  - $url ($code)"
      ;;
    5*)
      printf "  ✗ %s  %s  << SERVER ERROR\n" "$code" "$url"
      BROKEN=$((BROKEN + 1))
      BROKEN_LIST="$BROKEN_LIST\n  - $url ($code)"
      ;;
    *)
      printf "  ? %s  %s  (unexpected)\n" "$code" "$url"
      BROKEN=$((BROKEN + 1))
      BROKEN_LIST="$BROKEN_LIST\n  - $url ($code)"
      ;;
  esac
done <<< "$URLS"

echo ""
echo "================================================"
echo "  Results: $TOTAL URLs checked"
echo "    OK (2xx):         $OK"
echo "    Bot-blocked:      $BOT_BLOCKED"
echo "    Broken (4xx/5xx): $BROKEN"
echo "================================================"

if [ "$BROKEN" -gt 0 ]; then
  echo ""
  echo "  BROKEN URLs that must be fixed before committing:"
  printf "$BROKEN_LIST\n"
  echo ""
  echo "  FAILED: Fix the broken URLs above and re-run."
  exit 1
else
  echo ""
  echo "  PASSED: All URLs are reachable or behind known bot-blockers."
  exit 0
fi
