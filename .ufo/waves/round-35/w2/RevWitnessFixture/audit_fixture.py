#!/usr/bin/env python3
"""Audit tools/mechanism-witness.py generate()/build()/Gen.span against the
landed gate's contract, per RevWitnessFixture assignment. Read-only on the lane.
"""
import importlib.util, json, os, re, sys, collections

MW = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py"
BASE = "/tmp/hyaku/chousa-r35/w2/RevWitnessFixture"
os.makedirs(BASE, exist_ok=True)
spec = importlib.util.spec_from_file_location("mw", MW)
mw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mw)

DZ_MIN, DZ_MAX = mw.DZ_MIN, mw.DZ_MAX
SEEDS = list(range(9100, 9120))

def all_offsets(hay, span):
    """non-overlapping left-to-right offsets, the order grep -o reports."""
    out, i = [], hay.find(span)
    while i >= 0:
        out.append(i)
        i = hay.find(span, i + len(span))
    return out

def delimited_line_ranges(hay, span):
    """Reproduce the gate's boundary rule (research-gate.sh tok_left_ok /
    tok_right_ok, ASCII-letters fixture variant): left char must not be a
    letter/digit-class word char etc. Fixture vocab is letters+space+newline,
    so the only boundary-breakers possible are letters (and the word-internal
    '-' / "'" rule can never trigger: no '-' or "'" bytes exist)."""
    res = []
    for off in all_offsets(hay, span):
        left_ok = off == 0 or hay[off - 1] not in mw.LETTERS and not hay[off - 1].isalnum()
        # boundary = file/line edge, ASCII whitespace, or punctuation;
        # a letter or digit before/after makes it glued. Fixture bytes are
        # letters, spaces, newlines only -> check alnum-ish bytes only.
        lb = hay[off - 1] if off > 0 else None
        rb = hay[off + len(span)] if off + len(span) < len(hay) else None
        def is_word_byte(c):
            return c is not None and (c in mw.LETTERS or c.isdigit() or c == "_")
        lo = not is_word_byte(lb)
        ro = not is_word_byte(rb)
        # word-internal '-'/'\'': adjacent word bytes both sides -> still
        # boundary breakers; impossible here (no such bytes), kept for form.
        if lb in ("-", "'") and off >= 2 and is_word_byte(hay[off - 2]):
            lo = False
        if rb in ("-", "'") and off + len(span) + 1 < len(hay) and is_word_byte(hay[off + len(span) + 1]):
            ro = False
        if lo and ro:
            l1 = hay.count("\n", 0, off) + 1
            res.append((l1, l1 + span.count("\n"), off))
    return res

print("== A: generate() audit over %d seeds ==" % len(SEEDS))
all_stats = collections.defaultdict(lambda: [None, None, 0])
per_seed_meta = []
line_checks = []
problems = []
for seed in SEEDS:
    root = os.path.join(BASE, "fx", "s%d" % seed)
    claims_path, truth, scheme = mw.generate(root, seed)
    rows = [json.loads(l) for l in open(claims_path, encoding="utf-8")]
    meta = {"seed": seed, "scheme": scheme, "n_records": len(rows),
            "class_order": [], "key_orders": set(), "id_widths": set(),
            "id_prefixes": set(), "rel_names": []}
    for r_i, row in enumerate(rows):
        cls, t = truth[row["id"]]
        meta["class_order"].append(cls)
        meta["key_orders"].add(tuple(sorted(row)))
        meta["rel_names"].append(row["source"])
        m = re.match(r"^([a-z]+)([0-9a-f]+)$", row["id"])
        if m:
            meta["id_prefixes"].add(m.group(1))
            meta["id_widths"].add(len(m.group(2)))
        span = row["span"]
        n = len(span)
        lo, hi = (DZ_MIN, DZ_MAX) if cls != "short-verbatim" else (512, 4096)
        if cls == "dz-edge":
            ok_len = n in (DZ_MIN, DZ_MAX)
        else:
            ok_len = lo <= n <= hi
        st = all_stats[cls]
        st[0] = n if st[0] is None else min(st[0], n)
        st[1] = n if st[1] is None else max(st[1], n)
        st[2] += 1
        if not ok_len:
            problems.append("seed %d rec %d class %s span len %d out of [%d,%d]" % (seed, r_i, cls, n, lo, hi))
        if cls == "dz-verbatim-1l" and "\n" in span:
            problems.append("seed %d: dz-verbatim-1l span contains newline" % seed)
        if cls != "dz-verbatim-1l" and cls != "short-verbatim" and cls != "dz-edge" and "\n" not in span:
            problems.append("seed %d rec %d: %s span has no newline (injection failed)" % (seed, r_i, cls))
        if row["expect"] != "supported":
            problems.append("seed %d rec %d: expect=%r" % (seed, r_i, row["expect"]))
        # line-bound check
        fpath = os.path.join(root, row["source"])
        if not os.path.isfile(fpath):
            problems.append("seed %d rec %d: source file missing %s" % (seed, r_i, fpath))
            continue
        hay = open(fpath, encoding="utf-8").read()
        if "line" in row:
            occ = delimited_line_ranges(hay, span)
            rngs = [(a, b) for a, b, _ in occ]
            want = tuple(int(x) for x in row["line"].split("-"))
            line_checks.append({"seed": seed, "id": row["id"], "line": row["line"],
                                "occ_ranges": rngs, "binds": want in rngs,
                                "raw_occurrences": len(all_offsets(hay, span))})
            if want not in rngs:
                problems.append("seed %d: line %s not a delimited range %s" % (seed, row["line"], rngs))
        else:
            # supported classes: span must occur boundary-delimited;
            # unsupported: span must NOT occur boundary-delimited
            occ = delimited_line_ranges(hay, span)
            if t == "supported" and not occ:
                problems.append("seed %d rec %d %s: supported span has no delimited occurrence" % (seed, r_i, cls))
            if t == "unsupported":
                if cls == "dz-glued-left":
                    raw = all_offsets(hay, span)
                    if occ:
                        problems.append("seed %d rec %d: glued-left unexpectedly delimited" % (seed, r_i))
                    if not raw:
                        problems.append("seed %d rec %d: glued-left raw occurrence missing (gate would report miss, still unsupported)" % (seed, r_i))
                elif cls == "dz-mut" and occ:
                    problems.append("seed %d rec %d: mutated span unexpectedly found" % (seed, r_i))
    meta["key_orders"] = sorted(meta["key_orders"])
    meta["id_widths"] = sorted(meta["id_widths"])
    meta["id_prefixes"] = sorted(meta["id_prefixes"])
    # duplicate rel name check
    if len(set(meta["rel_names"])) != len(meta["rel_names"]):
        problems.append("seed %d: duplicate source rel names %s" % (seed, meta["rel_names"]))
    per_seed_meta.append(meta)

print("span len min/max/count per class (generate(), 9 records x 20 seeds):")
for cls in [c for c, _, _ in mw.CLASS_COUNTS]:
    lo, hi, n = all_stats[cls]
    print("  %-15s min=%s max=%s n=%d" % (cls, lo, hi, n))
print("line-bound checks: %d records, all bind=%s"
      % (len(line_checks), all(c["binds"] for c in line_checks)))
for c in line_checks[:4]:
    print("   sample %s" % json.dumps(c, sort_keys=True)[:220])
print("problems: %d" % len(problems))
for p in problems[:40]:
    print("   " + p)

print()
print("== B: randomization diversity across the %d seeds ==" % len(SEEDS))
schemes = set(m["scheme"] for m in per_seed_meta)
widths = set(w for m in per_seed_meta for w in m["id_widths"])
prefixes = set(p for m in per_seed_meta for p in m["id_prefixes"])
orders = set(tuple(m["class_order"]) for m in per_seed_meta)
keysets = set(tuple(m["key_orders"]) for m in per_seed_meta)
first_lines = []
for seed in SEEDS:
    rows = open(os.path.join(BASE, "fx", "s%d" % seed, "claims.jsonl")).read().splitlines()
    first_lines.append(rows[0][:60])
key_seqs = set()
for seed in SEEDS:
    for l in open(os.path.join(BASE, "fx", "s%d" % seed, "claims.jsonl")).read().splitlines():
        key_seqs.add(tuple(json.loads(l).keys()))
print("schemes=%s" % sorted(schemes))
print("distinct id widths=%s prefixes=%d" % (sorted(widths), len(prefixes)))
print("distinct class orders=%d/%d" % (len(orders), len(SEEDS)))
print("distinct first-record lines=%d/%d" % (len(set(first_lines)), len(SEEDS)))
print("distinct key-order permutations=%d (of max %d records)" % (len(key_seqs), 9 * len(SEEDS)))
rel_pats = collections.Counter()
for m in per_seed_meta:
    for r in m["rel_names"]:
        rel_pats["hex" if re.fullmatch(r"corpus/[0-9a-f]{16}\.md", r) else "word"] += 1
print("source-name schemes seen: %s" % dict(rel_pats))
print("per-seed schemes: %s" % [m["scheme"] for m in per_seed_meta])

print()
print("== C: 300 draws per class via build() across 20 fresh Gen seeds ==")
import random
draw = collections.defaultdict(list)
for s_i, seed in enumerate(range(7200, 7220)):
    rng = random.Random(seed)
    g = mw.Gen(rng)
    per = 300 // 20
    for _ in range(per):
        for cls, _, _ in mw.CLASS_COUNTS:
            _, span, _, _ = mw.build(g, rng, cls)
            draw[cls].append(len(span))
for cls, _, _ in mw.CLASS_COUNTS:
    v = draw[cls]
    print("  %-15s n=%d min=%d max=%d" % (cls, len(v), min(v), max(v)))

json.dump({"problems": problems,
           "span_stats": {c: list(all_stats[c]) for c in all_stats},
           "line_checks": line_checks,
           "meta": [{k: (list(v) if isinstance(v, set) else v) for k, v in m.items()} for m in per_seed_meta],
           "draw_minmax": {c: [min(v), max(v)] for c, v in draw.items()}},
          open(os.path.join(BASE, "fixture_audit.json"), "w"), indent=1, sort_keys=True)
print("\nwrote %s" % os.path.join(BASE, "fixture_audit.json"))
