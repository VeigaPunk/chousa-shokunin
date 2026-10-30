# Counter01 — frozen C2 v1 matrix

Executed the frozen matrix against the frozen v1 target. No instrument or production files were changed.

Command (from the seat scratch directory):

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c2-mutrun.py --target /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/claims-audit.py --matrix v1 --work /fast/scratch/hyaku/chousa-r64/Counter01/work
```

Observed exit: **1**. Complete stdout, stderr, and exit code are retained alongside this report as `c2-v1.stdout`, `c2-v1.stderr`, and `c2-v1.exit`.

Survivors: **A05, A06, A07, A08, A10, A11**. Killed: A01, A02, A03, A04, A09, A12. Summary: `AUDIT_MUTANTS_KILLED=6/12`.

The observed stdout matches the frozen claim's stated v1 survivor list and 6/12 result. Stderr was empty. Scratch `/fast/scratch/hyaku/chousa-r64/Counter01/` was removed after the run. No tools were installed or updated.
