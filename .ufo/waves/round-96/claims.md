# chousa round 96 — frozen claims (ChousaR96, attempt 1)

Base `bbf64970b6c73ca64bcc5f6de2f33b0550459813` (round-95 landing + its non-author spot-check). Two claims, two
axes, no exploratory claim. C2 rests on `S223` and `S224`, both opened this round. Every command runs from the
lane root. `<scratch>` is `/fast/scratch/hyaku/chousa-r96/<seat>`.

## C1 `C1-SELFTEST-R96` — operability (lowest scored axis, historical 3/10)

**Sentence.** `tools/search-rerun.py` has a `--selftest` mode (round-95 spot-check D1: the tool had no
self-invocation mode, so it could not be registered as a gate) that runs 32 in-memory cases — 14 parse cases, 8
matching cases and 10 judgement cases scored by the same `evaluate` function `verify` runs — and exits 0 with
`SEARCH_RERUN_SELFTEST: PASS cases=32/32`. Each of the 23 one-site mutants named in
`corpus/evidence/round96/selftest-controls-r96.py` makes it exit 1; the base tool exits 2 on the same command;
three stand-ins (a constant PASS printer, a hollow self-test, an always-FAIL self-test) fail the battery; the
self-test leaves an empty cwd/HOME directory empty and the lane status unchanged; and the round-95 battery and
mutant rebuild still pass on the changed tool. SKILL.md registers the tool as a gate naming the self-test.

**Predicate (at the landing revision):**

1. `python3 -B tools/search-rerun.py --selftest` → exit 0, last line `SEARCH_RERUN_SELFTEST: PASS cases=32/32`.
2. `python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 CASES=32`
   and `SELFTEST_CONTROLS=PASS`.
3. `grep -c '^| \`search-rerun\` (r96 re-registration' SKILL.md` → 1, and that row's kind cell is `gate`.

**Before (base `bbf64970`).** `python3 -B tools/search-rerun.py --selftest` exits 2 (argparse: the subcommand is
required) — `corpus/evidence/round96/before/c1-base.txt`. The battery's DO_NOTHING group re-derives this from
`git show BASE:tools/search-rerun.py`.

**Kill rules.** K1 predicate unmet at landing. K2 a named mutant survives. K3 a stand-in passes the battery. K4
`--selftest` writes a file, runs git or opens a socket. K5 (harm) the round-95 battery or `mutants-r95.py` no
longer passes on the landing tool, or `verify` changes a verdict on the round-95 record.

**Named limits.** (a) The self-test does not exercise the git and disk readers (`files_at_rev`, `blob`,
`run_at_rev`, `tree_files`, `run_on_tree`, the ROOT check in `verify`); the round-95 battery does, through the
CLI. (b) The 23 mutants are the lane's chosen sites; a defect outside them may pass the self-test. (c) NO_WRITE
checks the cwd/HOME directory and `git status --porcelain`, not system calls. (d) The cases' expectations live in
the tool itself, so an edit that changes code and expectation together passes the self-test; the battery's
mutants, written outside the tool, are the external check. (e) One mutant (`m34`, dropping the leading-`/` check)
was removed before the freeze as equivalent: an absolute glob always has an empty first segment, which the
empty-segment check refuses (`plans/round-96.md` pre-freeze fix P1).

## C2 `C2-ENTRY-R96` — depth

**Sentence.** The lane holds `corpus/knowledge/search-peer-review-dedup-r96.md`, whose 8 decision rows are each
warranted by located quotes of PRISMA-S items 14 and 16 and its Box 1 glossary (`S224`, the PRISMA-S publisher
PDF re-opened this round under a second scope) and of the PRESS 2015 updated guideline authors' abstract
(`S223`, opened this round): its 31 `GATE-RECORD` lines (30 located quotes, 1 unreachable-route reject) all
verify, the Located-quotes table equals the 30 quoted records one-to-one, every row's Do cell shares a content
word with its warrant quotes and every Lane cell is filled, and the entry's own 8 searches — run with GNU grep at
`bbf64970` — re-run at that revision with the recorded count and set.

**Predicate (at the landing revision):**

1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-peer-review-dedup-r96.md` → exit 0,
   `GATE_RECORDS files=1 records=31 ok=31 fail=0`.
2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-peer-review-dedup-r96.md --root .` → exit 0,
   `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`.
3. `python3 -B tools/search-rerun.py verify corpus/knowledge/search-peer-review-dedup-r96.md --root .` → exit 0,
   `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` and `SEARCH_RERUN: CLEAN`.
4. `python3 -B corpus/evidence/round96/entry-controls-r96.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1`
   and `ENTRY_CONTROLS=PASS`.

**Before (base).** The entry does not exist; `gate-records.py verify` on its path exits 2
(`corpus/evidence/round96/before/c2-base.txt`). The coverage map names the gap: `corpus/README.md:1445` ("PRISMA-S
item 14 (search peer review) and item 16 (deduplication) are read in the capture but not held").

**Separability.** C2's predicate 3 needs only `verify`, which exists at base: the base tool re-runs the entry's
record `rev_match=8/8` CLEAN (`corpus/evidence/round96/before/c2-separable-base-tool.txt`). C1's self-test is in
memory and reads no entry.

**Kill rules.** K1 predicate unmet at landing. K2 a wave artifact shows a Do or Never cell asserting what its
warranting quotes do not say (that row is narrowed or withdrawn and the row count in the sentence changes with
it). K3 a quote located only by joining text across columns. K4 S223's tier or scope cell, or S224's scope cell,
claims more than the opened bytes support.

**Named limits.** (a) The decision rows' wording is the lane's paraphrase; the instruments check that a warrant
exists and shares a content word, not that the paraphrase is faithful — that is the wave's reviewer item. (b) PRESS
is held through an abstract (tier B); the guideline statement and its Explanation and Elaboration answered 403.
(c) The searches run over the lane's own capture store, per line; a sentence wrapped across two layout lines is
not found (the entry's Q6). (d) Consecutive column-line fragments are read as one sentence from line order.

## Amendments after the freeze — re-frozen at F2 (wave-forced; the text above stays as the F record)

Every amendment is forced by a named wave artifact under `.ufo/waves/round-96/w1/`; reasons and artifacts are in
`plans/round-96.md` § Amendments (A1-A5, B1-B6). The claims are judged at F2 on the sentences and predicates below.

### C1 amended sentence (F2)

`tools/search-rerun.py` has a `--selftest` mode that runs 32 in-memory cases — 14 parse cases (12 setup refusals,
a well-formed record, the `\|` alternation), 8 matching cases and 10 judgement cases that call `evaluate`, the
function `verify` also calls (read at source; the self-test does not check that `verify` uses its verdict — the
round-95 battery inside the REGRESSION leg does) — and exits 0 with `SEARCH_RERUN_SELFTEST: PASS cases=32/32`.
Each of the 23 one-site mutants named in `selftest-controls-r96.py` makes it exit 1 (this shows the self-test
fails at those 23 sites, not that it detects defects elsewhere); the base tool exits 2 on the same command; three
stand-ins fail the battery; the self-test leaves an empty cwd/HOME directory empty and `git status --porcelain`
unchanged; and the round-95 battery and mutant rebuild still pass on the changed tool. SKILL.md carries one r96
re-registration row for the tool (counted by predicate 3), whose kind cell reads `gate` (checked by reading).

**Predicate (F2):** unchanged — the three commands and tallies of the F predicate, measured at F2.
**K4 (F2):** judged on NO_WRITE's scope (the empty cwd/HOME and the lane status); file, git and socket activity
outside it is a seat observation, not a battery leg.

### C2 amended sentence (F2)

The lane holds `corpus/knowledge/search-peer-review-dedup-r96.md`, whose 8 decision rows each cite located quotes
of PRISMA-S items 14 and 16 and its Box 1 glossary (`S224`, the S222 PDF bytes re-opened this round under a second
scope) and of the PRESS 2015 updated guideline authors' abstract (`S223`, new bytes this round), and whose Do cells
each share a content word with those quotes (a lexical floor; each row's faithfulness is the wave reviewer's
judgment, repaired at B1-B3): its 33 `GATE-RECORD` lines (32 located quotes, 1 unreachable-route reject) all verify,
the Located-quotes quote strings equal the 32 quoted records as a multiset (the source column is not compared),
every Lane cell is filled, and the entry's own 8 searches — run with GNU grep at `bbf64970` — re-run at that
revision with the recorded count and set.

**Predicate (F2):**

1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-peer-review-dedup-r96.md` → exit 0,
   `GATE_RECORDS files=1 records=33 ok=33 fail=0`.
2. as F (verify-metadata CLEAN).
3. as F (`search-rerun.py verify` → `rev_match=8/8`, CLEAN).
4. `python3 -B corpus/evidence/round96/entry-controls-r96.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1`
   with `LQ_BOUND=32/32 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8`, and `ENTRY_CONTROLS=PASS`.

**Named limit (d) (F2):** fragment groups are read as one sentence from the reading-order text form; in the layout
form L17-L18 skip a line and L24-L25 cross a page break, the running header and a column (named in the entry).
Each quote remains a substring of one capture line (K3 does not fire; `gate-records.py` does not check this — a
seat measured it).
