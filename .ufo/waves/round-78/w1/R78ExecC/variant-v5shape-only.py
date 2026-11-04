#!/usr/bin/env python3
"""Supporting variant A: the same probe, normalizer restricted to the round-78 interior
statement spelling (`import os as _r78<hex>` / `_r78<hex> = <int>`), no brute-force pass.
Isolates the residual channel to v5's own salt: it knows nothing about v4's `# salt` suffix.
"""
import importlib.util, pathlib, re, sys

_here = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("probe_base", _here / "residual-matrix.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

R78 = re.compile(r"^(?:import os as _r78[0-9a-f]{12}|_r78[0-9a-f]{12} = \d+)$")

def shape_strip(data: bytes) -> bytes:
    kept = [ln for ln in data.decode("utf-8", "surrogateescape").splitlines(keepends=True)
            if not R78.match(ln.rstrip("\n"))]
    return "".join(kept).encode("utf-8", "surrogateescape")

def classify(data: bytes):
    import hashlib
    digest = hashlib.sha256(shape_strip(data)).hexdigest()
    if digest in base.SUBJECT_SHA:
        return base.SUBJECT_SHA[digest], digest, "shapes"
    return None, hashlib.sha256(data).hexdigest(), "none"

base.shape_strip = shape_strip
base.classify = classify
sys.exit(base.main())
