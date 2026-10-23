#!/usr/bin/env bash
# Disclosed C2 feasibility reference only; not a candidate implementation.
exec python3 - "$@" <<'PY_REFERENCE_C2'
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

LANE_ROOT = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin').resolve()
SOURCE_READ_MAX_BYTES = 8 * 1024 * 1024
ASCII_WS = b' \t\n\r\v\f'
ASCII_PUNCT = b'!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'


def word_byte(value):
    return value is not None and value not in ASCII_WS + ASCII_PUNCT + b"-'"


def edge_ok(data, span, start, left):
    end = start + len(span)
    if left:
        if start == 0:
            return True
        edge = data[start - 1]
        outer = data[start - 2] if start >= 2 else None
        inner = span[0]
    else:
        if end == len(data):
            return True
        edge = data[end]
        outer = data[end + 1] if end + 1 < len(data) else None
        inner = span[-1]
    if edge in b"-'":
        return not (word_byte(outer) and word_byte(inner))
    return edge in ASCII_WS + ASCII_PUNCT


def locate_span(data, span):
    start = data.find(span)
    while start != -1:
        if edge_ok(data, span, start, True) and edge_ok(data, span, start, False):
            first = data.count(b'\n', 0, start) + 1
            return first, first + span.count(b'\n')
        start = data.find(span, start + 1)
    return None


def normalize_pointer(source):
    if source.startswith('`'):
        source = source[1:]
    if source.endswith('`'):
        source = source[:-1]
    return source


def denied_path_value(source):
    patterns = ('*op.env', '*.env', '*server.token*', '*credentials/*', '*/oauth/*',
                '*chrome-profile*', '*Cookies*', '*Login Data*', '*/.omp/*',
                '*/.config/*', '*/.local/state/*', '.omp/*', '.config/*', '.local/state/*')
    return any(fnmatch.fnmatchcase(source, pattern) for pattern in patterns)


def denied_path(source):
    return denied_path_value(source) or denied_path_value(source.split(':', 1)[0])


def in_root(path, root):
    return path == root or root in path.parents


def resolve_source(source, root):
    source = normalize_pointer(source)
    if re.search(r':9222(/|$)|/json(/|list)?$', source) or denied_path(source):
        return None, 'CLAIM_SOURCE_SESSION'
    if re.match(r'^(local|artifact|agent|proc|history)://', source):
        return None, 'CLAIM_SOURCE_EPHEMERAL'
    if re.match(r'^https?://', source):
        return None, 'CLAIM_SOURCE_EXTERNAL'
    candidate = Path(source)
    if not candidate.is_absolute():
        if (root / source).exists():
            candidate = root / source
        elif (LANE_ROOT / source).exists():
            candidate = LANE_ROOT / source
        else:
            candidate = root / source
    try:
        canonical = candidate.resolve()
    except (OSError, ValueError, RuntimeError):
        return None, 'CLAIM_SOURCE_MISSING'
    if denied_path(str(canonical)):
        return None, 'CLAIM_SOURCE_SESSION'
    allowed = [parent for parent in (root, LANE_ROOT) if in_root(canonical, parent)]
    if not allowed:
        return None, 'CLAIM_SOURCE_OUT_OF_CORPUS'
    resolving_root = max(allowed, key=lambda parent: len(str(parent)))
    try:
        info = canonical.stat()
        if not stat.S_ISREG(info.st_mode) or not os.access(canonical, os.R_OK):
            return None, 'CLAIM_SOURCE_MISSING'
        if info.st_nlink != 1:
            return None, 'CLAIM_SOURCE_MULTILINKED'
        if info.st_size > SOURCE_READ_MAX_BYTES:
            return None, 'CLAIM_SOURCE_READ_TOO_LARGE'
        if info.st_dev != resolving_root.stat().st_dev:
            return None, 'CLAIM_SOURCE_CROSS_DEVICE'
    except (OSError, ValueError):
        return None, 'CLAIM_SOURCE_MISSING'
    return canonical, None


def source_sha256(data):
    return hashlib.sha256(data).hexdigest()


def evaluate(record, root, default_marker):
    required = ('id', 'source', 'span', 'expect')
    if any(not isinstance(record.get(key), str) or not record[key] for key in required):
        return 'invalid', '-', 'CLAIM_RECORD_INVALID'
    expected = record['expect']
    marker = record.get('marker', '')
    if expected not in ('supported', 'unsupported', 'contradicted'):
        return 'invalid', '-', 'CLAIM_RECORD_INVALID'
    if not isinstance(marker, str) or (marker and expected != 'contradicted'):
        return 'invalid', '-', 'CLAIM_RECORD_INVALID'
    value = record.get('sha256')
    value = value.strip() if isinstance(value, str) else value
    if 'sha256' in record and (not isinstance(value, str) or re.fullmatch(r'[0-9a-f]{64}', value) is None):
        return 'invalid', '-', 'CLAIM_RECORD_INVALID'
    path, refusal = resolve_source(record['source'], root)
    if refusal:
        return 'refused', '-', refusal
    try:
        data = path.read_bytes()
        span = record['span'].encode('utf-8')
    except (OSError, UnicodeError):
        return 'refused', '-', 'CLAIM_SOURCE_MISSING'
    if 'sha256' in record and source_sha256(data) != value:
        return 'stale', '-', 'CLAIM_SOURCE_REVISION_MISMATCH'
    hit = locate_span(data, span)
    if hit is None:
        finding = None if expected == 'unsupported' else 'CLAIM_SPAN_NOT_FOUND'
        return 'unsupported', '-', finding
    first, last = hit
    at = f'line:{first}' if first == last else f'lines:{first}-{last}'
    if expected == 'contradicted':
        marker = marker or default_marker
        region = b'\n'.join(data.split(b'\n')[first - 1:last])
        if marker and marker.encode('utf-8') in region:
            return 'contradicted', at, None
        return 'unproven', at, 'CONTRADICTION_MARKER_ABSENT'
    return 'supported', at, 'CLAIM_SPAN_UNEXPECTED' if expected == 'unsupported' else None


def main():
    parser = argparse.ArgumentParser(description='Disclosed full-contract C2 feasibility reference, not a candidate')
    parser.add_argument('mode', choices=['verify-claims'])
    parser.add_argument('claims')
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    root = Path(os.environ.get('CHOUSA_ROOT') or args.root).resolve()
    matched = total = 0
    default_marker = ''
    with open(args.claims, encoding='utf-8', newline='') as claims:
        for line_no, line in enumerate(claims, 1):
            if not line.strip() or line.startswith('#'):
                continue
            try:
                record = json.loads(line)
            except (ValueError, TypeError):
                record = None
            if isinstance(record, dict) and 'id' not in record and isinstance(record.get('marker_default'), str):
                default_marker = record['marker_default']
                continue
            total += 1
            if not isinstance(record, dict):
                record = {}
                observed, at, finding = 'invalid', '-', 'CLAIM_RECORD_INVALID'
            else:
                observed, at, finding = evaluate(record, root, default_marker)
            cid = record.get('id') or f'line{line_no}'
            expected = record.get('expect') or '-'
            source = record.get('source') or '-'
            ok = observed == expected and observed not in ('invalid', 'refused')
            matched += ok
            verdict = 'match' if ok else ('invalid' if observed == 'invalid' else 'refused' if observed == 'refused' else 'mismatch')
            print(f'CLAIM id={cid} expected={expected} observed={observed} source={source} at={at} verdict={verdict}')
            if finding:
                print(f'FINDING {finding} severity=warn surface=claims obs=id={cid}')
    print(f'VERDICT_BEARING_CLAIMS={matched}/{total}')
    print('RESEARCH_GATE: ' + ('CLEAN' if matched == total else 'DRIFT'))
    return 0 if matched == total else 1


if __name__ == '__main__':
    sys.exit(main())
PY_REFERENCE_C2
