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
  of the span (not necessarily the first) starts on line N and ends on line N
  ("N") or starts on N and ends on M ("N-M"); line numbers are 1-based,
  counted by newlines as in the gate's at=; bound -> supported; not bound ->
  mislocated, and the gate prints
  "FINDING CLAIM_LINE_MISMATCH severity=warn|crit surface=claims obs=id=<id> ..."
  for that claim; no such finding names any other claim.
- "line" absent -> unchanged behaviour; unknown JSON keys are ignored, as at base.

Design v2 (claims.md): fixed sub-variant counts per class (M3 includes
inner-word damage with both endpoint tokens intact; M4 wrong ranges keep the
true start line or the true end line), the finding rule
above, CHOUSA_* environment variables removed from the gate's environment, an
id reported twice scores "none", harness errors exit 2.

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
# design v2: the claim-level finding must name the claim (obs=id=<id>), and only for
# claims whose truth is mislocated.
FINDING_ID = "CLAIM_LINE_MISMATCH"
FINDING_TRUTH = "mislocated"
FINDING_RE = re.compile(r"^FINDING " + FINDING_ID + r" severity=(?:warn|crit) surface=claims obs=id=(\S+)(?:\s|$)")


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


# Sub-variant counts are fixed per class (design v2): a gate that mishandles one
# sub-variant must miss it on every seed, never only on the seeds that happen to
# draw it.
SUBVARIANTS = {
    "B1_bound_single": ["first_line"] * 2 + ["last_line"] * 2 + ["inner"] * 8,
    "B2_bound_later_occurrence": ["k2_second"] * 6 + ["k3_second"] * 3 + ["k3_third"] * 3,
    "B3_bound_multiline": ["inner"] * 12,
    "B4_no_line": ["inner"] * 6,
    "M1_other_line": ["adjacent_before"] * 3 + ["adjacent_after"] * 3 + ["far"] * 6,
    "M2_glued_on_named_line": ["prefix"] * 6 + ["suffix"] * 6,
    "M3_partial_on_named_line": ["prefix"] * 4 + ["mid_sub"] * 4 + ["mid_swap"] * 4,
    "M4_multiline_wrong_range": ["start", "wide", "end", "early"] * 2,
    "M5_beyond_eof": ["inner"] * 6,
    "M6_two_occurrences_named_third": ["inner"] * 8,
    "I1_invalid_line_value": list(INVALID_VALUES),
    "U1_absent_span_with_line": ["inner"] * 8,
}
for _cls, _n, _t in CLASS_COUNTS:
    assert len(SUBVARIANTS[_cls]) == _n, _cls


def build_item(gen, rng, cls, sub):
    """Return (lines, span, line_value or None). lines are without newline."""
    n = rng.randint(14, 30)
    lines = [gen.filler_line() for _ in range(n)]

    def put(idx, text):  # place a delimited occurrence inside line idx (0-based)
        lines[idx] = gen.word() + " " + text + ". " + gen.word() + "."

    span = gen.span()
    if cls == "B1_bound_single":
        L = {"first_line": 0, "last_line": n - 1}.get(sub, None)
        if L is None:
            L = rng.randrange(1, n - 1)
        put(L, span)
        return lines, span, str(L + 1)
    if cls == "B2_bound_later_occurrence":
        k = 2 if sub == "k2_second" else 3
        idxs = sorted(rng.sample(range(n), k))
        for i in idxs: put(i, span)
        named = idxs[2] if sub == "k3_third" else idxs[1]
        return lines, span, str(named + 1)
    if cls in ("B3_bound_multiline", "M4_multiline_wrong_range"):
        words = span.split(" "); cut = rng.randint(1, len(words) - 1)
        a = rng.randrange(1, n - 3)
        first, second = " ".join(words[:cut]), " ".join(words[cut:])
        lines[a] = gen.word() + " " + gen.word() + " " + first
        lines[a + 1] = second + ", " + gen.word() + " " + gen.word() + "."
        mspan = first + "\n" + second
        if cls == "B3_bound_multiline":
            return lines, mspan, "%d-%d" % (a + 1, a + 2)
        # start/wide keep the true start line, end/early keep the true end line (v2)
        val = {"start": str(a + 1), "wide": "%d-%d" % (a + 1, a + 3), "end": str(a + 2),
               "early": "%d-%d" % (a, a + 2)}[sub]
        return lines, mspan, val
    if cls == "B4_no_line":
        L = rng.randrange(n); put(L, span)
        return lines, span, None
    if cls == "M1_other_line":
        L = rng.randrange(1, n - 1); put(L, span)
        if sub == "adjacent_before":
            O = L - 1
        elif sub == "adjacent_after":
            O = L + 1
        else:
            O = rng.choice([i for i in range(n) if abs(i - L) > 1])
        return lines, span, str(O + 1)
    if cls == "M2_glued_on_named_line":
        L, O = rng.sample(range(n), 2); put(L, span)
        if sub == "prefix":
            lines[O] = gen.word() + " " + gen.word() + span + " " + gen.word() + "."
        else:
            lines[O] = gen.word() + " " + span + gen.word() + " " + gen.word() + "."
        return lines, span, str(O + 1)
    if cls == "M3_partial_on_named_line":
        L, O = rng.sample(range(n), 2); put(L, span)
        words = span.split(" ")
        if sub == "prefix":
            k = rng.randint(2, len(words) - 1)
            text = " ".join(words[:k]) + " " + gen.word()
        elif sub == "mid_sub":  # both endpoint tokens intact, one inner word replaced (v2)
            j = rng.randint(1, len(words) - 2)
            text = " ".join(words[:j] + [gen.word()] + words[j + 1:])
        else:  # mid_swap: endpoints intact, two inner words swapped (v2)
            j = rng.randint(1, len(words) - 3) if len(words) >= 4 else 1
            w = list(words); w[j], w[j + 1] = w[j + 1], w[j]
            text = " ".join(w)
        lines[O] = gen.word() + " " + text + ". " + gen.word() + "."
        return lines, span, str(O + 1)
    if cls == "M5_beyond_eof":
        L = rng.randrange(n); put(L, span)
        return lines, span, str(n + rng.randint(1, 40))
    if cls == "M6_two_occurrences_named_third":
        a, b, O = rng.sample(range(n), 3); put(a, span); put(b, span)
        return lines, span, str(O + 1)
    if cls == "I1_invalid_line_value":
        L = rng.randrange(n); put(L, span)
        return lines, span, sub
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
        plan += [(cls, truth, sub) for sub in SUBVARIANTS[cls]]
    rng.shuffle(plan)
    rows, truth_map = [], {}
    for cls, truth, sub in plan:
        lines, span, line_value = build_item(gen, rng, cls, sub)
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
        try:
            claims, truth = generate(root, seed)
        except Exception as e:  # design v2: harness errors exit 2, never 1
            print("%s: fixture generation failed: %r" % (os.path.basename(__file__), e), file=sys.stderr)
            return 2
        rc, out, err, timed_out = None, "", "", False
        try:
            env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}  # design v2
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root], capture_output=True, env=env,
                               text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            timed_out = True
        observed, dup, flagged = {}, set(), set()
        if not timed_out and rc in (0, 1):
            for line in out.splitlines():
                f = FINDING_RE.match(line)
                if f:
                    flagged.add(f.group(1))
                m = LINE_RE.match(line)
                if m and m.group(1) in truth:
                    if m.group(1) in observed:
                        dup.add(m.group(1))
                    observed[m.group(1)] = m.group(2)
        for cid in dup:  # design v2: an id reported twice is ambiguous and scores "none"
            observed[cid] = "none"
        per_class, misses, matched = {}, [], 0
        for cid, (cls, t) in truth.items():
            obs = observed.get(cid, "none")
            ok = obs == t and ((cid in flagged) == (t == FINDING_TRUTH))
            if obs == t and not ok:
                obs = obs + ("+no-finding" if t == FINDING_TRUTH else "+stray-finding")
            matched += ok
            pc = per_class.setdefault(cls, [0, 0]); pc[1] += 1; pc[0] += ok
            if not ok:
                misses.append({"id": cid, "class": cls, "truth": t, "observed": obs})
        if a.keep:
            try:
                shutil.copytree(root, a.keep)
            except OSError as e:
                print("%s: --keep failed: %r" % (os.path.basename(__file__), e), file=sys.stderr)
                return 2
    finally:
        shutil.rmtree(root, ignore_errors=True)
    holds = matched == TOTAL
    print("LINE_BINDING_MATCH=%d/%d" % (matched, TOTAL))
    for cls, _, _ in CLASS_COUNTS:
        print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r31-c1-receipt/v2",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "total": TOTAL, "matched": matched,
            "label": "LINE_BINDING_MATCH=%d/%d" % (matched, TOTAL), "predicate_holds": holds,
            "per_class": {k: "%d/%d" % tuple(v) for k, v in per_class.items()}, "misses": misses,
        }
        try:
            with open(a.receipt, "w") as f:
                json.dump(receipt, f, indent=1)
                f.write("\n")
        except OSError as e:
            print("%s: --receipt failed: %r" % (os.path.basename(__file__), e), file=sys.stderr)
            return 2
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
