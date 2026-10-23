#!/usr/bin/env bash
# Round-33 W1 no-harm battery, revision-bound header (repairs round-32 routed defect D3:
# ".ufo/waves/round-32/measure/final/battery.out has no gate_sha256/lane-rev header").
#
# Usage: battery.sh GATE OUTDIR
#   GATE    gate script to measure (base: <lane>/tools/research-gate.sh,
#           sha256 f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0)
#   OUTDIR  directory for one log per run, the selftest case-line list, counter
#           receipts and (when the caller redirects) this stdout transcript.
#
# First output is the header: lane revision, gate path + sha256, every counter path +
# sha256, fixture hashes, utc, hostname, seeds, battery-script hash. Then one row per
# run: command, exit code (with the expected code), wall time, log path + sha256 and the
# run's key lines. Comparator: .ufo/waves/round-32/measure/final/battery.out (claims
# 17/17 CLEAN, chain 17/22 CLEAN, broken chain 1/2 DRIFT, observable 3/3, counters
# 132/132). Exit 0 iff every asserted row matched.
#
# Control rule (round 33): this script never invokes corpus/evidence/round33/c1-count.py.
set -u

GATE=${1:?usage: battery.sh GATE OUTDIR}
OUTDIR=${2:?usage: battery.sh GATE OUTDIR}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/chousa-shokunin}
FLEET=${FLEET:-/home/vgpnk/Projects/shokunin}
SCRATCH=${SCRATCH:-/fast/scratch/hyaku/chousa-r33/w1/ExecNoHarmBase33}
SELFTEST_TIMEOUT=${SELFTEST_TIMEOUT:-1800}
RUN_TIMEOUT=${RUN_TIMEOUT:-900}
SEED_A=${SEED_A:-3601}
SEED_B=${SEED_B:-3602}
SEED_C=${SEED_C:-3611}
SEED_D=${SEED_D:-3612}
SEED_E=${SEED_E:-3621}
SEED_F=${SEED_F:-3622}

[ -f "$GATE" ] || { echo "battery: no such gate: $GATE" >&2; exit 2; }
mkdir -p "$OUTDIR" "$SCRATCH" || exit 2
OUTDIR=$(cd "$OUTDIR" && pwd) || exit 2
C1_TMP=${C1_TMP:-$SCRATCH/tmp}
C2_TMP=${C2_TMP:-$SCRATCH/tmp}
TMPDIR=${TMPDIR:-$SCRATCH/tmp}
export C1_TMP C2_TMP TMPDIR
mkdir -p "$C1_TMP" "$C2_TMP" "$TMPDIR" || exit 2
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

GATE_ABS=$(realpath "$GATE")
SELF=$(realpath "$0")
GATE_SHA=$(sha256sum "$GATE_ABS" | cut -d' ' -f1)
LANE_REV=$(git -C "$LANE" rev-parse master 2>/dev/null || echo unknown)
GATE_REPO=$(dirname "$(dirname "$GATE_ABS")")
GATE_REV=$(git -C "$GATE_REPO" rev-parse HEAD 2>/dev/null || echo unknown)
UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HOST=$(hostname -s 2>/dev/null || hostname)

printf '%s\n' "# round-33 W1 no-harm battery (D3 revision-bound header)"
printf 'lane=%s\n' "$LANE"
printf 'lane_revision=%s\n' "$LANE_REV"
printf 'gate=%s\n' "$GATE_ABS"
printf 'gate_sha256=%s\n' "$GATE_SHA"
printf 'gate_tree_revision=%s\n' "$GATE_REV"
C1V3_SHA=$(sha256sum "$LANE/corpus/evidence/round31/c1-count-v3.py" | cut -d' ' -f1)
C2V3_SHA=$(sha256sum "$LANE/corpus/evidence/round31/c2-count-v3.py" | cut -d' ' -f1)
C2V2_SHA=$(sha256sum "$LANE/corpus/evidence/round32/c2-count-v2.py" | cut -d' ' -f1)
for c in corpus/evidence/round31/c1-count-v3.py \
         corpus/evidence/round31/c2-count-v3.py \
         corpus/evidence/round32/c2-count-v2.py; do
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
printf 'seeds=r31-c1:%s,%s r31-c2:%s,%s r32-c2:%s,%s\n' \
  "$SEED_A" "$SEED_B" "$SEED_C" "$SEED_D" "$SEED_E" "$SEED_F"

fail=0
rows=0
P_CLAIMS='^VERDICT_BEARING_CLAIMS=|^RESEARCH_GATE:'
P_SELFTEST='^RESEARCH_GATE_SELFTEST:|^FAIL-case'
P_CHAIN='^RESOLVED_HOPS=|^RESEARCH_GATE:'
P_OBS='^VERDICT_BEARING_EXPORTS='
P_CNT='^LINE_BINDING_MATCH=|^REVISION_BINDING_MATCH=|^EXEMPT_AUDIT_MATCH=|^RECORD_CHECKS=|^predicate_holds=|^COUNTER_ERROR='

# row NAME EXPECTED_EXIT TIMEOUT WORKDIR KEY_PATTERN COMMAND...
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
  printf 'cmd='
  printf '%q ' "$@"
  printf '(cwd=%s timeout=%ss)\n' "$wd" "$tmo"
  printf 'exit=%s want=%s wall_ms=%s log=%s sha256=%s\n' "$rc" "$want" "$ms" "$log" "$sha"
  grep -E "$pat" "$log" | sed 's/^/  /' || true
  if [ "$rc" -ne "$want" ]; then
    printf 'ROW %s MISMATCH: exit %s != %s\n' "$name" "$rc" "$want"
    fail=$((fail + 1))
  fi
}

# has NAME LITERAL  — the named run's log must contain LITERAL (grep -F)
has() {
  if grep -qF -- "$2" "$OUTDIR/$1.log"; then
    printf 'CHECK %s ok: %s\n' "$1" "$2"
  else
    printf 'CHECK %s FAIL: missing %s\n' "$1" "$2"
    fail=$((fail + 1))
  fi
}

# receipt NAME JSON TOTAL EXPECTED_COUNTER_SHA
# predicate_holds is a receipt field, not stdout; assert it together with matched=total,
# an empty misses list and the exact gate sha this battery measured.
receipt() {
  local name=$1 j=$2 tot=$3 csha=$4
  printf 'receipt=%s\n' "$j"
  if ! python3 - "$name" "$j" "$tot" "$csha" "$GATE_SHA" <<'PY'
import json, sys
name, path, total, csha, gsha = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
try:
    r = json.load(open(path))
except Exception as e:
    print("RECEIPT %s FAIL: unreadable (%r)" % (name, e))
    sys.exit(1)
ok = (r.get("predicate_holds") is True
      and r.get("matched") == total and r.get("total") == total
      and not r.get("misses") and not r.get("record_fails")
      and r.get("gate_timed_out") is False
      and r.get("gate_sha256") == gsha
      and r.get("counter_sha256") == csha)
print("RECEIPT %s %s predicate_holds=%s matched=%s/%s gate_sha256=%s counter_sha256=%s" % (
    name, "ok" if ok else "FAIL", r.get("predicate_holds"), r.get("matched"),
    r.get("total"), str(r.get("gate_sha256"))[:12], str(r.get("counter_sha256"))[:12]))
sys.exit(0 if ok else 1)
PY
  then
    fail=$((fail + 1))
  fi
}

# --- selftest: PASS count + case-line list + its sha256 -------------------------
row selftest 0 "$SELFTEST_TIMEOUT" "$LANE" "$P_SELFTEST" bash "$GATE_ABS" --selftest
grep -E '^(ok-case|FAIL-case)' "$OUTDIR/selftest.log" >"$OUTDIR/selftest.cases"
CASES=$(wc -l <"$OUTDIR/selftest.cases")
printf 'SELFTEST_CASES=%s cases_sha256=%s file=%s\n' \
  "$CASES" "$(sha256sum "$OUTDIR/selftest.cases" | cut -d' ' -f1)" "$OUTDIR/selftest.cases"
printf 'SELFTEST_FAIL_LINES=%s\n' "$(grep -c '^FAIL-case' "$OUTDIR/selftest.log" || true)"
has selftest 'RESEARCH_GATE_SELFTEST: PASS'

# --- claim and chain fixtures ---------------------------------------------------
# Assigned invocation: lane root. Its sources are fleet-root-relative, so at base this
# refuses all 17 claims with CLAIM_SOURCE_OUT_OF_CORPUS (round-32 ExecNoHarmBase32
# recorded the same root-convention artifact: 0/17, exit 1). The base fingerprint is
# asserted so a candidate that changes this path is surfaced, not silently accepted; it
# is not a correctness bar.
row claims-lane-root 1 "$RUN_TIMEOUT" "$LANE" "$P_CLAIMS" \
  bash "$GATE_ABS" verify-claims corpus/fixtures/claims-r2.jsonl --root .
# Round-32-comparable invocation (battery.out was measured this way).
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

# --- round-1 observable, extracted from SCORECARD.md ## Planned ------------------
OBS=$(awk '/^## Planned[[:space:]]*$/{seen=1} seen && /^```bash/{blk=1; next} blk && /^```/{exit} blk' \
  "$LANE/SCORECARD.md")
[ -n "$OBS" ] || { echo "battery: no round-1 observable block under ## Planned" >&2; exit 2; }
printf '\nobservable_source=%s ## Planned (bash block)\nobservable_cmd=%s\n' "$LANE/SCORECARD.md" "$OBS"
row observable 0 "$RUN_TIMEOUT" "$LANE" "$P_OBS" bash -c "$OBS"
has observable 'VERDICT_BEARING_EXPORTS=3/3'

# --- frozen counters from rounds 31/32 (never the round-33 counter) --------------
row r31-c1-v3-a 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c1-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_A" \
  --receipt "$OUTDIR/r31-c1-v3-a.json"
has r31-c1-v3-a 'LINE_BINDING_MATCH=132/132'
receipt r31-c1-v3-a "$OUTDIR/r31-c1-v3-a.json" 132 "$C1V3_SHA"
row r31-c1-v3-b 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c1-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_B" \
  --receipt "$OUTDIR/r31-c1-v3-b.json"
has r31-c1-v3-b 'LINE_BINDING_MATCH=132/132'
receipt r31-c1-v3-b "$OUTDIR/r31-c1-v3-b.json" 132 "$C1V3_SHA"

row r31-c2-v3-a 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c2-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_C" \
  --receipt "$OUTDIR/r31-c2-v3-a.json"
has r31-c2-v3-a 'REVISION_BINDING_MATCH=132/132'
receipt r31-c2-v3-a "$OUTDIR/r31-c2-v3-a.json" 132 "$C2V3_SHA"
row r31-c2-v3-b 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round31/c2-count-v3.py" --gate "$GATE_ABS" --seed "$SEED_D" \
  --receipt "$OUTDIR/r31-c2-v3-b.json"
has r31-c2-v3-b 'REVISION_BINDING_MATCH=132/132'
receipt r31-c2-v3-b "$OUTDIR/r31-c2-v3-b.json" 132 "$C2V3_SHA"

row r32-c2-v2-a 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round32/c2-count-v2.py" --gate "$GATE_ABS" --seed "$SEED_E" \
  --receipt "$OUTDIR/r32-c2-v2-a.json"
has r32-c2-v2-a 'EXEMPT_AUDIT_MATCH=132/132'
has r32-c2-v2-a 'RECORD_CHECKS=ok'
receipt r32-c2-v2-a "$OUTDIR/r32-c2-v2-a.json" 132 "$C2V2_SHA"
row r32-c2-v2-b 0 "$RUN_TIMEOUT" "$LANE" "$P_CNT" \
  python3 "$LANE/corpus/evidence/round32/c2-count-v2.py" --gate "$GATE_ABS" --seed "$SEED_F" \
  --receipt "$OUTDIR/r32-c2-v2-b.json"
has r32-c2-v2-b 'EXEMPT_AUDIT_MATCH=132/132'
has r32-c2-v2-b 'RECORD_CHECKS=ok'
receipt r32-c2-v2-b "$OUTDIR/r32-c2-v2-b.json" 132 "$C2V2_SHA"

printf '\nROWS=%s\n' "$rows"
if [ "$fail" -eq 0 ]; then
  printf 'BATTERY_RESULT=PASS\n'
  exit 0
fi
printf 'BATTERY_RESULT=FAIL mismatches=%s\n' "$fail"
exit 1
