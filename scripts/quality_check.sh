#!/bin/bash
# Pre-publication quality check for academic papers.
# Usage: ./scripts/quality_check.sh papers/my_paper.md
#
# Runs all automated grep checks from QUALITY_CHECKLIST.md in one pass.
# Fix every hit or justify why it's acceptable.

set -euo pipefail

PAPER="${1:?Usage: ./scripts/quality_check.sh <paper.md>}"

if [ ! -f "$PAPER" ]; then
  echo "Error: File not found: $PAPER"
  exit 1
fi

ISSUES=0
count_hits() {
  local n
  n=$(echo "$1" | grep -c . 2>/dev/null || true)
  ISSUES=$((ISSUES + n))
}

echo "╔══════════════════════════════════════════════════════╗"
echo "║          PRE-PUBLICATION QUALITY CHECK               ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Scanning: $PAPER"
echo ""

# 1. AI Phrasing & Unicode Dashes
echo "━━━ 1. AI PHRASING & UNICODE DASHES ━━━"
HITS=$(grep -nE '—|–|notably|comprehensive|striking|fundamental|furthermore|moreover|landscape|paradigm|unprecedented|leverage|foster|facilitate|delve|tapestry|testament|multifaceted|robust|pivotal|seamless|synergy|democratize|empower|beacon' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 2. Race / Competition Language
echo "━━━ 2. RACE / COMPETITION LANGUAGE ━━━"
HITS=$(grep -niE 'overtaking|overtook|beat|won the|race to|dominate|dominance|leader in|leading the' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 3. Semantic Overstatement
echo "━━━ 3. SEMANTIC OVERSTATEMENT ━━━"
HITS=$(grep -niE '\bconfirms?\b|\bprove[sd]?\b|has not plateaued|\breplaced\b|collect citations|paper abstracts' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 4. Hedging Violations
echo "━━━ 4. HEDGING VIOLATIONS (will/would/should) ━━━"
HITS=$(grep -nwE 'will|would|should' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 5. Sensitivity Red Flags
echo "━━━ 5. SENSITIVITY RED FLAGS ━━━"
HITS=$(grep -niE 'deserves|surprising|impressive|remarkable' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 6. AI Opener Patterns
echo "━━━ 6. AI OPENER PATTERNS ━━━"
HITS=$(grep -niE 'accelerating pace|rapidly evolving|comprehensive analysis|in recent years|it is worth noting|plays a crucial|increasingly important' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 7. Cliché Phrases
echo "━━━ 7. CLICHÉ PHRASES ━━━"
HITS=$(grep -niE 'blurred boundar|double-edged|paradigm shift|game.changer|at the forefront|paves the way|sheds light|tip of the iceberg|cautious optimism|not merely' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 8. Causal Language
echo "━━━ 8. CAUSAL LANGUAGE (review in context) ━━━"
HITS=$(grep -niE 'caused by|leads to|results in|\bdrives\b|driven by' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 9. Definitive Trend Claims
echo "━━━ 9. DEFINITIVE TREND CLAIMS ━━━"
HITS=$(grep -niE 'has (not )?plateaued|is (now )?dead|will (never|always)|inevitable' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

# 10. Colons in Prose (outside headers/refs)
echo "━━━ 10. COLONS IN PROSE (review in context) ━━━"
HITS=$(grep -nE '^[^#|*\[].*[a-z]:[ ]' "$PAPER" 2>/dev/null || true)
if [ -n "$HITS" ]; then echo "$HITS"; count_hits "$HITS"; else echo "  ✓ Clean"; fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$ISSUES" -eq 0 ]; then
  echo "✓ ALL AUTOMATED CHECKS PASSED"
else
  echo "⚠ $ISSUES lines flagged. Review and fix each one."
fi
echo ""
echo "Next: Run the 10-reviewer pass (see QUALITY_CHECKLIST.md §10)"
