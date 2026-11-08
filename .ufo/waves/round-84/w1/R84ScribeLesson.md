# R84ScribeLesson — lesson-draft seat, chousa round 84

Seat: `R84ScribeLesson` (role: scribe). Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scored landing + tip under test: `03bbb4580b39b442be69f998fae2db48d64b8c93`.
Deliverable: `.ufo/waves/round-84/w1/R84ScribeLesson/lesson-draft.md` (draft, **not landed**).
Receipts: `.ufo/waves/round-84/w1/R84ScribeLesson/receipts/` (13 files).

**Scope actually performed.** Drafted the four requested sections (`## Mistakes`,
`## considerthese`, `## Assimilation`, and a `## Gate` addendum) for
`corpus/lessons/round-84.md` against the Gate block at the scored landing. Nothing was
landed; no lane file was edited; no git/jj command mutated the lane or the fleet root.
The draft's `## Mistakes` row is a **sharper restatement of the committed row 2** of the
landed lesson's table, not a new claim, and the draft says so on its face.

## Commands run (exact, reproducible)

Trees and fixtures, all under `/fast/scratch/hyaku/chousa-r84/R84ScribeLesson/` (deleted
before yield; every receipt copied into the wave folder first):

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 03bbb4580b39b442be69f998fae2db48d64b8c93 | tar -x -C <scratch>/landing
python3 -B <landing>/corpus/evidence/round84/depth-r84.py --root <landing>
python3 -B <landing>/corpus/evidence/round84/gate-records-r84.py --root <landing> --repo <lane> --work <scratch>/work
python3 <landing>/tools/gate-records.py verify --root <landing> --repo <lane> corpus/lessons/round-84.md
```

Tooling: no install, no upgrade. `python3` 3.14.8 and `git` 2.56.0 as shipped (receipt 09).
`/home/vgpnk/.omp/agent/RULES.md` read first; the pacman guard is respected (nothing
installed from any channel).

## Findings

### F-1 — The frozen depth counter's own docstring contradicts its code (new; not in any peer report)

`corpus/evidence/round84/depth-r84.py` at the landing rev:

- `Usage:` line (line 5) names `corpus/evidence/round83/depth-r84.py` — a path that has
  **never existed in any revision** of the lane
  (`git log --all -- corpus/evidence/round83/depth-r84.py` → no commits;
  `git cat-file -e 03bbb458:corpus/evidence/round83/depth-r84.py` → rc 128). Run verbatim
  it exits **rc 2**, "No such file or directory" (receipt 03).
- The prose names round 83's base list (`corpus/evidence/round83/base-knowledge.txt`) and
  round 83's `ROUND_START` (`2026-11-06T20:53:00Z`); the code reads
  `corpus/evidence/round84/base-knowledge.txt` and `2026-11-08T02:05:00Z` (lines 52–53).
- The divergence is **load-bearing, not cosmetic**: with the docstring's constants the
  counter prints `entries=2 ok_entries=2 rows=21 located_quotes=28 fresh_sources=6`; with
  the code's constants it prints `entries=1 ok_entries=1 rows=11 located_quotes=12
  fresh_sources=3` (receipt 06). The documented contract measures a **different
  population**, one that includes the previous round's already-landed entry.
- A docstring-vs-code checker (scratch `check_docstring.py`, copied into receipts/04) reports
  `bad=3` on the round-84 counter and `bad=0` on the round-83 and round-82 counters it was
  copied from — i.e. the defect was introduced in round 84's copy-forward, not inherited
  (receipt 04).
- Peer overlap, stated for the record: seat `R84ScoutNovelty` finding 11 reaches the
  adjacent point that the added base-list entry "makes the counter's own docstring stale";
  the never-existing Usage path and the `ROUND_START` divergence are additional here.
- The counter is frozen; its repair cannot rescue a scored claim. Forward fix: regenerate a
  counter's `Usage` line, base list and `ROUND_START` prose from its code in the same
  commit, and diff a copy-forwarded counter's prose against its code before freezing.

### F-2 — The `url/unreach` form cannot express a 203 cookie-wall

A well-formed unreach record for a 403 row (`curl_rc=22 http=403`) verifies `OK` (rc 0);
the same form for the PubMed rows' `curl_rc=0 http=203` is refused `FAIL REFETCH` (rc 1),
because the tool's success test is "curl_rc == 0 and http starts with `2`" and 203 is a
2xx (receipt 12 §C/§D). The round's rejections of S021/S022/S032 as "HTTP 203
cookie-challenge pages, no content" are substantively right — both captures are the
190-byte wall "pubmed.ncbi.nlm.nih.gov Cookies must be enabled … HHS Vulnerability
Disclosure", and neither "survival analysis" nor "living systematic review" occurs in them
(receipt 12 §E) — but they cannot be written as `GATE-RECORD` unreach lines under the
tool's current contract.

### F-3 — The round-84 tool cannot see the twelve open Gate-record defects it is meant to re-check

`tools/gate-records.py` reads only the `GATE-RECORD` line grammar. The twelve round-80
remainder ids live in two older grammars: ten as `| S170 |` table rows (lessons 70–72),
two (S191, S193) as prose `Admit S191` / `Admit S193` bullets (lessons 77–78) — zero in the
tool's grammar (receipt 11). The tool prints `GATE_RECORDS files=1 records=0 ok=0 fail=0`
(rc 1) on every lesson that carries them, and sees exactly 21 records across all 133
lessons. This is the mechanical reason the `considerthese` proposal "One open Gate-record
S-id per daily review" (`considerthese/2026-11-06.md:28`) is still unimplemented: the
round-84 lesson's claim that it "is implementable via `tools/gate-records.py verify`" holds
for the round's three **new** records and stops there.

### F-4 — Independent reproduction of the C1 setup-leg K2 (corroborates `R84ExecRepro`, `R84CriticClaims`, `R84ReviewerTool`)

At the landing rev, a genuine rev record checked with `--repo` = a scratch dir with no git
history gives `GATE_RECORD …:1 S214 FAIL LINE,REV`, stderr empty, **rc 1**; the same record
against the real lane repo gives `OK`, rc 0 (receipt 09). The frozen expectation
(`claims.md` C1 class 4: "must exit 2 with `GATE_RECORDS_ERROR` on stderr — not `FAIL
REV,LINE` with exit 1") is therefore not met at the landing revision. Three other wave
seats reached the same result independently; this seat's reproduction is the fourth and is
recorded because the landed lesson's `## Claim outcomes` row for C1 still reads
"**verified** (measured)" and the L1 will need to reconcile it. **This seat does not
adjudicate the claim** — that is the canonical judge's call; the observation is reported
verbatim with its command, receipt path, observed line and exit code.

### F-5 — The mined mistake, with the fix shown able to fail

Round 83's committed control fixture
`corpus/evidence/round83/c1-controls/B1-salad-boundary/replace.txt` (at `3b616420`) writes
a **single-valued** `used-by` cell (`corpus/knowledge/ctl-entry-r83.md`); round 84 reused
that fixture verbatim against a wider tree. The defect was **latent in round 83** — the
real r83 entry `corpus/knowledge/appraisal-judgment-records-r83.md` did not exist at round
83's control rev `1b9b2ff8` (`git cat-file -e` → rc 128; round 83's own control receipt
prints `entries=1`, the control entry only) — and went **live in round 84** because the
round-84 base list added that entry (94 → 95 lines), putting the real entry in scope when
the overlay replaced the S214/S018/S023 rows.

Before/after on the same landing tree with the same frozen counter (receipt 10):

```
BEFORE (round-83-shaped overlay, single used-by)
ENTRY search-transparency-reporting-r84.md ok=no rows=11 quotes=0/12 fails=E3,E6
DEPTH_R84 entries=2 ok_entries=1 rows=19 located_quotes=8 fresh_sources=3 / DEPTH_R84=FAIL   rc=1

AFTER (committed comma-separated used-by)
ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-
DEPTH_R84 entries=2 ok_entries=2 rows=19 located_quotes=20 fresh_sources=3 / DEPTH_R84=PASS  rc=0
```

The counters were right to refuse the tree whose registry no longer claimed the real entry;
the defect is in the **control fixture**, not in the counter, the tool or the entry.

### F-6 — The S017 landing page carries no quotable checklist text (confirms the round's disposition)

All five S214 quotes are ABSENT from both S017 captures (`259c96bf7088a12bc7ce65c4`
landing page, `1f5f4eec0b85edf1dc53db7b` checklist page) and FOUND in the PDF capture
`a640b15abf781e5c583d7088.txt` at lines 17, 18, 19, 20, 53 (receipt 13). A forged admit
record for S017 quoting the landing page is refused `FAIL QUOTE_ABSENT` (rc 1, receipt 12
§A). The round's "S017 … reverted to queued — the landing page carries no quotable
checklist text" is correct. The counter-level shape of the same fact: with the S214
registry row **present but its URL pointed at the S017 landing page**, the depth counter
prints the identical `quotes=7/12 fails=E3,E6` / `DEPTH_R84=FAIL` rc 1 as with the row
removed (receipt 05) — the counter resolves a source's capture by the registry row's URL,
so a row naming the landing page cannot locate the PDF's quotes. Separately, the lesson's
prose "the checklist page linked to the PDF" is not what the bytes show — the
checklist-page capture has 0 hits for `PRISMA_2020_checklist-ab3g` and its only two URLs
are a Creative Commons licence and `prisma.shinyapps.io/checklist/` (receipt 13). Seat
`R84ScoutNovelty` finding 7 reached the same point.

## Gates measured by this seat

- `tools/gate-records.py verify --root <landing> --repo <lane> corpus/lessons/round-84.md`
  → `S214 OK`, `S018 OK`, `S023 OK`, `GATE_RECORDS files=1 records=3 ok=3 fail=0`, **rc 0**
  (receipts 01, 07).
- `depth-r84.py --root <landing>` → `entries=1 ok_entries=1 rows=11 located_quotes=12
  fresh_sources=3`, `DEPTH_R84=PASS`, **rc 0** (receipt 02) — the C2 counting command's
  predicate line, reproduced independently of the committed `after/c2-after.txt`.
- `gate-records-r84.py --root <landing> --repo <lane> --work <scratch>` → `TOOL=present
  POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288
  EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored`, `GATE_RECORDS_R84=PASS`, **rc 0**.
- Setup leg, public CLI, non-git `--repo`: `FAIL LINE,REV`, stderr empty, **rc 1** where
  the frozen wording requires exit 2 + `GATE_RECORDS_ERROR` (receipt 09) — see F-4.

## Touched surfaces

Written (all inside this seat's own wave folder; nothing else on disk was modified):

- `.ufo/waves/round-84/w1/R84ScribeLesson/lesson-draft.md`
- `.ufo/waves/round-84/w1/R84ScribeLesson/receipts/01..13-*.txt`
- this report, `.ufo/waves/round-84/w1/R84ScribeLesson.md`

Scratch `/fast/scratch/hyaku/chousa-r84/R84ScribeLesson/` (landing tree, four mutated trees,
fixtures, the checker script) was removed before yield.

## Out of scope for this seat

- Adjudicating C1 or C2 (canonical judge / L1 seat). F-4 is reported, not ruled on.
- Editing `corpus/lessons/round-84.md`, the frozen counters, the controls or any lane
  production file.
- Any network fetch (this seat's item names no re-open, so the egress allowance was not
  used; every claim below rests on committed bytes).
- The `merge/chousa/` campaign bytes: read-only presence check only; nothing adopted,
  nothing re-grounded, no §10 validation.

## Artifact paths

- Draft: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-84/w1/R84ScribeLesson/lesson-draft.md`
- Receipts: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-84/w1/R84ScribeLesson/receipts/`
- This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-84/w1/R84ScribeLesson.md`

VERDICT: R84ScribeLesson C1 fired — the setup leg misreports at the landing revision (non-git `--repo` → `FAIL LINE,REV`, empty stderr, rc 1, where the frozen wording requires exit 2 + `GATE_RECORDS_ERROR`); reproduced independently in receipt 09, and the landed lesson's C1 "verified (measured)" row still needs reconciling by the canonical judge.
VERDICT: R84ScribeLesson C2 n/a — this seat mined no C2 kill rule; it measured the C2 counting predicate at the landing revision (`entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3`, `DEPTH_R84=PASS`, rc 0) and confirmed all five S214 quotes locate in the committed capture while the S017 landing page carries none of them.
