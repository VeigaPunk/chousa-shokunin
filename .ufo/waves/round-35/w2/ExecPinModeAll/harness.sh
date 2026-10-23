#!/usr/bin/env bash
# ExecPinModeAll harness — verify-all --json under the grep pin.
# Shadow environments + refusal checks. All artifacts under this directory.
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeAll
LANE=$D/fleet/chousa-shokunin
GATE=$LANE/tools/research-gate.sh
MAN=$D/manifests
SHIM=$D/shim
LOGS=$D/logs
mkdir -p "$MAN" "$SHIM" "$LOGS"

CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
REC=corpus/fixtures/full-r6.md
EPOCH=1700000000

# --- farm without any grep --------------------------------------------------
FARM=$D/nogrepfarm
if [[ ! -d $FARM ]]; then
  mkdir -p "$FARM"
  for p in /usr/bin/*; do
    b=${p##*/}
    case "$b" in grep|egrep|fgrep) continue;; esac
    [[ -x $p ]] || continue
    ln -sf "$p" "$FARM/$b"
  done
fi

# --- shims ------------------------------------------------------------------
TRIP_PATH=$SHIM/trip-path.log
TRIP_FN=$SHIM/trip-fn.log
TRIP_HOSTILE=$SHIM/trip-hostile.log
: >"$TRIP_PATH"; : >"$TRIP_FN"; : >"$TRIP_HOSTILE"

SHIMDIR=$SHIM/bin; mkdir -p "$SHIMDIR"
cat >"$SHIMDIR/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP_PATH" 2>/dev/null
exec /usr/bin/grep "\$@"
EOF
chmod 755 "$SHIMDIR/grep"

HOSTILE=$SHIM/hostile; mkdir -p "$HOSTILE"
cat >"$HOSTILE/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP_HOSTILE" 2>/dev/null
exit 1
EOF
chmod 755 "$HOSTILE/grep"

BASHENV=$SHIM/bash_env.sh
cat >"$BASHENV" <<EOF
grep() { printf 'fn %s\n' "\$*" >>"$TRIP_FN" 2>/dev/null; command /usr/bin/grep "\$@"; }
EOF

# a manifest that already carries one line, for the refusal-no-append check
PRE=$MAN/prefilled.jsonl
printf '{"schema":"chousa-verify-all/v1","ts":"pre-existing"}\n' >"$PRE"

run_env() { # NAME [--preexisting FILE] ENVASSIGN...
  local name=$1; shift
  local pre=''
  if [[ ${1:-} == --preexisting ]]; then pre=$2; shift 2; fi
  local mf=$MAN/m-$name.jsonl
  rm -f "$mf"
  if [[ -n $pre ]]; then cp "$pre" "$mf"; fi
  local out=$LOGS/$name.out err=$LOGS/$name.err
  : >"$TRIP_PATH"; : >"$TRIP_FN"; : >"$TRIP_HOSTILE"
  ( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME=/root \
      CHOUSA_NOW_EPOCH="$EPOCH" "$@" \
      bash "$GATE" verify-all "$REC" --root .. --json "$mf" ) >"$out" 2>"$err"
  local rc=$?
  local exists=no nlines=0
  if [[ -f $mf ]]; then exists=yes; nlines=$(grep -c '' -- "$mf" 2>/dev/null || echo 0); fi
  {
    echo "### env=$name"
    echo "exit=$rc"
    echo "manifest_exists=$exists manifest_lines=$nlines"
    echo "trip_path_bytes=$(wc -c <"$TRIP_PATH")"
    echo "trip_fn_bytes=$(wc -c <"$TRIP_FN")"
    echo "trip_hostile_bytes=$(wc -c <"$TRIP_HOSTILE")"
    echo "-- VERIFY_ALL line(s):"
    grep '^VERIFY_ALL ' "$out" || echo "(none)"
    echo "-- RESEARCH_GATE line:"
    grep '^RESEARCH_GATE: ' "$out" || echo "(none)"
    echo "-- GATE_GREP line (stderr):"
    grep '^GATE_GREP: ' "$err" || echo "(none)"
    echo "-- refusal marker (stderr):"
    grep 'GREP_PROVENANCE' "$err" || echo "(none)"
    echo "-- stderr (whole, first 6 lines):"
    head -n 6 "$err"
  } >"$LOGS/$name.summary"
  cat "$LOGS/$name.summary"
}

echo "===== E1 clean ====="
run_env clean
echo; echo "===== E2 shim-first PATH (faithful shim) ====="
run_env shim-path PATH="$SHIMDIR:$CLEAN_PATH"
echo; echo "===== E3 BASH_ENV grep() function ====="
run_env bashenv BASH_ENV="$BASHENV"
echo; echo "===== E4 no grep on PATH ====="
run_env nogrep PATH="$FARM"
echo; echo "===== E5 hostile PATH shim (never matches) ====="
run_env hostile PATH="$HOSTILE:$CLEAN_PATH"
echo; echo "===== E6 refusal: relative override ====="
run_env refuse-relative RESEARCH_GATE_GREP=bin/grep
echo; echo "===== E7 refusal: missing override, manifest already has 1 line ====="
run_env refuse-missing --preexisting "$PRE" RESEARCH_GATE_GREP=/nonexistent/grep
echo; echo "===== E8 refusal: non-GNU override ====="
run_env refuse-nongnu RESEARCH_GATE_GREP="$SHIM/stub-grep"
