# Connector: sibling-overlap scan, round 34 (read-only)

Seat `chousa-r34-w2a2-ConnectorOverlap-10`. Read-only: I opened the six sibling
round-34 reports under fleet `.ufo/reports/round-34/` plus the fleet index, the
frozen claims (`corpus/evidence/round34/claims-a2.md`), both C2/C3 tools, and —
read-only — one sibling tool. No file in any lane was written. Access date
2026-10-23.

Commands run (all read-only, exit 0): `read` of each report; `grep -n
'TOK_DIRECT_SPAN_MAX' tools/research-gate.sh` → line 1581
`TOK_DIRECT_SPAN_MAX=32764`, routing at :1599-1602 (landed fix matches
claims-a2 §Fix); `grep 'self.assessment' tsukuroi-shokunin/tools` (see row 2);
`grep 'round-34|PCRE|3276|self-audit' .ufo/reports/fleet-index-2026.md` (only
audio-lane sample counts, see Index). `corpus/evidence/round34/audit-dispositions.md`
exists (glob).

## Overlap table

| Lane (round-34 report) | Overlapping surface | Relation to chousa C2 (dead zone) / C3 (self-audit) | Import candidate |
|---|---|---|---|
| kaidoku | No span/PCRE surface (ELF Verneed). Counter method: a structure-blind size-lookup control met the frozen counter 12/12 ("selects a template by input size", kaidoku.md:9); lesson M34-4 "counter cannot tell structure from shape" (kaidoku.md:16) | No duplication of C2's surface; the lesson is the round's main external risk to C2's counter | kaidoku's pre-freeze replay-control discipline is already operationalized here: c2-count.py's dz-mut/dz-decoy classes and `expect=supported` labels (content-blind gates score ≤4), attacked by the live MutC2Keyed/NoReader/Accept seats |
| tsukuroi | Closest C3 twin: `tools/check-self-assessment.py` — "Count self-assessment mismatches between a lane's stated axes and observed state. Round 26 … K01 to K27" (tsukuroi-shokunin/tools/check-self-assessment.py:2-5). Also argv/env-adjacent: r34 C1 is a child-env allowlist (env propagation, not argv length) | C3's concept is a fleet precedent (r26), not novel: duplicate in kind. Divergence, not contradiction: tsukuroi gates (exit 1 on mismatch, :42-43); chousa counts and exits 0 with a dispositions ledger — claims-a2's r33 rule "a calibration claim counts mismatches, never asserts" (claims-a2.md:18-19). No C2 overlap: env-copy ≠ E2BIG argv ceiling | tsukuroi's selftest fixture matrix (stale-ordinal, stale-count, unstated-fact, missing-capability-path, shonen-x-without-verifier; :1033-1035) as a committed selftest for self-audit.py; chousa's counter-design already contains the scratch-inject defense (claims-a2.md:157-159) |
| mori | Same-axis: mori C2 is also calibration ("QUALITY 98, the pre-data shortcut battery", mori.md:13-14), judged `unprovable-but-better` (mori.md:30-33); mori C1 fell to skip programs meeting the counter (mori.md:26-29) | Neither duplicates nor contradicts chousa's objects; converging evidence that shortcut controls meet counters — the exact attack C2's P2 must survive | Named non-author judge pattern (ReviewC2Judge3) applied to the C3 audit set itself, and mori's disclosure that a claim can fail verification while the tool remains useful |
| kake | No span/PCRE surface (link previews). Source-row re-opening twin: wave-2 re-opened all Gate rows and "the reasons hold" (kake.md:101-102). Counter insufficiency: "both declared counters give their full score to a control that does none of the work" (kake.md:39) | S065 re-check method duplicated (both re-open rows live and log); no contradiction | kake's `criteria/lookup_control_check.py` "gives exit 1 on the frozen C1 counter" (kake.md:42) — the only sibling that committed a shortcut detector next to its counter; same artifact class fits C2 |
| kumitate | Round-record self-audit twin: `round-gate.mjs --round 34` → `ROUND_GATE: CLEAN … checks=10` (kumitate.md:54); mined mistake "own round-gate failing own record" (kumitate.md:74) | Methodological duplicate of C3's goal at coarser grain (10 structural checks vs chousa's 43 pointer checks incl. `receipt_binding`); kumitate gates, chousa counts | kumitate's failure mode marks a boundary chousa shares: self-audit.py cannot audit this round's report (written after the counted run); already covered by claims-a2 "Not claimed" (:164-165) — worth restating in the round record |
| kotodama | Calibration twin at citation level: claim C pins "28/28 executables resolve at SKILL.md `f9bd07c2…`" plus re-issue of seven stale cites with a "C09-F2 guards against phantom rows" guard (kotodama.md:40-45) | Duplicate in spirit (pinned-digest verification of self-description), orthogonal in object (citation anchors vs repo pointers); anchor-reissue ≡ chousa's dispositions (fixed/routed/accepted, filed bytes untouched) | The phantom-row guard idea: an audit-set sanity check that every enumerated id is actually exercised (inject-and-watch-the-count-move is the manual form claims-a2 already names) |

Fleet index: `.ufo/reports/fleet-index-2026.md` (1 week old) is an audio-lane
adjudicator index; its `round-34` row names `r34-adjudicator.md` (impact_third) —
a different numbering namespace, no PCRE/span/self-audit content. `AGGREGATE.md`
(3 days old) also predates this round's reports. No fleet-level index row covers
the shokunin round-34 reports yet.

## Synthesis (one bounded move, proposal only — no edit made)

The round's one cross-lane regularity, hit independently by kaidoku, mori and
kake: a frozen counter can be met by a control that does none of the work.
C2 already absorbs it in design (decoys/mutations, truth-free labels,
before-ceiling 4/37) and in dispatch (the running MutC2Keyed/MutC2NoReader/
MutC2Accept seats). The increment no lane has and chousa could adopt after
freeze — kake's `lookup_control_check.py` is the template — is a committed
check retaining a shortcut gate bundle so `DEADZONE_MATCH` on it is provably
low, making the shortcut rejection re-derivable by one command instead of by
re-running wave seats. Cal axis +, operability axis untouched (report-only row;
contract forbids me landing it).

## Contradictions and limits

- No contradiction found on either claim: no sibling measured PCRE compiled-
  pattern limits or argv per-string ceilings this round, so C2's 32765 boundary
  has neither corroboration nor dispute in the fleet; tsukuroi's exec-surface
  work is environment copying, a different limit. The only named divergence is
  gating-vs-counting on C3 (row 2), which claims-a2 motivates explicitly.
- Per-lane SOURCES namespaces (chousa S065 vs kake S067-S077 vs kumitate
  S001-S020) do not collide; the fleet census validates them per lane.
- I read reports and named sibling tools only; I did not re-run any counter or
  self-audit, and did not open wave artifacts inside sibling lanes. Row ids in
  mori/kake/kumitate rows are quoted from their reports, not re-derived
  [they are their lanes' assertions].
