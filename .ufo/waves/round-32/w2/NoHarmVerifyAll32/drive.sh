#!/usr/bin/env bash
# Single-writer verify-all --json matrix: base vs landed gate.
# Every run gets a fresh fixture; manifest seed states are fixed; ts is pinned
# via CHOUSA_NOW_EPOCH so manifest bytes are comparable (gate_sha256 masked).
set -u
S=/fast/scratch/hyaku/chousa-r32/w2/NoHarmVerifyAll32
OUT=$S/out
mkdir -p "$OUT"
SUM=$OUT/matrix.tsv
: >"$SUM"
printf 'gate\trec\tstate\tinv\targ\tfx_rc\tm_rc\tsha_before\tsha_after\tinode_before\tinode_after\tmode_before\tmode_after\tsize_after\tblank\tglued\n' >>"$SUM"

seed() { # DIR STATE
  local fx=$1 st=$2 f=$1/manifest.jsonl
  case $st in
    absent) : ;;
    empty)  : >"$f" ;;
    term)   printf '{"prior":true}\n' >"$f" ;;
    unterm) printf '{"prior":true}' >"$f" ;;
    nul)    printf '{"prior":true}\0' >"$f" ;;
    cr)     printf '{"prior":true}\r' >"$f" ;;
    wore)   printf '{"prior":true}\n' >"$f"; chmod 0200 "$f" ;;
    dir)    mkdir "$f" ;;
  esac
}

run_one() { # GATE REC STATE
  local g=$1 r=$2 st=$3 inv="$S/$1/tools/research-gate.sh"
  local fx="$OUT/fx/$g-$r-$st" rc=0 mrc=0 mb ma ib ia db da sa
  rm -rf "$fx"; cp -a "$S/tpl" "$fx"
  if [[ $st != nodir ]]; then seed "$fx" "$st"; else rm -rf "$S/out/nodir"; fi
  local mf="$fx/manifest.jsonl"
  local arg="$mf"
  [[ $st == nodir ]] && arg="$S/out/nodir/manifest.jsonl"
  local pre='-' post='-'
  if [[ $st != nodir && $st != dir && -e $mf ]]; then
    pre=$(stat -c '%s %i %a' "$mf")
  fi
  local cmd
  if [[ $r == B ]]; then
    cmd=(bash "$inv" verify-all claims.jsonl --json manifest.jsonl --root .)
  else
    cmd=(bash "$inv" verify-all "rec$r.md" --claims claims.jsonl --json manifest.jsonl --root .)
  fi
  ( cd "$fx" && CHOUSA_NOW_EPOCH=1790000000 timeout 900 "${cmd[@]}" ) >"$fx/stdout" 2>"$fx/stderr"
  rc=$?
  # manifest post state
  if [[ $st != nodir && -f $mf ]]; then
    post=$(stat -c '%s %i %a' "$mf")
    mb=$(sha256sum "$mf" | cut -d' ' -f1)
    # blank lines (binary-safe) + glued-line check: every 0x0a-separated line
    # that has content from the last append must start with '{' after trimming
    # a NUL/CR prior byte.
    local blanks glued
    blanks=$(grep -ac '^$' "$mf" 2>/dev/null || true)
    glued=$(python3 - "$mf" <<'PY'
import sys
b=open(sys.argv[1],'rb').read()
n=0
for ln in b.split(b'\n'):
    t=ln.strip(b'\0\r')
    if not t: continue
    if t.startswith(b'{"prior":true}'):
        rest=t[len(b'{"prior":true}'):]
        if rest: n+=1   # glued object on the prior line
    elif t.startswith(b'{'):
        import json
        try: json.loads(t)
        except Exception: n+=1
    else: n+=1
print(n)
PY
)
  else
    post='-'; mb='-'; blanks='-'; glued='-'
  fi
  local ib='-' ia='-' ma='-'
  if [[ $pre != '-' ]]; then ib=$(echo "$pre" | cut -d' ' -f2); ia=$(echo "$post" | cut -d' ' -f2); fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$g" "$r" "$st" "verify-all" "$arg" "$rc" "$mrc" \
    "${pre}" "${post}" "${ib}" "${ia}" "$(echo "$pre"|cut -d' ' -f3)" "$(echo "$post"|cut -d' ' -f3)" \
    "$(echo "$post"|cut -d' ' -f1)" "$blanks" "$glued" >>"$SUM"
}

for g in base landed; do
  for r in A B C D E; do
    for st in absent empty term unterm nul cr; do
      run_one "$g" "$r" "$st"
    done
  done
  for st in wore dir nodir; do run_one "$g" A "$st"; done
done
echo DONE; wc -l "$SUM"
