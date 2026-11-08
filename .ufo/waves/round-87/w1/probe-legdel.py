import subprocess, sys, os
root = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt"
repo = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
work = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/work"
orig = os.path.join(root, "corpus/evidence/round87/gate-records-r87.py")
src = open(orig, encoding="utf-8").read()
# Delete one leg append entirely (14 legs)
v = src.replace('                ("SETUP", setup_ok == 1, f"{setup_ok}/1"),\n', '')
p = os.path.join(root, "corpus/evidence/round87/", "E8_legdeleted.py")
open(p, "w", encoding="utf-8").write(v)
r = subprocess.run([sys.executable, "-B", p, "--root", root, "--repo", repo, "--work", work], capture_output=True, text=True)
print("E8 delete-one-append rc=", r.returncode)
print([l for l in (r.stdout+r.stderr).splitlines() if "LEGS" in l or "GATE_RECORDS" in l or "LEG_FAIL" in l])
