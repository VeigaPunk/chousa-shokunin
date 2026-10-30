# Round 65 report — draft "Work performed" and "Landed changes" (R65D01, scribe)

Draft only, for L1 integration into the fleet report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/chousa.md`
(that file does not exist yet; sibling lanes already have theirs in `/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/`).
Every line below is derived from committed bytes read with read-only `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin`;
this seat ran no counter, no battery and no validator, edited no lane file, and installed nothing.

**Revision note.** The tip moved while this seat was reading: the range named in the seat brief
(`0a85189821322e01db06216b5cb82d2d858c19f0~1..9672a2e998bff2b51d18b0df4d835bd3ae2c453f`) is a strict prefix of the round's
landed history, and the round gained four further commits on top of it — `9171732` (wave-1 results and the wave-2
falsify dispatch), `a6b6f93` (L1 boundary probes), `1df2af7` (wave-2 falsify findings: exit-2 environment taxonomy,
two quote-location corrections, QUALITY 131) and `36281d6` (re-measured receipts, updated scorecard verdicts, the
LOG.md round-65 entry) — plus `62b0af1`, which commits this seat's own earlier draft bytes as a released-unsettled
partial output. The draft below is therefore written against the current tip `62b0af1538e067f014ed96d6973e9a711b9d2487`,
and the two claims' final verdicts are the ones the lane actually reached (C1 admitted, C2 not admitted on its
counter), not the earlier intermediate wording.

## Work performed

Round 65 declared exactly two claims, frozen at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` against base
`d6ed8155e9b4735639a2cf0a3e479c62f2056195` (`corpus/evidence/round65/claims.md:5` and `:12`, with the freeze-and-kill
rule at `:16`). **C1 is an operability claim** on the lane's lowest numerically scored non-retired axis, historical
3/10, whose target is a receipt-header consistency validator at `tools/receipt-pin.py` scored by
`CASES=20/20 C1=PASS` through `python3 corpus/evidence/round65/c1-count.py --work <fresh-dir>`; it is explicitly not
a claim to cryptographic execution authentication or general parser safety, and no numeric score moves.
**C2 is a depth claim, sourced**, whose target is a knowledge entry `corpus/knowledge/receipt-identity-r65.md`
separating object identity, content digest, reported exit and execution authenticity, scored by
`ENTRY_CHECKS=10/10 C2=PASS` through `python3 corpus/evidence/round65/c2-count.py`; it is a structural check and
cannot establish entailment. The two claims share no counter, no denominator and no artifact, and the lane later
proved that separation causally in a scratch clone — with C1's target removed C2 still reads 10/10, with C2's entry
removed C1 still reads 20/20 (`corpus/evidence/round65/controls/c1-c2-separability.txt:8-13`).

Work items, each with an evidence pointer:

- **Freeze and controls.** The two claims, the two counters, the always-pass/always-fail stubs and the reference
  validator were committed at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`; the frozen counters stayed byte-identical
  through every later landing (`git -C … diff --stat f99de3b 0a851898 -- corpus/evidence/round65/c1-count.py
  corpus/evidence/round65/c2-count.py corpus/evidence/round65/claims.md corpus/evidence/round65/controls/` prints
  nothing, and `corpus/evidence/round65/measurement-summary.json:15` states the same). The before receipts are
  `corpus/evidence/round65/controls/c1-before.txt:5` (`CASES=0/20 C1=FAIL missing-target`, exit 1) and
  `corpus/evidence/round65/controls/c2-before.txt:5` (`ENTRY_CHECKS=0/10 C2=FAIL`, exit 1); the positive control is
  `controls/c1-positive.txt:25` (`CASES=20/20 C1=PASS`, exit 0).
- **Source opening and registry admission.** Four local sources were opened and digest-pinned in
  `corpus/evidence/round65/source-openings.json`: S154 the installed `git-cat-file(1)` OUTPUT paragraph, S155
  `/usr/lib/python3.14/hashlib.py`, S156 the round-64 before receipt, S157 the reference validator's docstring.
  S154–S156 were admitted as rows `corpus/SOURCES.md:164-166` (tiers A, A, B) and S157 was rejected at
  `corpus/SOURCES.md:167` with the flip "independent process evidence binding command, bytes and result"; the
  registry went 153 → 157 rows and the census end receipt `.ufo/waves/round-65/census-end.txt` is byte-identical to
  the start receipt, exit 0, the same five pre-existing W04 warnings.
- **Implementation.** `tools/receipt-pin.py` validates the frozen receipt format against committed bytes, never the
  working tree: exactly ordered `REVISION`/`EXIT`/`SHA256` headers, one empty separator line, a nonempty body, a
  canonical repository-relative path, a revision equal to the caller-supplied `--revision`, and a digest bound to
  `git -C ROOT cat-file blob REVISION:PATH` (`tools/receipt-pin.py:45-67`, `:79-91`), exiting 0 `RECEIPT_PIN=PASS`,
  1 `RECEIPT_PIN=FAIL`, 2 `RECEIPT_PIN=ERROR` for usage/environment (`:30-33`). Its own docstring states the limit
  (`:10-12`): header consistency is not execution authenticity.
- **Sourced interpretation entry.** `corpus/knowledge/receipt-identity-r65.md` carries the source line, `verified-at`
  and `recheck` fields, four numbered claims (`:9-12`), a Limits section naming the missing command/body binding,
  signature, timestamp and attestation and the replay hazard (`:16-18`), and a "Use in research" section requiring an
  outside reviewer to re-open the source (`:22`).
- **Corpus records.** `corpus/QUALITY.md:1014` adds criterion 130 (a self-contained receipt declares revision, child
  exit and instrument-blob digest without treating consistency as execution authentication) and `:1016` adds
  criterion 131 (a structural sourced-entry counter attests shape, not substance); `SKILL.md:158-160` registers the
  round-64 honest-stop exemption, the `receipt-pin` gate and the two round-65 counters; `corpus/README.md:1340-1343`
  indexes the entry and the remaining frontier.
- **Wave w1 (64 seats, inherited from attempt 1).** The spec, dispatch, registry and results are committed under
  `.ufo/waves/round-65/`; the registry records 20 executor, 20 critic, 12 scribe, 8 scout, 2 reviewer and 2 connector
  seats and `w1-results.json:5` records `"seats": 64` with 9 empty outputs (Attack03, Attack06, Attack19,
  RegistryDraft, ScoreDraft, ReadmeDraft, Considerthese, Assimilation, SourceGit). The sharpest review finding, a
  6-line basename-keyed tool scoring `CASES=20/20 C1=PASS` without parsing any receipt, is recorded at
  `.ufo/waves/round-65/w1/ReviewFreeze/c1-boundary-probes.txt:36-40` and
  `.ufo/waves/round-65/w1/ReviewFreeze.md:50-54`, and became the third Mistakes row
  (`corpus/lessons/round-65.md:25`).
- **Wave w2 (32 seats, falsify).** Dispatched by attempt 2 at 12:40 local (`.ufo/waves/round-65/w2.ready.dispatched`),
  it attacked the landed bytes and changed the round three times: the validator's environment taxonomy was returning
  exit 1 where the frozen contract assigns exit 2, fixed in the tool at `1df2af73` (`tools/receipt-pin.py:13-16`,
  `:30-33`, `:71-77`; Mistakes row `corpus/lessons/round-65.md:26`); two located-quote imprecisions in the entry were
  corrected (`corpus/knowledge/receipt-identity-r65.md:9-10`, `corpus/evidence/round65/source-openings.json`); and
  boilerplate controls showed the C2 counter attests shape, not substance, so C2 is reported unprovable
  (`corpus/lessons/round-65.md:27`, `corpus/QUALITY.md:1016`). The wave's own findings are summarized at
  `corpus/lessons/round-65.md:64-85`.
- **Lesson.** `corpus/lessons/round-65.md` records the gate (`:6-17`), five Mistakes rows (`:23-27`), six prior closure
  routed items (`:29-36`), the "assimilation: none" stance (`:38-42`), the attempt-2 continuation (`:44-56`), the
  boundaries (`:58-62`) and the wave-2 falsify findings (`:64-85`): C1 enumerates twenty cases rather than universal
  input correctness, C2 checks structure and citations rather than entailment, and generic testing stays adjacent to
  tameshi while dispatch and receipt lifecycle stay with kumitate.
- **Final measurement.** At the landed tip the frozen counters read `CASES=20/20 C1=PASS` exit 0
  (`corpus/evidence/round65/controls/c1-after.txt:25`, pinned `REVISION=1df2af73…`) and `ENTRY_CHECKS=10/10 C2=PASS`
  exit 0 (`controls/c2-after.txt:5`); the do-nothing stubs stay red at `3/20` and `17/20`, both exit 1
  (`controls/c1-stubs-after.txt:5-6`). `corpus/evidence/round65/measurement-summary.json` pins the freeze, the base,
  the five landing commits and every run (`:5-30`).
- **Verdict.** `SCORECARD.md:3074-3099` carries the round-65 verdict table and the per-axis reading: C1 operability
  improved (capability acquired, counter-verified, do-nothing-unreachable), C2 depth improved only narrowly on the
  landed entry and its re-opened sources **with the claim itself reported unprovable / not admitted on its counter**,
  coverage, freshness, calibration and adjacency unchanged, expansion and quality improved narrowly, discernment
  unchanged pending the outside non-author spot-check. `SCORECARD.md:3101-3105` adds the one capability row,
  "receipt-header consistency checking", first working in round 65. The lane's own LOG record is
  `LOG.md:2037-2047`, whose Outcome bullet states the same split: C1 admitted, C2 not admitted, round admission
  withheld on C2.

## Landed changes (each tied to a LOG.md entry and to the commit carrying it)

Every item is carried by a named commit and tied to the **LOG.md round-65 entry at `LOG.md:2037-2048`**
("Round65 (attempt 2) — a receipt-header consistency capability (admitted), a sourced receipt-identity entry (not
admitted on its counter), and a falsify wave that found two real defects"), which landed with the measurement commit
`36281d6`.

- `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` — freeze: `corpus/evidence/round65/{claims.md,c1-count.py,c2-count.py}`
  and the seven frozen controls. LOG tie: `LOG.md:2037` entry, the "Freeze preserved" bullet.
- `0a85189821322e01db06216b5cb82d2d858c19f0` — implementation and corpus landing: `tools/receipt-pin.py`,
  `corpus/knowledge/receipt-identity-r65.md`, `corpus/lessons/round-65.md`, SOURCES rows S154–S157,
  `corpus/evidence/round65/source-openings.json`, QUALITY criterion 130, the three `SKILL.md` gate rows, the
  `corpus/README.md` index lines, the `SCORECARD.md` "Planned — round65" section (`SCORECARD.md:3070-3072`) and the
  64-seat wave-1 evidence tree. LOG tie: `LOG.md:2037` entry, the "Implementation" and "Frontier" bullets.
- `91717322e4dc7f38d4f84010e48b832032808e0c` — wave-1 results bookkeeping (64 seats, 9 empty outputs) and the wave-2
  falsify spec, dispatch, registry and `.ready`. LOG tie: `LOG.md:2037` entry, the "Wave" bullet.
- `a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe` — L1 boundary probes on the landed validator and the CRLF disclosure
  appended to the lesson (`corpus/lessons/round-65.md:62`). LOG tie: `LOG.md:2037` entry, the "Mistakes" and
  "Boundaries" content.
- `1df2af73a79d038edf0b62ebc5691cb579ca3445` — wave-2 falsify findings: the exit-2 environment taxonomy fix in
  `tools/receipt-pin.py`, the two quote-location corrections in the knowledge entry and `source-openings.json`,
  QUALITY criterion 131, the wave-2 seat reports, and the `c1-c2-separability.txt` receipt. LOG tie: `LOG.md:2037`
  entry, the "Implementation", "C1 after" and "Mistakes" bullets.
- `36281d6` — the LOG.md round-65 entry itself (`LOG.md:2037-2048`), the re-measured after receipts at the fixed tip,
  `corpus/evidence/round65/measurement-summary.json`, and the updated SCORECARD verdicts (C1 admitted, C2 not
  admitted). LOG tie: this is the entry — `LOG.md:2037`.
- `62b0af1538e067f014ed96d6973e9a711b9d2487` — this seat's own draft bytes, committed by the L1 as a
  released-unsettled partial output (`.ufo/waves/round-65/w2/R65D01/draft.md`). LOG tie: `LOG.md:2037` entry, the
  "Wave" bullet's w2 seat accounting.

## Drafting notes for the L1 (not part of the report text)

- The report's before→after table should use the frozen before receipts (`controls/c1-before.txt:5`,
  `controls/c2-before.txt:5`), not the intermediate `9672a2e` SCORECARD table: that table predates wave-2 and still
  reads "C2 improved", whereas the current verdict at `SCORECARD.md:3087` reads "unprovable / not admitted" for C2
  with the depth move resting on the re-opens and the source review rather than on `ENTRY_CHECKS`.
- Because C2 is not admitted, the report must not present the `ENTRY_CHECKS=10/10` counter run as the depth claim's
  proof; the honest statement is that the entry landed with its sources pinned and that the counter attests shape
  only (`corpus/QUALITY.md:1016`).
- The w2 seat accounting in the LOG entry counts 29 reported seats of 32 dispatched; this seat's own draft is
  included in that count only through its committed bytes at `62b0af1`, and the L1 should say so explicitly rather
  than letting this seat's partial output count as a settled falsify result.
- No tool was installed by this seat and none was needed; pacman was not run.
