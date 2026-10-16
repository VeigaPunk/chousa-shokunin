# chousa-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `lessons/round-1.md` | Round-1 gate lesson: real-CLI vs function-under-`set +e` entrypoint gap behind `VERDICT_BEARING_EXPORTS=0/3`, with the gate's candidates/admitted/rejected and the spot-check status | baseline commit `34774a1`; `LOG.md:72-83`; `SCORECARD.md:29`; anchors re-derived from `tools/research-gate.sh` sha256 `e8f07a06…` |
| `knowledge/archived-export-intake.md` | One filled research-record specimen: pinned archive identity, scoped local observations, unresolved external hops, kept rejections, and explicit semantic-verification limits | note opening metadata and integration errata; `.ufo/evidence/round-1/acceptance.json`; `final-intake.json` |
| `knowledge/claim-verification-r2.md` | Round-2 note: `verify-claims` mode design (CLI + JSONL schema, fail-closed source boundary, verbatim-span check, structural marker convention), honest limits, receipts and open items | note metadata (gate sha `03a3324455…`); `fixtures/claims-r2.README.md`; `evidence/README.md` and `evidence/claims-r2-*.log` |
| `knowledge/chain-resolution-r3.md` | Round-3 note: `verify-chain` mode design (CLI + hop citation grammar, `heading`/`quote`/`line` anchors, fail-closed source boundary, exempt-but-counted statuses, per-hop verdicts + `RESOLVED_HOPS=N/M` under the CLEAN/DRIFT/exit contract), what anchor existence does not establish, receipts and open items | note metadata (gate sha `67daf85e…`); `fixtures/chain-r3.README.md`; `evidence/README.md` and `evidence/chain-r3-*.log` |
| `knowledge/anchor-boundaries-r4.md` | Round-4 note: the token-boundary matching semantics now shared by `verify-claims` spans and `verify-chain` quote anchors — one matcher (`tok_span_at`), the documented boundary class (file/line edge, ASCII whitespace, ASCII punctuation; word-internal hyphens/apostrophes not boundaries; non-ASCII fails closed; outer edges only), before→after attack-class measurements, residual limits (token-aligned shortening, non-ASCII neighbours, `_` gluing), receipts and open items | note metadata (gate sha `6b83705b…`, replacing `67daf85e…`); fixtures `claims-r2.jsonl`/`chain-r3.md`/`chain-r3-broken.md` at their pinned shas; `evidence/README.md` and `evidence/boundary-r4-*.log`; the seat's gate-free python re-derivation (86 probes, `INDEPENDENT_CHECK: AGREE`) |
| `knowledge/sweeps-rejections-r5.md` | Round-5 note: `verify-sweeps` mode design (rejection reason + flip-condition presence, sweep `where` tokenization classes, local glob/existence re-run with exempt-but-counted non-local/source-id classes, boundary guard, per-item verdicts + `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L` under the CLEAN/DRIFT/0-1-2 contract), the measured flip presence-vs-quality class table, what a CLEAN sweep does not prove, receipts and open items | note metadata (gate sha `55adb92d…`, replacing `6b83705b…`); fixtures `sweeps-r5.md`/`sweeps-r5-broken.md`/`sweeps-r5-hit.md` at their pinned shas; `evidence/README.md` and `evidence/sweeps-r5-20261016T011543Z-*.log`; the seat's gate-free flip-class/exempt-class probes |
| `knowledge/verify-all-r6.md` | Round-6 note: `verify-all` composition mode — per-section applicability (structure always for a Markdown record; claims only when a surface binds via `--claims`, the input itself as a claims JSONL, or a resolving `## Meta` row; chain on `## Chain`; sweeps on `## Sweeps`/`## Negatives`/`## Rejections`), each section executed as a fresh gate subprocess so its tally equals the solo mode's by construction, composed DRIFT iff any run section drifts, absent sections reported (`state=absent`) and never drifting — plus the append-only `--json` lane manifest (`chousa-verify-all/v1`: UTC, record+gate sha256, per-section state/verdict/tallies, composed verdict and counters), the two transient mid-wave revisions, strace-measured zero network, the omission limit named as the r7 candidate, honest limits and open items | note metadata (gate sha `0c3d51ed…`, replacing `55adb92d…`); fixtures `full-r6.md`/`full-r6-broken.md`/`full-r6-absent.md` + claims companions at their pinned shas; `fixtures/full-r6.README.md`; `evidence/README.md` and `evidence/compose-r6-20261016T020330Z-*.log`; the seat's battery (composed runs, manifest append/prefix probes, 64-case selftest) |
| `knowledge/reference-integrity-r7.md` | Round-7 note: `verify-integrity` mode + fifth composed section — declared-id sets (Sources ids; Claims+Negatives ids; Sweeps ids), the per-section reference cells read (chain `from`/`claim`/`to`; claims `sweep`/`source`/`ref`/`pointer`; negatives `sweep`/`where`; sweeps `claim_id`/`where`; rejections `ref`), one-pass token classification (declared → resolved; undeclared id shape → `REF_UNRESOLVED` drift; non-local → exempt; else not counted), exempt-but-counted classes (non-local namings; the tokens of an exempt-status row), `INTEGRITY refs=N resolved=M unresolved=K` (`refs = resolved + unresolved + exempt`) as the native tally in `sections=5` composed runs, fail-closed semantics under the unchanged 0/1/2 contract, the critic's 29-probe attack catalog dispositioned (caught classes vs named limits, both fail-open and fail-closed directions), the fixture reshape, honest limits and open items | note metadata (gate sha `3ba718bf…`, replacing `0c3d51ed…`, with ten distinct revised shas observed during the wave); fixtures `integrity-r7.md`/`integrity-r7-broken.md` + byte-identical companions at their pinned shas; `fixtures/integrity-r7.README.md`; `evidence/README.md` and `evidence/integrity-r7-20261016T030552Z-*.log`; the seat's battery (fixture pair, selftest stability, regressions, manifest, strace) |
| `fixtures/claims-r2.jsonl` | Pre-registered 17-claim span fixture (13 supported / 2 contradicted / 2 unsupported) whose spans are verbatim bytes of the three archived inputs, with fixed expected verdicts and an independent byte-check | the three archived inputs at fleet commit `0863746e…`; sha256 pins and provenance table in `fixtures/claims-r2.README.md` |
| `fixtures/chain-r3.md` + `chain-r3-broken.md` | Pre-registered chain-hop pair built from real chains in the three archived inputs: a 22-hop positive control (17 resolved / 5 exempt → `RESOLVED_HOPS=17/22`, CLEAN) and a tampered 2-hop control (1/2, DRIFT, `CHAIN_ANCHOR_NOT_FOUND`); the round-1 hole live — `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, hop provenance table and the gate-free byte-check in `fixtures/chain-r3.README.md` |
| `fixtures/sweeps-r5.md` + `sweeps-r5-broken.md` (+ `sweeps-r5-hit.md`) | Pre-registered rejection/sweep pair: a positive control (3 kept rejections with reason + flip_condition, W1 local glob set genuinely empty, W2 non-local → `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, CLEAN, exit 0) and a tampered control (R1 without flip-condition; W1 naming a planted hit file) that DRIFTs, exit 1, naming `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`; the round-1 hole live — r1 `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, provenance tables and the gate-free re-run in `fixtures/sweeps-r5.README.md` |
| `fixtures/full-r6.md` + `full-r6-broken.md` + `full-r6-absent.md` (+ `full-r6.claims.jsonl`, `full-r6-broken.claims.jsonl`) | Round-6 composition fixture set: a positive all-section record (4 sources; 3 resolved hops quote/quote/line; 3 companion claims; 2 complete rejections; one local and one source-id sweep) that composes CLEAN `run=4` with per-section tallies equal to the solo modes (claims 3/3; chain 3/3; sweeps 1/2 + 2/2); a two-defect twin (padded hop-2 quote → `CHAIN_ANCHOR_NOT_FOUND`, `RESOLVED_HOPS=2/3`; R2 flip-condition emptied → `SWEEP_REJECTION_INCOMPLETE`, `REJECTIONS_OK=1/2`) that composes DRIFT `drift-sections=2` naming exactly `chain`+`sweeps` while structure and claims stay green — both CLEAN under r1 `verify` (the hole); and an omission probe (no claims binding, no Sweeps/Negatives rows) that composes CLEAN `run=3 absent=1` | the three archived inputs at fleet commit `0863746e…`; sha256 pins, the pre-registered expected outputs, the recorded composed runs and a re-run recipe in `fixtures/full-r6.README.md` |
| `fixtures/integrity-r7.md` + `integrity-r7-broken.md` (+ `integrity-r7.claims.jsonl`, `integrity-r7-broken.claims.jsonl`) | Round-7 reference-integrity fixture pair: the `full-r6.md` bytes plus a reference mix (resolved hop 4 citing declared source `S4` and claim `C3`; sweeps `SW3` bound to declared claim `C2`) that composes CLEAN `INTEGRITY refs=16 resolved=15 unresolved=0`, and a structural twin differing in exactly five lines with two dangling cells (chain hop 4 `from` `C3`→`S9`, sweeps `SW3` `claim_id` `C2`→`C9`) that every r1–r6 mode passes — both compose CLEAN `sections=4` at the round-6 gate (the hole) while the landed gate drifts the twin with exactly two `REF_UNRESOLVED` and `integrity` the only drifting section | `full-r6.md` lineage (the three archived inputs at fleet commit `0863746e…`; hop-4 anchor `archived-export-intake.md:11`); sha256 pins, the pre-registered after-contract, the measured before-state block and the reshape note in `fixtures/integrity-r7.README.md` |
| `lessons/2026-10-15-claims-span-fidelity.md` | Round-2 lesson: span fidelity is not claim truth — the unchecked `claim` label, strace-measured bounds (no fetch, fail-closed refusals), byte-stable r1 behavior, named debt | gate sha `03a3324455…`; probes summarized in the note; `evidence/claims-r2-*.log` |
| `lessons/2026-10-15-chain-hop-resolution.md` | Round-3 lesson: `RESOLVED_HOPS`/chain CLEAN counts anchor existence only — a numeral tamper drifts; URL and out-of-corpus sources are refused unopened; exemption is record-declared and never checked (a marked hop can hide a resolvable citation); `nearest_line` is a heuristic; carried cosmetic banner item | gate sha `67daf85e…`; probes summarized in the lesson; `evidence/chain-r3-*.log` |
| `lessons/2026-10-15-anchor-token-boundaries.md` | Round-4 lesson: a quote is not any substring — before→after probe partitions on byte-identical anchors (claims 18/18 → 8/18; chain 17/17 → 8/17) with identical miss sets across both modes, the first 40 selftest case lines byte-identical, a gate-free analysis showing every matched r2/r3 fixture span/anchor sits on a line-edge/whitespace/ASCII-punctuation edge, and the class choices with visible consequences (non-ASCII fail-closed, `_` boundary, token-aligned shortening still passing) | gate sha `6b83705b…`; probes summarized in the lesson; `evidence/README.md` and `evidence/boundary-r4-*.log` |
| `lessons/2026-10-16-sweeps-rejections-verdict-bearing.md` | Round-5 lesson: existence is not falsifiability — the structural before-state (both fixtures CLEAN under r1 `verify`), the landed presence/glob checks, what a CLEAN `verify-sweeps` establishes and what it cannot (flip-condition quality, command re-run, rightness of an empty location set), defect notes and named follow-ups | gate sha `55adb92d…`; probes summarized in the lesson; `evidence/sweeps-r5-20261016T011543Z-*.log` |
| `lessons/2026-10-16-verify-all-composition.md` | Round-6 lesson: a composed CLEAN covers only the run sections — absence is reported, not clean (the only reachable absence for a structurally-CLEAN record is the claims surface; `CHAIN_ABSENT`/`CLAIM_TABLE_ABSENT`/`REJECTION_DROPPED` keep the others from vanishing silently), the manifest only appends (sentinel survives, prefix/inode probes, never read back — not an audit trail), tally equality re-derived key-by-key from manifest tallies vs solo summaries, the transient-revision and companion-alias defects, rejected overclaims, and the omission limit as the named r7 candidate | gate sha `0c3d51ed…`; probes summarized in the lesson; `evidence/README.md` and `evidence/compose-r6-20261016T020330Z-*.log` |
| `lessons/2026-10-16-reference-integrity.md` | Round-7 lesson: reference integrity — the before-hole probe table (five single-cell dangling variants composing CLEAN at `0c3d51ed…`, the resolved-`to` control already drifting, the exempt-status probe CLEAN), the landed rule (declared sets, reference cells read, one-pass classification, the exempt-status boundary), what an integrity CLEAN does not establish (kind-correctness, referenced-row truth, unscanned cells, the exempt-status relaxation), the fixture reshape, the ≥6-revision writing-window churn after the section first appeared, and the rejected overclaims | gate sha `3ba718bf…`; probes summarized in the lesson; `evidence/README.md` and `evidence/integrity-r7-20261016T030552Z-*.log` |

Count: 14 entries, seven knowledge notes and seven lessons — `functions.glob`
pattern `corpus/knowledge/*.md;corpus/lessons/*.md`, 2026-10-16. Fixture and
evidence files are coverage-listed but not additional knowledge entries.

## Round-1 evidence

- `evidence/round-1/expected.json`: archive content digests and expected CLI verdicts.
- `../.ufo/evidence/round-1/acceptance.json`: committed gate revision, all full CLI outputs/exits, and draft-intake digest.
- `../.ufo/evidence/round-1/final-intake.json`: final integrated note's structural recheck.
- `../.ufo/evidence/round-1/wave-reconciliation.json`: all 32 preserved member report hashes, routes, runtime-ID errata and integration dispositions.

## Round-2 evidence

- `evidence/README.md`: index of these receipts with pinned gate/fixture shas and a self-contained re-run recipe.
- `evidence/claims-r2-20261015T233027Z-live.log`: r1-gate before-state on the claims file; the frozen fixture run (`VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN`, exit 0); four negative controls (tampered span, external URL, out-of-corpus path, contradicted-without-marker), each exit 1.
- `evidence/claims-r2-20261015T233027Z-fixture.log`: fixture inventory, pinned inputs, and two independent byte-checks (`bad []`; span check `ok=17 mismatch=0`).
- `evidence/claims-r2-20261015T233027Z-gate.log`: round-1 regression at the frozen gate — A/B/C exits and outputs byte-identical to the r1 baseline; `VERDICT_BEARING_EXPORTS=3/3`.
- `evidence/claims-r2-20261015T233027Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (30 cases)`, exit 0; first 20 case lines byte-identical to the r1 baseline (run under a `TMPDIR` scratch while the host `/tmp` quota was intermittent).

## Round-3 evidence

- `evidence/README.md`: index of both receipt sets (round 2 and round 3) with pinned gate/fixture shas and self-contained re-run recipes.
- `evidence/chain-r3-20261015T235623Z-live.log`: before-state on the shipped r2 gate (both chain records CLEAN under `verify`, exit 0 — the tampered control's anchor-missing hop passes structurally); live `verify-chain` (positive `RESOLVED_HOPS=17/22` CLEAN exit 0; broken `1/2` DRIFT exit 1 with `CHAIN_ANCHOR_NOT_FOUND`); four negative controls (appended-byte anchor tamper `semanticsX` → 16/22 DRIFT; out-of-corpus `/etc/hostname` and external URL refused crit, never fetched, 16/22 DRIFT each; an existing-anchor hop re-marked `unresolved` stays exempt but counted, 16/22 CLEAN); zero network (0 socket/connect syscalls); r2 `verify-claims` stdout byte-stable.
- `evidence/chain-r3-20261015T235623Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (40 cases)`, exit 0; case lines 1–30 byte-identical to the r2 selftest.
- `evidence/chain-r3-20261015T235623Z-gate.log`: round-1 regression byte-identical to the frozen baseline (A/B/C each exit 1 with one DRIFT summary; `VERDICT_BEARING_EXPORTS=3/3`).
- `evidence/chain-r3-20261015T235623Z-fixture.log`: fixture inventory and two independent gate-free checks (README byte-check `17/22 bad_hops=[]` and `1/2 bad_hops=['2']`, exit 0; the seat's record checker success, exit 0).
- An earlier cut (`chain-r3-20261015T235411Z-*`) was superseded and removed in this wave: its fixture log recorded a checker `FAIL` summary and a quote-truncation control that still resolved (substring containment). The standing cut re-derives both cleanly; references to the removed names are historical samples, not standing receipts.

## Round-4 evidence

- `evidence/README.md`: index extended to round 4 with pinned gate/fixture shas, the seven single-delta attack controls and a self-contained re-run recipe.
- `evidence/boundary-r4-20261016T002701Z-live.log`: r3-gate structural state (the broken chain record still closes CLEAN under `verify`, exit 0 — the hole this round closes); r1 archive observable each exit 1 with `VERDICT_BEARING_EXPORTS=3/3` and stdout byte-identical to the round-3 gate receipt; intake `CLEAN (… chains=8 …)` exit 0; claims/chain stdout byte-identical to the round-2/3 live receipts; zero network syscalls under `strace`.
- `evidence/boundary-r4-20261016T002701Z-attacks.log`: on the same attack copies, `67daf85e…` closes each CLEAN exit 0 and `6b83705b…` drifts each exit 1 — seven single-delta claims/chain controls (mid-token truncation and padding, hyphen/apostrophe cuts, glued start, glued extra word); the boundary helpers and both call sites printed verbatim; a gate-free checker classifies all 11 copies with `BOUNDCHECK_SUMMARY: all copies agree`, exit 0. Attack copies are ephemeral scratch sha-pinned inside the receipt.
- `evidence/boundary-r4-20261016T002701Z-claims.log`: canonical `VERDICT_BEARING_CLAIMS=17/17` CLEAN exit 0 (unchanged); three claims attacks each `16/17` DRIFT with one `CLAIM_SPAN_NOT_FOUND` at the line-aware report; legit controls `19/19` CLEAN (span followed by `,`; span bounded by `(`/`)` with slashes/apostrophe/hyphen inside).
- `evidence/boundary-r4-20261016T002701Z-chain.log`: canonical `RESOLVED_HOPS=17/22` CLEAN and broken control `1/2` DRIFT (both unchanged); four chain attacks each `16/22` DRIFT with `CHAIN_ANCHOR_NOT_FOUND`; legit control `18/23` CLEAN (quote followed by `,`).
- `evidence/boundary-r4-20261016T002701Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (44 cases)`, exit 0; case lines 1–40 byte-identical to the round-3 selftest; new cases 41–44 = `claims-boundary-pass`/`-fail` and `chain-pass-boundary`/`-fail` on the gate's own `lib/boundary.md` fixture.

## Round-5 evidence

- `evidence/README.md`: index extended to round 5 with pinned gate/fixture shas, the seven single-delta negative controls and a self-contained re-run recipe.
- `evidence/sweeps-r5-20261016T011543Z-live.log`: before-state (the r4 CLI has no `verify-sweeps` — exit 2 — and passes both fixtures structurally, CLEAN exit 0); live canonical run `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN exit 0; broken control DRIFT exit 1 naming `SWEEP_REJECTION_INCOMPLETE` and `SWEEP_CLAIM_FALSE`; seven negative controls (flip emptied, reason emptied, false-emptiness hit, non-local exempt-but-counted, nowhere, out-of-corpus refused crit, undeclared source id); cross-round stdout pairs byte-identical to the round-4 receipts (claims 17/17, chain 17/22, chain-broken 1/2, archives 3/3); zero network (`strace`: 0 syscalls, 992 trace lines).
- `evidence/sweeps-r5-20261016T011543Z-broken.log`: the tampered control under both revisions — r4 `verify` CLEAN exit 0 (the hole) → landed `verify-sweeps` DRIFT exit 1 with both named findings.
- `evidence/sweeps-r5-20261016T011543Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (54 cases)`, exit 0; the first 44 ok-case lines byte-identical to the round-4 receipt (`cmp` YES); new cases 45–54 = the eight `sweeps-*` cases plus two setup exits.
- `evidence/sweeps-r5-20261016T011543Z-fixture.log`: fixture inventory (3 rejections + 2 sweeps; 1 + 1 broken), the archive-set URL emptiness census (zero matches), the record's own W1 glob re-run (zero hits), the planted hit on disk, export pins matching the fixture README, and an independent gate-free re-derivation (`canonical=CLEAN broken=DRIFT`).

## Round-6 evidence

- `evidence/README.md`: index extended to round 6 with pinned gate/fixture shas, the composed-run and manifest receipts and a self-contained re-run recipe.
- `evidence/verify-all-manifest.jsonl`: the lane's first real manifest (sha256 `2ed28f9f…` when checked) — three appended `chousa-verify-all/v1` lines at gate `0c3d51ed…` (positive CLEAN `run=4`; twin DRIFT `drift-sections=2`; omission probe CLEAN `run=3 absent=1`), each carrying UTC, `record_sha256`/`gate_sha256`, per-section tallies and the composed verdict; written with `>>` only (the cut replaced its own earlier rehearsal lines, no other rewrite path).
- `evidence/compose-r6-20261016T020330Z-live.log`: composed runs on all three fixtures, the omission probe and the `--claims` binding; r5-gate-vs-r6-gate stdout byte-identical (frozen clock) on claims 17/17, chain 17/22, chain-broken 1/2, sweeps 1/2 + 3/3 and archive A; `VERDICT_BEARING_EXPORTS=3/3`; zero network (`strace`: 0 network syscalls in 4237 trace lines).
- `evidence/compose-r6-20261016T020330Z-full.log`: the four solo modes, then the composed run on `full-r6.md`, with the side-by-side tally comparison — composed per-section tallies equal the solo summaries (claims 3/3; chain 3/3; sweeps 1/2 + 2/2), CLEAN exit 0.
- `evidence/compose-r6-20261016T020330Z-broken.log`: the twin's two single-line defects localized by the solo modes, then composed DRIFT naming exactly `chain` (`CHAIN_ANCHOR_NOT_FOUND` hop=2, 2/3) and `sweeps` (`SWEEP_REJECTION_INCOMPLETE` id=R2 `missing=flip`, 1/2), exit 1; r5 `verify` on the twin CLEAN exit 0 (the hole).
- `evidence/compose-r6-20261016T020330Z-json.log`: manifest before-state (0 lines), the three appended lines verbatim, append-only prefix compares (all YES), JSON well-formedness, and the exit-2 boundary refusals (missing directory; path is a directory).
- `evidence/compose-r6-20261016T020330Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (64 cases)`, exit 0; the first 54 case lines byte-identical to the round-5 receipt; new cases 55–64 = the `verify-all` family (composed positive; tampered claims; structure-dirty; absent claims surface; claims JSONL as input; two manifest appends with the line-1 hash memo; Meta-bound claims; Meta-declared but missing binding; missing-record exit 2).

## Round-7 evidence

- `evidence/README.md`: index extended to round 7 with the pinned gate/fixture shas, the receipt table, the four single-delta controls (ctl-01…04) and a self-contained re-run recipe (including `verify-integrity`).
- `evidence/verify-all-manifest.jsonl`: lines 3 → 5 — the three round-6 lines byte-preserved (prefix compare YES); the two appended `chousa-verify-all/v1` lines (03:07:26Z `integrity-r7.md` CLEAN `run=5` `drift_sections=0`; 03:07:31Z `integrity-r7-broken.md` DRIFT `run=5` `drift_sections=1`) each parse and carry the integrity tallies (`refs=16 resolved=15/13 unresolved=0/2`).
- `evidence/integrity-r7-20261016T030552Z-live.log`: before-state at the round-6 gate (both r7 fixtures compose CLEAN `sections=4`; `verify-integrity` unknown to it — exit 2, `multiple record paths` — the hole); nine solo-mode pairs at the landed gate vs the round-6 gate byte-identical after ts-normalization with matching rc; `VERDICT_BEARING_EXPORTS=3/3`; manifest 3 → 5 appended with `>>`; zero network (`strace`: 0 network syscalls in 8991 trace lines).
- `evidence/integrity-r7-20261016T030552Z-broken.log`: the twin's two dangling cells, the solo run (`INTEGRITY refs=16 resolved=13 unresolved=2` with exactly the two `REF_UNRESOLVED` lines at `cell=from` (chain row 4, S9) and `cell=claim_id` (sweeps SW3, C9)), the composed run (`drift-sections=1 findings=2`, integrity the only drifting section, the four r6 sections CLEAN with the positive's tallies), the four prior modes still passing the twin (the hole, frozen at the landed revision), and four single-delta controls: ctl-01 claims `sweep`→`SW9` DRIFT (`refs=17 resolved=15 unresolved=1`), ctl-02 rejections `ref`→`S9` DRIFT (`17/15/1`), ctl-03 exempt-status dangling `SW9` CLEAN exempt-but-counted (`16/15/0`), ctl-04 non-local URL exempt (`reason=non-local`, `16/14/0`) CLEAN.
- `evidence/integrity-r7-20261016T030552Z-fixture.log`: inventory and shas, companion `cmp` identical, twin delta = 5 changed lines, the receipts seat's independent checker re-deriving all 16 `REF` lines with reconciliation `diff … EMPTY`, then the positive's composed and solo runs.
- `evidence/integrity-r7-20261016T030552Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (74 cases)`, exit 0; the first 64 case lines byte-identical to the round-6 receipt (`cmp` YES); new cases 65–74 = `integrity-pass`, `-fail-dangling-claim`, `-fail-dangling-source`, `-fail-dangling-chain-claim`, `-fail-dangling-sweep`, `integrity-exempt-counted`, `integrity-fail-counting`, two setup exits, and the composed `all-dangling.md`.

## Known gaps

- CLEAN is mode-dependent, not semantic: `verify` checks record structure (r1);
  `verify-claims` checks byte-span identity at token boundaries plus a declared
  marker (r2 mode, r4 boundary rule); `verify-chain` checks that each unmarked
  resolved hop's source canonicalizes under the boundary and its
  `heading`/`quote`/`line` anchor occurs in the target — `quote` at token
  boundaries (r3 mode, r4 rule), `heading`/`line` by trimmed equality (r3);
  `verify-sweeps` checks rejection reason/flip-condition presence and re-runs
  each named local sweep location set as a glob/existence test (r5);
  `verify-integrity` checks that every id-shaped reference token in the cells
  it reads names a declared row, with named exempt classes outside that
  requirement (r7). None of the five proves semantic support, location binding,
  uniqueness or the source's own truth; chain CLEAN additionally does not prove
  agreement (hop 6 resolves across disagreeing statements) or authorship
  (cross-input hops are co-anchors); sweep CLEAN proves the named location set
  re-measured empty, not that it was the right place to look. `verify-all` (r6)
  composes the modes under one verdict — five sections after r7 — and appends
  a manifest line per run; it adds no check of its own, and its CLEAN covers
  only the sections that ran. No original external source was fetched and none
  may be.
- The round-5 sweep/rejection check is presence- and location-level: a
  non-empty but vacuous flip-condition (placeholder, tautology, never-fires,
  vague) passes, the recorded sweep command is never executed and its prose
  never compared (a sweep can be empty because the wrong glob was named), and
  a record with no rejections/sweeps at all closes `VERIFIED_SWEEPS=0/0`
  CLEAN — section existence stays r1 `verify`'s check. Non-local and
  declared-source-id sweeps stay exempt-but-counted
  (`knowledge/sweeps-rejections-r5.md`).
- The r7 integrity check resolves declared-ness, not kind, truth, spelling or
  completeness: a `claim_id` cell holding a source id resolves (membership in
  the union of declared ids — the gate's own selftest pins it); duplicate
  declarations are tolerated; lowercase (`c1`, `sw1`) and non-id-shape variants
  are invisible; tokens in unscanned cells and companion-file ids are never
  seen; the tokens of an exempt-status row
  (`unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable`) stay
  exempt-but-counted even when undeclared; and prose inside a scanned cell can
  over-extract into a false positive. `refs=N` counts the tokens the extractor
  sees, not every reference a record carries
  (`knowledge/reference-integrity-r7.md`,
  `lessons/2026-10-16-reference-integrity.md`).
- Composed CLEAN inherits every bound above and covers only the RUN sections:
  an absent section is reported, never asserted to have been needed, and for a
  structurally-CLEAN record the only reachable absence measured is the claims
  surface (no binding) — fine-grained omission reporting and the Chain-less
  case remain the named candidates for a future round (round 7 took the
  binding-integrity move instead) alongside the sweeps-with-only-rejections
  representation seam (`knowledge/verify-all-r6.md`,
  `fixtures/full-r6.README.md`).
- The lane manifest appends by discipline, not construction: one `>>` per run
  to the named file, pre-existing foreign lines preserved unvalidated, never
  read back — `record_sha256`/`gate_sha256` bind the recorded bytes and the
  gate, so a later edit to the record falsifies the recorded state
  (`lessons/2026-10-16-verify-all-composition.md`,
  `evidence/verify-all-manifest.jsonl`).
- The round-4 boundary class is syntactic and ASCII-anchored: an occurrence
  whose outer edge abuts a non-ASCII character (`”`, `’`, `—`, `。`, `→`) is a
  miss even when its bytes are real, `_` is a boundary by decision, and
  token-aligned shortening — whole words dropped at genuine edges — still
  resolves; the hardening closes glued truncation/padding, not quoting less
  than the sentence (`knowledge/anchor-boundaries-r4.md`,
  `evidence/boundary-r4-20261016T002701Z-attacks.log`). The r2/r3 marker,
  uniqueness, exemption-truth and external-source limits stand unchanged.
- `knowledge/chain-resolution-r3.md` cites the superseded
  `chain-r3-20261015T235411Z-live.log` for its one-byte-truncated-anchor
  example (that cut was removed in-wave; Round-3 evidence above) — the
  surviving live receipt's control 1 is a padded `semanticsX` variant that
  drifted. The substring-truncation fact itself is re-established by the
  round-4 before-state (`knowledge/anchor-boundaries-r4.md`).
- The mode reads `id/source/span/expect[/marker]` only; the `claim` sentence is
  never compared with its span, so a claim label can assert the opposite of its
  span and still close CLEAN (`lessons/2026-10-15-claims-span-fidelity.md`).
- Round-3 chain checks are single-hop, single-target, text-only, and report
  first occurrence; transitivity and entailment-level verification remain
  unbuilt, the `verify-claims` `claim` label stays unchecked, and exemption is
  the record's own declaration, never verified
  (`knowledge/chain-resolution-r3.md`).
- Carried residuals stand from rounds 2–3: in-root hardlinks bypass path
  canonicalization, there is no size cap on source reads, and the banner still
  reads `research-gate-r1` (cosmetic) (`knowledge/chain-resolution-r3.md`).
- Receipt identity for mission acceptance is still open (round 1): no authentic
  queue taskKey or expected receipt bag exists, so proven receipt-backed rounds
  remain 0. Integrator/operator-owned; this wave ran on the operator's
  in-session direct dispatch, not a fleet wave render.
- Discernment is unchanged: a non-author has not sampled an admit and a reject
  (`lessons/round-1.md` and `lessons/2026-10-15-claims-span-fidelity.md`,
  Spot-check sections). No promotion marks are granted.
- Scope-refusal finding IDs proposed in the old wave never landed in the
  gate; the documentary province boundary is not executable enforcement yet.
- `SKILL.md` now supersedes the old “unchecked grep” cause with the informational
  emitter's false status under CLI errexit. Old corpus/log references remain
  historical and their integration errata identify the superseded assertions.
- The expected-input file pins inputs but is not a separate frozen-run gate.
  Input integrity was checked by the L1 acceptance; no stronger conformance
  or semantic-verification claim is made.

## Frontier

Round 2 ran its pre-registered local-only claim-verification move; routing was
satisfied by the operator's in-session direct dispatch (no fleet render, no
Sighting). It measures span identity, not semantics: the fixture closes
`VERDICT_BEARING_CLAIMS=17/17` CLEAN with four negative controls drifting, and
the r1 archive observable stays byte-stable at `VERDICT_BEARING_EXPORTS=3/3`.
Neither observable saturates its axis.

Round 3 ran its pre-registered chain-hop move on the same direct-dispatch
routing: the r1 structural check closes the tampered chain control CLEAN,
exit 0, while `verify-chain` reports `anchor-missing` and drifts it
(`RESOLVED_HOPS=1/2`), and the 22-hop positive control closes
`RESOLVED_HOPS=17/22` CLEAN with five exempt hops counted. That observable is
not saturated either — exemption is record-declared and unverifiable, one hop
at a time, no transitivity — and the r3 receipts are lane-local logs (no queue
taskKey), so the receipt-identity debt is unchanged.

Round 4 ran the calibration move round 3 registered, on the same
direct-dispatch routing: the pinned observables hold byte-stable (selftest
40 → 44 with case lines 1–40 identical, `VERDICT_BEARING_CLAIMS=17/17`,
`RESOLVED_HOPS=17/22`, broken control `1/2` DRIFT, r1 archive observable
`3/3`), while the attack class flips — truncated/padded/glued copies that
closed CLEAN under `67daf85e…` now drift under `6b83705b…` with the
line-aware reports, and the two modes miss on identical probe sets (claims
5/5 → 2/5 and chain 8/8 → 5/8 in the note's attack fixtures; 86-probe
battery 86/86 → 71/86). That observable is not saturated either: the
boundary class is ASCII-anchored (non-ASCII neighbours fail closed), `_` is a
boundary, and token-aligned shortening still passes, so quote integrity
stays partial and location binding, uniqueness and semantics remain
unverified. The r4 receipts are lane-local logs (no queue taskKey), so the
receipt-identity debt is unchanged.

Round 5 ran the last registered r1 structural move — kept rejections and
negative sweeps become verdict-bearing — on the same direct-dispatch routing:
both fixtures closed CLEAN structurally under `verify` at `6b83705b…` (the
hole), while at `55adb92d…` the canonical record closes
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN and the tampered control DRIFTs
naming `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`, with the pinned
observables byte-stable (selftest 44 → 54, case lines 1–44 identical; claims
17/17; chain 17/22; broken control 1/2; r1 archives 3/3). That observable is
not saturated either: flip-condition presence is screened, not quality
(vacuity passes); the sweep re-run is a glob/existence check over the named
locations, never the recorded command; section absence is still r1's to flag;
and non-local sweeps stay exempt-but-counted. The r5 receipts are lane-local
logs (no queue taskKey), so the receipt-identity debt is unchanged.

Round 6 ran the r5-registered composition move on the same direct-dispatch
routing: at `55adb92d…` no composed verdict and no manifest existed
(`verify-all` degraded to a record argument, exit 2; `--json` was an unknown
flag; no manifest file in the lane), while at `0c3d51ed…` the pre-registered
fixture set composes exactly as registered — the positive all-section record
CLEAN `run=4` with per-section tallies equal to the solo modes (claims 3/3;
chain 3/3; sweeps 1/2 + 2/2); the two-defect twin DRIFT `drift-sections=2`
naming `chain` (`CHAIN_ANCHOR_NOT_FOUND` hop 2, 2/3) and `sweeps`
(`SWEEP_REJECTION_INCOMPLETE` R2, `REJECTIONS_OK=1/2`) while structure and
claims stay green (r1 `verify` alone closes both twins CLEAN — the hole); the
omission probe CLEAN `run=3 absent=1`; the lane manifest holds three appended
`chousa-verify-all/v1` lines (as of the receipts cut); and the pinned
observables hold (selftest 54 → 64 with case lines 1–54 identical; claims
17/17; chain 17/22; broken control 1/2;
r1 archives 3/3). That observable is not saturated either: composition adds a
rollup, not a stronger check, the omission limit — no assertion that an absent
section should have been present; fine-grained omission reporting and the
Chain-less case — is the named r7 candidate, and the manifest is a local
append-only jsonl with no read path or audit-trail guarantee. The r6 receipts
are lane-local logs (no queue taskKey), so the receipt-identity debt is
unchanged.

Round 7 ran the r6-registered binding-integrity move on the same
direct-dispatch routing: at `0c3d51ed…` both r7 fixtures closed CLEAN under
every landed mode (`verify-all` composing `sections=4`), with the twin's two
dangling cells (a hop `from` naming an undeclared source id, a sweeps
`claim_id` naming an undeclared claim id) sitting in cells no r1–r6 mode
inspected — while at `3ba718bf…` the landed `verify-integrity` mode and its
fifth composed section resolve every extracted reference token against the
record's declared ids: the positive composes CLEAN `run=5` (`INTEGRITY
refs=16 resolved=15 unresolved=0`) and the twin composes DRIFT
`drift-sections=1 findings=2` with exactly the two `REF_UNRESOLVED` findings
and integrity the only drifting section; the pinned observables hold (selftest
64 → 74 with case lines 1–64 byte-identical; claims 17/17; chain 17/22;
broken control 1/2; sweeps 1/2 `REJECTIONS_OK=3/3`; r1 archives 3/3); and the
lane manifest gained two integrity lines (3 → 5, prefix preserved).
That observable is not saturated either: the check resolves declared-ness only — kind-blind,
case-sensitive, bounded by the extractor's cell list, exempt-but-counted
behind exempt statuses and non-local namings — so reference integrity stays
partial by its named limits. The r7 receipts are lane-local logs (no queue
taskKey), so the receipt-identity debt is unchanged.

Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0;
operator target at least 100), the non-author admit/reject spot-check,
scope-refusal gate findings, and frozen-replay conformance. Semantic and
external-source verification remain out of scope by design.
