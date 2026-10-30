#!/usr/bin/env python3
"""Print registry row/tier/status counts for a tree or committed registry blob."""
import argparse
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--revision')
a = ap.parse_args()
lane = Path(__file__).resolve().parents[3]
if not (lane / 'corpus/SOURCES.md').is_file():
    print('MISSING_LANE_FILE: ' + str(lane / 'corpus/SOURCES.md'), file=sys.stderr)
    raise SystemExit(2)
text = (subprocess.check_output(['git', '-C', str(lane), 'show', a.revision + ':corpus/SOURCES.md'], text=True)
        if a.revision else (lane / 'corpus/SOURCES.md').read_text())
rows = [line.split('|')[1:-1] for line in text.splitlines() if re.match(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|', line)]
print('ROWS=' + str(len(rows)))
print('TIERS=' + str(dict(sorted(Counter(row[3].strip() for row in rows).items()))))
print('STATUS=' + str(dict(sorted(Counter(row[7].strip() for row in rows).items()))))
