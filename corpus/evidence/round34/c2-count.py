#!/usr/bin/env python3
"""Round 34 attempt 2, C2 counter, design v4: `verify-claims` verifies spans of
32765..32767 bytes (the PCRE dead zone just under the argv limit).

Frozen predicate (claims-a2.md, C2, P2): C2 is met iff, on the landed lane
revision, this counter (c2-count.py) prints DEADZONE_MATCH=37/37 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no committed run of this
counter on the landed gate prints a lower count.
Code condition: holds = matched == TOTAL (TOTAL = 37). Receipt label: predicate_holds.

Surface: the span matcher routes spans of length <= TOK_DIRECT_SPAN_MAX to one
grep(1) invocation carrying the span as one \\xHH PCRE pattern of four argv bytes
per span byte, and longer spans to the round-34 chunk matcher. Two ceilings bound
the direct path: execve(2) MAX_ARG_STRLEN (span >= 32768 -> E2BIG, C1's surface)
and PCRE2's compiled-pattern ceiling ("approximately 64 thousand code units",
pcre2limits(3), row S065). On this host the second ceiling binds first: a pattern
for a 32764-byte span compiles; 32765 fails with "regular expression is too
large". Spans of 32765..32767 bytes therefore read observed=unsupported even when
the source holds the span verbatim. C2 moves exactly those three lengths onto the
chunk matcher by lowering TOK_DIRECT_SPAN_MAX to 32764; no other matcher change.

The fixture: one root, one source file per record, one claims JSONL of 37 records
in 17 classes (below), all content generated per seed: random lowercase
vocabulary, random separators, span lengths drawn in 32765..32767 (enforced at a
word end), mutation offsets (head <=63, tail last 64, center within 64 of len/2),
near-copy decoy edits (substitution, adjacent transposition, upper-casing,
separator swap), split points and line positions; ids and file names random hex;
record and file-creation order shuffled; random mtimes. Every record carries
expect="supported", so the label carries no truth; the hidden truth per class:
- dz-verbatim-ml 3 supported (multi-line span, delimited occurrence)
- dz-verbatim-1l 2 supported (single-line span)
- dz-edge 2 supported (length exactly 32765 and exactly 32767)
- dz-mut-head 2 / dz-mut-tail 2 / dz-mut-center 2 unsupported (one letter changed)
- dz-decoys 5 unsupported (12 near-copies, no exact copy: a gate that compares
  only a fraction g of the span's bytes passes with probability about g**12)
- dz-decoys-exact 2 supported (one exact copy among the near-copies)
- dz-decoys-line-wrong 2 mislocated (exact copy present, "line" names a decoy's
  lines: requires exact occurrence enumeration for line binding)
- dz-split 2 unsupported (both halves present, never adjacent)
- dz-glued-left 2 / dz-glued-right 2 unsupported (glued to a word character)
- dz-glued-then-valid 1 supported (glued occurrence first, delimited one later)
- dz-line-bound 2 supported / dz-line-wrong 2 mislocated (round-31 line binding)
- short-verbatim 2 supported / short-mut 2 unsupported (64..4096 bytes, the
  unchanged direct path, as controls)

Per-record match: the gate prints exactly one `CLAIM id=<id> ...` line whose
observed= equals the truth, and a FINDING CLAIM_LINE_MISMATCH line naming the id
iff the truth is mislocated.
Exit: 0 iff matched == TOTAL; 1 otherwise; 2 harness error. A gate run that exits
other than 1, prints no `RESEARCH_GATE: DRIFT` line, or outlives 1500 s scores
every record "none" (the fixture always holds drifting records).
No network; writes only its temp dir (C2_TMP or C1_TMP or TMPDIR), --keep and
--receipt.
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

LABEL = "DEADZONE_MATCH"
GATE_TIMEOUT_S = 1500
DZ_MIN = 32765
DZ_MAX = 32767
CLASS_COUNTS = [
    ("dz-verbatim-ml", 3, "supported"),
    ("dz-verbatim-1l", 2, "supported"),
    ("dz-edge", 2, "supported"),
    ("dz-mut-head", 2, "unsupported"),
    ("dz-mut-tail", 2, "unsupported"),
    ("dz-mut-center", 2, "unsupported"),
    ("dz-decoys", 5, "unsupported"),
    ("dz-decoys-exact", 2, "supported"),
    ("dz-decoys-line-wrong", 2, "mislocated"),
    ("dz-split", 2, "unsupported"),
    ("dz-glued-left", 2, "unsupported"),
    ("dz-glued-right", 2, "unsupported"),
    ("dz-glued-then-valid", 1, "supported"),
    ("dz-line-bound", 2, "supported"),
    ("dz-line-wrong", 2, "mislocated"),
    ("short-verbatim", 2, "supported"),
    ("short-mut", 2, "unsupported"),
]
TOTAL = sum(n for _, n, _ in CLASS_COUNTS)
assert TOTAL == 37
DECOYS = 11          # dz-decoys-exact / dz-decoys-line-wrong hold 11 decoys + 1 exact
DECOYS_ABSENT = 12   # dz-decoys holds 12 near-copies, none exact
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
        """A span whose byte length is in [lo, hi], cut at a word end.

        The dead-zone classes must place the span inside 32765..32767 exactly, so
        the cut is the LAST separator position in [lo, hi]; text is extended until
        such a separator exists (words are <=9 bytes, the window is 3, so a
        separator falls inside within a few draws).
        """
        rng = self.rng
        while True:  # redraw the base text until a word end falls in [lo, hi]
            s = self.text(hi + 12, newlines)
            cuts = [i for i in range(lo, min(hi, len(s) - 1) + 1) if s[i] in " \n" and s[i - 1] in LETTERS]
            if cuts:
                s = s[:cuts[-1]]
                break
        if newlines and "\n" not in s:  # multi-line spans must cross a line
            i = s.index(" ", len(s) // 2)
            s = s[:i] + "\n" + s[i + 1:]
        assert lo <= len(s.encode()) <= hi, (lo, hi, len(s.encode()))
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


def decoy(rng, span):
    """One edit at a uniform offset, of a kind drawn per decoy; never equal to span."""
    kind = rng.choice(["sub", "swap", "upper", "sep"])
    if kind == "sub":
        return mutate(rng, span, 0, len(span) - 1)
    if kind == "swap":
        cand = [i for i in range(len(span) - 1)
                if span[i] in LETTERS and span[i + 1] in LETTERS and span[i] != span[i + 1]]
        i = rng.choice(cand)
        return span[:i] + span[i + 1] + span[i] + span[i + 2:]
    if kind == "upper":
        i = rng.choice([i for i in range(len(span)) if span[i] in LETTERS])
        return span[:i] + span[i].upper() + span[i + 1:]
    i = rng.choice([i for i in range(len(span)) if span[i] in " \n"])
    return span[:i] + ("\n" if span[i] == " " else " ") + span[i + 1:]


def line_range(text, off, span):
    l1 = text.count("\n", 0, off) + 1
    return l1, l1 + span.count("\n")


def build(gen, rng, cls):
    """-> (source_text, record_span, line_field_or_None, truth)"""
    g = gen
    if cls == "dz-verbatim-ml":
        s = g.span(DZ_MIN, DZ_MAX)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls == "dz-verbatim-1l":
        s = g.span(DZ_MIN, DZ_MAX, newlines=False)
        return g.filler() + "\n" + s + "\n" + g.filler() + "\n", s, None, "supported"
    if cls == "dz-edge":
        n = rng.choice([DZ_MIN, DZ_MAX])
        s = g.span(n, n)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls in ("dz-decoys", "dz-decoys-exact", "dz-decoys-line-wrong"):
        s = g.span(DZ_MIN, DZ_MAX)
        copies = [decoy(rng, s) for _ in range(DECOYS_ABSENT if cls == "dz-decoys" else DECOYS)]
        exact = None
        if cls != "dz-decoys":
            exact = rng.randrange(DECOYS + 1)
            copies.insert(exact, s)
        src, offs = g.filler() + "\n", []
        for c in copies:
            offs.append(len(src))
            src += c + "\n" + g.filler(300, 2000) + "\n"
        if cls == "dz-decoys":
            return src, s, None, "unsupported"
        if cls == "dz-decoys-exact":
            return src, s, None, "supported"
        j = rng.choice([k for k in range(len(copies)) if k != exact])
        named = line_range(src, offs[j], s)
        assert named != line_range(src, offs[exact], s)
        return src, s, "%d-%d" % named, "mislocated"
    if cls in ("dz-mut-head", "dz-mut-tail", "dz-mut-center"):
        s = g.span(DZ_MIN, DZ_MAX)
        if cls == "dz-mut-head":
            m = mutate(rng, s, 0, 63)
        elif cls == "dz-mut-tail":
            m = mutate(rng, s, len(s) - 64, len(s) - 1)
        else:
            m = mutate(rng, s, len(s) // 2 - 64, len(s) // 2 + 64)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", m, None, "unsupported"
    if cls == "dz-split":
        s = g.span(DZ_MIN, DZ_MAX)
        seps = [i for i in range(len(s) // 4, 3 * len(s) // 4) if s[i] in " \n"]
        k = rng.choice(seps)
        p1, p2 = s[:k], s[k + 1:]
        src = g.filler() + g.sep() + p1 + g.sep() + g.filler(300, 2000) + g.sep() + p2 + g.sep() + g.filler() + "\n"
        return src, s, None, "unsupported"
    if cls == "dz-glued-left":
        s = g.span(DZ_MIN, DZ_MAX)
        return g.filler() + " " + rng.choice(LETTERS) + s + g.sep() + g.filler() + "\n", s, None, "unsupported"
    if cls == "dz-glued-then-valid":
        s = g.span(DZ_MIN, DZ_MAX)
        return (g.filler() + " " + rng.choice(LETTERS) + s + g.sep() + g.filler(300, 2000) + g.sep() + s + g.sep()
                + g.filler() + "\n", s, None, "supported")
    if cls == "dz-glued-right":
        s = g.span(DZ_MIN, DZ_MAX)
        return g.filler() + g.sep() + s + rng.choice(LETTERS) + " " + g.filler() + "\n", s, None, "unsupported"
    if cls in ("dz-line-bound", "dz-line-wrong"):
        s = g.span(DZ_MIN, DZ_MAX)
        head = g.filler() + "\n"
        mid = "\n" + g.filler(300, 2000) + "\n"
        src = head + s + mid + s + "\n" + g.filler() + "\n"
        a1 = line_range(src, len(head), s)
        a2 = line_range(src, len(head) + len(s) + len(mid), s)
        if cls == "dz-line-bound":
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
        print("c2-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C2_TMP") or os.environ.get("C1_TMP") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="chousa-r34-c2-", dir=base)
    except OSError as e:
        print("c2-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    rc, timed_out, stderr_tail = None, False, ""
    try:
        try:
            claims, truth = generate(root, seed)
        except Exception as e:
            print("c2-count: fixture generation failed: %r" % (e,), file=sys.stderr)
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
                print("c2-count: --keep failed: %r" % (e,), file=sys.stderr)
                return 2
    finally:
        shutil.rmtree(root, ignore_errors=True)
    holds = matched == TOTAL
    label = "%s=%d/%d" % (LABEL, matched, TOTAL)
    if a.receipt:
        receipt = {
            "schema": "chousa-r34-c2-receipt/v1",
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
            print("c2-count: --receipt failed: %r" % (e,), file=sys.stderr)
            return 2
    try:
        print(label)
        for cls, _, _ in CLASS_COUNTS:
            v = per_class.get(cls, [0, 0])
            print("  %s %d/%d" % (cls, v[0], v[1]))
        for m_ in misses:
            print("  MISS %s %s truth=%s observed=%s" % (m_["id"], m_["class"], m_["truth"], m_["observed"]))
    except BrokenPipeError:
        pass
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
