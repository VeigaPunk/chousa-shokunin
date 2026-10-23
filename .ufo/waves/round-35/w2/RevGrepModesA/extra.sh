#!/usr/bin/env bash
# RevGrepModesA follow-ups: honest no-grep PATH, shim as pin override,
# readonly-function BASH_ENV trap, raw-diff evidence, artifact manifest.
R=/tmp/hyaku/chousa-r35/w2/RevGrepModesA
RUN=$R/run; OUT=$R/out; CLONE=$RUN/chousa-shokunin
GATE=tools/research-gate.sh
mkdir -p "$OUT" "$RUN/nogrepbin" "$RUN/tmp"

# nogrepbin: every /usr/bin entry EXCEPT grep-like names, symlinked
for f in /usr/bin/*; do
  b=${f##*/}
  case $b in *grep*) ;; *) ln -sfn "$f" "$RUN/nogrepbin/$b" ;; esac
done
ls "$RUN/nogrepbin" | grep -c . ; ls "$RUN/nogrepbin" | grep grep && echo "GREP PRESENT (bad)" || echo "nogrepbin: no grep entries"

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

VERIFY_ARGS=(verify corpus/fixtures/full-r6.md --root ..)
CLAIMS_ARGS=(verify-claims corpus/fixtures/claims-r2.jsonl --root ..)
SHIMPATH="PATH=$RUN/shim:$PATH"

echo "== honest no-grep PATH (coreutils present, zero grep entries) =="
run_gate nogrep2-verify verify  "PATH=$RUN/nogrepbin" -- "${VERIFY_ARGS[@]}"
run_gate nogrep2-claims verify-claims "PATH=$RUN/nogrepbin" -- "${CLAIMS_ARGS[@]}"
head -2 "$OUT/nogrep2-verify.out"; head -3 "$OUT/nogrep2-claims.out" | tail -1

echo "== shim itself as the pin override (self-reported provenance limit) =="
run_gate pinshim-verify verify  "PATH=$RUN/nogrepbin" "GREP_SHIM_LOG=$OUT/trip-pinshim-verify.log" "RESEARCH_GATE_GREP=$RUN/shim/grep" "CHOUSA_GREP_PIN_ECHO=1" -- "${VERIFY_ARGS[@]}"
run_gate pinshim-claims verify-claims "PATH=$RUN/nogrepbin" "GREP_SHIM_LOG=$OUT/trip-pinshim-claims.log" "RESEARCH_GATE_GREP=$RUN/shim/grep" "CHOUSA_GREP_PIN_ECHO=1" -- "${CLAIMS_ARGS[@]}"
grep -H '^GATE_GREP:' "$OUT"/pinshim-*.err
echo "pinshim byte-eq (claims vs base):"
diff <(norm "$OUT/base-claims.out") <(norm "$OUT/pinshim-claims.out") && echo "  stdout byte-equal (ts-normalized)"
diff <(norm "$OUT/base-claims.err") <(norm "$OUT/pinshim-claims.err" ) >/dev/null 2>&1 && echo "  stderr byte-equal" || diff <(norm "$OUT/base-claims.err") <(norm "$OUT/pinshim-claims.err") | head -4

echo "== readonly -f grep BASH_ENV trap =="
run_gate b-readonly-verify verify  "BASH_ENV=$RUN/bashenv-ro.sh" "GREP_BASHENV_LOG=$OUT/trip-b-readonly-verify.log" -- "${VERIFY_ARGS[@]}"
run_gate b-readonly-claims verify-claims "BASH_ENV=$RUN/bashenv-ro.sh" "GREP_BASHENV_LOG=$OUT/trip-b-readonly-claims.log" -- "${CLAIMS_ARGS[@]}"
echo "--- b-readonly-claims stderr head:"; head -4 "$OUT/b-readonly-claims.err"
echo "--- b-readonly-claims stdout bytes: $(wc -c < "$OUT/b-readonly-claims.out")"

echo "== raw (un-normalized) diffs vs baseline: expected exactly the ts token =="
echo "--- diff base-verify.out vs a-shim-verify.out:"; diff "$OUT/base-verify.out" "$OUT/a-shim-verify.out" | head -6
echo "--- diff base-claims.out vs c-override-claims.out:"; diff "$OUT/base-claims.out" "$OUT/c-override-claims.out" | head -6

echo "== artifact manifest =="
( cd "$R" && sha256sum run/matrix.sh run/extra.sh run/shim/grep run/bashenv.sh run/bashenv-ro.sh \
    out/base-verify.out out/base-verify.err out/base-verify.rc \
    out/base-claims.out out/base-claims.err out/base-claims.rc \
    out/trip-*.log out/e-a-verify.err out/e-b-verify.err out/e-c-verify.err \
    out/e-a-claims.err out/e-b-claims.err out/e-c-claims.err \
    out/nogrep2-verify.out out/nogrep2-claims.out out/pinshim-verify.err out/pinshim-claims.err \
    out/b-readonly-claims.err out/ref-rel-claims.err out/ref-nongnu-claims.err ) > "$OUT/manifest.txt"
cat "$OUT/manifest.txt"
echo "== done =="
