#!/usr/bin/env bash
# ExecPinModeAll harness pass 3: run the SAME battery against BOTH gate
# revisions (wave-base 1f2fb4f5 and current landed a4768851).
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeAll
SHIM=$D/shim
LOGS=$D/logs3
MAN=$D/manifests3
mkdir -p "$LOGS" "$MAN"
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
REC=corpus/fixtures/full-r6.md
EPOCH=1700000000
TRIP_PATH=$SHIM/trip-path.log
TRIP_FN=$SHIM/trip-fn.log
TRIP_HOSTILE=$SHIM/trip-hostile.log

# gates: name -> lane dir
declare -A LANES=(
  [base]=$(ls -d $D/fleet/chousa-shokunin)
)

run_env() { # LANEDIR NAME ENVASSIGN...
  local LANE=$1 name=$2; shift 2
  local GATE=$LANE/tools/research-gate.sh
  local mf=$MAN/m-$name.jsonl
  rm -f "$mf"
  local out=$LOGS/$name.out err=$LOGS/$name.err
  : >"$TRIP_PATH"; : >"$TRIP_FN"; : >"$TRIP_HOSTILE"
  ( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME=/root CHOUSA_NOW_EPOCH="$EPOCH" "$@" \
      bash "$GATE" verify-all "$REC" --root .. --json "$mf" ) >"$out" 2>"$err"
  local rc=$?
  local nlines=0
  [[ -f $mf ]] && nlines=$(grep -c '' -- "$mf" 2>/dev/null || echo 0)
  {
    echo "### gate=$(sha256sum "$GATE" | cut -c1-16) env=$name"
    echo "exit=$rc manifest_lines=$nlines trip_path=$(wc -c <"$TRIP_PATH") trip_fn=$(wc -c <"$TRIP_FN") trip_hostile=$(wc -c <"$TRIP_HOSTILE")"
    echo "-- VERIFY_ALL:"; grep '^VERIFY_ALL ' "$out" || echo "(none)"
    echo "-- GATE_GREP:"; grep '^GATE_GREP: ' "$err" || echo "(none)"
    echo "-- refusal:"; grep 'GREP_PROVENANCE' "$err" || echo "(none)"
    echo "-- stderr head:"; head -n 3 "$err"
  } >"$LOGS/$name.summary"
}

for G in "$D/fleet/chousa-shokunin" "$D/fleet2/chousa-shokunin"; do
  [[ -d $G ]] || continue
  tag=$(basename $(dirname "$G"))-$(sha256sum $G/tools/research-gate.sh | cut -c1-8)
  echo "########## GATE $G ($(sha256sum $G/tools/research-gate.sh | cut -c1-16))"
  run_env $G ${tag}-clean
  run_env $G ${tag}-shimpath PATH="$SHIM/bin:$CLEAN_PATH"
  run_env $G ${tag}-bashenv BASH_ENV="$SHIM/bash_env.sh"
  run_env $G ${tag}-nogrep PATH="$D/nogrepfarm"
  run_env $G ${tag}-hostile PATH="$SHIM/hostile:$CLEAN_PATH"
  run_env $G ${tag}-ovr-echo PATH="$SHIM/bin:$CLEAN_PATH" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1
  run_env $G ${tag}-refuse-rel RESEARCH_GATE_GREP=bin/grep
  run_env $G ${tag}-refuse-missing RESEARCH_GATE_GREP=/nonexistent/grep
  run_env $G ${tag}-refuse-nongnu RESEARCH_GATE_GREP="$SHIM/stub-grep"
  run_env $G ${tag}-hostile-pin RESEARCH_GATE_GREP="$SHIM/hostile/grep-gnu"
  for s in "$LOGS/${tag}-"*.summary; do echo; cat "$s"; done
  echo
done
