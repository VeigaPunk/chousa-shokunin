#!/usr/bin/env python3
"""Probe08 — isolated negative-exit surface probe against round65 reference receipt-pin control.

Independently derived expectation (from frozen claims.md round65):
  Format: "REVISION full lowercase 40 hex, EXIT decimal 0..255, SHA256 ...".
  EXIT=-1 is outside the declared grammar (decimal 0..255, no sign) => receipt
  invalid/malformed => exit code 1 (exit 2 is reserved for usage/environment:
  "0 consistent,1 invalid,2 usage/environment") and a RECEIPT_PIN=FAIL token on stdout.
Surface: only the EXIT header's negative sign handling. One fixture git surface
(the frozen lane repo, read-only via git -C cat-file). No battery, no production writes.
"""
import hashlib, pathlib, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
REF = LANE + '/corpus/evidence/round65/controls/ref-receipt-pin.py'
WORK = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe08')

raw = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', BASE + ':SKILL.md'],
                     capture_output=True, check=True).stdout
h = hashlib.sha256(raw).hexdigest()

def receipt(exit_field: str) -> str:
    return (f'REVISION={BASE}\n'
            f'EXIT={exit_field}\n'
            f'SHA256={h} SKILL.md\n'
            '\n'
            'measured output\n')

# (name, EXIT field, independently expected rc, expect token)
cases = [
    ('positive-exit0',  '0',    0, 'RECEIPT_PIN=PASS'),
    ('boundary-exit255','255',  0, 'RECEIPT_PIN=PASS'),  # 255 in-grammar: proves minus sign, not magnitude, is rejected
    ('negative-exit-frozen', '-1', 1, 'RECEIPT_PIN=FAIL '),  # exact frozen battery case
    ('negative-zero',   '-0',   1, 'RECEIPT_PIN=FAIL '),
    ('negative-255',    '-255', 1, 'RECEIPT_PIN=FAIL '),
    ('negative-256',    '-256', 1, 'RECEIPT_PIN=FAIL '),
    ('sign-space',      '- 1',  1, 'RECEIPT_PIN=FAIL '),
    ('minus-minus',     '--1',  1, 'RECEIPT_PIN=FAIL '),
]

results = []
for name, field, want_rc, want_tok in cases:
    f = WORK / (name + '.receipt.txt')
    f.write_text(receipt(field), encoding='utf-8')
    q = subprocess.run([sys.executable, '-B', REF, '--receipt', str(f),
                        '--root', LANE, '--revision', BASE],
                       capture_output=True, text=True, timeout=20)
    ok = q.returncode == want_rc and (
        (want_rc == 0 and q.stdout.strip() == want_tok)
        or (want_rc != 0 and q.stdout.startswith(want_tok)))
    results.append((name, field, want_rc, q.returncode, q.stdout.strip(), ok))
    print(f'CASE {name:22s} EXIT={field:5s} want_rc={want_rc} got_rc={q.returncode} '
          f'stdout={q.stdout.strip()!r} {"OK" if ok else "MISMATCH"}')

n = sum(r[-1] for r in results)
print(f'NEGATIVE-EXIT-SURFACE {n}/{len(results)} {"CONSISTENT" if n == len(results) else "DIVERGENT"}')
sys.exit(0 if n == len(results) else 1)
