#!/usr/bin/env python3
"""Independent instrument-identity leg: D1 record + M17 mutant derived from the subject tool's own bytes."""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

S = sys.argv[1]
tree = os.path.join(S, "tree")
tool = os.path.join(tree, "tools", "gate-records.py")
counter = os.path.join(tree, "corpus", "evidence", "round86", "gate-records-r86.py")

# --- independent read of the committed S021 refetch row and its capture -------------------------------
refp = os.path.join(tree, "corpus", "evidence", "round57", "refetch.tsv")
row = None
for ln in open(refp, encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) == 9 and f[0] == "S021":
        row = f
        break
assert row is not None, "S021 row absent"
sid, url, key, attempt, fetched, curl_rc, http, raw, txt_sha = row
print(f"S021 row: attempt={attempt} fetched={fetched} curl_rc={curl_rc} http={http} txt_sha={txt_sha[:16]}")
assert http == "203" and curl_rc == "0"
cap = os.path.join(tree, "corpus", "captures", key + ".txt")
body = open(cap, "rb").read()
h = hashlib.sha256(body).hexdigest()
print(f"capture={os.path.relpath(cap, tree)} sha256={h[:16]} matches_txt_sha={h == txt_sha}")

reg = {}
for ln in open(os.path.join(tree, "corpus", "SOURCES.md"), encoding="utf-8"):
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    if len(cells) == 11 and re.match(r"^S\d{3,}$", cells[0]):
        reg[cells[0]] = cells
print(f"S021 registry tier={reg['S021'][3]}")

# --- the battery's own builder (exercised, not trusted) ------------------------------------------------
spec = importlib.util.spec_from_file_location("g86", counter)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
d1 = mod.build_d1_203_admit(tree)
assert d1 is not None
d1_sid, d1_line, d1_code = d1
print(f"build_d1_203_admit -> sid={d1_sid} expected_code={d1_code}")
print("D1 LINE:", d1_line)
assert d1_sid == "S021" and d1_code == "REFETCH"
assert f"capture=corpus/captures/{key}.txt" in d1_line
assert f"capture_sha256={h[:16]}" in d1_line
assert f"fetched={fetched}" in d1_line
assert f"tier={reg['S021'][3]}" in d1_line

# --- repaired tool refuses D1 with REFETCH -------------------------------------------------------------
d1f = os.path.join(S, "d1.md")
open(d1f, "w", encoding="utf-8").write(d1_line + "\n")
p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", tree, "--repo",
                    "/home/vgpnk/Projects/shokunin/chousa-shokunin", d1f],
                   capture_output=True, text=True)
print(f"REPAIRED_TOOL_EXIT={p.returncode}")
print("REPAIRED_TOOL_OUT:", p.stdout.strip().replace("\n", " | "))
assert p.returncode == 1
assert "FAIL" in p.stdout and "REFETCH" in p.stdout

# --- mutant built from the subject tool's bytes --------------------------------------------------------
src = open(tool, encoding="utf-8").read()
mutant_src = src.replace('r[6] == "200"', 'r[6].startswith("2")')
print(f"MUTANT_BYTES_DIFFER={mutant_src != src} replacements={src.count(chr(114) + chr(91) + chr(54) + chr(93))}")
assert mutant_src != src
mpath = os.path.join(S, "gate-records-M17.py")
open(mpath, "w", encoding="utf-8").write(mutant_src)

p2 = subprocess.run([sys.executable, "-B", mpath, "verify", "--root", tree, "--repo",
                     "/home/vgpnk/Projects/shokunin/chousa-shokunin", d1f],
                    capture_output=True, text=True)
print(f"MUTANT_D1_EXIT={p2.returncode}")
print("MUTANT_D1_OUT:", p2.stdout.strip().replace("\n", " | "))

# every frozen positive, on the mutant
files = sorted({ln.split("\t", 2)[0] for ln in open(os.path.join(tree, "corpus", "evidence", "round86",
                                                                 "c2-positives.tsv"), encoding="utf-8") if ln.strip()})
p3 = subprocess.run([sys.executable, "-B", mpath, "verify", "--root", tree, "--repo",
                     "/home/vgpnk/Projects/shokunin/chousa-shokunin"] + [os.path.join(tree, f) for f in files],
                    capture_output=True, text=True)
print(f"MUTANT_POSITIVES_EXIT={p3.returncode}")
print("MUTANT_POSITIVES_TAIL:", p3.stdout.strip().split("\n")[-1])
print(f"MUTANT_POSITIVES_FILES={len(files)}")
