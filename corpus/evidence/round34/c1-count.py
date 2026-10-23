#!/usr/bin/env python3
"""Round 34 C1 counter, design v1: `verify-claims` verifies spans of 32 KiB and more.

Frozen predicate (claims.md, C1, P1): C1 is met iff, on the landed lane revision,
this counter (c1-count.py) prints LONGSPAN_MATCH=30/30 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no committed run of this
counter on the landed gate prints a lower count.
Code condition: holds = matched == TOTAL (TOTAL = 30). Receipt label: predicate_holds.

Surface: the span matcher of `verify-claims` (`tok_span_at`, `tok_span_all` in
tools/research-gate.sh). At base both pass the span to grep(1) as one argv string of
4 bytes per span byte (`\\xHH`), so a span of 32768 bytes or more fails with
"Argument list too long" (E2BIG, the 131072-byte single-string limit) and the claim
reads observed=unsupported although the span is in the source verbatim.

Counted contract (claims.md, C1 contract):
- A span of 32768..65536 bytes that occurs in its source with token boundaries on
  both sides reads observed=supported; one that does not (one byte changed anywhere,
  split into two non-adjacent halves, or glued to a word character) reads
  observed=unsupported, exactly as the round-4..33 rules read short spans.
- With a "line" field, a long span binds iff some delimited occurrence starts and
  ends on the named lines (round 31); otherwise observed=mislocated and a
  CLAIM_LINE_MISMATCH finding names the id.
- Short spans (64..4096 bytes) keep their verdicts.

Fixture (generated per seed; the gate cannot know any of it in advance): a fresh temp
root, one source file per record, one claims JSONL of 30 records in 13 classes with
fixed counts. Every word is drawn from a per-seed random vocabulary of lowercase
letters; separators are one space or one newline. Spans start and end with a letter.
Every record carries expect="supported", so the label carries no truth; the hidden
truth is supported / unsupported / mislocated and is never written beside the claims.
Ids and file names are random hex, record order and file creation order are shuffled,
file mtimes are random. Mutation offsets, split points and line numbers are drawn per
record.

Classes (count; truth):
  long-verbatim-ml   3  supported    multi-line span, 33000..65000 bytes
  long-verbatim-1l   2  supported    single-line span (no newline), 33000..65000 bytes
  long-edge          2  supported    span of 32768..32900 bytes
  long-mut-head      2  unsupported  one letter changed within the first 64 bytes
  long-mut-tail      2  unsupported  one letter changed within the last 64 bytes (span >= 34000)
  long-mut-mid       3  unsupported  one letter changed at offset 8192..len-8192
  long-split         2  unsupported  both halves in the source, never adjacent
  long-glued-left    2  unsupported  only occurrence preceded by a letter
  long-glued-right   2  unsupported  only occurrence followed by a letter
  long-line-bound    2  supported    two delimited occurrences; "line" names the second
  long-line-wrong    2  mislocated   two delimited occurrences; "line" names neither
  short-verbatim     3  supported    64..4096 bytes
  short-mut          3  unsupported  64..4096 bytes, one letter changed

Per-record match: the gate prints exactly one `CLAIM id=<id> ...` line whose
observed= equals the truth, AND a `FINDING CLAIM_LINE_MISMATCH ... obs=id=<id>` exists
iff the truth is mislocated. An id printed on two CLAIM lines scores "none".

Exit: 0 iff matched == TOTAL; 1 otherwise; 2 harness error. A gate run that exits
other than 1, prints no `RESEARCH_GATE: DRIFT` line, or outlives 1500 s scores every
record "none" (the fixture always holds drifting records).
No network; writes only its temp dir (C1_TMP or TMPDIR), --keep and --receipt.
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

LABEL = "LONGSPAN_MATCH"
GATE_TIMEOUT_S = 1500
LONG_MIN = 32768
CLASS_COUNTS = [
    ("long-verbatim-ml", 3, "supported"),
    ("long-verbatim-1l", 2, "supported"),
    ("long-edge", 2, "supported"),
    ("long-mut-head", 2, "unsupported"),
    ("long-mut-tail", 2, "unsupported"),
    ("long-mut-mid", 3, "unsupported"),
    ("long-split", 2, "unsupported"),
    ("long-glued-left", 2, "unsupported"),
    ("long-glued-right", 2, "unsupported"),
    ("long-line-bound", 2, "supported"),
    ("long-line-wrong", 2, "mislocated"),
    ("short-verbatim", 3, "supported"),
    ("short-mut", 3, "unsupported"),
]
TOTAL = sum(n for _, n, _ in CLASS_COUNTS)
assert TOTAL == 30
LETTERS = "abcdefghijklmnopqrstuvwxyz"
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) ")
FIND_LINE_RE = re.compile(r"^FINDING CLAIM_LINE_MISMATCH .*\bobs=id=(\S+)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Gen:
    def __init__(self, rng):
        self.rng = rng
        self.vocab = ["".join(rng.choice(LETTERS) for _ in range(rng.randint(2, 9))) for _ in range(4000)]
        self.nl_every = rng.randint(8, 16)

    def text(self, nbytes, newlines=True):
        """Words joined by single separators; starts and ends with a letter; len >= nbytes."""
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
        s = self.text(self.rng.randint(lo, hi), newlines)
        if newlines and "\n" not in s:  # multi-line spans must cross a line
            i = s.index(" ", len(s) // 2)
            s = s[:i] + "\n" + s[i + 1:]
        return s

    def sep(self):
        return self.rng.choice([" ", "\n"])

    def filler(self, lo=200, hi=3000):
        return self.text(self.rng.randint(lo, hi))


def mutate(rng, span, lo, hi):
    """Change one letter at a letter offset in [lo, hi] to a different letter."""
    cand = [i for i in range(max(0, lo), min(len(span) - 1, hi) + 1) if span[i] in LETTERS]
    i = rng.choice(cand)
    c = rng.choice([x for x in LETTERS if x != span[i]])
    return span[:i] + c + span[i + 1:]


def line_range(text, off, span):
    l1 = text.count("\n", 0, off) + 1
    return l1, l1 + span.count("\n")


def build(gen, rng, cls):
    """-> (source_text, record_span, line_field_or_None, truth)"""
    g = gen
    if cls == "long-verbatim-ml":
        s = g.span(33000, 65000)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls == "long-verbatim-1l":
        s = g.span(33000, 65000, newlines=False)
        return g.filler() + "\n" + s + "\n" + g.filler() + "\n", s, None, "supported"
    if cls == "long-edge":
        while True:
            s = g.span(LONG_MIN, LONG_MIN + 120)
            if LONG_MIN <= len(s.encode()) <= 32900:
                break
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls in ("long-mut-head", "long-mut-tail", "long-mut-mid"):
        s = g.span(34000, 65000)
        if cls == "long-mut-head":
            m = mutate(rng, s, 0, 63)
        elif cls == "long-mut-tail":
            m = mutate(rng, s, len(s) - 64, len(s) - 1)
        else:
            m = mutate(rng, s, 8192, len(s) - 8192)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", m, None, "unsupported"
    if cls == "long-split":
        s = g.span(33000, 65000)
        seps = [i for i in range(len(s) // 4, 3 * len(s) // 4) if s[i] in " \n"]
        k = rng.choice(seps)
        p1, p2 = s[:k], s[k + 1:]
        src = g.filler() + g.sep() + p1 + g.sep() + g.filler(300, 2000) + g.sep() + p2 + g.sep() + g.filler() + "\n"
        return src, s, None, "unsupported"
    if cls == "long-glued-left":
        s = g.span(33000, 65000)
        return g.filler() + " " + rng.choice(LETTERS) + s + g.sep() + g.filler() + "\n", s, None, "unsupported"
    if cls == "long-glued-right":
        s = g.span(33000, 65000)
        return g.filler() + g.sep() + s + rng.choice(LETTERS) + " " + g.filler() + "\n", s, None, "unsupported"
    if cls in ("long-line-bound", "long-line-wrong"):
        s = g.span(33000, 65000)
        head = g.filler() + "\n"
        mid = "\n" + g.filler(300, 2000) + "\n"
        src = head + s + mid + s + "\n" + g.filler() + "\n"
        a1 = line_range(src, len(head), s)
        a2 = line_range(src, len(head) + len(s) + len(mid), s)
        if cls == "long-line-bound":
            return src, s, "%d-%d" % a2, "supported"
        wrong = (a1[0] + 1, a1[1] + 1)
        assert wrong not in (a1, a2)
        return src, s, "%d-%d" % wrong, "mislocated"
    if cls == "short-verbatim":
        s = g.span(64, 4096)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls == "short-mut":
        s = g.span(64, 4096)
        m = mutate(rng, s, 1, len(s) - 2)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", m, None, "unsupported"
    raise ValueError(cls)


def generate(root, seed):
    rng = random.Random(seed)
    gen = Gen(rng)
    os.makedirs(os.path.join(root, "src"))
    plan = [cls for cls, n, _ in CLASS_COUNTS for _ in range(n)]
    rng.shuffle(plan)
    rows, truth_map, files = [], {}, []
    want = {cls: t for cls, _, t in CLASS_COUNTS}
    for cls in plan:
        cid = "c%010x" % rng.getrandbits(40)
        while cid in truth_map:
            cid = "c%010x" % rng.getrandbits(40)
        rel = "src/%016x.md" % rng.getrandbits(64)
        src, span, line, truth = build(gen, rng, cls)
        assert truth == want[cls]
        rec = {"id": cid, "source": rel, "span": span, "expect": "supported"}
        if line is not None:
            rec["line"] = line
        keys = list(rec)
        rng.shuffle(keys)
        rows.append(json.dumps({k: rec[k] for k in keys}))
        files.append((rel, src))
        truth_map[cid] = (cls, truth)
    rng.shuffle(files)  # creation order carries no class
    for rel, text in files:
        p = os.path.join(root, rel)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        t = 1.6e9 + rng.randrange(10 ** 8)
        os.utime(p, (t, t))
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    return claims, truth_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--keep", default=None, help="copy the fixture and its truth here (audit only)")
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C1_TMP") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="chousa-r34-c1-", dir=base)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    rc, timed_out, stderr_tail = None, False, ""
    try:
        try:
            claims, truth = generate(root, seed)
        except Exception as e:
            print("c1-count: fixture generation failed: %r" % (e,), file=sys.stderr)
            return 2
        out = ""
        try:
            env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root], capture_output=True, env=env,
                               text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out, stderr_tail = p.returncode, p.stdout, p.stderr[-2000:]
        except subprocess.TimeoutExpired:
            timed_out = True
        observed, dup, f_line = {}, set(), set()
        drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
        if not timed_out and rc == 1 and drift:
            for line in out.splitlines():
                m = FIND_LINE_RE.match(line)
                if m:
                    f_line.add(m.group(1))
                m = LINE_RE.match(line)
                if m and m.group(1) in truth:
                    if m.group(1) in observed:
                        dup.add(m.group(1))
                    observed[m.group(1)] = m.group(2)
        for cid in dup:
            observed[cid] = "none"
        per_class, misses, matched = {}, [], 0
        for cid, (cls, t) in truth.items():
            obs = observed.get(cid, "none")
            ok = obs == t and ((cid in f_line) == (t == "mislocated"))
            if obs == t and not ok:
                obs += "+finding-set"
            matched += ok
            pc = per_class.setdefault(cls, [0, 0])
            pc[1] += 1
            pc[0] += ok
            if not ok:
                misses.append({"id": cid, "class": cls, "truth": t, "observed": obs})
        if a.keep:
            try:
                shutil.copytree(root, a.keep)
                with open(os.path.join(a.keep, "truth.json"), "w") as f:
                    json.dump({k: list(v) for k, v in truth.items()}, f, indent=1)
            except OSError as e:
                print("c1-count: --keep failed: %r" % (e,), file=sys.stderr)
                return 2
    finally:
        shutil.rmtree(root, ignore_errors=True)
    holds = matched == TOTAL
    label = "%s=%d/%d" % (LABEL, matched, TOTAL)
    print(label)
    for cls, _, _ in CLASS_COUNTS:
        print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r34-c1-receipt/v1",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "gate_stderr_tail": stderr_tail,
            "total": TOTAL, "matched": matched, "label": label, "predicate_holds": holds,
            "per_class": {k: "%d/%d" % tuple(v) for k, v in per_class.items()}, "misses": misses,
        }
        try:
            with open(a.receipt, "w") as f:
                json.dump(receipt, f, indent=1)
                f.write("\n")
        except OSError as e:
            print("c1-count: --receipt failed: %r" % (e,), file=sys.stderr)
            return 2
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
