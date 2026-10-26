# R52MutCapture — C1 tool mutation test (wave 1)

Seat: R52MutCapture. Target: frozen C1 counter `corpus/evidence/round52/c1-count.py`
(detector) vs `tools/capture-text.py` (program under test). Lane tool copied to
scratch (read-only lane); mutants built in scratch; counter run read-only with
`TMPDIR` = scratch. Python 3.14.8. Fixed seed `--seed 20261026` for every run
(identical packages across runs; differences caused by the mutant alone). REAL
leg pin verified: `.qcache/3a8b45977cd111e45e3980a5.raw` sha256
`16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` (matches
counter's REAL_SHA).

## Baseline (pristine copy `capture-text.py`, sha256 3986a971…)

Command:
```
TMPDIR=/fast/scratch/hyaku/chousa-r52/R52MutCapture python3 \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/c1-count.py \
  --tool /fast/scratch/hyaku/chousa-r52/R52MutCapture/capture-text.py --seed 20261026
```
Output:
```
PARAS=PASS ok
RUNS_ENTITIES=PASS ok
REVISIONS=PASS ok
LAYOUT=PASS ok
ALTCONTENT=PASS ok
MAIN_PART=PASS ok
LOCATE=PASS ok
REFUSE=PASS ok
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS
```
exit 0. Baseline healthy (not inconclusive).

## Mutants (one per class; each = single behavioral change in a copy)

| # | class | change applied |
|---|-------|----------------|
| 1 | fixed member word/document.xml | `main_part` returns `"word/document.xml"` unconditionally before the rels loop |
| 2 | no mc:Fallback skip | `fallback` never increments/decrements (`+= 0` / `-= 0`) |
| 3 | w:delText emitted | end-handler gains `elif el.tag == W+"delText": out.append(el.text or "")` |
| 4 | w:instrText emitted | end-handler gains `elif el.tag == W+"instrText": out.append(el.text or "")` |
| 5 | every w:tab emitted | start condition: tab bypasses parent `w:r` check (`el.tag == W+"tab" or (stack and stack[-1]==W+"r")`) |
| 6 | no newline at w:p end | `elif el.tag == W+"p": out.append("\n")` → `pass` |
| 7 | newline only at top-level w:p | newline only when w:p's parent is `w:body` (`top_p[id(el)] = bool(stack) and stack[-1]==W+"body"`) |
| 8 | --locate offset off by one | prints `text.find(a.locate) + 1` when found |
| 9 | --locate exit 0 on count 2 | `return 0 if n >= 1 else 1` |
| 10 | non-zip not refused | `if not zipfile.is_zipfile(path): return ""` (empty text, exit 0) |
| 11 | REFUSED on stdout | `print(f"REFUSED {e}")` (drop `file=sys.stderr`) |
| 12 | entities not decoded | w:t text re-escaped (`&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`) |
| 13 | w:cr ignored | `RUN_BREAKS` drops `W+"cr"` |
| 14 | leading '/' not stripped | `lstrip("/")` removed from target normalization |

## Detector runs per mutant (same command as baseline, `--tool mutantNN.py`)

```
===== mutant01 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=FAIL text differs at 0 (got 21 chars, want 25)
LOCATE=PASS REFUSE=FAIL norel not refused REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=7/9 C1=FAIL rc=1
===== mutant02 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=FAIL text differs at 38 (got 38 chars, want 55) MAIN_PART=PASS LOCATE=PASS
REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=12314
LEGS=8/9 C1=FAIL rc=1
===== mutant03 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=FAIL text differs at 8 (got 43 chars, want 33)
LAYOUT=PASS ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant04 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=FAIL text differs at 8 (got 73 chars, want 33)
LAYOUT=PASS ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 10293) chars=20979
LEGS=8/9 C1=FAIL rc=1
===== mutant05 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=FAIL text differs at 0 (got 94 chars, want 74)
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 9009) chars=19695
LEGS=8/9 C1=FAIL rc=1
===== mutant06 =====   PARAS=FAIL text differs at 13 (got 69 chars, want 72)
RUNS_ENTITIES=FAIL text differs at 8 (got 94 chars, want 99)
REVISIONS=FAIL text differs at 23 (got 62 chars, want 65)
LAYOUT=FAIL text differs at 19 (got 57 chars, want 65)
ALTCONTENT=FAIL text differs at 18 (got 79 chars, want 83)
MAIN_PART=FAIL text differs at 14 (got 14 chars, want 15)
LOCATE=FAIL once=(0, 1, 89) want (0,1,91) absent=(1, 0, -1) twice=(1, 2, 0)
REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8477) chars=18463
LEGS=2/9 C1=FAIL rc=1
===== mutant07 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=FAIL text differs at 25 (got 66 chars, want 74)
ALTCONTENT=FAIL text differs at 36 (got 56 chars, want 57) MAIN_PART=PASS LOCATE=PASS
REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8743) chars=19026
LEGS=7/9 C1=FAIL rc=1
===== mutant08 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=FAIL once=(0, 1, 22) want (0,1,21) absent=(1, 0, -1) twice=(1, 2, 1)
REFUSE=PASS REAL=FAIL rc=0 count=1 locate=(0, 1, 8997) chars=19682
LEGS=7/9 C1=FAIL rc=1
===== mutant09 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=FAIL once=(0, 1, 21) want (0,1,21) absent=(1, 0, -1) twice=(0, 2, 0)
REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant10 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=FAIL bytes not refused
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant11 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=FAIL bytes not refused
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant12 =====   PARAS=PASS RUNS_ENTITIES=FAIL text differs at 6 (got 169 chars, want 135)
REVISIONS=PASS LAYOUT=PASS ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS
REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant13 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=FAIL text differs at 17 (got 73 chars, want 74)
ALTCONTENT=PASS MAIN_PART=PASS LOCATE=PASS REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
===== mutant14 =====   PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=PASS LAYOUT=PASS
ALTCONTENT=PASS MAIN_PART=FAIL rc=2 LOCATE=PASS REFUSE=PASS
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=8/9 C1=FAIL rc=1
```

## Kill matrix (F = leg failed; all runs `C1=FAIL`)

```
        PARAS RUNS REV LAY ALTC MAIN LOC REF REAL  verdict
M01  .   .    .   .   .    F   .  F  .    KILLED
M02  .   .    .   .   F    .   .  .  .    KILLED
M03  .   .    F   .   .    .   .  .  .    KILLED
M04  .   .    F   .   .    .   .  .  .    KILLED
M05  .   .    .   F   .    .   .  .  .    KILLED
M06  F   F    F   F   F    F   F  .  .    KILLED
M07  .   .    .   F   F    .   .  .  .    KILLED
M08  .   .    .   .   .    .   F  .  F    KILLED
M09  .   .    .   .   .    .   F  .  .    KILLED
M10  .   .    .   .   .    .   .  F  .    KILLED
M11  .   .    .   .   .    .   .  F  .    KILLED
M12  .   F    .   .   .    .   .  .  .    KILLED
M13  .   .    .   F   .    .   .  .  .    KILLED
M14  .   .    .   .   .    F   .  .  .    KILLED
```

## Survivors

None. All 14 mutant classes are detected by the frozen counter: 13 by a
generated-package leg, and every mutant that touches text shape also perturbs
the pinned NIPH REAL leg (same 19682-char text, `--locate` offset 8996) where
its defect is present in that document (M02 chars=12314, M04 chars=20979, M05
chars=19695, M06 chars=18463, M07 chars=19026, M08 offset=8997). No generator
change is required to kill any class; for completeness, the weakest pair is
M10/M11, caught only by the REFUSE leg — a sharper variant would also return
exit 0 on `norel`/`dangling` cases (drop `main_part`'s Refused raises), and the
counter would still catch both via REFUSE.

## Notes

- M07's first construction crashed (`NameError: top_p`, rc=1 on every text leg)
  because the insertion anchor was missed; the mutant was regenerated with the
  insertion verified (`a1 count: 1`, `top_p` at lines 75/79/92) and re-run.
  The crashed variant was also killed; the regenerated variant is the one in
  the matrix.
- The counter was run read-only; only its output was captured. TMPDIR pointed
  at scratch for all runs.

## Restoration evidence

Scratch pristine `capture-text.py` was never modified in place; each mutant is a
separate file. Before/after hashes:
```
before: 3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1  tools/capture-text.py (lane)
before: 3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1  scratch/capture-text.py
after:  3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1  tools/capture-text.py (lane)
after:  3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1  scratch/capture-text.py
```
Lane repo untouched (only this report written). Scratch removed on exit.

VERDICT: built 14 single-class mutants of capture-text.py; all 14 killed by the frozen C1 counter (0 survivors), baseline 9/9 PASS.
