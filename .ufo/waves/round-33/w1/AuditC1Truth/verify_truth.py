#!/usr/bin/env python3
"""Independent C1 truth audit (AuditC1Truth, round 33 wave 1).

For each kept counter fixture: parse every claims.jsonl line with json.loads
(object_pairs_hook keeps top-level pairs, so duplicates are visible), derive the
contract verdict from the source file bytes with a local re-implementation of the
gate's documented token-boundary rule (research-gate.sh header + r31 rules), and
compare the derived truth with the counter's truth.json.

Not derived from c1-count.py: no import, no reuse of its classes or helpers.
Also: JSON validity of every line; per-class truth tallies; creation-order
(mtime_rank, inode_rank) association with class (rank-biserial per class and
Kruskal-Wallis over 15 classes, plus a seeded permutation p-value).
Prints one JSON object to stdout; exits 1 if any disagreement or invalid line.
"""
import hashlib
import json
import os
import statistics
import sys

READ_KEYS = ("id", "source", "span", "expect", "marker", "line", "sha256")
WS = " \t\n\r\v\f"
PUNCT = "!\"#$%&()*+,./:;<=>?@[\\]^_`{|}~"


def word_char(c):
    if not c:
        return False
    if c.isascii() and c.isalnum():
        return True
    if c in "-'":
        return False
    if c in WS or c in PUNCT:
        return False
    return True


def left_ok(before, span):
    if not before:
        return True
    c = before[-1]
    if c in "-'":
        n = before[-2] if len(before) >= 2 else ""
        if word_char(n) and word_char(span[0]):
            return False
        return True
    return c in WS or c in PUNCT


def right_ok(after, span):
    if not after:
        return True
    c = after[0]
    if c in "-'":
        n = after[1] if len(after) >= 2 else ""
        if word_char(n) and word_char(span[-1]):
            return False
        return True
    return c in WS or c in PUNCT


def occurrences(hay, span):
    """Yield (l1, l2) for every boundary-delimited occurrence, file order."""
    if not span:
        return
    pos = hay.find(span)
    while pos != -1:
        before, after = hay[:pos], hay[pos + len(span):]
        if left_ok(before, span) and right_ok(after, span):
            l1 = before.count("\n") + 1
            l2 = l1 + span.count("\n")
            yield (l1, l2)
        pos = hay.find(span, pos + 1)


class Obj(dict):
    """dict mirroring pairs so top-level duplicates stay visible."""
    def __init__(self, pairs):
        super().__init__(pairs)
        self.pairs = list(pairs)


def parse_line(line):
    return json.loads(line, object_pairs_hook=Obj)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def derive(rec, root):
    """Contract verdict for one record, from its top-level members and bytes."""
    pairs = rec.pairs
    seen = {}
    for k, _ in pairs:
        seen[k] = seen.get(k, 0) + 1
    dup_keys = sorted(k for k in seen if k in READ_KEYS and seen[k] > 1)
    if dup_keys:
        return "invalid", "duplicate read key(s): %s" % ",".join(dup_keys)
    get = lambda k: rec.get(k) if isinstance(rec.get(k), str) else None
    # a present non-string value for a string-read field makes the gate's read
    # malformed only for sha256/line; the fixture has string values only.
    rid, src, span, expect = get("id"), get("source"), get("span"), get("expect")
    if not rid:
        return "invalid", "missing id"
    if not src:
        return "invalid", "missing source"
    if not span:
        return "invalid", "missing/empty span"
    if not expect:
        return "invalid", "missing expect"
    if expect not in ("supported", "contradicted", "unsupported"):
        return "invalid", "expect=%r invalid" % expect
    if "sha256" in rec:
        sha = rec.get("sha256")
        if not isinstance(sha, str):
            return "invalid", "sha256 non-string"
        if not (len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)):
            return "invalid", "sha256 malformed"
    linef = rec.get("line") if "line" in rec else None
    line_range = None
    if linef is not None:
        if not isinstance(linef, str):
            return "invalid", "line not a JSON string"
        if len(linef) > 0 and linef[0] in "123456789" and linef.isdigit():
            line_range = (int(linef), int(linef))
        elif "-" in linef:
            a, _, b = linef.partition("-")
            if a.isdigit() and b.isdigit() and a[0] != "0" and b[0] != "0" and int(b) > int(a):
                line_range = (int(a), int(b))
            else:
                return "invalid", "line range malformed"
        else:
            return "invalid", "line value malformed"
    marker = rec.get("marker")
    if isinstance(marker, str) and marker and expect != "contradicted":
        return "invalid", "marker with expect=%s" % expect
    path = os.path.realpath(os.path.join(root, src))
    if not path.startswith(os.path.realpath(root) + os.sep) or not os.path.isfile(path):
        return "refused", "source not readable in root"
    data = open(path, "rb").read()
    if "sha256" in rec:
        if sha256_bytes(data) != rec["sha256"]:
            return "stale", "sha256 mismatch"
    hay = data.decode("utf-8")
    occ = list(occurrences(hay, span))
    if line_range is None:
        if occ:
            if expect == "supported":
                return "supported", "delimited occurrence %s" % (occ[0],)
            return "unsupported", "span present but expect=%s" % expect
        return "unsupported", "no delimited occurrence"
    if any(o == line_range for o in occ):
        if expect == "supported":
            return "supported", "occurrence on named line %s" % (line_range,)
        return "unsupported", "span on named line but expect=%s" % expect
    if occ:
        return "mislocated", "delimited occurrences %s, named %s" % (occ, line_range)
    return "unsupported", "no delimited occurrence"


def ranks(values):
    """Average ranks for ties, 1-based."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for t in range(i, j + 1):
            out[order[t]] = avg
        i = j + 1
    return out


def kruskal(values, groups):
    n = len(values)
    r = ranks(values)
    idx = {}
    for i, g in enumerate(groups):
        idx.setdefault(g, []).append(r[i])
    h = 0.0
    for g, rs in idx.items():
        m = sum(rs) / len(rs)
        h += len(rs) * (m - (n + 1) / 2.0) ** 2
    h *= 12.0 / (n * (n + 1))
    # tie correction
    from collections import Counter
    cnt = Counter(values)
    tie = sum(t ** 3 - t for t in cnt.values() if t > 1)
    if tie:
        h /= (1.0 - tie / (n ** 3 - n))
    k = len(idx)
    return h, k - 1, n


def rank_biserial(values, groups, g):
    inr = [values[i] for i, x in enumerate(groups) if x == g]
    outr = [values[i] for i, x in enumerate(groups) if x != g]
    n1, n2 = len(inr), len(outr)
    if n1 == 0 or n2 == 0:
        return None
    u = sum(1 for a in inr for b in outr if a > b) + 0.5 * sum(1 for a in inr for b in outr if a == b)
    return 2.0 * u / (n1 * n2) - 1.0


def audit(keep):
    root = os.path.abspath(keep)
    truth = json.load(open(os.path.join(root, "truth.json")))
    lines = open(os.path.join(root, "claims.jsonl"), "rb").read().decode("utf-8").split("\n")
    assert lines and lines[-1] == ""
    lines = lines[:-1]
    bad_json, derived, disagree = [], {}, []
    file_of_record = {}
    raw_of_record = {}
    for i, line in enumerate(lines):
        try:
            rec = parse_line(line)
        except Exception as e:
            bad_json.append({"lineno": i + 1, "err": repr(e)})
            continue
        if not isinstance(rec, Obj) or not rec.pairs:
            bad_json.append({"lineno": i + 1, "err": "not a JSON object"})
            continue
        rid = rec.get("id")
        v, why = derive(rec, root)
        derived[rid] = (v, why)
        raw_of_record[rid] = line
        for k, _ in rec.pairs:
            pass
    # attribute each source file to the record whose line text mentions it
    src_dir = os.path.join(root, "src")
    files = sorted(os.listdir(src_dir))
    for f in files:
        rel = "src/" + f
        owners = [rid for rid, raw in raw_of_record.items() if ('"' + rel + '"') in raw]
        file_of_record[rel] = owners
    for rid, (cls, t) in truth.items():
        if rid not in derived:
            disagree.append({"id": rid, "class": cls, "truth": t, "derived": None, "why": "record missing"})
            continue
        v, why = derived[rid]
        if v != t:
            disagree.append({"id": rid, "class": cls, "truth": t, "derived": v, "why": why})
    # truth tallies vs 15 class labels
    per_class = {}
    for rid, (cls, t) in truth.items():
        per_class.setdefault(cls, {}).setdefault(t, 0)
        per_class[cls][t] += 1
    # creation order vs class
    st = []
    for f in files:
        p = os.path.join(src_dir, f)
        s = os.stat(p)
        st.append((f, s.st_mtime_ns, s.st_ino, s.st_ctime_ns))
    mtime_rank = ranks([x[1] for x in st])
    ino_rank = ranks([x[2] for x in st])
    n_orig = len(st)
    # collapse ties to unique order for reporting mean ranks
    groups, unclassed = [], []
    for i, (f, _, _, _) in enumerate(st):
        rel = "src/" + f
        owners = file_of_record.get(rel, [])
        o = sorted(owners)
        if len(o) == 1:
            groups.append(truth[o[0]][0])
        elif len(o) > 1:
            groups.append("MULTI:" + ",".join(sorted(set(truth[x][0] for x in o))))
        else:
            groups.append("UNOWNED")
            unclassed.append(rel)
    h_m, df_m, n_m = kruskal(mtime_rank, groups)
    h_i, df_i, n_i = kruskal(ino_rank, groups)
    cls_names = sorted(set(groups))
    rb_m = {g: rank_biserial(mtime_rank, groups, g) for g in cls_names}
    rb_i = {g: rank_biserial(ino_rank, groups, g) for g in cls_names}
    # permutation test for H (mtime), seeded
    import random
    rng = random.Random(20261023)
    idx = list(range(n_m))
    ge = 0
    for _ in range(4000):
        rng.shuffle(idx)
        shuffled = [groups[j] for j in idx]
        hh, _, _ = kruskal(mtime_rank, shuffled)
        if hh >= h_m:
            ge += 1
    p_m = (ge + 1) / 4001.0
    ge = 0
    for _ in range(4000):
        rng.shuffle(idx)
        shuffled = [groups[j] for j in idx]
        hh, _, _ = kruskal(ino_rank, shuffled)
        if hh >= h_i:
            ge += 1
    p_i = (ge + 1) / 4001.0
    mean_rank = {}
    for g in cls_names:
        rs = [mtime_rank[i] for i, x in enumerate(groups) if x == g]
        mean_rank[g] = round(statistics.fmean(rs) / (n_m + 1), 3)
    return {
        "keep": keep,
        "records": len(lines),
        "bad_json_lines": bad_json,
        "derived_counts": {k: sum(1 for v, _ in derived.values() if v == k) for k in sorted(set(v for v, _ in derived.values()))},
        "truth_counts": {k: sum(1 for _, t in truth.values() if t == k) for k in sorted(set(t for _, t in truth.values()))},
        "disagreements": disagree,
        "disagreement_classes": sorted(set(d["class"] for d in disagree)),
        "per_class_truth": {k: dict(sorted(v.items())) for k, v in sorted(per_class.items())},
        "files": n_orig,
        "unowned_files": unclassed,
        "multi_owned_files": [f for f, o in file_of_record.items() if len(o) > 1],
        "creation_order": {
            "mtime": {"kruskal_h": round(h_m, 3), "df": df_m, "perm_p": p_m,
                      "mean_rank_per_class": mean_rank,
                      "rank_biserial": {k: (round(v, 3) if v is not None else None) for k, v in rb_m.items()}},
            "inode": {"kruskal_h": round(h_i, 3), "df": df_i, "perm_p": p_i,
                      "rank_biserial": {k: (round(v, 3) if v is not None else None) for k, v in rb_i.items()}},
        },
    }


def main():
    out = {"keeps": [audit(k) for k in sys.argv[1:]]}
    print(json.dumps(out, indent=1, sort_keys=True))
    bad = any(k["bad_json_lines"] or k["disagreements"] for k in out["keeps"])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
