# audit-findings-draft.md — chousa round-11 capstone audit: findings draft (scribe+note seat)

seat: scribe+note | round: 11 (capstone audit) | verified-at: 2026-10-16T06:50–07:15Z
scope: this seat re-ran the load-bearing surface (below) from the lane cwd
(`--root ..`), resolved every cited commit/hash, and diffed the receipts'
bytes; no lane file was written by this seat except the round-11 drafts and
`corpus/knowledge/audit-r11.md`. Tools/ was not touched; `git diff --numstat
tools/research-gate.sh` is empty and the gate sha256 is
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` before and
after the battery.

Falsifiable claim under audit: the audit either confirms every admitted
round's evidence chain with measured coverage (receipts, commits, verdicts,
limits, re-executions at today's bytes) or produces the defects table — plus
the final debt register and a SHONEN readiness assessment WITHOUT
self-attestation.

## A. The findings table

| # | claim checked | verdict | evidence (this seat's run, 2026-10-16) |
|---|---|---|---|
| A1 | Evidence commits `c3df458 cc9fe8f a6f3118 e7ab39a 74c533d a1948c3 27b55c3 ebd04d2 5f99fa3` (+ records commits) are ancestors of HEAD `44cbad6` | supported | `git merge-base --is-ancestor <c> HEAD` → all ANCESTOR-OK |
| A2 | Each round's "after" gate blob sha is really the blob at its commit | supported | `git show <c>:tools/research-gate.sh \| sha256sum` → `31b4683`→`08843552`, `c3df458`→`03a33244`, `cc9fe8f`→`67daf85e`, `a6f3118`→`6b83705b`, `e7ab39a`→`55adb92d`, `74c533d`→`0c3d51ed`, `a1948c3`→`3ba718bf`, `27b55c3`/`ebd04d2`/`5f99fa3`→`46f5ddb3` — all MATCH |
| A3 | Gate unchanged through r9/r10/this audit; no gate change without a reported defect | supported | sha unchanged `46f5ddb3…`; `git log -- tools/research-gate.sh` ends at `27b55c3`; worktree == HEAD blob; `git diff` empty before and after the battery |
| A4 | `--selftest` PASS (85 cases) | supported | `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0 |
| A5 | Selftest case lines are byte-stable across receipts and today reproduces r8 | supported | first-N comparisons r1→r2(20), r3(30), r4(40), r5(44), r6(54), r7(64), r8(74) all IDENTICAL; today's first 85 case lines == r8 receipt's first 85 |
| A6 | `--drift` on the committed baseline reads none | supported | `GATE_DRIFT: none` exit 0; baseline sha256 `1c81a6cb…`, 2988 B, header `gate_sha256=46f5ddb3…` (correct) |
| A7 | r2: claims 17/17 CLEAN | supported | `VERDICT_BEARING_CLAIMS=17/17` + `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 …)`, exit 0 |
| A8 | r3: chain 17/22 CLEAN; broken control DRIFT naming anchor-missing | supported | `RESOLVED_HOPS=17/22` CLEAN exit 0; broken → `FINDING CHAIN_ANCHOR_NOT_FOUND … hop=2 …`, `RESOLVED_HOPS=1/2` DRIFT exit 1 |
| A9 | r4: token-boundary rule holds; attack classes fail | supported | receipt evidence (`boundary-r4-*-attacks.log`: each attack CLEAN under the r3 gate, DRIFT under the landed gate; legit controls 19/19 & 18/23 CLEAN); today's selftest includes cases 41–44 PASS |
| A10 | r5: sweeps canonical CLEAN; broken DRIFT naming both classes | supported | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN exit 0; broken → `SWEEP_REJECTION_INCOMPLETE`+`SWEEP_CLAIM_FALSE` DRIFT exit 1 |
| A11 | r6: composed positive CLEAN run=5; twin DRIFT `drift-sections=2` (chain+sweeps); omission probe CLEAN `run=4 absent=1` | supported | re-ran all three (at the r7+ gate the sections compose 5; r6's own receipt records the r6-era `run=4`) |
| A12 | r7: integrity 16/15/0 CLEAN; twin DRIFT with exactly S9 + C9 | supported | `INTEGRITY refs=16 resolved=15 unresolved=0` CLEAN; twin → 16/13/2, `drift-sections=1 findings=2`, two `REF_UNRESOLVED` (S9 chain/from; C9 sweeps/claim_id), exit 1 |
| A13 | r8: baseline catches (field mutant, skipped mode, volatile list) | **defect (partial)** | `+finds -findings` supported (gate selftest case `drift-one-field-mutant`, `tools/research-gate.sh:4071`, PASS today); `-SECTION:sweeps` **not in any committed receipt** — see D2 |
| A14 | r9: A/B/C records compose CLEAN with the declared tallies; claims-r9 10/10 | supported | A: 10/10 · 6/7 · 1/1 4/4 · 13/12/0; B: 10/10 · 6/7 · 1/1 3/3 · 14/13/0; C: 10/10 · 7/8 · 1/1 4/4 · 15/14/0 — all CLEAN exit 0; `VERDICT_BEARING_CLAIMS=10/10` (7/2/1) exit 0 |
| A15 | r9 coverage accounting (27 spans / 23 lines / union 31) | supported | gate-free re-derivation: JSONL spans 17+10=27; distinct first-occurrence lines A10/B7/C6 = 23; union with 19 in-record spans A11/B9/C11 = 31; 24 spans byte-present, 3 byte-absent = exactly the 3 `unsupported` probes (r2 A06, r2 B05, r9 C07) |
| A16 | r9 honest finding `A-r9.md:50` C3 pointer vs span | supported (finding re-confirmed) | 19-row re-derivation: 18 MATCH / 1 MISMATCH — row C3 pointer `:76`, span first occurrence `:86` (archive A) |
| A17 | r10 controls: six classes, each DRIFT with exactly one class-named finding | supported | re-ran all six: exit=1 findings=1 drift-sections=1 each — `CLAIM_SPAN_NOT_FOUND`, `CHAIN_ANCHOR_NOT_FOUND`, `SWEEP_REJECTION_INCOMPLETE`, `SWEEP_CLAIM_FALSE`, `REF_UNRESOLVED`, `NO_QUESTION` |
| A18 | r10 exempt audit 6/6 | supported | solo runs re-derived all six items (A hop7 `コトバンク`/`C1`, B hop7 `arxiv.org`/`C3`, C hop8 `jstage.jst.go.jp`/`C8`); chips byte-present at A:68/:72, B:51/:72, C:103 |
| A19 | r10 ledger counts (71 rows; 38/25/3/1/4; 30-item queue) | supported | table parse: 71 rows, numbering 1..71 contiguous; by-design 38 · carried 25 · closed 3 · finding 1 · operator 4 |
| A20 | Manifest 8 lines, sha `78627e6d…`, untouched by this round | supported | `wc -l`=8; sha256 `78627e6da14c…` == HEAD blob; battery used no `--json` |
| A21 | r1 observable 3/3 at today's bytes | supported | SCORECARD counting command → `VERDICT_BEARING_EXPORTS=3/3` |
| A22 | r1 metrics (gate `08843552…` at commit `31b46832…`; selftest 20; report sha `ada72514…`) | supported | blob sha MATCH; `acceptance.txt` PASS (20 cases); `.ufo/reports/round-1/chousa.md` sha `ada725145904…` matches the LOG claim |
| A23 | Receipts carry the headline verdicts they claim | supported for 8 of 9 families; **r10 controls receipts carry 5 of 6 class runs** | `corpus/evidence/*.log` grep: every family's headline lines match; controls receipt body omits the `C-r9-structure-break` verify-all run while closing "all six" — see D1 |
| A24 | LOG r8–r10 point at their evidence commits | **defect** | `LOGPEND8`/`LOGPEND9`/`LOGPEND10` placeholders — see D3 |
| A25 | SKILL.md registry matches the landed gate | **defect** | uncommitted registry with 4× malformed gate sha `46f5ddbf…` and stale interim ledger counts — see D4 |
| A26 | r10 lesson ↔ ledger consistency | **defect (documented desync)** | lesson cites superseded revision `f5dc8889…` (68 rows / 27 queue / 38/22/3/1/4) vs on-disk `3845709b…` (71 / 30 / 38/25/3/1/4) — see D5 |
| A27 | Cross-round gate-blob regression protection (receipts show earlier blobs recoverable) | supported | `git show cc9fe8f:…` etc. reproduce the before-state gates (e.g. `git show 4835426:…` → `0c3d51ed…`) |
| A28 | Receipt identity (mission-level) | unverifiable at lane level (operator side) | `.ufo/evidence/round-1/receipt-blocker.json`: no queue `taskKey`, no expected bag; all receipts self-declare lane-local |

## B. Defects, verbatim

### D1 — the r10 controls receipt carries five of six class runs

- `corpus/evidence/controls-r10-20261016T055530Z-controls.log` body: five
  `## verify-all run` sections — A-span, A-anchor, B-false-sweep,
  B-rejection-missing-flip, C-dangling-ref — and a five-row summary block;
  the file pins `C-r9-structure-break.md` (`:23`) and MATCHes it (`:70`) but
  contains no verify-all run for it, while the closing line reads verbatim:
  `all six exit 1 with exactly one class-naming finding and one drifted
  section each.` (line 297).
- The sixth run exists committed in `corpus/fixtures/archives-r9/controls/README.md`
  §Measured outputs, `corpus/knowledge/hardening-r10.md` §1, and the r10
  lesson §1; this audit re-ran it (A17) — `NO_QUESTION severity=crit`,
  `drift-sections=1 findings=1`, exit 1.
- Root cause already named in `corpus/README.md` §Known gaps (cut-script read
  loop dropped the unterminated last `controls.tsv` line). Disposition:
  receipts regeneration candidate; the class claim itself is true.

### D2 — SCORECARD r8 / LOG r8 cite `-SECTION:sweeps`; the receipt names tally keys

- `SCORECARD.md:327-328`: "a one-field mutant names `+finds -findings`; a
  silently-skipped mode names `-REJECTIONS_OK -SECTION:sweeps`; a volatile-list
  rewrite names `volatile_fields`." `LOG.md:440-441` repeats
  "silently-skipped mode (-SECTION:sweeps)".
- The committed receipt's line: `GATE_DRIFT: -REJECTIONS_OK -hit -rejections-ok
  anchor-missing native rejections tallies tally` (`pin-r8-…-drift.log:62`,
  exit 1), and `corpus/evidence/README.md` §Round-8 explains why: the mutant's
  `SECTION sweeps` line still prints `state=run verdict=CLEAN` under a stale
  tally, so no `SECTION` token vanishes. A repo-wide search for
  `-SECTION:sweeps` finds only SCORECARD.md:328 and LOG.md:441 — no receipt.
- `+finds -findings` is supported: the gate's selftest case
  `drift-one-field-mutant` asserts exactly those tokens
  (`tools/research-gate.sh:4071`) and passes today. The skip-mutant probes
  elsewhere in the committed trail name `-SECTION:chain` (r8 report draft) and
  `-SECTION:integrity` (`corpus/knowledge/gate-baseline-r8.md:103`), never
  `SECTION:sweeps`.

### D3 — LOG.md rounds 8–10 evidence pointers are placeholders

- `LOG.md:437` `Landed (evidence commit \`LOGPEND8\`)`, `:459` `LOGPEND9`,
  `:480` `LOGPEND10` — committed at `44cbad6`. The real commits exist and are
  ancestors: `27b55c3`, `ebd04d2`, `5f99fa3` (subjects match the rounds); every
  other round's LOG entry names its real sha.

### D4 — the r2–r10 SKILL.md registry is uncommitted and carries wrong tokens

- `git status`: ` M SKILL.md`; `git log -- SKILL.md` last commit = `cfb803a`
  (round 1); diff +347/−10; mtime `2026-10-16 02:49:42 -0300`; HEAD blob
  `66277c8a…` vs worktree `9a6d2719…`. Everything rounds 2–10 landed in the
  gate (7 modes + `--pin`/`--drift`, selftest 85) is documented only in this
  uncommitted revision (and in `corpus/README.md`).
- Malformed tokens: `46f5ddbf…` ×4 (SKILL.md:70, 71, 324, 350) where the gate
  sha is `46f5ddb39d5f…`; `:71` claims the baseline header records
  `gate_sha256=46f5ddbf…` while the committed header verbatim reads
  `# gate_sha256=46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`.
- Stale interim counts: SKILL.md (:364-369) "68 rows in all … by-design 38 ·
  carried 22 · closed 3 · finding 1 · operator 4 — with the 27-item round-11
  audit queue" vs the on-disk ledger 71 rows / 38 · 25 · 3 · 1 · 4 / 30-item
  queue.
- All other hash tokens in the file validate against real prefixes
  (`03a332445585…`, `67daf85ecc49…`, `6b83705b02fe…`, `55adb92d…`,
  `3ba718bf…`, `0c3d51ed…`, `1c81a6cb…`, `31b46832e56a…`).

### D5 — the r10 lesson cites the superseded ledger revision (documented, unreconciled)

- `corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md:7-8` cites
  `hardening-r10.md` at `f5dc8889…`; `:118-128` states "68 rows — by-design 38 ·
  carried 22 · closed 3 · finding 1 · operator 4" and a 27-item queue, and
  spot-checks rows 9/16/29/53. On-disk ledger sha `3845709b…`, 71 rows,
  38/25/3/1/4, 30-item queue; the note's §5 documents the mapping (9→12,
  16→19, 29→32, 53→56). Already named in the note §5 and in
  `corpus/README.md` (row 35) — recorded here as still open.

### Cosmetic / carried (re-confirmed live, no fix by this seat)

- `corpus/evidence/README.md` intro enumerates "rounds 2-9" while the file
  carries the round-10 section (:781+).
- `corpus/fixtures/integrity-r7.README.md:243-245` — stray empty fenced block
  (documented in the r7 receipts as a cosmetic fixture-side observation).
- `corpus/knowledge/chain-resolution-r3.md` cites the removed
  `chain-r3-20261015T235411Z-live.log` (ledger row 24, carried).
- Ledger row 56 (single live `finding`): A C3 pointer `:76` vs span `:86` —
  re-derived 18/19 by this audit (A16).

## C. Battery — verbatim key outputs (this seat, lane cwd)

```text
$ bash tools/research-gate.sh --selftest            → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit 0
$ bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json
                                                     → GATE_DRIFT: none exit 0
$ … verify-claims corpus/fixtures/claims-r2.jsonl --root ..
                                                     → VERDICT_BEARING_CLAIMS=17/17; CLEAN exit 0
$ … verify-chain corpus/fixtures/chain-r3.md --root ..
                                                     → RESOLVED_HOPS=17/22; CLEAN exit 0
$ … verify-chain corpus/fixtures/chain-r3-broken.md --root ..
                                                     → RESOLVED_HOPS=1/2; CHAIN_ANCHOR_NOT_FOUND; DRIFT exit 1
$ … verify-sweeps corpus/fixtures/sweeps-r5.md --root ..
                                                     → VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3; CLEAN exit 0
$ … verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..
                                                     → SWEEP_REJECTION_INCOMPLETE + SWEEP_CLAIM_FALSE; DRIFT exit 1
$ … verify-integrity corpus/fixtures/integrity-r7.md --root ..
                                                     → INTEGRITY refs=16 resolved=15 unresolved=0; CLEAN exit 0
$ … verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..
                                                     → INTEGRITY refs=16 resolved=13 unresolved=2; two REF_UNRESOLVED (S9 chain/from, C9 sweeps/claim_id); DRIFT exit 1
$ … verify-all corpus/fixtures/{full-r6,full-r6-broken,full-r6-absent}.md --root ..
                                                     → CLEAN run=5 / DRIFT drift-sections=2 (chain+sweeps) / CLEAN run=4 absent=1
$ … verify-all corpus/fixtures/integrity-r7.md --root ..   → CLEAN run=5 exit 0
$ … verify-all corpus/fixtures/integrity-r7-broken.md --root .. → DRIFT drift-sections=1 findings=2 exit 1
$ … verify-all corpus/fixtures/archives-r9/A-r9.md --root .. → CLEAN: claims 10/10 · chain 6/7 · sweeps 1/1 4/4 · integrity 13/12/0 exit 0
$ … verify-all corpus/fixtures/archives-r9/B-r9.md --root .. → CLEAN: claims 10/10 · chain 6/7 · sweeps 1/1 3/3 · integrity 14/13/0 exit 0
$ … verify-all corpus/fixtures/archives-r9/C-r9.md --root .. → CLEAN: claims 10/10 · chain 7/8 · sweeps 1/1 4/4 · integrity 15/14/0 exit 0
$ … verify-claims corpus/fixtures/claims-r9.jsonl --root .. → VERDICT_BEARING_CLAIMS=10/10 (7/2/1); CLEAN exit 0
$ six controls (verify-all) → each exit=1 findings=1 drift-sections=1 with its own class id
$ SCORECARD counting command → VERDICT_BEARING_EXPORTS=3/3
$ exempt re-derivation (solo chain+integrity on A/B/C) → 6/6 items, each observed=exempt (A コトバンク/C1, B arxiv.org/C3, C jstage.jst.go.jp/C8)
$ 19-row claims-table audit → 18 MATCH / 1 MISMATCH (A C3 :76 vs span :86)
$ JSONL span presence → r2: 15 present / 2 absent (both unsupported-expect); r9: 9 / 1 (unsupported) → 27 spans: 24 present, 3 by-design absent
```

## D. Coverage counts

- commits: 9 round-2–10 evidence commits (+ round-1 commits and the ten
  records/report commits, `0aa794d`…`44cbad6`), all ancestors of
  HEAD `44cbad6a2f96669361c997bf3df408a2dd364cb5`.
- gate blobs verified: 8 distinct claims (r1–r8) + r9/r10 unchanged.
- receipts: 39 logs under `corpus/evidence/` (claims-r2 4 · chain-r3 4 ·
  boundary-r4 5 · sweeps-r5 4 · compose-r6 5 · integrity-r7 4 · pin-r8 4 ·
  archives-r9 5 · controls-r10 4) + 7 files under `.ufo/evidence/round-1/`.
- ledger: 71 rows / 30-item queue re-parsed; 19-row claims audit; 27-span
  presence; 23/31 line unions.
- re-executions: 1 selftest (85), 1 drift, 4 solo content modes + 3 broken twins,
  3 r6 fixtures, 2 r7 fixtures, 3 archives, 6 controls, 1 r1 observable,
  6 exempt solo runs — all recorded above.