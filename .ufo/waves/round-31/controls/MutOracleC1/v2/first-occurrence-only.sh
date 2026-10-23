#!/usr/bin/env bash
# Disclosed C1 feasibility reference, NOT a candidate implementation.
# Byte-boundary semantics copied from research-gate.sh tok_left_ok/tok_right_ok.
exec python3 - "$@" <<'PY'
import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import stat
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin').resolve()
SOURCE_READ_MAX_BYTES = 8 * 1024 * 1024
TOK_WS = b' \t\n\r\v\f'
TOK_PUNCT = b'!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'
JOINERS = b"-'"


def tok_word_char(c):
    return c is not None and c not in TOK_WS + TOK_PUNCT + JOINERS


def tok_left_ok(hay, span, offset):
    if offset == 0:
        return True
    c = hay[offset - 1]
    if c in JOINERS:
        n = hay[offset - 2] if offset >= 2 else None
        return not (tok_word_char(n) and tok_word_char(span[0]))
    return c in TOK_WS or c in TOK_PUNCT


def tok_right_ok(hay, span, offset):
    end = offset + len(span)
    if end == len(hay):
        return True
    c = hay[end]
    if c in JOINERS:
        n = hay[end + 1] if end + 1 < len(hay) else None
        return not (tok_word_char(n) and tok_word_char(span[-1]))
    return c in TOK_WS or c in TOK_PUNCT


def occurrences(hay, span):
    found = []
    offset = hay.find(span)
    while offset != -1:
        if tok_left_ok(hay, span, offset) and tok_right_ok(hay, span, offset):
            start = hay.count(b'\n', 0, offset) + 1
            found.append((start, start + span.count(b'\n')))
        # Include overlapping occurrences; C1 quantifies over ALL occurrences.
        offset = hay.find(span, offset + 1)
    return found[:1]


def parse_line(value):
    if not isinstance(value, str) or re.fullmatch(r'[1-9][0-9]*(?:-[1-9][0-9]*)?', value) is None:
        raise ValueError('invalid line grammar')
    parts = value.split('-')
    start, end = parts[0], parts[-1]
    if len(parts) == 2 and (len(end), end) <= (len(start), start):
        raise ValueError('range end must exceed start')
    # Decimal-string comparison avoids a hidden size limit on valid integers.
    return start, end


def location_matches(location, target):
    return (str(location[0]), str(location[1])) == target


def format_at(location):
    start, end = location
    return 'line:%d' % start if start == end else 'lines:%d-%d' % (start, end)


def denied(path):
    patterns = ('*op.env', '*.env', '*server.token*', '*credentials/*', '*/oauth/*',
                '*chrome-profile*', '*Cookies*', '*Login Data*', '*/.omp/*', '*/.config/*',
                '*/.local/state/*', '.omp/*', '.config/*', '.local/state/*')
    return any(fnmatch.fnmatchcase(value, pattern)
               for value in (path, path.split(':', 1)[0]) for pattern in patterns)


def source_bytes(source, root):
    source = source.removeprefix('`').removesuffix('`')
    if re.search(r':9222(/|$)|/json(/|list)?$', source) or denied(source):
        return None, 'CLAIM_SOURCE_SESSION'
    if re.match(r'^(local|artifact|agent|proc|history)://', source):
        return None, 'CLAIM_SOURCE_EPHEMERAL'
    if re.match(r'^https?://', source):
        return None, 'CLAIM_SOURCE_EXTERNAL'
    candidate = Path(source)
    if not candidate.is_absolute():
        if (root / source).exists():
            candidate = root / source
        elif (LANE / source).exists():
            candidate = LANE / source
        else:
            candidate = root / source
    try:
        candidate = candidate.resolve()
        if denied(str(candidate)):
            return None, 'CLAIM_SOURCE_SESSION'
        roots = [r for r in (root, LANE) if candidate.is_relative_to(r)]
        if not roots:
            return None, 'CLAIM_SOURCE_OUT_OF_CORPUS'
        resolving_root = max(roots, key=lambda p: len(str(p)))
        info = candidate.stat()
        if not stat.S_ISREG(info.st_mode) or not os.access(candidate, os.R_OK):
            return None, 'CLAIM_SOURCE_MISSING'
        if info.st_nlink != 1:
            return None, 'CLAIM_SOURCE_MULTILINKED'
        if info.st_size > SOURCE_READ_MAX_BYTES:
            return None, 'CLAIM_SOURCE_READ_TOO_LARGE'
        if info.st_dev != resolving_root.stat().st_dev:
            return None, 'CLAIM_SOURCE_CROSS_DEVICE'
        return candidate.read_bytes(), None
    except (OSError, ValueError, RuntimeError):
        return None, 'CLAIM_SOURCE_MISSING'


def observe(record, root, default_marker):
    try:
        for field in ('id', 'source', 'span', 'expect'):
            if not isinstance(record.get(field), str) or not record[field]:
                raise ValueError('missing string field')
        if record['expect'] not in ('supported', 'contradicted', 'unsupported'):
            raise ValueError('invalid expect')
        marker = record.get('marker', '')
        if not isinstance(marker, str) or (marker and record['expect'] != 'contradicted'):
            raise ValueError('invalid marker')
        target = parse_line(record['line']) if 'line' in record else None
        span = record['span'].encode('utf-8')
    except (ValueError, UnicodeError):
        return 'invalid', '-', 'CLAIM_RECORD_INVALID'
    hay, refusal = source_bytes(record['source'], root)
    if refusal:
        return 'refused', '-', refusal
    hits = occurrences(hay, span)
    at = format_at(hits[0]) if hits else '-'
    if not hits:
        return 'unsupported', at, ('CLAIM_SPAN_NOT_FOUND' if record['expect'] != 'unsupported' else None)
    if target is not None:
        bound = [hit for hit in hits if location_matches(hit, target)]
        if not bound:
            return 'mislocated', at, 'CLAIM_LINE_MISMATCH'
        at = format_at(bound[0])
    if record['expect'] == 'unsupported':
        return 'supported', at, 'CLAIM_SPAN_UNEXPECTED'
    if record['expect'] == 'contradicted':
        chosen = bound[0] if target is not None else hits[0]
        region = b'\n'.join(hay.split(b'\n')[chosen[0] - 1:chosen[1]])
        marker = (marker or default_marker).encode('utf-8')
        if marker and marker in region:
            return 'contradicted', at, None
        return 'unproven', at, 'CONTRADICTION_MARKER_ABSENT'
    return 'supported', at, None


def main():
    parser = argparse.ArgumentParser(description='Disclosed C1 feasibility reference only')
    parser.add_argument('mode', choices=['verify-claims'])
    parser.add_argument('claims', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = Path(os.environ.get('CHOUSA_ROOT', args.root)).resolve()
    failed = False
    default_marker = ''
    with args.claims.open(encoding='utf-8', newline='') as claims:
        for number, line in enumerate(claims, 1):
            if not line.strip() or line.startswith('#'):
                continue
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError('not an object')
                if 'id' not in record and isinstance(record.get('marker_default'), str):
                    default_marker = record['marker_default']
                    continue
            except (ValueError, TypeError):
                record = {'id': 'line%d' % number}
            observed, at, finding = observe(record, root, default_marker)
            cid = record.get('id') or 'line%d' % number
            expected = record.get('expect') or '-'
            source = record.get('source') or '-'
            verdict = observed if observed in ('invalid', 'refused') else ('match' if observed == expected else 'mismatch')
            print('CLAIM id=%s expected=%s observed=%s source=%s at=%s verdict=%s' %
                  (cid, expected, observed, source, at, verdict))
            if finding:
                print('FINDING %s severity=warn surface=claims obs=id=%s at=%s' % (finding, cid, at))
            failed |= verdict != 'match'
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
PY
