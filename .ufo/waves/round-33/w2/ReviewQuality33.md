# ReviewQuality33 — QUALITY criteria 36–39 operability review

Scope: run each check named in `corpus/QUALITY.md` criteria 36–39 exactly as written; confirm it
fails on the cited failing evidence and passes on the cited passing evidence; flag any check that
cannot fail, cannot be run as written, or cites a wrong path/line. Lane tip `0fb300b5`. All commands
run from lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin` on 2026-10-23. Read-only; no lane
files touched, no `c1-count-v2.py` runs (not required by this item).

## Q36 — fixture metadata cannot stand in for reading (QUALITY.md:275-284)

Check as written: committed control receipts' `matched` must be below `total`. This is a field
comparison over committed JSON, not a script — runnable as stated.

Failing evidence (cited `matched=132/132`):
- `.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s32320021.json` → `matched=132, total=132`,
  `seed=32320021`, `counter_sha256=8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`,
  `label=EXEMPT_AUDIT_MATCH=132/132`, `predicate_holds=true`.
- `control-metadata-s32320022.json` → identical, `seed=32320022`.
- `sha256sum corpus/evidence/round32/c2-count-v2.py` = `8ec1a1ed…23c8a` — receipts are the round-32
  counter v2 as cited. `matched == total` → check FAILS on this evidence, as claimed.

Passing evidence (cited 96/132, 95/132, 78/132):
- `.ufo/waves/round-33/w1/ExecD1CounterV3/receipts/v3-metadata-s7331.json` → `matched=96, total=132`.
- `v3-metadata-s7332.json` → `matched=95, total=132`.
- `v3-noreader-s7331.json` and `v3-noreader-s7332.json` → `matched=78, total=132`.
- All carry `counter_sha256=6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa` =
  `sha256sum corpus/evidence/round32/c2-count-v3.py`. The v3 metadata receipts even reuse the same
  control gate (`gate_sha256=79c4f44e…`) that scored 132/132 under v2 — the counter, not the control,
  changed. Sibling controls also below total: `v3-inode-s7331` 95/132, `v3-mtime-s7331` 96/132.
Result: fails on cited failing evidence, passes on cited passing evidence. Paths and values exact.
Residual: no runnable check command is named; "matched below total" is a manual read — operable but
not automatable as written.

## Q37 — every numeric tally carries its counting command (QUALITY.md:286-291)

Check as written: `python3 corpus/evidence/round33/d2-census.py --lane .` — ran verbatim, exit 0.
Output line: `C1 receipts on gate 10f2fe12: 21` — exactly the cited string. Full census: 255 C1
receipts in round-32, per-gate breakdown printed.
- Cited failing tally: `SCORECARD.md:1817` says "committed receipts on landed gates: `10f2fe12`
  ×18" — disagrees with 21 → check fails on it.
- Cited spot-check: `corpus/lessons/round-32-verifier-spotcheck.md:70` says "20 receipt files" —
  also disagrees; QUALITY's parenthetical (extra receipts written after the tally) is consistent
  with the census's utc ordering (21st receipt 07:56:21Z).
Result: runs as written, correct path, fails on the cited tally, and the cited output matches.
Residual: `--lane .` counts the live tree; the number grows as receipts land (21 today vs the
spot-check's 20), so the check's target value is time-dependent — that is the criterion's point.

## Q38 — battery output starts with its revision header (QUALITY.md:293-298)

Check as written:
`awk '/^=== RUN/{exit} /gate_sha256=/{g=1} /lane_revision=/{r=1} END{print (g&&r)?"HEADER_OK":"HEADER_MISSING"}' <battery.out>`
- `.ufo/waves/round-32/measure/final/battery.out` → prints `HEADER_MISSING`. Verified for the right
  reason: `grep -n '=== RUN\|gate_sha256=\|lane_revision='` on that file returns nothing — the header
  is absent entirely, not merely misplaced.
- `.ufo/waves/round-33/measure/battery-candidate/battery.out` → prints `HEADER_OK`; header lines at
  `:3 lane_revision=eb179ec3…` and `:5 gate_sha256=52f07c74…`, first `=== RUN` at line 19.
Result: fails on failing evidence, passes on passing evidence, paths correct.
Residual: `awk` exits 0 either way — the verdict is the stdout token, so a consumer must compare
the string, not the exit code; also a file whose keys sit anywhere before the first `=== RUN` (not
necessarily at the top) passes, matching the criterion's "before its first result row" wording.

## Q39 — seats signal only processes they recorded (QUALITY.md:300-306)

Check as written: `bash corpus/evidence/round33/no-name-signals.sh <wave dir>` (script sha256
`453388d0…b95c`).
- `bash corpus/evidence/round33/no-name-signals.sh .ufo/waves/round-32` → exit 1, RESULT DIRTY,
  one hit: `HIT .ufo/waves/round-32/w2/RerunC1b.md:31 [doc; pkill]` — cited location and token
  (`pkill -x sleep`) confirmed; `RerunC1b.md:31` contains the admission "My cleanup `pkill -x sleep`
  in an early probe also killed 3 sibling `sleep` processes".
- `bash corpus/evidence/round33/no-name-signals.sh tools/` → exit 0, CLEAN, 0 hits / 2 candidate
  files.
- `--exclude` support exists (`no-name-signals.sh:53,72-74,186`); `[doc]` classification at `:186`.
Result: fails on failing evidence (exit 1 at cited file:line), passes on `tools/` (exit 0).
Residual: the only failing hit is `[doc]`-class prose quoting the violation; per the criterion it
stays DIRTY until a human passes `--exclude`, so the check errs dirty on reports that document their
own breach — documented behavior, not a defect.

## Verdict

HOLDS for the scoped item. All four checks (Q36–Q39) run as written from the lane root; each fails
on its cited failing evidence (132/132 receipts, ×18 vs 21, HEADER_MISSING, exit 1 on RerunC1b.md:31)
and passes on its cited passing evidence (96/95/78 of 132, HEADER_OK, exit 0 on tools/). Every cited
path, line number, script hash and output token verified against the working tree. No check is
incapable of failing; no wrong path or line found.

Residual risks: (1) Q36 and Q38's verdicts are manual token reads, not exit codes — automation must
compare strings; (2) Q37's census number is live and will drift upward as receipts land — matches
the criterion's intent but means today's 21 is not frozen; (3) Q39's doc-class hits keep a wave
DIRTY until adjudicated — intentional per the rule text.

No tools installed. Receipts/artifacts: none beyond this report (all evidence is committed lane
bytes; commands quoted above, all exit codes recorded).
