# K3 harm: verify output must not differ from base. Check receipts + re-run quickly on 4 fixtures (no-regression battery already runs R95 regression, but do an independent check).
import subprocess, sys, os
repo="/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo"
base="98b8177c1e8b39cdf1167928e4f5d609f6fa81b6"
# Extract base tool
base_src = subprocess.run(["git","-C",repo,"show",f"{base}:tools/search-rerun.py"],capture_output=True,text=True).stdout
open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/base-tool.py","w").write(base_src)
for rec in ["corpus/fixtures/search-rerun-r95.md","corpus/knowledge/search-peer-review-dedup-r96.md","corpus/knowledge/press-checklist-questions-r97.md","corpus/knowledge/press-2015-statement-questions-r98.md"]:
    for strict in [[], ["--strict"]]:
        r1 = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/base-tool.py","verify",rec,"--root",repo]+strict,capture_output=True,text=True)
        r2 = subprocess.run([sys.executable,"-B",os.path.join(repo,"tools/search-rerun.py"),"verify",rec,"--root",repo]+strict,capture_output=True,text=True)
        print(rec, strict, "rc", r1.returncode, r2.returncode, "out_same", r1.stdout==r2.stdout, "err_same", r1.stderr==r2.stderr)
    print("---")
