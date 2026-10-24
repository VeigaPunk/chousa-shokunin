#!/usr/bin/env python3
"""Round 32 C2 counter, design v2: exempt-hop audit in `research-gate.sh verify-chain`.

v2 differs from v1 (c2-count.py) in four respects, all forced by the
pre-data control wave (MutC2CounterB: four wrong output controls scored
120/120 under v1; CtlC2WeakReaderB/CtlC2StatusBlindB: fixture inside the
gate's lane root):
1. Findings are counted, not de-duplicated: a resolvable hop matches only
   when exactly one FINDING line names it and that line is
   CHAIN_EXEMPT_RESOLVABLE (v1 used a set, so a duplicate passed).
2. Record checks: the gate exits 1, prints exactly one line starting
   `RESEARCH_GATE: DRIFT`, and no FINDING line names a hop id outside the
   record. If any record check fails, no hop matches (the record's verdict
   is part of the contract: the record drifts).
3. Layout guard: exit 2 if the fixture temp dir lies inside the gate's lane
   root (the parent of the gate's directory), where the out-of-corpus
   sibling would be in corpus.
4. Two negative classes (6 hops each; TOTAL 120 -> 132): E11, the anchor is
   in the source only in upper case; E12, the anchor is in the source only
   with its words separated by two spaces. Both stay exempt (the resolved
   path does not find them). CtlC2WeakReaderB: case-insensitive and
   whitespace-collapsing readers scored 120/120 under v1.

Frozen predicate (claims.md, P2 v2): C2 is met iff, on the landed lane
revision, this counter (c2-count-v2.py) prints EXEMPT_AUDIT_MATCH=132/132
(receipt label predicate_holds=true) on each of two fresh-seed runs, and no
run of this counter on that revision in round 32 prints a lower count.

The counter writes a fresh fixture under a temporary directory: a root with
opaque source files, one directory beside the root (out of corpus), and one
record whose `## Chain` table holds 120 hops in shuffled order with random
hop ids. It runs `bash <gate> verify-chain <record> --root <root>` once,
with every CHOUSA_* variable removed from the gate's environment, and
compares each hop with its hidden truth.

Contract the candidate must meet (claims.md, C2 contract):
- U = {unresolved, blocked-no-fetch, labelled-dead} (statuses that say the
  hop could not be followed). A U hop whose citation the gate would verify
  if the same row said `resolved` (citation parses; source is a declared id
  with a pointer or a local path inside the boundary; the anchor is found as
  the resolved path finds it) prints `observed=resolvable` and exactly one
  `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn|crit surface=chain
  obs=hop=<hop> ...` line, and drifts.
- Every other U hop (no citation, external URL, missing file, undeclared id,
  out-of-corpus path, anchor absent) stays `observed=exempt` and no FINDING
  line names it (obs=hop=<hop>).
- `rejected` and `not-applicable` hops stay `observed=exempt`, unread, with
  no finding naming them, whatever their citation.
- `resolved` hops are unchanged: a resolvable one prints `observed=verified`
  and no finding names it.

A hop counts as matched only when the record checks hold, exactly one CHAIN
line names its id, its `observed=` equals the truth, and the list of FINDING
ids naming it is [CHAIN_EXEMPT_RESOLVABLE] for truth `resolvable` and empty
otherwise.

Exit: 0 iff matched == 132; 1 otherwise; 2 harness error. A gate run that
exits other than 0 or 1, or outlives 600 s, scores every hop "none". No
network (external URLs use the reserved .invalid TLD and are never fetched by
this counter); writes only its temp dir and --receipt.
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

TOTAL = 132
U = ["unresolved", "blocked-no-fetch", "labelled-dead"]
J = ["rejected", "not-applicable"]
KINDS = ["heading", "quote", "line"]
# class, count, truth
CLASS_COUNTS = [
    ("R1_U_fragment_quote", 12, "resolvable"),
    ("R2_U_path_anchor_cols", 12, "resolvable"),
    ("R3_U_declared_id", 12, "resolvable"),
    ("F1_resolved_verifiable", 12, "verified"),
    ("E1_U_anchor_absent", 12, "exempt"),
    ("E2_U_missing_file", 6, "exempt"),
    ("E3_U_external_url", 6, "exempt"),
    ("E4_U_no_citation", 6, "exempt"),
    ("E5_J_resolvable", 12, "exempt"),
    ("E6_U_undeclared_id", 6, "exempt"),
    ("E7_U_out_of_corpus", 6, "exempt"),
    ("E8_U_quote_glued", 6, "exempt"),
    ("E9_U_heading_as_plain_line", 6, "exempt"),
    ("E10_U_line_partial", 6, "exempt"),
    ("E11_U_case_only", 6, "exempt"),
    ("E12_U_whitespace_only", 6, "exempt"),
]
assert sum(c for _, c, _ in CLASS_COUNTS) == TOTAL
FINDING_ID = "CHAIN_EXEMPT_RESOLVABLE"
GATE_TIMEOUT_S = 600
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
LINE_RE = re.compile(r"^CHAIN hop=(\S+) .*?observed=(\S+)")
FIND_RE = re.compile(r"^FINDING (\S+) severity=\S+ surface=\S+ obs=hop=(\S+)(?:\s|$)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
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

    def phrase(self, n=None):
        return " ".join(self.word() for _ in range(n or self.rng.randint(2, 4)))

    def hid(self):
        while True:
            h = "h%08x" % self.rng.getrandbits(32)
            if h not in self.used:
                self.used.add(h)
                return h

    def name(self, prefix):
        while True:
            n = "%s%010x" % (prefix, self.rng.getrandbits(40))
            if n not in self.used:
                self.used.add(n)
                return n


def source_body(gen, kind, anchor, mode):
    """Lines of a source file. mode: present | absent | glued | plain_heading | partial_line | case | spaced."""
    lines = [gen.phrase(5) for _ in range(gen.rng.randint(3, 7))]
    pos = gen.rng.randint(1, len(lines) - 1)
    if mode == "present":
        if kind == "heading":
            ins = "## " + anchor
        elif kind == "quote":
            ins = gen.phrase(2) + " " + anchor + " " + gen.phrase(2)
        else:
            ins = anchor
    elif mode == "absent":
        # near miss: the anchor's first word and a fresh tail, never the anchor itself
        first = anchor.split(" ")[0]
        near = first + " " + gen.phrase(2)
        ins = ("## " + near) if kind == "heading" else near
    elif mode == "glued":
        ins = gen.phrase(2) + " x" + anchor + " " + gen.phrase(2)
    elif mode == "plain_heading":
        ins = anchor
    elif mode == "partial_line":
        ins = anchor + " " + gen.phrase(2)
    elif mode in ("case", "spaced"):
        alt = anchor.upper() if mode == "case" else anchor.replace(" ", "  ")
        if kind == "heading":
            ins = "## " + alt
        elif kind == "quote":
            ins = gen.phrase(2) + " " + alt + " " + gen.phrase(2)
        else:
            ins = alt
    else:
        raise ValueError(mode)
    lines.insert(pos, ins)
    return "\n".join(lines) + "\n"


def generate(tmp, seed):
    rng = random.Random(seed)
    gen = Gen(rng)
    root = os.path.join(tmp, "root")
    outside = os.path.join(tmp, "outside")
    os.makedirs(root)
    os.makedirs(outside)
    hops, truth, sources = [], {}, []

    def put_file(directory, body):
        n = gen.name("f") + ".md"
        with open(os.path.join(directory, n), "w") as f:
            f.write(body)
        return n

    def add(cls, t, status, to, kind="", anchor=""):
        hid = gen.hid()
        frm = "%s:%d" % (gen.name("A"), rng.randint(1, 90))
        hops.append("| %s | %s | %s | %s | %s | %s | %s |" % (hid, frm, to, kind, anchor, status, gen.phrase(3)))
        truth[hid] = (cls, t)

    for cls, count, t in CLASS_COUNTS:
        for i in range(count):
            ustat = U[i % 3]
            kind = KINDS[(i // 3) % 3] if count == 12 else KINDS[i % 3]
            anchor = gen.phrase()
            if cls == "R1_U_fragment_quote":
                n = put_file(root, source_body(gen, "quote", anchor, "present"))
                add(cls, t, ustat, "%s#quote:%s" % (n, anchor))
            elif cls == "R2_U_path_anchor_cols":
                n = put_file(root, source_body(gen, kind, anchor, "present"))
                add(cls, t, ustat, n, kind, anchor)
            elif cls == "R3_U_declared_id":
                n = put_file(root, source_body(gen, kind, anchor, "present"))
                sid = gen.name("S")
                sources.append((sid, n))
                add(cls, t, ustat, sid, kind, anchor)
            elif cls == "F1_resolved_verifiable":
                n = put_file(root, source_body(gen, kind, anchor, "present"))
                if i % 2:
                    sid = gen.name("S")
                    sources.append((sid, n))
                    add(cls, t, "resolved", sid, kind, anchor)
                else:
                    add(cls, t, "resolved", n, kind, anchor)
            elif cls == "E1_U_anchor_absent":
                n = put_file(root, source_body(gen, kind, anchor, "absent"))
                add(cls, t, ustat, n, kind, anchor)
            elif cls == "E2_U_missing_file":
                add(cls, t, ustat, gen.name("f") + ".md", kind, anchor)
            elif cls == "E3_U_external_url":
                add(cls, t, ustat, "https://%s.invalid/%s" % (gen.name("h"), gen.word()), kind, anchor)
            elif cls == "E4_U_no_citation":
                n = put_file(root, source_body(gen, kind, anchor, "present"))
                add(cls, t, ustat, n)
            elif cls == "E5_J_resolvable":
                n = put_file(root, source_body(gen, kind, anchor, "present"))
                add(cls, t, J[i % 2], n, kind, anchor)
            elif cls == "E6_U_undeclared_id":
                add(cls, t, ustat, gen.name("S"), kind, anchor)
            elif cls == "E7_U_out_of_corpus":
                n = put_file(outside, source_body(gen, kind, anchor, "present"))
                add(cls, t, ustat, "../outside/" + n, kind, anchor)
            elif cls == "E8_U_quote_glued":
                n = put_file(root, source_body(gen, "quote", anchor, "glued"))
                add(cls, t, ustat, n, "quote", anchor)
            elif cls == "E9_U_heading_as_plain_line":
                n = put_file(root, source_body(gen, "heading", anchor, "plain_heading"))
                add(cls, t, ustat, n, "heading", anchor)
            elif cls == "E10_U_line_partial":
                n = put_file(root, source_body(gen, "line", anchor, "partial_line"))
                add(cls, t, ustat, n, "line", anchor)
            elif cls == "E11_U_case_only":
                n = put_file(root, source_body(gen, kind, anchor, "case"))
                add(cls, t, ustat, n, kind, anchor)
            elif cls == "E12_U_whitespace_only":
                n = put_file(root, source_body(gen, kind, anchor, "spaced"))
                add(cls, t, ustat, n, kind, anchor)
            else:
                raise ValueError(cls)
    rng.shuffle(hops)
    rng.shuffle(sources)
    rec = ["# %s" % gen.phrase(3), "", "## Sources", "", "| id | pointer | tier |", "|---|---|---|"]
    rec += ["| %s | %s | A |" % (sid, p) for sid, p in sources]
    rec += ["", "## Chain", "", "| hop | from | to | anchor_kind | anchor | status | notes |",
            "|---|---|---|---|---|---|---|"]
    rec += hops
    record = os.path.join(root, gen.name("r") + ".md")
    with open(record, "w") as f:
        f.write("\n".join(rec) + "\n")
    return root, record, truth


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
        print("c2-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C2_TMP") or tempfile.gettempdir()
    try:
        tmp = tempfile.mkdtemp(prefix="chousa-r32-c2-", dir=base)
    except OSError as e:
        print("c2-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    lane_root = os.path.realpath(os.path.dirname(os.path.dirname(os.path.realpath(gate))))
    rtmp = os.path.realpath(tmp)
    if rtmp == lane_root or rtmp.startswith(lane_root.rstrip("/") + "/"):
        print("c2-count: fixture dir %s lies inside the gate's lane root %s" % (rtmp, lane_root), file=sys.stderr)
        shutil.rmtree(tmp, ignore_errors=True)
        return 2
    t0 = time.time()
    try:
        try:
            root, record, truth = generate(tmp, seed)
        except Exception as e:
            print("c2-count: fixture generation failed: %r" % (e,), file=sys.stderr)
            return 2
        rc, out, timed_out = None, "", False
        try:
            env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
            p = subprocess.run(["bash", gate, "verify-chain", record, "--root", root], capture_output=True,
                               env=env, text=True, timeout=GATE_TIMEOUT_S, cwd=root)
            rc, out = p.returncode, p.stdout
        except subprocess.TimeoutExpired:
            timed_out = True
        observed, dup, named = {}, set(), {}
        record_fails = []
        if timed_out or rc not in (0, 1):
            record_fails.append("gate-rc=%s" % ("timeout" if timed_out else rc))
        else:
            if rc != 1:
                record_fails.append("gate-rc=%d" % rc)
            n_drift = 0
            for line in out.splitlines():
                if line.startswith("RESEARCH_GATE: DRIFT"):
                    n_drift += 1
                f = FIND_RE.match(line)
                if f:
                    named.setdefault(f.group(2), []).append(f.group(1))
                m = LINE_RE.match(line)
                if m and m.group(1) in truth:
                    if m.group(1) in observed:
                        dup.add(m.group(1))
                    observed[m.group(1)] = m.group(2)
            if n_drift != 1:
                record_fails.append("drift-summary-lines=%d" % n_drift)
            stray = sorted(h for h in named if h not in truth)
            if stray:
                record_fails.append("stray-finding-hops=%d" % len(stray))
        for hid in dup:
            observed[hid] = "none"
        record_ok = not record_fails
        per_class, misses, matched = {}, [], 0
        for hid, (cls, t) in truth.items():
            obs = observed.get(hid, "none")
            want = [FINDING_ID] if t == "resolvable" else []
            got = sorted(named.get(hid, []))
            ok = record_ok and obs == t and got == want
            if obs == t and got != want:
                obs = obs + "+findings=" + (",".join(got) or "none")
            elif obs == t and not record_ok:
                obs = obs + "+record-fail"
            matched += ok
            pc = per_class.setdefault(cls, [0, 0])
            pc[1] += 1
            pc[0] += ok
            if not ok:
                misses.append({"hop": hid, "class": cls, "truth": t, "observed": obs})
        if a.keep:
            try:
                shutil.copytree(tmp, a.keep)
            except OSError as e:
                print("c2-count: --keep failed: %r" % (e,), file=sys.stderr)
                return 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    holds = matched == TOTAL
    print("EXEMPT_AUDIT_MATCH=%d/%d" % (matched, TOTAL))
    print("  RECORD_CHECKS=%s" % ("ok" if not record_fails else "fail:" + ",".join(record_fails)))
    for cls, _, _ in CLASS_COUNTS:
        print("  %s %d/%d" % (cls, per_class[cls][0], per_class[cls][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r32-c2-receipt/v2", "record_fails": record_fails,
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "gate_rc": rc, "gate_timed_out": timed_out, "total": TOTAL, "matched": matched,
            "label": "EXEMPT_AUDIT_MATCH=%d/%d" % (matched, TOTAL), "predicate_holds": holds,
            "per_class": {k: "%d/%d" % tuple(v) for k, v in per_class.items()}, "misses": misses,
        }
        try:
            with open(a.receipt, "w") as f:
                json.dump(receipt, f, indent=1)
                f.write("\n")
        except OSError as e:
            print("c2-count: --receipt failed: %r" % (e,), file=sys.stderr)
            return 2
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
