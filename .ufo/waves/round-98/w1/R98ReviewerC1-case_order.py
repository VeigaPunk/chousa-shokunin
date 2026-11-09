# Check battery CASE_IDS order vs actual selftest order, and CASE_IDS count.
import subprocess, sys
out = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py","--selftest"],capture_output=True,text=True)
ids = [ln.split()[1] for ln in out.stdout.splitlines() if ln.startswith("SELFTEST ")]
import ast
src = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/corpus/evidence/round98/selftest-controls-r98.py").read()
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id=="CASE_IDS" for t in node.targets):
        battery = list(ast.literal_eval(node.value))
print("battery len", len(battery), "selftest len", len(ids), "equal", battery==ids)
if battery!=ids:
    print(set(battery)^set(ids))
# Check the selftest docstring claim about NO_WRITE/socket against reality: selftest reads /dev/null (r30) — parse_record opens it. r29 reads via git. Any other file open? Only __file__ for hash oracle (not in real tool). The real tool opens no other path (mem fixtures are dicts). Verified via audit hook Popen count=2 and strace execve.
# Check plans/round-98.md for pre-freeze P0 description consistency
print(open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/plans/round-98.md").read()[:2000])
