# Round 45 lesson

author: chousa L1 (omp in-session L1, hyaku run 6)
date: 2026-10-25
base: `d29bf47d94149a1b71581eeb0f36d9ff22d41da3`
freeze: `d82cec904bf0fb8736886b9f17be913c7807427a`

No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Round tag
(QUALITY 64): C1 plumbing, C2 plumbing, C3 ground.

## Claims

Frozen in `corpus/evidence/round45/claims.md` before any seat scored.

- C1 operability: `tools/parent-lifetime.sh` gets an exit contract — exit 3
  when the end line records zero spawned tasks or a seat timed out, a required
  `--timeout` in dispatch mode, `timeout_s=` in the start line. Counter
  `python3 corpus/evidence/round45/c1-count.py`, stub `kimi` on PATH. Before:
  the round-44 tool scores `CASES_MATCH=1/5`, exit 1. After: `5/5`, exit 0.
  Routed from the round-44 closure, D5.
- C2 calibration: every committed gate entry point named in a SKILL.md Gates
  row. Counter `python3 corpus/evidence/round45/c2-count.py --list`. Before:
  `UNREGISTERED=26` of 51 at the base tree, 29 of 54 at the freeze tree.
  After: `UNREGISTERED=0`, 54/54, exit 0. Routed from the round-44 closure, D2.
- C3 depth: two AVeriTeC entries adopted, rows S082–S084, four located quotes
  in lane-committed spans, seven counts re-derived. Counter
  `python3 corpus/evidence/round45/c3-count.py` and `--lane-only`. Before:
  `ENTRIES=0/2`, exit 1. After: full in both modes, exit 0. The lane-only mode
  closes the round-44 closure's D1 (a counter that could not run from the lane
  tree alone).

## Mistakes

1. Class: unverified-assertion. Evidence: while writing
   `corpus/knowledge/evidence-snapshot-coverage-r40.md` the L1 wrote that the
   answers without a `cached_source_url` key "are mostly 'No answer could be
   found.' answers"; the recount says 386 of 1,968
   (`corpus/evidence/round45/counts.json`, `extra_not_frozen`). Captured-by:
   none — the frozen C3 counter checks seven figures, not every figure an
   entry states. Fix: the sentence was replaced by the recount (1,582 sourced
   answers with no archive key), every extra figure is in `counts.json` from a
   committed builder (`corpus/evidence/round45/build-spans.py`), and QUALITY 65
   asks for a recount behind every coverage figure. Shown able to fail: the
   builder prints `answers_without_key_unanswerable: 386` against
   `answers_without_key: 1968`.
2. Class: field-count-for-value-count (staged package). Evidence: the staged
   entry says "6,510 hold a non-empty archive.org URL"; 5,959 of those 6,510
   values are web.archive.org links and 429 are the literal `Metadata`
   (`.ufo/waves/round-45/w1/ExecEmptyEvidenceRecord.md`, recount in
   `counts.json`). Captured-by: none — the campaign gate checked a quote, not
   a count. Fix: QUALITY 65. Shown able to fail: `filled_web_archive: 5959`
   against `evidence_nonempty: 6510`.
3. Class: mirror-scope. Evidence: the first scratch validate of the
   pre-append mirror exited 1 with `file E11 S077 missing used-by
   tools/quarantine-check.py` — the mirror held `corpus/` only, and the
   pre-existing row S077 names a tool in used-by. Captured-by: census E11.
   Fix: the mirror carries `tools/quarantine-check.py` (as round 44's did);
   re-run exit 0, five W04, no E03/E04
   (`.ufo/waves/round-45/assimilation/validate-census.txt`, which the passing
   run overwrote; the failing line is recorded here).
4. Class: misroot. Evidence: four wave-1 seats wrote their reports under the
   fleet root's `.ufo/waves/round-45/w1/` (`ScribeGateR33`, `MutC2Forges`,
   `ConnectSiblings`, `ScribeQuality64`) although the wave context named the
   absolute lane path. Captured-by: the round prompt's misroot sweep. Fix:
   each copied byte-exact into the lane, `cmp`-verified, fleet copy deleted
   (sha256 `69aa781a…`, `78e1ec9c…`, `64fcf33c…`, `bc42d319…`). Shown able to
   fail: the sweep found four files.
5. Class: write-by-default counter. Evidence: `ScribeGateR41` ran
   `corpus/evidence/round41/c1-count.py`, which rewrites
   `corpus/evidence/round41/receipts/cells/cells.json` in the lane with no
   option; the seat snapshotted and restored the bytes (sha256
   `1f5c0afae802…`; diff stat unchanged, 185 lines, the round-44 left-named
   state). Captured-by: none — the seat contract said "pass no option that
   writes a receipt", and this counter writes without one. Fix: the new
   round-41 Gates row names that write scope, so the next wave context can
   name it. Shown able to fail: the row's write-scope cell.
6. Class: number-drift (round-44 closure D4, erratum). The round-44 lesson
   gives the E2867 capture mtime as 20:37 and the launch as
   2026-10-24T21:47:59−03:00. Observed: `stat` gives `2026-10-23
   20:36:20.291295276 -0300`, and `.ufo/watchdog.log:1223` gives
   `2026-10-24T21:36:37-03:00 launch chousa round=44`; no 21:47:59 line exists
   (`.ufo/waves/round-45/w1/ScribeMistakes.md`). The freshness grade is
   unchanged either way.

## Round-44 closure defects — disposition

| defect | disposition this round |
|---|---|
| D1 captures not committed | C3: located spans committed under `corpus/evidence/round45/spans/` with the capture sha256 and offset; `c3-count.py --lane-only` runs from the lane tree alone |
| D2 Gates rows missing | C2: 11 rows added (rounds 31–34 v1/v2/v3, 40, 41, 42 with `tools/quarantine-check.py`, 43 with `tools/absent-split.py`, 44, 45, `tools/parent-lifetime.sh`) plus the QUALITY 64 check row |
| D3 L2-floor wording | this round's floor sits inside wave 1 (46 seats; connector 2, executor 4, scribe 19, scout 5, reviewer 6, critic 5; planner = the L1); the round-44 report is a fleet file and is not edited |
| D4 minor numbers | erratum, mistake 6 |
| D5 launcher exit and timeout | C1 |
| D6 inherited tree | unchanged: the three modified JSONs stay left-named; the operator's round-43 question is unanswered (`.ufo/waves/round-45/w1/ScoutInheritedTree.md`) |

## Gate

Theme: what an AVeriTeC archive field documents, and how many stored values
are archive links. One theme, two entries, three rows. No fetch. Ids bound by
document (`.ufo/waves/round-45/assimilation/renumber-map.tsv`): staged S139 →
lane S082, S140 → S083, S132 → S084; in the staged append the strings S082,
S083 and S084 name PRISMA-S, Cochrane chapter 4 and RFC 7089.
`assimilation/collisions` is empty; the indented guard row `  | S084 |` is
caught by the 0–3-space pattern and missed by the column-zero one
(`assimilation/guard/`). No adopted URL is in the quarantine slice: the
staged rows S132, S139 and S140 carry no quarantine id in
`.ufo/waves/round-45/assimilation/staged-map.tsv` (URL equality against
`tools/quarantine-check.py slice`), and `grep -c -i
'averitec\|2305.13117\|MichSchli'` over the register prints 0
(`.ufo/waves/round-45/w1/ScoutQuarantineOverlap.md` searched the same
keywords).

Admit:

- `corpus/knowledge/evidence-archive-field-policy-r41.md`, citing S082 and
  S083. Province: claim-vs-source verification
  (`.ufo/waves/round-45/w1/ScoutProvinceFit.md`). Re-grounded, not copied: the
  staged inference "an empty claim-level field records that no archive was
  taken" was narrowed to "records only that no link is stored", because the
  README's own `original_claim_url` is conditional on the claim having
  appeared online (`CritFieldPolicyInference`); the paper's 404 warning is the
  lane's own addition.
- `corpus/knowledge/evidence-snapshot-coverage-r40.md`, citing S084.
  Re-grounded: the staged "6,510 hold a non-empty archive.org URL" and "two
  orders of magnitude" were wrong and are replaced by the recount; "the single
  empty evidence entry is worth more than the 6,510 that are filled" was
  dropped — that answer has no source URL (`ExecEmptyEvidenceRecord`,
  `CritSnapshotInference`); the staged pointer to a campaign entry the lane
  does not hold was removed.

Reject:

- `evidence-pool-versioning-r39-amendment-2026-10-23.md` (staged S127, S128).
  Reason: it amends a base entry the lane does not hold, and its prose ids
  point at other documents in lane numbering — S071 is used for RFC 7089,
  which is lane S079 (`.ufo/waves/round-45/w1/CritRejectPoolAmendment.md`).
  Flip: the base entry is adopted in the same round, every prose id re-bound
  by document, and its quotes located in the captures.

Rows: normalized to the census schema in scratch — status `mined`, opened
2026-10-25, recheck `365d`, no pipe in any cell, used-by exactly the citing
entry. Stripped recheck prose: S082 "re-fetch the README and confirm the two
field descriptions"; S083 "re-fetch the v3 HTML and confirm the caching
sentence"; S084 "re-download the file and re-count the empty fields"; each
also carried a stale "(ran 2026-10-24)" stamp. Scratch census before the
append: `validate --file` on the mirror, exit 0, five W04, no E03/E04.

## Sources opened

All from the campaign's on-disk capture cache (file = sha256(url)[:24].txt),
accessed 2026-10-25, no fetch. Spans committed in
`corpus/evidence/round45/spans/`, offsets in `spans.tsv`.

- S082 https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md —
  "Where possible, an archive.org link to the original claim url" (char 1027)
  and "An archive.org link for the source url" (char 1969).
- S083 https://arxiv.org/html/2305.13117v3 — "we cache all pages used as
  evidence in the internet archive" (char 14575); "Archive.org returns a 404
  page for these" (char 120884, Appendix J.4.1, guideline 8).
- S084 https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json
  — a JSON file, no prose quote; its located evidence is the seven frozen
  counts and the recount in `counts.json`, capture sha256
  `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`.

Freshness is not a claim: every capture predates this round's launch
(2026-10-25T06:19:59−03:00); they were written on 2026-10-23 and 2026-10-24.

## Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
chousa`: round start exit 0 (81 rows, five W04); after the append exit 0
(84 rows, the same five W04).

## Spot-check

Seats this lane dispatched are still the lane. What wave 1 found against the
frozen claims:

- `MutC2Forges`: prose paths, a 7-separator row, a row without `exit` and a
  row past the next `## ` heading are all refused; a `### ` subsection stays
  inside the section, as the frozen rule says.
- `MutC3Mutants`: seven single-field mutations all fail the default mode; a
  span offset +1 and a wrong capture sha256 pass `--lane-only`, the named
  blind spot. One finding: a count checked only for presence somewhere in the
  entry can be masked by a second occurrence.
- `MutC1Mutants`: inconclusive in wave 1 — every mutant was built from the
  pre-fix tool, which already fails.
- `CritC2Framing`: C2 is coverage of a path pattern, not correctness of the
  account; the superseded v1/v2 counters of rounds 32–34 are now registered
  (their rows say `superseded`, with the successor path), and some executable
  verifiers under `corpus/evidence/` (for example `round34/self-audit.py`)
  fall outside the frozen set. Named as a limit of C2, not fixed.

Pending: the non-author spot-check.
