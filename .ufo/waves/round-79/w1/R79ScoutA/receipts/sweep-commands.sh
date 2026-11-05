#!/bin/sh
# R79ScoutA sweep commands, exactly as run against the 13 subjects
# (copied to $S/scratch/subjects/ from the battery's POSITIVES/FORGERS lists).
set -e
D="SUBJECTS_DIR"
cd "$D"
echo "===== 1. getattr/setattr/hasattr/delattr/globals/locals/vars/eval/exec ====="
grep -nE '\b(getattr|setattr|hasattr|delattr|globals|locals|vars|eval|exec)\s*\(' *.py || echo "NO MATCH"
echo "===== 2. match/case ====="
grep -nE '^\s*(match|case)\b' *.py || echo "NO MATCH"
echo "===== 3. f-string debug {expr=} (conversion=114 marks the repr specifier) ====="
python3 - <<'PY'
import ast, pathlib
for p in sorted(pathlib.Path('.').glob('*.py')):
    t = ast.parse(p.read_text())
    for n in ast.walk(t):
        if isinstance(n, ast.JoinedStr):
            for i, part in enumerate(n.values):
                if isinstance(part, ast.Constant) and isinstance(part.value, str) \
                   and part.value.endswith("="):
                    nxt = n.values[i+1] if i+1 < len(n.values) else None
                    if isinstance(nxt, ast.FormattedValue) and nxt.conversion == 114:
                        print(f"DEBUG-SPECIFIER {p.name}:{n.lineno}: {part.value!r}")
print("(end of debug-specifier scan)")
PY
echo "===== 4. __all__ ====="
grep -nE '__all__' *.py || echo "NO MATCH"
echo "===== 5. importlib / __import__ ====="
grep -nE '\b(importlib|__import__)\b' *.py || echo "NO MATCH"
echo "===== 6. global/nonlocal ====="
grep -nE '^\s*(global|nonlocal)\b' *.py || echo "NO MATCH"
echo "===== 7. __name__ == '__main__' ====="
grep -nE '__name__\s*==\s*["'"'"']__main__["'"'"']' *.py || echo "NO MATCH"
echo "===== 8. decorators ====="
grep -nE '^\s*@[A-Za-z_]' *.py || echo "NO MATCH"
echo "===== 9. star imports ====="
grep -nE '^\s*from\s+[A-Za-z0-9_.]+\s+import\s+\*' *.py || echo "NO MATCH"
echo "===== 10. **-splat calls ====="
grep -nE '\*\*' *.py || echo "NO MATCH"
echo "===== 11. __file__ / sys.argv ====="
grep -nE '__file__|sys\.argv' *.py || echo "NO MATCH"
echo "===== 12. class definitions / self. attribute access ====="
grep -nE '^\s*class\s|\bself\.' *.py || echo "NO MATCH"
echo "===== 13. __doc__ ====="
grep -nE '__doc__' *.py || echo "NO MATCH"
