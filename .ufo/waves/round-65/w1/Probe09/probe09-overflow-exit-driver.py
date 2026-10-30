#!/usr/bin/env python3
"""Probe09 — R65-C1 isolated fixture, overflow-exit surface (one surface only).

Builds EXIT-header variants of an otherwise fully valid receipt binding the SKILL.md
blob at the round freeze, runs the frozen reference with the canonical argv shape, and
compares against expectations derived INDEPENDENTLY from the frozen format text in
claims.md ("EXIT decimal 0..255"; "0 consistent,1 invalid,2 usage/environment").

No production writes. Read-only git (cat-file) via explicit -C. TMPDIR stays in scratch.
"""
import hashlib, json, os, pathlib, re, subprocess, sys

SCRATCH = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe09')
LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
REF = LANE / 'corpus/evidence/round65/controls/ref-receipt-pin.py'
FREEZE = 'f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd'
REL = 'SKILL.md'
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')

# --- canonical valid receipt (same construction recipe as the frozen counter) ---
raw = subprocess.run(['git', '-C', str(LANE), 'cat-file', 'blob', f'{FREEZE}:{REL}'],
                     capture_output=True, check=True).stdout
DIGEST = hashlib.sha256(raw).hexdigest()
VALID = f'REVISION={FREEZE}\nEXIT=0\nSHA256={DIGEST} {REL}\n\nmeasured output\n'

def receipt(exit_token: str) -> str:
    return f'REVISION={FREEZE}\nEXIT={exit_token}\nSHA256={DIGEST} {REL}\n\nmeasured output\n'

# --- independent expectation, derived from frozen claims.md text only ---
# Format rule: "EXIT decimal 0..255". Canonical decimal for an integer in [0,255] has
# no sign, no leading zeros (except the numeral "0" itself). Receipt-content problems
# are "invalid" -> exit 1; only argv/environment problems are "usage/environment" -> exit 2.
def expected(exit_token: str):
    if not re.fullmatch(r'[0-9]+', exit_token):
        return 1, 'non-decimal/signed'
    if len(exit_token) > 1 and exit_token[0] == '0':
        return 1, 'non-canonical (leading zero)'
    if int(exit_token) > 255:
        return 1, 'out of range 0..255'
    return 0, 'canonical decimal in 0..255'

CASES = [
    # (name, receipt text or None->argv probe, expected exit, note)
    ('control-valid',       receipt('0'),      0, 'in-range baseline; also harness sanity control'),
    ('nonzero-valid',       receipt('1'),      0, 'in-range nonzero'),
    ('max-exit',            receipt('255'),    0, 'range boundary, must stay consistent'),
    ('overflow-256',        receipt('256'),    1, 'minimal overflow (frozen counter case name)'),
    ('overflow-999',        receipt('999'),    1, 'largest 3-digit'),
    ('overflow-1000',       receipt('1000'),   1, '4-digit: range + width overflow'),
    ('overflow-65535',      receipt('65535'),  1, 'width-5 overflow'),
    ('leading-zero-0255',   receipt('0255'),   1, 'numerically in range, non-canonical decimal'),
    ('leading-zeros-000',   receipt('000'),    1, 'zero with leading zeros'),
    ('negative-exit',       receipt('-1'),     1, 'signed'),
    ('plus-exit',           receipt('+1'),     1, 'explicit sign'),
    ('empty-value',         receipt(''),       1, 'bare EXIT='),
    ('hexish-exit',         receipt('0xff'),   1, 'non-decimal alphabet'),
    ('space-padded-exit',   receipt(' 255'),   1, 'whitespace inside header value'),
    ('bad-revision-argv',   VALID,             2, 'argv probe: uppercase --revision -> usage/environment, not exit 1'),
]

def run_ref(receipt_path: pathlib.Path, revision: str):
    q = subprocess.run([sys.executable, '-B', str(REF), '--receipt', str(receipt_path),
                        '--root', str(LANE), '--revision', revision],
                       capture_output=True, text=True, timeout=20)
    return q.returncode, q.stdout, q.stderr

def main():
    (SCRATCH / 'tmp').mkdir(parents=True, exist_ok=True)
    rdir = SCRATCH / 'receipts'
    rdir.mkdir(exist_ok=True)
    rows, all_agree = [], True
    for name, text, exp_rc, note in CASES:
        f = rdir / f'{name}.txt'
        f.write_text(text)
        revision = FREEZE if name != 'bad-revision-argv' else 'F' * 40
        rc, out, err = run_ref(f, revision)
        if name != 'bad-revision-argv':
            exp_rc_ind, why = expected(text.splitlines()[1][5:])
        else:
            exp_rc_ind, why = 2, 'usage/environment partition'
        agree = (rc == exp_rc == exp_rc_ind)
        fail_shape = (rc == 0 and out.strip() == 'RECEIPT_PIN=PASS') or \
                     (rc != 0 and out.startswith('RECEIPT_PIN=FAIL '))
        all_agree &= agree
        rows.append({
            'case': name, 'expect': exp_rc_ind, 'expect_why': why,
            'actual_rc': rc, 'actual_stdout': out.strip(), 'actual_stderr': err.strip(),
            'agree': agree, 'frozen_fail_token_shape': fail_shape, 'note': note,
        })
        print(f'{name:22s} expect={exp_rc_ind} actual={rc} agree={agree} out={out.strip()!r}')
    verdict = {'freeze': FREEZE, 'revision': FREEZE, 'blob': f'{FREEZE}:{REL}',
               'digest': DIGEST, 'all_agree': bool(all_agree), 'cases': rows}
    (SCRATCH / 'probe09-overflow-exit-results.json').write_text(json.dumps(verdict, indent=2) + '\n')
    print(f'ALL_AGREE={all_agree}')
    return 0 if all_agree else 1

if __name__ == '__main__':
    sys.exit(main())
