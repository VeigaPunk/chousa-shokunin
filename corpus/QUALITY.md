# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command, evidence id).
3. Observation, inference and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Round-24 additions (appended 2026-10-19; criteria 1–5 unchanged)

Each criterion cites the mined mistake (`lessons/round-24.md` `## Mistakes`) or
the admitted entry that motivates it. Tier definitions live in
`corpus/SOURCES.md` (contract v1); this file holds admission only. Criteria
6–8 bind `knowledge/` entries; 9–12 bind every lane record (corpus, `SKILL.md`,
`LOG.md`, `SCORECARD.md`), because a record is admitted when it is committed.

6. **Metadata header.** A `knowledge/` entry admitted from round 24 on opens
   with `source:` (≥1 `S###` row of `corpus/SOURCES.md` whose status is
   `mined` and whose `used-by` names this entry, plus its URL or repo path and
   an exact anchor), `verified-at:` (ISO date + what was checked) and
   `recheck:` (an ISO date or a cadence — `90d`, `180d`, `365d`, `on-release` —
   optionally followed by the re-run command). A `recheck:` that is only a
   command leaves "overdue" uncomputable. — M-13.
7. **Scoped tier.** An admitted claim rests on ≥1 tier-A or tier-B
   `SOURCES.md` row whose `scope` covers that claim; a tier-C or `community`
   row is never sole support, and a source used outside its row's scope is an
   inference and labelled one. — `knowledge/contextual-source-admission-r24.md`.
8. **Support states stay distinct.** "Source exists / opens", "source is on
   topic", "source states the claim" and "the claim is true" are four
   observations; an entry never reports a claim verified from the first two,
   and never reports truth from the third alone. —
   `knowledge/claim-support-states-r24.md`.
9. **One home per number and finding.** A restated count, total or open
   finding names its owning file + revision and carries the command that
   re-derives it; closing a finding closes it in every restating file in the
   same landing, and the owning ledger gets the disposition in that landing;
   an index row lands under its own round's heading. — M-3, M-4, M-6, M-12.
10. **No unfilled template; snapshots are dated.** No placeholder ships in a
    record — `${…}`, `<…>` template slots, `TODO`, `TBD`, `[record …]` or an
    uppercase stand-in for a hash such as `LANE_HASH` (check: every hit of
    `grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH' <file>` sits inside
    a backtick span that names the token as data, as in this criterion and
    `lessons/round-24.md` M-5). A dated reflection names the commit window it measured
    (`git log --since --until` bounds) and is re-measured, or not committed,
    when a commit has landed inside that window since. — M-5, M-7.
11. **Plan, claim and table agree.** A pre-registered wave, seat count or
    provider that is not what ran is closed by a disposition line naming what
    ran and the substitute evidence (`honest stop` is reserved for an
    unjudged exploratory claim, `AXES.md` §Working the axes); a capability a
    `LOG.md` entry claims has its `SCORECARD.md` capabilities row in the same
    landing, or the LOG line says it has none and why. — M-1, M-14.
12. **A kept score is re-derived or frozen.** A numeric axis score cited at
    a landing is re-measured there by the counting command its row names, or
    is marked `frozen at rN` with the reason and the round that will
    re-measure it. — M-11.

## Round-25 additions (appended 2026-10-21; criteria 1–12 unchanged)

13. **Runnable recheck.** A new `recheck:` command states its cwd and names
    the research root by role (`--root "$SHOKUNIN_ROOT"`, the fleet root),
    or explicitly states the checkout layout a relative root assumes. A bare
    `--root ..` is not placement-independent. — `lessons/round-25.md` R25-M2;
    `lessons/round-24-verifier-spotcheck.md:17`. Shown able to fail:
    `! grep -nE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/citation-chain-fidelity-r24.md`
    exits 1 on the base line; the clone re-run with `--root ..` is DRIFT,
    with the explicit fleet root CLEAN (`.ufo/waves/round-25/build/ReviewRecheckRoot.md`).
    This syntax check sees only the `--root` argument, not command runnability;
    a reviewer checks the command in a clone outside the assumed layout.
14. **Spot-check intake.** A `lessons/round-<N>.md` landed from round 25 on
    carries `## Spot-check intake`, one row per debt or disagreement in the
    previous verifier spot-check, each fixed (pointer), carried (criterion or
    round), or refused (reason). — `lessons/round-25.md` R25-M3;
    `lessons/round-24-verifier-spotcheck.md:17`. Shown able to fail:
    `grep -qx '## Spot-check intake' corpus/lessons/round-24.md` exits 1 at
    the base; the round-25 lesson exits 0 (the per-debt rows need a reviewer).

15. **Measured bytes must be in the cited commit.** Before a report or a
    falsify wave pins a revision, the executable's digest from
    `git show "$REV":tools/research-gate.sh | sha256sum` must equal the
    measured working-tree digest (and every changed production path is in the
    helper's path list). A successful helper landing proves only its named
    paths landed. — `lessons/round-25.md` R25-M13: the first integration
    checkpoint omitted the gate, so prose said 154 cases while its gate had
    136. This check failed on `0fc037e` and matched at `d8c8cff`.

16. **An owning total must reconcile.** A disposition tuple names the row
    population, counts those rows and applies explicit addendum deltas; its
    components must sum to the row count. Queue-item counts stay separate
    from row dispositions. — lesson R25-M7 (captured-by none before this rule):
    E4's sum72 over71 fails, row-true38/22/8/0/3 sum71 passes. Re-derive with
    `python3 corpus/evidence/round25-ledger-recount.py`; an owner pointer
    alone is not validation of the owner's arithmetic.
17. **A new runnable screen needs an independent failing control.** Derive
    at least one negative fixture from the declared contract independently
    of the implementation; disable its targeted check in an isolated clone
    and show the detector fails for that reason, not a parse error. A printed
    tally without a nonzero mismatch exit is a probe, not a passing gate.
    — lesson R25-M11 (captured-by none); `FxMutateMissing.md` kills the missing
    source/recheck arms, `FxMutateRefusal.md` kills canonical/NUL guards;
    `round25-meta-differential.sh` now exits1 on any table/oracle disagreement.

## Round-26 additions (appended 2026-10-21; criteria 1–17 unchanged)

18. **A bound names its unit.** A byte-read cap is not a memory or time
    budget: downstream representations can amplify a bounded input. Before
    calling a reader resource-bounded, exercise a newline-dense input and
    record peak RSS and elapsed time against a small control. Scope the
    conclusion to the measured shapes; keep time/memory limits distinct.
    — `lessons/round-26.md` R26-M1 (captured-by none): the 8 MiB reader
    allocated over2 GiB before parsing. Shown able to fail:
    `bash corpus/evidence/round26-measure.sh <base-tree> c1` yields
    `C1_AMPLIFIED=4/4` at `ba333325`; same probe and frozen shapes evaluate
    the replacement. The probe exit0 is completion only; compare its values.
