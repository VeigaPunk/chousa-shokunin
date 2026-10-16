# log-entry-draft.md — chousa round 11 (capstone audit), for LOG.md — DRAFT

## Round 11 — capstone audit (goal wave)

**Round 11 — goal-wave admission (2026-10-16).** Motivating evidence: the r10
registration (the chousa capstone audit) and `corpus/README.md` §Known gaps
(the r10 receipts gap "flagged for the capstone audit"). Scope: the deep audit
of rounds 1–10 — evidence chains, receipts, verdicts, the limit ledger,
re-execution of the load-bearing claims at today's bytes, the final debt
register, and a SHONEN readiness assessment without self-attestation. No gate
change (the round's standing rule held; TOOLS/ read-only; gate sha
`46f5ddb3…` unchanged before and after the battery; `git diff` empty).
Wave: this seat (scribe+note) performed the audit battery and wrote
`corpus/knowledge/audit-r11.md` + the round-11 drafts; [PARENT] markers where
acceptance binds.

**Confirmations (re-executions at today's bytes).** Selftest
`PASS (85 cases)`; `GATE_DRIFT: none`; claims-r2 17/17; chain-r3 17/22 +
broken DRIFT naming `CHAIN_ANCHOR_NOT_FOUND`; sweeps-r5 CLEAN + broken DRIFT
naming both classes; integrity-r7 16/15/0 + broken naming S9+C9; full-r6
CLEAN/twin/absent; integrity-r7 composed pair; A/B/C archive records CLEAN
(10/10 claims each; 6/7·6/7·7/8 chains; integrity 13/12/0·14/13/0·15/14/0);
claims-r9 10/10; all six archive-scale controls DRIFT with exactly one
class-named finding each; r1 observable `VERDICT_BEARING_EXPORTS=3/3`; exempt
set 6/6 re-derived; 19-row claims-table audit 18/1 (the live `A-r9.md:50` C3
finding); coverage 27 spans / 23 lines / union 31 re-derived; ledger 71 rows /
38·25·3·1·4 / 30-item queue re-parsed; every cited commit/hash resolved — the
nine round-2–10 evidence commits (+ round-1/records) ancestors of HEAD
`44cbad6`, each round's gate blob sha
matching its commit (`08843552`→`03a33244`→`67daf85e`→`6b83705b`→`55adb92d`→
`0c3d51ed`→`3ba718bf`→`46f5ddb3`, unchanged through r9/r10).

**Defects found (verbatim in `corpus/knowledge/audit-r11.md` §3).** D1: the
r10 controls receipt body carries five of six class runs while its closing
line reads "all six" (the sixth run exists in three committed artifacts; the
audit re-ran it — regeneration candidate). D2: SCORECARD r8 / LOG r8 cite
`-SECTION:sweeps` for the silently-skipped mode; the committed drift receipt
names the tally-key list instead (`+finds -findings` is supported by the
gate's selftest case `drift-one-field-mutant`). D3: LOG r8–r10 evidence
pointers are unreplaced placeholders `LOGPEND8`/`LOGPEND9`/`LOGPEND10` (real
commits `27b55c3`/`ebd04d2`/`5f99fa3` exist and are ancestors). D4: the
r2–r10 SKILL.md registry is uncommitted (last commit touching SKILL.md =
round 1) and its worktree revision carries the malformed gate sha
`46f5ddbf…` ×4 and the interim ledger counts 68/22/27 (on-disk: 71/25/30).
D5: the r10 lesson still cites the superseded ledger revision `f5dc8889…`
(68 rows / 27 queue) vs on-disk `3845709b…` (71 / 30); the note's §5 maps the
rows (9→12, 16→19, 29→32, 53→56). No gate defect surfaced; no gate change.

**Verdicts ([PARENT]-owned; draft).** ADMIT as the capstone audit round:
coverage-of-verification improved (every admitted round's chain re-executed
and reconciled; the defects table produced), calibration improved narrowly
(five record-level defects measured with verbatim evidence; the limit ledger
re-parsed), depth improved (`audit-r11.md` = the consolidated audit artifact +
the final debt register + the readiness assessment), operability/freshness/
adjacency unchanged (no gate change; zero network; corpus read-only; quota
held). No scalar score. Round 11 completes the registered goal sequence; the
open items move to the debt register.

**Boundaries held.** Zero network; research corpus read-only; TOOLS/
untouched; seats committed nothing; scratch cleaned (`/tmp/chousa-r11-scribe`
removed after the battery).

**Receipt identity remains OPEN** (operator side, unchanged; 0 of 10
receipt-backed rounds); this round's evidence is lane-local logs + this
audit, no `task_…` value invented.