# Counter02 — frozen C2 v2 matrix

Executed the frozen C2 runner against the requested candidate checker.

- Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c2-mutrun.py --target /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/claims-audit-v2.py --matrix v2 --work /fast/scratch/hyaku/chousa-r64/Counter02/work`
- Exit: `1`.
- Result: `AUDIT_MUTANTS_KILLED=9/12`; this does **not** meet the frozen C2 target of 12/12. A07, A10, and A11 survived. All other listed mutants were killed. Stderr was empty.
- Exact captured output: `evidence/stdout.txt`, `evidence/stderr.txt`, and `evidence/exit.txt`.
- Tool installation: none.
- Scratch: `/fast/scratch/hyaku/chousa-r64/Counter02/` removed after the run.

This is an observed frozen-matrix miss, not a modification or reinterpretation of the frozen claim. No production/instrument/claim/counter files were changed.