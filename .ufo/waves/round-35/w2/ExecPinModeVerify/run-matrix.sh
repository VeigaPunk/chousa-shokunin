#!/usr/bin/env bash
# ExecPinModeVerify matrix: mode `verify` on a committed record, CLEAN verdict,
# under the round-35 grep pin. Clone pinned at e87c5d7e.
set -u
BASE=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
CLONE=$BASE/clone
OUT=$BASE/out2
SHIM=$BASE/shim
TRIP=$BASE/tripwire2
CLEANPATH=/usr/local/bin:/usr/bin:/bin
RECORD=corpus/fixtures/archives-r9/A-r9.md
ROOT=$BASE/root          # holds research/deep-research-2026-09-28/*.md (copied, read-only source)
CLOCK=1750000000
mkdir -p "$OUT" "$TRIP"

: > "$TRIP/trip-path.log"; : > "$TRIP/trip-fn.log"

run() { # NAME PATH [RGREP] [ECHO] [BASHENV]
  local name=$1 p=$2 rg=${3:-} ec=${4:-} be=${5:-}
  ( cd "$CLONE" && env -i HOME=/tmp PATH="$p" \
      ${rg:+RESEARCH_GATE_GREP="$rg"} ${ec:+CHOUSA_GREP_PIN_ECHO="$ec"} \
      ${be:+BASH_ENV="$be"} CHOUSA_NOW_EPOCH="$CLOCK" \
      bash tools/research-gate.sh verify --record "$RECORD" --root "$ROOT" \
      >"$OUT/$name.out" 2>"$OUT/$name.err"; echo $? > "$OUT/$name.rc" )
  printf '%-24s rc=%-3s trip_path=%-6s trip_fn=%-6s verdict=%s\n' "$name" \
    "$(cat "$OUT/$name.rc")" \
    "$(wc -c < "$TRIP/trip-path.log")" "$(wc -c < "$TRIP/trip-fn.log")" \
    "$(grep -h '^RESEARCH_GATE: ' "$OUT/$name.out" || echo NONE)"
}

run a-clean            "$CLEANPATH"
run b-pathshim         "$SHIM:$CLEANPATH"
run c-override+shim    "$SHIM:$CLEANPATH" "/usr/bin/grep"
run d-echo             "$CLEANPATH" "" "1"
run e-override+echo+shim "$SHIM:$CLEANPATH" "/usr/bin/grep" "1"
run f-bashenv-fn       "$CLEANPATH" "" "" "$BASE/bash_env.sh"
run g-bashenv+override "$SHIM:$CLEANPATH" "/usr/bin/grep" "" "$BASE/bash_env.sh"

echo "--- byte compare stdout (fixed clock) ---"
for p in b-pathshim c-override+shim d-echo e-override+echo+shim f-bashenv-fn g-bashenv+override; do
  if cmp -s "$OUT/a-clean.out" "$OUT/$p.out"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "  a-clean vs $p : $r"
done
echo "--- byte compare stderr ---"
for p in b-pathshim c-override+shim f-bashenv-fn g-bashenv+override; do
  if cmp -s "$OUT/a-clean.err" "$OUT/$p.out.err" 2>/dev/null; then :; fi
  if cmp -s "$OUT/a-clean.err" "$OUT/$p.err"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "  a-clean vs $p : $r"
done
echo "--- GATE_GREP echo lines ---"
for f in "$OUT"/*.err; do
  l=$(grep -h '^GATE_GREP: ' "$f" || true)
  [[ -n $l ]] && printf '  %s :: %s\n' "$(basename "$f")" "$l"
done
echo "--- verdict line (a) ---"; grep '^RESEARCH_GATE: ' "$OUT/a-clean.out"
echo "--- verdict lines all (unique) ---"; grep -h '^RESEARCH_GATE: ' "$OUT"/*.out | sort | uniq -c
