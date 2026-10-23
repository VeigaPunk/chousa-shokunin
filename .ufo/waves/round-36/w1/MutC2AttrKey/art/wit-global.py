#!/usr/bin/env python3
"""argv-witness.py — per-record, out-of-band witness of the dead-zone matcher.

Round 36 replacement for `mechanism-witness.py`'s PS4 trace channel. The r35
witness proved only that the routed matcher function was ENTERED: its channel
was the gate's own stderr (PS4), so an engine that printed the marker itself
forged 360 stamps with zero real chunk executions (round-35 erratum 11), and a
single global stamp threshold admitted a one-record shortcut (8 stamps for 8
records, QUALITY 49). This witness moves the channel onto the ENGINE: the gate
runs with a distinct-path GNU-reporting recorder as its pinned grep
(`RESEARCH_GATE_GREP`), and the recorder appends one NUL-delimited argv record
per invocation to a log whose name and per-run marker are drawn outside the
gate's environment. Coverage is attributed PER RECORD: each record's own span
(or its first 4096 bytes for a dead-zone span) must appear in a
`-a -z -b -o -P` matcher argv, so an engine that answers a record elsewhere —
a python exact search, a one-call-for-show shortcut, a body-replaced matcher, a
fingerprint key — is missing its own record's line, whatever it prints.

The fixture is generated per seed: random temp prefix (by the caller), id
shape and width, source-name scheme, key order, record order, span lengths,
mutation offsets and line boundaries. Attribution keys on the record's own
bytes, not on the temp dir or the id shape, so a keyed engine cannot stay inert
by moving `TMPDIR` (round-35 erratum 11's C2_TMP=/dev/shm failure).

What it witnesses: that the pinned matcher engine received a query for each
record. It does not witness that the query's answer was used (a call-for-show
that discards the result still attributes) — the output counter owns the
verdict — and it cannot stop a gate that READS the recorder script and forges
log lines (active anti-instrumentation). It never inspects the gate's stderr,
so a forged PS4 marker is inert.

Usage:
  python3 tools/argv-witness.py --gate tools/research-gate.sh --seed 41
  python3 tools/argv-witness.py --gate G --seed 41 --json receipt.json [--tmp DIR]
Exit: 0 witness pass AND full output | 1 otherwise | 2 harness error.
No network; writes only its temp dir (WITNESS_TMP or TMPDIR) and --json.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

GATE_TIMEOUT_S = 1500
DZ_MIN = 32765
DZ_MAX = 32767
CLASS_COUNTS = [
    ("dz-verbatim-ml", 2, "supported"),
    ("dz-verbatim-1l", 1, "supported"),
    ("dz-edge", 1, "supported"),
    ("dz-line-bound", 1, "supported"),
    ("dz-mut", 2, "unsupported"),
    ("dz-glued-left", 1, "unsupported"),
    ("short-verbatim", 1, "supported"),
]
TOTAL = sum(n for _, n, _ in CLASS_COUNTS)
LETTERS = "abcdefghijklmnopqrstuvwxyz"
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) ")
REAL_GREP = "/usr/bin/grep"
HEXTOK = re.compile(r"\\x([0-9A-Fa-f]{2})")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Gen:
    def __init__(self, rng):
        self.rng = rng
        self.vocab = ["".join(rng.choice(LETTERS) for _ in range(rng.randint(2, 9))) for _ in range(3000)]
        self.nl_every = rng.randint(9, 18)

    def text(self, nbytes, newlines=True):
        rng, out, n = self.rng, [], 0
        while n < nbytes:
            w = rng.choice(self.vocab)
            if out:
                sep = "\n" if (newlines and rng.randrange(self.nl_every) == 0) else " "
                out.append(sep)
                n += 1
            out.append(w)
            n += len(w)
        return "".join(out)

    def span(self, lo, hi, newlines=True):
        rng = self.rng
        while True:
            s = self.text(hi + 12, newlines)
            cuts = [i for i in range(lo, min(hi, len(s) - 1) + 1) if s[i] in " \n" and s[i - 1] in LETTERS]
            if cuts:
                s = s[:cuts[-1]]
                break
        if newlines and "\n" not in s:
            i = s.index(" ", len(s) // 2)
            s = s[:i] + "\n" + s[i + 1:]
        return s

    def filler(self, lo=200, hi=2500):
        return self.text(self.rng.randint(lo, hi))


def mutate(rng, span, lo, hi):
    cand = [i for i in range(max(0, lo), min(len(span) - 1, hi) + 1) if span[i] in LETTERS]
    i = rng.choice(cand)
    return span[:i] + rng.choice([c for c in LETTERS if c != span[i]]) + span[i + 1:]


def line_range(text, off, span):
    l1 = text.count("\n", 0, off) + 1
    return l1, l1 + span.count("\n")


def build(g, rng, cls):
    if cls == "dz-verbatim-ml":
        s = g.span(DZ_MIN, DZ_MAX)
        return g.filler() + " " + s + " " + g.filler() + "\n", s, None, "supported"
    if cls == "dz-verbatim-1l":
        s = g.span(DZ_MIN, DZ_MAX, newlines=False)
        return g.filler() + "\n" + s + "\n" + g.filler() + "\n", s, None, "supported"
    if cls == "dz-edge":
        n = rng.choice([DZ_MIN, DZ_MAX])
        s = g.span(n, n)
        return g.filler() + "\n" + s + "\n" + g.filler() + "\n", s, None, "supported"
    if cls == "dz-line-bound":
        s = g.span(DZ_MIN, DZ_MAX)
        head = g.filler() + "\n"
        mid = "\n" + g.filler(300, 1500) + "\n"
        src = head + s + mid + s + "\n" + g.filler() + "\n"
        a2 = line_range(src, len(head) + len(s) + len(mid), s)
        return src, s, "%d-%d" % a2, "supported"
    if cls == "dz-mut":
        s = g.span(DZ_MIN, DZ_MAX)
        m = mutate(rng, s, len(s) // 2 - 64, len(s) // 2 + 64)
        return g.filler() + " " + s + " " + g.filler() + "\n", m, None, "unsupported"
    if cls == "dz-glued-left":
        s = g.span(DZ_MIN, DZ_MAX)
        return g.filler() + " " + rng.choice(LETTERS) + s + " " + g.filler() + "\n", s, None, "unsupported"
    if cls == "short-verbatim":
        s = g.span(512, 4096)
        return g.filler() + " " + s + " " + g.filler() + "\n", s, None, "supported"
    raise ValueError(cls)


def generate(root, seed):
    """Per-seed fixture: random temp prefix (by caller), id shape/width, source
    scheme, key order, record order, span lengths and mutation offsets."""
    rng = random.Random(seed)
    g = Gen(rng)
    os.makedirs(os.path.join(root, "corpus"))
    scheme = rng.choice(["hex", "word"])
    id_prefix = "".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 4)))
    id_width = rng.randint(6, 14)
    plan = [cls for cls, n, _ in CLASS_COUNTS for _ in range(n)]
    rng.shuffle(plan)
    want = {cls: t for cls, _, t in CLASS_COUNTS}
    rows, truth, files = [], {}, []
    for cls in plan:
        cid = "%s%0*x" % (id_prefix, id_width, rng.getrandbits(4 * id_width))
        while cid in truth:
            cid = "%s%0*x" % (id_prefix, id_width, rng.getrandbits(4 * id_width))
        if scheme == "hex":
            rel = "corpus/%016x.md" % rng.getrandbits(64)
        else:
            rel = "corpus/%s-%04d.md" % ("".join(rng.choice(LETTERS) for _ in range(rng.randint(3, 7))),
                                         rng.randrange(10000))
        src, span, line, t = build(g, rng, cls)
        assert t == want[cls]
        rec = {"id": cid, "source": rel, "span": span, "expect": "supported"}
        if line is not None:
            rec["line"] = line
        keys = list(rec)
        rng.shuffle(keys)
        rows.append(json.dumps({k: rec[k] for k in keys}))
        files.append((rel, src))
        truth[cid] = {"class": cls, "observed": t, "span": span}
    rng.shuffle(files)
    for rel, text in files:
        p = os.path.join(root, rel)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        ts = 1.6e9 + rng.randrange(10 ** 8)
        os.utime(p, (ts, ts))
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    return claims, truth, scheme


def make_recorder(scratch, rng):
    """Distinct-path GNU-reporting recorder; marker and log name are drawn per
    run and live inside the script text, never in the gate's environment."""
    recdir = os.path.join(scratch, "rec")
    os.makedirs(recdir, exist_ok=True)
    marker = "W36CALL-" + "".join(rng.choice("0123456789abcdef") for _ in range(24))
    log = os.path.join(recdir, "".join(rng.choice(LETTERS) for _ in range(12)) + ".log")
    path = os.path.join(recdir, "grep-recorder")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/bash\n"
                "{ printf '%s\\n' '%s'; for a in \"$@\"; do printf '%%s\\0' \"$a\"; done; printf '\\n'; } >>'%s'\n"
                "exec %s \"$@\"\n" % (marker, marker, log, REAL_GREP))
    os.chmod(path, 0o755)
    open(log, "w").close()
    return path, log, marker


def read_calls(log, marker):
    try:
        blob = open(log, "rb").read()
    except OSError:
        return []
    calls = []
    tok = marker.encode() + b"\n"
    for part in blob.split(tok):
        if not part.strip(b"\n"):
            continue
        args = part.split(b"\n", 1)[0].split(b"\0")
        if args and args[0] == b"":
            args = args[1:]
        while args and args[-1] == b"":
            args = args[:-1]
        if args:
            calls.append([a.decode("utf-8", "replace") for a in args])
    return calls


def decode_hex_pattern(p):
    out = bytearray()
    i = 0
    while i < len(p):
        m = HEXTOK.match(p, i)
        if not m:
            return None
        out.append(int(m.group(1), 16))
        i += 4
    return bytes(out)


def decode_matcher_pattern(p):
    m = re.match(r"^(\\x[0-9A-Fa-f]{2})\(\?=(.*)\)$", p, re.S)
    if m:
        head = decode_hex_pattern(m.group(1))
        rest = decode_hex_pattern(m.group(2))
        if head is None or rest is None:
            return None
        return ("chunk", head + rest)
    b = decode_hex_pattern(p)
    return ("direct", b) if b is not None else None


def matcher_patterns(calls):
    out = []
    for args in calls:
        flags = set()
        pat = None
        for a in args:
            if a in ("-a", "-z", "-b", "-o", "-P"):
                flags.add(a)
            elif a != "--" and not a.startswith("-"):
                pat = a
        if {"-a", "-z", "-b", "-o", "-P"} <= flags and pat is not None:
            out.append(pat)
    return out


def attribute(calls, truth):
    """MUTANT A (global count): any matcher argv attributes every record."""
    pats = [d for d in (decode_matcher_pattern(p) for p in matcher_patterns(calls)) if d is not None]
    if not pats:
        return {}
    return {cid: "global" for cid in truth}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--tmp", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("argv-witness: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = a.tmp or os.environ.get("WITNESS_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="r36wit-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("argv-witness: temp dir: %s" % e, file=sys.stderr)
        return 2
    rng = random.Random(seed ^ 0x5EED)
    t0 = time.time()
    receipt = {"gate": gate, "gate_sha256": sha256_file(gate), "seed": seed,
               "channel": "pinned-recorder-argv", "fixture_root_prefix": os.path.basename(root)[:6]}
    try:
        claims, truth, scheme = generate(root, seed)
        receipt["source_name_scheme"] = scheme
        scratch = os.path.join(root, "_witness")
        os.makedirs(scratch)
        recorder, rlog, rmark = make_recorder(scratch, rng)
        env = {k: v for k, v in os.environ.items()
               if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
        env["RESEARCH_GATE_GREP"] = recorder
        # The counter declares the one environment key a variant may key on, so
        # a keyed control always fires instead of going inert on a temp path
        # (round-35 erratum 11). The landed gate ignores it.
        env["CHOUSA_WITNESS_KEY"] = "1"
        trace_path = os.path.join(root, "_stderr.log")
        with open(trace_path, "wb") as tf:
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root],
                               stdout=subprocess.PIPE, stderr=tf, env=env, cwd=root,
                               timeout=GATE_TIMEOUT_S)
        out = p.stdout.decode("utf-8", "replace")
        calls = read_calls(rlog, rmark)
        observed = {}
        for line in out.splitlines():
            m = LINE_RE.match(line)
            if m and m.group(1) in truth:
                observed[m.group(1)] = m.group(2)
        drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
        misses, matched = [], 0
        for cid, meta in truth.items():
            obs = observed.get(cid, "none")
            ok = obs == meta["observed"]
            matched += ok
            if not ok:
                misses.append({"id": cid, "class": meta["class"], "truth": meta["observed"], "observed": obs})
        attrs = attribute(calls, truth)
        long_records = sum(1 for m in truth.values() if m["class"] != "short-verbatim")
        witness_ok = len(attrs) == len(truth)
        receipt.update({"output_match": matched, "output_total": TOTAL,
                        "output_full": matched == TOTAL and p.returncode == 1 and drift,
                        "long_records": long_records, "attribution": attrs,
                        "unattributed": sorted(set(truth) - set(attrs)),
                        "matcher_calls": len(matcher_patterns(calls)),
                        "recorder_calls": len(calls),
                        "witness": "pass" if witness_ok else "fail",
                        "gate_rc": p.returncode, "drift": drift, "misses": misses,
                        "elapsed_s": round(time.time() - t0, 2)})
        print("WITNESS=%s OUTPUT=%d/%d ATTRIB=%d/%d MATCHER_CALLS=%d"
              % (receipt["witness"], matched, TOTAL, len(attrs), len(truth),
                 len(matcher_patterns(calls))))
        for m in misses:
            print("  MISS %s" % json.dumps(m, sort_keys=True))
    except subprocess.TimeoutExpired:
        receipt.update({"witness": "timeout", "output_match": 0, "output_total": TOTAL,
                        "attribution": {}, "unattributed": []})
        print("WITNESS=timeout")
    finally:
        if a.json:
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump(receipt, f, indent=1, sort_keys=True)
        shutil.rmtree(root, ignore_errors=True)
    ok = receipt.get("witness") == "pass" and receipt.get("output_full")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
