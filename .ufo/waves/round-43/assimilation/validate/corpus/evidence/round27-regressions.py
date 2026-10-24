#!/usr/bin/env python3
"""Independent r27 contract controls; local synthetic fixtures, no network/host probes.

Run from the lane root: python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh
Exit0 means every declared expectation matched; exit1 mismatch; exit2 setup.
The reported r26 failures are retained evidence, not reproduced by this script.
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


def observe(claim, name, result, expected_rc, required=(), forbidden=(), counts=None):
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
    results.append(dict(claim=claim, name=name, expected_exit=expected_rc,
                        actual_exit=result.returncode, errors=errors,
                        stdout=result.stdout, stderr=result.stderr))


with tempfile.TemporaryDirectory(prefix='chousa-r27-synthetic-') as directory:
    root = Path(directory)
    knowledge = root / 'corpus/knowledge'
    knowledge.mkdir(parents=True)
    entry = knowledge / 'entry.md'
    registry = root / 'registry.md'
    relative = 'corpus/knowledge/entry.md'
    header = '| id | status | used-by |\n|---|---|---|\n'
    row = f'| S001 | mined | {relative} |\n'

    def entry_text(source='S001', verified='2026-01-02 checked synthetic fixture', recheck='90d'):
        entry.write_text(f'source: {source}\nverified-at: {verified}\nrecheck: {recheck}\n\n## Claim\nsynthetic\n')

    def run(*options, locale='C'):
        try:
            return subprocess.run(['bash', str(gate), 'verify-metadata', str(entry),
                                   '--root', str(root), *map(str, options)],
                                  cwd=root, env=env | {'LC_ALL': locale},
                                  text=True, capture_output=True, timeout=30)
        except subprocess.TimeoutExpired as exc:
            return subprocess.CompletedProcess(exc.cmd, 124, '', 'synthetic control timed out')

    # Exercise the exact shipped usage helper in isolation, not a duplicated predicate.
    stub = root / 'synthetic-cli.sh'
    stub.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$FAKE_OUTPUT"\nexit "$FAKE_RC"\n')
    usage = 'expected diagnostic\nusage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT\n'
    helpers = []
    for name in ('metadata_asof_usage_accepts', 'metadata_asof_usage_case'):
        match = re.search(r'^  ' + name + r'\(\).*?^  }\n', text, re.M | re.S)
        if match is None:
            parser.error(f'usage selftest helper not found: {name}')
        helpers.append(match.group(0))
    scenarios = [
        ('correct-usage-with-help', 2, usage, 0),
        ('reject-clean-verdict', 2, usage + 'RESEARCH_GATE: CLEAN\n', 1),
        ('reject-drift-verdict', 2, usage + 'RESEARCH_GATE: DRIFT\n', 1),
        ('reject-wrong-exit', 1, usage, 1),
        ('reject-missing-diagnostic', 2, 'usage only\n', 1),
        ('nonrecord-mention-is-not-verdict', 2, usage + 'note RESEARCH_GATE: not a record\n', 0),
    ]
    for name, rc, output, expected in scenarios:
        script = ('cases=0; failures=0; SELF=$1\n' + '\n'.join(helpers) +
                  '\nmetadata_asof_usage_case fixture "expected diagnostic"\nexit "$failures"\n')
        result = subprocess.run(['bash', '-c', script, 'fixture', str(stub)], cwd=root,
                                env=env | {'FAKE_RC': str(rc), 'FAKE_OUTPUT': output},
                                text=True, capture_output=True, timeout=30)
        observe('C1', name, result, expected, forbidden=('command not found',))

    # Calendar expectations derive from Python datetime, not the gate arithmetic.
    date_cases = [
        ('leading-128k-zeros', '2026-01-02', '0' * 131072 + '90d', '2026-10-21', '2026-04-02'),
        ('allzero-128k', '2026-01-02', '0' * 131072 + 'd', '2026-01-02', '2026-01-02'),
        ('huge-magnitude', '2026-01-02', '9' * 40 + 'd', '2026-10-21', None),
        ('one-then-39-zeros', '2026-01-02', '1' + '0' * 39 + 'd', '2026-10-21', None),
        ('pow64-plus-90', '2026-01-02', '18446744073709551706d', '2026-10-21', None),
        ('max-span', '0001-01-01', '0003652058d', '9999-12-31', '9999-12-31'),
        ('overflow-span', '0001-01-01', '3652059d', '9999-12-31', None),
        ('max-date-overflow', '9999-12-31', '1d', '9999-12-31', None),
        ('decimal08', '2026-01-01', '08d', '2026-01-09', '2026-01-09'),
        ('decimal09-overdue', '2026-01-01', '09d', '2026-01-11', '2026-01-10'),
    ]
    for year in (1900, 2000, 2028, 2100):
        start = date(year, 2, 28)
        due = start + timedelta(days=1)
        date_cases.append((f'leap-{year}', start.isoformat(), '1d', due.isoformat(), due.isoformat()))
    for name, verified, recheck, asof, due in date_cases:
        entry_text(verified=verified + ' checked synthetic fixture', recheck=recheck)
        freshness = 'unknown' if due is None else ('overdue' if date.fromisoformat(asof) > date.fromisoformat(due) else 'current')
        observe('C2', name, run('--as-of', asof), int(freshness == 'overdue'),
                (f'due={due or "unknown"} freshness={freshness}',),
                counts={r'^RESEARCH_GATE: ': 1, r'^META entry=': 1})
    entry_text(recheck='0' * 131072 + '90d')
    observe('C2', 'long-zero-plain-mode', run(), 0,
            ('recheck=scheduled verdict=clean',), (' due=', ' freshness='),
            {r'^RESEARCH_GATE: ': 1})
    entry_text()
    for locale in ('C', 'en_US.UTF-8'):
        for token in ('２０２６-10-21', '٢٠٢٦-10-21', '2026-10-2１'):
            observe('C2', f'ascii-cli-{locale}-{token}', run('--as-of', token, locale=locale), 2,
                    ('--as-of must be a valid YYYY-MM-DD date',),
                    ('invalid integer', 'arithmetic syntax', 'cannot change locale'),
                    {r'^RESEARCH_GATE: ': 0})

    # Named-header state and ID occurrence expectations are explicit, not code sets.
    entry_text()
    tables = [
        ('valid-table', header + row, 0, None),
        ('header-break-blank', '| id | status | used-by |\n\n| a | b | c |\n|---|---|---|\n' + row, 2, None),
        ('header-break-prose', '| id | status | used-by |\nprose\n| a | b | c |\n|---|---|---|\n' + row, 2, None),
        ('reorder-clean', '| id | status | used-by |\nprose\n| id | note | status | used-by |\n|---|---|---|---|\n' + f'| S001 | ignored | mined | {relative} |\n', 0, None),
        ('reorder-queued', '| id | status | used-by |\nprose\n| id | note | used-by | status |\n|---|---|---|---|\n' + f'| S001 | mined | {relative} | queued |\n', 1, 'META_SOURCE_NOT_MINED'),
        ('delimiter-too-short', '| id | status | used-by |\n|---|---|\n' + row, 2, None),
        ('delimiter-too-long', '| id | status | used-by |\n|---|---|---|---|\n' + row, 2, None),
        ('valid-no-outer-pipes', 'id | status | used-by\n---|---|---\n' + f'S001 | mined | {relative}\n', 0, None),
        ('valid-crlf', (header + row).replace('\n', '\r\n'), 0, None),
        ('valid-aligned', '| id | status | used-by |\n|:---|---:|:---:|\n' + row, 0, None),
    ]
    for name, table, rc, finding in tables:
        registry.write_text(table)
        required = (finding,) if finding else ()
        if rc == 2:
            required = ('metadata registry has no table',)
        observe('C3', name, run('--registry', registry), rc, required,
                counts={r'^RESEARCH_GATE: ': int(rc != 2)})
    registry.write_text(header + row + '| S002 | queued | — |\n')
    for name, source, rc, occurrences in [
        ('glued-before-terminal', 'see S001S002 and S001', 0, 0),
        ('glued-missing-before-terminal', 'see S001S003 and S001', 0, 0),
        ('underscore-glued', 'xS002 S002x _S002 S002_ S001', 0, 0),
        ('nonstandalone-duplicate', 'ref S002x and S002', 1, 1),
        ('glued-repeat-duplicate', 'ref S002S002 and S002', 1, 1),
        ('two-real-occurrences', 'S002,S002', 1, 2),
        ('adjacent-real-ids', 'S001,S002', 1, 1),
    ]:
        entry_text(source=source)
        observe('C3', name, run('--registry', registry), rc,
                counts={r'^FINDING META_SOURCE_NOT_MINED\b[^\n]* source_id=S002(?: |$)': occurrences,
                        r'^FINDING META_SOURCE_': occurrences})
    entry_text()
    for name, protected in [
        ('plain-denied-component', root / '.config/registry.md'),
        ('colon-denied-component', root / 'synthetic:fixture/.config/registry.md'),
        ('colon-denied-suffix', root / 'synthetic:fixture.env'),
        ('legacy-env-anchor-refusal', root / 'synthetic.env:1'),
    ]:
        protected.parent.mkdir(parents=True, exist_ok=True)
        protected.write_text(header + row)
        observe('C3', name, run('--registry', protected), 2,
                ('metadata registry refused: denylist',), counts={r'^RESEARCH_GATE: ': 0})
    registry_alias = root / 'registry-alias.md'
    registry_alias.symlink_to(root / 'synthetic:fixture/.config/registry.md')
    observe('C3', 'registry-colon-denied-canonical-alias', run('--registry', registry_alias), 2,
            ('metadata registry refused: denylist',), counts={r'^RESEARCH_GATE: ': 0})
    # A colon in a normal pathname is not itself forbidden.
    normal = root / 'synthetic:ordinary.md'
    normal.write_text(header + row)
    observe('C3', 'ordinary-colon-is-allowed', run('--registry', normal), 0,
            counts={r'^RESEARCH_GATE: ': 1})
    # Preserve the entry reader's refusal, including its canonical alias path.
    original_entry = entry
    entry = root / 'synthetic:fixture/.config/entry.md'
    entry_text()
    observe('C3', 'entry-colon-denied-component', run(), 1,
            ('META_ENTRY_REFUSED', 'source=refused'), counts={r'^RESEARCH_GATE: ': 1})
    alias = root / 'entry-alias.md'
    alias.symlink_to(entry)
    entry = alias
    observe('C3', 'entry-colon-denied-canonical-alias', run(), 1,
            ('META_ENTRY_REFUSED', 'source=refused'), counts={r'^RESEARCH_GATE: ': 1})
    entry = original_entry
    registry.write_text(header + row)
    entry_text()
    observe('C3', 'composed-overdue-registry', run('--registry', registry, '--as-of', '2026-10-21'), 1,
            ('due=2026-04-02 freshness=overdue', 'META_RECHECK_OVERDUE'),
            counts={r'^FINDING META_SOURCE_': 0, r'^RESEARCH_GATE: ': 1})
    entry_text(verified='2026-10-21 checked synthetic fixture')
    observe('C3', 'composed-current-registry', run('--registry', registry, '--as-of', '2026-10-21'), 0,
            ('due=2027-01-19 freshness=current',),
            counts={r'^FINDING ': 0, r'^RESEARCH_GATE: ': 1})
    registry.write_text(header + row.replace('mined', 'queued'))
    observe('C3', 'composed-current-queued', run('--registry', registry, '--as-of', '2026-10-21'), 1,
            ('due=2027-01-19 freshness=current',),
            counts={r'^FINDING META_SOURCE_NOT_MINED\b': 1, r'^RESEARCH_GATE: ': 1})
    # Source paths are filesystem inputs too; citations elsewhere keep their wrapper.
    claims = root / 'claims.jsonl'
    for name, source_path in (
        ('claims-raw-colon-denied', root / 'synthetic:fixture/.config/entry.md'),
        ('claims-canonical-colon-denied', alias),
        ('claims-legacy-env-anchor-refused', root / 'synthetic.env:1'),
    ):
        claims.write_text(json.dumps({'id': 'C1', 'source': str(source_path),
                                      'span': 'synthetic', 'expect': 'supported'}) + '\n')
        result = subprocess.run(['bash', str(gate), 'verify-claims', str(claims),
                                 '--root', str(root)], cwd=root, env=env,
                                text=True, capture_output=True, timeout=30)
        observe('C3', name, result, 1, ('FINDING CLAIM_SOURCE_SESSION',),
                counts={r'^RESEARCH_GATE: ': 1})

summary = {'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(),
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'total': len(results), 'mismatches': sum(bool(r['errors']) for r in results),
           'claims': {claim: {'total': sum(r['claim'] == claim for r in results),
                              'mismatches': sum(r['claim'] == claim and bool(r['errors']) for r in results)}
                      for claim in ('C1', 'C2', 'C3')}, 'results': results}
print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, indent=2))
for item in results:
    if item['errors']:
        print('MISMATCH', item['claim'], item['name'], '; '.join(item['errors']))
if args.output:
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
raise SystemExit(int(summary['mismatches'] != 0))
