# Counter06 — frozen C1 reference-candidate run

Ran the frozen `corpus/evidence/round64/c1-battery-v3.py` once against `corpus/evidence/round64/controls/ref-preflight-v3.py`, using `--jobs 2` and exclusive scratch `/fast/scratch/hyaku/chousa-r64/Counter06/work`.

Command:

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round64/c1-battery-v3.py --tool corpus/evidence/round64/controls/ref-preflight-v3.py --fleet /home/vgpnk/Projects/shokunin --work /fast/scratch/hyaku/chousa-r64/Counter06/work --jobs 2
```

Observed exit: **1**. Output is preserved in `Counter06/run.txt`. Exact summary: `CLEAN=1/1 DEFECTS=28/28 BENIGN=9/11 ZERO=3/3 BATTERY=FAIL`. All legs passed except `E12 benign FAIL rc=1 want 0` and `E13 benign FAIL rc=1 want 0`; E14 passed. D13 and E10 passed their required usage checks. No tool installed or updated.

Scratch cleanup initially hit a permission-denied error on the battery-created `corpus/knowledge`; changed permissions only within my own scratch tree and removed that tree successfully. No production, fixture, or frozen instrument files were edited.
