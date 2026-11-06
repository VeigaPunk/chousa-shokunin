# chousa round 83 — frozen claims

Base (round-82 tip, closed `rejected-honest-stop`): `a46534a51756f7e7d9bb55dd9a275156d908d84c`.
Egress table committed before any fetch: `8fff80ee43fbb99fb391c0f4751dbfd47c722744` (commit time 2026-11-06T20:53:00Z;
first round-83 refetch row 20:53:06Z).
Prefreeze instruments, fixtures, stubs and captures: `1b9b2ff8955190a3e5cd42800009d13d6b8e4e04`.
Prefreeze control receipts: `corpus/evidence/round83/controls/receipts/` (driver `run-controls-r83.sh 1b9b2ff8…`,
`CONTROLS_AS_EXPECTED=8/8`), committed with this file, before the candidate tool and the candidate entry are committed.

Disclosure: the candidate tool `tools/gate-records.py` was drafted in L1 scratch (`/fast/scratch/hyaku/chousa-r83/L1/`)
before this freeze and run against the battery while the counter was written; no counter or predicate below was changed
after that run except to add what is stated here. Its bytes enter the lane only in the landing commit after this file.

## Fresh-start / rejection-history reads (done before this file)

- r82 (`round-82-verifier-spotcheck.md`): C1 gate claim fell on K2 — a parser property (`load_sections` keeps the last
  body of a repeated heading) no vocabulary control covered; C2 depth fell on K3 — row 1's Never was stronger than its
  quotes and contradicted in part by a sentence of the same paragraph. Routed defects 1–4.
- r81 (`round-81-verifier-spotcheck.md`): depth counter passed filler; checklist Run lines passed placeholder forms.
- r80 (`round-80-verifier-spotcheck.md`): a planted record that a counter parsed but never opened.
- Lesson applied: (1) each kill rule below names the exact spec the subject must meet, so a finding is decidable from
  bytes; (2) a K2 class is the subject's own documented contract, not an open vocabulary; (3) every Never in the entry is
  read against the full paragraph of its quote before landing (the r82 K3 cause); (4) do-nothing, filler, re-landed
  old work, blanket-accept, blanket-refuse and cheapest-partial-work controls are executed and committed here.

## C1 — depth (sourced on S009 re-opened, S212, S213 — all fetched this round)

**Claim.** One new knowledge entry teaches how to record an appraisal judgment — duplicate independent judgment,
a disagreement process fixed in advance, support and source location recorded for each judgment, the narrow use of
"no information", and overriding a proposed judgment only with a stated reason — on ground no base entry cites (the
MECIR C52–C60 page, queued since round 1, and Cochrane Handbook chapters 7 and 8).

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round83/depth-r83.py" --root "$D"`

**Before** (`controls/receipts/c1-d0-donothing.txt`, tree 1b9b2ff8): `DEPTH_R83 entries=0 ok_entries=0 rows=0
located_quotes=0 fresh_sources=0`, `DEPTH_R83=FAIL`, rc 1.

**Predicate (target).** At the landing revision the counting command prints `entries=1 ok_entries=1`, `rows=` ≥ 7,
`located_quotes=` ≥ 8, `fresh_sources=3`, and `DEPTH_R83=PASS`, rc 0.

**Controls (executed, committed):** `c1-d0-donothing` FAIL; `c1-d1-r81-filler` (the round-81 filler pair as new entries)
FAIL; `c1-d3-r82-entry-relanded` (the round-82 entry re-landed under a new name: old work re-declared) FAIL;
`c1-b1-salad-boundary` (located quotes from the three fresh sources under content-free rows) PASS — the stated counter
limit: the counter does not judge whether a row follows from its quote; kill rule K3 does.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2 (located): a declared quote of the entry does not occur (whitespace-collapsed, curly quotes folded) in its
  committed capture, or occurs there but is absent from the live page when a non-author re-open gets HTTP 200 and
  tag-strips it. An unreachable re-open is recorded, not a kill.
- K3 (warrant): a non-author reviewer shows, for any decision-table row, (a) that its Do or Never states something its
  cited quotes do not state or entail, or (b) a sentence of the same cited source (located in the committed capture,
  quoted by line) that contradicts the row's Do or Never. One such row falsifies C1. Repairs after scoring do not rescue.
- K4 (ground): a base-list entry (`base-knowledge.txt`) cites S009, S212 or S213 or contains any of their URLs.

## C2 — operability (lowest-scored non-retired axis, historical 3/10) — capability acquisition

**Claim.** A new runnable lane tool, `tools/gate-records.py verify`, checks every `GATE-RECORD` line of a lesson against
committed lane bytes (registry row and tier, capture path/key/sha, refetch row, quote location and word count, or for the
rev form the git blob line) — the checks the lessons' hand "Location command" covered only in part — refusing forged
records with the documented code and passing the lane's 15 genuine records of rounds 80–82.

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round83/gate-records-r83.py" --root "$D" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku`

**Before** (`controls/receipts/c2-k0-donothing.txt`, tree 1b9b2ff8): `TOOL=absent POSITIVE=0/15 FORGED_REFUSED=0/198
EXPECTED_CODE=0/198 EMPTY_REFUSED=0/1 RC=0/3`, `GATE_RECORDS_R83=FAIL`, rc 1.

**Predicate (target).** (a) At the landing revision the counting command prints exactly `TOOL=present POSITIVE=15/15
FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3` and `GATE_RECORDS_R83=PASS`, rc 0; and (b) at the
round's final tip `python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md` prints `ok=` equal to
`records=` with `records=` ≥ 3 and exits 0 (the capability used on this round's own Gate block).

**Controls (executed, committed):** `c2-k0-donothing` (tool absent) FAIL; `c2-f1-stub-accept` (blanket OK:
`POSITIVE=15/15 FORGED_REFUSED=0/198`) FAIL; `c2-f2-stub-refuse` (blanket FAIL with every code: `POSITIVE=0/15`) FAIL;
`c2-f3-stub-quote-only` (the hand Location command as a tool — quote and word count only: `FORGED_REFUSED=71/198
EXPECTED_CODE=40/198`) FAIL.

**Declared record class (closed, frozen):** a line whose first text, after leading whitespace and Unicode Cf format
characters, is `GATE-RECORD` followed by whitespace or end of line. Mentions inside inline code, list items, blockquotes or
HTML comments are prose, not records, and are out of class.

**Kill rules (frozen):**
- K1: predicate (a) or (b) is not met.
- K2 (spec generalization): any in-class record line, authored by anyone, that violates one of the checks the tool's
  own docstring defines (PARSE, REGISTRY, TIER, CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN,
  QUOTE_ABSENT, REV, LINE), judged against the lane's committed `corpus/SOURCES.md`, `corpus/captures/`,
  `corpus/evidence/round57/refetch.tsv` and git history at the landing revision, on which the landed tool prints `OK`
  → C2 falsified. Editing those registry/capture/log files themselves is out of class (their integrity is the git
  history's).
- K3 (harm): a genuine record — one that meets every docstring check — on which the landed tool prints `FAIL`, or any
  file the tool writes, any network access, or any mutating git command it runs → C2 falsified.
- K4 (exit contract): the tool exits 0 on input with no in-class record, or exits 0 while printing any `FAIL` line.
