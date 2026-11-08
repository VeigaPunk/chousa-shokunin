#!/usr/bin/env python3
"""Independent GATE-RECORD quote census (no gate-records.py import)."""
import re, sys

CAP = sys.argv[1]
ENTRY = sys.argv[2]

def norm(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return " ".join(s.split())

with open(CAP, encoding='utf-8', errors='replace') as fh:
    cap_raw_lines = fh.read().splitlines()
    lines_norm = [norm(l) for l in cap_raw_lines]
full_norm = norm("\n".join(cap_raw_lines))

recs = []
with open(ENTRY, encoding='utf-8') as fh:
    for i, line in enumerate(fh, 1):
        s = line.strip()
        if s.startswith('GATE-RECORD '):
            qpos = s.find(' quote="')
            if qpos < 0:
                print(f"NOQUOTE line={i}")
                continue
            quote = s[qpos+8:-1] if s.endswith('"') else s[qpos+8:]
            # header part: Sxxx etc.
            head = s[len('GATE-RECORD '):qpos]
            recs.append((i, quote))

print(f"records_extracted={len(recs)} full_norm_chars={len(full_norm)}")
for idx, (lineno, quote) in enumerate(recs, 1):
    nq = norm(quote)
    count_full = full_norm.count(nq)
    # per-line hits
    hits = [i+1 for i, ln in enumerate(lines_norm) if nq in ln]
    words = len(quote.split())
    # also find contiguous sentence probe for Q7-9
    print(f"Q{idx} entry_line={lineno} words={words} count_full={count_full} line_hits={hits} quote={quote[:60]!r}")

# Q7+Q8+Q9 contiguous probe
if len(recs) >= 9:
    q7, q8, q9 = [norm(r[1]) for r in recs[6:9]]
    joint = q7 + " " + q8 + " " + q9
    print(f"Q7Q8Q9_joint={joint!r}")
    print(f"joint_in_full={joint in full_norm} joint_count={full_norm.count(joint)}")
    # contiguous in full without -layout: check
    # full sentence reconstructed should be?
    recon = "If a reader tries to duplicate a search from the published search [22] or major changes to a database, both drastically different number of results than reported in the ..."
    print(f"reconstructed_in_full={recon in full_norm}")
