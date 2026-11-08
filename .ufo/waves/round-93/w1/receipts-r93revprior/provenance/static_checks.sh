#!/bin/bash
# Seat R93RevPrior static checks — committed bytes only.
S=/fast/scratch/hyaku/chousa-r93/R93RevPrior
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
R="$S/repo"
F=b7241252c2358613d3b22b7d0454d98c56dab373
C=754b62fb6adc60e44e12375af5461a0ebe302994
out="$S/out-static-checks.txt"
exec > "$out" 2>&1

echo "# seat R93RevPrior static checks; tree = committed C2 clone $R (HEAD $C)"
echo
echo '$ grep -c receipt_pins corpus/evidence/round92/control-driver-r92.py'
n=$(grep -c receipt_pins "$R/corpus/evidence/round92/control-driver-r92.py"); echo "$n (grep rc=$?)"
echo
echo '$ grep -c "PIN_DISK_MISMATCH\|RECEIPT_MISMATCH\|RECEIPT_UNPINNED\|RECEIPT_PINS" corpus/evidence/round92/control-driver-r92.py'
n=$(grep -c 'PIN_DISK_MISMATCH\|RECEIPT_MISMATCH\|RECEIPT_UNPINNED\|RECEIPT_PINS' "$R/corpus/evidence/round92/control-driver-r92.py"); echo "$n"
echo
echo '$ grep -c Q_WSQUOT corpus/evidence/round92/curation-r92.py'
n=$(grep -c Q_WSQUOT "$R/corpus/evidence/round92/curation-r92.py"); echo "$n"
echo
echo '$ grep -n "DEFAULT_" corpus/evidence/round92/control-driver-r92.py'
grep -n "DEFAULT_" "$R/corpus/evidence/round92/control-driver-r92.py"
echo
echo '$ grep -n "def pin_report|wanted[rel_for|base += [(rel_for(root, os.path.join(receipts|escapes base" corpus/evidence/round92/control-driver-r92.py'
grep -n "def pin_report\|wanted\[rel_for(root, expected)\]\|wanted\[rel_for(root, pins_path)\]\|base += \[(rel_for(root, os.path.join(receipts\|escapes base" "$R/corpus/evidence/round92/control-driver-r92.py"
echo
echo '$ grep -n "EXPECTED_OTHERS = " corpus/evidence/round92/skill-tally-r92.py'
grep -n "EXPECTED_OTHERS = " "$R/corpus/evidence/round92/skill-tally-r92.py"
echo
echo '$ grep -n "PASS (215 cases, 0 skipped)" SKILL.md'
grep -n "PASS (215 cases, 0 skipped)" "$R/SKILL.md"
echo
echo '$ grep -n "### Round27" SKILL.md'
grep -n "### Round27" "$R/SKILL.md"
echo
echo '$ grep -n "PASS (283 cases, 0 skipped)" SKILL.md | tail -1'
grep -n "PASS (283 cases, 0 skipped)" "$R/SKILL.md" | tail -1 | cut -c1-110
echo
echo "\$ git -C $R cat-file -e $F:corpus/evidence/round93/controls/receipts/c2-prior-landing.txt"
git -C "$R" cat-file -e "$F:corpus/evidence/round93/controls/receipts/c2-prior-landing.txt" && echo "exists-at-F2 (rc=0)"
echo
echo "\$ git -C $R diff --stat $F $C"
git -C "$R" diff --stat "$F" "$C"
echo
echo "\$ git -C $L status --porcelain corpus/evidence/round93/evidence-before"
git -C "$L" status --porcelain corpus/evidence/round93/evidence-before
echo
echo "\$ git -C $L log --all --oneline -- 'corpus/evidence/round93/evidence-before/*'"
git -C "$L" log --all --oneline -- 'corpus/evidence/round93/evidence-before/*'
echo "(commit count: $(git -C "$L" log --all --oneline -- 'corpus/evidence/round93/evidence-before/*' | wc -l))"
echo
echo "\$ git -C $R ls-tree -r --name-only HEAD corpus/evidence/round93/evidence-before"
git -C "$R" ls-tree -r --name-only HEAD corpus/evidence/round93/evidence-before
echo "(tree count at C2: $(git -C "$R" ls-tree -r --name-only HEAD corpus/evidence/round93/evidence-before | wc -l))"
echo
echo '$ ls -A corpus/evidence/round93/evidence-before (lane working tree)'
ls -A "$L/corpus/evidence/round93/evidence-before"
echo
echo '$ cat corpus/evidence/round93/evidence-before/.keep'
cat "$L/corpus/evidence/round93/evidence-before/.keep"
echo
echo "\$ git -C $R ls-tree -r --name-only HEAD corpus/evidence/round92/evidence-before"
git -C "$R" ls-tree -r --name-only HEAD corpus/evidence/round92/evidence-before
echo
echo '$ python3 -B shape-probe (r92 vs r93 q_shape_violation on the same cell)'
python3 - <<'PY'
import importlib.util
R = "/fast/scratch/hyaku/chousa-r93/R93RevPrior/repo"
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r92 = load(R + "/corpus/evidence/round92/curation-r92.py", "a")
r93 = load(R + "/corpus/evidence/round93/curation-r93.py", "b")
for cell in ['" "', '"\t"', '""']:
    print("  cell=%r r92=%r r93=%r" % (cell, r92.q_shape_violation(["Q2", "S214", cell]),
                                       r93.q_shape_violation(["Q2", "S214", cell])))
PY
echo
echo "# done"
