#!/usr/bin/env python3
"""Probe10 word-exit probe: one surface only — the EXIT= token of the receipt header.

Independent oracle (derived from frozen claims.md round65: "EXIT decimal 0..255";
"0 consistent,1 invalid,2 usage/environment"):
  accept word iff it is a canonical ASCII decimal numeral for an integer in [0,255]:
    - nonempty, all chars ASCII digits
    - no leading zero unless the word is exactly "0"
    - at most 3 digits and value <= 255
Everything else about the receipt is held fixed and valid, so the EXIT word is the
only varied surface. Malformed word must yield exit 1 (invalid receipt), never 2.
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe10')
FIX = ROOT / 'fixture'
REV = (ROOT / 'fixture-REV').read_text().strip()
DIGEST = (ROOT / 'fixture-DIGEST').read_text().strip()
REL = 'pin.txt'
REF = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py')
BODY = 'probe10 word-exit body'
OUT = ROOT / 'word-exit-matrix.tsv'

WORDS = [
    # expected-accept canonical decimals
    '0', '1', '9', '42', '127', '200', '255',
    # leading zeros
    '00', '01', '09', '042', '0255', '000',
    # out of range
    '256', '257', '300', '999',
    # too many digits
    '1000', '10000',
    # empty / sign / whitespace
    '', '-1', '+1', ' 42', '42 ', '\t42', '42\t', '4 2',
    # non-decimal notation
    '0x2a', '0b101010', '2.5', '2a', '4_2',
    # non-ASCII digit lookalikes
    '\u0664\u0662',          # Arabic-Indic 42
    '\uff14\uff12',          # fullwidth 42
    '4\u00b2',               # 4 + superscript two (isdigit() True, not a numeral)
]

def expected(word: str) -> bool:
    if not word or not word.isascii() or not word.isdigit():
        return False
    if len(word) > 3:
        return False
    if len(word) > 1 and word[0] == '0':
        return False
    return int(word) <= 255

def shown(word: str) -> str:
    return json.dumps(word)  # escaped, single-line representation

receipts = ROOT / 'receipts'
receipts.mkdir(exist_ok=True)
rows = []
for i, w in enumerate(WORDS):
    tag = f'w{i:02d}'
    rp = receipts / f'{tag}.txt'
    rp.write_text(
        f'REVISION={REV}\nEXIT={w}\nSHA256={DIGEST} {REL}\n\n{BODY}\n',
        encoding='utf-8',
    )
    q = subprocess.run(
        [sys.executable, str(REF), '--receipt', str(rp),
         '--root', str(FIX), '--revision', REV],
        capture_output=True, text=True,
    )
    exp = expected(w)
    got_accept = q.returncode == 0
    stdout = q.stdout.strip()
    verdict = 'AGREE'
    if got_accept != exp:
        verdict = 'MISMATCH'
    elif q.returncode not in (0, 1):
        verdict = 'BADEXIT'
    elif got_accept and stdout != 'RECEIPT_PIN=PASS':
        verdict = 'BADOUT'
    elif (not got_accept) and not stdout.startswith('RECEIPT_PIN=FAIL'):
        verdict = 'BADOUT'
    rows.append((tag, shown(w), str(exp).lower(), str(q.returncode), stdout, verdict))

with OUT.open('w', encoding='utf-8') as f:
    f.write('tag\texit_word\texpected_accept\tactual_exit\tactual_stdout\tverdict\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')

mism = [r for r in rows if r[5] != 'AGREE']
print(f'cases={len(rows)} mismatches={len(mism)}')
for r in mism:
    print('MISMATCH', r)
print('matrix=', OUT)
