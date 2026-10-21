#!/usr/bin/env bash
# Round-25 differential for `verify-metadata` (chousa-shokunin). From the lane root:
#   bash corpus/evidence/round25-meta-differential.sh
# Three independent derivations per fixture in corpus/fixtures/metadata-r25/:
# (1) the hand-derived README table (ExecMetaMutants seat, written from spec v1),
# (2) the gate, (3) the stdlib oracle corpus/evidence/round25-meta-oracle.py
# (ExecMetaOracle seat, written from spec v1 without reading the gate).
# Compares META line, finding-id set and exit, normal and CHOUSA_STRICT=1.
# Read-only; prints one row per fixture × mode and AGREE=N/M.
set -u
F=corpus/fixtures/metadata-r25
python3 - "$F" <<'PY'
import re, subprocess, sys, os
F = sys.argv[1]
rows = {}
for l in open(os.path.join(F, "README.md"), encoding="utf-8"):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(c) == 4 and c[0].startswith("`") and c[0].endswith(".md`"):
        name = c[0].strip("`")
        assert name not in rows, "duplicate fixture row: " + name
        metas = re.findall(r"`(META [^`]+)`", c[1])
        normal = metas[0]; strict = metas[1] if len(metas) > 1 else normal
        ids = set(re.findall(r"META_[A-Z_]+", c[2]))
        en, es = [int(x) for x in re.findall(r"\d", c[3])[:2]]
        rows[name] = {"0": (normal, ids, en), "1": (strict, ids, es)}
assert len(rows) == 27, "frozen fixture population must contain 27 rows"
assert set(rows) == {n for n in os.listdir(F) if n.endswith(".md") and n != "README.md"}, "fixture table/file population mismatch"
def run(cmd, strict):
    env = dict(os.environ, CHOUSA_STRICT=strict)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    meta = [l for l in r.stdout.splitlines() if l.startswith("META ")]
    ids = set(re.findall(r"^FINDING (META_[A-Z_]+)", r.stdout, re.M))
    return (meta[0] if meta else "-", ids, r.returncode)
agree = total = 0
for name in sorted(rows):
    p = os.path.join(F, name)
    for strict in ("0", "1"):
        want = rows[name][strict]
        gate = run(["bash", "tools/research-gate.sh", "verify-metadata", p, "--root", "."], strict)
        orc = run(["python3", "corpus/evidence/round25-meta-oracle.py", p], strict)
        ok = gate == want and orc == want
        total += 1; agree += ok
        if not ok:
            print("DISAGREE %s strict=%s want=%s gate=%s oracle=%s" % (name, strict, want, gate, orc))
print("AGREE=%d/%d (fixtures=%d, modes normal+strict)" % (agree, total, len(rows)))
sys.exit(0 if total > 0 and agree == total else 1)
PY
