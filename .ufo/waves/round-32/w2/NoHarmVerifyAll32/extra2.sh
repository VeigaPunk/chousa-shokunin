#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/chousa-r32/w2/NoHarmVerifyAll32
OUT=$S/out
G() { # GATE FIXTURE TAG
  local g=$1 d=$2 tag=$3 rc=0
  ( cd "$d" && CHOUSA_NOW_EPOCH=1790000000 timeout 200 bash "$S/$g/tools/research-gate.sh" \
      verify-all recA.md --claims claims.jsonl --json manifest.jsonl --root . \
      >"$OUT/$tag-$g.out" 2>"$OUT/$tag-$g.err" ) || rc=$?
  echo "$rc"
}
echo "== absent manifest in non-writable dir (cannot create)"
for g in base landed; do
  d="$OUT/fx/nwdir-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"; chmod 0500 "$d"
  r=$(G "$g" "$d" nwdir)
  chmod 0700 "$d"
  echo "$g rc=$r file=$([[ -e $d/manifest.jsonl ]] && echo created || echo absent) stderr=$(tr '\n' '|' <"$OUT/nwdir-$g.err")"
done
echo "== existing 0644 terminated manifest inside 0500 dir (append allowed by fs)"
for g in base landed; do
  d="$OUT/fx/rodir2-$g"; rm -rf "$d"; cp -a "$S/tpl/." "$d"; printf '{"prior":true}\n' >"$d/manifest.jsonl"
  h0=$(sha256sum "$d/manifest.jsonl" | cut -d' ' -f1); i0=$(stat -c %i "$d/manifest.jsonl")
  chmod 0500 "$d"; r=$(G "$g" "$d" rodir2); chmod 0700 "$d"
  echo "$g rc=$r lines=$(wc -l <"$d/manifest.jsonl") blanks=$(grep -ac '^$' "$d/manifest.jsonl") prefix_kept=$([[ $(head -c 15 "$d/manifest.jsonl") == '{"prior":true}' ]] && echo yes || echo no) inode_same=$([[ $(stat -c %i "$d/manifest.jsonl") == "$i0" ]] && echo yes || echo no)"
done
echo "== empty read-only manifest, full stderr"
for g in base landed; do
  echo "-- $g:"; sed 's/^/   /' "$OUT/erom-$g.err"
done
echo DONE
