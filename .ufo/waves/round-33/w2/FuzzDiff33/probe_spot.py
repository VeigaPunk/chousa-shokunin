#!/usr/bin/env python3
"""Hand-written spot probe: minimal C1 records, one per contract clause.
Expected verdict is stated in EXPECT; the gate output is printed verbatim."""
import os
import subprocess
import sys

root = sys.argv[1]
gate = sys.argv[2]
os.makedirs(os.path.join(root, "src"), exist_ok=True)
src = "src/spot.md"
lines = ["alpha beta gamma.", "delta SPANWORD epsilon.", "zeta eta theta.", "iota kappa lambda.",
         "mu nu xi.", "omicron pi rho.", "sigma tau upsilon.", "phi chi psi.", "omega alif bet."]
with open(os.path.join(root, src), "w", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

RECS = [
    ("S1 nested decoy before top-level line, top right",
     '{"meta": {"line": "9"}, "id": "s1", "source": "%s", "span": "SPANWORD", "expect": "supported", "line": "2"}' % src,
     "supported"),
    ("S2 nested line right, top-level line wrong",
     '{"meta": {"line": "2"}, "id": "s2", "source": "%s", "span": "SPANWORD", "expect": "supported", "line": "4"}' % src,
     "mislocated"),
    ("S3 duplicated top-level span, identical values",
     '{"id": "s3", "source": "%s", "span": "SPANWORD", "span": "SPANWORD", "expect": "supported"}' % src,
     "invalid"),
    ("S4 top-level line is an object holding the right line",
     '{"id": "s4", "source": "%s", "span": "SPANWORD", "expect": "supported", "line": {"line": "2"}}' % src,
     "invalid"),
    ("S5 depth-4 nesting holding all seven keys, none top-level except the four required",
     '{"d1": [{"d2": {"d3": [{"line": "2", "sha256": "x", "marker": "m", "id": "fake", "source": "fake.md", "span": "fake", "expect": "contradicted"}]}}], '
     '"id": "s5", "source": "%s", "span": "SPANWORD", "expect": "supported"}' % src,
     "supported"),
    ("S6 string value carries fake members before a wrong top-level line",
     '{"note": "fake \\"line\\": \\"2\\", \\"sha256\\": \\"z\\" } ]", "id": "s6", "source": "%s", "span": "SPANWORD", "expect": "supported", "line": "4"}' % src,
     "mislocated"),
    ("S7 duplicated top-level id, identical values",
     '{"id": "s7", "id": "s7", "source": "%s", "span": "SPANWORD", "expect": "supported"}' % src,
     "invalid"),
    ("S8 duplicated top-level id, differing values",
     '{"id": "s8", "source": "%s", "span": "SPANWORD", "expect": "supported", "id": "zzz"}' % src,
     "invalid"),
    ("S9 top-level id is a number",
     '{"id": 9, "source": "%s", "span": "SPANWORD", "expect": "supported"}' % src,
     "invalid"),
    ("S10 duplicated top-level expect, identical values",
     '{"id": "s10", "source": "%s", "span": "SPANWORD", "expect": "supported", "expect": "supported"}' % src,
     "invalid"),
]
path = os.path.join(root, "claims_spot.jsonl")
with open(path, "w", newline="\n") as f:
    f.write("\n".join(r for _, r, _ in RECS) + "\n")
env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
p = subprocess.run(["bash", gate, "verify-claims", path, "--root", root],
                   capture_output=True, text=True, env=env, timeout=300, cwd=root)
claims = {l.split()[1][3:]: l for l in p.stdout.splitlines() if l.startswith("CLAIM id=")}
finds = [l for l in p.stdout.splitlines() if l.startswith("FINDING CLAIM_RECORD_INVALID")]
print("rc=%d" % p.returncode)
pos = 0
ok = 0
for i, (label, rec, want) in enumerate(RECS, start=1):
    hit = claims.get("s%d" % i) or claims.get("line%d" % i)
    got = hit.split("observed=")[1].split()[0] if hit else "none"
    ok += got == want
    print("%-4s want=%-11s got=%-11s %s" % ("S%d" % i, want, got, label))
    print("      %s" % (hit or "NO CLAIM LINE"))
print("finds=%d" % len(finds))
for fl in finds:
    print("  " + fl)
print("SPOT_OK=%d/%d" % (ok, len(RECS)))
