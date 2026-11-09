# Q6: does the battery read the 37 mutants, r97 battery literals, r96 set from committed BASE bytes faithfully?
# Battery lines 193-199: reads probe/base/r97/r96 via `git -C root show BASE:path` where BASE="98b8177...". Verify those files at BASE match F (R98 didn't change them, but verify no cherry trick).
import subprocess
base="98b8177c1e8b39cdf1167928e4f5d609f6fa81b6"
for p in [".ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt","tools/search-rerun.py","corpus/evidence/round97/selftest-controls-r97.py","corpus/evidence/round96/selftest-controls-r96.py"]:
    a = subprocess.run(["git","-C","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo","show",f"{base}:{p}"],capture_output=True,text=True)
    b = subprocess.run(["git","-C","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo","show",f"aac826848dda5029ba459568b29d9a92176dc2b6:{p}"],capture_output=True,text=True)
    print(p, "rc", a.returncode, b.returncode, "same", a.stdout==b.stdout, "len", len(a.stdout))
# Check the r97 battery chain: battery reads R97_BATTERY at BASE (round98's BASE). r97_lits = literal(r97_src, ...) for BASE/MUTPROBE/EXCLUDED/SENTINEL/RESIDUE. The r97 battery's BASE is c8087ac (round96 landing). Battery then reads git show r97_BASE:MUTPROBE (the R96 probe), NOT the R97 probe. So R96 probe read is: git show c8087ac:.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt. Verify that object exists and equals the R98-BASE version.
c = subprocess.run(["git","-C","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo","show","c8087ac529003e667505bcc624f9a7bde0cffbce:.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt"],capture_output=True,text=True)
d = subprocess.run(["git","-C","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo","show","98b8177c1e8b39cdf1167928e4f5d609f6fa81b6:.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt"],capture_output=True,text=True)
print("R96 probe c8087ac==R98BASE", c.stdout==d.stdout, "len", len(c.stdout))
# Prior set construction (battery lines 228-230): prior = {r96probe mutants if not in EXCLUDED}; update SENTINEL; update RESIDUE. EXCLUDED from r97 battery = {n08...}. So prior = 29 (r96 probe 30 minus n08) + 2 sentinel + 3 residue = 34. Battery reported PRIOR_R97_KILLED=34/34. But the R97 battery's own EXTERNAL_KILLED leg at F had n=34 too (29+2+3). Consistent.
# R96 battery leg: literal(reads["r96"], "MUTANTS") where reads["r96"] is round96 battery at R98BASE. MUTANTS is a dict of 23 (verified). Battery reported R96_MUTANTS_KILLED=23/23. But note the battery calls literal twice (line 234) — once for scoring, once for the tally denominator. Both re-parse the same string. Deterministic.
# KILL_REQUIRED denominator: required = sorted(set(external)-set(NAMED_SURVIVORS)); external from R97 probe MUTANTS (37). required=35. Battery reported 35/35.
# One risk: battery reads R97_BATTERY and R96_BATTERY at R98BASE, but the CLAIM says "the round-97 battery's 34 and the round-96 battery's 23 mutants". The r97 battery file at R98BASE is byte-identical to at F (R98 didn't touch it). Verify r96 battery file identical too, and check the r97 battery hasn't been edited between its own F and now — not needed; battery reads at BASE so even if F altered it, battery uses BASE. That's faithful-to-BASE but could silently diverge from F if someone edited those batteries in the R98 diff. The diff stat earlier showed R98 diff does NOT touch round97/round96 battery files. Confirmed via diff --stat (20 files, none in round96/97 battery dirs except the probe which is read-only). Let me confirm:
import subprocess as sp
diff = sp.run(["git","-C","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo","diff","98b8177c1e8b39cdf1167928e4f5d609f6fa81b6","aac826848dda5029ba459568b29d9a92176dc2b6","--name-only"],capture_output=True,text=True)
print(diff.stdout)
