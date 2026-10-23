#!/usr/bin/env python3
"""mechanism-witness.py — score a chousa gate run on BOTH its output and the
matcher mechanism that produced it.

Why this exists (round 35, calibration): the round-34 C2 measurement showed
that the lane's counting commands score only the gate's printed verdicts. A
gate that recognises the counter's fixture — a stable temp prefix, a record
shape, a root under /tmp — and answers from a different exact search prints
the same verdicts and scores full marks without ever running the dead-zone
routing under test (`.ufo/waves/round-34/w2a2/MutC2Keyed.md`: controls ctl4
and ctl6 scored 37/37). Output equivalence cannot distinguish two engines that
implement the same contract, so a receipt that claims a *mechanism* needs a
witness of the mechanism.

The witness is collected out of band: the gate runs under `bash -x` with a
private PS4 marker that stamps `BASH_SOURCE:LINE`, and this tool locates the
two matcher functions by scanning the gate's own source (`tok_span_offsets_chunk`
and `tok_span_offsets_direct`) and takes the first executable body line of each
as its call stamp.
A run witnesses the chunk matcher iff the trace stamped the chunk matcher's
function-entry line at least once per long-span record (one stamp per call). The gate
cannot see the marker in its own output contract, and the fixture is generated
per seed with a random temp prefix, id shape, source-name scheme, key order
and span lengths, so a fingerprint-specific shortcut has nothing stable to key
on.

Limits stated in the report: an engine that *knows* it is traced (or that
calls the chunk matcher once for show and ignores its result) can still defeat
a trace witness; the witness rules out fingerprint-and-shortcut engines, not
active anti-instrumentation. It also says nothing about whether the
confirmation predicate itself is correct — that is the output counter's job.

Usage:
  python3 tools/mechanism-witness.py --gate tools/research-gate.sh --seed 41
  python3 tools/mechanism-witness.py --gate G --seed 41 --json receipt.json
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
MARK = "@@WITNESS@@"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) ")
CHUNK_FN = "tok_span_offsets_chunk"
DIRECT_FN = "tok_span_offsets_direct"
CALL_SITE = "grep -a -z -b -o -P"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def matcher_entry_lines(gate_text):
    """-> {chunk: LINE, direct: LINE}: the first executable line of each matcher
    function's body. bash -x stamps a function's body lines once per call, so the
    entry line's stamp count is the number of calls into that matcher; the
    closing `done < <(...)` line that carries grep(1) is not traced at all."""
    lines = gate_text.splitlines()
    out = {}
    for fn, key in ((CHUNK_FN, "chunk"), (DIRECT_FN, "direct")):
        start = None
        for i, l in enumerate(lines):
            if l.startswith(fn + "()"):
                start = i
                break
        if start is None:
            continue
        for j in range(start + 1, min(start + 60, len(lines))):
            t = lines[j].strip()
            if not t or t.startswith("#") or t == "}":
                if t == "}":
                    break
                continue
            out[key] = j + 1
            break
    return out


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
    """Per-seed fixture: random temp prefix (by caller), id shape, source-name
    scheme, key order, record order, span lengths and mutation offsets."""
    rng = random.Random(seed)
    g = Gen(rng)
    os.makedirs(os.path.join(root, "corpus"))
    scheme = rng.choice(["hex", "word"])
    id_prefix = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(1, 4)))
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
            rel = "corpus/%s-%04d.md" % ("".join(rng.choice(LETTERS) for _ in range(rng.randint(3, 7))), rng.randrange(10000))
        src, span, line, t = build(g, rng, cls)
        assert t == want[cls]
        rec = {"id": cid, "source": rel, "span": span, "expect": "supported"}
        if line is not None:
            rec["line"] = line
        keys = list(rec)
        rng.shuffle(keys)
        rows.append(json.dumps({k: rec[k] for k in keys}))
        files.append((rel, src))
        truth[cid] = (cls, t)
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
        print("mechanism-witness: gate not found: %s" % gate, file=sys.stderr)
        return 2
    gate_text = open(gate, encoding="utf-8", errors="surrogateescape").read()
    call_lines = matcher_entry_lines(gate_text)
    base = a.tmp or os.environ.get("WITNESS_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="w35wit-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("mechanism-witness: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    receipt = {"gate": gate, "gate_sha256": sha256_file(gate), "seed": seed,
               "matcher_entry_lines": call_lines, "fixture_root_prefix": os.path.basename(root)[:6]}
    try:
        if set(call_lines) != {"chunk", "direct"}:
            receipt.update({"witness": "unparseable", "output_match": 0, "output_total": TOTAL,
                            "reason": "matcher function entry lines not located"})
            print("WITNESS=unparseable (matcher call sites not found)")
            return 1
        claims, truth, scheme = generate(root, seed)
        receipt["source_name_scheme"] = scheme
        env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
        env["PS4"] = "%s${BASH_SOURCE}:${LINENO} " % MARK
        trace_path = os.path.join(root, "_trace.log")
        with open(trace_path, "wb") as tf:
            p = subprocess.run(["bash", "-x", gate, "verify-claims", claims, "--root", root],
                               stdout=subprocess.PIPE, stderr=tf, env=env, cwd=root, timeout=GATE_TIMEOUT_S)
        out = p.stdout.decode("utf-8", "replace")
        stamps = {"chunk": 0, "direct": 0}
        # bash replicates PS4's first character once per indirection level, so a
        # trace line inside a function or a process substitution starts with
        # "@@@..." instead of "@@..."; the marker is found by search, not prefix.
        stamp_re = re.compile(r"WITNESS@@(.*?):(\d+) ")
        for raw in open(trace_path, "rb"):
            line = raw.decode("utf-8", "replace")
            if MARK[2:] not in line:
                continue
            m = stamp_re.search(line)
            if not m or m.group(1) != gate:
                continue
            ln = int(m.group(2))
            for key, want in call_lines.items():
                if ln == want:
                    stamps[key] += 1
        observed = {}
        for line in out.splitlines():
            m = LINE_RE.match(line)
            if m and m.group(1) in truth:
                observed[m.group(1)] = m.group(2)
        drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
        misses, matched = [], 0
        for cid, (cls, t) in truth.items():
            obs = observed.get(cid, "none")
            ok = obs == t
            matched += ok
            if not ok:
                misses.append({"id": cid, "class": cls, "truth": t, "observed": obs})
        long_records = sum(1 for cls, t in truth.values() if cls != "short-verbatim")
        witness_ok = stamps["chunk"] >= long_records and stamps["chunk"] > 0
        receipt.update({"output_match": matched, "output_total": TOTAL,
                        "output_full": matched == TOTAL and p.returncode == 1 and drift,
                        "long_records": long_records, "stamps": stamps,
                        "witness": "pass" if witness_ok else "fail",
                        "gate_rc": p.returncode, "drift": drift, "misses": misses,
                        "elapsed_s": round(time.time() - t0, 2)})
        print("WITNESS=%s OUTPUT=%d/%d STAMPS chunk=%d direct=%d (long records=%d)"
              % (receipt["witness"], matched, TOTAL, stamps["chunk"], stamps["direct"], long_records))
        for m in misses:
            print("  MISS %s" % json.dumps(m, sort_keys=True))
    except subprocess.TimeoutExpired:
        receipt.update({"witness": "timeout", "output_match": 0, "output_total": TOTAL})
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
