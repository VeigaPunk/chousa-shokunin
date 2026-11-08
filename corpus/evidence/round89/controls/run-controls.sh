#!/usr/bin/env bash
# run-controls.sh — round-89 control-receipt driver.
#
# Round 88's spot-check routed defect 5: `controls/expected.tsv` carried a `c1-do-nothing` row expecting exit 1
# while its own committed receipt printed PASS, and `c2-d0-donothing.txt` had no expectation row at all — the
# receipts were never checked against their expectations. This driver IS that check: it runs each control, writes
# its receipt, and refuses to pass unless the receipt's exit code and every `required_fields` token agree with the
# row in expected.tsv.
#
# Usage: bash corpus/evidence/round89/controls/run-controls.sh <lane-root> <work-dir>
# Exit 0 every receipt agrees, 1 a disagreement (printed RECEIPT_MISMATCH), 2 setup.
set -uo pipefail
ROOT=${1:?lane root}
WORK=${2:?work dir}
HERE=$(cd "$(dirname "$0")" && pwd)
REC="$HERE/receipts"
mkdir -p "$REC" "$WORK"

rc_all=0
while IFS=$'\t' read -r case_id instrument expected_exit required fields_src; do
  [ "$case_id" = "case" ] && continue
  [ -z "${case_id:-}" ] && continue
  out="$REC/$case_id.txt"
  # shellcheck disable=SC2086
  ( cd "$ROOT" && eval "$instrument" ) >"$out" 2>&1
  got=$?
  bad=""
  [ "$got" != "$expected_exit" ] && bad="$bad exit=$got want=$expected_exit"
  for f in $required; do
    grep -qF -- "$f" "$out" || bad="$bad missing[$f]"
  done
  if [ -n "$bad" ]; then
    echo "RECEIPT_MISMATCH $case_id:$bad"
    rc_all=1
  else
    echo "RECEIPT_OK $case_id exit=$got"
  fi
done < "$HERE/expected.tsv"
echo "CONTROL_RECEIPTS=$([ $rc_all -eq 0 ] && echo PASS || echo FAIL)"
exit $rc_all
