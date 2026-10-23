#!/usr/bin/env bash
# Round-35 W2 no-harm battery (ExecNoHarm), adapted from
# .ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh (read-only source).
# Differences from r34: gate is the round-35 landed gate in a scratch clone at
# e87c5d7ea2dbf3730b36a3961de3f06261d015e4; the round-1 observable runs in a
# mimic fleet root (obsroot) because the clone has no ../research sibling; the
# round-34 C2 counter (round34/c2-count.py, DEADZONE_MATCH) is added as a row;
# r31 v1 counters are run in addition to v3.
#
# Usage: battery.sh GATE LANE_DIR OUTDIR FLEET_ROOT [OBS_CWD]
# OBS_CWD: directory that contains tools/research-gate.sh and whose parent holds
# research/ (the round-1 observable runs `bash tools/research-gate.sh verify
# ../research/... --root ..`).  Defaults to $FLEET/chousa-shokunin.
set -u

GATE=${1:?usage: battery.sh GATE LANE_DIR OUTDIR FLEET_ROOT [OBS_CWD]}
LANE=${2:?}
OUTDIR=${3:?}
FLEET=${4:?}
OBS_CWD=${5:-$FLEET/chousa-shokunin}
SELFTEST_TIMEOUT=${SELFTEST_TIMEOUT:-1800}
RUN_TIMEOUT=${RUN_TIMEOUT:-900}
SEED_A=${SEED_A:-3901}   # r31 c1-count-v3
SEED_B=${SEED_B:-3902}   # r31 c2-count-v3
SEED_C=${SEED_C:-3903}   # r32 c2-count-v2
SEED_D=${SEED_D:-3904}   # r33 c1-count-v2
SEED_E=${SEED_E:-3905}   # r32 c2-count-v3
SEED_F=${SEED_F:-3906}   # r34 c2-count (dead zone)
SEED_G=${SEED_G:-3907}   # r31 c1-count (v1)
SEED_H=${SEED_H:-3908}   # r31 c2-count (v1)

[ -f "$GATE" ] || { echo "battery: no such gate: $GATE" >&2; exit 2; }
mkdir -p "$OUTDIR" || exit 2
OUTDIR=$(cd "$OUTDIR" && pwd) || exit 2
SCRATCH=${SCRATCH:-/tmp/hyaku/chousa-r35/w2/ExecNoHarm/tmp}
C1_TMP=${C1_TMP:-$SCRATCH/tmp}; C2_TMP=${C2_TMP:-$SCRATCH/tmp}; TMPDIR=${TMPDIR:-$SCRATCH/tmp}
export C1_TMP C2_TMP TMPDIR
mkdir -p "$C1_TMP" "$C2_TMP" "$TMPDIR" || exit 2
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

GATE_ABS=$(realpath "$GATE")
SELF=$(realpath "$0")
GATE_SHA=$(sha256sum "$GATE_ABS" | cut -d' ' -f1)
LANE_REV=$(git -C "$LANE" rev-parse HEAD 2>/dev/null || echo unknown)
UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HOST=$(hostname -s 2>/dev/null || hostname)

printf '%s\n' "# round-35 W2 no-harm battery (ExecNoHarm)"
printf 'lane_clone=%s\n' "$LANE"
printf 'lane_clone_revision=%s\n' "$LANE_REV"
printf 'gate=%s\n' "$GATE_ABS"
printf 'gate_sha256=%s\n' "$GATE_SHA"
printf 'fleet_root=%s\n' "$FLEET"
for c in corpus/evidence/round31/c1-count-v3.py \
         corpus/evidence/round31/c2-count-v3.py \
         corpus/evidence/round31/c1-count.py \
         corpus/evidence/round31/c2-count.py \
         corpus/evidence/round32/c2-count-v2.py \
         corpus/evidence/round33/c1-count-v2.py \
         corpus/evidence/round32/c2-count-v3.py \
         corpus/evidence/round34/c2-count.py; do
  printf 'counter=%s sha256=%s\n' "$LANE/$c" "$(sha256sum "$LANE/$c" | cut -d' ' -f1)"
done
for f in corpus/fixtures/claims-r2.jsonl \
         corpus/fixtures/chain-r3.md \
         corpus/fixtures/chain-r3-broken.md; do
  printf 'fixture=%s sha256=%s\n' "$LANE/$f" "$(sha256sum "$LANE/$f" | cut -d' ' -f1)"
done
printf 'battery_script=%s sha256=%s\n' "$SELF" "$(sha256sum "$SELF" | cut -d' ' -f1)"
printf 'utc=%s\n' "$UTC"
printf 'hostname=%s\n' "$HOST"
printf 'scratch=%s\n' "$SCRATCH"
printf 'seeds=r31-c1-v3:%s r31-c2-v3:%s r32-c2-v2:%s r33-c1-v2:%s r32-c2-v3:%s r34-c2:%s r31-c1-v1:%s r31-c2-v1:%s\n' \
  "$SEED_A" "$SEED_B" "$SEED_C" "$SEED_D" "$SEED_E" "$SEED_F" "$SEED_G" "$SEED_H"

fail=0; rows=0
P_CLAIMS='^VERDICT_BEARING_CLAIMS=|^RESEARCH_GATE:'
P_SELFTEST='^RESEARCH_GATE_SELFTEST:|^FAIL-case'
P_CHAIN='^RESOLVED_HOPS=|^RESEARCH_GATE:'
P_OBS='^VERDICT_BEARING_EXPORTS='
P_CNT='^LINE_BINDING_MATCH=|^REVISION_BINDING_MATCH=|^EXEMPT_AUDIT_MATCH=|^RECORD_CHECKS=|^predicate_holds=|^COUNTER_ERROR=|^TOPLEVEL_FIELD_MATCH=|^COUNTER |^DEADZONE_MATCH='

row() {
  local name=$1 want=$2 tmo=$3 wd=$4 pat=$5 log t0 t1 rc ms sha
  shift 5
  log=$OUTDIR/$name.log
  t0=$(date +%s%N)
  ( cd "$wd" && timeout -k 5 "$tmo" "$@" ) >"$log" 2>&1
  rc=$?
  t1=$(date +%s%N)
  ms=$(( (t1 - t0) / 1000000 ))
  sha=$(sha256sum "$log" | cut -d' ' -f1)
  rows=$((rows + 1))
  printf '\n=== RUN %s\n' "$name"
  printf 'cmd='; printf '%q ' "$@"; printf '(cwd=%s timeout=%ss)\n' "$wd" "$tmo"
  printf 'exit=%s want=%s wall_ms=%s log=%s sha256=%s\n' "$rc" "$want" "$ms" "$log" "$sha"
  grep -E "$pat" "$log" | sed 's/^/  /' || true
  if [ "$rc" -ne "$want" ]; then
    printf 'ROW %s MISMATCH: exit %s != %s\n' "$name" "$rc" "$want"
    fail=$((fail + 1))
  fi
}

has() {
  if grep -qF -- "$2" "$OUTDIR/$1.log"; then
    printf 'CHECK %s ok: %s\n' "$1" "$2"
  else
    printf 'CHECK %s FAIL: missing %s\n' "$1" "$2"
    fail=$((fail + 1))
  fi
}

receipt() {
  local name=$1 j=$2 tot=$3 csha=$4
  printf 'receipt=%s\n' "$j"
  if ! python3 - "$name" "$j" "$tot" "$csha" "$GATE_SHA" <<'PY'
import json, sys
name, path, tot, csha, gsha = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
try:
    d = json.load(open(path))
except Exception as e:
    print("RECEIPT %s FAIL: unreadable %r" % (name, e)); sys.exit(1)
ok = True
def chk(cond, msg):
    global ok
    if not cond:
        print("RECEIPT %s FAIL: %s" % (name, msg)); ok = False
chk(d.get("predicate_holds") is True, "predicate_holds != true")
chk(d.get("matched") == tot, "matched=%r != %d" % (d.get("matched"), tot))
chk(d.get("total") == tot, "total=%r != %d" % (d.get("total"), tot))
chk(d.get("misses") == [] or d.get("misses") == {}, "misses not empty: %r" % (d.get("misses"),))
chk(str(d.get("gate_sha256", "")).startswith(gsha[:12]), "gate_sha256=%r != %s" % (d.get("gate_sha256"), gsha))
chk(str(d.get("counter_sha256", "")).startswith(csha[:12]), "counter_sha256=%r != %s" % (d.get("counter_sha256"), csha))
sys.exit(0 if ok else 1)
PY
  then
    fail=$((fail + 1))
  else
    printf 'RECEIPT %s ok\n' "$name"
  fi
}

# --- selftest ------------------------------------------------------------------
row selftest 0 "$SELFTEST_TIMEOUT" "$LANE" "$P_SELFTEST" bash "$GATE_ABS" --selftest
grep -E '^(ok-case|FAIL-case)' "$OUTDIR/selftest.log" >"$OUTDIR/selftest.cases"
CASES=$(wc -l <"$OUTDIR/selftest.cases")
printf 'SELFTEST_CASES=%s cases_sha256=%s file=%s\n' \
  "$CASES" "$(sha256sum "$OUTDIR/selftest.cases" | cut -d' ' -f1)" "$OUTDIR/selftest.cases"
printf 'SELFTEST_FAIL_LINES=%s\n' "$(grep -c '^FAIL-case' "$OUTDIR/selftest.log" || true)"
has selftest 'RESEARCH_GATE_SELFTEST: PASS'

# --- claims / chain fixtures ---------------------------------------------------
row claims-lane-root 1 "$RUN_TIMEOUT" "$LANE" "$P_CLAIMS" \
  bash "$GATE_ABS" verify-claims corpus/fixtures/claims-r2.jsonl --root .
row claims-fleet-root 0 "$RUN_TIMEOUT" "$LANE" "$P_CLAIMS" \
  bash "$GATE_ABS" verify-claims corpus/fixtures/claims-r2.jsonl --root "$FLEET"
has claims-fleet-root 'VERDICT_BEARING_CLAIMS=17/17'
has claims-fleet-root 'RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2'

row chain-r3 0 "$RUN_TIMEOUT" "$LANE" "$P_CHAIN" \
  bash "$GATE_ABS" verify-chain corpus/fixtures/chain-r3.md --root "$FLEET"
has chain-r3 'RESOLVED_HOPS=17/22'
has chain-r3 'RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5'

row chain-r3-broken 1 "$RUN_TIMEOUT" "$LANE" "$P_CHAIN" \
  bash "$GATE_ABS" verify-chain corpus/fixtures/chain-r3-broken.md --root "$FLEET"
has chain-r3-broken 'RESOLVED_HOPS=1/2'
has chain-r3-broken 'RESEARCH_GATE: DRIFT (hops=2 verified=1'

# --- round-1 observable (SCORECARD.md ## Planned bash block) --------------------
OBS=$(awk '/^## Planned[[:space:]]*$/{seen=1} seen && /^```bash/{blk=1; next} blk && /^```/{exit} blk' \
  "$LANE/SCORECARD.md")
[ -n "$OBS" ] || { echo "battery: no round-1 observable block under ## Planned" >&2; exit 2; }
printf '\nobservable_source=%s ## Planned (bash block)\nobservable_cmd=%s\n' "$LANE/SCORECARD.md" "$OBS"
row observable 0 "$RUN_TIMEOUT" "$OBS_CWD" "$P_OBS" bash -c "$OBS"
has observable 'VERDICT_BEARING_EXPORTS=3/3'

# --- frozen counters from rounds 31/32/33/34 ------------------------------------
row r31-c1-v3 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c1-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_A" \
  --receipt "$OUTDIR/r31-c1-v3.json"
has r31-c1-v3 'LINE_BINDING_MATCH=132/132'
receipt r31-c1-v3 "$OUTDIR/r31-c1-v3.json" 132 "$(sha256sum "$LANE/corpus/evidence/round31/c1-count-v3.py" | cut -d' ' -f1)"

row r31-c2-v3 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c2-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_B" \
  --receipt "$OUTDIR/r31-c2-v3.json"
has r31-c2-v3 'REVISION_BINDING_MATCH=132/132'
receipt r31-c2-v3 "$OUTDIR/r31-c2-v3.json" 132 "$(sha256sum "$LANE/corpus/evidence/round31/c2-count-v3.py" | cut -d' ' -f1)"

row r32-c2-v2 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round32/c2-count-v2.py" --gate "$GATE_ABS" --seed "$SEED_C" \
  --receipt "$OUTDIR/r32-c2-v2.json"
has r32-c2-v2 'EXEMPT_AUDIT_MATCH=132/132'
has r32-c2-v2 'RECORD_CHECKS=ok'
receipt r32-c2-v2 "$OUTDIR/r32-c2-v2.json" 132 "$(sha256sum "$LANE/corpus/evidence/round32/c2-count-v2.py" | cut -d' ' -f1)"

row r33-c1-v2 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round33/c1-count-v2.py" --gate "$GATE_ABS" --seed "$SEED_D" \
  --receipt "$OUTDIR/r33-c1-v2.json"
has r33-c1-v2 'TOPLEVEL_FIELD_MATCH=156/156'
receipt r33-c1-v2 "$OUTDIR/r33-c1-v2.json" 156 "$(sha256sum "$LANE/corpus/evidence/round33/c1-count-v2.py" | cut -d' ' -f1)"

row r32-c2-v3 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round32/c2-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_E" \
  --receipt "$OUTDIR/r32-c2-v3.json"
has r32-c2-v3 'EXEMPT_AUDIT_MATCH=132/132'
has r32-c2-v3 'RECORD_CHECKS=ok'
receipt r32-c2-v3 "$OUTDIR/r32-c2-v3.json" 132 "$(sha256sum "$LANE/corpus/evidence/round32/c2-count-v3.py" | cut -d' ' -f1)"

row r34-c2 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round34/c2-count.py" --gate "$GATE_ABS" --seed "$SEED_F" \
  --receipt "$OUTDIR/r34-c2.json"
has r34-c2 'DEADZONE_MATCH=37/37'
receipt r34-c2 "$OUTDIR/r34-c2.json" 37 "$(sha256sum "$LANE/corpus/evidence/round34/c2-count.py" | cut -d' ' -f1)"

row r31-c1-v1 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c1-count.py" --gate "$GATE_ABS" --seed "$SEED_G" \
  --receipt "$OUTDIR/r31-c1-v1.json"
has r31-c1-v1 'LINE_BINDING_MATCH=120/120'
receipt r31-c1-v1 "$OUTDIR/r31-c1-v1.json" 120 "$(sha256sum "$LANE/corpus/evidence/round31/c1-count.py" | cut -d' ' -f1)"

row r31-c2-v1 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c2-count.py" --gate "$GATE_ABS" --seed "$SEED_H" \
  --receipt "$OUTDIR/r31-c2-v1.json"
has r31-c2-v1 'REVISION_BINDING_MATCH=120/120'
receipt r31-c2-v1 "$OUTDIR/r31-c2-v1.json" 120 "$(sha256sum "$LANE/corpus/evidence/round31/c2-count.py" | cut -d' ' -f1)"

printf '\nROWS=%s\n' "$rows"
if [ "$fail" -eq 0 ]; then
  printf 'BATTERY_RESULT=PASS\n'
  exit 0
fi
printf 'BATTERY_RESULT=FAIL mismatches=%s\n' "$fail"
exit 1
