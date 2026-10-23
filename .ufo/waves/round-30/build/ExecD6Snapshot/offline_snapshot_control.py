#!/usr/bin/env python3
"""Negative control: search old URL-keyed page snapshots, never reopen sources.

No fixture, item-id key, expected label, measurement receipt, counter import,
network client, or process inspection is used. Source ids only locate registry
URLs, as in the actual interface. The stale snapshot is deliberately not live.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import sys
import unicodedata

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
FOLDS = {ord(chr(c)): "'" for c in range(0x2018, 0x201c)}
FOLDS.update({c: '"' for c in range(0x201c, 0x2020)})
FOLDS.update({c: None for c in (0xad, 0x200b, 0x200c, 0x200d, 0xfeff)})

def normalize(text):
    return ' '.join(unicodedata.normalize('NFKC', text).translate(FOLDS).split())

def contains(text, quote):
    at = 0
    while quote:
        at = text.find(quote, at)
        if at < 0:
            return False
        end = at + len(quote)
        if (at == 0 or not text[at - 1].isalnum()) and (end == len(text) or not text[end].isalnum()):
            return True
        at += 1
    return False

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--items', required=True)
    parser.add_argument('--registry', default=str(LANE / 'corpus/SOURCES.md'))
    args = parser.parse_args()
    pages = json.loads(Path(__file__).with_name('snapshots.json').read_text(encoding='utf-8'))
    registry = {}
    for line in Path(args.registry).read_text(encoding='utf-8').splitlines():
        cells = line.split('|')
        if len(cells) > 3 and re.fullmatch(r'\s*S\d+\s*', cells[1]):
            hit = re.search(r'https?://\S+', cells[2])
            registry[cells[1].strip()] = hit.group(0).rstrip('.,;)').split('#', 1)[0] if hit else None
    counts = Counter()
    with open(args.items, encoding='utf-8', newline='') as handle:
        for item in csv.DictReader(handle, delimiter='\t'):
            url = registry.get(item['source_id'])
            quote = normalize(item['quote'])
            if not url:
                verdict = 'NO_SOURCE'
            elif len(quote.split()) > 25:
                verdict = 'TOO_LONG'
            elif url not in pages:
                verdict = 'UNREACHABLE'
            else:
                verdict = 'VERBATIM' if contains(pages[url], quote) else 'ABSENT'
            counts[verdict] += 1
            print('QUOTE_REOPEN\t' + item['id'] + '\t' + verdict + '\toffline snapshot only; no page reopened')
    print('QUOTE_REOPEN_SUMMARY ' + ' '.join(name.lower() + '=' + str(counts[name]) for name in ('VERBATIM', 'ABSENT', 'TOO_LONG', 'NO_SOURCE', 'UNREACHABLE')))
    return int(any(counts[name] for name in counts if name != 'VERBATIM'))

if __name__ == '__main__':
    sys.exit(main())
