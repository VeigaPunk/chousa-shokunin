#!/usr/bin/env bash
# matrix.sh — byte-comparison of stdout and stderr SEPARATELY.
#   Axis A: gate variant (base | basepin | land) — same cwd, same env, same inputs.
#   Axis B: CHOUSA_GREP_PIN_ECHO (unset | 1) on the landed gate.
# The gate file is copied into ONE fixed path so SELF / printed paths match.
set -uo pipefail

SC=/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
FLEET=$SC/fleet
LANE=$FLEET/chousa-shokunin
GATE=$LANE/tools/research-gate.sh

REC=corpus/fixtures/full-r6.md
REC_BROKEN=corpus/fixtures/full-r6-broken.md
CLAIMS=corpus/fixtures/full-r6.claims.jsonl
INTEG=corpus/fixtures/integrity-r7.md
META=corpus/fixtures/metadata-r25/verified-at-below-heading.md

# run OUTDIR TAG GATEFILE ECHO(off|on) ARGS...
run() {
  local outdir=$1 tag=$2 gatefile=$3 echo_flag=$4; shift 4
  cp -f "$gatefile" "$GATE"
  local -a e=()
  [[ $echo_flag == on ]] && e=(CHOUSA_GREP_PIN_ECHO=1)
  ( cd "$LANE" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp \
      LANG=C.UTF-8 LC_ALL=C.UTF-8 CHOUSA_NOW_EPOCH=1761000000 \
      "${e[@]+"${e[@]}"}" bash tools/research-gate.sh "$@" ) \
      >"$outdir/$tag.out" 2>"$outdir/$tag.err"
  echo $? >"$outdir/$tag.rc"
}

MODE_ARGS=(
  "verify|verify|$REC"
  "verify-drift|verify|$REC_BROKEN"
  "claims|verify-claims|$CLAIMS"
  "chain|verify-chain|$REC"
  "sweeps|verify-sweeps|$REC"
  "integrity|verify-integrity|$INTEG"
  "metadata|verify-metadata|$META"
  "all|verify-all|$REC --claims $CLAIMS"
  "help|--help|"
  "usage-bad|--no-such-flag|"
  "usage-norec|verify|"
  "drift-missing|--drift|NONE"
)

# ---- Axis A: gate variants, echo OFF ---------------------------------------
A=$SC/outA; rm -rf "$A"; mkdir -p "$A"
for v in base basepin land; do
  for spec in "${MODE_ARGS[@]}"; do
    IFS='|' read -r name mode arg <<<"$spec"
    args=("$mode"); [[ -n $arg ]] && read -r -a args <<<"$mode $arg"
    [[ $name == drift-missing ]] && args=(--drift "$A/nonexistent-baseline.txt")
    run "$A" "$v.$name" "$SC/$v-gate.sh" off "${args[@]}" --root ..
  done
  # --pin / --drift need their own path handling (no --root)
  run "$A" "$v.pin" "$SC/$v-gate.sh" off --pin "$A/$v.baseline"
done
# self-drift: each variant against its own baseline
for v in base basepin land; do
  run "$A" "$v.drift-self" "$SC/$v-gate.sh" off --drift "$A/$v.baseline"
  # cross-drift: each variant against the LAND baseline
  run "$A" "$v.drift-vs-land" "$SC/$v-gate.sh" off --drift "$A/land.baseline"
done

# ---- Axis B: echo OFF vs ON, landed gate ---------------------------------
B=$SC/outB; rm -rf "$B"; mkdir -p "$B"
for spec in "${MODE_ARGS[@]}"; do
  IFS='|' read -r name mode arg <<<"$spec"
  args=("$mode"); [[ -n $arg ]] && read -r -a args <<<"$mode $arg"
  [[ $name == drift-missing ]] && args=(--drift "$B/nonexistent-baseline.txt")
  run "$B" "off.$name" "$SC/land-gate.sh" off "${args[@]}" --root ..
  run "$B" "on.$name"  "$SC/land-gate.sh" on  "${args[@]}" --root ..
done
run "$B" "off.pin" "$SC/land-gate.sh" off --pin "$B/off.baseline"
run "$B" "on.pin"  "$SC/land-gate.sh" on  --pin "$B/on.baseline"
# json manifest under both flags
run "$B" "off.json" "$SC/land-gate.sh" off verify-all "$REC" --claims "$CLAIMS" --root .. --json "$B/off.manifest.jsonl"
run "$B" "on.json"  "$SC/land-gate.sh" on  verify-all "$REC" --claims "$CLAIMS" --root .. --json "$B/on.manifest.jsonl"

cp -f "$SC/land-gate.sh" "$GATE"
echo "matrix done"
