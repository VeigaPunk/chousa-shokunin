#!/usr/bin/env python3
r"""Round 34 repair E2 counter, design v3 (derived from the round 33 counter
corpus/evidence/round33/c1-count-v2.py, kept frozen and unedited there):
`verify-claims` reads a claim's fields from its top-level JSON object.

Counted rule (unchanged from round 33): the gate must print one CLAIM line per
record whose observed= equals the hidden truth, with the two finding sets
matching the truth; TOPLEVEL_FIELD_MATCH=156/156 on a fresh seed.

v3 changes against v2, made before any candidate was scored, per the routed
defect E2 (corpus/lessons/round-33-verifier-spotcheck.md:163-166, QUALITY 40):
- the six FIXED confuser literals are replaced by confuser string content
  GENERATED PER SEED. Each generated confuser is a random string carrying the
  structural characters { } [ ] : , a quote (JSON-escaped), a backslash
  (JSON-escaped, and for one slot the escaped backslash sits immediately
  before the closing quote), a \u escape (a non-ASCII character, JSON-encoded
  as \uXXXX) and text that looks like a member ("line":"7"). The content is
  used in the flat position (class S1_flat_confusers) and in the nested
  position (class S2_nested_confusers). Because no confuser literal is fixed,
  a gate cannot pre-mask the fixture by literal: the round-33 shortcut
  (wave-33 w2/L1ShortcutMask/mask-gate.sh) masks exactly the six old literals.
- NOTHING ELSE changes: the same 15 classes, the same sub-variant counts, the
  same TOTAL 156, the same per-record match rule, the same label
  TOPLEVEL_FIELD_MATCH, the same exit convention.
- the receipt schema is bumped to chousa-r34-c1-receipt/v3.

v2 changes against v1 (c1-count.py, kept frozen and unedited), made before any
candidate was scored, after the pre-data critic CriticAxisFit33 (F1, F2):
- the duplicate class covers six read keys: line, sha256, source, span, expect
  (identical and differing values) and id (identical values only, so the CLAIM
  line identity stays decidable); 24 records instead of 12. TOTAL 144 -> 156.
- the gate run must exit 1 and print a `RESEARCH_GATE: DRIFT` line (every
  fixture holds drifting records); any other exit or no DRIFT line scores every
  record "none".

Counted contract (claims.md, C1 contract v2):
- A claim record is one JSON object per line. The fields the gate reads -- "id",
  "source", "span", "expect", "marker", "line", "sha256" -- are members of that
  top-level object only. A member of the same name inside a nested object or
  array value is not the record's field and changes nothing.
- A duplicated top-level "line", "sha256", "source", "span", "expect" (identical
  or differing values) or "id" (identical values) makes the record invalid, and
  the CLAIM line carries the record's id.
- Characters inside JSON string values ({ } [ ] : , escaped quotes, a trailing
  escaped backslash, text that looks like a member) are string content, never
  structure.

Fixture: a fresh temp root with opaque source files and one claims JSONL of 156
records in 15 classes with fixed sub-variant counts (a gate that mishandles one
sub-variant misses it on every seed). Every record carries expect="supported"
at top level, so the label carries no truth; the hidden truth per record is one
of supported / mislocated / stale / unsupported / invalid and is never written
next to the claims. Nested container member names are random words; ids and
file names are random hex; member order is drawn per record; source files are
written in shuffled order. The counter runs
`bash <gate> verify-claims <claims> --root <tmp>` once (CHOUSA_* variables
removed from the environment).

Per-record match: the gate prints exactly one `CLAIM id=<top-level id> ...`
line whose observed= equals the truth, AND a
`FINDING CLAIM_LINE_MISMATCH ... obs=id=<id>` exists iff the truth is
mislocated, AND a `FINDING CLAIM_SOURCE_REVISION_MISMATCH ... obs=id=<id>`
exists iff the truth is stale. An id printed on two CLAIM lines scores "none".

Exit: 0 iff matched == TOTAL; 1 otherwise; 2 harness error. A gate run that
exits other than 1, prints no `RESEARCH_GATE: DRIFT` line, or outlives 600 s,
scores every record "none".
No network; writes only its temp dir, --keep and --receipt.
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

LABEL = "TOPLEVEL_FIELD_MATCH"
GATE_TIMEOUT_S = 600
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
READ_KEYS = {"id", "source", "span", "expect", "marker", "line", "sha256", "marker_default", "claim"}
KINDS = ["obj", "arr", "deep"]
POS = ["before", "after"]
# String contents that look like structure (C1 contract item 3). v3 (repair E2):
# the six confusers are GENERATED PER SEED, so no fixed literal exists to mask
# (the round-33 shortcut masks exactly the six old literals). Every generated
# confuser carries the structural characters { } [ ] : , , a quote (JSON-
# escaped), a backslash (JSON-escaped; for one slot per seed the escaped
# backslash sits immediately before the closing quote), a \u escape (a
# non-ASCII character, JSON-encoded as \uXXXX by JC) and text that looks like
# a member ("line":"7", with a per-seed key and digits).
CONFUSER_NONASCII = "éüñç€ΩλЖ日"


def gen_confusers(rng):
    """Six confuser strings for one seed. Returns a list of Python strings;
    JC() encodes each as a JSON string body.

    Every generated confuser carries: the structural characters { } [ ] : , ;
    a quote (JSON-escaped); a backslash (JSON-escaped) and, for one slot per
    seed, that escaped backslash immediately before the closing quote; a
    non-ASCII character, which JC() writes as a \\uXXXX escape; and text that
    looks like a member ("line":"<digits>", digits per seed).
    """
    out = []
    tail_slot = rng.randrange(6)  # the slot whose escaped backslash precedes the closing quote
    for i in range(6):
        w = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(3, 9)))
        # every confuser carries all six structural characters { } [ ] : , ,
        # in a per-seed random order, plus extra random repetitions
        chars = list("{}[]:,")
        rng.shuffle(chars)
        struct = "".join(chars) + "".join(rng.choice("{}[]:,") for _ in range(rng.randint(1, 4)))
        # the member look-alike: key "line", per-seed digits; slot 0 carries the
        # literal digits "7" so the ("line":"7") shape is always present
        mnum = "7" if i == 0 else "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 4)))
        member = '"line":"%s"' % mnum
        uni = rng.choice(CONFUSER_NONASCII)
        s = "%s %s %s \" %s \\ %s" % (w, struct, member, w, uni)
        if i == tail_slot:
            s += " \\"
        out.append(s)
    return out

CLASS_COUNTS = [  # (class, sub-variants, truth)
    ("N1_nested_line_decoy", [(p, k) for p in POS for k in KINDS] * 2, "supported"),
    ("N2_nested_line_only", [(k, v) for k in KINDS for v in ("string", "number")] * 2, "supported"),
    ("N3_top_line_wrong_nested_right", [(p, k) for p in POS for k in KINDS] * 2, "mislocated"),
    ("N4_nested_sha_decoy", [(p, v, k) for p in POS for v in ("hex", "malformed") for k in KINDS], "supported"),
    ("N5_nested_sha_only", [(k, v) for k in KINDS for v in ("hex", "malformed")] * 2, "supported"),
    ("N6_top_sha_stale_nested_right", [(p, k) for p in POS for k in KINDS] * 2, "stale"),
    ("N7_nested_source_decoy_sup", [(p, k) for p in POS for k in KINDS], "supported"),
    ("N8_nested_source_decoy_uns", [(p, k) for p in POS for k in KINDS], "unsupported"),
    ("N9_nested_id_decoy", [(p, k) for p in POS for k in KINDS], "supported"),
    ("N10_nested_span_decoy", [(p, k) for p in POS for k in KINDS], "supported"),
    ("N11_nested_marker_expect_decoy", [(k, v) for k in KINDS for v in ("marker", "expect")], "supported"),
    ("D1_duplicate_top_level", ([(key, v) for key in ("line", "sha256", "source", "span", "expect")
                                 for v in ("same", "diff")] + [("id", "same")] * 2) * 2, "invalid"),
    ("S1_flat_confusers", [(c, t) for c in range(6) for t in ("right", "wrong")], None),
    ("S2_nested_confusers", [(c,) for c in range(6)], "supported"),
    ("F1_flat_plain", [("supported",), ("mislocated",), ("stale",), ("unsupported",)] * 3, None),
]
TOTAL = sum(len(s) for _, s, _ in CLASS_COUNTS)
assert TOTAL == 156, TOTAL

LINE_RE = re.compile(r"^CLAIM id=(\S+) .*?observed=(\S+)")
FIND_LINE_RE = re.compile(r"^FINDING CLAIM_LINE_MISMATCH severity=(?:warn|crit) surface=claims obs=id=(\S+)(?:\s|$)")
FIND_REV_RE = re.compile(r"^FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=(?:warn|crit) surface=claims obs=id=(\S+)(?:\s|$)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class Gen:
    def __init__(self, rng):
        self.rng = rng
        self.used = set(READ_KEYS)
        # v3: the six confuser strings are drawn per seed, never fixed.
        self.confusers = gen_confusers(rng)

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


def J(v):
    return json.dumps(v, ensure_ascii=False)


def JC(v):
    """JSON string body for a confuser: ensure_ascii=True so a non-ASCII
    character is written as a \\uXXXX escape (v3)."""
    return json.dumps(v, ensure_ascii=True)


def container(gen, rng, kind, inner):
    """inner: list of (key, json_text) members placed in a nested object."""
    members = [(gen.word(), J(gen.word() + " " + gen.word()))] + list(inner)
    rng.shuffle(members)
    obj = "{" + ", ".join("%s: %s" % (J(k), v) for k, v in members) + "}"
    if kind == "obj":
        return obj
    if kind == "arr":
        return "[" + J(gen.word()) + ", " + obj + ", " + str(rng.randint(1, 99)) + "]"
    return "{" + J(gen.word()) + ": {" + J(gen.word()) + ": [" + obj + "]}}"


class Item:
    def __init__(self, gen, rng):
        self.gen, self.rng = gen, rng
        self.files = []  # (rel, text)
        self.members = []  # top-level (key, json_text) in final order

    def source(self, with_span=None, span_line=None):
        n = self.rng.randint(14, 30)
        lines = [self.gen.filler_line() for _ in range(n)]
        L = None
        if with_span is not None:
            L = span_line if span_line is not None else self.rng.randrange(1, n - 1)
            lines[L] = self.gen.word() + " " + with_span + ". " + self.gen.word() + "."
        text = "\n".join(lines) + "\n"
        rel = "src/%016x.md" % self.rng.getrandbits(64)
        self.files.append((rel, text))
        return rel, text, n, L

    def other_line(self, n, L):
        return str(self.rng.choice([i for i in range(n) if i != L]) + 1)


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build(gen, rng, cls, sub, cid):
    """Return (Item, truth) with item.members set (top-level order final)."""
    it = Item(gen, rng)
    span = gen.span()
    rel, text, n, L = it.source(with_span=span)
    base = [("id", J(cid)), ("claim", J("fixture claim " + gen.word())), ("source", J(rel)),
            ("span", J(span)), ("expect", J("supported"))]

    def place(members, target, decoy, pos):
        """Insert target member and decoy container (pos before/after target) at a random slot."""
        rest = [m for m in members]
        rng.shuffle(rest)
        pair = ([decoy, target] if pos == "before" else [target, decoy]) if target else [decoy]
        k = rng.randint(0, len(rest))
        return rest[:k] + pair + rest[k:]

    def without(key):
        return [m for m in base if m[0] != key]

    def deco(kind, key, val):
        return (gen.word(), container(gen, rng, kind, [(key, val)]))

    truth = dict(CLASS_COUNTS_T)[cls]
    if cls == "N1_nested_line_decoy":
        pos, kind = sub
        it.members = place(base, ("line", J(str(L + 1))), deco(kind, "line", J(it.other_line(n, L))), pos)
    elif cls == "N2_nested_line_only":
        kind, v = sub
        val = J(it.other_line(n, L)) if v == "string" else str(rng.randint(2, 9))
        it.members = place(base, None, deco(kind, "line", val), None)
    elif cls == "N3_top_line_wrong_nested_right":
        pos, kind = sub
        it.members = place(base, ("line", J(it.other_line(n, L))), deco(kind, "line", J(str(L + 1))), pos)
    elif cls == "N4_nested_sha_decoy":
        pos, v, kind = sub
        bad = sha_text(gen.filler_line()) if v == "hex" else "zz" + gen.word()
        it.members = place(base, ("sha256", J(sha_text(text))), deco(kind, "sha256", J(bad)), pos)
    elif cls == "N5_nested_sha_only":
        kind, v = sub
        bad = sha_text(gen.filler_line()) if v == "hex" else "zz" + gen.word()
        it.members = place(base, None, deco(kind, "sha256", J(bad)), None)
    elif cls == "N6_top_sha_stale_nested_right":
        pos, kind = sub
        it.members = place(base, ("sha256", J(sha_text(gen.filler_line()))), deco(kind, "sha256", J(sha_text(text))), pos)
    elif cls == "N7_nested_source_decoy_sup":
        pos, kind = sub  # top-level source holds the span; nested names a file without it
        other, _, _, _ = it.source(with_span=None)
        it.members = place(without("source"), ("source", J(rel)), deco(kind, "source", J(other)), pos)
    elif cls == "N8_nested_source_decoy_uns":
        pos, kind = sub  # top-level source lacks the span; nested names the file that has it
        other, _, _, _ = it.source(with_span=None)
        it.members = place(without("source"), ("source", J(other)), deco(kind, "source", J(rel)), pos)
    elif cls == "N9_nested_id_decoy":
        pos, kind = sub
        fake = "c%010x" % rng.getrandbits(40)
        it.members = place(without("id"), ("id", J(cid)), deco(kind, "id", J(fake)), pos)
    elif cls == "N10_nested_span_decoy":
        pos, kind = sub
        it.members = place(without("span"), ("span", J(span)), deco(kind, "span", J(gen.span())), pos)
    elif cls == "N11_nested_marker_expect_decoy":
        kind, v = sub
        if v == "marker":
            it.members = place(base, None, deco(kind, "marker", J(gen.word())), None)
        else:  # nested expect=contradicted before the top-level expect
            it.members = place(without("expect"), ("expect", J("supported")),
                               deco(kind, "expect", J("contradicted")), "before")
    elif cls == "D1_duplicate_top_level":
        key, v = sub
        rest = list(base)
        if key == "line":
            a = J(str(L + 1)); b = a if v == "same" else J(it.other_line(n, L))
        elif key == "sha256":
            a = J(sha_text(text)); b = a if v == "same" else J(sha_text(gen.filler_line()))
        elif key == "source":
            other, _, _, _ = it.source(with_span=None)
            a = J(rel); b = a if v == "same" else J(other)
        elif key == "span":
            a = J(span); b = a if v == "same" else J(gen.span())
        elif key == "expect":
            a = J("supported"); b = a if v == "same" else J("contradicted")
        else:  # id: identical values only
            a = b = J(cid)
        if key != "line" and key != "sha256":
            rest = without(key)
        extra = [(key, a), (key, b)]
        if rng.random() < 0.5:
            extra.reverse()
        rng.shuffle(rest)
        i = rng.randint(0, len(rest)); rest.insert(i, extra[0])
        j = rng.randint(i + 1, len(rest)); rest.insert(j, extra[1])
        it.members = rest
    elif cls == "S1_flat_confusers":
        c, t = sub  # confuser string member placed before the top-level "line"
        conf = (gen.word(), JC(gen.confusers[c]))
        line_val = J(str(L + 1)) if t == "right" else J(it.other_line(n, L))
        rest = list(base); rng.shuffle(rest)
        k = rng.randint(0, len(rest))
        it.members = rest[:k] + [conf, ("line", line_val)] + rest[k:]
        truth = "supported" if t == "right" else "mislocated"
    elif cls == "S2_nested_confusers":
        (c,) = sub  # container: confuser string, then a wrong nested "line"; top-level right "line" after it
        inner = "{" + J(gen.word()) + ": " + JC(gen.confusers[c]) + ", " + J("line") + ": " + J(it.other_line(n, L)) + "}"
        cont = inner if c % 2 == 0 else "[" + JC(gen.confusers[(c + 1) % 6]) + ", " + inner + "]"
        rest = list(base); rng.shuffle(rest)
        k = rng.randint(0, len(rest))
        it.members = rest[:k] + [(gen.word(), cont), ("line", J(str(L + 1)))] + rest[k:]
    elif cls == "F1_flat_plain":
        (t,) = sub
        truth = t
        if t == "supported":
            extra = ("line", J(str(L + 1)))
        elif t == "mislocated":
            extra = ("line", J(it.other_line(n, L)))
        elif t == "stale":
            extra = ("sha256", J(sha_text(gen.filler_line())))
        else:  # unsupported: span text absent from its source
            extra = None
            span2 = gen.span()
            base = [("span", J(span2)) if m[0] == "span" else m for m in base]
        rest = list(base) + ([extra] if extra else [])
        rng.shuffle(rest)
        it.members = rest
    else:
        raise ValueError(cls)
    return it, truth


CLASS_COUNTS_T = [(c, t) for c, _, t in CLASS_COUNTS]


def generate(root, seed):
    rng = random.Random(seed)
    gen = Gen(rng)
    os.makedirs(os.path.join(root, "src"))
    plan = []
    for cls, subs, _ in CLASS_COUNTS:
        plan += [(cls, s) for s in subs]
    rng.shuffle(plan)
    rows, truth_map, files = [], {}, []
    for cls, sub in plan:
        cid = "c%010x" % rng.getrandbits(40)
        while cid in truth_map:
            cid = "c%010x" % rng.getrandbits(40)
        it, truth = build(gen, rng, cls, sub, cid)
        files += it.files
        rows.append("{" + ", ".join("%s: %s" % (J(k), v) for k, v in it.members) + "}")
        truth_map[cid] = (cls, truth)
    rng.shuffle(files)  # creation order carries no class
    for rel, text in files:
        with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows) + "\n")
    for row in rows:  # every record is valid JSON with one top-level object
        assert isinstance(json.loads(row), dict)
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
        print("c1-count: gate not found: %s" % gate, file=sys.stderr); return 2
    base = os.environ.get("C1_TMP") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="chousa-r33-c1-", dir=base)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr); return 2
    t0 = time.time()
    try:
        try:
            claims, truth = generate(root, seed)
        except Exception as e:
            print("c1-count: fixture generation failed: %r" % (e,), file=sys.stderr)
            return 2
        rc, out, timed_out = None, "", False
        try:
            env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
            p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root], capture_output=True, env=env,
                               text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out = p.returncode, p.stdout
        except subprocess.TimeoutExpired:
            timed_out = True
        observed, dup, f_line, f_rev = {}, set(), set(), set()
        drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
        if not timed_out and rc == 1 and drift:  # v2: the fixture always drifts
            for line in out.splitlines():
                m = FIND_LINE_RE.match(line)
                if m:
                    f_line.add(m.group(1))
                m = FIND_REV_RE.match(line)
                if m:
                    f_rev.add(m.group(1))
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
            ok = (obs == t and ((cid in f_line) == (t == "mislocated"))
                  and ((cid in f_rev) == (t == "stale")))
            if obs == t and not ok:
                obs += "+finding-set"
            matched += ok
            pc = per_class.setdefault(cls, [0, 0]); pc[1] += 1; pc[0] += ok
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
            "schema": "chousa-r34-c1-receipt/v3",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "total": TOTAL, "matched": matched,
            "label": label, "predicate_holds": holds,
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
