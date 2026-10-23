#!/usr/bin/env python3
"""Build independent-chunk controls from the landed gate (only the dead-zone
chunk matcher tok_span_offsets_chunk is replaced; routing and boundary helpers
are untouched). Controls: (a) k=2, (b) k=4, (c) k=16 chunk-presence anywhere,
(d) k=4 chunks in strictly increasing order (adjacency not required)."""
import re
import sys

SRC = sys.argv[1]
OUTDIR = sys.argv[2]

with open(SRC, "r", encoding="utf-8", newline="") as f:
    gate = f.read()

start = gate.index("tok_span_offsets_chunk() {")
end = gate.index("tok_span_at() {")
orig = gate[start:end]

ANY = r'''tok_span_offsets_chunk() { # CONTROL: every k-chunk occurs anywhere (no adjacency)
  local LC_ALL=C
  export LC_ALL
  local hay=$1 span=$2 slen=${#span} k=__K__
  local csize a b i part pattern occurrence found_all=1
  csize=$(( (slen + k - 1) / k ))
  for (( i=0; i<k; i++ )); do
    a=$(( i * csize )); b=$(( a + csize ))
    if (( b > slen )); then b=$slen; fi
    part=${span:a:b-a}
    pattern=$(tok_hex_pattern "$part")
    if ! printf '%s' "$hay" | grep -a -z -q -P -- "$pattern"; then
      found_all=0
      break
    fi
  done
  if (( found_all == 0 )); then return 0; fi
  part=${span:0:csize}
  pattern=$(tok_hex_pattern "$part")
  while IFS= read -r -d '' occurrence; do
    printf '%s\n' "${occurrence%%:*}"
  done < <(printf '%s' "$hay" | grep -a -z -b -o -P -- "$pattern")
}

'''

ORDERED = r'''ctl_chunk_offsets() { # HAY PART -> stdout: byte offsets of PART, one per line
  local LC_ALL=C
  export LC_ALL
  printf '%s' "$1" | grep -a -z -b -o -P -- "$(tok_hex_pattern "$2")" | {
    while IFS= read -r -d '' r; do printf '%s\n' "${r%%:*}"; done
  }
}

tok_span_offsets_chunk() { # CONTROL: k chunks occur at strictly increasing offsets
  local LC_ALL=C
  export LC_ALL
  local hay=$1 span=$2 slen=${#span} k=__K__
  local csize a b i part cand o prev ok found
  local -a coff=()
  local -a ioff=()
  csize=$(( (slen + k - 1) / k ))
  mapfile -t coff < <(ctl_chunk_offsets "$hay" "${span:0:csize}")
  for cand in "${coff[@]}"; do
    prev=$cand; ok=1
    for (( i=1; i<k; i++ )); do
      a=$(( i * csize )); b=$(( a + csize ))
      if (( b > slen )); then b=$slen; fi
      part=${span:a:b-a}
      mapfile -t ioff < <(ctl_chunk_offsets "$hay" "$part")
      found=
      for o in "${ioff[@]}"; do
        if (( o > prev )); then found=$o; break; fi
      done
      if [[ -z $found ]]; then ok=0; break; fi
      prev=$found
    done
    if (( ok == 1 )); then printf '%s\n' "$cand"; fi
  done
}

'''

variants = [
    ("ctl2-any", ANY.replace("__K__", "2")),
    ("ctl4-any", ANY.replace("__K__", "4")),
    ("ctl16-any", ANY.replace("__K__", "16")),
    ("ctl4-ordered", ORDERED.replace("__K__", "4")),
]

for name, body in variants:
    out = gate[:start] + body + gate[end:]
    path = OUTDIR + "/" + name + ".sh"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(name, len(out))
