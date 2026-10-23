#!/usr/bin/env python3
"""Audit L1-v2-rescore receipts: gate hash vs file, counter hash, summary cross-check, v1 receipts."""
import hashlib, json, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
CTRL = f"{LANE}/.ufo/waves/round-33/controls/L1-v2-rescore"
W1 = f"{LANE}/.ufo/waves/round-33/w1"
ART = f"{LANE}/.ufo/waves/round-33/w2/ReviewControlReceipts33"
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
V1 = "ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229"
BASE = "f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0"
BASE_OK_NAMES = {"research-gate-do-nothing", "pristine-gate", "base-pristine"}  # base by design

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()

findings, notes = [], []
lines_out = []

def F(sev, msg):
    findings.append((sev, msg))
    print(f"[{sev}] {msg}")

# --- sanity of referenced hashes ---
for name, p, want in (("landed gate", f"{LANE}/tools/research-gate.sh", None),
                      ("counter v2", f"{LANE}/corpus/evidence/round33/c1-count-v2.py", V2),
                      ("counter v1", f"{LANE}/corpus/evidence/round33/c1-count.py", V1)):
    h = sha(p)
    tag = "" if (want is None or h == want) else "  << MISMATCH vs expected"
    print(f"sha256 {name} {p}: {h}{tag}")
    lines_out.append(f"sha256 {name}: {h}{tag}")
    if want is not None and h != want:
        F("HIGH", f"{name} hash != design hash: {h}")

# --- per-receipt audit ---
receipts = sorted(fn for fn in os.listdir(CTRL) if fn.endswith(".json"))
print(f"\n{len(receipts)} json receipts in {CTRL}")
summary = {}
with open(f"{CTRL}/summary.txt") as f:
    for ln in f:
        m = re.match(r"^(\S+) (\S+) (\d+) rc=(\d+) (TOPLEVEL_FIELD_MATCH=\d+/\d+)$", ln.rstrip("\n"))
        if not m:
            F("HIGH", f"summary.txt unparsable line: {ln!r}")
            continue
        key = (m.group(1), m.group(2), int(m.group(3)))
        if key in summary:
            F("HIGH", f"summary.txt duplicate key {key}")
        summary[key] = (int(m.group(4)), m.group(5))
print(f"summary.txt: {len(summary)} lines")

seen_keys = set()
gate_hash_by_control = {}
rc_tab = []
for fn in receipts:
    p = f"{CTRL}/{fn}"
    with open(p) as f:
        r = json.load(f)
    seat, rest = fn.split("--", 1)
    rest = rest[:-len(".json")]
    name, seed = rest.rsplit("-s", 1)
    seed = int(seed)
    key = (seat, name, seed)
    seen_keys.add(key)
    tag = f"{fn}"
    # 1 counter hash
    if r.get("counter_sha256") != V2:
        F("HIGH", f"{tag}: counter_sha256={r.get('counter_sha256')} != v2 {V2}")
    # 2 gate file + hash
    g = r.get("gate", "")
    gp = g if os.path.isabs(g) else f"{LANE}/{g}"
    if not g.startswith(".ufo/waves/round-33/w1/"):
        F("HIGH", f"{tag}: gate path outside w1 controls: {g}")
    if not os.path.isfile(gp):
        F("HIGH", f"{tag}: gate file missing: {g}")
    else:
        h = sha(gp)
        if h != r.get("gate_sha256"):
            F("HIGH", f"{tag}: gate_sha256={r.get('gate_sha256')} != sha256(file)={h} ({g})")
    if r.get("gate_sha256") == BASE and name not in BASE_OK_NAMES:
        F("CRIT", f"{tag}: BASE gate hash under mutated-control name '{name}' (round-32 mistake)")
    # 3 arithmetic / labels
    tot, mat = r.get("total"), r.get("matched")
    lbl = r.get("label", "")
    if tot != 156:
        F("HIGH", f"{tag}: total={tot} != 156")
    if lbl != f"TOPLEVEL_FIELD_MATCH={mat}/{tot}":
        F("HIGH", f"{tag}: label={lbl!r} vs matched/total={mat}/{tot}")
    if r.get("predicate_holds") != (mat == 156):
        F("HIGH", f"{tag}: predicate_holds={r.get('predicate_holds')} vs matched==156 ({mat})")
    if seed not in (3341, 3342):
        F("MEDIUM", f"{tag}: unexpected seed {seed}")
    # gate_rc must be 1 per counter contract (DRIFT gate run)
    grc = r.get("gate_rc")
    if grc != 1:
        F("MEDIUM", f"{tag}: gate_rc={grc} != 1 (counter requires gate exit 1 + DRIFT)")
    # .out first line
    op = f"{CTRL}/{fn[:-5]}.out"
    if os.path.isfile(op):
        first = open(op).readline().strip()
        if first != lbl:
            F("MEDIUM", f"{tag}: .out first line {first!r} != label {lbl!r}")
    else:
        F("MEDIUM", f"{tag}: missing .out sidecar")
    # summary cross-check
    if key not in summary:
        F("HIGH", f"{tag}: no summary.txt line for {key}")
    else:
        _, slbl = summary[key]
        if slbl != lbl:
            F("HIGH", f"{tag}: summary label {slbl!r} != receipt label {lbl!r}")
        # rc vs matched (counter exits 0 iff matched==TOTAL else 1)
        exp_rc = 0 if mat == 156 else 1
        # note: oracle gates: counter exit 0; for rc we check both directions below
    # collect gate hash per control for duplicate check
    gate_hash_by_control.setdefault((seat, name), set()).add(r.get("gate_sha256"))

# counter rc consistency using summary rc values
for (seat, name, seed), (rc, slbl) in sorted(summary.items()):
    m = re.match(r"TOPLEVEL_FIELD_MATCH=(\d+)/(\d+)", slbl)
    mat, tot = int(m.group(1)), int(m.group(2))
    exp = 0 if mat == tot else 1
    if rc != exp:
        F("MEDIUM", f"summary {seat} {name} s{seed}: rc={rc} but matched={mat}/{tot} (counter exit should be {exp})")
    fn = f"{seat}--{name}-s{seed}.json"
    if not os.path.isfile(f"{CTRL}/{fn}"):
        F("HIGH", f"summary row without receipt: {fn}")

missing = set(summary) - seen_keys
if missing:
    F("HIGH", f"summary rows without receipts: {sorted(missing)}")

# duplicate gate hashes across distinct control names in one seat
for (seat, name), hs in sorted(gate_hash_by_control.items()):
    for h in hs:
        pass
all_pairs = {}
for (seat, name), hs in gate_hash_by_control.items():
    for h in hs:
        all_pairs.setdefault(h, []).append(f"{seat}/{name}")
for h, who in sorted(all_pairs.items()):
    uniq = sorted(set(who))
    if len(uniq) > 1:
        print(f"NOTE gate hash {h[:12]}… shared by: {', '.join(uniq)}")
        lines_out.append(f"NOTE gate hash {h[:12]} shared by: {', '.join(uniq)}")
        if not (set(uniq) <= {"CtlC1DoNothing/research-gate-do-nothing", "CtlC1BraceDepth/pristine-gate", "CtlC1NoFinding/base-pristine"}):
            F("MEDIUM", f"distinct controls share one gate file content: {uniq} (hash {h[:16]}…)")

# --- seat v1 receipts: w1/<Seat>/*.json ---
print("\n--- v1 receipts in w1/<Seat>/ ---")
v1_rows = []
for d in sorted(os.listdir(W1)):
    dd = f"{W1}/{d}"
    if not os.path.isdir(dd) or not d.startswith("CtlC1"):
        continue
    for fn in sorted(os.listdir(dd)):
        if not fn.endswith(".json"):
            continue
        p = f"{dd}/{fn}"
        try:
            with open(p) as f:
                r = json.load(f)
        except Exception as e:
            F("MEDIUM", f"w1/{d}/{fn}: unparsable json: {e}")
            continue
        if not isinstance(r, dict) or "counter_sha256" not in r:
            continue
        cs = r.get("counter_sha256")
        kind = "v1" if cs == V1 else ("v2" if cs == V2 else f"OTHER:{cs}")
        g = r.get("gate", "")
        gp = g if os.path.isabs(g) else f"{LANE}/{g}"
        gexists = os.path.isfile(gp)
        gh = sha(gp) if gexists else None
        hm = (gh == r.get("gate_sha256")) if gexists else None
        v1_rows.append((d, fn, kind, r.get("gate"), r.get("gate_sha256"), r.get("seed"), r.get("matched"), r.get("total"), gexists, hm))
        if kind == "v1" and r.get("gate_sha256") == BASE:
            if d not in ("CtlC1DoNothing",) and not re.search(r"(pristine|do-nothing|base)", fn):
                F("CRIT", f"w1/{d}/{fn}: v1 receipt gate_sha256 == BASE under control name (round-32 mistake)")
        if gexists and not hm:
            F("HIGH", f"w1/{d}/{fn}: receipt gate_sha256 != current file hash ({g})")

for row in v1_rows:
    d, fn, kind, g, gh, seed, mat, tot, gexists, hm = row
    print(f"w1/{d}/{fn} counter={kind} seed={seed} matched={mat}/{tot} gate={g} gate_sha256={gh} file_ok={hm}")

print("\n--- RESULT ---")
print(f"findings: {len(findings)}")
for sev, msg in findings:
    print(f"{sev}: {msg}")
with open(f"{ART}/audit-detail.txt", "w") as f:
    f.write("\n".join(lines_out) + "\n")
    f.write("\nFINDINGS\n")
    for sev, msg in findings:
        f.write(f"{sev}: {msg}\n")
print(f"detail -> {ART}/audit-detail.txt")
