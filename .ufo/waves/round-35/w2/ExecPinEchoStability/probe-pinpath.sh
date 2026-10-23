#!/usr/bin/env bash
# probe-pinpath.sh — the pin's DEFAULT path vs base when grep cannot be verified,
# and a same-path --pin echo A/B (removes my harness's differing baseline paths).
set -uo pipefail
SC=/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
L=$SC/fleet/chousa-shokunin
G=$L/tools/research-gate.sh
OUT=$SC/out-pinpath; rm -rf "$OUT"; mkdir -p "$OUT"

# A PATH with the tools the gate needs but NO grep binary.
NG=$OUT/nogrep; mkdir -p "$NG"
for t in bash sh env od tr sed cut head tail date wc sort uniq cat mkdir mktemp \
         dirname basename readlink sha256sum stat ls find flock timeout touch rm \
         cp mv awk xargs expr true false id printf; do
  p=$(command -v "$t" 2>/dev/null) && ln -sf "$p" "$NG/$t"
done
echo "nogrep PATH grep present? $(ls "$NG" | grep -c '^grep$')"

REC=corpus/fixtures/full-r6.md
CLAIMS=corpus/fixtures/full-r6.claims.jsonl

go() { # label gate echo pathmode args...
  local label=$1 gate=$2 echo_flag=$3 pathmode=$4; shift 4
  cp -f "$gate" "$G"
  local -a E=()
  [[ $echo_flag == on ]] && E=(CHOUSA_GREP_PIN_ECHO=1)
  local P=/usr/local/bin:/usr/bin:/bin
  [[ $pathmode == nogrep ]] && P=$NG
  ( cd "$L" && env -i PATH="$P" HOME=/tmp TMPDIR=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8 \
      CHOUSA_NOW_EPOCH=1761000000 "${E[@]+"${E[@]}"}" bash tools/research-gate.sh "$@" ) \
      >"$OUT/$label.out" 2>"$OUT/$label.err"
  echo $? >"$OUT/$label.rc"
}

for v in base land; do
  for pm in clean nogrep; do
    go "$v.$pm.verify"     "$SC/$v-gate.sh" off "$pm" verify "$REC" --root ..
    go "$v.$pm.claims"     "$SC/$v-gate.sh" off "$pm" verify-claims "$CLAIMS" --root ..
    go "$v.$pm.sweeps"     "$SC/$v-gate.sh" off "$pm" verify-sweeps "$REC" --root ..
    go "$v.$pm.help"       "$SC/$v-gate.sh" off "$pm" --help
  done
done

# same-path --pin A/B: pin to the SAME path twice (echo off, then echo on)
P1=$OUT/same.baseline
go land.pinA "$SC/land-gate.sh" off clean --pin "$P1"
cp "$P1" "$OUT/same.baseline.echooff"
go land.pinB "$SC/land-gate.sh" on  clean --pin "$P1"
cp "$P1" "$OUT/same.baseline.echoon"

cp -f "$SC/land-gate.sh" "$G"
{
for f in "$OUT"/*.rc; do
  b=${f%.rc}; n=$(basename "$b")
  printf '%-22s rc=%-3s out=%-60s err=%s\n' "$n" "$(cat "$f")" \
    "$(cat "$b.out" | head -2 | tr '\n' '|' | cut -c1-120)" \
    "$(wc -c <"$b.err")B"
done
echo "--- same-path baseline diff (echo off -> on):"
diff "$OUT/same.baseline.echooff" "$OUT/same.baseline.echoon" || true
} | tee "$OUT/summary.txt"
