#!/usr/bin/env python3
"""Attack17 probe battery: duplicate-adjacent forged/malformed receipts vs frozen reference validator.
Read-only git; bounded; no frozen bytes altered."""
import hashlib, pathlib, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
REF = LANE + '/corpus/evidence/round65/controls/ref-receipt-pin.py'
OUT = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Attack17/probe')

raw = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', BASE + ':SKILL.md'],
                     capture_output=True, check=True).stdout
h = hashlib.sha256(raw).hexdigest()
v = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'

cases = {
    # --- controls ---
    'control-valid': (v, 0),
    'control-frozen-duplicate-exit-before-sep': (v.replace('\n\n', '\nEXIT=0\n\n'), 1),
    # --- duplicate BEFORE separator (index 3 must be blank) ---
    'dup-revision-before-sep': (v.replace('\n\n', f'\nREVISION={BASE}\n\n'), 1),
    'dup-sha256-before-sep': (v.replace('\n\n', f'\nSHA256={h} SKILL.md\n\n'), 1),
    'dup-unknown-line-before-sep': (v.replace('\n\n', '\nGARBAGE\n\n'), 1),
    'dup-two-exit-before-sep': (v.replace('\n\n', '\nEXIT=0\nEXIT=0\n\n'), 1),
    'sep-is-single-space': (v.replace('\n\n', '\n \n'), 1),
    'header-order-shuffled': ('REVISION=%s\nSHA256=%s SKILL.md\nEXIT=0\n\nmeasured output\n' % (BASE, h), 1),
    # --- duplicate AFTER separator (body) ---
    'dup-exit-after-sep': (v.replace('\n\n', '\n\nEXIT=0\n'), 0),
    'dup-revision-after-sep': (v.replace('\n\n', f'\n\nREVISION={BASE}\n'), 0),
    'dup-sha256-after-sep': (v.replace('\n\n', f'\n\nSHA256={h} SKILL.md\n'), 0),
    'dup-full-second-header-block': (v + f'REVISION={BASE}\nEXIT=1\nSHA256={"0"*64} forged.md\n', 0),
    # --- nearby shape shifts ---
    'exit-leading-zeros': (v.replace('EXIT=0', 'EXIT=00'), 1),
    'receipt-with-utf8-bom': ('\ufeff' + v, 1),
    'crlf-line-endings': (v.replace('\n', '\r\n'), 0),
}

rows = []
for name, (text, expect) in cases.items():
    f = OUT / (name + '.txt')
    f.write_text(text)
    q = subprocess.run([sys.executable, '-B', REF, '--receipt', str(f),
                        '--root', LANE, '--revision', BASE],
                       capture_output=True, text=True, timeout=20)
    got = 'PASS' if q.returncode == 0 else 'FAIL'
    ok = 'OK' if q.returncode == expect else 'UNEXPECTED'
    rows.append((name, expect, q.returncode, q.stdout.strip(), ok))

print(f'{"case":42s} {"expect_rc":>9s} {"got_rc":>6s} {"result":>10s}  token')
for name, expect, rc, tok, ok in rows:
    print(f'{name:42s} {expect:9d} {rc:6d} {ok:>10s}  {tok[:60]}')

n_unexpected = sum(1 for r in rows if r[4] == 'UNEXPECTED')
print(f'\nTOTAL={len(rows)} UNEXPECTED={n_unexpected}')
