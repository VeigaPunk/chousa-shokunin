# R55W2CritMistakes — attack on round-55 lesson `## Mistakes` rows 1–3

Axes attacked: operability (pointer/fix checks actually fail on the cited defect); calibration (captured-by and row-3 characterization). Frozen round-56 claims read first: `corpus/evidence/round56/claims.md` lines 14–19 and 41–49. All row targets are round-55 corrections; no round-56 predicate, target, counter, or control is proposed for change.

Scratch: `/fast/scratch/hyaku/chousa-r56/R55W2CritMistakes`; `TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`; removed at exit. No installs.

## Row 1 — pointers and shown failure survive

Pointers resolve: `corpus/lessons/round-55.md` row 1 points to the round-54 fleet report and the round-54 W2 result note/settled_by; independent closure `corpus/lessons/round-54-verifier-spotcheck.md:17-20` dates report commit 23:50:07 and W2 result 00:14, and says W2 was killed at session exit then salvaged. The direct cited failing check was run:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round55/wave-settled-check.py --round 54
SETTLED w1 results=2026-10-26T23:41:46-03:00
UNSETTLED w2 results=2026-10-27T00:22:58-03:00 after report=2026-10-26T23:50:07-03:00
WAVES=2 SETTLED=1
exit 1
```

`captured-by` accurately identifies the prompt rule and its specific gap: the rule was stated but no lane command checked it. The fix shown fails on the exact round-54 case, with exit 1 and W2-after-report; the row's round-52 passing control is cited in the row but was not rerun here. No material defect found.

## Row 2 — pointers and E08 observation survive; exact reproduction is embedded in frozen checker

Pointers resolve to round-54 lesson row 2, W2 `R54W2CritMistakes.md:12-18`, and round-55 SCORECARD erratum E08. E08's observation is not an unsupported assertion: frozen `corpus/evidence/round55/c3-count.py:34-35` defines it as `pointer-anchor-check` at BASE on a BASE mirror with both round-54 dumps removed; implementation `:162-174` archives BASE, deletes both dumps, runs the BASE pointer checker, and records its `ANCHORED=` output. I exercised the encompassing counter with an explicit empty work dir:

```text
python3 .../corpus/evidence/round55/c3-count.py --skip-slow --work <scratch>/work
E08 OK
E11 WRONG (slow item skipped)
ERRATA=10/11 MISSING=0 ANCHOR=0 WRONG=1
C3=FAIL
exit 1
```

`E08 OK` is not itself the raw BAD=9 line, but verifies the erratum's byte-exact observation against that recomputation; the exact observation is quoted in the lesson row and in W2 `R54W2CritMistakes.md:17` (`ANCHORED=7/16 UNANCHORED=9 BAD=9`). The earlier W2 report also records the controls: both dumps missing gives BAD=9; S101 alone missing BAD=6; S100 alone missing BAD=3. The row's `captured-by: none` is honest about the *original* mistake (no requirement to run a claimed shown-failure figure); the current check and E08 are the correction, not an attribution that retroactively fixes the omitted process rule. No mismatch found. The `--skip-slow` run deliberately cannot pass C3; it does confirm E08 while E11 remains untested by this invocation.

## Row 3 — the finding is real, but calling it a separate lane mistake is not established

The row points to a real defect in the round-54 supplement's *claim of isolation*: `corpus/evidence/round54/c1-supplement.py:9-11` says generated documents are outside the generation tree/no HTML or sibling; round-54 closure §6.2 (`corpus/lessons/round-54-verifier-spotcheck.md:126-130`) records the W2 `R54W2SentFinal` finding that oracle exports and generation HTML remain two directories above, allowing a non-reading echo tool to score 3/3. The closure §6.2 also separates a second W2 finding (ctypes delegate bypass, `R54W2CritC1Verdict`) and routes both as counter/instrument limits.

The round-55 row then says the *same* isolation defect was corrected: its cited C1 counter keeps expected offsets in memory, removes generation trees before candidate runs, and audits reads; W1 forge reports are named as demonstrations. `R55CritForgeEcho.md:75-81` explicitly cautions its own surrogate attempt was misconfigured and calls for a corrected rerun; `R55CritForgeReader.md:49-53` tests a distinct approximate OLE reader, which fails the exact-form gate, not the sibling-isolation defect. The strongest evidence that row 3 is a **restatement of W2's round-54 finding**, not a new mistake made by this lane in round 55, is the chronology itself: it describes the round-54 defect, cites the round-54 W2 falsifier, and presents the round-55 fix plus W1 attacks as its remedy. The row does not identify a round-55 regression or new violation. Thus its content is true and the fix is relevant, but categorizing it as one of this lesson's lane mistakes overstates provenance / duplicates the W2 finding already integrated in round 54's closure. This is a calibration defect in the lesson classification, not evidence the hook/counter correction failed.

Smallest safe correction: label row 3 as a carried round-54 W2 finding and round-55 remediation (or move it to the spot-check intake), rather than a newly repeated lane mistake, unless a distinct round-55 regression is evidenced. Do not alter either frozen claim.

## Larger round-54 omission check

Round-54 closure §6 (`corpus/lessons/round-54-verifier-spotcheck.md:124-134`) lists seven routed defects. Round-55 lesson `Spot-check intake` lines 21–22 summarizes the carried items: W2 findings, receipt/quality fixes, and ledger hazards. Compared with `R54W2CritCredit.md:32-34`, the source-tier/scope-clause misattribution is a real additional fixable finding that is absent from the round-55 `Mistakes` table; it is not a mistake in the three rows under attack and is not described as a correction in the round-55 lesson. `R54W2CritTrends.md:27` independently notes the stale S100/S101 Registry cells and their append-only correction convention; closure §6 has no separately named issue for that. These are larger possible carried omissions, but the latter is explicitly a disclosed append-only residual, not plainly an unintegrated defect. Do not infer that every closure item belongs in `## Mistakes`: some were separately corrected/recorded (E08, QUALITY 101–105, round-55 intake) and round-54's RW-1 is addressed in round-55 C1.

Verdict: rows 1–2 survive; row 3 accurately recites a real round-54 W2 hook/isolation finding and a round-55 remedy, but is misclassified as a new lane mistake absent evidence of a round-55 regression; a round-54 scope-clause credit wording finding also appears missing from the round-55 Mistakes table.