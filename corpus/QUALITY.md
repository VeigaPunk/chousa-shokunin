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
