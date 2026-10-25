# ScribeGatesR47 — round 47 wave 1, Gates row for the round-47 counters

seat: scribe `L1Chousa47.ScribeGatesR47` · date 2026-10-25 · read-only on the lane
item: draft SKILL.md `## Gates` rows for `corpus/evidence/round47/c1-count.py`,
`c2-count.py`, `c3-count.py` with the frozen targets (`corpus/evidence/round47/claims.md`)
and controls (`corpus/evidence/round47/controls/`); run each once read-only on a /tmp
archive; prove with the round-47 C2 counter that the paths leave UNREGISTERED.

## Verdict

One row (one instrument family, matching the `chousa round-46 counters` convention at
`SKILL.md:118`). It has 8 cells, starts with `| ` and ends with ` |`. Its entry cell names all
three counters by full repo-relative path, and its verdict map states exit `0`/`1`/`2` with
the exact PASS prints. With the row inserted after `SKILL.md:118` in a /tmp copy, the
round-47 C2 counter drops `UNREGISTERED` from 25 to 22 with `DANGLING=0`, and the three
round-47 paths no longer print as `UNREGISTERED_PATH`. The round-46 C2 counter still prints
`C2=PASS` on that copy. The row is NOT applied to the lane, because this seat writes only
this report.

## Inputs (resolvable)

- lane `master` = HEAD = `a15610a59aaeaf43b79ccc650acee4bd4da00341`; freeze `22a44b8`.
- sha256 (archive): c1 `6d39dce5a925d8557449ef3df08bc9dac749fe043c5478dc127973bbc23d0cc7`,
  c2 `36b3934eda5b8ccd569bf577db51f1ac5286463ba8104ec43d777b72658336d1`,
  c3 `ce93fe29bc9df508af9d3119ef6a5c5be5320752ed0bd78a31d7e53fe430c956`,
  SKILL.md `0fcdc442481b117bbcdb431966ebf06a641232481ec2a3d3140f5d89cf3fd2d1`.
- Gates header `SKILL.md:78`; 36 rows before; Gates section `SKILL.md:76`–`509`.
- Exit paths read from source: c1 `main()` returns 2 only on missing fixture dir
  (`C1=FAIL no-fixtures`), 1 on `FIXTURES_CHANGED=` or any short leg; c2 returns 2 on
  `R46_INSTRUMENT=absent|changed` (pin `R46_SHA=f93cb107…`, `FLOOR = 92` at c2-count.py:51–52);
  c3 returns only `0 if ok else 1` (c3-count.py:209), so exit 2 is argparse usage alone.

## Commands run (verbatim, decisive lines)

```
$ T=/tmp/chousa-r47-ScribeGatesR47; git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive master | tar -x -C $T/lane
$ python3 corpus/evidence/round47/c1-count.py          (cwd $T/lane)
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS
exit=0
$ python3 corpus/evidence/round47/c2-count.py --list
UNREGISTERED_PATH … (22 pre-round-47 paths, identical to controls/c2-before.txt tree A)
UNREGISTERED_PATH corpus/evidence/round47/c1-count.py
UNREGISTERED_PATH corpus/evidence/round47/c2-count.py
UNREGISTERED_PATH corpus/evidence/round47/c3-count.py
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=36
REGISTERED=67/92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL
exit=1
$ python3 corpus/evidence/round47/c3-count.py
ENTRIES=0/2 CITES_BOUND=0/6 QUOTE_ROWS=0 (min 12) SPAN_IDS=0/6 QUOTES_IN_SPAN=0/0
QUOTES_IN_ENTRY=0/0 SPAN_CONTEXT=0/0 CAPTURE_BOUND=0/0 REF_ID_UNBOUND=0 ANCHOR_BOUND=0/6
INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/4 QUARANTINE_ABSENT_ADOPTED=0 C3=FAIL
exit=1
$ python3 corpus/evidence/round47/c3-count.py --lane-only
(same legs, CAPTURE_BOUND=skipped) C3=FAIL
exit=1
```

C1 at the landing equals the frozen target. C2 equals the frozen "before" (`ENTRY_POINTS=92
UNREGISTERED=25 DANGLING=0 MISMATCHES=25`). C3 equals `controls/c3-before.txt`. Both C2 and
C3 FAIL before landing, as expected.

Row inserted after line 118 of `$T/lane/SKILL.md` (awk on the scratch copy; row file sha256
`24da6a727b23…`, patched copy `9a67036d0a45…`). Shape check: `cells 8 starts True ends True
lines 1`, `entry has 3 counters True`, `exit codes in vmap True`.

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round47/c2-count.py --root /tmp/chousa-r47-ScribeGatesR47/lane --list
UNREGISTERED_PATH … (the same 22 pre-round-47 paths; no round47 path listed)
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=37
REGISTERED=70/92 UNREGISTERED=22 DANGLING=0 MISMATCHES=22 C2=FAIL
exit=1
$ python3 corpus/evidence/round46/c2-count.py --root /tmp/chousa-r47-ScribeGatesR47/lane
ENTRY_POINTS=84 (tools=8 counters=53 named=82) GATES_ROWS=37 REGISTERED=84/84 UNREGISTERED=0 C2=PASS
exit=0
```

The control tools named in the self-test cell (`controls/base-tool-r46.py`,
`always-exit-1.py`, `neg-word-refuser.py`) exist, so they add no DANGLING, and no entry-point
leg reaches them, so they add no UNREGISTERED. That is observed: `DANGLING=0` and
`ENTRY_POINTS` unchanged at 92.

## Row (verbatim)

```
| `chousa round-47 counters` | gate | `python3 corpus/evidence/round47/c1-count.py [--root DIR] [--tool PATH]` · `python3 corpus/evidence/round47/c2-count.py --list [--root DIR]` · `python3 corpus/evidence/round47/c3-count.py [--root DIR] [--cache DIR]` · `python3 corpus/evidence/round47/c3-count.py --lane-only` | C1 exit `0` `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` · exit `1` any leg short or a pinned fixture byte changed (`FIXTURES_CHANGED=` then `C1=FAIL`) · exit `2` `C1=FAIL no-fixtures` or argparse usage · C2 exit `0` `MISMATCHES=0 C2=PASS` with `ENTRY_POINTS` ≥ `FLOOR=92` · exit `1` `UNREGISTERED>0`, `DANGLING>0` or `ENTRY_POINTS<92` (`C2=FAIL`) · exit `2` `R46_INSTRUMENT=absent` or `R46_INSTRUMENT=changed <sha12>` (round-46 c2 counter sha256 pin) then `C2=FAIL` · C3 exit `0` `ENTRIES=2/2 CITES_BOUND=6/6 QUOTE_ROWS=n (min 12) SPAN_IDS=6/6 QUOTES_IN_SPAN=n/n QUOTES_IN_ENTRY=n/n SPAN_CONTEXT=n/n CAPTURE_BOUND=n/n REF_ID_UNBOUND=0 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=4/4 QUARANTINE_ABSENT_ADOPTED=0 C3=PASS` (n ≥ 12), `--lane-only` the same with `CAPTURE_BOUND=skipped` · exit `1` any leg short · exit `2` argparse usage only (no env branch) · all three gate; none superseded, none a probe | `corpus/evidence/round47/controls/`: `c1-before.txt` (base tool `JUNK_KILLED=0/3 CANARY=fail C1=FAIL` exit 1); `c1-controls.txt` — control tools (not gates) `corpus/evidence/round47/controls/base-tool-r46.py` `JUNK_KILLED=0/3`, `corpus/evidence/round47/controls/always-exit-1.py` `POSITIVE_PASS=0/3 R46_COUNTER=fail`, `corpus/evidence/round47/controls/neg-word-refuser.py` `POSITIVE_PASS=1/3 R46_ENTRIES=0/2`, each `C1=FAIL` exit 1; `c2-before.txt` (freeze tree `UNREGISTERED=25 MISMATCHES=25`, base archive `UNREGISTERED=22`, both `C2=FAIL` exit 1); `c2-controls.txt` — round-46 c2 counter `C2=PASS` exit 0 on base 9a9f94db where this counter prints `MISMATCHES=22 C2=FAIL` exit 1, and `corpus/QUALITY.md` emptied gives `ENTRY_POINTS=86` < `FLOOR=92` exit 1; `c3-before.txt` (every leg 0, `C3=FAIL` exit 1); `c3-controls.txt` — staged entries copied unchanged `REF_ID_UNBOUND=17 CITES_BOUND=0/6` exit 1, a forged self-consistent 12-row manifest `CAPTURE_BOUND=0/12` exit 1 in default mode | frozen claims `corpus/evidence/round47/claims.md` at freeze `22a44b8b5c923d25123a96a852c11938559bb9b2`; measured on `git archive` of lane `a15610a59aaeaf43b79ccc650acee4bd4da00341` (receipt `.ufo/waves/round-47/w1/ScribeGatesR47.md`): C1 `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0; C2 `ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) REGISTERED=67/92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL` exit 1 (target `MISMATCHES=0`); C3 both modes every leg 0, `C3=FAIL` exit 1 (target every leg full, `C3=PASS`); sha256 c1 `6d39dce5a925`, c2 `36b3934eda5b`, c3 `ce93fe29bc9d`; c2 pins round-46 counter `f93cb10795ef` and `FLOOR=92` in code; c1 pins fixture bytes of `corpus/fixtures/inference-ground-r47/` | read-only: c1 copies canary fixtures into a `tempfile` dir only; c3 reads the capture cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (skipped under `--lane-only`); no network | chousa |
```

## Findings

1. The row closes 3 of the 25 C2 mismatches. The remaining 22 are pre-round-47 paths that
   other seats own (same list as `controls/c2-before.txt` tree D). C2 stays `FAIL` until
   those 22 are registered.
2. The pinned-values cell states the C2/C3 numbers observed before landing. When C2/C3 land,
   the integrator SHOULD re-measure and replace those numbers. The frozen targets in the
   verdict map do not change.
3. Named limit (claims R47-C2): row truth is still a reader's check. The C2 counter would
   accept this row even if its verdict map were wrong. I checked the verdict map by reading
   the source exit paths cited above.
4. C3's verdict map uses `n` for the QUOTE_ROWS-derived denominators, because their value
   depends on the spans manifest that lands later. The floor `n ≥ 12` is frozen.

## Scope

Touched: this report only. Scratch `/tmp/chousa-r47-ScribeGatesR47/` was deleted.
Out of scope: applying the row to lane `SKILL.md`, and the 22 other unregistered paths.
Installs: none. No network.
