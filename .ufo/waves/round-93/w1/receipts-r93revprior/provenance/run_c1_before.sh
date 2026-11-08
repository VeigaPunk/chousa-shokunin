#!/bin/bash
# Seat R93RevPrior: C1 BEFORE-state reproduction on committed bytes of C2.
set -u
S=/fast/scratch/hyaku/chousa-r93/R93RevPrior
F=b7241252c2358613d3b22b7d0454d98c56dab373
C=754b62fb6adc60e44e12375af5461a0ebe302994
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
SLANE=/fast/scratch/hyaku/chousa-r93/RevPrior-lane-unused

mk() {
  d=$1
  rm -rf "$d"
  git clone --shared "$S/repo" "$d" -q || return 9
  git -C "$d" checkout -q "$C" || return 9
  top=$(git -C "$d" rev-parse --show-toplevel)
  test "$top" = "$d" || { echo "TOPLEVEL MISMATCH $top != $d"; return 9; }
}

explicit() {
  root=$1
  printf -- '--expected %s/corpus/evidence/round93/controls/expected.tsv --receipts %s/corpus/evidence/round93/controls/receipts --pins %s/corpus/evidence/round93/instrument-pins.txt' "$root" "$root" "$root"
}

run92() {
  tag=$1; root=$2; shift 2
  driver="$root/corpus/evidence/round92/control-driver-r92.py"
  python3 -B "$driver" verify --root "$root" --work "$S/w-$tag" --rev "$F" --receipts-rev "$C" "$@" \
    > "$S/out-c1-$tag.txt" 2>&1
  echo "rc=$?" >> "$S/out-c1-$tag.txt"
}

# 1 pristine, no --repo
( mk "$S/t-pris" && read -r -a A <<< "$(explicit "$S/t-pris")" && run92 pristine-norepo "$S/t-pris" "${A[@]}" ) &
# 2 pristine, with --repo
( mk "$S/t-pris2" && read -r -a A <<< "$(explicit "$S/t-pris2")" && run92 pristine-repo "$S/t-pris2" "${A[@]}" --repo "$S/t-pris2" ) &
# 3 receipt tampered, no --repo
( mk "$S/t-tr" && printf '# tampered\n' >> "$S/t-tr/corpus/evidence/round93/controls/receipts/c2-prior-landing.txt" \
  && read -r -a A <<< "$(explicit "$S/t-tr")" && run92 receipt-tamper-norepo "$S/t-tr" "${A[@]}" ) &
# 4 receipt tampered, with --repo
( mk "$S/t-tr2" && printf '# tampered\n' >> "$S/t-tr2/corpus/evidence/round93/controls/receipts/c2-prior-landing.txt" \
  && read -r -a A <<< "$(explicit "$S/t-tr2")" && run92 receipt-tamper-repo "$S/t-tr2" "${A[@]}" --repo "$S/t-tr2" ) &
# 5 unexecuted pinned instrument tampered, no --repo
( mk "$S/t-ti" && printf '\n# tampered\n' >> "$S/t-ti/corpus/evidence/round93/curation-controls-r93.py" \
  && read -r -a A <<< "$(explicit "$S/t-ti")" && run92 instr-tamper-norepo "$S/t-ti" "${A[@]}" ) &
# 6 derivation: lane driver, HERE-relative defaults, --root names the archive, no explicit paths
( mk "$S/t-derive" && python3 -B "$LANE/corpus/evidence/round92/control-driver-r92.py" verify \
    --root "$S/t-derive" --work "$S/w-derive" --rev "$F" --receipts-rev "$C" \
    > "$S/out-c1-derive.txt" 2>&1; echo "rc=$?" >> "$S/out-c1-derive.txt" ) &
wait
echo "ALL DONE"
for f in "$S"/out-c1-*.txt; do echo "== $f"; tail -4 "$f"; done
