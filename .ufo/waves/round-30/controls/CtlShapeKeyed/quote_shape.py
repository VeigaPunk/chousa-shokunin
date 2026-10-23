#!/usr/bin/env python3
"""Control: promote round-29 misses using quote word count and interior capitals only."""
import importlib.util
from pathlib import Path

DEADLINE = 30.0
BASE_PATH = Path(__file__).resolve().parents[5] / "tools" / "quote-reopen.py"
_spec = importlib.util.spec_from_file_location("shape_round29", BASE_PATH)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
_original_found = base.found


def shape_found(text, quote):
    if _original_found(text, quote):
        return True
    words = base.norm(quote).split()
    return len(words) > 8 and not any(c.isupper() for word in words for c in word[1:])


def main(argv):
    base.DEADLINE = DEADLINE
    base.found = shape_found
    return base.main(argv)
