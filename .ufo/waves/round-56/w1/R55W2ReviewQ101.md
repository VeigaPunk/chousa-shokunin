# R55W2ReviewQ101 — QUALITY 101 review

## Findings
No actionable defect found in QUALITY 101 (`corpus/QUALITY.md:945`). Its stated offsets, drift/count observations, hook result and control score reproduce; the Check runs successfully and its RESTATE control fails as claimed.

## Re-derivation
Copied the pinned reader with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show dba605deb5cd5ed4874e0e3c39ba24737409cd80:tools/capture-text.py > $S/ct.py`. Ran `python3 $S/ct.py <raw> --locate '<phrase>'` for the six S101 `correction:` phrases in `SCORECARD.md`, Round 54 pointer corrections. Each returned `LOCATED count=1 offset=N`:

```
old -> corrected / located: 11170 -> 11972; 11205 -> 12007;
11993 -> 12795; 12161 -> 12963; 13247 -> 14049; 34374 -> 25123
```

Thus the phrase at old anchor 11993 (`本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。`) is at 12795; the phrase at 12161 (`文献类型及载体类型标志；`) is at 12963. Drift from the old offsets is `+802,+802,+802,+802,+802,-9251`: +802 repairs five anchors, and no one constant repairs all six. The corrected offsets equal all six locate results.

On the captured raw bytes (`6dc68fd6b32ce9c8dfcebce8.raw`), Python `decode('utf-16le', errors='replace')` counted 18,451 C0 code points; excluding tab/LF/CR counted 18,242 (excluding tab/LF alone: 18,431). The copied defined-form tool output was 27,012 characters, 0 U+FFFD, and 469 C0 characters; all 469 were LF. This supports QUALITY 101's exclusions and its “469 LFs and nothing else.”

Directly repeated the BASE round-54 hook probe in scratch: `ctypes.CDLL(None).system(('printf SPAWNED > ' + marker).encode())` yielded `rc=0 marker='SPAWNED'` (no stderr). `corpus/evidence/round54/controls/c1-controls.txt` has `## shell` → `LEGS=1/6`; current receipt equals the BASE receipt. The separate forge `LEGS=0/6` is reported in `.ufo/waves/round-54/w2/R54W2ExecQualityChecks.md`, row 98 / its ran output.

## Check and anchor review
Ran the full Check with its required scratch work directory:

```
python3 corpus/evidence/round55/c3-count.py --work $S/w1
E05 OK
E06 OK
E07 OK
E09 OK
E10 OK
ERRATA=11/11 MISSING=0 ANCHOR=0 WRONG=0
C3=PASS
EXIT=0
```

The remaining E01-E04, E08, E11 also printed `OK`. Separately ran `controls/build-c3-controls.py $S/ctl`, then scored `$S/ctl/restate` with `c3-count.py --root ... --work $S/w2`: it printed `WRONG` for E01-E11, `ERRATA=0/11 MISSING=0 ANCHOR=0 WRONG=11`, `C3=FAIL`, exit 1. In particular all five QUALITY-targeted errata E05/E06/E07/E09/E10 print `WRONG`, as claimed by “Shown able to fail”; the filed receipt `corpus/evidence/round55/controls/c3-controls.txt` agrees.

Compared the full eleven erratum anchor strings from `SCORECARD.md`, “Round 55 statement errata,” against the QUALITY 101 paragraph: none occurs there. Each of the five QUALITY-targeted anchors occurs exactly once in `QUALITY.md`; the full counter reports `ANCHOR=0`.

VERDICT: QUALITY 101 survived this review; all requested numbers and the Check/RESTATE claims were reproduced.