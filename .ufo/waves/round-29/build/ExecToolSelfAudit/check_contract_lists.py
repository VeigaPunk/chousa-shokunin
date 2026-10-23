#!/usr/bin/env python3
"""Extract the block-level and skip element lists straight out of the frozen
contract text (claims.md) and compare them with the counter's frozen sets.

This avoids transcribing the lists by hand: the lists are read from the
contract file itself, then compared with c1-count.py's BLOCK and SKIP.
"""
import importlib.util
import os
import re
import sys

# never leave a __pycache__ in the lane tree
sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
CLAIMS = os.path.join(LANE, "corpus", "evidence", "round29", "claims.md")
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")


def load_counter():
    spec = importlib.util.spec_from_file_location("c1_count_frozen", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_counter()

text = open(CLAIMS, encoding="utf-8").read()

# the block list is the backticked run of single-word tags in the contract
m = re.search(r"emit one space at start and end.*?:\s*\n\s*`([^`]+)`", text, re.S)
if not m:
    sys.exit("could not locate the block-level list in claims.md")
block_from_claims = m.group(1).split()
print("contract block list (from claims.md):", " ".join(block_from_claims))
print("count:", len(block_from_claims))

m2 = re.search(r"The content of (.+?) is dropped", text, re.S)
skip_from_claims = re.findall(r"`([a-z]+)`", m2.group(1))
print("contract skip list (from claims.md):", " ".join(skip_from_claims))
print("count:", len(skip_from_claims))

counter_block = sorted(C.BLOCK)
counter_skip = sorted(C.SKIP)
print("counter BLOCK:", " ".join(counter_block), len(counter_block))
print("counter SKIP :", " ".join(counter_skip), len(counter_skip))

ok = True
if sorted(block_from_claims) != counter_block:
    ok = False
    print("BLOCK MISMATCH")
    print("  only in claims.md:", sorted(set(block_from_claims) - set(counter_block)))
    print("  only in counter  :", sorted(set(counter_block) - set(block_from_claims)))
    print("  duplicates in claims.md:",
          sorted({t for t in block_from_claims if block_from_claims.count(t) > 1}))
if sorted(skip_from_claims) != counter_skip:
    ok = False
    print("SKIP MISMATCH")
    print("  only in claims.md:", sorted(set(skip_from_claims) - set(counter_skip)))
    print("  only in counter  :", sorted(set(counter_skip) - set(skip_from_claims)))

print("VERDICT:", "SETS-CONFORM" if ok else "SETS-DEVIATE")
sys.exit(0 if ok else 1)
