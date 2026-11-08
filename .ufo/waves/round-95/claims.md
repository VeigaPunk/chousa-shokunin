# chousa round 95 — frozen claims (ChousaR95a2, attempt 2)

Base `7b2373586fb70f0ead6446c671fcc8b546d3e687` (round-94 landing + its non-author spot-check). Two claims, two
axes, no exploratory claim. Both claims rest on `S222` (PRISMA-S, JMLA publisher PDF), opened this round. Every
command runs from the lane root. `<scratch>` is `/fast/scratch/hyaku/chousa-r95/<seat>`.

## C1 `C1-RERUN-R95` — operability (lowest scored axis, historical 3/10) — capability acquisition

**Sentence.** The lane can re-run a recorded local search expression at the revision the record names and refuse a
record whose filed count or hit set differs from what the expression finds there (`COUNT_DRIFT`, `SET_DRIFT`,
exit 1), while reporting separately whether the current tree moved since that revision (`TREE_CHANGED`, exit 0
unless `--strict`). On the committed 8-search record every search matches at its revision; the nearest prior
instrument, `research-gate verify-sweeps`, accepts all 8 one-cell forgeries the new tool refuses.

**Predicate (both commands, at the landing revision):**

1. `python3 -B tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root .` → exit 0, prints
   `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` and `SEARCH_RERUN: CLEAN`.
2. `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work <scratch>` → exit 0, prints
   `POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2
   DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3` and `RERUN_CONTROLS=PASS`.

**Before (base `7b237358`).** `tools/search-rerun.py` and the record do not exist; the counting command exits 2
(`corpus/evidence/round95/before/c1-base.txt`). Do-nothing control inside the battery: the tool path materialised
from base is absent, so the command exits non-zero and prints no CLEAN line.

**Kill rules.** K1 predicate unmet at landing. K2 a forgery the tool should refuse is accepted, or the positive
record is refused. K3 the tool writes a file, opens a socket, or reads a path outside `--root` (symlinks
included). K4 a constant or source-blind stand-in passes the battery (the `ORACLES` group exists to catch it).

**Named limits.** (a) The regex engine is Python `re`; the record was produced with GNU grep `-P` (PCRE); their
agreement is measured on these 8 expressions only, not in general. (b) Matching is per line; a pattern spanning a
newline never matches. (c) The tree re-run reads files on disk under each glob's static directory, tracked or not.
(d) Agreement proves the record matches what its expression finds, not that the expression was the right search
(recall is not measured). (e) An expression containing a backtick cannot be filed. (f) Only lane-local committed
files are searchable; no external database is re-run.

## C2 `C2-ENTRY-R95` — depth

**Sentence.** The lane holds `corpus/knowledge/search-rerun-record-r95.md`, whose 7 decision rows are each
warranted by located quotes of PRISMA-S (`S222`, opened this round): all 9 quotes are located (gate-records
normalization) in the committed `.txt` capture of the publisher PDF, the Located-quotes table equals the 9
`GATE-RECORD` quotes one-to-one, and each row's `Lane` column is marked as the lane's reading, not a PRISMA-S
requirement.

**Predicate (at the landing revision):**

1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md` → exit 0,
   `GATE_RECORDS files=1 records=9 ok=9 fail=0`.
2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-rerun-record-r95.md --root .` → exit 0,
   `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`.
3. `python3 -B corpus/evidence/round95/entry-controls-r95.py --root . --work <scratch>` → exit 0,
   `POSITIVE=1/1 FORGERY_REFUSED=8/8 DO_NOTHING_REFUSED=1/1` with `LQ_BOUND=9/9 WARRANTS_OK=7/7` and
   `ENTRY_CONTROLS=PASS`.

**Before (base).** The entry does not exist: `gate-records.py verify` on its path exits 2
(`corpus/evidence/round95/before/c2-base.txt`); no `.txt` capture at base contains the item-15 sentence.

**Kill rules.** K1 predicate unmet at landing. K2 a wave artifact shows a Do/Never cell asserting what its
warranting quote does not say (then that row is narrowed or withdrawn, and the count in the sentence changes
with it). K3 a quote is located only by joining text across the two columns of the text form.

**Named limits.** (a) Located means present in the capture's `pdftotext -layout` text after gate-records
normalization; Q6–Q9 are single column-line fragments, and that Q7–Q9 form one sentence is read from layout.
(b) The decision rows' `Do`/`Never` wording is the lane's paraphrase of the quote; the instruments check that a
warrant exists, not that the paraphrase is faithful — that is the wave's reviewer item.
