author: hyaku closure (non-author integrator, @m_zfl)
round: chousa lane-round 65 · verified 2026-10-30 · lane tip `c46acf83b9464b8e40f869fd0674db8d7533bb1f` (branch `master`, local = remote)

# Round-65 verifier spot-check — chousa (non-author)

Written by the hyaku closure judge for chousa round 65. The judge dispatched four read-only
re-check seats (C1, C2, source spot-check, conformance) and re-opened every source itself;
no lane-authored file was edited. Report verified: `.ufo/reports/round-65/chousa.md`
(fleet commit `60db156321d2bbe3c424b7bef986e350e50904dc`, lane identity, report path only).
This file is the only byte this closure wrote in the lane.

## 1. Conformance — PASS

- Report landed by the lane identity (`chousa-shokunin <chousa@shokunin.local>`), path
  `.ufo/reports/round-65/chousa.md`, `## SHONEN` ×1 with four `[~]` box lines; required
  sections in order. Not a marker: real work, evidence pointers, LOG-tied changes, checkable hashes.
- All eight cited lane commits exist and are ancestors of `master`
  (`git merge-base --is-ancestor` over d6ed8155, f99de3b, 62b0af15, 0a85189, 1df2af73,
  9672a2e, 36281d6, 9171732 → all OK); `jj-lane.sh state`: `ahead=0 behind=0`,
  `git status --porcelain` empty — no uncommitted round work, pushed.
- Dispatched prompt `.ufo/prompts/chousa-round-65.md` (committed `da67973e`; attempt-1
  evidence `f9212294`) carries §1–§5 byte-identical to `templates/round-prompt.md` modulo
  placeholders plus hyaku addendum §6: all five child-lane items and the full round contract
  present; L2 floor 8 = MISSION.md §L2 concurrency 8 (match).
- Dispatch/completion digest (`.ufo/watchdog.log`, copied verbatim):
  - `2026-10-30T11:14:56-03:00 launch chousa round=65 pgid=550136 driver=hyaku-inline attempt=1`
  - `2026-10-30T12:08:09-03:00 lane-dead-no-report chousa round=65; retry same round (hyaku-inline attempt=1: L1 ChousaR65 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-65/chousa.md)`
  - `2026-10-30T12:08:11-03:00 launch chousa round=65 pgid=2226258 driver=hyaku-inline attempt=2`
  - `2026-10-30T12:59:32-03:00 complete chousa round=65; hyaku-inline attempt=2` (plus three re-logged completes 13:03:32 / 13:06:14 / 13:07:32)
  Attempt 1 died without a report; attempt 2 inherited its uncommitted bytes, re-verified
  them, and landed. Five post-report wrap-up commits (`aaecb85`→`c46acf8`, 14:46, lane
  identity, "round wrap-up (run 12)") landed the three released w2 seats' evidence —
  durable-state resolution, noted, no defect.
- Wave shape verified from committed dispatch files: w1 = 64 seats (executor 20, critic 20,
  scribe 12, scout 8, connector 2, reviewer 2; §3 L2 floor met inside one batched call of 64),
  w2 = 32 (attack share 10/32 = 31 % ≥ 25 %), total 96 inside the 64–128 band, no residual
  call; w2 was released un-settled by the operator stop (no `w2-results.json`), reported honestly.

## 2. Claim re-checks

### C1 — operability: receipt-header consistency capability — RE-MEASURED, verdict `improved`

- Frozen instruments unchanged since the freeze: `git diff f99de3b 1df2af73 -- corpus/evidence/round65/{c1-count.py,c2-count.py,claims.md,controls/always-pass.py,controls/always-fail.py,controls/ref-receipt-pin.py}` → empty (also empty freeze→tip).
- Counter re-run at the committed tip: `python3 corpus/evidence/round65/c1-count.py --work <fresh>` → `CASES=20/20 C1=PASS`, exit 0 — matches the reported after value.
- Committed receipts at `36281d6`: `c1-before.txt` `CASES=0/20 C1=FAIL missing-target` exit 1 (base d6ed8155); `c1-after.txt` 20/20 PASS exit 0 (1df2af73); `c1-stubs-after.txt` always-pass 3/20 / always-fail 17/20, both exit 1 — the do-nothing control cannot reach the target; `c1-c2-separability.txt` confirms causal separability. `measurement-summary.json` names `measured-revision 1df2af73…`; receipts self-pin `REVISION=`/`EXIT=`.
- Capability row `receipt-header consistency checking` entered SCORECARD with this passing
  demonstration; SKILL.md registry row `receipt-pin (r65)` present with the corrected
  exit-2 taxonomy; lane gate G05 (`lane-preflight.py --only G05`) → `PASS 86` pointers resolve at the tip.
- Per §Gate standard the lane's `receipt-pin` gate was NOT executed by this closure; its
  committed evidence (registry row, frozen-run receipts, measured revision, boundary-probe
  receipt) was verified instead.

### C2 — depth, sourced: receipt-identity entry — RE-MEASURED, verdict `unprovable` (lane's non-admission upheld)

- Counter re-run at the tip: `python3 corpus/evidence/round65/c2-count.py` → `ENTRY_CHECKS=10/10 C2=PASS`, exit 0 — matches the reported after value. Before receipt `c2-before.txt` `ENTRY_CHECKS=0/10 C2=FAIL` exit 1 reproduced at the freeze tree.
- Shape-only finding independently reproduced by this closure (not taken from seat reports):
  a 9-line boilerplate entry + three stub registry rows in a scratch tree score
  `ENTRY_CHECKS=10/10 C2=PASS` exit 0; entry removed → `2/10 FAIL`. The counter is pure
  substring/prefix shape. The lane therefore correctly withheld admission per its own frozen
  kill rule ("A missed target is unprovable/not admitted, not rewritten"); wave evidence
  `R65C03.md` and `R65M02.md` committed at the tip say the same.
- The entry itself is real: `corpus/knowledge/receipt-identity-r65.md` opens with the
  provenance trio, cites S154–S156; all three sources re-opened by this closure (below).
  Per AXES.md a measured claim whose predicate fails lands `unprovable`; C2 was not declared
  exploratory and had no non-author reviewer at claim time, so no `unprovable-but-better`
  route exists. Depth-axis credit stays artifact-level; the honest-stop statement covers it.

## 3. Discernment spot-check (LEARNING.md) — 3 admits + 1 reject sampled, all AGREE

Gate sampled from `corpus/lessons/round-65.md` `## Gate`; every source re-opened by this
closure; digest pins recomputed from `corpus/evidence/round65/source-openings.json`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S154 git-cat-file(1) | admit, tier A, "object-content output only" | `/usr/share/man/man1/git-cat-file.1.gz` (roff line 505, OUTPUT section; TH: Git 2.56.0, 2026-09-27) | **agree** | Quote verbatim after roff-strip incl. the corrected `<object>` notation; sha256 `8eb0bb07…` byte-exact; sentence supports object-bytes-not-working-tree scoping |
| S155 hashlib | admit, tier A, "installed digest semantics" | `/usr/lib/python3.14/hashlib.py` line 31 | **agree** | `digest(): Return the digest of the bytes passed to the update() method` verbatim on line 31 (bullet spans 31–32); sha256 `88fa6248…` byte-exact; digest-of-bytes ≠ provenance |
| S156 round-64 before receipt | admit, tier B, "receipt text, not execution authenticity" | `corpus/evidence/round64/controls/c1v3-before-full.txt` lines 1 and 44 | **agree** | Line 1 `LEG CLEAN clean ok ok` exact; 44-line file ends `…BATTERY=FAIL`; no in-file revision/exit/digest headers; sha256 `ca05f579…` byte-exact |
| S157 validator reference docstring | **reject**, tier C, "execution proof" | `corpus/evidence/round65/controls/ref-receipt-pin.py` module docstring | **agree** | Sentence `Validate receipt header consistency, not execution authenticity.` verbatim and self-disclaiming; rejection with flip condition is sound taste; sha256 `0719d717…` byte-exact |

Quotes check: 15/11/5+5/7 words, all ≤25, each located. Duplicate-id sweep over the registry
prints nothing. `sources-census.sh validate --root … chousa` → exit 0, 157 rows, the same
five pre-existing W04 duplicate-URL warnings (S051/S053/S073/S074/S075), final `ok` line;
registry freeze→tip diff is exactly the four added rows, zero held cells changed (153→157;
A 118→120, B 27→28, C 8→9; mined 124→127, rejected 10→11 — matches the report).

## 4. Trend verdicts (closure ruling, evidence-backed)

- **expansion — improved.** Admitted, counter-verified capability `receipt-header consistency
  checking` (C1 re-measured 20/20; do-nothing control 3/20 — target unreachable by a control);
  registry 153→157 with +2A/+1B/+1C-rejected; README coverage row + frontier line; census exit 0.
- **quality — improved.** New knowledge entry admitted narrowly with three digest-pinned
  sources this closure re-opened byte-exactly; quote-location corrections landed; QUALITY
  criteria 130/131 added from mined mistakes; no admitted entry failed re-check. Bounded by
  the lane's own disclosed limits: C2's counter attests shape only; forged body passes; CRLF accepted.
- **discernment — improved.** The lane claimed only `unchanged` (wave seats are lane-authored);
  this closure's outside spot-check agrees with all four sampled gate decisions (3 admits, 1
  reject) with located quotes and byte-exact digests, and the falsify wave's two real defects
  (exit taxonomy, shape-only counter) were fixed and converted into QUALITY criterion 131.

## 5. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | **improved** | C1 re-measured (counter + receipts + control); capability row; G05 PASS 86 |
| depth | **unprovable** | C2's counter shape-only (boilerplate control reaches 10/10, independently reproduced); entry real and sourced, but the frozen predicate failed its own kill rule; honest stop |
| coverage | unchanged | PROVINCE/coverage map not moved this round (lane's own record; no evidence against) |
| freshness | unchanged | sources opened and digest-pinned; no drift detector added |
| calibration | unchanged | limits disclosed honestly; SHONEN stays four `[~]` author assertions |
| adjacency | unchanged | generic testing → tameshi, receipt/dispatch lifecycle → kumitate; PROVINCE.md untouched |

No axis harmed: `git diff 10e1b84e c46acf83 -- SCORECARD.md` is additions-only (0 deleted
lines); axes table and `## Retired` untouched.

## 6. Routed defects (status-neutral; the lane fixes these next round)

1. **SCORECARD stale measurement pin.** `SCORECARD.md` round-65 section (≈lines 3080–3084)
   labels the C2 after-column "measured at `0a851898`", but no round-65 receipt names that
   revision — every after-receipt header pins `1df2af73`, and `36281d6` re-issued
   `c2-after.txt` for exactly this reason (QUALITY-108-class citation mismatch). Relabel to
   `1df2af73`.
2. **`source-openings.json` S155 location string** still reads `module documentation31-32`
   while the corrected entry and report say line 31. Cosmetic; digest and quote are correct.
3. **Report wave-evidence sentence overstates a gap.** "Six further seats returned output
   without leaving a report file" — observed: only two (`PriorClosure`, `SourcesCensus`);
   `Attack10`, `EntryDraft`, `LessonDraft`, `SourceReject` each wrote `<name>/report.md`
   inside their seat directory. The error is conservative (understates evidence).
4. **Depth/quality credit wording.** SCORECARD records `depth improved narrowly` /
   `quality improved narrowly` on an unadmitted claim supported by an author-side seat
   review (`R65R02`). This closure keeps the entry as landed work but grades the depth axis
   `unprovable`; align the wording with round-64 precedent ("sourced explanation does not
   rescue the claim") next round.
5. **Axes-table sync.** `| operability | 3 | … | 1 |` still shows last-change round 1 while
   the round records an operability improvement verdict with the score deliberately frozen
   (frozen claim: numeric score remains historical 3/10). Intentional or not, say so in the row.
6. **Third bare `## Capabilities` heading** (line ≈3101) — precedented and parser-safe
   (`startswith`), but the lane's recent convention is `## Capabilities (round-N addition)`.
7. **Operator-side, not a chousa defect:** `templates/round-prompt.md` itself carries only
   1 of the 5 child-lane items — the dispatched prompt satisfies the other four via hyaku
   addendum §6, contradicting `PROTOCOL.md` ("template embeds all five") and `MISSION.md`
   §fidelity-check wording. Named for the operator/protocol lane.

## 7. Admission ruling

Every value the report declares re-derived and confirmed (C1 admitted by re-measurement, C2
`unprovable` with the lane's non-admission independently reproduced; sources, registry,
census, waves, freeze integrity all verified). Not every claim verifies, so the round is
**not admitted**: verdict `rejected-honest-stop` — a real admitted capability landed, C2's
admission is withheld on its own counter, and the operator stopped the round before wave 2
settled (three seats released un-settled, no WAVE-DONE, no settlement fabricated). SHONEN
remains four `[~]` assertions; boxes 1–3 look checkable by a non-author on current evidence
(SKILL.md gate rows + counters + measurement-summary + LOG entry) — promotion review is
operator-owned and is not manufactured here.
