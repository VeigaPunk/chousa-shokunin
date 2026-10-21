# FxLedgerR20 — fresh history attack on the Round-20 addendum (hardening-r10.md)

Checkpoint: verified at full pin **e93ac71** in private clone /tmp/chousa-r25-FxLedgerR20
(base 0fc037e per contract; corrections applied). Packaging failures recorded: 0fc037e
omitted `tools/research-gate.sh` (landed d8c8cff) and `corpus/evidence/README.md`
(landed e93ac71). Measured gate hash at d8c8cff = e93ac71:
`git show e93ac71:tools/research-gate.sh | sha256sum` → `63a39282a15f19f5…` (bytes
unchanged between the two pins — parent's claim holds). hardening-r10.md is
byte-identical at 0fc037e, d8c8cff, e93ac71 (path-scoped log: last toucher 0fc037e).

## F1 — FALSIFIED: Round-16 addendum preamble "None of these rounds edited this file"
`corpus/knowledge/hardening-r10.md:605` claims rounds 16–23 never edited the file
("path-scoped `git log` between the round landings is empty"). Counterexample:
`git log --oneline a25bde4..6572827 -- corpus/knowledge/hardening-r10.md` →
`edcffba round-20: HTML-comment heading shadow fix …` (only r16–r23 toucher).
`git diff edcffba^ edcffba --stat -- corpus/knowledge/hardening-r10.md` →
`1 file changed, 34 insertions(+)` — the "Independent closure recheck" section
appended at EOF (current :568-599), committed with the round-20 landing itself.
The landed Round-20 addendum (:646 "the round's independent closure recheck (above)")
and seat draft `.ufo/waves/round-25/build/LedgerAddR20.md` (which cites the 34-line
diff) both presuppose the edit; the preamble sentence is false as written for r20
(true for r16–r19, r21–r23). Addendum-text defect, not gate-behavior divergence.

## F2 — gate SHA transition and selftest attribution VERIFIED
- Before/after blobs: `git show 2bb556b:tools/research-gate.sh | sha256sum` →
  `9f1638076915d9bf…`; `git show edcffba:…` → `49b36759bc47ffed…`. Matches addendum
  `hardening-r10.md:644-645`, LOG.md:758, SCORECARD.md:1021-1027.
- Reproduction (private clone worktree at edcffba, not the live lane):
  `bash tools/research-gate.sh --selftest` → `PASS (124 cases, 0 skipped)`, 19.0 s;
  case 123 `claims-cap-eof` exit=0, case 124 `scope-comment-shadow` exit=1 —
  byte-consistent with receipt `corpus/evidence/verify-r20-20261019T180000Z-selftest.log`.
  Receipt is authentic, not transcribed. Demo receipt: before CLEAN → after
  `SCOPE_BOUNTY_ABSORBED` + DRIFT; drift receipt `GATE_DRIFT: none`. `in_comment`
  present at `edcffba:tools/research-gate.sh:425,438-439,451`.

## F3 — no-§3-row / no-round11-queue-delta VERIFIED
edcffba's only change to the file is the +34 append; §3 rows and §3.9
(:160-350) untouched. The recheck itself rewrites nothing: row 9 "Keep the
recorded `closed(r12, partial)` status … unchanged" (:576-578); row 70 "remains
declaration-only" (:583-585); "No historical erratum or disposition counts were
rewritten" (:598-599). Row 70's closure owner is E1's r12 note (:445 `closed(r12)`);
row text (:300) still carries original wording — closures are append-only notes,
consistent with the erratum item 2 recount (38/22/8/0/3, sum 71).

## F4 — named-debt vs original-row distinction (r19 contrast) CORRECT
r19 E8 closed round-16 **named debt** — `corpus/knowledge/verification-r16.md`
seat-20 sweeps-symlink row (disposition "named debt"; preamble "carried to the
round-17 queue") — not a §3 row or §3.9 queue item. E4 (r15) was the genuine
§3.9 **queue-item** closure ("--root /" item entered E3; `mount-alias-r14.md:61`
"queued"→"closed" edited at a14516f). E9 claims no delta of any kind — structurally
proven (F3). Minor imprecision: the R19 addendum says "that row's 'queue for round
17' wording", but the seat-20 row itself does not carry that literal wording (only
the table preamble does); substance unaffected (owner: FxLedgerR19).

## F5 — append-only position + GSHA substitution VERIFIED
`git diff b820e4e e93ac71 -- corpus/knowledge/hardening-r10.md` →
`94 insertions(+), 1 deletion(-)`; the sole deleted line is the disclosed template
slot `(r12 §6) → this revision. Gate \`91a01695…\` → \`${GSHA}…\`. Sites naming`,
filled in place at :488 with `6b17e50c…` =
`git show 5993dc4:tools/research-gate.sh | sha256sum` (round-13 landing) ✓;
Round-14 before-side `6b17e50c… → d8bbd0bf…` (:514) ✓ (e17742f = `d8bbd0bf…`).
Addenda order: R16:602, R17:616, R18:624, R19:631, **R20:640**, R21:648, R22:656,
R23:664, erratum:674 — appended in round order in one commit (0fc037e). No other
historical line changed. In-session gates 76f25105/1abd7eee (LOG.md:736,747) were
never landing blobs; the addendum's landing-to-landing transition is the right cut.

## F6 — E-number/round mapping: no errors in the landed file
E5=r16 d36fd63=`2b64a1c8…` case 111; E6=r17 6e328ce=`c2915f24…` 112–116; E7=r18
a80964c=`6e694881…` 117–119; E8=r19 3eaa0cd=`9f163807…` 120–122; E9=r20 edcffba=
`49b36759…` case 124; E10=r21 8a21559=`bfc291ef…` 125–128; E11=r22 a27128e=
`dfb798b4…` 129–132; E12=r23 f818652=`b5d0f93d…` case 129 (r22 renumber 130–133
consistent: 132+1 case sorting earlier → 133 total; r24 134–136); r24 6572827=
`752e4e38…`. All blobs re-derived via `git show <c>:tools/research-gate.sh |
sha256sum`. Draft `LedgerAddR20.md` labels the item "E5" — integration correctly
renumbered to E9 (observation only; draft superseded).

## F7 — calibration observations (no defect claim)
1. E9's line names case 124 only; the round's landing also added case 123
   (absorbed `tok_span_at` work, LOG.md:736-755, SCORECARD.md:1041-1044) — a
   reader of the addendum alone undercounts the round's selftest delta by one.
2. `--json` delimiter defect was first named at r16 (verification-r16.md seat 24)
   and re-found at r20 (round-20 report seat 69 "DEFECT — `--` delimiter edge");
   `hardening-r10.md:672` "closed round-20 named debt" is true but not first-naming.

Installs: none. All runs in /tmp/chousa-r25-FxLedgerR20 (clone) + /tmp worktree,
removed after use; live lane untouched.

VERDICT: E9's gate/case/no-delta/append-only claims verified against blobs,
receipts and a reproduced selftest; one falsified sentence — the Round-16
preamble's "None of these rounds edited this file" is contradicted by edcffba's
+34-line recheck append (disclosed elsewhere, so an addendum-text fix, not a
regate).
