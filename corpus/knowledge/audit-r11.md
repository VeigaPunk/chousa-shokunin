# audit-r11.md — the chousa capstone audit: measured findings, the defects table, the final debt register, and a SHONEN readiness assessment (round 11)

source: this seat's own battery (scribe+note, round 11) over the admitted
rounds 1–10 at today's lane bytes — HEAD
`44cbad6a2f96669361c997bf3df408a2dd364cb5`, gate `tools/research-gate.sh`
sha256 `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`
(unchanged before and after the battery; `git diff --numstat
tools/research-gate.sh` empty), ledger `corpus/knowledge/hardening-r10.md`
sha256 `3845709bae62603aa67b8fc56e15c55b20dd0673b0c9f83d160806196a5018d5`,
manifest `corpus/evidence/verify-all-manifest.jsonl` sha256
`78627e6da14c4bcf1b49c8725a763b9c6ed998b56f03460c1c7d843c15d0814d`
(8 lines, == HEAD blob). This note is the round-11 consolidated audit
artifact; the round's supporting drafts are under
`.ufo/round-11/goal-wave/` (`audit-findings-draft.md`, `report-draft.md`,
`log-entry-draft.md`, `scorecard-verdict-draft.md`). `[PARENT]` marks where
the parent's acceptance/merging binds.

verified-at: 2026-10-16T06:50–07:15Z, from the lane cwd (`--root ..`), fresh
processes, read-only local opens only; nothing fetched; zero lane files
written by this seat outside the round-11 artifacts named above.

recheck (from the lane cwd; each line's expected result in §4):

```sh
bash tools/research-gate.sh --selftest                      # PASS (85 cases)
bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json   # none
bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --root ..          # CLEAN
for c in A-r9-span-not-found A-r9-anchor-missing B-r9-rejection-missing-flip \
         B-r9-false-sweep C-r9-dangling-ref C-r9-structure-break; do
  bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/controls/$c.md --root ..; done
```

Note on method: this seat ran the battery itself and resolved every cited
commit/hash by command — citation was not treated as verification. Wave-seat
reports beyond this seat were not visible to it; any additional wave findings
merge at the parent's integration ([PARENT]).

## 1. Coverage of the audit (what was re-executed, and the counts)

| surface | count | how |
|---|---|---|
| admitted rounds re-audited | 10 (r1–r10) | per-round table in §4 |
| evidence commits resolved/ancestry | 9 round-2–10 evidence commits + round-1 and records commits | `git merge-base --is-ancestor <c> HEAD` → all ANCESTOR-OK |
| gate blobs verified at commits | 8 distinct claims | `git show <c>:tools/research-gate.sh \| sha256sum` MATCH each |
| receipt files covered | 39 logs under `corpus/evidence/` (claims-r2 4 · chain-r3 4 · boundary-r4 5 · sweeps-r5 4 · compose-r6 5 · integrity-r7 4 · pin-r8 4 · archives-r9 5 · controls-r10 4) + 7 files under `.ufo/evidence/round-1/` | existence + headline-line greps |
| verdict re-executions | 1 selftest · 1 drift · 4 solo content modes + 3 broken twins · r6 trio · r7 pair · 3 archive records · claims-r9 · 6 controls · r1 observable (3 `verify` runs) · 6 exempt solo runs | §4 verbatim |
| ledger | 71 rows / queue 30 re-parsed | by-design 38 · carried 25 · closed 3 · finding 1 · operator 4 |
| pointer/claims audits | 19 in-record rows (18 match / 1 mismatch) · 27 JSONL spans (24 present / 3 by-design absent) | gate-free python on archive + fixture bytes |
| coverage accounting | 23 distinct span lines (A10·B7·C6); union 31 (A11·B9·C11) | re-derived, matches `archives-verified-r9.md` §3 |

## 2. Findings table (claim / supported | defect | unverifiable / evidence)

| # | claim checked | verdict | evidence |
|---|---|---|---|
| A1 | the cited evidence/records commits are ancestors of HEAD `44cbad6` | supported | `git merge-base --is-ancestor` over `c3df458 cc9fe8f a6f3118 e7ab39a 74c533d a1948c3 27b55c3 ebd04d2 5f99fa3 44cbad6` → all ANCESTOR-OK |
| A2 | each round's "after" gate blob sha is the blob at its commit | supported | `31b4683`→`08843552` · `c3df458`→`03a33244` · `cc9fe8f`→`67daf85e` · `a6f3118`→`6b83705b` · `e7ab39a`→`55adb92d` · `74c533d`→`0c3d51ed` · `a1948c3`→`3ba718bf` · `27b55c3`/`ebd04d2`/`5f99fa3`→`46f5ddb3` — all MATCH |
| A3 | no gate change r9→r11 without a reported defect | supported | sha unchanged; `git log -- tools/research-gate.sh` ends at `27b55c3`; worktree == HEAD; diff empty |
| A4 | selftest 85 | supported | `RESEARCH_GATE_SELFTEST: PASS (85 cases)`, exit 0 |
| A5 | selftest case lines byte-stable across rounds; today == r8 | supported | first-N prefixes r1→r2(20), r3(30), r4(40), r5(44), r6(54), r7(64), r8(74) all IDENTICAL; today's first 85 == r8's first 85 |
| A6 | committed baseline drifts none | supported | `GATE_DRIFT: none`, exit 0; baseline `1c81a6cb…`, 2988 B, header `gate_sha256=46f5ddb3…` correct |
| A7 | r2 claims 17/17 | supported | `VERDICT_BEARING_CLAIMS=17/17` + CLEAN (13/2/2), exit 0 |
| A8 | r3 chain 17/22; broken DRIFT | supported | 17/22 CLEAN; broken `CHAIN_ANCHOR_NOT_FOUND` hop=2, `RESOLVED_HOPS=1/2`, exit 1 |
| A9 | r4 boundary rule holds; attack classes fail | supported | receipts' attack table (each CLEAN under `67daf85e…`, DRIFT under `6b83705b…`); cases 41–44 PASS today |
| A10 | r5 sweeps CLEAN + broken DRIFT×2 | supported | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN; broken `SWEEP_REJECTION_INCOMPLETE`+`SWEEP_CLAIM_FALSE`, exit 1 |
| A11 | r6 composition: positive/twin/absent | supported | CLEAN `run=5` / DRIFT `drift-sections=2` (chain+sweeps) / CLEAN `run=4 absent=1` (r6-era receipt records `run=4`; at the r7+ gate the same fixtures compose 5 sections) |
| A12 | r7 integrity 16/15/0; twin S9+C9 | supported | CLEAN; twin 16/13/2, `drift-sections=1 findings=2`, `REF_UNRESOLVED` ×2 (S9 chain/from, C9 sweeps/claim_id), exit 1 |
| A13 | r8 catches: field mutant, skipped mode, volatile list | **defect (partial)** | `+finds -findings` supported by the gate selftest case `drift-one-field-mutant` (`tools/research-gate.sh:4071`, PASS today); `-SECTION:sweeps` is in no committed receipt — **D2** |
| A14 | r9 archives CLEAN; claims-r9 10/10 | supported | A 10/10·6/7·1/1 4/4·13/12/0; B 10/10·6/7·1/1 3/3·14/13/0; C 10/10·7/8·1/1 4/4·15/14/0 — all CLEAN exit 0; claims-r9 10/10 (7/2/1), exit 0 |
| A15 | r9 coverage accounting | supported | 27 spans / 23 lines / union 31 re-derived; 3 byte-absent = exactly the 3 `unsupported` probes (r2 A06, r2 B05, r9 C07) |
| A16 | the live `A-r9.md:50` finding | supported (still live) | 19-row re-derivation 18 MATCH / 1 MISMATCH — C3 pointer `:76`, span at `:86` |
| A17 | six controls, one class each | supported | all six exit=1 findings=1 drift-sections=1: `CLAIM_SPAN_NOT_FOUND`, `CHAIN_ANCHOR_NOT_FOUND`, `SWEEP_REJECTION_INCOMPLETE`, `SWEEP_CLAIM_FALSE`, `REF_UNRESOLVED`, `NO_QUESTION` |
| A18 | exempt set 6/6 | supported | re-derived from solo runs; chips byte-present at A:68/:72, B:51/:72, C:103 |
| A19 | ledger 71 / 38·25·3·1·4 / queue 30 | supported | parse of §3.1–3.8 tables: numbering 1..71 contiguous; counts exact |
| A20 | manifest 8 lines, sha unchanged | supported | `78627e6d…` == HEAD blob; battery used no `--json` |
| A21 | r1 observable 3/3 | supported | SCORECARD counting command → `VERDICT_BEARING_EXPORTS=3/3` |
| A22 | r1 gate blob + selftest 20 + report sha | supported | `08843552…` at `31b46832…`; `acceptance.txt` PASS (20 cases); `.ufo/reports/round-1/chousa.md` = `ada725145904…` as logged |
| A23 | receipts carry their headline verdicts | supported, one gap | every family's headline lines match on grep; the r10 controls receipt carries 5 of 6 class runs — **D1** |
| A24 | LOG r8–r10 name their evidence commits | **defect** | `LOGPEND8`/`LOGPEND9`/`LOGPEND10` placeholders — **D3** |
| A25 | SKILL.md registry matches the landed state | **defect** | uncommitted registry; `46f5ddbf…` ×4; stale 68/22/27 counts — **D4** |
| A26 | r10 lesson ↔ ledger consistency | **defect (documented desync)** | lesson cites `f5dc8889…` (68/27; 38/22/3/1/4) vs on-disk `3845709b…` (71/30; 38/25/3/1/4) — **D5** |
| A27 | historical before-states recoverable from git | supported | `git show cc9fe8f:…`→`67daf85e…`, `git show 4835426:…`→`0c3d51ed…` etc. reproduce |
| A28 | mission-level receipt identity | unverifiable at lane level | `.ufo/evidence/round-1/receipt-blocker.json`: no queue `taskKey`/expected bag; all receipts lane-local (operator side) |

## 3. Defects (verbatim evidence)

### D1 — r10 controls receipt carries 5 of 6 class runs, closing line says "all six"

- `corpus/evidence/controls-r10-20261016T055530Z-controls.log` body: five
  `## verify-all run` sections (A-span, A-anchor, B-false-sweep,
  B-rejection-missing-flip, C-dangling-ref) and a five-row summary; it pins
  and MATCHes `C-r9-structure-break.md` (`:23`, `:70`) but has no run for it,
  while `:297` reads verbatim: `all six exit 1 with exactly one class-naming
  finding and one drifted section each.`
- The missing run exists committed in
  `corpus/fixtures/archives-r9/controls/README.md` §Measured outputs,
  `corpus/knowledge/hardening-r10.md` §1, and the r10 lesson §1; this audit
  re-ran it (A17: `NO_QUESTION severity=crit`, exit 1).
- Root cause already named in `corpus/README.md` §Known gaps (cut-script read
  loop dropped the unterminated last `controls.tsv` line). Disposition:
  receipts regeneration candidate; the class claim itself is true.

### D2 — SCORECARD r8 / LOG r8 cite `-SECTION:sweeps`; the receipt names tally keys

- `SCORECARD.md:327-328` verbatim: "a one-field mutant names `+finds
  -findings`; a silently-skipped mode names `-REJECTIONS_OK -SECTION:sweeps`;
  a volatile-list rewrite names `volatile_fields`." `LOG.md:440-441` repeats
  "silently-skipped mode (-SECTION:sweeps)".
- The committed receipt records for the sweeps-skip mutant:
  `GATE_DRIFT: -REJECTIONS_OK -hit -rejections-ok anchor-missing native
  rejections tallies tally` (`pin-r8-…-drift.log:62`, exit 1), and
  `corpus/evidence/README.md` explains why no `SECTION` token vanishes (the
  mutant's `SECTION sweeps` line still prints `state=run verdict=CLEAN` under
  a stale tally). A repo-wide search finds `-SECTION:sweeps` only in
  SCORECARD.md and LOG.md — never in a receipt.
- `+finds -findings` is supported by the gate's own selftest case
  `drift-one-field-mutant` (`tools/research-gate.sh:4071`); other committed
  skip-mutant probes name `-SECTION:chain` (r8 report draft) and
  `-SECTION:integrity` (`gate-baseline-r8.md:103`).
- Disposition: records correction (parent-owned files); the capability claim
  (skipped modes are caught) is supported — only the token citation is wrong.

### D3 — LOG.md rounds 8–10 evidence pointers are placeholders

- `LOG.md:437` ``Landed (evidence commit `LOGPEND8`)``; `:459` `LOGPEND9`;
  `:480` `LOGPEND10` (committed at `44cbad6`). Real commits exist and are
  ancestors: `27b55c3` (r8), `ebd04d2` (r9), `5f99fa3` (r10). Every other
  round names its real sha.
- Disposition: records correction.

### D4 — the r2–r10 SKILL.md registry is uncommitted and carries wrong tokens

- `git status` → ` M SKILL.md`; `git log -- SKILL.md` last commit `cfb803a`
  (round 1); diff +347/−10; mtime `2026-10-16 02:49:42 -0300`; HEAD blob
  `66277c8a…` vs worktree `9a6d2719…`. All rounds 2–10 gate documentation
  (7 modes, `--pin`/`--drift`, 85 cases) exists only in this uncommitted
  revision (plus `corpus/README.md`).
- `46f5ddbf…` ×4 (SKILL.md:70, 71, 324, 350) — the gate sha is
  `46f5ddb39d5f…`; `:71` mis-states the baseline header, which verbatim
  records `# gate_sha256=46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`.
- Stale interim ledger counts at SKILL.md (:364-369): "68 rows in all …
  by-design 38 · carried 22 · closed 3 · finding 1 · operator 4 — with the
  27-item round-11 audit queue" vs on-disk 71 / 38·25·3·1·4 / 30.
- All other hash tokens in the file validate against real prefixes.
- Disposition: [PARENT] integration decision — commit a corrected registry or
  leave it uncommitted; the audit reports, it does not edit (write ownership).

### D5 — the r10 lesson cites the superseded ledger revision (documented, unreconciled)

- `corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md:7-8` cites
  `hardening-r10.md` at `f5dc8889…`; `:118-128` states "68 rows — by-design
  38 · carried 22 · closed 3 · finding 1 · operator 4" and a 27-item queue
  (spot-checks rows 9/16/29/53). On-disk ledger `3845709b…`, 71 rows,
  38/25/3/1/4, 30-item queue; the note's §5 maps rows 9→12, 16→19, 29→32,
  53→56. Already named in the note §5 and `corpus/README.md`; still open.
- Disposition: lesson reconciliation candidate (documentation).

### Cosmetic / carried (re-confirmed live; no fix by this seat)

- `corpus/evidence/README.md` intro enumerates "rounds 2-9" while the file
  carries the round-10 section (`:781+`).
- `corpus/fixtures/integrity-r7.README.md:243-245` — stray empty fenced block
  (r7's own receipts name it as a cosmetic fixture-side observation).
- `corpus/knowledge/chain-resolution-r3.md` cites the removed
  `chain-r3-20261015T235411Z-live.log` (ledger row 24, carried).
- Ledger row 56 (single live `finding`): `A-r9.md:50` C3 pointer `:76` vs
  span `:86` — re-derived 18/19 by this audit; fix-or-absorb pending; any fix
  moves the record's sha and its pins.

## 4. What held — the re-executed chain (verbatim key lines, this seat)

```text
--selftest                    → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit 0
--drift <r8 baseline>         → GATE_DRIFT: none exit 0
verify-claims claims-r2       → VERDICT_BEARING_CLAIMS=17/17 → CLEAN exit 0
verify-chain chain-r3         → RESOLVED_HOPS=17/22 → CLEAN exit 0
verify-chain chain-r3-broken  → RESOLVED_HOPS=1/2 · FINDING CHAIN_ANCHOR_NOT_FOUND hop=2 → DRIFT exit 1
verify-sweeps sweeps-r5       → VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3 → CLEAN exit 0
verify-sweeps sweeps-r5-broken→ FINDING SWEEP_REJECTION_INCOMPLETE id=R1 missing=flip · FINDING SWEEP_CLAIM_FALSE id=W1 hits=1 → DRIFT exit 1
verify-integrity integrity-r7 → INTEGRITY refs=16 resolved=15 unresolved=0 → CLEAN exit 0
verify-integrity integrity-r7-broken
                              → INTEGRITY refs=16 resolved=13 unresolved=2 · REF_UNRESOLVED S9 (chain row 4 from) · REF_UNRESOLVED C9 (sweeps SW3 claim_id) → DRIFT exit 1
verify-all full-r6            → CLEAN  sections=5 run=5 absent=0 findings=0
verify-all full-r6-broken     → DRIFT  drift-sections=2 (chain + sweeps) exit 1
verify-all full-r6-absent     → CLEAN  run=4 absent=1 exit 0
verify-all integrity-r7       → CLEAN  run=5 exit 0
verify-all integrity-r7-broken→ DRIFT  drift-sections=1 findings=2 exit 1
verify-all A-r9.md            → CLEAN  claims 10/10 · chain 6/7 · sweeps 1/1 4/4 · integrity 13/12/0 exit 0
verify-all B-r9.md            → CLEAN  claims 10/10 · chain 6/7 · sweeps 1/1 3/3 · integrity 14/13/0 exit 0
verify-all C-r9.md            → CLEAN  claims 10/10 · chain 7/8 · sweeps 1/1 4/4 · integrity 15/14/0 exit 0
six controls                  → each exit=1 findings=1 drift-sections=1, class id exact (A17)
claims-r9                     → VERDICT_BEARING_CLAIMS=10/10 (7/2/1) → CLEAN exit 0
r1 counting command           → VERDICT_BEARING_EXPORTS=3/3
exempt solo runs (A/B/C)      → 6/6 items observed=exempt (A コトバンク/C1 · B arxiv.org/C3 · C jstage.jst.go.jp/C8)
19-row pointer audit          → 18 MATCH / 1 MISMATCH (A C3 :76 vs span :86)
JSONL span presence           → 27 spans: 24 present / 3 by-design absent (r2 A06, r2 B05, r9 C07)
coverage line unions          → JSONL 23 (A10·B7·C6); union 31 (A11·B9·C11)
ledger parse                  → rows=71 (1..71); 38·25·3·1·4; queue 30
strace (verify-all A-r9.md)   → 0 network syscalls (12541 trace lines; this audit's own)
manifest                      → 8 lines; sha 78627e6d… == HEAD blob
selftest stability            → r1→r8 prefixes IDENTICAL at every step; today first 85 == r8 first 85
```

Methodological note (not a defect): the r9/r10 live receipts record the
case-line-stability result as a `cmp` statement plus the `PASS (85 cases)`
line rather than embedding the case lines; the embedded comparator is the r8
selftest receipt — this audit verified the same comparison directly and it
holds.

## 5. The final debt register

Register composition: (a) the new audit-layer defects D1–D5; (b) the
cosmetic/carried items above; (c) the 30-item hardening limits/queue in
`corpus/knowledge/hardening-r10.md` §3.9 — **unchanged by this audit** (the
counts and the queue were re-parsed and re-derived exact; this register does
not rewrite that map); (d) the four operator items. Nothing else is added;
nothing is silently reclassified.

| id | item | owner | disposition / next move |
|---|---|---|---|
| D1 | r10 controls receipt 5-of-6 runs ("all six" closing line) | receipts/parent | regenerate the receipt or append the sixth run (its verbatim run is in the controls README; re-run recipe works) [PARENT] |
| D2 | SCORECARD r8 / LOG r8 `-SECTION:sweeps` token | records/parent | correct to the receipt's token list (or to `-SECTION:chain`/`-SECTION:integrity` if a skip probe is re-cited); `+finds -findings` stands [PARENT] |
| D3 | LOG r8–r10 `LOGPEND8/9/10` placeholders | records/parent | replace with `27b55c3` / `ebd04d2` / `5f99fa3` [PARENT] |
| D4 | uncommitted SKILL.md registry; `46f5ddbf…` ×4; stale 68/22/27 counts | parent | commit a corrected registry (`46f5ddb3…`; 71/38·25·3·1·4/30) — or ratify the uncommitted state with the defects fixed [PARENT] |
| D5 | r10 lesson cites superseded ledger revision | parent | reconcile the lesson to `3845709b…` (or mark the cited revision superseded inline) [PARENT] |
| C1 | `corpus/evidence/README.md` intro "rounds 2-9" vs file through r10 | parent | cosmetic; fold into the next README touch |
| C2 | `integrity-r7.README.md:243-245` stray fence | parent | cosmetic |
| C3 | r3 note cites the removed receipt log | parent | carried (ledger row 24); fact re-established by r4's before-state |
| F1 | `A-r9.md:50` C3 pointer `:76` vs span `:86` | fixtures/parent | queue item 1 (cheapest-first); fix-or-absorb; a fix moves the record sha and its pins |
| Q | the 30-item hardening queue (25 carried + 1 finding + 4 operator) | lane/parent | `hardening-r10.md` §3.9 — unchanged; the audit hands it forward intact |
| O1 | receipt identity (no queue taskKey/expected bag; 0 of 10 receipt-backed) | operator | bind or re-scope the acceptance model; the mission target (≥100) is untouched by this audit |
| O2 | non-author admit/reject spot-check (discernment) | operator | the one move that can unlock SHONEN boxes (§6) |
| O3 | scope-refusal finding IDs never landed | lane/operator | documented province boundary, not executable enforcement |
| O4 | frozen-replay conformance (`expected.json` pins inputs; not a rerunnable comparator) | operator | unchanged r1/r2 debt |

## 6. SHONEN readiness assessment (without self-attestation)

The standard (`SHONEN.md`): all four boxes must be true for promotion;
per the report contract a box is `[x]` only with a **named non-author
verifier**, `[~]` with a resolvable evidence pointer, `[ ]` if untouched.

| box | measured state (evidence pointer) | verdict |
|---|---|---|
| SKILL.md decision tables, error patterns, checklists, cited sources | The worktree SKILL.md carries a 7-mode gate registry + decision tables + checklists — but it is **uncommitted** and carries `46f5ddbf…` ×4 and stale ledger counts (D4); the committed HEAD revision documents only the r1-era gate (selftest 20). | `[~]` with defects; not `[x]` (no named non-author verifier; artifact needs correction first) |
| ≥1 end-to-end domain task executed and logged in LOG.md | Ten rounds of end-to-end tasks executed and logged with commands/outputs/receipts/commits (this audit re-ran them); but LOG r8–r10 pointers are placeholders (D3), and no queue receipt exists (O1). | `[~]`; not `[x]` |
| Instructions executable by an agent without oral context | Every documented recipe (selftest, drift, the solo content modes, verify-all, controls, archives) executed successfully from the lane cwd by this seat at today's bytes. Executability was demonstrated by an author-lane seat — not a non-author. | `[~]`; not `[x]` |
| No cross-domain bleed (PROVINCE.md accurate) | `PROVINCE.md` unchanged since round 1 (`3282042`); all work in-province (gate/corpus/fixtures); refusals intact; the scope-refusal enforcement IDs remain unbuilt (O3). | `[~]`; not `[x]` |

**Readiness verdict: NOT promotion-eligible.** No box reaches `[x]` (no named
non-author verifier exists anywhere in the lane's records — every round's
"wave seats are the lane" note and `corpus/README.md`'s discernment line say
so), receipt-backed completed rounds remain **0 of 10** (O1), and four
record-level defects (D1–D5) are open. The strongest defensible local
statement is: **ten ADMITTED rounds whose evidence chain was re-verified at
today's bytes by this audit** — self-verification, which by the standard
cannot grant promotion marks, and this note does not claim otherwise.

What would move it (each is external to this lane seat): (1) the operator
binds receipt identity / re-scopes acceptance; (2) a non-author with lane
access samples an admit and a reject (and re-runs the §4 battery); (3) the
parent lands the D2–D5 records corrections and the D1 regeneration; (4) the
`A-r9.md:50` fix-or-absorb decision.

## 7. Operator recommendations (ordered)

1. **Receipt identity**: decide the acceptance model for the ten admitted
   rounds (bind a queue receipt or record the in-session dispatch as the
   accepted routing); the false-zero (0 receipt-backed vs 10 admitted) is the
   lane's largest unresolved ambiguity.
2. **Non-author spot-check**: commission one — it is the single blocking
   item for every SHONEN box.
3. **Records corrections** (cheap, no gate risk): D3 (LOG placeholders), D2
   (r8 token), D5 (lesson reconciliation), C1/C2 cosmetics.
4. **D4 decision**: commit a corrected SKILL.md registry (fix
   `46f5ddbf…`→`46f5ddb3…`; 71/38·25·3·1·4/30) — or explicitly ratify the
   uncommitted state; either way, do not leave a stale registry as the only
   r2–r10 documentation.
5. **D1 regeneration**: re-cut the r10 controls receipt with the sixth run,
   or append a note pointing at the three committed carriers (the class claim
   is already sound).
6. **`A-r9.md:50` fix-or-absorb**: queue item 1; if fixed, re-pin the record
   sha and the README/note pins in the same change.
7. **Gate**: keep `46f5ddb3…` frozen absent a reported defect; any future
   gate change must carry its defect, a receipt, and a re-pin decision.

## 8. What this note does not claim

- No field readiness, no scalar score, no admission verdict (parent-owned);
  no promotion mark.
- No claim about artifacts this seat did not itself open and run; no claim
  that the wave's other seats' reports say anything (they were not visible
  here) — [PARENT] merges any additional findings.
- No semantic/external truth of the archives' sources; nothing was fetched;
  zero network.
- No fix of any defect (report-only; write ownership: this note + the
  round-11 drafts).
- The 30-item queue is not re-narrated here; it stands in
  `hardening-r10.md` §3.9 unchanged.

## Pins (re-derived by this seat)

| artifact | sha256 |
|---|---|
| lane HEAD | `44cbad6a2f96669361c997bf3df408a2dd364cb5` |
| gate (unchanged; == HEAD blob) | `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` |
| baseline `gate-baseline-r8-20261016T033757Z.json` | `1c81a6cb34543bb99c8797a7a0dd8dfbd1f13e3d86ec5b81aa0c7249381a8426` (2988 B) |
| manifest `verify-all-manifest.jsonl` (8 lines) | `78627e6da14c4bcf1b49c8725a763b9c6ed998b56f03460c1c7d843c15d0814d` |
| ledger `hardening-r10.md` (71 rows / queue 30) | `3845709bae62603aa67b8fc56e15c55b20dd0673b0c9f83d160806196a5018d5` (superseded round 12 by `46534902…`, §6 erratum: 71 / 38·23·7·0·3 / queue 26) |
| `SKILL.md` worktree / HEAD blob | `9a6d2719…` / `66277c8a…` (uncommitted; D4) |
| records A/B/C | `dfd2ae1a…` (A, round-12 revision; pre-fix `338918fc…`) / `abfa5290…` / `97be0e69…` |
| archive sources A/B/C | `9033857d…` / `6d8dbddd…` / `e48fe70f…` |
| control shas | `5dedb73b…`(+`0edb78ee…`) · `e3490cf4…` · `b0d488aa…` · `69b7b08f…` · `b24be0f0…` · `21d77e6c…`; controls README `23f47722…` |
## Errata (append-only; round 12, 2026-10-19)

F1 / the §3 carried bullet is closed by fixture correction. Superseded lines
(measurements stand for the pre-fix revision `338918fc…`; only present-tense
status is superseded):

| line | superseded fragment | superseded how |
|---|---|---|
| :70 | "supported (still live) … 18 MATCH / 1 MISMATCH" | finding closed; 18/19 is the pre-fix measurement |
| :165-167 | "Ledger row 56 (single live `finding`) … fix-or-absorb pending; any fix moves the record's sha and its pins" | fix applied; sha moved as predicted |
| :194 | "19-row pointer audit → 18 MATCH / 1 MISMATCH" | post-fix sweep 19/19 (parent re-measured 2026-10-19) |
| :228 | "\| F1 \| … \| queue item 1 … fix-or-absorb" | closed(r12) |
| :261 | "(4) the `A-r9.md:50` fix-or-absorb decision" | decided: fix |
| :280-281 | "6. **`A-r9.md:50` fix-or-absorb** … re-pin the record sha" | executed |
| :8-9, :307 | ledger sha `3845709b…` | superseded by `46534902…` (hardening-r10 §6) |
| :47, :73 | "ledger 71 / … finding 1 … queue 30" | true of `3845709b…`; current: 71 / 38·23·7·0·3 / 26 |
| :309 | "records A/B/C \| `338918fc…`" | A = `dfd2ae1a…`; B/C unchanged |

Correction: A-r9.md line 50 pointer `…A-shokunin-tradition.md:76` → `:86`;
only cell changed; 7210 B / 73 lines unchanged; sha256 `338918fc…` →
`dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d`.
claims-r9.jsonl A11 carries no line suffix; claims-r9.README.md already
pins A:86 — neither moves. Gate moved `46f5ddb3…` → `91a01695…` (round 12:
scope screen, size cap, banner, linear count_nl); the class row 56 names
("no mode pairs a row's path:line with its span's occurrence line") remains
uncovered — only the instance is closed. Verdict-neutrality confirmed by
re-run: `verify-all A-r9 --claims claims-r9.jsonl --root ..` → CLEAN
`sections=5 run=5 absent=0 drift-sections=0 findings=0` at the corrected
bytes (receipt `corpus/evidence/scope-r12-20261019T115519Z-A-fix.log`).

Controls: A-r9-span-not-found.md / A-r9-anchor-missing.md keep `:76` — they
are byte-copies of the pre-fix base `338918fc…`, not of the corrected
revision (`controls/README.md` carries the desync note).
