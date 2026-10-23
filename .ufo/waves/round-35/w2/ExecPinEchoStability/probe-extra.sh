#!/usr/bin/env bash
# probe-extra.sh — remaining invocation forms, base vs land, echo OFF.
set -uo pipefail
SC=/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
L=$SC/fleet/chousa-shokunin
G=$L/tools/research-gate.sh
OUT=$SC/out-extra; rm -rf "$OUT"; mkdir -p "$OUT"

REC=corpus/fixtures/full-r6.md
CLAIMS=corpus/fixtures/full-r6.claims.jsonl
META=corpus/fixtures/metadata-r25/recheck-90d.md
REG=$L/corpus/fixtures/metadata-r25/../metadata-r25/README.md

run() { # variant tag args...
  local v=$1 tag=$2; shift 2
  cp -f "$SC/$v-gate.sh" "$G"
  ( cd "$L" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp \
      LANG=C.UTF-8 LC_ALL=C.UTF-8 CHOUSA_NOW_EPOCH=1761000000 \
      bash tools/research-gate.sh "$@" ) >"$OUT/$v.$tag.out" 2>"$OUT/$v.$tag.err"
  echo $? >"$OUT/$v.$tag.rc"
}

for v in base basepin land; do
  run "$v" noargs
  run "$v" recordflag    verify --record "$REC" --root ..
  run "$v" claimsjsonl   verify-all "$CLAIMS" --root ..
  run "$v" meta-asof     verify-metadata "$META" --root .. --as-of 2026-01-15
  run "$v" meta-registry verify-metadata "$META" --root .. --registry "$REG"
  run "$v" meta-bad-asof verify-metadata "$META" --root .. --as-of 2026-02-30
  run "$v" json          verify-all "$REC" --claims "$CLAIMS" --root .. --json "$OUT/$v.manifest.jsonl"
  run "$v" claims-missing verify-claims "$OUT/absent.jsonl" --root ..
  run "$v" verify-missing verify corpus/fixtures/absent.md --root ..
done

cp -f "$SC/land-gate.sh" "$G"
{
printf '%-22s %-6s %-6s %-6s %-9s %-9s\n' CASE base_rc basepin_rc land_rc base==land bp==land
for c in noargs recordflag claimsjsonl meta-asof meta-registry meta-bad-asof json claims-missing verify-missing; do
  j() { cat "$OUT/$1.$c.out" "$OUT/$1.$c.err"; }
  br=$(cat "$OUT/base.$c.rc"); pr=$(cat "$OUT/basepin.$c.rc"); lr=$(cat "$OUT/land.$c.rc")
  cmp -s <(j base) <(j land) && bl=SAME || bl=DIFF
  cmp -s <(j basepin) <(j land) && pl=SAME || pl=DIFF
  printf '%-22s %-6s %-6s %-6s %-9s %-9s\n' "$c" "$br" "$pr" "$lr" "$bl" "$pl"
done
echo "--- manifest diff base vs land (gate_sha256 expected to differ):"
diff "$OUT/base.manifest.jsonl" "$OUT/land.manifest.jsonl" | head -6 || true
} | tee "$OUT/summary.txt"
