#!/usr/bin/env python3
"""Attack08 bounded probes (chousa r65): C1 receipt-pin framing/canonicalization attack.

Read-only on frozen bytes: copies reference validator into scratch, crafts nearby
malformed receipts OUTSIDE the frozen 20-case battery, runs reference + strict-NL
validators, and calibrates the frozen counter against both.
"""
import hashlib, pathlib, shutil, subprocess, sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Attack08')
REF_SRC = LANE / 'corpus/evidence/round65/controls/ref-receipt-pin.py'
REF = SCRATCH / 'ref-pin-copy.py'
STRICT = SCRATCH / 'strict-pin.py'
COUNTER = LANE / 'corpus/evidence/round65/c1-count.py'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'

def banner(t):
    print(f'\n=== {t} ===')

def run_tool(tool, receipt):
    q = subprocess.run([sys.executable, '-B', str(tool), '--receipt', str(receipt),
                        '--root', str(LANE), '--revision', BASE],
                       capture_output=True, text=True, timeout=30)
    return q.returncode, q.stdout.strip()

banner('environment')
print('python', sys.version.split()[0])
print(subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip())

shutil.copy(REF_SRC, REF)
strict_src = REF_SRC.read_text().replace('text.splitlines()', "text.split('\\n')")
STRICT.write_text(strict_src)

raw = subprocess.run(['git', '-C', str(LANE), 'cat-file', 'blob', BASE + ':SKILL.md'],
                     capture_output=True, check=True).stdout
h = hashlib.sha256(raw).hexdigest()
V = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'

variants = {
    'lf-valid': V,
    'frozen-negative-exit': V.replace('EXIT=0', 'EXIT=-1'),
    'crlf-every-lf': V.replace('\n', '\r\n'),
    'cr-only': V.replace('\n', '\r'),
    'vt-separator': V.replace('\n\n', '\n\x0b'),
    'ff-separator': V.replace('\n\n', '\n\x0c'),
    'fs-separator': V.replace('\n\n', '\n\x1c'),
    'nel-separator': V.replace('\n\n', '\n\u0085'),
    'u2028-separator': V.replace('\n\n', '\n\u2028'),
    'body-forged-header-block': V.replace(
        'measured output',
        'measured output\nREVISION=' + '0' * 40 + '\nEXIT=999\nSHA256=' + '0' * 64 + ' forged.txt'),
    'exit-leading-zero': V.replace('EXIT=0', 'EXIT=00'),
    'exit-tab-trailing': V.replace('EXIT=0', 'EXIT=0\t'),
}

banner('crafted receipts (exact bytes preserved)')
receipt_files = {}
for name, text in variants.items():
    p = SCRATCH / f'r-{name}.txt'
    p.write_text(text, encoding='utf-8', newline='')
    receipt_files[name] = p
    head = text.encode('utf-8')[:70]
    print(f'{name}: {head!r}')

banner('reference validator (frozen controls copy) on each variant')
ref_results = {}
for name, p in receipt_files.items():
    rc, out = run_tool(REF, p)
    ref_results[name] = (rc, out)
    print(f'{name}: rc={rc} out={out!r}')

banner('strict-NL validator (split("\\n") only) on each variant')
for name, p in receipt_files.items():
    rc, out = run_tool(STRICT, p)
    print(f'{name}: rc={rc} out={out!r}')

banner('frozen counter calibration')
for tool, tag in [(REF, 'ref-copy'), (STRICT, 'strict-nl'), (SCRATCH / 'absent.py', 'missing-target')]:
    w = SCRATCH / f'wk-{tag}'
    q = subprocess.run([sys.executable, '-B', str(COUNTER), '--tool', str(tool), '--work', str(w)],
                       capture_output=True, text=True, timeout=180)
    tail = (q.stdout.strip().splitlines() or [''])[-1]
    print(f'tool={tag}: counter rc={q.returncode} | {tail}')

banner('attack summary (reference validator verdicts)')
bypasses = [n for n, (rc, _) in ref_results.items() if rc == 0 and n != 'lf-valid']
print('reference-PASS on malformed variants:', bypasses if bypasses else 'NONE')
