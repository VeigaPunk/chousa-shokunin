#!/usr/bin/env python3
"""Round 34 C1 counter, design v3: `verify-claims` verifies spans of 32 KiB and more.

Frozen predicate (claims.md, C1, P1 v3): C1 is met iff, on the landed lane revision,
this counter (c1-count-v3.py) prints LONGSPAN_MATCH=42/42 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no committed run of this
counter on the landed gate prints a lower count.
Code condition: holds = matched == TOTAL (TOTAL = 42). Receipt label: predicate_holds
(the per-run condition; P1 needs two such receipts and no committed landed-gate
receipt with predicate_holds=false).

v3 changes against v2 (c1-count-v2.py, kept frozen and unedited), made before any
candidate was scored, after CritC1Shapes (.ufo/waves/round-34/w1/CritC1Shapes.md) named
gate shapes no v2 class distinguishes: order-insensitive fingerprints (byte sum,
histogram), whitespace-normalising and case-insensitive comparison, and a matcher that
keeps only the first raw occurrence; and after CritC1AxisFit noted that no generated
span exceeded 65009 bytes although the contract names 65536.
- Each near-copy decoy now carries one edit of a kind drawn per decoy: a letter
  substituted by another lowercase letter, two adjacent different letters transposed,
  a letter upper-cased, or one separator swapped (space <-> newline). A gate that is
  order-blind, case-blind or whitespace-blind accepts some decoy on almost every seed.
- long-glued-then-valid (2, supported): the source holds a glued occurrence first and a
  delimited one later.
- Long span lengths are drawn up to 65536 bytes (text is trimmed to the drawn length at
  a word end, never above it).
- long-decoys holds 24 near-copies instead of 8 (sources up to about 1.7 MB, under the
  gate's 8 MiB read limit): a gate that compares all but a fraction g of a long span's
  bytes passes that class with probability about (1-g)**168 per seed (g=0.02: 0.03).
- TOTAL 40 -> 42. Matching rule, run bounds and every other class unchanged.

v2 changes against v1 (c1-count.py, kept frozen and unedited), made before any
candidate was scored, after the L1-built window controls (CtlC1Windows was a
cyber_policy hold; .ufo/waves/round-34/controls/L1-windows/): a gate that compares
only the first and last 16384 bytes of a long span at consistent offsets (the middle
never compared) scored 30/30 under v1 on seed 3421, and a gate that compares 90% of
the bytes (three windows) scored 30/30 on seeds 3421-3424, because v1's single
middle mutation per record often fell inside the compared bytes.
- long-mut-mid (3, offset 8192..len-8192) is replaced by long-mut-center (2, offset
  within 64 bytes of len/2: any check that skips the centre misses it on every seed).
- Near-copy decoys: a source may hold DECOYS=8 copies of the span, each with one
  letter changed at an offset drawn uniformly over the whole span. A gate that
  accepts a copy matching only on some bytes accepts a decoy. long-decoys (7, no
  exact copy, unsupported) is matched by a gate that compares a fixed fraction f of
  the bytes with probability about f**56 per seed (f=0.9: 0.003);
  long-decoys-exact (2, one exact copy among the decoys, supported) and
  long-decoys-line-wrong (2, exact copy present, "line" names a decoy's lines,
  mislocated) require exact occurrence enumeration for line binding.
- TOTAL 30 -> 40. Matching rule, run bounds and every other class unchanged.

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
root, one source file per record, one claims JSONL of 42 records in 17 classes with
fixed counts. Every word is drawn from a per-seed random vocabulary of lowercase
letters; separators are one space or one newline. Spans start and end with a letter.
Every record carries expect="supported", so the label carries no truth; the hidden
truth is supported / unsupported / mislocated and is never written beside the claims.
Ids and file names are random hex, record order and file creation order are shuffled,
file mtimes are random. Mutation offsets, split points and line numbers are drawn per
record.

Classes (count; truth):
  long-verbatim-ml   3  supported    multi-line span, about 33000..65536 bytes
  long-verbatim-1l   2  supported    single-line span (no newline), about 33000..65536 bytes
  long-edge          2  supported    span of 32768..32900 bytes
  long-mut-head      2  unsupported  one letter changed within the first 64 bytes
  long-mut-tail      2  unsupported  one letter changed within the last 64 bytes (span >= 34000)
  long-mut-center    2  unsupported  one letter changed within 64 bytes of len/2
  long-decoys        7  unsupported  24 near-copy decoys (one edit each: substitution, transposition,
                                     upper-casing or separator swap, uniform offset), no exact copy
  long-decoys-exact  2  supported    8 decoys plus one exact copy at a random slot
  long-decoys-line-wrong 2 mislocated  8 decoys plus one exact copy; "line" names a decoy's lines
  long-split         2  unsupported  both halves in the source, never adjacent
  long-glued-left    2  unsupported  only occurrence preceded by a letter
  long-glued-right   2  unsupported  only occurrence followed by a letter
  long-glued-then-valid 2 supported  a glued occurrence first, a delimited one later
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
    ("long-mut-center", 2, "unsupported"),
    ("long-decoys", 7, "unsupported"),
    ("long-decoys-exact", 2, "supported"),
    ("long-decoys-line-wrong", 2, "mislocated"),
    ("long-split", 2, "unsupported"),
    ("long-glued-left", 2, "unsupported"),
    ("long-glued-right", 2, "unsupported"),
    ("long-glued-then-valid", 2, "supported"),
    ("long-line-bound", 2, "supported"),
    ("long-line-wrong", 2, "mislocated"),
    ("short-verbatim", 3, "supported"),
    ("short-mut", 3, "unsupported"),
]
TOTAL = sum(n for _, n, _ in CLASS_COUNTS)
assert TOTAL == 42
DECOYS = 8
DECOYS_ABSENT = 24  # long-decoys: no exact copy among 24 near-copies
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
        n = self.rng.randint(lo, hi)
        s = self.text(n, newlines)
        if len(s) > n:  # trim to the drawn length at a word end (v3: lengths reach 65536)
            cut = max(s.rfind(" ", 0, n + 1), s.rfind("\n", 0, n + 1))
            s = s[:cut]
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
    if cls == "long-verbatim-ml":
        s = g.span(33000, 65536)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls == "long-verbatim-1l":
        s = g.span(33000, 65536, newlines=False)
        return g.filler() + "\n" + s + "\n" + g.filler() + "\n", s, None, "supported"
    if cls == "long-edge":
        while True:
            s = g.span(LONG_MIN, LONG_MIN + 120)
            if LONG_MIN <= len(s.encode()) <= 32900:
                break
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", s, None, "supported"
    if cls in ("long-decoys", "long-decoys-exact", "long-decoys-line-wrong"):
        s = g.span(33000, 65536)
        copies = [decoy(rng, s) for _ in range(DECOYS_ABSENT if cls == "long-decoys" else DECOYS)]
        exact = None
        if cls != "long-decoys":
            exact = rng.randrange(DECOYS + 1)
            copies.insert(exact, s)
        src, offs = g.filler() + "\n", []
        for c in copies:
            offs.append(len(src))
            src += c + "\n" + g.filler(300, 2000) + "\n"
        if cls == "long-decoys":
            return src, s, None, "unsupported"
        if cls == "long-decoys-exact":
            return src, s, None, "supported"
        j = rng.choice([k for k in range(len(copies)) if k != exact])
        named = line_range(src, offs[j], s)
        assert named != line_range(src, offs[exact], s)
        return src, s, "%d-%d" % named, "mislocated"
    if cls in ("long-mut-head", "long-mut-tail", "long-mut-center"):
        s = g.span(34000, 65536)
        if cls == "long-mut-head":
            m = mutate(rng, s, 0, 63)
        elif cls == "long-mut-tail":
            m = mutate(rng, s, len(s) - 64, len(s) - 1)
        else:
            m = mutate(rng, s, len(s) // 2 - 64, len(s) // 2 + 64)
        return g.filler() + g.sep() + s + g.sep() + g.filler() + "\n", m, None, "unsupported"
    if cls == "long-split":
        s = g.span(33000, 65536)
        seps = [i for i in range(len(s) // 4, 3 * len(s) // 4) if s[i] in " \n"]
        k = rng.choice(seps)
        p1, p2 = s[:k], s[k + 1:]
        src = g.filler() + g.sep() + p1 + g.sep() + g.filler(300, 2000) + g.sep() + p2 + g.sep() + g.filler() + "\n"
        return src, s, None, "unsupported"
    if cls == "long-glued-left":
        s = g.span(33000, 65536)
        return g.filler() + " " + rng.choice(LETTERS) + s + g.sep() + g.filler() + "\n", s, None, "unsupported"
    if cls == "long-glued-then-valid":
        s = g.span(33000, 65536)
        return (g.filler() + " " + rng.choice(LETTERS) + s + g.sep() + g.filler(300, 2000) + g.sep() + s + g.sep()
                + g.filler() + "\n", s, None, "supported")
    if cls == "long-glued-right":
        s = g.span(33000, 65536)
        return g.filler() + g.sep() + s + rng.choice(LETTERS) + " " + g.filler() + "\n", s, None, "unsupported"
    if cls in ("long-line-bound", "long-line-wrong"):
        s = g.span(33000, 65536)
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
    if a.receipt:
        receipt = {
            "schema": "chousa-r34-c1-receipt/v3",
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
    try:
        print(label)
        for cls, _, _ in CLASS_COUNTS:
            print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    except BrokenPipeError:
        pass
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
