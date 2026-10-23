# Chronology33 — pre-data discipline attack (wave 2 falsify)

Attacked: the ordering claims for round 33 — (a) design v1 (3b528b9a) and v2 (e3e24ec8) committed
before any candidate receipt; (b) every control receipt (w1/Ctl*, controls/L1-*) has `utc` before
the first candidate receipt (`measure/candidate/c1v2-s3351.json`); (c) every control receipt was
committed in 96be7925, before the candidate commit eb179ec3; (d) no counter or claims.md P1 text
changed after 96be7925. Method: `git log/diff` (read-only) plus a full `utc`/`matched` extraction of
every JSON under `.ufo/waves/round-33/` (340 rows, `w2/Chronology33/receipt-scan.tsv`) and a
per-file add-commit map (`w2/Chronology33/add-map.txt`). All times below are commit %cI (-03:00) or
receipt `utc` (Z); -03:00 == +3h to Z.

## Commit spine (`git log base..tip`)
- 3b528b9a 2026-10-23T05:23:29-03:00 (=08:23:29Z) — design v1 + c1-count.py + claims.md (A).
- e3e24ec8 05:35:29-03:00 (08:35:29Z) — design v2: claims.md (M, adds Design v2 section), c1-count-v2.py (A).
- 96be7925 05:40:56-03:00 (08:40:56Z) — all w1 evidence + L1-v2-rescore receipts (308 files listed).
- eb179ec3 05:41:10-03:00 (08:41:10Z) — C1 candidate (gate 52f07c74…).
- 7f6aeb70 05:43:17-03:00 (08:43:17Z) — candidate receipts + battery + D1-v3 receipts + c2-count-v3.py (A).
- 0fb300b5 05:47:52-03:00 (08:47:52Z) — landed 94a7be5a + integrated receipts. HEAD==master==tip (rev-parse).

## (a) Design-before-data: HOLDS
First candidate receipt `measure/candidate/c1v2-s3351.json`: `utc=2026-10-23T08:41:21Z`, gate 52f07c74.
v1 committed 08:23:29Z, v2 committed 08:35:29Z — 17m52s and 5m52s before the first candidate receipt
respectively; both also strictly precede the candidate commit eb179ec3 (08:41:10Z). L1 "before"
receipts sit inside their design commits: v1 base/oracle utc 08:22:39–08:23:03Z < commit 08:23:29Z;
v2 base/oracle utc 08:34:15–08:34:40Z < commit 08:35:29Z.

## (b) Control utc < first candidate utc: HOLDS for every committed control
Latest utc among committed controls: `CtlC1StripNested--control-c-s3342.json` 08:40:37Z and
`CtlC1NoReader--control-c-s3341/2` 08:40:19Z — all < 08:41:21Z. Every `w1/Ctl*` receipt spans
08:28:42–08:36:08Z; `controls/L1-design*` 08:22:39–08:34:40Z; `controls/L1-v2-rescore/*`
08:39:21–08:40:37Z. Also every committed non-control w1 receipt (ExecNoHarmBase33 08:37:01–13Z,
ExecD1CounterV3 08:30:18–08:31:11Z, AuditC1Truth 08:28:01Z, ReviewerCounter33 08:39:04Z) <
08:41:21Z. And receipt utc < its commit's cI for every commit checked (latest committed receipt
utc 08:40:37Z < 96be7925's 08:40:56Z).

## (c) Commit ordering: HOLDS (with one scope correction)
Every w1/Ctl* and controls/L1-v2-rescore file was added in 96be7925 (add-map.txt); controls/L1-design
in 3b528b9a and controls/L1-design-v2 in e3e24ec8 — all ancestors of eb179ec3. The assignment's
"committed in 96be7925" is exact for the wave-1 + rescore controls; the L1-design receipts are
committed even earlier, in their design commits. Candidate receipts committed in 7f6aeb70
(08:43:17Z) — after both the receipts (08:41:21/23Z) and the candidate commit (08:41:10Z).

## (d) No counter/P1 amendment after 96be7925: HOLDS
`git log base..tip -- corpus/evidence/round33/claims.md c1-count.py c1-count-v2.py` shows only
3b528b9a and e3e24ec8. `git diff 96be7925..0fb300b5` on those three files: empty. `git diff
e3e24ec8..0fb300b5 -- claims.md`: empty — no claims.md text touched even after the v2 design commit.
Worktree hashes match committed blobs: c1-count.py ab6b2ae2…e229, c1-count-v2.py cb354dd1…a514
(= claims.md:5,:103), claims.md 27a4063f…, gate 94a7be5a… (= goal hash). Counters under
corpus/evidence unchanged since their design commits.

## Anomalies / residuals
1. **Untracked post-candidate control receipts.** `.ufo/waves/round-33/controls/L1-mistake/` is
   untracked (`git status ??`; absent from add-map) with utc 08:51:14–08:52:25Z — *after* the first
   candidate receipt and after the landed tip. Its gate `three-key-dup-gate.sh` (86bc8b96…) is a
   wave-2 mutant, not the landed gate: v1 counter scores 144/144 (predicate_holds=true, the F1
   mistake the v2 widening fixes) and v2 scores 144/156. A literal reading of "every control
   receipt (controls/L1-*) has utc before the first candidate receipt" is violated *on disk*; it is
   not committed pre-data evidence and does not affect (a)–(d) as chronology of record. If L1
   integrates it, it lands as post-landing falsify evidence — no kill-rule exposure: the v2 misses
   are on the mutant, not the landed revision.
2. **D1 repair counter committed after its own receipts.** `corpus/evidence/round32/c2-count-v3.py`
   was *added* in 7f6aeb70 (after 96be7925 and after the candidate commit), yet receipts naming its
   hash 6f362ece… exist at 08:30:18–08:31:11Z (w1/ExecD1CounterV3, control gates) and
   08:41:46–08:42:52Z (measure/d1-v3, base+candidate gates) — i.e., the counter ran uncommitted and
   was committed later; committed blob hash equals the receipt `counter_sha256`, so no content
   drift. D1 is a repair, not the claim; the C1 counters were never amended. Flagged as residual
   risk only.
3. **w2 receipts.** Peers' landed-gate runs under `.ufo/waves/round-33/w2/` (untracked): 10 runs on
   gate 94a7be5a (RerunC1a 7701–7703, RerunC1b 4101–4103, MutC1GateDup, MutC1GateString x4,
   MutC1GateDepth), all `TOPLEVEL_FIELD_MATCH=156/156 predicate_holds=true` — consistent with P1;
   none below 156 on the landed revision. I ran no counter runs myself.
4. Worktree carries unrelated peer WIP: `M SKILL.md`, `M corpus/SOURCES.md`, `?? corpus/lessons/round-33.md`
   — not gate/counter/claims; noted, untouched.

## Verdict
**HOLDS** — the committed chronology satisfies all four invariants. Design v1 (08:23:29Z) and v2
(08:35:29Z) precede the first candidate receipt (08:41:21Z) and candidate commit (08:41:10Z); every
committed control receipt has utc < 08:41:21Z and was committed at or before 96be7925 < eb179ec3;
claims.md and both counters are byte-identical to their pre-96be7925 commits (empty diffs,
hash-matched). No violation that falsifies C1. Residuals: the uncommitted `controls/L1-mistake/`
receipts post-date the candidate (literal-reading violation, no committed-evidence impact) and
`c2-count-v3.py` ran before it was committed (repair counter, hash-verified, outside P1).

Report: .ufo/waves/round-33/w2/Chronology33.md
Artifacts: .ufo/waves/round-33/w2/Chronology33/receipt-scan.tsv (b3981e2f…), add-map.txt (bbd5d51b…)
