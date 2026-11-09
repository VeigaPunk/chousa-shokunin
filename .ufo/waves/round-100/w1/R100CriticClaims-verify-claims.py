# Verify claims.md numbers at F in scratch clone, checking each counting command ourselves.
import subprocess, sys, os
LANE="/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo"
def sh(cmd, **kw):
    p=subprocess.run(cmd, capture_output=True, text=True, cwd=LANE, **kw)
    return p.returncode, (p.stdout+p.stderr).strip()
for name, cmd in [
  ("gate-new", [sys.executable,"-B","tools/gate-records.py","verify","--root",".","corpus/knowledge/quotation-error-update-r100.md"]),
  ("metadata", ["bash","tools/research-gate.sh","verify-metadata","corpus/knowledge/quotation-error-update-r100.md","--root","."]),
  ("rerun", [sys.executable,"-B","tools/search-rerun.py","verify","corpus/knowledge/quotation-error-update-r100.md","--root","."]),
  ("gate-old", [sys.executable,"-B","tools/gate-records.py","verify","--root",".","corpus/knowledge/quotation-error-rates-r99.md"]),
  ("r99-controls", [sys.executable,"-B","corpus/evidence/round99/entry-controls-r99.py","--root","."]),
]:
    rc,out=sh(cmd)
    print(f"== {name} rc={rc}")
    print("\n".join(out.splitlines()[-4:]))
