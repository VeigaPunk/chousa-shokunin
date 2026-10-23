#!/usr/bin/env python3
"""Round 31 C2 counter: the revision clause of SKILL.md checklist item 1
("Every claim carries a resolvable pointer to the artifact and revision read")
as a runnable check in `research-gate.sh verify-claims`.

Frozen predicate (claims.md, C2): C2 is met iff, on the landed lane revision,
this counter prints REVISION_BINDING_MATCH=120/120 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no run of this
counter on that revision in round 31 prints a lower count.

The counter writes a fresh fixture under a temporary root: opaque source
files and one claims JSONL with 120 claims, every one with expect=supported
(a constant). The hidden truth per claim is supported / unsupported / stale /
invalid. It runs `bash <gate> verify-claims <claims> --root <tmp>` once and
compares each `CLAIM id=<id> ... observed=<obs>` line with the hidden truth.

Contract the candidate must meet (claims.md, C2 contract):
- optional JSON string field "sha256": exactly 64 lowercase hex characters;
  any other value of a present "sha256" -> invalid.
- "sha256" present and not equal to the SHA-256 of the exact bytes of the
  source file -> stale (before and regardless of the span check).
- "sha256" equal -> the existing span behaviour (supported / unsupported).
- "sha256" absent -> unchanged behaviour.

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
    ("R1_match_span_present", 24, "supported"),
    ("R2_match_span_absent", 10, "unsupported"),
    ("S1_one_byte_elsewhere", 16, "stale"),
    ("S2_newline_variant", 12, "stale"),
    ("S3_hash_of_span_only", 10, "stale"),
    ("S4_mismatch_span_absent", 10, "stale"),
    ("S5_hash_of_other_fixture_file", 8, "stale"),
    ("I1_invalid_sha_value", 14, "invalid"),
    ("N1_no_sha", 16, "supported"),
]
assert sum(c for _, c, _ in CLASS_COUNTS) == TOTAL
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
GATE_TIMEOUT_S = 600
LINE_RE = re.compile(r"^CLAIM id=(\S+) .*?observed=(\S+)")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    with open(path, "rb") as f:
        return sha256_bytes(f.read())


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


def make_file(gen, rng, span, present):
    n = rng.randint(10, 24)
    lines = [gen.filler_line() for _ in range(n)]
    L = rng.randrange(n)
    if present:
        lines[L] = gen.word() + " " + span + ". " + gen.word() + "."
    else:
        words = span.split(" ")
        lines[L] = gen.word() + " " + " ".join(words[:-1] + [gen.word()]) + ". " + gen.word() + "."
    crlf = rng.random() < 0.25
    nl = "\r\n" if crlf else "\n"
    data = (nl.join(lines) + nl).encode("utf-8")
    return data, lines, L, nl


def one_byte_elsewhere(data, lines, L, nl):
    # change one ASCII letter on a line other than the span line
    other = [i for i in range(len(lines)) if i != L]
    rng_line = other[len(data) % len(other)]
    text = lines[rng_line]
    pos = next(i for i, ch in enumerate(text) if ch.isalpha())
    ch = text[pos]
    new = text[:pos] + ("q" if ch != "q" else "x") + text[pos + 1:]
    changed = list(lines); changed[rng_line] = new
    return (nl.join(changed) + nl).encode("utf-8")


def generate(root, seed):
    rng = random.Random(seed)
    gen = Gen(rng)
    os.makedirs(os.path.join(root, "src"))
    plan = []
    for cls, count, truth in CLASS_COUNTS:
        plan += [(cls, truth)] * count
    rng.shuffle(plan)
    items = []
    for cls, truth in plan:
        span = gen.span()
        present = cls not in ("R2_match_span_absent", "S4_mismatch_span_absent")
        data, lines, L, nl = make_file(gen, rng, span, present)
        fid = "%016x" % rng.getrandbits(64)
        rel = "src/%s.md" % fid
        with open(os.path.join(root, rel), "wb") as f:
            f.write(data)
        items.append({"cls": cls, "truth": truth, "span": span, "rel": rel, "data": data, "lines": lines,
                      "L": L, "nl": nl})
    rows, truth_map = [], {}
    for idx, it in enumerate(items):
        cls, data = it["cls"], it["data"]
        real = sha256_bytes(data)
        sha = None
        if cls in ("R1_match_span_present", "R2_match_span_absent"):
            sha = real
        elif cls in ("S1_one_byte_elsewhere", "S4_mismatch_span_absent"):
            sha = sha256_bytes(one_byte_elsewhere(data, it["lines"], it["L"], it["nl"]))
        elif cls == "S2_newline_variant":
            variant = rng.choice(["strip_final", "add_final", "swap_eol"])
            if variant == "strip_final":
                v = data[:-len(it["nl"])]
            elif variant == "add_final":
                v = data + it["nl"].encode()
            else:
                other = "\n" if it["nl"] == "\r\n" else "\r\n"
                v = (other.join(it["lines"]) + other).encode("utf-8")
            sha = sha256_bytes(v)
        elif cls == "S3_hash_of_span_only":
            sha = sha256_bytes(it["span"].encode("utf-8"))
        elif cls == "S5_hash_of_other_fixture_file":
            j = (idx + 1 + rng.randrange(len(items) - 1)) % len(items)
            sha = sha256_bytes(items[j]["data"])
        elif cls == "I1_invalid_sha_value":
            kind = rng.choice(["upper", "short", "long", "prefixed", "nonhex", "spaced", "upper", "prefixed"])
            sha = {"upper": real.upper(), "short": real[:63], "long": real + "0",
                   "prefixed": "sha256:" + real, "nonhex": real[:63] + "g", "spaced": " " + real}[kind]
        elif cls == "N1_no_sha":
            sha = None
        cid = "c%010x" % rng.getrandbits(40)
        rec = {"id": cid, "claim": "fixture claim " + cid, "source": it["rel"], "span": it["span"],
               "expect": "supported"}
        if sha is not None:
            rec["sha256"] = sha
        keys = list(rec.keys()); rng.shuffle(keys)
        rows.append(json.dumps({k: rec[k] for k in keys}, ensure_ascii=False))
        truth_map[cid] = (cls, it["truth"])
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
        print("c2-count: gate not found: %s" % gate, file=sys.stderr); return 2
    base = os.environ.get("C2_TMP") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="chousa-r31-c2-", dir=base)
    except OSError as e:
        print("c2-count: temp dir: %s" % e, file=sys.stderr); return 2
    t0 = time.time()
    try:
        claims, truth = generate(root, seed)
        rc, out, timed_out = None, "", False
        try:
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root], capture_output=True,
                               text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out = p.returncode, p.stdout
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
    print("REVISION_BINDING_MATCH=%d/%d" % (matched, TOTAL))
    for cls, _, _ in CLASS_COUNTS:
        print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r31-c2-receipt/v1",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "total": TOTAL, "matched": matched,
            "label": "REVISION_BINDING_MATCH=%d/%d" % (matched, TOTAL), "predicate_holds": holds,
            "per_class": {k: "%d/%d" % tuple(v) for k, v in per_class.items()}, "misses": misses,
        }
        with open(a.receipt, "w") as f:
            json.dump(receipt, f, indent=1)
            f.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
