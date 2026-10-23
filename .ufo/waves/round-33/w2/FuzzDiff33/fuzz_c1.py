#!/usr/bin/env python3
"""Round 33 W2 (FuzzDiff33): differential fuzz of verify-claims' top-level field reader.

Target: the landed gate's C1 contract (corpus/evidence/round33/claims.md, design v2):
  - id/source/span/expect/marker/line/sha256 are read from the TOP-LEVEL JSON object only;
    a member of the same name inside a nested object or array changes nothing;
  - a read field repeated among the top-level members makes the record invalid
    (CLAIM_RECORD_INVALID), whatever the values;
  - string content is never structure.

This harness generates random VALID claim records (one JSON object per line): nested
objects/arrays up to depth 4 holding random subsets of the seven read keys, random
member order, random whitespace, occasional top-level duplicates.  It computes the
contract verdict with its OWN python reference (json.loads + object_pairs_hook;
duplicate read key -> invalid; reads no gate code) and compares it with the landed
gate's observed verdict per id.

Mismatches are delta-minimized (drop top-level members / collapse nested values /
collapse whitespace) and re-observed on the gate.
"""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time

READ7 = ["id", "source", "span", "expect", "marker", "line", "sha256"]
READ8 = READ7 + ["marker_default"]
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
CONF = [
    "open { brace and [ bracket",
    "close } brace ] bracket",
    'a quote " then } more',
    "ends with a backslash \\",
    'fake "line": "3", "sha256": "x"',
    '{"line": "2"} ] } , :',
    'escaped quote \\" then } brace',
    'text with \\u007b and \\u005b escapes',
    'trailing \\\\ two backslashes then }',
    "line\nbreak text",
]
MISS = object()
CLAIM_RE = re.compile(r"^CLAIM id=(\S+) expected=(\S+) observed=(\S+)")
INV_RE = re.compile(r"^FINDING CLAIM_RECORD_INVALID .*line=(\d+)(?: |$)")


class Pairs(list):
    """json object from object_pairs_hook (arrays stay plain list)."""


class Obj:
    __slots__ = ("pairs",)

    def __init__(self, pairs=()):
        self.pairs = list(pairs)


def J(s):
    """Value passthrough: ser() JSON-encodes plain python values."""
    return s


def wsp(rng):
    r = rng.random()
    if r < 0.60:
        return ""
    if r < 0.85:
        return " "
    if r < 0.95:
        return "  "
    return "\t"


def ser(v, rng, bare=False):
    if isinstance(v, Obj):
        if not v.pairs:
            return "{}" if bare else "{" + (wsp(rng) if rng.random() < 0.2 else "") + "}"
        parts = [json.dumps(k, ensure_ascii=False) + ("" if bare else wsp(rng)) + ":" + ("" if bare else wsp(rng)) + ser(x, rng, bare)
                 for k, x in v.pairs]
        sep = "," if bare else "," + wsp(rng)
        head = "" if bare else wsp(rng)
        tail = "" if bare else wsp(rng)
        return "{" + head + sep.join(parts) + tail + "}"
    if isinstance(v, list):
        if not v:
            return "[]" if bare else "[" + (wsp(rng) if rng.random() < 0.2 else "") + "]"
        sep = "," if bare else "," + wsp(rng)
        head = "" if bare else wsp(rng)
        tail = "" if bare else wsp(rng)
        return "[" + head + sep.join(ser(x, rng, bare) for x in v) + tail + "]"
    return json.dumps(v, ensure_ascii=False)


class Gen:
    def __init__(self, rng):
        self.rng = rng
        self.used = set(READ8) | {"claim", "meta", "note", "extra"}

    def word(self):
        while True:
            w = "".join(self.rng.choice(SYL) for _ in range(self.rng.randint(2, 4)))
            if w not in self.used:
                self.used.add(w)
                return w

    def confuser(self):
        return self.rng.choice(CONF)

    def scalar(self):
        r = self.rng.random()
        if r < 0.45:
            return self.word()
        if r < 0.6:
            return self.rng.randint(0, 99)
        if r < 0.7:
            return self.rng.choice([True, False])
        if r < 0.78:
            return None
        return self.confuser()

    def readval(self, key):
        r = self.rng.random()
        if key == "line":
            return self.rng.randint(1, 9) if r < 0.15 else J(str(self.rng.randint(1, 9)))
        if key == "sha256":
            if r < 0.15:
                return self.rng.randint(1, 9)
            if r < 0.3:
                return J("zz" + self.word())
            return J("%064x" % self.rng.getrandbits(256))
        if key == "id":
            return J("c%010x" % self.rng.getrandbits(40))
        if key == "source":
            return J("src/%016x.md" % self.rng.getrandbits(64))
        if key == "expect":
            return J(self.rng.choice(["supported", "unsupported", "contradicted"]))
        return J(self.word())


def decoy(rng, gen, keys, budget):
    """Nested value holding a random subset of read keys, at most `budget` levels deep."""
    members = [(gen.word(), gen.scalar()) for _ in range(rng.randint(0, 2))]
    for k in keys:
        if rng.random() < 0.55:
            members.append((k, gen.readval(k)))
    rng.shuffle(members)
    node = Obj(members) if rng.random() < 0.8 else [gen.scalar(), Obj(members)]
    lvl = 1
    while lvl < budget and rng.random() < 0.6:
        style = rng.choice(["obj", "arr", "objstr", "arrstr"])
        if style == "obj":
            node = Obj([(gen.word(), node)])
        elif style == "arr":
            node = [node]
        elif style == "objstr":
            node = Obj([(gen.word(), gen.confuser()), (gen.word(), node)])
        else:
            node = [gen.confuser(), node]
        lvl += 1
    return node


def make_sources(rng, gen, root):
    os.makedirs(os.path.join(root, "src"))
    files, pool = [], []
    for _ in range(6):
        n = rng.randint(12, 20)
        lines = [" ".join(gen.word() for _ in range(rng.randint(5, 9))) + "." for _ in range(n)]
        spans = []
        for L in rng.sample(range(n), rng.randint(1, 2)):
            span = gen.word()
            while span in "\n".join(lines):
                span = gen.word()
            lines[L] = gen.word() + " " + span + ". " + gen.word() + "."
            spans.append((span, L))
        text = "\n".join(lines) + "\n"
        rel = "src/%016x.md" % rng.getrandbits(64)
        with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        files.append((rel, text))
        for span, L in spans:
            assert text.count(span) == 1, (span, text.count(span))
            pool.append((rel, text, span, L))
    return files, pool


def build_record(rng, gen, pool, cid):
    rel, text, span, L = rng.choice(pool)
    nlines = text.count("\n")
    sha_right = hashlib.sha256(text.encode()).hexdigest()
    kind = rng.choice(["supported"] * 5 + ["mislocated"] * 4 + ["stale"] * 3
                      + ["unsupported"] * 2 + ["linebad"] * 1)
    top = [("id", J(cid)), ("claim", J("fixture " + gen.word()))]
    top.append(("source", J(rel)))
    if kind == "unsupported":
        sp = gen.word()
        while sp in text:
            sp = gen.word()
        top.append(("span", J(sp)))
    else:
        top.append(("span", J(span)))
    top.append(("expect", J("supported")))
    wrong = L + 1 + rng.randrange(max(1, nlines - 1))
    while wrong == L:
        wrong = L + 1 + rng.randrange(max(1, nlines - 1))
    if kind == "supported":
        r = rng.random()
        if r < 0.30:
            top.append(("line", J(str(L + 1))))
        elif r < 0.40:
            top.append(("line", J("%d-%d" % (L + 1, L + 1))))
        if rng.random() < 0.25:
            top.append(("sha256", J(sha_right)))
    elif kind == "mislocated":
        if rng.random() < 0.15:
            top.append(("line", J("%d-%d" % (L + 1, L + 2))))
        else:
            top.append(("line", J(str(wrong + 1))))
        if rng.random() < 0.3:
            top.append(("sha256", J(sha_right)))
    elif kind == "stale":
        if rng.random() < 0.5:
            top.append(("sha256", J("%064x" % rng.getrandbits(256))))
        else:
            top.append(("sha256", J(hashlib.sha256(gen.word().encode()).hexdigest())))
        if rng.random() < 0.4:
            top.append(("line", J(str(L + 1))))
    elif kind == "linebad":
        top.append(("line", rng.choice([J("0"), J("01"), J("3-2"), J("3-"), J("abc"), J("%d-%d" % (L + 2, L + 1)),
                                        3, None, J("")])))
    # nested decoys (no top-level read-key names)
    for _ in range(rng.randint(0, 3)):
        keys = [k for k in READ7 if rng.random() < 0.5]
        top.append((gen.word(), decoy(rng, gen, keys, rng.randint(1, 3))))
    # string confusers as unknown top-level members
    if rng.random() < 0.3:
        top.append((gen.word(), gen.confuser()))
    # a read key whose TOP-LEVEL value is a nested container that holds the same
    # key: the reader must fail closed (non-string), never descend into it
    if rng.random() < 0.10:
        key = rng.choice(["line", "sha256", "span", "source", "id", "expect"])
        right = {"line": str(L + 1), "sha256": sha_right, "span": span,
                 "source": rel, "id": cid, "expect": "supported"}[key]
        style = rng.choice(["obj", "arr", "deep"])
        if style == "obj":
            val = Obj([(key, right)])
        elif style == "arr":
            val = [Obj([(key, right)]), gen.scalar()]
        else:
            val = Obj([(gen.word(), Obj([(gen.word(), [Obj([(key, right)])])]))])
        top = [(k, val if k == key else v) for k, v in top]
    # near-miss spellings of read keys (not read keys; must be ignored)
    if rng.random() < 0.10:
        for nm in rng.sample(["line ", " line", "LINE", "Line", "linex", "sha256 "], rng.randint(1, 2)):
            top.append((nm, Obj([("line", str(wrong + 1)), ("sha256", "zz")]) if rng.random() < 0.5
                        else str(wrong + 1)))
    # empty member name (valid JSON; bash cannot subscript ""), nested or flat
    if rng.random() < 0.10:
        top.append(("", Obj([("line", str(wrong + 1))]) if rng.random() < 0.5 else gen.confuser()))
    # occasional top-level duplicate of a read key
    if rng.random() < 0.25:
        key = rng.choice(["line", "sha256", "source", "span", "expect", "id", "marker"])
        have = [(i, v) for i, (k, v) in enumerate(top) if k == key]
        if have:
            i, val = rng.choice(have)
            if rng.random() < 0.5:
                if key == "line":
                    val = J(str(wrong + 1)) if rng.random() < 0.8 else rng.randint(1, 9)
                elif key == "sha256":
                    val = J("%064x" % rng.getrandbits(256)) if rng.random() < 0.8 else 7
                elif key == "source":
                    val = J(rng.choice(pool)[0])
                elif key == "span":
                    val = J(gen.word())
                elif key == "expect":
                    val = J("contradicted")
            elif key == "id":
                val = J(cid) if rng.random() < 0.5 else J("c%010x" % rng.getrandbits(40))
            elif key == "line":
                val = Obj([("line", str(L + 1))]) if rng.random() < 0.2 else J(gen.word())
            elif key == "sha256":
                val = [J(sha_right)] if rng.random() < 0.2 else J("zz")
            else:
                val = J(gen.word())
        else:
            if key == "line":
                val = J(str(L + 1))
            elif key == "sha256":
                val = J(sha_right)
            elif key == "marker":
                # duplicated marker (invalid by the implementation, not counted by the
                # counter): insert the same key twice
                pos = rng.randint(0, len(top))
                top.insert(pos, (key, J(gen.word())))
                top.insert(rng.randint(0, len(top)), (key, J(gen.word())))
                rng.shuffle(top)
                return Obj(top), kind
            elif key == "id":
                val = J(cid)
            elif key == "source":
                val = J(rel)
            elif key == "span":
                val = J(span)
            else:
                val = J("supported")
        pos = rng.randint(0, len(top))
        top.insert(pos, (key, val))
    rng.shuffle(top)
    return Obj(top), kind


# ---------------- independent contract reference ----------------

def word_char(c):
    return c.isalnum() or ord(c) > 127


def occurrences(text, span):
    out = []
    i = text.find(span)
    while i >= 0:
        left_ok = i == 0 or not word_char(text[i - 1])
        j = i + len(span)
        right_ok = j == len(text) or not word_char(text[j])
        if left_ok and right_ok:
            out.append(i)
        i = text.find(span, i + 1)
    return out


def ref_verdict(line, root):
    try:
        obj = json.loads(line, object_pairs_hook=Pairs)
    except Exception:
        return "parse_error"
    if not isinstance(obj, Pairs):
        return "not_object"
    cnt = {}
    for k, _ in obj:
        cnt[k] = cnt.get(k, 0) + 1
    if any(cnt.get(k, 0) > 1 for k in READ8):
        return "invalid"
    d = {}
    for k, v in obj:
        d.setdefault(k, v)

    def s(k):
        v = d.get(k, MISS)
        return v if isinstance(v, str) else None

    idv, src, span, exp = s("id"), s("source"), s("span"), s("expect")
    if not idv or not src or not span or not exp:
        return "invalid"
    if exp not in ("supported", "contradicted", "unsupported"):
        return "invalid"
    if "sha256" in d:
        v = d["sha256"]
        if not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v):
            return "invalid"
    if "marker" in d and exp != "contradicted" and isinstance(d["marker"], str) and d["marker"]:
        return "invalid"
    line_range = None
    if "line" in d:
        v = d["line"]
        if not isinstance(v, str) or not v:
            return "invalid"
        m = re.fullmatch(r"([1-9][0-9]*)", v)
        if m:
            line_range = (int(m.group(1)), int(m.group(1)))
        else:
            m = re.fullmatch(r"([1-9][0-9]*)-([1-9][0-9]*)", v)
            if not m or int(m.group(2)) <= int(m.group(1)):
                return "invalid"
            line_range = (int(m.group(1)), int(m.group(2)))
    path = os.path.join(root, src)
    if not os.path.isfile(path):
        return "refused"
    if "sha256" in d:
        with open(path, "rb") as f:
            actual = hashlib.sha256(f.read()).hexdigest()
        if actual != d["sha256"]:
            return "stale"
    with open(path, encoding="utf-8") as f:
        text = f.read()
    idxs = occurrences(text, span)
    if not idxs:
        return "unsupported"
    if line_range is not None:
        starts = [text.count("\n", 0, i) + 1 for i in idxs]
        ends = [text.count("\n", 0, i + len(span)) + 1 for i in idxs]
        if any(a == line_range[0] and b == line_range[1] for a, b in zip(starts, ends)):
            return "supported"
        return "mislocated"
    return "supported"


# ---------------- gate observation ----------------

def run_gate(gate, root, lines, env, tag):
    path = os.path.join(root, "claims_%s.jsonl" % tag)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    p = subprocess.run(["bash", gate, "verify-claims", path, "--root", root],
                       capture_output=True, text=True, env=env, timeout=300, cwd=root)
    obs, inv, nclaim = {}, set(), {}
    for ln in p.stdout.splitlines():
        m = CLAIM_RE.match(ln)
        if m:
            wid = m.group(1)
            nclaim[wid] = nclaim.get(wid, 0) + 1
            obs[wid] = m.group(3)
        m = INV_RE.match(ln)
        if m:
            inv.add(int(m.group(1)))
    return p.returncode, obs, nclaim, inv, p.stdout, p.stderr


def observe_one(ctx, line):
    """Observed verdict the gate assigns to a single-record file; cached by text."""
    if line in ctx["cache"]:
        return ctx["cache"][line]
    rc, obs, nclaim, inv, out, err = run_gate(ctx["gate"], ctx["root"], [line], ctx["env"], "mini")
    if not obs and not inv:
        got = "none"
    elif 1 in inv and not obs:
        got = "invalid"
    elif len(obs) == 1:
        got = next(iter(obs.values()))
    else:
        got = "ambig"
    ctx["cache"][line] = (got, out)
    return got, out


def minimize(ctx, line):
    cur = line

    def disagree(text):
        return observe_one(ctx, text)[0] != ref_verdict(text, ctx["root"])

    if not disagree(cur):
        return cur
    obj = json.loads(cur, object_pairs_hook=Pairs)
    cur_obj = Obj(list(obj))
    # 1) drop top-level members except one string id
    changed = True
    guard = 0
    while changed and guard < 60:
        changed = False
        guard += 1
        base = ser(cur_obj, ctx["rng"], bare=True)
        if not disagree(base):
            cur_obj = Obj(obj)  # restore (should not happen)
            break
        for i in range(len(cur_obj.pairs) - 1, -1, -1):
            if cur_obj.pairs[i][0] == "id":
                continue
            cand = Obj(cur_obj.pairs[:i] + cur_obj.pairs[i + 1:])
            text = ser(cand, ctx["rng"], bare=True)
            if disagree(text):
                cur_obj = cand
                changed = True
                break
    # 2) collapse nested container values
    for i, (k, v) in enumerate(list(cur_obj.pairs)):
        if isinstance(v, (Obj, list)):
            for repl in (Obj([]), []):
                cand = Obj(list(cur_obj.pairs))
                cand.pairs[i] = (k, repl)
                if disagree(ser(cand, ctx["rng"], bare=True)):
                    cur_obj = cand
                    break
    cur = ser(cur_obj, ctx["rng"], bare=True)
    # 3) collapse whitespace / duplicates left by serialization
    if disagree(cur):
        pass
    return cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, default=650)
    ap.add_argument("--flat", type=int, default=60, help="flat calibration records (no nesting/dups)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    gen = Gen(rng)
    root = a.root
    os.makedirs(root, exist_ok=True)
    t0 = time.time()
    files, pool = make_sources(rng, gen, root)

    # flat calibration: same contract model must agree with the gate, no nesting/dups
    flat_lines, flat_ids = [], []
    for i in range(a.flat):
        rel, text, span, L = rng.choice(pool)
        kind = ["supported", "mislocated", "stale", "unsupported"][i % 4]
        cid = "f%010x" % rng.getrandbits(40)
        flat_ids.append(cid)
        top = [("id", J(cid)), ("source", J(rel)), ("span", J(span)), ("expect", J("supported"))]
        if kind == "mislocated":
            top.append(("line", J(str((L + 1) % 9 + 1 if (L + 1) % 9 + 1 != L + 1 else L + 2))))
        elif kind == "supported":
            top.append(("line", J(str(L + 1))))
        elif kind == "stale":
            top.append(("sha256", J("%064x" % rng.getrandbits(256))))
        else:
            sp = gen.word()
            while sp in text:
                sp = gen.word()
            top = [(k, J(sp) if k == "span" else v) for k, v in top]
        rng.shuffle(top)
        flat_lines.append(ser(Obj(top), rng, bare=True))

    records, kinds, ids = [], [], []
    for i in range(a.n):
        cid = "c%010x" % rng.getrandbits(40)
        while cid in ids:
            cid = "c%010x" % rng.getrandbits(40)
        ids.append(cid)
        obj, kind = build_record(rng, gen, pool, cid)
        text = ser(obj, rng)
        try:
            json.loads(text, object_pairs_hook=Pairs)
        except Exception as e:  # harness error: never compare an invalid fixture
            print("FIXTURE_INVALID %s %r" % (cid, e), file=sys.stderr)
            return 2
        records.append(text)
        kinds.append(kind)

    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    for i in rng.sample(range(len(records)), max(1, len(records) // 25)):
        records[i] = records[i] + "\r"   # CRLF lines: same record, different trailing space
    for i in rng.sample(range(len(records)), max(1, len(records) // 14)):
        records[i] = rng.choice(["  ", "\t", " \t"]) + records[i]        # leading whitespace
    for i in rng.sample(range(len(records)), max(1, len(records) // 18)):
        records[i] = records[i] + rng.choice([" ", "\t", "  "])          # trailing whitespace
    # structural coverage stats, computed from the fixture with this harness's own parser
    stats = {"dup_read_key_records": 0, "nested_read_key_records": 0, "max_depth": 0}

    def walk(v, depth, st):
        st["max_depth"] = max(st["max_depth"], depth)
        seen = set()
        if isinstance(v, Pairs):
            for k, x in v:
                if k in READ8:
                    seen.add(k)
                walk(x, depth + 1, st)
        elif isinstance(v, list):
            for x in v:
                walk(x, depth + 1, st)
        return seen

    for line in records:
        obj = json.loads(line, object_pairs_hook=Pairs)
        names = [k for k, _ in obj]
        if any(names.count(k) > 1 for k in READ8):
            stats["dup_read_key_records"] += 1
        top = set(names) & set(READ8)
        deep = set()
        for k, x in obj:
            deep |= walk(x, 1, stats)
        if deep:
            stats["nested_read_key_records"] += 1
    with open(os.path.join(root, "claims.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(records) + "\n")

    # calibration first
    flat_path = os.path.join(root, "claims_flat.jsonl")
    with open(flat_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(flat_lines) + "\n")
    p = subprocess.run(["bash", a.gate, "verify-claims", flat_path, "--root", root],
                       capture_output=True, text=True, env=env, timeout=600, cwd=root)
    fobs = {}
    for ln in p.stdout.splitlines():
        m = CLAIM_RE.match(ln)
        if m:
            fobs[m.group(1)] = m.group(3)
    calib = []
    for cid, line in zip(flat_ids, flat_lines):
        ref = ref_verdict(line, root)
        got = fobs.get(cid, "none")
        if ref != got:
            calib.append({"line_id": cid, "ref": ref, "gate": got, "line": line})
    flat_ok = len(flat_ids) - len(calib)
    print("CALIBRATION_FLAT=%d/%d" % (flat_ok, len(flat_ids)))

    p = subprocess.run(["bash", a.gate, "verify-claims", os.path.join(root, "claims.jsonl"), "--root", root],
                       capture_output=True, text=True, env=env, timeout=900, cwd=root)
    rc, out = p.returncode, p.stdout
    obs, nclaim, inv = {}, {}, set()
    for ln in out.splitlines():
        m = CLAIM_RE.match(ln)
        if m:
            wid = m.group(1)
            nclaim[wid] = nclaim.get(wid, 0) + 1
            obs[wid] = m.group(3)
        m = INV_RE.match(ln)
        if m:
            inv.add(int(m.group(1)))

    ctx = {"gate": a.gate, "root": root, "env": env, "cache": {}, "rng": rng}
    rows, mismatches = [], []
    counts = {"match": 0, "mismatch": 0}
    for idx, (cid, line, kind) in enumerate(zip(ids, records, kinds), start=1):
        ref = ref_verdict(line, root)
        src_label = cid
        got = obs.get(cid)
        if got is None and idx in inv:
            got = "invalid"  # gate fell back to id=lineN (unreadable/duplicated id)
            src_label = "line%d" % idx
        else:
            src_label = cid
        if got is None:
            got = "none"
        n = nclaim.get(cid, 0) + (nclaim.get("line%d" % idx, 0))
        ok = ref == got and n == 1
        counts["match" if ok else "mismatch"] += 1
        rows.append({"n": idx, "id": cid, "kind": kind, "ref": ref, "gate": got, "nclaim": n,
                     "ok": ok, "line": line})
        if not ok:
            mismatches.append({"n": idx, "id": cid, "kind": kind, "ref": ref, "gate": got,
                               "nclaim": n, "line": line, "gate_id_label": src_label})

    for mm in mismatches:
        try:
            mm["minimal"] = minimize(ctx, mm["line"])
            mm["minimal_ref"] = ref_verdict(mm["minimal"], root)
            mm["minimal_gate"] = observe_one(ctx, mm["minimal"])[0]
            mm["minimal_output"] = observe_one(ctx, mm["minimal"])[1][:4000]
        except Exception as e:
            mm["minimal_error"] = repr(e)

    by_kind = {}
    for r in rows:
        b = by_kind.setdefault(r["kind"], [0, 0])
        b[1] += 1
        b[0] += r["ok"]
    result = {
        "seed": a.seed, "n": a.n, "flat": a.flat, "calibration_flat_ok": flat_ok,
        "calibration_flat_failures": calib, "gate_rc": rc,
        "gate_last_line": [l for l in out.splitlines() if l.startswith("RESEARCH_GATE:")][-1:] or [],
        "matched": counts["match"], "mismatched": counts["mismatch"],
        "structural_stats": stats,
        "ref_counts": {v: sum(1 for r in rows if r["ref"] == v) for v in {r["ref"] for r in rows}},
        "by_kind": {k: "%d/%d" % tuple(v) for k, v in by_kind.items()},
        "mismatches": mismatches, "elapsed_s": round(time.time() - t0, 1),
        "gate_sha256": hashlib.sha256(open(a.gate, "rb").read()).hexdigest(),
    }
    with open(a.out, "w") as f:
        json.dump(result, f, indent=1)
        f.write("\n")
    print("DIFF_CLAIMS=%d/%d" % (counts["match"], a.n))
    for k, v in sorted(by_kind.items()):
        print("  %-12s %d/%d" % (k, v[0], v[1]))
    print("MISMATCHES=%d" % counts["mismatch"])
    return 0 if counts["mismatch"] == 0 and flat_ok == a.flat else 1


if __name__ == "__main__":
    sys.exit(main())
