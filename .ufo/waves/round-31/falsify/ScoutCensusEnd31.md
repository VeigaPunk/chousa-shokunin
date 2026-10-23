# ScoutCensusEnd31 — frontier census at the tip (round-31 wave 2, FALSIFY)

Date 2026-10-23. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at
`ee1024fd492144c9c7b315890fac247543c37208`; `corpus/SOURCES.md` SHA-256
`4fb59253ad3a93acf679b2d36aabfba977e1076e5b0ada211bfd4e4d76b9cace` (equal in a fresh clone at the
same commit). No tools installed or updated; no network.

## What was attacked

The landed claims that the round adds S057–S059 as tier-A mined rows whose `used-by` resolves, and
the before→after census in `.ufo/waves/round-31/build/ExecCensusStart.md` (start at `fc97f43b`).

## Ran, with exit codes

1. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
   → **exit 0**, stderr 0 bytes. stdout: `W04 S051 duplicate url …syntax.html across scopes`,
   `W04 S053 duplicate url …socket.html across scopes`, `chousa ok …/corpus/SOURCES.md`.
   `diff` against `ExecCensusStart/validate.stdout` → **byte-identical** (`VALIDATE_STDOUT_IDENTICAL`).
2. `sources-census.sh census … chousa` → **exit 0**, stderr 0 bytes: `rows 59`, `tier.A 53`,
   `tier.B 1`, `tier.C 5`, `status.mined 36`, `status.queued 19`, `status.rejected 4`; `FLEET` block
   identical plus `tier.invalid 0`, `status.invalid 0`, `missing 0`.
3. `sources-census.sh overdue … --today 2026-10-23 chousa` → **exit 0**: 59 `cadence` lines and
   **0 `overdue` lines** (script prints `cadence` for every NNd/symbolic row, `overdue` only when due).
4. Manual census (`manual-census.py`, my scratch; parses only `## Registry`, keeps lead/trail empties):
   rows **59**, parsed 59, bad NF 0; header 11 cols (13 with lead/trail, as the start census states);
   tier A 53 / B 1 / C 5; mined 36 / queued 19 / rejected 4; kind docs 19 / spec 18 / paper 11 /
   own-work 9 / community 2; **ids S001–S059, no gaps, no duplicates, monotonic, next free S060**;
   status×used-by = mined/used 36, queued/unused 19, rejected/unused 4 (no W01/W03 candidates);
   **38 used-by tokens, 0 missing, 0 symlinks**; `opened` 2026-10-19 ×18, 2026-10-21 ×27, 2026-10-23 ×14.
5. Contract's own census snippet (`SOURCES-CONTRACT-v1.md` §Census): `rows=59`,
   `malformed_NF_ne_13=0`, tier `A=53 B=1 C=5`.
6. Fresh `git clone` at `ee1024fd` → `validate` **exit 0**, same two W04 lines; `census` same numbers.
7. `verify-metadata corpus/knowledge/line-binding-r31.md --root . --registry corpus/SOURCES.md` →
   **exit 0**, `CLEAN (entries=1 complete=1 findings=0)`; same for `revision-binding-r31.md`.
8. `git diff fc97f43b..ee1024fd -- corpus/SOURCES.md` → **3 insertions, 0 deletions** (exactly the
   S057, S058, S059 rows); the same diff adds `line-binding-r31.md` (+42) and `revision-binding-r31.md` (+36).

## Before → after

| metric | start `fc97f43b` | tip `ee1024fd` | delta |
|---|---|---|---|
| rows | 56 | **59** | +3 |
| tier.A / B / C | 50 / 1 / 5 | **53 / 1 / 5** | +3 / 0 / 0 |
| mined / queued / rejected | 33 / 19 / 4 | **36 / 19 / 4** | +3 / 0 / 0 |
| missing registry | 0 | **0** | 0 |
| validate findings | 2 × W04 | **2 × W04 (identical bytes)** | 0 |
| next free id | S057 | **S060** | — |
| recheck shapes (on-rel/365d/90d/180d) | 23/26/4/3 | **24/28/4/3** | +1/+2/0/0 |
| rows due on 2026-10-23 | 0 | **0** | 0 |

Script census, manual parse and the contract snippet agree exactly; the +3/+3/+3 deltas reconcile
with exactly three added tier-A mined rows and no in-place row change (append-only rule 2 intact).

## used-by S057–S059 (resolves)

- S057 → `corpus/knowledge/line-binding-r31.md` (5427 B, regular file, mentions S057) ✔
- S058, S059 → `corpus/knowledge/revision-binding-r31.md` (4091 B, mentions both ids) ✔
- Three independent confirmations: filesystem check (38/38 tokens), validate silent on E11, and
  `verify-metadata --root .` CLEAN. Values are lane-relative, matching the contract's census block.
- The same check with `--root ..` from the lane root emits `META_SOURCE_USEDBY_MISSING` for S057,
  S058, S059 — this is a **pre-existing root-convention artifact**, not a regression: round-30's
  `quote-reopen-r30.md` produces the same finding for S050–S056 under `--root ..` and is CLEAN
  under `--root .` (both observed).

## Gaps observed at the tip

- **G1 — no Round 31 search-log entry.** `## Search log` holds exactly two bullets (Round 30 at
  line 94, Round 29 at line 106); `grep -n "Round 31" corpus/SOURCES.md` prints nothing. Contract
  rule 5 requires one note per bounded search, and the three new rows were admitted `mined`.
  Precedent: round 30 put rows and note in one commit (`a9d3a05`); round 29 put rows at `30c9d24`
  and the note one commit later (`7692bf1`). [INFERENCE] the note is close-commit work, but at the
  tip the admitting sweep is unrecorded in the registry.
- **G2 — no Round 31 SCORECARD section.** `SCORECARD.md` ends at line 1735 with
  `## Planned — round 31 (not started)`; no results/verdict section, and `LOG.md` has no round-31
  entry. Yet both new knowledge entries say "The counter's measured result is in SCORECARD.md,
  section \"Round 31\"" and `corpus/lessons/round-31.md` `## Census` says "End: in the round-31
  report and SCORECARD" — both pointers dangle at the tip. [INFERENCE] close-commit work (rounds
  25/29 recorded score after their falsify waves); no round-31 report file exists either.
- **G2b — the round-31 lesson is untracked at the tip.** `git ls-files --error-unmatch
  corpus/lessons/round-31.md` → exit 1, `git status --porcelain` → `?? corpus/lessons/round-31.md`;
  it is not in `ee1024fd`. Observed mtime 2026-10-23 01:47:46, SHA-256 `8ec6f032…dcff` (9588 B);
  it was rewritten during this wave (my earlier read at ~01:45 saw the same `## Gate` S057–S059 table
  and the same `## Census` sentence, still present at line 71 in the current bytes). So every
  round-31 narrative record (`## Gate` quotes, `## Census` pointer, the S057–S059 admission table)
  currently lives outside the landed commit. [INFERENCE] it lands with the close commit.
- **G3 — start-census arithmetic slip.** `ExecCensusStart.md` says "earliest due 2027-01-16"; S006
  (90d, opened 2026-10-19) is due **2027-01-17**, which my independent `date + timedelta` and the
  tool's own due arithmetic both give. Conclusion unaffected: no row is due on 2026-10-23.
- **G4 — S057's digest is only elided.** `c8fff6f2…24f4` in `corpus/SOURCES.md:67` and
  `corpus/lessons/round-31.md:53`; `grep -rhoE '\bc8fff6f2[0-9a-f]{40,}\b' .` prints nothing, so the
  row's byte pin cannot be re-checked from the lane. S058/S059 full digests exist only in build-wave
  drafts (`.ufo/waves/round-31/build/ScribeSrc{SRI,Hashlib}/drafts.md` and the seat reports). Not a
  contract breach — SOURCES-CONTRACT-v1 requires `anchor` section + revision, no hash.

## Verdict

Census claim **holds**: 59 rows, tier A/B/C 53/1/5, mined/queued/rejected 36/19/4, 0 missing,
0 due, validate clean with only the two known W04 warnings, and `used-by` for S057–S059 resolves
under the contract's own lane-relative check. **Not yet true at the tip**: the round-31 search-log
note (G1), the SCORECARD end-census/verdict pointer (G2), and the untracked lesson (G2b) —
bookkeeping gaps left for the close commit, not counter or row defects. No existing row changed; no harm observed.

## Limits

Read-only throughout; no counter, gate or lane file touched; no network; no edits. I did not re-open
S057–S059 or test quote fidelity against the served pages (out of this seat's question); `[INFERENCE]`
marks only the close-timing readings. Lesson quotes are from the working-tree bytes
SHA-256 `8ec6f032…dcff` (untracked, rewritten at 01:47:46 during this wave; the file may change
again before the close commit).

Artifacts: `validate.stdout/stderr`, `census.stdout/stderr`, `validate-clone.stdout/stderr`,
`overdue.stdout/stderr`, `manual-census.out`, `contract-census.out` under
`.ufo/waves/round-31/falsify/ScoutCensusEnd31/`; parser and clone at
`/fast/scratch/hyaku/chousa-r31/w2/ScoutCensusEnd31/`.
