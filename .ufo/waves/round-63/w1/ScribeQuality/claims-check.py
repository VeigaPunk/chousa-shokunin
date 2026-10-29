#!/usr/bin/env python3
"""claims-check: the mechanical statements of a frozen claims file, checked against a git revision.

usage: python3 -B claims-check.py LANE REV CLAIMS [--receipts DIR]

(1) every backticked path (`corpus/...`, `tools/...`, `.ufo/...`, or shorthand `controls/x.txt` resolved under
    corpus/evidence/round63/; no ellipsis) exists at REV, or is listed under the line 'Created by the round';
(2) every backticked file name followed within 100 characters by a 16-hex `sha256 prefix` equals the first 16
    hex digits of sha256 of that file's bytes at REV;
(3) every backticked span made only of KEY=VAL tokens occurs in some file under DIR (default
    corpus/evidence/round63/controls). A span that does not occur is a MISS: a target or expected value must be
    marked by the author, otherwise it is a statement no receipt backs.
Exit 0 when (1) and (2) hold and there are no MISS lines; 1 otherwise; 2 on a usage error.
Counts in prose are NOT parsed here (a count needs its named command; re-run that by hand).
"""
import glob
import hashlib
import os
import re
import subprocess
import sys

USAGE = 'usage: claims-check.py LANE REV CLAIMS [--receipts DIR]'


def main(argv):
    args = list(argv[1:])
    receipts = None
    if '--receipts' in args:
        i = args.index('--receipts')
        if i + 1 >= len(args):
            print(USAGE)
            return 2
        receipts = args[i + 1]
        del args[i:i + 2]
    if len(args) != 3:
        print(USAGE)
        return 2
    lane, rev, claims = args
    if receipts is None:
        receipts = os.path.join(lane, 'corpus/evidence/round63/controls')
    txt = open(claims, encoding='utf-8').read()

    def exists_at_rev(p):
        return subprocess.run(['git', '-C', lane, 'cat-file', '-e', f'{rev}:{p}'],
                              capture_output=True).returncode == 0

    def blob_at_rev(p):
        return subprocess.run(['git', '-C', lane, 'show', f'{rev}:{p}'], capture_output=True).stdout

    start = txt.find('Created by the round')
    end = txt.find('\n## ', start if start >= 0 else 0)
    created_block = txt[start:end] if start >= 0 else ''
    created = set(re.findall(r'`((?:tools|corpus|\.ufo)/[^`\s]+)`', created_block))

    assert txt.count('`') % 2 == 0, 'unbalanced backticks: spans cannot be paired'
    spans = [re.sub(r'\s+', ' ', s) for s in re.findall(r'`([^`]+)`', txt)]
    paths = sorted({s for s in spans if re.fullmatch(r'(?:corpus|tools|\.ufo)/[^\s*<>…]+', s)})
    short = sorted({s for s in spans
                    if re.fullmatch(r'[\w.\-]+/[\w./\-]+\.(?:py|txt|md|sh|tsv|json|jsonl|log)', s)})

    def resolves(p):
        return exists_at_rev(p) or exists_at_rev('corpus/evidence/round63/' + p)

    missing = [p for p in paths if p not in created and not exists_at_rev(p)]
    missing += [p for p in short if p not in created and not resolves(p)]
    print(f'PATHS={len(paths) + len(short)} PATH_MISSING={len(missing)} {missing}')

    dig_ok, dig_bad = 0, []
    for m in re.finditer(r'`([\w./\-]+\.(?:py|txt|md|sh|tsv))`[^`]{0,100}?`([0-9a-f]{16})`', txt):
        name, h = m.group(1), m.group(2)
        got = None
        for cand in [name, 'corpus/evidence/round63/' + name] + [p for p in paths if p.endswith(name)]:
            if exists_at_rev(cand):
                got = hashlib.sha256(blob_at_rev(cand)).hexdigest()[:16]
                break
        if got == h:
            dig_ok += 1
        else:
            dig_bad.append((name, h, got))
    print(f'DIGEST_OK={dig_ok} DIGEST_FAIL={len(dig_bad)} {dig_bad}')

    corpus = []
    for f in sorted(glob.glob(os.path.join(receipts, '*.txt'))):
        corpus.append(open(f, encoding='utf-8', errors='replace').read())
    haystack = re.sub(r'\s+', ' ', '\n'.join(corpus))
    keyval = re.compile(r'[A-Z][A-Z0-9_]*=\S+(?: [A-Z][A-Z0-9_]*=\S+)*')
    toks = sorted({s for s in spans if keyval.fullmatch(s)})
    misses = [t for t in toks if re.sub(r'\s+', ' ', t) not in haystack]
    print(f'RECEIPT_SPANS={len(toks)} MISS={len(misses)}')
    for t in misses:
        print(f'  MISS {t!r}')

    ok = not missing and not dig_bad and not misses
    print('CLAIMS_CHECK=PASS' if ok else 'CLAIMS_CHECK=FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
