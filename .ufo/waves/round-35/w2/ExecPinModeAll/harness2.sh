#!/usr/bin/env bash
# ExecPinModeAll harness pass 2: override+echo under shadow envs, masked manifest
# comparison, refusal-before-write proofs.
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeAll
LANE=$D/fleet/chousa-shokunin
GATE=$LANE/tools/research-gate.sh
MAN=$D/manifests
SHIM=$D/shim
LOGS=$D/logs
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
REC=corpus/fixtures/full-r6.md
EPOCH=1700000000
TRIP_PATH=$SHIM/trip-path.log
TRIP_FN=$SHIM/trip-fn.log

run2() { # NAME ENVASSIGN...
  local name=$1; shift
  local mf=$MAN/m-$name.jsonl
  rm -f "$mf"
  local out=$LOGS/$name.out err=$LOGS/$name.err
  : >"$TRIP_PATH"; : >"$TRIP_FN"
  ( cd "$LANE" && env -i PATH="$CLEAN_PATH" HOME=/root CHOUSA_NOW_EPOCH="$EPOCH" "$@" \
      bash "$GATE" verify-all "$REC" --root .. --json "$mf" ) >"$out" 2>"$err"
  local rc=$?
  local nlines=0
  [[ -f $mf ]] && nlines=$(grep -c '' -- "$mf" 2>/dev/null || echo 0)
  {
    echo "### env=$name"
    echo "exit=$rc  manifest_lines=$nlines  trip_path_bytes=$(wc -c <"$TRIP_PATH")  trip_fn_bytes=$(wc -c <"$TRIP_FN")"
    echo "-- VERIFY_ALL:"; grep '^VERIFY_ALL ' "$out" || echo "(none)"
    echo "-- GATE_GREP (stderr):"; grep '^GATE_GREP: ' "$err" || echo "(none)"
    echo "-- refusal:"; grep 'GREP_PROVENANCE' "$err" || echo "(none)"
    echo "-- stderr head:"; head -n 4 "$err"
  } >"$LOGS/$name.summary"
  cat "$LOGS/$name.summary"
}

echo "===== F1 override=/usr/bin/grep + PATH shim + echo ====="
run2 ovr-shim PATH="$SHIM/bin:$CLEAN_PATH" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1
echo; echo "===== F2 default + echo (clean PATH) ====="
run2 def-echo CHOUSA_GREP_PIN_ECHO=1
echo; echo "===== F3 BASH_ENV fn + override + echo ====="
run2 ovr-bashenv BASH_ENV="$SHIM/bash_env.sh" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1
echo; echo "===== F4 no-grep-on-PATH + override + echo ====="
run2 ovr-nogrep PATH="$D/nogrepfarm" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1

echo; echo "===== masked manifest comparison (ts masked) ====="
python3 - <<'PY'
import json,glob,os,re
D="/tmp/hyaku/chousa-r35/w2/ExecPinModeAll/manifests"
base=None
for f in sorted(glob.glob(D+"/m-*.jsonl")):
    b=open(f,'rb').read()
    if b"GREP_PROVENANCE" in b or b'pre-existing' in b: 
        print(os.path.basename(f),"SKIP (prefilled/refusal)"); continue
    m=re.sub(rb'"ts":"[^"]*"',b'"ts":"<MASK>"',b)
    if base is None:
        base=(os.path.basename(f),m)
        print(os.path.basename(f),"len",len(m),"sha256",__import__('hashlib').sha256(m).hexdigest())
    else:
        print(os.path.basename(f),"identical_to_clean" if m==base[1] else "DIFFERS",
              "sha256",__import__('hashlib').sha256(m).hexdigest())
PY
