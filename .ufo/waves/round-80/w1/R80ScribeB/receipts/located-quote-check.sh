#!/bin/sh
# located-quote-check.sh REV FILE LINE QUOTE RECEIPT
# Re-opens a located quote at a named revision (grep -cF on the named line), counts its words (wc -w)
# and requires the control receipt to name its measured revision as a 40-hex REV= key.
REV=$1; FILE=$2; LINE=$3; QUOTE=$4; RECEIPT=$5
LOCATED=$(git show "$REV:$FILE" | sed -n "${LINE}p" | grep -cF -- "$QUOTE")
WORDS=$(printf '%s' "$QUOTE" | wc -w | tr -d ' ')
RECEIPT_REV=$(grep -cE '(^|[^A-Z_])REV=[0-9a-f]{40}' "$RECEIPT")
echo "LOCATED=$LOCATED WORDS=$WORDS RECEIPT_REV=$RECEIPT_REV"
if [ "$LOCATED" -eq 1 ] && [ "$WORDS" -le 25 ] && [ "$RECEIPT_REV" -ge 1 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
