# chousa round 97 — frozen claims (ChousaR97, attempt 1)

Base `c8087ac529003e667505bcc624f9a7bde0cffbce` (round-96 landing; its non-author spot-check is on the lane at
`corpus/lessons/round-96-verifier-spotcheck.md`). Two claims, two axes, no exploratory claim. C2 rests on `S225`
and `S226`, both opened this round. Every command runs from the lane root. `<scratch>` is
`/fast/scratch/hyaku/chousa-r97/<seat>`.

## C1 `C1-SELFTEST-GRIP-R97` — operability (lowest scored axis, historical 3/10)

**Sentence.** `tools/search-rerun.py --selftest` runs 47 in-memory cases, each inside a guard that turns an
exception raised inside the case into that case's FAIL, and exits 0 with `SEARCH_RERUN_SELFTEST: PASS cases=47/47`.
Each of 30 named external one-site mutants — the 28 non-equivalent mutants that `R96MutantsC1` wrote and applied in
round 96, read by the battery from the committed probe `.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt` at
base, and the two `git_env` mutants `R96SentinelC1` reported (F1: `GIT_NO_REPLACE_OBJECTS` dropped; F7: only
`GIT_DIR` scrubbed) — makes it exit 1, print `SEARCH_RERUN_SELFTEST: FAIL` and print no traceback; the base tool
kills 10 of the same 30 by the same rule. The round-96 battery's 23 mutants are still killed, three stand-ins (a
constant PASS printer, a hollow self-test, an always-FAIL self-test) fail the battery, the self-test writes nothing
into an empty cwd/HOME/TMPDIR and leaves the lane's `git status --porcelain` and `git diff` digest equal to their
battery-start values, and the round-95 battery and mutant rebuild still pass on the changed tool.

**Predicate (at the landing revision):**

1. `python3 -B tools/search-rerun.py --selftest` → exit 0, last line `SEARCH_RERUN_SELFTEST: PASS cases=47/47`.
2. `python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 BASE_KILLED=10/30 CASES=47`
   and `SELFTEST_CONTROLS_R97=PASS`.

**Before (base `c8087ac5`).** The base tool's self-test passes 32/32; scored by the same battery
(`--tool <base tool> --no-regression`) it kills 10 of the 30 external mutants (`EXTERNAL_KILLED=10/30`; 16 survive
with PASS, and n11, n12, n13 and n26 exit 1 with a traceback and no FAIL line, so they count as survivors) and the
battery prints `SELFTEST_CONTROLS_R97=FAIL` — `corpus/evidence/round97/before/c1-base.txt`.
That is the do-nothing control scored by the frozen counter; it does not reach the target.

**Kill rules.** K1 predicate unmet at landing. K2 a named external mutant survives, or is counted killed while
printing a traceback. K3 a stand-in passes the battery. K4 (harm) the round-95 battery or `mutants-r95.py` no longer
passes, or `verify` prints a different verdict line than the base tool on `corpus/fixtures/search-rerun-r95.md` or
`corpus/knowledge/search-peer-review-dedup-r96.md`.

**Named limits.** (a) The 30 mutants were known when the 15 new cases were written: the claim is that these named
sites are now covered, not that the self-test detects defects in general; a fresh mutant elsewhere may survive.
(b) The guard covers exceptions raised inside a case; a mutant of the guard itself (`case`) or of the summary line
is outside the 30. (c) The self-test still does not exercise the git and disk readers; the round-95 battery does.
(d) That `verify` uses `evaluate`'s verdict is not checked by the self-test (round-96 `R96CriticClaims` §Aa); the
round-95 battery checks it through the CLI. (e) NO_WRITE sees the empty directory and the lane's status and diff
digest, not system calls. (f) `n30` is excluded as equivalent (the seat's own verdict, `R96MutantsC1.md:154-159`)
and `n08` because it applied 0 times in round 96; the battery fails setup if the exclusions leave other than 28.

## C2 `C2-ENTRY-R97` — depth

**Sentence.** The lane holds `corpus/knowledge/press-checklist-questions-r97.md`, whose 8 decision rows each cite at
least one located quote of the PRESS 2015 checklist questions as Cochrane reprints them for editors (`S225`, tier
B, opened this round), with a second reprint (`S226`, Karolinska Institutet University Library, tier C, opened this
round) used for corroboration and never as a row's only support: its 30 `GATE-RECORD` lines (29 located quotes and
1 unreachable-route reject of the CADTH Table 9 PDF, `S227`) all verify; the Located-quotes strings equal the 29
quoted records as a multiset; each quote is a substring of one line of its own source's capture; every row's Do
cell shares a content word with its warrant quotes, every Lane cell is filled and every row names an S225 quote;
the entry states, and the controls recompute from the two captures, that 10 of the 26 S225 quotes occur verbatim
in S226 and 14 after deleting every non-alphanumeric character; and the entry's 7 searches, run with GNU grep at
`c8087ac5`, re-run at that revision with the recorded count and set.

**Predicate (at the landing revision):**

1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-checklist-questions-r97.md` → exit 0,
   `GATE_RECORDS files=1 records=30 ok=30 fail=0`.
2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/press-checklist-questions-r97.md --root .` → exit 0,
   `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`.
3. `python3 -B tools/search-rerun.py verify corpus/knowledge/press-checklist-questions-r97.md --root .` → exit 0,
   `SEARCH_RERUN_SUMMARY searches=7 rev_match=7/7` and `SEARCH_RERUN: CLEAN`.
4. `python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SOLE_SUPPORT=2/2 CORROBORATION=2/2 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1`
   with `LQ_BOUND=29/29 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8 SOLE_SUPPORT=8/8 ONE_LINE=29/29 VERBATIM=10/26 LETTERS=14/26`,
   and `ENTRY_CONTROLS=PASS`.

**Before (base).** The entry does not exist and `gate-records.py verify` on its path exits 2; no base capture holds a
line with "Are there any spelling errors" or "orphan lines" (`git grep` exit 1) —
`corpus/evidence/round97/before/c2-base.txt`. The round-96 entry's first named limit names the gap: "the checklist's
own element wording ... [is] not held" (`corpus/knowledge/search-peer-review-dedup-r96.md`, `## Named limits`).

**Separability.** C2's predicate 3 needs only `verify`, which is byte-identical in behaviour at base (C1 changes
only the self-test); the base tool re-runs the entry's record and must print `rev_match=7/7` (receipt
`after/c2-separable-base-tool.txt`). C1's self-test is in memory and reads no entry.

**Kill rules.** K1 predicate unmet at landing. K2 a wave artifact shows a Do or Never cell asserting what its
warranting quotes do not say (the row is narrowed or withdrawn and the sentence's row count changes with it). K3 a
quote located only by joining capture lines. K4 S225's or S226's tier or scope cell claims more than the opened
bytes support. K5 the stated corroboration counts differ from a recount over the committed captures.

**Named limits.** (a) The rows' wording is the lane's paraphrase; the instruments check a warrant exists, shares a
content word and includes an S225 quote, not that the paraphrase is faithful — that is the wave reviewer's item.
(b) Neither reprint is the guideline statement; where they differ the entry does not choose. (c) The corroboration
counts are string tests: *letters* can match across a line break in S226 and cannot see a reordering. (d) The
searches are per line over the lane's own capture store.

## Amendments after the freeze — re-frozen at F2 (wave-forced; the text above stays as the F record)

Every amendment is forced by a named wave artifact under `.ufo/waves/round-97/w1/`; reasons and artifacts are in
`plans/round-97.md` § Amendments (A1-A5, B1-B10). The claims are judged at F2 on the sentences and predicates below.

### C1 amended sentence (F2)

`tools/search-rerun.py --selftest` prints 48 named case lines `SELFTEST <id> ok`, in a fixed order, and exits 0 with
`SEARCH_RERUN_SELFTEST: PASS cases=48/48`; each case runs inside a guard that turns an exception inside it into
that case's FAIL, and the shared set-up runs inside an outer guard that turns an exception there (or in `case`)
into a `setup` FAIL. Each of 34 named external one-site mutants — the 29 `R96MutantsC1` mutants that applied in
round 96 (read by the battery from the committed probe at base; `n30` is scored, A1), the two `git_env` mutants
`R96SentinelC1` reported, and the three set-up mutants `R97ScribeLesson` built against F (`x1`-`x3`, transcribed) —
makes it exit 1, print `SEARCH_RERUN_SELFTEST: FAIL` naming at least one failing case (or `setup`), and print no
`Traceback` on stderr; the base tool kills 10 of the same 34 by the same rule. The round-96 battery's 23 mutants are
still killed, three stand-ins fail the battery, the self-test writes nothing into an empty cwd/HOME/TMPDIR and leaves
the lane's `git status --porcelain` and `git diff` digest equal to their battery-start values, and the round-95
battery and mutant rebuild still pass on the changed tool.

**Predicate (F2):**

1. `python3 -B tools/search-rerun.py --selftest` → exit 0, last line `SEARCH_RERUN_SELFTEST: PASS cases=48/48`.
2. `python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 EXTERNAL_KILLED=34/34 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 BASE_KILLED=10/34 CASES=48`
   and `SELFTEST_CONTROLS_R97=PASS`.

**Before (F2 battery on the base tool).** `corpus/evidence/round97/before-f2/c1-base.txt`.

**Named limit (a) (F2):** the 34 mutants were known when the 16 new cases and the outer guard were written; the claim
is that these named sites are covered, not that the self-test detects defects in general. **(b) (F2):** a mutant of
the summary line, of the outer guard itself, or one that turns the guard into a no-op while forging lines is outside
the 34. **(g) (new, A4):** the battery reads the self-test's printed lines; a self-test that prints the 48 expected
lines without computing them (for example, keyed on a hash of its own source — `R97CriticClaims` F4) is not
distinguished. Limits (c)-(f) stand; (f) now reads: `n08` is excluded because it applied 0 times in round 96.

### C2 amended sentence (F2)

The lane holds `corpus/knowledge/press-checklist-questions-r97.md`, whose 8 decision rows each cite at least one
located quote of the PRESS 2015 checklist questions as Cochrane reprints them for editors (`S225`, tier B, opened
this round) with a second reprint on another host (`S226`,
Karolinska Institutet University Library, tier C, opened this round) used for corroboration, every row that cites it
also naming an S225 quote: its 30 `GATE-RECORD` lines (29 located quotes and 1 unreachable-route reject of the CADTH
Table 9 PDF, `S227`) all verify; the Located-quotes strings equal the 29 quoted records as a multiset; each quote is a
substring of one line of its own source's capture; every row's Do cell shares a content word with its warrant quotes
(a lexical floor), every Lane cell is filled and every row names an S225 quote; the entry states, in
`## Two reprints compared` and in the Citing row's Lane cell, and the controls recompute from the two captures, that
10 of the 26 S225 quotes occur verbatim in S226 (16 do not) and 14 after deleting every non-alphanumeric character
(12 do not); and the entry's 7 searches, run with GNU grep at `c8087ac5`, re-run at that revision with the recorded
count and set.

**Predicate (F2):** 1-3 as F. 4: `python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work <scratch>`
→ exit 0, prints
`POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SOLE_SUPPORT=2/2 CORROBORATION=3/3 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1`
with `LQ_BOUND=29/29 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8 SOLE_SUPPORT=8/8 ONE_LINE=29/29 VERBATIM=10/26 LETTERS=14/26`,
and `ENTRY_CONTROLS=PASS`.

**Named limits (F2):** (a) as F, and: Never cells are not instrument-checked, and a Do cell that inverts its quote
while sharing a content word passes WARRANT_TERMS (`R97CriticClaims` F3, `R97MutantsC2` F1); the Never cells were
repaired by the reviewer's reading (B5). (e) (new) SOLE_SUPPORT checks that an S225 quote is named, not that it
carries the row's point (`R97MutantsC2` F2). (f) (new) S226 links CADTH's 2016 report as its source; the two reprints
are separate transcriptions, not shown independent of one upstream.

### C2 wording amendment recorded after F2 (B11; no instrument byte changed)

The F2 sentence carried "16 of the 33 question lines that reprint prints", a count no C2 instrument recomputes
(QUALITY 228, `lessons/round-97.md` Mistakes 4); it is removed from the sentence and stays in the entry's prose,
marked there as seat-measured.

### C2 separability pointer (B12; no instrument byte changed)

The F text names `after/c2-separable-base-tool.txt`, which was never written (`R97ConnectorSiblings`); the separability
receipt is `corpus/evidence/round97/after/c1-verify-harm-and-c2-separable.txt` at F and
`corpus/evidence/round97/after-f2/c1-verify-harm-and-c2-separable.txt` at F2 (the base tool re-runs the entry's record
`SEARCH_RERUN: CLEAN`, byte-identical to the F2 tool).
