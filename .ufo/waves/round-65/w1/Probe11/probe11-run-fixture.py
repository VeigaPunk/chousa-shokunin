#!/usr/bin/env python3
"""Probe11 isolated fixture: receipt-pin 'no-digest' surface only.

Builds an isolated fixture git repo under the scratch seat dir, crafts the
frozen-format receipt with the entire SHA256= header line removed, and runs
the round65 reference validator (controls/ref-receipt-pin.py) against it.
Also cross-checks the same no-digest receipt text against the frozen BASE
blob (d6ed8155...:SKILL.md) read-only from the lane repo.

Expected result derived independently from the frozen format in claims.md:
  - line 2 must match SHA256=<64 lowercase hex> <repo-relative path>
  - with the SHA256 line absent, regex match fails -> ValueError('digest header')
  - validator prints RECEIPT_PIN=FAIL <msg> and exits 1
No production writes. Fixture git mutations happen only inside the scratch
fixture repo after asserting rev-parse toplevel == that repo.
"""
import hashlib, pathlib, subprocess, sys

SEAT = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Probe11')
REPO = SEAT / 'repo'
RECEIPTS = SEAT / 'receipts'
LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
REF = LANE / 'corpus/evidence/round65/controls/ref-receipt-pin.py'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
ART = 'artifact-r65.txt'
BODY = 'measured output\n'

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30, **kw)

def runb(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, timeout=30, **kw)

def main():
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    transcript = []

    # --- fixture repo (isolated; mutations only here) ---
    top = run(['git', '-C', str(REPO), 'rev-parse', '--show-toplevel'])
    assert top.returncode == 0 and top.stdout.strip() == str(REPO), (
        f'fixture guard failed: {top.stdout!r} {top.stderr!r}')
    (REPO / ART).write_text('probe11 fixture artifact\n', encoding='utf-8')
    c = run(['git', '-C', str(REPO), 'add', ART])
    assert c.returncode == 0, c.stderr
    c = run(['git', '-C', str(REPO), 'commit', '-m', 'probe11 fixture'])
    assert c.returncode == 0, c.stderr
    rev = run(['git', '-C', str(REPO), 'rev-parse', 'HEAD']).stdout.strip()
    assert len(rev) == 40 and all(ch in '0123456789abcdef' for ch in rev), rev
    blob = runb(['git', '-C', str(REPO), 'cat-file', 'blob', f'{rev}:{ART}'], check=False)
    assert blob.returncode == 0, blob.stderr.decode('utf-8', 'replace')
    digest = hashlib.sha256(blob.stdout).hexdigest()
    transcript.append(f'fixture revision={rev}')
    transcript.append(f'fixture sha256({ART})={digest}')

    # --- receipts ---
    valid = f'REVISION={rev}\nEXIT=0\nSHA256={digest} {ART}\n\n{BODY}'
    no_digest = valid.replace(f'SHA256={digest} {ART}\n', '')
    (RECEIPTS / 'valid.txt').write_text(valid, encoding='utf-8')
    nd = RECEIPTS / 'no-digest.txt'
    nd.write_text(no_digest, encoding='utf-8')
    transcript.append('--- no-digest receipt text (repr) ---')
    transcript.append(repr(no_digest))

    # --- run reference on no-digest, fixture substrate ---
    q = run([sys.executable, '-B', str(REF), '--receipt', str(nd),
             '--root', str(REPO), '--revision', rev])
    transcript.append(f'[fixture] rc={q.returncode} stdout={q.stdout!r} stderr={q.stderr!r}')

    # --- cross-check: same no-digest shape vs frozen BASE blob, lane read-only ---
    base_blob = runb(['git', '-C', str(LANE), 'cat-file', 'blob', f'{BASE}:SKILL.md'])
    assert base_blob.returncode == 0, base_blob.stderr.decode('utf-8', 'replace')
    h = hashlib.sha256(base_blob.stdout).hexdigest()
    frozen_valid = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\n{BODY}'
    frozen_nd = frozen_valid.replace(f'SHA256={h} SKILL.md\n', '')
    fnd = RECEIPTS / 'no-digest-frozen-base.txt'
    fnd.write_text(frozen_nd, encoding='utf-8')
    q2 = run([sys.executable, '-B', str(REF), '--receipt', str(fnd),
              '--root', str(LANE), '--revision', BASE])
    transcript.append(f'[frozen-base] rc={q2.returncode} stdout={q2.stdout!r} stderr={q2.stderr!r}')

    # --- sanity: valid receipt passes on fixture substrate ---
    q3 = run([sys.executable, '-B', str(REF), '--receipt', str(RECEIPTS / 'valid.txt'),
              '--root', str(REPO), '--revision', rev])
    transcript.append(f'[valid-control] rc={q3.returncode} stdout={q3.stdout!r}')

    # --- production target presence check (read-only stat) ---
    target = LANE / 'tools/receipt-pin.py'
    transcript.append(f'production target exists: {target.is_file()}')

    ok = (q.returncode == 1 and q.stdout.startswith('RECEIPT_PIN=FAIL ')
          and q2.returncode == 1 and q2.stdout.startswith('RECEIPT_PIN=FAIL ')
          and q3.returncode == 0 and q3.stdout.strip() == 'RECEIPT_PIN=PASS')
    transcript.append(f'PROBE_VERDICT={"PASS" if ok else "FAIL"}')
    (SEAT / 'transcript.txt').write_text('\n'.join(transcript) + '\n', encoding='utf-8')
    print('\n'.join(transcript))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
