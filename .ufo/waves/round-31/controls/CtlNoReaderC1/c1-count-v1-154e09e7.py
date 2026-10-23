#!/usr/bin/env python3
"""Round 31 C1 counter: claim location binding in `research-gate.sh verify-claims`.

Frozen predicate (claims.md, C1): C1 is met iff, on the landed lane revision,
this counter prints LINE_BINDING_MATCH=120/120 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no run of this
counter on that revision in round 31 prints a lower count.

The counter writes a fresh fixture under a temporary root: opaque source
files and one claims JSONL with 120 claims. Every claim carries
expect=supported (a constant, so the label carries no truth). The hidden
truth per claim is one of supported / mislocated / invalid / unsupported and
is never written next to the claims. The counter runs
`bash <gate> verify-claims <claims> --root <tmp>` once and compares each
`CLAIM id=<id> ... observed=<obs>` line with the hidden truth.

Contract the candidate must meet (claims.md, C1 contract):
- optional JSON string field "line": "N" or "N-M" (N>=1, M>N, decimal, no
  leading zero, no spaces); any other value of a present "line" -> invalid.
- span absent (no boundary-delimited occurrence) -> unsupported, as today.
- span present, "line" present: bound iff some boundary-delimited occurrence
  of the span starts on line N and ends on line N ("N") or starts on N and
  ends on M ("N-M"); bound -> supported; not bound -> mislocated.
- "line" absent -> unchanged behaviour.

Exit: 0 iff matched == 120; 1 otherwise; 2 harness error. A gate run that
exits other than 0 or 1, or outlives 600 s, scores every claim as observed
"none" (not matched). No network; writes only its temp dir and --receipt.
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

TOTAL = 120
CLASS_COUNTS = [
    ("B1_bound_single", 12, "supported"),
    ("B2_bound_later_occurrence", 12, "supported"),
    ("B3_bound_multiline", 12, "supported"),
    ("B4_no_line", 6, "supported"),
    ("M1_other_line", 12, "mislocated"),
    ("M2_glued_on_named_line", 12, "mislocated"),
    ("M3_partial_on_named_line", 12, "mislocated"),
    ("M4_multiline_wrong_range", 8, "mislocated"),
    ("M5_beyond_eof", 6, "mislocated"),
    ("M6_two_occurrences_named_third", 8, "mislocated"),
    ("I1_invalid_line_value", 12, "invalid"),
    ("U1_absent_span_with_line", 8, "unsupported"),
]
assert sum(c for _, c, _ in CLASS_COUNTS) == TOTAL
INVALID_VALUES = ["0", "-3", "x7", "5-3", "07", "4-4", " 4", "4 ", "4-", "-4", "1.5", "4\u20135"]
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
GATE_TIMEOUT_S = 600
LINE_RE = re.compile(r"^CLAIM id=(\S+) .*?observed=(\S+)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class Gen:
    def __init__(self, rng):
        self.rng = rng
        self.used = set()

    def word(self):
        while True:
            w = "".join(self.rng.choice(SYL) for _ in range(self.rng.randint(2, 4)))
            if w not in self.used:
                self.used.add(w)
                return w

    def filler_line(self):
        return " ".join(self.word() for _ in range(self.rng.randint(5, 9))) + "."

    def span(self):
        return " ".join(self.word() for _ in range(self.rng.randint(4, 7)))


def build_item(gen, rng, cls):
    """Return (lines, span, line_value or None). lines are without newline."""
    n = rng.randint(14, 30)
    lines = [gen.filler_line() for _ in range(n)]

    def put(idx, text):  # place a delimited occurrence inside line idx (0-based)
        lines[idx] = gen.word() + " " + text + ". " + gen.word() + "."

    span = gen.span()
    if cls == "B1_bound_single":
        L = rng.randrange(n); put(L, span)
        return lines, span, str(L + 1)
    if cls == "B2_bound_later_occurrence":
        k = rng.choice([2, 3]); idxs = sorted(rng.sample(range(n), k))
        for i in idxs: put(i, span)
        return lines, span, str(rng.choice(idxs[1:]) + 1)
    if cls in ("B3_bound_multiline", "M4_multiline_wrong_range"):
        words = span.split(" "); cut = rng.randint(1, len(words) - 1)
        a = rng.randrange(n - 3)
        first, second = " ".join(words[:cut]), " ".join(words[cut:])
        lines[a] = gen.word() + " " + gen.word() + " " + first
        lines[a + 1] = second + ", " + gen.word() + " " + gen.word() + "."
        mspan = first + "\n" + second
        if cls == "B3_bound_multiline":
            return lines, mspan, "%d-%d" % (a + 1, a + 2)
        wrong = rng.choice(["start", "end", "wide", "late"])
        val = {"start": str(a + 1), "end": str(a + 2), "wide": "%d-%d" % (a + 1, a + 3),
               "late": "%d-%d" % (a + 2, a + 3)}[wrong]
        return lines, mspan, val
    if cls == "B4_no_line":
        L = rng.randrange(n); put(L, span)
        return lines, span, None
    if cls == "M1_other_line":
        L, O = rng.sample(range(n), 2); put(L, span)
        return lines, span, str(O + 1)
    if cls == "M2_glued_on_named_line":
        L, O = rng.sample(range(n), 2); put(L, span)
        glue = rng.choice(["prefix", "suffix"])
        if glue == "prefix":
            lines[O] = gen.word() + " " + gen.word() + span + " " + gen.word() + "."
        else:
            lines[O] = gen.word() + " " + span + gen.word() + " " + gen.word() + "."
        return lines, span, str(O + 1)
    if cls == "M3_partial_on_named_line":
        L, O = rng.sample(range(n), 2); put(L, span)
        words = span.split(" "); k = rng.randint(2, len(words) - 1)
        lines[O] = gen.word() + " " + " ".join(words[:k]) + " " + gen.word() + " " + gen.word() + "."
        return lines, span, str(O + 1)
    if cls == "M5_beyond_eof":
        L = rng.randrange(n); put(L, span)
        return lines, span, str(n + rng.randint(1, 40))
    if cls == "M6_two_occurrences_named_third":
        a, b, O = rng.sample(range(n), 3); put(a, span); put(b, span)
        return lines, span, str(O + 1)
    if cls == "I1_invalid_line_value":
        L = rng.randrange(n); put(L, span)
        return lines, span, None  # value assigned by caller
    if cls == "U1_absent_span_with_line":
        L = rng.randrange(n)
        words = span.split(" ")
        near = " ".join(words[:-1] + [gen.word()])  # same prefix, different last word
        put(L, near)
        return lines, span, str(L + 1)
    raise ValueError(cls)


def generate(root, seed):
    rng = random.Random(seed)
    gen = Gen(rng)
    os.makedirs(os.path.join(root, "src"))
    plan = []
    for cls, count, truth in CLASS_COUNTS:
        plan += [(cls, truth)] * count
    rng.shuffle(plan)
    inv = list(INVALID_VALUES); rng.shuffle(inv); inv_i = 0
    rows, truth_map = [], {}
    for cls, truth in plan:
        lines, span, line_value = build_item(gen, rng, cls)
        if cls == "I1_invalid_line_value":
            line_value = inv[inv_i % len(inv)]; inv_i += 1
        fid = "%016x" % rng.getrandbits(64)
        rel = "src/%s.md" % fid
        with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        cid = "c%010x" % rng.getrandbits(40)
        rec = {"id": cid, "claim": "fixture claim " + cid, "source": rel, "span": span, "expect": "supported"}
        if line_value is not None:
            rec["line"] = line_value
        keys = list(rec.keys()); rng.shuffle(keys)  # key order carries nothing
        rows.append(json.dumps({k: rec[k] for k in keys}, ensure_ascii=False))
        truth_map[cid] = (cls, truth)
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    return claims, truth_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--keep", default=None, help="copy the fixture here (audit only)")
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr); return 2
    base = os.environ.get("C1_TMP") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="chousa-r31-c1-", dir=base)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr); return 2
    t0 = time.time()
    try:
        claims, truth = generate(root, seed)
        rc, out, err, timed_out = None, "", "", False
        try:
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root], capture_output=True,
                               text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            timed_out = True
        observed = {}
        if not timed_out and rc in (0, 1):
            for line in out.splitlines():
                m = LINE_RE.match(line)
                if m and m.group(1) in truth and m.group(1) not in observed:
                    observed[m.group(1)] = m.group(2)
        per_class, misses, matched = {}, [], 0
        for cid, (cls, t) in truth.items():
            obs = observed.get(cid, "none")
            ok = obs == t
            matched += ok
            pc = per_class.setdefault(cls, [0, 0]); pc[1] += 1; pc[0] += ok
            if not ok:
                misses.append({"id": cid, "class": cls, "truth": t, "observed": obs})
        if a.keep:
            shutil.copytree(root, a.keep)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    holds = matched == TOTAL
    print("LINE_BINDING_MATCH=%d/%d" % (matched, TOTAL))
    for cls, _, _ in CLASS_COUNTS:
        print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r31-c1-receipt/v1",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "total": TOTAL, "matched": matched,
            "label": "LINE_BINDING_MATCH=%d/%d" % (matched, TOTAL), "predicate_holds": holds,
            "per_class": {k: "%d/%d" % tuple(v) for k, v in per_class.items()}, "misses": misses,
        }
        with open(a.receipt, "w") as f:
            json.dump(receipt, f, indent=1)
            f.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
