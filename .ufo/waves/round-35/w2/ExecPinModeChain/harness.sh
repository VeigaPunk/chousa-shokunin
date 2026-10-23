#!/bin/bash
# ExecPinModeChain harness — verify-chain mode under the grep pin (round-35 C1 surface).
# Read-only on the lane; writes only into OUT.
# Usage: harness.sh OUTDIR
set -u
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
GATE=$LANE/tools/research-gate.sh
FIX=$LANE/corpus/fixtures/chain-r3.md
BROKEN=$LANE/corpus/fixtures/chain-r3-broken.md
OUT=${1:?outdir}
S=/tmp/hyaku/chousa-r35/w2/ExecPinModeChain
mkdir -p "$OUT" "$S"

REAL_GREP=/usr/bin/grep
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin

# --- shims ---------------------------------------------------------------
SHIM_BIN=$S/bin; mkdir -p "$SHIM_BIN"
TRIP_PATH=$S/trip-path.log; : >"$TRIP_PATH"
cat >"$SHIM_BIN/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP_PATH" 2>/dev/null
exec $REAL_GREP "\$@"
EOF
chmod 755 "$SHIM_BIN/grep"

TRIP_FN=$S/trip-fn.log; : >"$TRIP_FN"
cat >"$S/bash_env.sh" <<EOF
grep() { printf 'fn %s\n' "\$*" >>"$TRIP_FN" 2>/dev/null; command $REAL_GREP "\$@"; }
EOF

# logging wrapper that execs the real grep (stamps argv + provenance)
TRIP_WRAP=$S/trip-wrap.log; : >"$TRIP_WRAP"
WRAP=$S/grep-wrapper.sh
cat >"$WRAP" <<EOF
#!/bin/sh
printf 'ARGV[%s]\n' "\$*" >>"$TRIP_WRAP" 2>/dev/null
exec $REAL_GREP "\$@"
EOF
chmod 755 "$WRAP"

# no-grep PATH farm
NOGREP=$S/nogrepbin; mkdir -p "$NOGREP"
for n in bash sh od tr sed cut head tail date wc sort uniq cat mkdir mktemp dirname basename readlink sha256sum stat ls find python3 sleep mv rm cp touch awk env xargs flock printf expr test true false id; do
  for b in /usr/bin /bin; do
    if [ -x "$b/$n" ] && [ ! -e "$NOGREP/$n" ]; then ln -s "$b/$n" "$NOGREP/$n"; break; fi
  done
done

run() { # name env... -- cmd...
  local name=$1; shift
  local envargs=(); while [[ $1 != -- ]]; do envargs+=("$1"); shift; done; shift
  ( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 \
      "${envargs[@]}" timeout 900 bash "$GATE" "$@" ) >"$OUT/$name.out" 2>"$OUT/$name.err"
  echo "$?" >"$OUT/$name.rc"
}

runsimple() { # name pathenv... args
  local name=$1 path=$2; shift 2
  ( cd "$LANE" && env -i PATH="$path" HOME="$HOME" LANG=C.UTF-8 \
      timeout 900 bash "$GATE" "$@" ) >"$OUT/$name.out" 2>"$OUT/$name.err"
  echo "$?" >"$OUT/$name.rc"
}

echo "== E1 clean reference (default pin) =="
runsimple E1-clean "$CLEAN_PATH" verify-chain "$FIX" --root ..
echo "== E2 shim-first PATH =="
runsimple E2-shimpath "$SHIM_BIN:$CLEAN_PATH" verify-chain "$FIX" --root ..
echo "== E3 BASH_ENV function shim =="
( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 BASH_ENV="$S/bash_env.sh" \
    timeout 900 bash "$GATE" verify-chain "$FIX" --root .. ) >"$OUT/E3-bashenv.out" 2>"$OUT/E3-bashenv.err"
echo "$?" >"$OUT/E3-bashenv.rc"
echo "== E4 grep absent from PATH =="
runsimple E4-nogrep "$NOGREP" verify-chain "$FIX" --root ..
echo "== R1 refused override (relative path) =="
( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 RESEARCH_GATE_GREP=bin/grep \
    timeout 900 bash "$GATE" verify-chain "$FIX" --root .. ) >"$OUT/R1-override-relative.out" 2>"$OUT/R1-override-relative.err"
echo "$?" >"$OUT/R1-override-relative.rc"
echo "== R2 refused override (non-GNU stub) =="
cat >"$S/stub-grep" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;; esac
exit 0
EOF
chmod 755 "$S/stub-grep"
( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 RESEARCH_GATE_GREP="$S/stub-grep" \
    timeout 900 bash "$GATE" verify-chain "$FIX" --root .. ) >"$OUT/R2-override-nongnu.out" 2>"$OUT/R2-override-nongnu.err"
echo "$?" >"$OUT/R2-override-nongnu.rc"
echo "== W1 wrapper override (argv stamp) =="
( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 RESEARCH_GATE_GREP="$WRAP" CHOUSA_GREP_PIN_ECHO=1 \
    timeout 900 bash "$GATE" verify-chain "$FIX" --root .. ) >"$OUT/W1-wrapper.out" 2>"$OUT/W1-wrapper.err"
echo "$?" >"$OUT/W1-wrapper.rc"
echo "== W2 wrapper override on broken fixture (anchor-missing path) =="
( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME="$HOME" LANG=C.UTF-8 RESEARCH_GATE_GREP="$WRAP" CHOUSA_GREP_PIN_ECHO=1 \
    timeout 900 bash "$GATE" verify-chain "$BROKEN" --root .. ) >"$OUT/W2-wrapper-broken.out" 2>"$OUT/W2-wrapper-broken.err"
echo "$?" >"$OUT/W2-wrapper-broken.rc"

echo "== tripwire sizes =="
for t in "$TRIP_PATH" "$TRIP_FN" "$TRIP_WRAP"; do printf '%s %s\n' "$t" "$(stat -c%s "$t")"; done
echo "done"
