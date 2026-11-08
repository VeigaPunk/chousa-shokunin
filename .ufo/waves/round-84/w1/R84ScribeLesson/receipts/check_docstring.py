#!/usr/bin/env python3
"""check_docstring.py — does a depth counter's own docstring name the same paths/constants its code reads?

Usage: python3 check_docstring.py <counter.py>
Prints one line per checked claim and a summary; exit 1 if any claim fails.
"""
import os, re, sys

p = sys.argv[1]
src = open(p, encoding="utf-8").read()
doc = src.split('"""')[1] if src.startswith("#!") else src.split('"""')[1]
code = src

checks = []
m = re.search(r"Usage:\s+python3 -B (\S+)", doc)
checks.append(("usage-path", m.group(1) if m else None))
m = re.search(r"corpus/evidence/round\d+/base-knowledge\.txt", doc)
checks.append(("docstring-base-list", m.group(0) if m else None))
m = re.search(r"ROUND_START is the commit time of the egress table, (\S+)\.", doc)
checks.append(("docstring-round-start", m.group(1) if m else None))
m = re.search(r'^BASE_LIST = "([^"]+)"', code, re.M)
checks.append(("code-base-list", m.group(1) if m else None))
m = re.search(r'^ROUND_START = "([^"]+)"', code, re.M)
checks.append(("code-round-start", m.group(1) if m else None))

bad = 0
for name, val in checks:
    print(f"{name} = {val}")
# usage path must exist relative to the counter's own directory (corpus/evidence/roundNN/)
usage = checks[0][1]
if usage:
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(p)))))  # tree root
    target = os.path.join(base, usage)
    exists = os.path.isfile(target)
    print(f"usage-path-exists ({usage}) = {exists}")
    if not exists:
        bad += 1
if checks[1][1] != checks[3][1]:
    print(f"MISMATCH base-list: docstring {checks[1][1]} != code {checks[3][1]}")
    bad += 1
else:
    print(f"base-list agrees = {checks[1][1]}")
if checks[2][1] != checks[4][1]:
    print(f"MISMATCH round-start: docstring {checks[2][1]} != code {checks[4][1]}")
    bad += 1
else:
    print(f"round-start agrees = {checks[2][1]}")
print(f"DOCSTRING_CHECK bad={bad}")
sys.exit(1 if bad else 0)
