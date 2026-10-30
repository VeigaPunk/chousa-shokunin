#!/usr/bin/env python3
"""Probe12 isolated fixture: wrong-digest surface of R65-C1 receipt-pin format.

Independent expectation is derived ONLY from the frozen spec text in claims.md:
  - "SHA256 full lowercase 64 hex plus canonical relative POSIX path"
  - "Digest binds the Git blob at the declared revision"
  - "0 consistent,1 invalid,2 usage/environment"
  - frozen counter predicate: rc==1 cases must print a line starting "RECEIPT_PIN=FAIL "

Therefore a well-formed receipt whose declared digest does not equal the blob digest
at the declared revision is inconsistent -> exit 1, stdout starts with "RECEIPT_PIN=FAIL ".
No reference-tool code is consulted for expectations.
"""
import hashlib, json, pathlib, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
REF = LANE + '/corpus/evidence/round65/controls/ref-receipt-pin.py'
WORK = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe12/work')

# 1. Independently derive the true blob digest (read-only git, explicit -C).
q = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', BASE + ':SKILL.md'],
                   capture_output=True, check=True)
h = hashlib.sha256(q.stdout).hexdigest()

valid = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'
flip = h[:-1] + ('0' if h[-1] != '0' else '1')

cases = [
    ('control-valid', valid, 0),
    ('wrong-digest-zeros', valid.replace(h, '0' * 64), 1),   # counter's wrong-digest construction
    ('wrong-digest-flip', valid.replace(h, flip), 1),        # same surface, different wrong value
]
assert flip != h and '0' * 64 != h, 'fixture degenerate: wrong digest equals true digest'

rows = []
all_agree = True
for name, text, expect_rc in cases:
    f = WORK / (name + '.txt')
    f.write_text(text)
    q2 = subprocess.run(
        [sys.executable, '-B', REF, '--receipt', str(f), '--root', LANE, '--revision', BASE],
        capture_output=True, text=True, timeout=20,
        env={'PATH': '/usr/bin:/bin', 'TMPDIR': '/fast/scratch/hyaku/chousa-r65/Probe12/tmp'},
    )
    expect_prefix = 'RECEIPT_PIN=PASS' if expect_rc == 0 else 'RECEIPT_PIN=FAIL '
    agree = (q2.returncode == expect_rc) and q2.stdout.startswith(expect_prefix)
    all_agree &= agree
    rows.append({
        'case': name, 'expect_rc': expect_rc,
        'expect_stdout_prefix': expect_prefix,
        'actual_rc': q2.returncode, 'actual_stdout': q2.stdout, 'actual_stderr': q2.stderr,
        'agree': agree,
        'declared_digest_matches_blob': ('SHA256=' + h + ' ') in text,
    })
    print(f'{name}: expect rc={expect_rc} prefix={expect_prefix!r} '
          f'actual rc={q2.returncode} stdout={q2.stdout!r} stderr={q2.stderr!r} agree={agree}')

out = WORK / 'probe12-wrong-digest-results.json'
out.write_text(json.dumps({
    'lane': LANE, 'base': BASE, 'blob_bytes': len(q.stdout), 'true_blob_sha256': h,
    'reference': REF, 'argv_shape': '--receipt <file> --root <lane> --revision <BASE>',
    'rows': rows, 'ALL_AGREE': all_agree,
}, indent=1))
print('ALL_AGREE=' + str(all_agree))
sys.exit(0 if all_agree else 1)
