#!/usr/bin/env python3
"""Round27 post-falsify controls: discriminating inputs named by the falsify wave.

Run from the lane root: python3 corpus/evidence/round27-falsify-controls.py --gate tools/research-gate.sh
Exit0 every expectation matched; exit1 mismatch; exit2 setup. Synthetic temp fixtures only;
no network, host files or live-process probes. Each control names the falsify report
(.ufo/waves/round-27/falsify/<report>.md) whose counterexample or surviving mutant it encodes.
Expectations come from the frozen claims text (corpus/evidence/round27-claims.md), Python
datetime, or GFM table rules -- never from gate output. round27-regressions.py stays unchanged.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from datetime import date, timedelta

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--gate', required=True, type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
gate = args.gate.resolve()
if not gate.is_file():
    parser.error('gate must be an existing file')
text = gate.read_text()
results = []
env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_')}
env.update(CHOUSA_STRICT='0', LC_ALL='C')
VERDICT = r'^RESEARCH_GATE: '


def observe(claim, name, report, result, expected_rc, required=(), forbidden=(), counts=None):
    output = result.stdout + result.stderr
    errors = []
    if result.returncode != expected_rc:
        errors.append(f'exit {result.returncode} != {expected_rc}')
    errors += [f'missing {item!r}' for item in required if item not in output]
    errors += [f'forbidden {item!r}' for item in forbidden if item in output]
    for pattern, expected in (counts or {}).items():
        actual = len(re.findall(pattern, output, re.MULTILINE))
        if actual != expected:
            errors.append(f'count {pattern!r}: {actual} != {expected}')
    results.append(dict(claim=claim, name=name, report=report, expected_exit=expected_rc,
                        actual_exit=result.returncode, errors=errors,
                        stdout=result.stdout[-4000:], stderr=result.stderr[-4000:]))


def call(argv, cwd, extra_env=None, timeout=30):
    try:
        return subprocess.run(argv, cwd=cwd, env=env | (extra_env or {}), text=True,
                              capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(exc.cmd, 124, '', f'control timed out after {timeout}s')


with tempfile.TemporaryDirectory(prefix='chousa-r27-falsify-controls-') as directory:
    root = Path(directory)
    knowledge = root / 'corpus/knowledge'
    knowledge.mkdir(parents=True)
    entry = knowledge / 'entry.md'
    relative = 'corpus/knowledge/entry.md'

    def entry_text(source='S001', verified='2026-01-02 checked synthetic fixture', recheck='90d'):
        entry.write_text(f'source: {source}\nverified-at: {verified}\nrecheck: {recheck}\n\n## Claim\nsynthetic\n')

    def run(*options, target=None, timeout=30):
        return call(['bash', str(gate), 'verify-metadata', str(target or entry), '--root', str(root),
                     *map(str, options)], root, timeout=timeout)

    # C1: the shipped usage helper must fail closed on a matcher fault and count only
    # column-0 `RESEARCH_GATE: ` records (claims C1: anchored records, missing diagnostic fails).
    stub = root / 'synthetic-cli.sh'
    stub.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$FAKE_OUTPUT"\nexit "$FAKE_RC"\n')
    faulty = root / 'faulty-bin'
    faulty.mkdir()
    (faulty / 'grep').write_text('#!/bin/sh\nexit 2\n')
    (faulty / 'grep').chmod(0o755)
    usage = 'expected diagnostic\nusage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT\n'
    helpers = []
    for name in ('metadata_asof_usage_accepts', 'metadata_asof_usage_case'):
        match = re.search(r'^  ' + name + r'\(\).*?^  }\n', text, re.M | re.S)
        if match is None:
            parser.error(f'usage selftest helper not found: {name}')
        helpers.append(match.group(0))
    script = ('cases=0; failures=0; SELF=$1\n' + '\n'.join(helpers) +
              '\nmetadata_asof_usage_case fixture "expected diagnostic"\nexit "$failures"\n')
    for name, report, rc, output, expected, path_prefix in [
        ('matcher-fault-fails-closed', 'FC1CorrectUsageWithHelp00', 2, usage, 1, str(faulty) + ':'),
        ('indented-mention-is-not-record', 'FC1NonrecordMentionIsNotV05', 2, usage + '  RESEARCH_GATE: CLEAN\n', 0, ''),
        ('column0-other-record-rejected', 'FC1NonrecordMentionIsNotV05', 2, usage + 'RESEARCH_GATE: PENDING\n', 1, ''),
        ('different-diagnostic-rejected', 'FC1RejectMissingDiagnosti04', 2, 'other diagnostic\nusage: fixture\n', 1, ''),
        ('exit-zero-rejected', 'FC1RejectWrongExit03', 0, usage, 1, ''),
    ]:
        result = call(['bash', '-c', script, 'fixture', str(stub)], root,
                      {'FAKE_RC': str(rc), 'FAKE_OUTPUT': output, 'PATH': path_prefix + env.get('PATH', '')})
        observe('C1', name, report, result, expected, forbidden=('command not found',))

    # C2: Gregorian validity of --as-of, one significant digit after zeros, the 8-19 digit
    # window, and an admissible 4 MiB zero run inside the 8 MiB entry cap.
    entry_text(verified='2000-02-01 checked synthetic fixture')
    for token, report, rc in [('2100-02-29', 'FC2Leap210019', 2), ('1900-02-29', 'FC2Leap190016', 2)]:
        observe('C2', f'as-of-invalid-leap-{token}', report, run('--as-of', token), rc,
                ('--as-of must be a valid YYYY-MM-DD date',), counts={VERDICT: 0})
    observe('C2', 'as-of-valid-leap-2000-02-29', 'FC2Leap200017', run('--as-of', '2000-02-29'), 0,
            ('due=2000-05-01 freshness=current',), counts={VERDICT: 1})
    date_cases = [
        ('one-significant-after-zeros', 'FC2Leading128KZeros06', '2026-01-01', '0007d', '2026-01-08'),
        ('twenty-char-value-seven', 'FC2Leading128KZeros06', '2026-01-01', '0' * 19 + '7d', '2026-01-08'),
        ('eight-digit-unknown', 'FC2HugeMagnitude08', '2026-01-01', '99999999d', None),
        ('nineteen-digit-unknown', 'FC2HugeMagnitude08', '2026-01-01', '9223372036854775807d', None),
        ('scale-4mib-leading-zeros', 'FC2Allzero128K07', '2026-01-02', '0' * 4194304 + '90d', '2026-04-02'),
    ]
    for name, report, verified, recheck, due in date_cases:
        entry_text(verified=verified + ' checked synthetic fixture', recheck=recheck)
        asof = '2026-01-08'
        if due is not None:
            assert date.fromisoformat(verified) + timedelta(days=int(recheck[:-1].lstrip('0') or '0')) == date.fromisoformat(due)
        freshness = 'unknown' if due is None else ('overdue' if date.fromisoformat(asof) > date.fromisoformat(due) else 'current')
        observe('C2', name, report, run('--as-of', asof, timeout=60), int(freshness == 'overdue'),
                (f'due={due or "unknown"} freshness={freshness}',),
                counts={VERDICT: 1, r'^META entry=': 1})

    # C3: GFM cell width (escaped pipes are content), mixed outer pipes, no header across a
    # blank line, a consulted row (findings=0 and its queued twin), single-leg raw-path refusal.
    entry_text()
    registry = root / 'registry.md'
    row = f'| S001 | mined | {relative} |\n'
    escaped = '| id | status | used-by | note \\| alt |\n'
    tables = [
        ('escaped-pipe-width', 'FC3ValidTable27', escaped + '|---|---|---|---|\n' + f'| S001 | mined | {relative} | x |\n', 0),
        ('escaped-pipe-overwide', 'FC3ValidTable27', escaped + '|---|---|---|---|---|\n' + f'| S001 | mined | {relative} | x |\n', 2),
        ('mixed-header-outer-only', 'FC3ValidTable27', '| id | status | used-by |\n---|---|---\n' + row, 0),
        ('mixed-delimiter-outer-only', 'FC3ValidTable27', 'id | status | used-by\n|---|---|---|\n' + row, 0),
        ('mixed-lead-pipe-header', 'FC3ValidTable27', '| id | status | used-by\n|---|---|---|\n' + row, 0),
        ('mixed-lead-pipe-delimiter', 'FC3ValidTable27', '| id | status | used-by |\n|---|---|---\n' + row, 0),
        ('mixed-trail-pipe-delimiter', 'FC3ValidTable27', '| id | status | used-by |\n---|---|---|\n' + row, 0),
        ('delimiter-after-blank', 'FC3HeaderBreakBlank28', '| id | status | used-by |\n\n|---|---|---|\n' + row, 2),
        ('valid-table-consulted', 'FC3ValidTable27', '| id | status | used-by |\n|---|---|---|\n' + row, 0),
        ('valid-table-queued-twin', 'FC3ValidTable27', '| id | status | used-by |\n|---|---|---|\n' + row.replace('mined', 'queued'), 1),
        ('escaped-before-status-queued', 'residual/ResControlsSuite', '| id | note \\| x | status | used-by |\n|---|---|---|---|\n' + f'| S001 | n | queued | mined | {relative} |\n', 1),
        ('escaped-before-status-mined', 'residual/ResControlsSuite', '| id | note \\| x | status | used-by |\n|---|---|---|---|\n' + f'| S001 | n | mined | {relative} |\n', 0),
        ('escaped-body-cell-before-status', 'residual/ResControlsSuite', '| id | note \\| x | status | used-by |\n|---|---|---|---|\n' + f'| S001 | n \\| queued | mined | {relative} |\n', 0),
        ('escaped-final-header-cell-no-outer-pipe', 'residual/ResWidthFix', '| id | status | used-by | note \\|\n|---|---|---|---|\n' + f'| S001 | mined | {relative} | n |\n', 0),
    ]
    for name, report, table, rc in tables:
        registry.write_text(table)
        if rc == 2:
            observe('C3', name, report, run('--registry', registry), 2,
                    ('metadata registry has no table',), counts={VERDICT: 0})
        elif rc == 1:
            observe('C3', name, report, run('--registry', registry), 1,
                    counts={r'^FINDING META_SOURCE_NOT_MINED\b': 1, r'^FINDING ': 1, VERDICT: 1})
        else:
            observe('C3', name, report, run('--registry', registry), 0,
                    ('findings=0 drift=0',), counts={r'^FINDING ': 0, VERDICT: 1})
    benign_registry = root / 'benign-registry.md'
    benign_registry.write_text('| id | status | used-by |\n|---|---|---|\n' + row)
    raw_registry = root / 'synthetic:fixture/.config/registry-link.md'
    raw_registry.parent.mkdir(parents=True)
    raw_registry.symlink_to(benign_registry)
    observe('C3', 'registry-raw-leg-only', 'FC3RegistryColonDeniedCan48', run('--registry', raw_registry), 2,
            ('metadata registry refused: denylist',), counts={VERDICT: 0})
    benign_entry = root / 'benign-entry.md'
    benign_entry.write_text(entry.read_text())
    raw_entry = root / 'synthetic:fixture/.config/entry-link.md'
    raw_entry.symlink_to(benign_entry)
    observe('C3', 'entry-raw-leg-only-reason', 'FC3EntryColonDeniedCompon50', run(target=raw_entry), 1,
            ('META_ENTRY_REFUSED', 'reason=denylist'), counts={VERDICT: 1})
    benign_source = root / 'benign-source.md'
    benign_source.write_text('synthetic span text\n')
    raw_source = root / 'synthetic:fixture/.config/source-link.md'
    raw_source.symlink_to(benign_source)
    claims = root / 'claims.jsonl'
    claims.write_text(json.dumps({'id': 'C1', 'source': str(raw_source), 'span': 'synthetic span',
                                  'expect': 'supported'}) + '\n')
    observe('C3', 'claims-raw-leg-only', 'FC3ClaimsRawColonDenied55',
            call(['bash', str(gate), 'verify-claims', str(claims), '--root', str(root)], root), 1,
            ('FINDING CLAIM_SOURCE_SESSION',), ('observed=supported',), {VERDICT: 1})

    # A scanner dependency fault cannot turn a queued source into informational
    # "no S-id" and CLEAN. Fault only scanner-specific options; other grep uses
    # remain real, so this is not a generic setup-failure witness.
    import shlex
    import shutil
    real_grep = shutil.which('grep')
    if real_grep is None:
        parser.error('grep executable is required')
    entry_text(source='S002')
    registry.write_text('| id | status | used-by |\n|---|---|---|\n'
                        + f'| S002 | queued | {relative} |\n')
    for scanner_option in ('-oE', '-xE'):
        (faulty / 'grep').write_text(
            '#!/bin/sh\nfor arg do\ncase "$arg" in ' + scanner_option
            + ') exit 2;; esac\ndone\nexec ' + shlex.quote(real_grep) + ' "$@"\n')
        observe('C3', 'source-scanner-fault-' + scanner_option,
                '../residual/ResTokenPrefilter',
                call(['bash', str(gate), 'verify-metadata', str(entry), '--root', str(root),
                      '--registry', str(registry)], root,
                     {'PATH': str(faulty) + ':' + env.get('PATH', '')}), 1,
                ('META_SOURCE_SCAN_FAILED',), ('META_SOURCE_NO_ROW_ID',),
                {VERDICT: 1, r'^FINDING META_SOURCE_SCAN_FAILED\b': 1, r'^FINDING ': 1})

summary = {'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(),
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'total': len(results), 'mismatches': sum(bool(r['errors']) for r in results),
           'claims': {claim: {'total': sum(r['claim'] == claim for r in results),
                              'mismatches': sum(r['claim'] == claim and bool(r['errors']) for r in results)}
                      for claim in ('C1', 'C2', 'C3')}, 'results': results}
print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, indent=2))
for item in results:
    if item['errors']:
        print('MISMATCH', item['claim'], item['name'], item['report'], '; '.join(item['errors']))
if args.output:
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
raise SystemExit(int(summary['mismatches'] != 0))
