#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/chousa-r32/w2/NoHarmVerifyAll32
OUT=$S/out
run_gate() { # GATE FIXTURE MANIFEST_REL_STATE
  local g=$1 d=$2 st=$3
  ( cd "$d" && CHOUSA_NOW_EPOCH=1790000000 timeout 200 bash "$S/$g/tools/research-gate.sh" \
      verify-all recA.md --claims claims.jsonl --json manifest.jsonl --root . >stdout 2>stderr )
  echo "$?"
}

echo "== sequential two appends (single writer)"
for g in base landed; do
  d="$OUT/fx/seq-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"; printf '{"prior":true}' >"$d/manifest.jsonl"
  ino0=$(stat -c %i "$d/manifest.jsonl")
  r1=$(run_gate "$g" "$d" x); r2=$(run_gate "$g" "$d" x)
  echo "$g rc1=$r1 rc2=$r2 inode=$ino0->$(stat -c %i "$d/manifest.jsonl") lines=$(wc -l <"$d/manifest.jsonl") blanks=$(grep -ac '^$' "$d/manifest.jsonl") stderr=$(cat "$d/stderr" | wc -c) bytes=$(wc -c <"$d/manifest.jsonl")"
done

echo "== read-only directory refusal"
for g in base landed; do
  d="$OUT/fx/rodir-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"; printf '{"prior":true}\n' >"$d/manifest.jsonl"
  h0=$(sha256sum "$d/manifest.jsonl" | cut -d' ' -f1); i0=$(stat -c %i "$d/manifest.jsonl")
  chmod 0500 "$d"
  r=0
  ( cd "$d" && CHOUSA_NOW_EPOCH=1790000000 timeout 200 bash "$S/$g/tools/research-gate.sh" \
      verify-all recA.md --claims claims.jsonl --json manifest.jsonl --root . \
      >"$OUT/rodir-$g.out" 2>"$OUT/rodir-$g.err" ) || r=$?
  chmod 0700 "$d"
  echo "$g rc=$r same_bytes=$([[ $(sha256sum "$d/manifest.jsonl"|cut -d' ' -f1) == "$h0" ]] && echo yes || echo no) inode_same=$([[ $(stat -c %i "$d/manifest.jsonl") == "$i0" ]] && echo yes || echo no) stderr_first=$(head -1 "$OUT/rodir-$g.err")"
done

echo "== empty read-only manifest"
for g in base landed; do
  d="$OUT/fx/erom-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"; : >"$d/manifest.jsonl"; chmod 0400 "$d/manifest.jsonl"
  r=0
  ( cd "$d" && CHOUSA_NOW_EPOCH=1790000000 timeout 200 bash "$S/$g/tools/research-gate.sh" \
      verify-all recA.md --claims claims.jsonl --json manifest.jsonl --root . >"$OUT/erom-$g.out" 2>"$OUT/erom-$g.err" ) || r=$?
  chmod 0600 "$d/manifest.jsonl"
  echo "$g rc=$r size=$(wc -c <"$d/manifest.jsonl") stderr_first=$(head -1 "$OUT/erom-$g.err")"
done

echo "== flock-free host (deliberate fail-closed difference)"
mkdir -p "$S/bin"
for f in /usr/bin/*; do
  [ -f "$f" ] || continue
  b=$(basename "$f"); [ "$b" = flock ] && continue
  [ -e "$S/bin/$b" ] || ln -s "$f" "$S/bin/$b" 2>/dev/null || true
done
for g in base landed; do
  d="$OUT/fx/noflock-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"
  rc=0
  ( cd "$d" && env -u CHOUSA_RECORD -u CHOUSA_CLAIMS CHOUSA_ROOT=. CHOUSA_STRICT=0 CHOUSA_NOW_EPOCH=1790000000 \
      PATH="$S/bin" /usr/bin/bash "$S/$g/tools/research-gate.sh" verify-all claims.jsonl --json manifest.jsonl --root . >stdout 2>stderr ) || rc=$?
  echo "$g rc=$rc manifest=$([[ -e $d/manifest.jsonl ]] && wc -l <"$d/manifest.jsonl" || echo absent) stderr_first=$(head -1 "$d/stderr")"
done
echo DONE
