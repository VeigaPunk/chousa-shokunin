#!/usr/bin/env bash
# RevGrepModesA matrix v2: modes verify / verify-claims under
# (a) PATH shim named grep first on PATH, (b) BASH_ENV logging grep() function,
# (c) RESEARCH_GATE_GREP=/usr/bin/grep with the shim on PATH.
# Layout: run/ = workspace dir; run/chousa-shokunin = physical clone at
# e87c5d7; run/research = copied workspace sources. Canonical invocation:
# cwd=run/chousa-shokunin, --root ..
R=/tmp/hyaku/chousa-r35/w2/RevGrepModesA
RUN=$R/run; OUT=$R/out; CLONE=$RUN/chousa-shokunin
GATE=tools/research-gate.sh
mkdir -p "$OUT" "$RUN/shim" "$RUN/emptybin" "$RUN/tmp"
chmod +x "$RUN/shim/grep"

norm() { sed -E 's/ts=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z/ts=TS/g' "$1"; }

run_gate() { # NAME MODE [env assignments...] -- gate args...
  local name=$1 mode=$2; shift 2
  local envp=() args=()
  while [[ ${1:-} != -- ]]; do envp+=("$1"); shift; done
  shift
  args=("$@")
  : > "$OUT/trip-$name.log"
  ( cd "$CLONE" && env -u BASH_ENV -u RESEARCH_GATE_GREP -u CHOUSA_GREP_PIN_ECHO \
      -u GREP_SHIM_LOG -u GREP_BASHENV_LOG -u CHOUSA_ROOT "${envp[@]}" \
      TMPDIR=$RUN/tmp timeout 300 bash "$GATE" "${args[@]}" \
      >"$OUT/$name.out" 2>"$OUT/$name.err" )
  local rc=$?
  echo "$rc" > "$OUT/$name.rc"
  printf '%-22s rc=%s tripwire_bytes=%s\n' "$name" "$rc" "$(wc -c < "$OUT/trip-$name.log")"
}

SHIMPATH="PATH=$RUN/shim:$PATH"
BENV="BASH_ENV=$RUN/bashenv.sh"

echo "== instrumentation controls (tripwire must log when interception happens) =="
: > "$OUT/trip-ctl-shim.log"
env -i PATH="$RUN/shim:/usr/bin:/bin" GREP_SHIM_LOG="$OUT/trip-ctl-shim.log" \
  bash -c 'grep --version >/dev/null'; echo "ctl-shim-direct rc=$? trip=$(wc -c < "$OUT/trip-ctl-shim.log")"
: > "$OUT/trip-ctl-bashenv.log"
env -i PATH=/usr/bin:/bin BASH_ENV="$RUN/bashenv.sh" GREP_BASHENV_LOG="$OUT/trip-ctl-bashenv.log" \
  bash -c 'grep --version >/dev/null'; echo "ctl-bashenv-direct rc=$? trip=$(wc -c < "$OUT/trip-ctl-bashenv.log")"

echo "== matrix =="
VERIFY_ARGS=(verify corpus/fixtures/full-r6.md --root ..)
CLAIMS_ARGS=(verify-claims corpus/fixtures/claims-r2.jsonl --root ..)
run_gate base-verify        verify  -- "${VERIFY_ARGS[@]}"
run_gate base-claims        verify-claims -- "${CLAIMS_ARGS[@]}"
run_gate a-shim-verify      verify  "$SHIMPATH" "GREP_SHIM_LOG=$OUT/trip-a-shim-verify.log" -- "${VERIFY_ARGS[@]}"
run_gate a-shim-claims      verify-claims "$SHIMPATH" "GREP_SHIM_LOG=$OUT/trip-a-shim-claims.log" -- "${CLAIMS_ARGS[@]}"
run_gate b-bashenv-verify   verify  "$BENV" "GREP_BASHENV_LOG=$OUT/trip-b-bashenv-verify.log" -- "${VERIFY_ARGS[@]}"
run_gate b-bashenv-claims   verify-claims "$BENV" "GREP_BASHENV_LOG=$OUT/trip-b-bashenv-claims.log" -- "${CLAIMS_ARGS[@]}"
run_gate c-override-verify  verify  "$SHIMPATH" "GREP_SHIM_LOG=$OUT/trip-c-override-verify.log" "RESEARCH_GATE_GREP=/usr/bin/grep" -- "${VERIFY_ARGS[@]}"
run_gate c-override-claims  verify-claims "$SHIMPATH" "GREP_SHIM_LOG=$OUT/trip-c-override-claims.log" "RESEARCH_GATE_GREP=/usr/bin/grep" -- "${CLAIMS_ARGS[@]}"
run_gate nogrep-verify      verify  "PATH=$RUN/emptybin" -- "${VERIFY_ARGS[@]}"
run_gate nogrep-claims      verify-claims "PATH=$RUN/emptybin" -- "${CLAIMS_ARGS[@]}"
run_gate ref-rel-claims     verify-claims "RESEARCH_GATE_GREP=shim/grep" -- "${CLAIMS_ARGS[@]}"
run_gate ref-nongnu-claims  verify-claims "RESEARCH_GATE_GREP=/bin/sh" -- "${CLAIMS_ARGS[@]}"

echo "== pin echo diagnostics (CHOUSA_GREP_PIN_ECHO=1, GATE_GREP on stderr) =="
run_gate e-a-verify   verify  "$SHIMPATH" "CHOUSA_GREP_PIN_ECHO=1" -- "${VERIFY_ARGS[@]}"
run_gate e-a-claims   verify-claims "$SHIMPATH" "CHOUSA_GREP_PIN_ECHO=1" -- "${CLAIMS_ARGS[@]}"
run_gate e-b-verify   verify  "$BENV" "CHOUSA_GREP_PIN_ECHO=1" -- "${VERIFY_ARGS[@]}"
run_gate e-b-claims   verify-claims "$BENV" "CHOUSA_GREP_PIN_ECHO=1" -- "${CLAIMS_ARGS[@]}"
run_gate e-c-verify   verify  "$SHIMPATH" "RESEARCH_GATE_GREP=/usr/bin/grep" "CHOUSA_GREP_PIN_ECHO=1" -- "${VERIFY_ARGS[@]}"
run_gate e-c-claims   verify-claims "$SHIMPATH" "RESEARCH_GATE_GREP=/usr/bin/grep" "CHOUSA_GREP_PIN_ECHO=1" -- "${CLAIMS_ARGS[@]}"
grep -H '^GATE_GREP:' "$OUT"/e-*.err || echo "(no GATE_GREP lines found)"

echo "== byte-for-byte comparison vs unshimmed baseline (ts= normalized; verdict line exact) =="
cmp_pair() { # BASE NAME
  local base=$1 name=$2 eq=UNKNOWN veq=UNKNOWN
  if diff <(norm "$OUT/$base.out") <(norm "$OUT/$name.out") >"$OUT/diff-$name.out" 2>&1 \
     && diff <(norm "$OUT/$base.err") <(norm "$OUT/$name.err") >"$OUT/diff-$name.err" 2>&1; then
    eq=YES
  else eq=NO; fi
  if [[ $(grep -h '^RESEARCH_GATE:' "$OUT/$base.out" "$OUT/$base.err") == \
        $(grep -h '^RESEARCH_GATE:' "$OUT/$name.out" "$OUT/$name.err") ]]; then veq=YES; else veq=NO; fi
  printf '%-22s bytes_eq=%s verdict_eq=%s rc=%s baseline_rc=%s\n' "$name" "$eq" "$veq" \
    "$(cat "$OUT/$name.rc")" "$(cat "$OUT/$base.rc")"
  [[ $eq == YES ]] || { echo "--- diff-$name.out ---"; head -20 "$OUT/diff-$name.out"; echo "--- diff-$name.err ---"; head -20 "$OUT/diff-$name.err"; }
}
cmp_pair base-verify a-shim-verify
cmp_pair base-verify b-bashenv-verify
cmp_pair base-verify c-override-verify
cmp_pair base-verify nogrep-verify
cmp_pair base-claims a-shim-claims
cmp_pair base-claims b-bashenv-claims
cmp_pair base-claims c-override-claims
cmp_pair base-claims nogrep-claims

echo "== verdict / refusal lines =="
for n in base-verify base-claims a-shim-verify a-shim-claims b-bashenv-verify b-bashenv-claims \
         c-override-verify c-override-claims nogrep-verify nogrep-claims ref-rel-claims ref-nongnu-claims; do
  v=$(grep -h '^RESEARCH_GATE:\|^research-gate: GREP_PROVENANCE' "$OUT/$n.out" "$OUT/$n.err" 2>/dev/null | head -1)
  printf '%-22s rc=%s | %s\n' "$n" "$(cat "$OUT/$n.rc")" "${v:-<no verdict line>}"
done
echo "== done =="
