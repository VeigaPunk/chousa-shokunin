# Round 65 report — draft "Work performed" and "Landed changes" (R65D01, scribe)

Draft only, for L1 integration into the fleet report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/chousa.md`
(that file does not exist yet; sibling lanes already have theirs at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/`).
Every line below is derived from committed bytes read with read-only `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin`;
no measurement was run by this seat, no lane file was edited, and no tool was installed.

## Work performed

Round 65 declared exactly two claims, frozen at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` against base
`d6ed8155e9b4735639a2cf0a3e479c62f2056195` (`corpus/evidence/round65/claims.md:5` and `:12`; the freeze commit's own
file list is the claims file, the two counters and the seven frozen controls). **C1 is an operability claim** on the
lane's lowest numerically scored non-retired axis, historical 3/10, whose target is a receipt-header consistency
validator at `tools/receipt-pin.py` scored by `CASES=20/20 C1=PASS` through
`python3 corpus/evidence/round65/c1-count.py --work <fresh-dir>`; it is explicitly not a claim to cryptographic
execution authentication or general parser safety, and no numeric score moves. **C2 is a depth claim, sourced**,
whose target is a knowledge entry `corpus/knowledge/receipt-identity-r65.md` separating object identity, content
digest, reported exit and execution authenticity, scored by `ENTRY_CHECKS=10/10 C2=PASS` through
`python3 corpus/evidence/round65/c2-count.py`; it is a structural check and cannot establish entailment. The two
claims share no counter, no denominator and no artifact, so a pass on one says nothing about the other.

Work items, each with an evidence pointer:

- **Freeze and controls.** The two claims, the two counters, the always-pass/always-fail stubs and the reference
  validator were committed at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`; the frozen counters stayed byte-identical
  through the implementation commit (`git -C … diff --stat f99de3b 0a851898 -- corpus/evidence/round65/c1-count.py
  corpus/evidence/round65/c2-count.py corpus/evidence/round65/claims.md corpus/evidence/round65/controls/` prints
  nothing). The before receipts are `corpus/evidence/round65/controls/c1-before.txt:5` (`CASES=0/20 C1=FAIL
  missing-target`, exit 1) and `corpus/evidence/round65/controls/c2-before.txt:5` (`ENTRY_CHECKS=0/10 C2=FAIL`,
  exit 1); the positive control is `controls/c1-positive.txt:25` (`CASES=20/20 C1=PASS`, exit 0).
- **Source opening and registry admission.** Four local sources were opened and digest-pinned in
  `corpus/evidence/round65/source-openings.json`: S154 the installed `git-cat-file(1)` OUTPUT paragraph, S155
  `/usr/lib/python3.14/hashlib.py`, S156 the round-64 before receipt, S157 the reference validator's docstring.
  S154–S156 were admitted as rows `corpus/SOURCES.md:164-166` (A, A, B) and S157 was rejected at
  `corpus/SOURCES.md:167` with the flip "independent process evidence binding command, bytes and result"; the
  registry went 153 → 157 rows and the census end receipt `.ufo/waves/round-65/census-end.txt` is byte-identical
  to the start receipt, exit 0, the same five pre-existing W04 warnings.
- **Implementation.** `tools/receipt-pin.py` was written from the frozen format contract: exactly ordered
  `REVISION`/`EXIT`/`SHA256` headers, one empty separator line, a nonempty body, a canonical repository-relative
  path, a revision equal to the caller-supplied `--revision`, and a digest bound to the committed blob via
  `git -C ROOT cat-file blob REVISION:PATH` rather than the working tree (`tools/receipt-pin.py:37-61`), exiting 0
  consistent, 1 malformed, 2 usage. Its docstring states the limit in the tool itself
  (`tools/receipt-pin.py:10-12`): header consistency is not execution authenticity.
- **Sourced interpretation entry.** `corpus/knowledge/receipt-identity-r65.md` carries the source line, `verified-at`
  and `recheck` fields, four numbered claims (`:9-12`), a Limits section that names the missing command/body
  binding, signature, timestamp and attestation and the replay hazard (`:16-18`), and a "Use in research" section
  requiring an outside reviewer to re-open the source (`:22`).
- **Corpus records.** `corpus/QUALITY.md:1014` adds criterion 130 (a self-contained receipt declares revision, child
  exit and instrument-blob digest without treating consistency as execution authentication); `SKILL.md:158-160`
  registers the round-64 honest-stop exemption, the `receipt-pin` gate and the two round-65 counters; and
  `corpus/README.md:1340-1343` indexes the new entry and the remaining frontier.
- **Wave w1 (64 seats).** The wave spec, dispatch, registry and results are committed under `.ufo/waves/round-65/`
  (`w1-spec.json`, `w1-dispatch.json`, `w1/swarm-registry.json`, `w1-results.json`); the registry records 20
  executor, 20 critic, 12 scribe, 8 scout, 2 reviewer and 2 connector seats, and `w1-results.json:5` records
  `"seats": 64` with 9 empty outputs (Attack03, Attack06, Attack19, RegistryDraft, ScoreDraft, ReadmeDraft,
  Considerthese, Assimilation, SourceGit). The review seats' findings stayed inside the claims' disclaimed scope:
  the sharpest, a 6-line basename-keyed tool scoring `CASES=20/20 C1=PASS` without parsing any receipt, is
  recorded at `.ufo/waves/round-65/w1/ReviewFreeze/c1-boundary-probes.txt:36-40` and at
  `.ufo/waves/round-65/w1/ReviewFreeze.md:50-54`, and it became the third Mistakes row
  (`corpus/lessons/round-65.md:25`).
- **Lesson.** `corpus/lessons/round-65.md` records the gate (`:6-17`), three Mistakes rows (`:23-25`), six prior
  closure routed items (`:27-34`), the "assimilation: none" stance (`:36-40`), the attempt-2 continuation
  (`:42-55`) and the boundaries (`:56-60`): C1 enumerates twenty cases rather than universal input correctness,
  C2 checks structure and citations rather than entailment, and generic testing stays adjacent to tameshi while
  dispatch and receipt lifecycle stay with kumitate.
- **Final measurement.** At the landed tip `0a85189821322e01db06216b5cb82d2d858c19f0` the frozen counters read
  `CASES=20/20 C1=PASS` exit 0 (`corpus/evidence/round65/controls/c1-after.txt:25`) and `ENTRY_CHECKS=10/10
  C2=PASS` exit 0 (`controls/c2-after.txt:5`); the do-nothing stubs stay red at `3/20` and `17/20`, both exit 1
  (`controls/c1-stubs-after.txt:5-6`). `corpus/evidence/round65/measurement-summary.json` pins the freeze, the
  base, the measured revision and the unchanged-counter statement (`:5-8`, `:15-19`).
- **Verdict.** `SCORECARD.md:3074-3096` carries the round-65 verdict table and the per-axis reading — operability
  and depth improved, coverage, freshness, calibration and adjacency unchanged, expansion and quality improved
  narrowly, discernment unchanged pending the outside non-author spot-check — and `SCORECARD.md:3102` adds the one
  capability row, "receipt-header consistency checking", first working in round 65. A later L1 commit
  (`a6b6f93`) probed the landed validator directly and disclosed its CRLF tolerance as a documented behaviour
  rather than a measured failure (`corpus/evidence/round65/controls/l1-boundary-probes.txt:6`, and the lesson
  paragraph at `corpus/lessons/round-65.md:60`).
- **Wave w2 (falsify).** `9171732` committed the wave-2 spec, dispatch, registry and `.ready` for the falsify wave
  (32 seats), and `a6b6f93` committed the L1 boundary probes; both sit above `9672a2e` and are outside this
  draft's assigned range, so they are listed here for completeness rather than claimed as measured work.

## Landed changes (each tied to a LOG.md entry and to the commit carrying it)

Every item below is carried by a named commit, and every item is tied to the round-65 LOG work record. **The LOG.md
tie for this round is currently a draft, not a landed entry**: the wave-1 scribe seat produced
`.ufo/waves/round-65/w1/LogDraft/report.md` (title line 1: "Round65 LOG work record — DRAFT (seat LogDraft, scribe;
not landed)"), and `LOG.md` at the tip still ends with the round-64 entry (`LOG.md:2023`), with no round-65 section
present. The L1 must land the round-65 LOG.md entry for the ties below to resolve against committed bytes.

- `0a85189821322e01db06216b5cb82d2d858c19f0` — implementation and corpus landing: `tools/receipt-pin.py`,
  `corpus/knowledge/receipt-identity-r65.md`, `corpus/lessons/round-65.md`, SOURCES rows S154–S157,
  `corpus/evidence/round65/source-openings.json`, QUALITY criterion 130, the three `SKILL.md` gate rows, the
  `corpus/README.md` index lines, the `SCORECARD.md` "Planned — round65" section (`SCORECARD.md:3070-3072`), and
  the 64-seat wave-1 evidence tree. LOG tie: the round-65 LOG.md entry (to be landed; the draft text is
  `.ufo/waves/round-65/w1/LogDraft/report.md`, whose C1 and C2 lines are still marked PENDING because it was
  written before the implementation existed).
- `9672a2e998bff2b51d18b0df4d835bd3ae2c453f` — after-measurement receipts and the verdict: the after receipts
  `controls/c1-after.txt`, `controls/c2-after.txt`, `controls/c1-stubs-after.txt`,
  `corpus/evidence/round65/measurement-summary.json`, the census-end receipt `.ufo/waves/round-65/census-end.txt`,
  and the `SCORECARD.md` round-65 verdict plus capability row (`SCORECARD.md:3074-3102`). LOG tie: the same
  round-65 LOG.md entry, its measurement and verdict bullets.
- `91717322e4dc7f38d4f84010e48b832032808e0c` — wave-1 results bookkeeping (64 seats, 9 empty outputs) and the
  wave-2 falsify spec, dispatch, registry and `.ready`. LOG tie: the round-65 LOG.md entry, its wave bullet.
- `a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe` — L1 boundary probes on the landed validator and the CRLF disclosure
  appended to the lesson. LOG tie: the round-65 LOG.md entry, its boundaries bullet.

## Drafting notes for the L1 (not part of the report text)

- The LOG.md gap above is the one thing that must be closed before the "each tied to a LOG.md entry" wording is
  true of the filed report; the wave-1 draft's C1/C2 lines read PENDING and would be inaccurate as landed text.
- The report's own before→after table should use the frozen before receipts (`controls/c1-before.txt:5`,
  `controls/c2-before.txt:5`) rather than restating the SCORECARD table verbatim.
- No tool was installed by this seat and none was needed; pacman was not run.
