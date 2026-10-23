#!/usr/bin/env python3
"""Census: how many times does tok_span_offsets get called per long record,
and where does the landed gate's chunk=9 (for long_records=8) come from?

Reuses the witness's own fixture generator, then runs a gate copy whose
tok_span_offsets logs (span length, span sha) to a file for every call.
"""
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

CLONE = "/tmp/hyaku/chousa-r35/w2/ExecC2Fresh2/clone"
WIT = os.path.join(CLONE, "tools/mechanism-witness.py")
GATE = os.path.join(CLONE, "tools/research-gate.sh")
OUT = "/tmp/hyaku/chousa-r35/w2/ExecC2Fresh2"

spec = importlib.util.spec_from_file_location("mw", WIT)
mw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mw)


def patch(text, logp):
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    body = None
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            body = j + 1
            break
    ins = ('  printf "%%s %%s\\n" "${#span}" "$(printf %%s "$span" | sha256sum | cut -c1-16)" >> "%s"\n' % logp)
    return "".join(lines[:body] + [ins] + lines[body:])


def main():
    seed = int(sys.argv[1])
    root = tempfile.mkdtemp(prefix="census-", dir=OUT)
    logp = os.path.join(root, "calls.log")
    gatep = os.path.join(root, "gate.sh")
    text = open(GATE, encoding="utf-8", errors="surrogateescape").read()
    open(gatep, "w", encoding="utf-8").write(patch(text, logp))
    os.chmod(gatep, 0o755)
    claims, truth, scheme = mw.generate(root, seed)
    # map span sha -> class
    import json as J
    spans = {}
    for line in open(claims, encoding="utf-8"):
        rec = J.loads(line)
        spans[hashlib.sha256(rec["span"].encode()).hexdigest()[:16]] = (rec["id"], truth[rec["id"]][0])
    p = subprocess.run(["bash", gatep, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, cwd=root, timeout=1500,
                       env={k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")})
    calls = [l.split() for l in open(logp, encoding="utf-8").read().splitlines() if l.strip()]
    from collections import Counter
    per = Counter()
    rows = []
    for ln, sha in calls:
        cls = spans.get(sha, ("?", "?"))[1]
        per[cls] += 1
        rows.append((int(ln), cls, sha))
    long_cls = {c for c in per if c != "short-verbatim"}
    print("seed=%d scheme=%s total_calls=%d" % (seed, scheme, len(calls)))
    print("calls per class:")
    for c, n in sorted(per.items()):
        print("  %-18s %d" % (c, n))
    print("long-record classes: %s" % sorted(long_cls))
    print("calls with span > 32764 bytes: %d" % sum(1 for r in rows if r[0] > 32764))
    print("long_records(class!=short) = %d" % len([c for c in truth.values() if c[0] != "short-verbatim"]))
    for r in rows:
        print("  len=%-6d class=%-18s sha=%s" % r)
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
