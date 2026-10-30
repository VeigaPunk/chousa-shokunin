#!/usr/bin/env bash
# Probe13 isolated short-digest fixture for receipt-header consistency.
# Scratch-only. No production writes, no network.
set -u
export TMPDIR=/fast/scratch/hyaku/chousa-r65/Probe13/tmp
mkdir -p "$TMPDIR"
ROOT=/fast/scratch/hyaku/chousa-r65/Probe13
FIX="$ROOT/fixture/repo"
cd "$ROOT"

rm -rf fixture receipts
mkdir -p fixture receipts

# --- build isolated git repo ---
git init -q "$FIX"
cd "$FIX"
git config user.email probe13@example.invalid
git config user.name Probe13
TOP="$(git rev-parse --show-toplevel)"
[ "$TOP" = "$FIX" ] || { echo "FATAL: toplevel $TOP != $FIX"; exit 99; }
echo 'hello receipt world' > a.txt
mkdir -p sub
echo 'nested content' > sub/b.txt
git add -A
git commit -qm 'fixture base'
REV="$(git rev-parse HEAD)"
FULL="$(git cat-file blob "$REV:a.txt" | sha256sum | awk '{print $1}')"
cd "$ROOT"

[ "${#FULL}" -eq 64 ] || { echo "FATAL: digest $FULL"; exit 99; }
SHORT32="${FULL:0:32}"
SHORT63="${FULL:0:63}"

mk_receipt() { # $1=outfile $2=sha-field $3=exit $4=path
  {
    printf 'REVISION=%s\n' "$REV"
    printf 'EXIT=%s\n' "$3"
    printf 'SHA256=%s %s\n' "$2" "$4"
    printf '\n'
    printf 'fixture output body\n'
  } > "$1"
}

mk_receipt receipts/short32.rcpt "$SHORT32" 0 a.txt
mk_receipt receipts/short63.rcpt "$SHORT63" 0 a.txt
mk_receipt receipts/control-full.rcpt "$FULL" 0 a.txt

REF=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py

run() { # $1=receipt
  python3 "$REF" --receipt "$ROOT/receipts/$1" --root "$FIX" --revision "$REV" \
    > "$ROOT/receipts/$1.out" 2> "$ROOT/receipts/$1.err"
  echo "$1 exit=$? stdout=$(cat "$ROOT/receipts/$1.out") stderr=$(cat "$ROOT/receipts/$1.err")"
}

run short32.rcpt
run short63.rcpt
run control-full.rcpt

{
  echo "REV=$REV"
  echo "FULL=$FULL"
  echo "SHORT32=$SHORT32"
  echo "SHORT63=$SHORT63"
} > "$ROOT/receipts/facts.env"
echo "FACTS: REV=$REV FULL=$FULL"
