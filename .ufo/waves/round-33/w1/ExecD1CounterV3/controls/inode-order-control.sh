#!/usr/bin/env bash
# NEGATIVE CONTROL ONLY: never read any citation source bytes.
exec python3 - "$@" <<'PY'
import os
import sys

args = sys.argv[1:]
if len(args) != 4 or args[0] != 'verify-chain' or args[2] != '--root':
    raise SystemExit(2)
record, root = os.path.realpath(args[1]), os.path.realpath(args[3])
sections = {}
section = ''
# The record is read; the cited sources are only stat'ed.
with open(record, encoding='utf-8') as handle:
    for raw in handle:
        line = raw.strip()
        if line.startswith('## '):
            section = line[3:].strip()
        elif line.startswith('|'):
            sections.setdefault(section, []).append([cell.strip() for cell in line.split('|')[1:-1]])

def table(name):
    rows = sections.get(name, [])
    if len(rows) < 2:
        return []
    return [dict(zip(rows[0], row)) for row in rows[2:]]

sources = {row['id']: row['pointer'] for row in table('Sources')}
entries = []
with os.scandir(root) as scan:
    for entry in scan:
        if entry.is_file(follow_symlinks=False) and os.path.realpath(entry.path) != record:
            stat = entry.stat(follow_symlinks=False)
            entries.append((stat.st_ino, os.path.realpath(entry.path)))
# VARIANT (D1 control b): rank by inode alone. Generator creates R1, R2, R3
# (12 sources each) before every negative under v2; this is a fixture-order
# shortcut, not anchor verification.
positive_paths = {path for _, path in sorted(entries)[:36]}
findings = []
verified = 0
hops = table('Chain')
for row in hops:
    hop, status = row['hop'], row['status']
    to = row['to'].split('#', 1)[0]
    pointer = sources.get(to, to)
    candidate = os.path.realpath(os.path.join(root, pointer))
    if status == 'resolved':
        observed, verdict = 'verified', 'match'
        verified += 1
    elif status in ('unresolved', 'blocked-no-fetch', 'labelled-dead') and candidate in positive_paths:
        observed, verdict = 'resolvable', 'mismatch'
        findings.append('FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=' + hop)
    else:
        observed, verdict = 'exempt', 'exempt'
    print(f'CHAIN hop={hop} status={status} observed={observed} source={to} anchor=- at=- verdict={verdict}')
for finding in findings:
    print(finding)
print(f'RESOLVED_HOPS={verified}/{len(hops)}')
print('RESEARCH_GATE: ' + ('DRIFT' if findings else 'CLEAN'))
raise SystemExit(1 if findings else 0)
PY
