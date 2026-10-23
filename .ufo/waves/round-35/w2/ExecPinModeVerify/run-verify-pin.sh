#!/usr/bin/env bash
# ExecPinModeVerify: mode `verify` under the round-35 grep pin.
# Clone at e87c5d7ea2dbf3730b36a3961de3f06261d015e4, gate sha256 pinned.
# Scenarios: (a) clean PATH, (b) PATH shim + tripwire, (c) override + shim,
# (d) CHOUSA_GREP_PIN_ECHO=1.
set -u

BASE=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
CLONE=$BASE/clone
OUT=$BASE/out
SHIM=$BASE/shim
TRIP=$BASE/tripwire
CLEANPATH=/usr/local/bin:/usr/bin:/bin
RECORD=corpus/fixtures/archives-r9/A-r9.md

mkdir -p "$OUT" "$SHIM" "$TRIP"

# PATH shim: logs every call, then execs the real GNU grep.
cat > "$SHIM/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP/trip-path.log" 2>/dev/null
exec /usr/bin/grep "\$@"
EOF
chmod 755 "$SHIM/grep"

# BASH_ENV function shim (function form, not a PATH binary).
cat > "$BASE/bash_env.sh" <<EOF
grep() { printf 'fn %s\n' "\$*" >>"$TRIP/trip-fn.log" 2>/dev/null; command /usr/bin/grep "\$@"; }
EOF

run() { # NAME ENVSPEC...  -- env applied via `env -i`-ish controlled set
  local name=$1; shift
  ( cd "$CLONE" && env -i \
      HOME=/tmp PATH="$1" \
      ${2:+RESEARCH_GATE_GREP="$2"} \
      ${3:+CHOUSA_GREP_PIN_ECHO="$3"} \
      ${4:+BASH_ENV="$4"} \
      ${5:+CHOUSA_NOW_EPOCH="$5"} \
      bash tools/research-gate.sh verify --record "$RECORD" --root . \
      >"$OUT/$name.out" 2>"$OUT/$name.err" ; echo $? > "$OUT/$name.rc" )
  printf '%-26s rc=%s\n' "$name" "$(cat "$OUT/$name.rc")"
}

: > "$TRIP/trip-path.log"; : > "$TRIP/trip-fn.log"

run a-clean            "$CLEANPATH" "" "" "" ""
run b-pathshim         "$SHIM:$CLEANPATH" "" "" "" ""
run c-override+shim    "$SHIM:$CLEANPATH" "/usr/bin/grep" "" "" ""
run d-echo             "$CLEANPATH" "" "1" "" ""
run e-override+echo    "$SHIM:$CLEANPATH" "/usr/bin/grep" "1" "" ""
run f-bashenv-fn       "$CLEANPATH" "" "" "$BASE/bash_env.sh" ""

# a2/b2 with a FIXED clock so the ts= header is stable -> byte comparison.
run a2-clean-fixed     "$CLEANPATH" "" "" "" "1750000000"
run b2-pathshim-fixed  "$SHIM:$CLEANPATH" "" "" "" "1750000000"
run c2-ovr+shim-fixed  "$SHIM:$CLEANPATH" "/usr/bin/grep" "" "" "1750000000"
run d2-echo-fixed      "$CLEANPATH" "" "1" "" "1750000000"

echo "--- tripwire sizes ---"
wc -c "$TRIP"/*.log
echo "--- byte compare (fixed clock) ---"
for p in b2-pathshim-fixed c2-ovr+shim-fixed; do
  if cmp -s "$OUT/a2-clean-fixed.out" "$OUT/$p.out"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "a2 vs $p stdout: $r"
done
if cmp -s "$OUT/a2-clean-fixed.err" "$OUT/b2-pathshim-fixed.err"; then r=IDENTICAL; else r=DIFFERENT; fi
echo "a2 vs b2-pathshim-fixed stderr: $r"
echo "--- verdict lines ---"
grep -h '^RESEARCH_GATE: ' "$OUT"/*.out | sort | uniq -c
echo "--- GATE_GREP echo lines (stderr) ---"
grep -h '^GATE_GREP: ' "$OUT"/*.err || echo "(none)"
