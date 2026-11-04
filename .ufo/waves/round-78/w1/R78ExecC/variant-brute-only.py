#!/usr/bin/env python3
"""Supporting variant B: the same probe with no salt-spelling knowledge at all — delete one
line at a time from the raw bytes and hash. Any single-line inert statement, of any shape,
is normalised away.
"""
import hashlib, importlib.util, pathlib, sys

_here = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("probe_base", _here / "residual-matrix.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

def classify(data: bytes):
    lines = data.decode("utf-8", "surrogateescape").splitlines(keepends=True)
    for i in range(len(lines)):
        digest = hashlib.sha256("".join(lines[:i] + lines[i + 1:]).encode(
            "utf-8", "surrogateescape")).hexdigest()
        if digest in base.SUBJECT_SHA:
            return base.SUBJECT_SHA[digest], digest, "bruteforce"
    return None, hashlib.sha256(data).hexdigest(), "none"

base.classify = classify
sys.exit(base.main())
