#!/usr/bin/env bash
# JSON oracle: uses the gate's OWN bash JSON reader (claim_scan/json_str/
# json_has_key/json_unescape, extracted verbatim from tools/research-gate.sh
# :1139-1400 into jsonread.sh) to parse each claims.jsonl line and report the
# top-level keys it sees plus the decoded span length.
# Output per line: RC <rc> KEYS <k1,k2,...> SPANBYTES <n> ID <id>
set -u
export LC_ALL=C
cd "$(dirname "$0")"
# shellcheck disable=SC1091
source ./jsonread.sh
JSON_SCAN_LINE=''; JSON_SCAN_RC=1
declare -A JSON_PRESENT=() JSON_STR=() JSON_DUP=() JSON_DUPDIFF=()
while IFS= read -r line; do
  if claim_scan "$line"; then rc=0; else rc=1; fi
  keys=''
  for k in id source span expect marker line sha256; do
    if json_has_key "$line" "$k"; then keys="$keys,$k"; fi
  done
  raw=$(json_str "$line" span 2>/dev/null || true)
  dec=$(json_unescape "$raw"; printf x); dec=${dec%x}
  n=${#dec}
  id=$(json_unescape "$(jfield "$line" id)")
  printf 'RC %d KEYS %s SPANBYTES %d ID %s\n' "$rc" "${keys#,}" "$n" "$id"
done < "$1"
