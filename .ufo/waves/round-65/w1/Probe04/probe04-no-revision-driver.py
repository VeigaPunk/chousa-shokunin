#!/usr/bin/env python3
"""Probe04 isolated fixture — R65-C1 no-revision surface.

Builds receipt fixtures that violate the REVISION header rule of the frozen
format (claims.md R65-C1), derives expected results independently from the
frozen spec text, runs the frozen reference controls/ref-receipt-pin.py with
the canonical argv shape, and cross-checks. Read-only git (cat-file only).
"""
import hashlib, json, pathlib, re, subprocess, sys, os

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
REF = LANE / 'corpus/evidence/round65/controls/ref-receipt-pin.py'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe04')
FIX = SCRATCH / 'fixtures'
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')

# --- canonical valid receipt, built exactly like the frozen counter does ---
raw = subprocess.run(['git', '-C', str(LANE), 'cat-file', 'blob', BASE + ':SKILL.md'],
                     capture_output=True, check=True).stdout
h = hashlib.sha256(raw).hexdigest()
VALID = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'

VARIANTS = {
    'absent': VALID.split('\n', 1)[1],                      # counter's no-revision case
    'empty-value': VALID.replace('REVISION=' + BASE, 'REVISION='),
    'upper-hex': VALID.replace(BASE, BASE.upper()),
    'mixed-hex': VALID.replace(BASE, BASE[:4].upper() + BASE[4:]),
    'nonhex-40': VALID.replace(BASE, 'g' * 40),
    'trailing-space': VALID.replace('REVISION=' + BASE, 'REVISION=' + BASE + ' '),
    'short-8': VALID.replace(BASE, BASE[:8]),
}

# --- independent expectation, derived from the frozen spec text only ---
# claims.md: "exactly ordered REVISION full lowercase 40 hex, EXIT decimal
# 0..255, SHA256 full lowercase 64 hex plus canonical relative POSIX path,
# empty separator, nonempty output. ... 0 consistent,1 invalid,2 usage/env."
REV_RE = re.compile(r'^REVISION=([0-9a-f]{40})$')

def independent_expect(text):
    lines = text.splitlines()
    if len(lines) < 5 or lines[3] != '' or not '\n'.join(lines[4:]).strip():
        return 1, 'header-count/separator/body'
    m = REV_RE.match(lines[0])
    if not m:
        return 1, 'revision-header-malformed'
    if m.group(1) != BASE:
        return 1, 'revision-mismatch'
    if not re.fullmatch(r'EXIT=(?:0|[1-9][0-9]{0,2})', lines[1]) or int(lines[1][5:]) > 255:
        return 1, 'exit-header'
    d = re.fullmatch(r'SHA256=([0-9a-f]{64}) (.+)', lines[2])
    if not d:
        return 1, 'digest-header'
    rel = pathlib.PurePosixPath(d.group(2))
    if rel.is_absolute() or '..' in rel.parts or str(rel) != d.group(2) or not rel.parts:
        return 1, 'path'
    if d.group(1) != h or rel != pathlib.PurePosixPath('SKILL.md'):
        return 1, 'digest/blob'
    return 0, 'consistent'

def run_ref(receipt):
    q = subprocess.run([sys.executable, '-B', str(REF), '--receipt', str(receipt),
                        '--root', str(LANE), '--revision', BASE],
                       capture_output=True, text=True, timeout=20)
    return q.returncode, q.stdout, q.stderr

def main():
    FIX.mkdir(parents=True, exist_ok=True)
    rows = []
    # harness sanity control: the valid receipt must PASS through this driver
    ctl = FIX / 'control-valid.txt'
    ctl.write_text(VALID)
    rc, out, err = run_ref(ctl)
    rows.append({'case': 'control-valid', 'expected_rc': 0, 'actual_rc': rc,
                 'stdout': out, 'stderr': err, 'independent_rc': 0,
                 'agree': rc == 0 and out.strip() == 'RECEIPT_PIN=PASS'})
    for name, text in VARIANTS.items():
        f = FIX / (name + '.txt')
        f.write_text(text)
        exp_rc, why = independent_expect(text)
        rc, out, err = run_ref(f)
        ok = (rc == exp_rc == 1) and out.startswith('RECEIPT_PIN=FAIL ') and not err
        rows.append({'case': name, 'expected_rc': exp_rc, 'actual_rc': rc,
                     'stdout': out, 'stderr': err, 'independent_rc': exp_rc,
                     'independent_why': why, 'agree': ok})
    verdict = all(r['agree'] for r in rows)
    (SCRATCH / 'results.json').write_text(json.dumps(
        {'base': BASE, 'tool': str(REF), 'argv_shape': '--receipt <f> --root <lane> --revision <BASE>',
         'rows': rows, 'all_agree': verdict}, indent=1))
    for r in rows:
        print(f"{r['case']:>16} expect={r['expected_rc']} actual={r['actual_rc']} "
              f"agree={r['agree']} :: {r['stdout'].strip()}")
    print('ALL_AGREE=' + str(verdict))
    return 0 if verdict else 1

if __name__ == '__main__':
    sys.exit(main())
