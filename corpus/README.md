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
| `knowledge/gate-baseline-r8.md` | Round-8 note: the gate's own behavioral baseline — `--pin <path>` writes a normalized baseline of a canonical hermetic invocation (`verify-all record.md --claims claims.jsonl --json manifest.jsonl --root .` inside a gate-written temp fixture, removed after capture, every printed path relative; the fixture's record carries one deliberately dangling `C9` binding so the capture covers `SECTION` (CLEAN and DRIFT), `FINDING`, `VERIFY_ALL`, the composed verdict and the manifest line), `--drift <path>` re-runs it and byte-compares the normalized captures (`GATE_DRIFT: none` exit 0 / named changed tokens exit 1 / missing-malformed exit 2; neither mode prints a `RESEARCH_GATE` line), the declared volatile contract `ts gate_sha256` (shape-scoped mask; the masked set travels in the baseline header; a changed list is itself drift) with its measured rationale (live churn is 1 of 16 field tokens, zero when the clock is pinned; the manifest surface is revision-bound where stdout is behavioral), what it catches measured (a mode-skip copy → `-SECTION:integrity` + `-FINDING:REF_UNRESOLVED` + moved counters while every composed verdict line still closed CLEAN at the entering bytes; an output-field rename → `-refs native tally`; a one-field tamper → the key; guards/refusals exit 2), what it cannot (exit-code-only regressions; behavior outside the canonical invocation; oracle strength — weakened assertions and dropped unasserted fields pass byte-identically; per-row movement outside the composed surface; the masked fields), the committed baseline and re-run recipe, honest limits and open items | note metadata (gate sha `46f5ddb3…`, replacing `3ba718bf…`, with ten observed shas during the wave: docs first, then mechanism, then selftest arms); `evidence/gate-baseline-r8-20261016T033757Z.json` and `evidence/pin-r8-20261016T033757Z-*.log`; `evidence/README.md`; the seat's three-arm battery (full at `c1a45a61…`, post at `bbd90e84…`, settled legs at `30d89dbf…`/`46f5ddb3…`); the lessons-distiller's independent surface measurements |
| `knowledge/scope-refusal-r12.md` | Round-12 note: the declared-scope refusal screen — the `## Meta` `domain`/`scope` trigger contract (table + `key: value` forms, prose never scanned), the three-province phrase lists with the deliberate not-triggers, the report-never-absorb disposition rule, and the named limits (declaration-only detection; solo modes lack the teeth; negations unparsed) | `tools/research-gate.sh` (scope_decl_screen); selftest cases 86-92; receipt `evidence/scope-r12-20261019T115519Z-selftest.log` |
| `knowledge/gate-baseline-r12.md` | Round-12 re-pin record: the recorded reason the r8 baseline was superseded (VERSION v2 banner contract + pin-fixture clean domain row), the unchanged volatile contract, and the re-run recipe | `evidence/gate-baseline-r12-20261019T115519Z.json` (`GATE_DRIFT: none` at pin time); `evidence/scope-r12-20261019T115519Z-drift-r8.log` |
| `knowledge/hardlink-alias-r13.md` | Round-13 note: the hardlink-alias boundary — the symlink/hardlink canonicalization asymmetry, the nlink-based refuse-unread rule (one stat probe serves the r12 size cap too), why partner enumeration was rejected (unsound), and the named limits (TOCTOU, bind mounts, unmeasurable stat, legit in-root families) | `evidence/alias-r13-20261019T123621Z-bypass-{before,after}.log`; selftest cases 99–102 |
| `knowledge/mount-alias-r14.md` | Round-14 note: the mount-alias (cross-device) boundary — the bind-alias gap r13 left open (a bind keeps its path and nlink but not its st_dev), the resolving-root device rule with the lane-fallback control, the nlink → size → device probe order, and the measured named limits (same-device binds stat-invisible, overlay roots, the `--root /` dead-arm queued) | `evidence/mount-r14-20261019T132025Z-bypass-{before,after}.log`; selftest cases 103–106 |
| `knowledge/archives-verified-r9.md` | Round-9 note: the three archived inputs' first full deep verification — one gate-format record per read-only archive (`A-r9.md`/`B-r9.md`/`C-r9.md`: Meta loopback/fetch-none with archive sha pin + claims binding, Question, Sources with the archive as S1 tier `export` and its named external works as pointer-only `secondary` rows, Chain quote/line self-anchors + cross-archive convergence hops + one `blocked-no-fetch` chip hop each, Claims span rows, Negatives/Sweeps, Rejections with reason + flip-condition), each composing CLEAN `sections=5 run=5 absent=0 findings=0 drift=0` at the unchanged gate (claims 10/10; chains 6/7·6/7·7/8; sweeps 1/1 with rejections 4/4·3/3·4/4; integrity 13/12/0·14/13/0·15/14/0) with the raw-DRIFT control for the same bytes unconverted (`run=2 absent=3 drift-sections=1 findings=6`, exit 1); the claims expansion (17 → 46 claim-surface rows, round-9 delta 29; ~one prose line in five under a span check); the reframing risk (record-format distortion: conversion-CLEAN is a property of the conversion and its span selection, not of the archive bytes, and the chain of custody stops at the export) named and mitigated in `fixtures/archives-r9/README.md` and re-derived in the lesson; honest limits and defects (the measured `A-r9.md:50` row-C3 pointer A:76 vs span occurrence A:86 — fix-or-absorb left to the fixtures seat; the in-record `span` column and row `pointer` lines outside every gate check; the `path#quote:text` structure-mode quirk) | note metadata (gate sha `46f5ddb3…` unchanged — fixture-led round, no gate change); fixtures `fixtures/archives-r9/*` and `fixtures/claims-r9.jsonl` at their pinned shas; `evidence/README.md` and `evidence/archives-r9-20261016T045404Z-*.log`; the seat's fresh-process battery and gate-free byte re-derivations |
| `knowledge/hardening-r10.md` | Round-10 note (the round-11 audit's starting map): (1) six archive-scale negative controls, one broken record per defect class — span-not-found → `CLAIM_SPAN_NOT_FOUND` (claims DRIFT `9/10`), anchor-missing → `CHAIN_ANCHOR_NOT_FOUND` (`5/7`), rejection-missing-flip → `SWEEP_REJECTION_INCOMPLETE` (`REJECTIONS_OK=2/3`), false-sweep → `SWEEP_CLAIM_FALSE` (`VERIFIED_SWEEPS=0/1`), dangling-ref → `REF_UNRESOLVED` (`15/13/1`), structure-break → `NO_QUESTION` crit — each composing `drift-sections=1 findings=1` exit 1 with the other four sections CLEAN at their base tallies, plus the measured why `NO_QUESTION` and not `RECORD_SCHEMA_INVALID` (the canonical finding cannot fire alone); (2) the exempt-item audit — the archive records' complete exempt set is 6 items (three `blocked-no-fetch` chip hops — A `コトバンク`, B `arxiv.org`, C `jstage.jst.go.jp` — plus the three integrity tokens on those rows, each a declared claim id), 6/6 justified byte-by-byte against the read-only archives (bare chips alone on their lines; no URL; no local copy), 0 findings, with the class-level limit kept named (an audit covers instances, not the class); (3) the final limit-disposition ledger — every r2–r9 named limit plus the r1-origin debts in 71 rows (`by-design 38 · carried 25 · closed 3 · finding 1 · operator 4`; nothing silently reclassified), reconciled item-by-item with the wave's enumeration, handing forward a 30-item cheapest-first round-11 queue; mid-wave revisions before settling (the scribe's completeness finding: the interim `f5dc8889…` revision missed three r2 carried residuals — in-root hardlinks, no source size cap, cosmetic banner — added as rows 8–10; the final revision is 71 rows / 30 queue items and the standing receipts pin it at `46534902…` (round-12 §6 erratum: 71 / 38·23·7·0·3 / queue 26); the lesson pins the interim revision and the note maps its spot-check rows 9→12, 16→19, 29→32, 53→56); honest folds (`A-r9.md:50` row C3 stays the single finding at `338918fc…`, 18/19 re-derived, fix-or-absorb pending) | note metadata (gate sha `46f5ddb3…` unchanged — fixture-led round, no gate change; controls README `23f47722…`); `fixtures/archives-r9/controls/*` and `lessons/2026-10-16-archive-scale-controls-and-ledger.md` at their pinned shas; `evidence/README.md` and `evidence/controls-r10-20261016T055530Z-*.log` (see Round-10 evidence) |
| `fixtures/claims-r2.jsonl` | Pre-registered 17-claim span fixture (13 supported / 2 contradicted / 2 unsupported) whose spans are verbatim bytes of the three archived inputs, with fixed expected verdicts and an independent byte-check | the three archived inputs at fleet commit `0863746e…`; sha256 pins and provenance table in `fixtures/claims-r2.README.md` |
| `fixtures/chain-r3.md` + `chain-r3-broken.md` | Pre-registered chain-hop pair built from real chains in the three archived inputs: a 22-hop positive control (17 resolved / 5 exempt → `RESOLVED_HOPS=17/22`, CLEAN) and a tampered 2-hop control (1/2, DRIFT, `CHAIN_ANCHOR_NOT_FOUND`); the round-1 hole live — `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, hop provenance table and the gate-free byte-check in `fixtures/chain-r3.README.md` |
| `fixtures/sweeps-r5.md` + `sweeps-r5-broken.md` (+ `sweeps-r5-hit.md`) | Pre-registered rejection/sweep pair: a positive control (3 kept rejections with reason + flip_condition, W1 local glob set genuinely empty, W2 non-local → `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, CLEAN, exit 0) and a tampered control (R1 without flip-condition; W1 naming a planted hit file) that DRIFTs, exit 1, naming `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`; the round-1 hole live — r1 `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, provenance tables and the gate-free re-run in `fixtures/sweeps-r5.README.md` |
| `fixtures/full-r6.md` + `full-r6-broken.md` + `full-r6-absent.md` (+ `full-r6.claims.jsonl`, `full-r6-broken.claims.jsonl`) | Round-6 composition fixture set: a positive all-section record (4 sources; 3 resolved hops quote/quote/line; 3 companion claims; 2 complete rejections; one local and one source-id sweep) that composes CLEAN `run=4` with per-section tallies equal to the solo modes (claims 3/3; chain 3/3; sweeps 1/2 + 2/2); a two-defect twin (padded hop-2 quote → `CHAIN_ANCHOR_NOT_FOUND`, `RESOLVED_HOPS=2/3`; R2 flip-condition emptied → `SWEEP_REJECTION_INCOMPLETE`, `REJECTIONS_OK=1/2`) that composes DRIFT `drift-sections=2` naming exactly `chain`+`sweeps` while structure and claims stay green — both CLEAN under r1 `verify` (the hole); and an omission probe (no claims binding, no Sweeps/Negatives rows) that composes CLEAN `run=3 absent=1` | the three archived inputs at fleet commit `0863746e…`; sha256 pins, the pre-registered expected outputs, the recorded composed runs and a re-run recipe in `fixtures/full-r6.README.md` |
| `fixtures/integrity-r7.md` + `integrity-r7-broken.md` (+ `integrity-r7.claims.jsonl`, `integrity-r7-broken.claims.jsonl`) | Round-7 reference-integrity fixture pair: the `full-r6.md` bytes plus a reference mix (resolved hop 4 citing declared source `S4` and claim `C3`; sweeps `SW3` bound to declared claim `C2`) that composes CLEAN `INTEGRITY refs=16 resolved=15 unresolved=0`, and a structural twin differing in exactly five lines with two dangling cells (chain hop 4 `from` `C3`→`S9`, sweeps `SW3` `claim_id` `C2`→`C9`) that every r1–r6 mode passes — both compose CLEAN `sections=4` at the round-6 gate (the hole) while the landed gate drifts the twin with exactly two `REF_UNRESOLVED` and `integrity` the only drifting section | `full-r6.md` lineage (the three archived inputs at fleet commit `0863746e…`; hop-4 anchor `archived-export-intake.md:11`); sha256 pins, the pre-registered after-contract, the measured before-state block and the reshape note in `fixtures/integrity-r7.README.md` |
| `fixtures/archives-r9/{A,B,C}-r9.md` + `README.md` (+ `fixtures/claims-r9.jsonl` + `claims-r9.README.md`) | Round-9 archive-record set (fixture-led; no gate change): each read-only archive converted to `research-record v1` with every span/anchor machine-extracted from the archive bytes, each composing CLEAN `sections=5 run=5 absent=0` (A/B/C chains 6/7·6/7·7/8 with one exempt chip hop each; sweeps 1/1 with rejections 4/4·3/3·4/4; integrity refs 13/14/15 resolved 12/13/14 unresolved 0; shared claims companion `VERDICT_BEARING_CLAIMS=10/10`), 19 in-record `span` rows byte-checked, 22 in-record hops (19 verified + 3 exempt), 5 inter-archive convergence hops (no cross-citation, re-derived 0/0/0), coverage 17 → 46 claim-surface rows (delta 29), plus the named-and-mitigated reframing risk, the raw-DRIFT control and authoring notes | the three archived inputs at the r2 pins (`9033857d…`/`6d8dbddd…`/`e48fe70f…`, unchanged); record/README shas, the pre-registered expected outputs and the re-run recipe in `fixtures/archives-r9/README.md`; claims provenance and the r2 non-overlap cross-product in `fixtures/claims-r9.README.md` |
| `fixtures/archives-r9/controls/*` (+ `README.md`) | Round-10 archive-scale negative controls (fixture-led; no gate change): six single-defect mutants of the clean archive records — each a scripted byte-copy with exactly one defect cell (plus the `## Meta` `note` row), every one DRIFTing `verify-all` naming exactly its class: one finding, `drift-sections=1 findings=1`, exit 1, every other section CLEAN at its base's tallies, and the clean bases re-verified CLEAN in the same window — `A-r9-span-not-found.md` (+ per-control claims copy: A07 span `four`→`five`, absent from A) → `CLAIM_SPAN_NOT_FOUND` `9/10`; `A-r9-anchor-missing.md` (hop-2 quote → `…certification ladder…`, absent from A) → `CHAIN_ANCHOR_NOT_FOUND` `5/7`; `B-r9-rejection-missing-flip.md` (R2 `flip_condition` emptied) → `SWEEP_REJECTION_INCOMPLETE` `2/3`; `B-r9-false-sweep.md` (SW1 `where` → `research/deep-research-2026-09-28/*.md`, a glob the directory satisfies — 3 hits) → `SWEEP_CLAIM_FALSE` `0/1`; `C-r9-dangling-ref.md` (hop-1 `from` `C1`→undeclared `C9`) → `REF_UNRESOLVED` `15/13/1`; `C-r9-structure-break.md` (`## Question` removed) → `NO_QUESTION` — plus generation asserts (each replacement occurs exactly once; mutated span/anchor asserted absent from the archive bytes), per-file pins, a re-run recipe, and the named does-not-cover set (one class per record / no multi-defect interaction; refusal classes stay with the r2/r3 fixtures; semantic drift invisible (r8); one existence proof per class ≠ a measured fraction of defect space) | bases `dfd2ae1a…`(A, round-12 corrected; pre-fix `338918fc…`)/`abfa5290…`/`97be0e69…` and archives `9033857d…`/`6d8dbddd…`/`e48fe70f…` at their r9 pins; control shas (`5dedb73b…`, claims copy `0edb78ee…`, `e3490cf4…`, `b0d488aa…`, `69b7b08f…`, `b24be0f0…`, `21d77e6c…`) in `controls/README.md`; §1 of `knowledge/hardening-r10.md` and the r10 lesson re-derive the outcomes |
| `lessons/2026-10-15-claims-span-fidelity.md` | Round-2 lesson: span fidelity is not claim truth — the unchecked `claim` label, strace-measured bounds (no fetch, fail-closed refusals), byte-stable r1 behavior, named debt | gate sha `03a3324455…`; probes summarized in the note; `evidence/claims-r2-*.log` |
| `lessons/2026-10-15-chain-hop-resolution.md` | Round-3 lesson: `RESOLVED_HOPS`/chain CLEAN counts anchor existence only — a numeral tamper drifts; URL and out-of-corpus sources are refused unopened; exemption is record-declared and never checked (a marked hop can hide a resolvable citation); `nearest_line` is a heuristic; carried cosmetic banner item | gate sha `67daf85e…`; probes summarized in the lesson; `evidence/chain-r3-*.log` |
| `lessons/2026-10-15-anchor-token-boundaries.md` | Round-4 lesson: a quote is not any substring — before→after probe partitions on byte-identical anchors (claims 18/18 → 8/18; chain 17/17 → 8/17) with identical miss sets across both modes, the first 40 selftest case lines byte-identical, a gate-free analysis showing every matched r2/r3 fixture span/anchor sits on a line-edge/whitespace/ASCII-punctuation edge, and the class choices with visible consequences (non-ASCII fail-closed, `_` boundary, token-aligned shortening still passing) | gate sha `6b83705b…`; probes summarized in the lesson; `evidence/README.md` and `evidence/boundary-r4-*.log` |
| `lessons/2026-10-16-sweeps-rejections-verdict-bearing.md` | Round-5 lesson: existence is not falsifiability — the structural before-state (both fixtures CLEAN under r1 `verify`), the landed presence/glob checks, what a CLEAN `verify-sweeps` establishes and what it cannot (flip-condition quality, command re-run, rightness of an empty location set), defect notes and named follow-ups | gate sha `55adb92d…`; probes summarized in the lesson; `evidence/sweeps-r5-20261016T011543Z-*.log` |
| `lessons/2026-10-16-verify-all-composition.md` | Round-6 lesson: a composed CLEAN covers only the run sections — absence is reported, not clean (the only reachable absence for a structurally-CLEAN record is the claims surface; `CHAIN_ABSENT`/`CLAIM_TABLE_ABSENT`/`REJECTION_DROPPED` keep the others from vanishing silently), the manifest only appends (sentinel survives, prefix/inode probes, never read back — not an audit trail), tally equality re-derived key-by-key from manifest tallies vs solo summaries, the transient-revision and companion-alias defects, rejected overclaims, and the omission limit as the named r7 candidate | gate sha `0c3d51ed…`; probes summarized in the lesson; `evidence/README.md` and `evidence/compose-r6-20261016T020330Z-*.log` |
| `lessons/2026-10-16-reference-integrity.md` | Round-7 lesson: reference integrity — the before-hole probe table (five single-cell dangling variants composing CLEAN at `0c3d51ed…`, the resolved-`to` control already drifting, the exempt-status probe CLEAN), the landed rule (declared sets, reference cells read, one-pass classification, the exempt-status boundary), what an integrity CLEAN does not establish (kind-correctness, referenced-row truth, unscanned cells, the exempt-status relaxation), the fixture reshape, the ≥6-revision writing-window churn after the section first appeared, and the rejected overclaims | gate sha `3ba718bf…`; probes summarized in the lesson; `evidence/README.md` and `evidence/integrity-r7-20261016T030552Z-*.log` |

| `lessons/2026-10-16-gate-behavioral-baseline.md` | Round-8 lesson: a behavioral pin freezes an output surface, not an oracle — the volatile contract is an invocation property (live churn is 1 of 16 tokens (`ts`), zero with `CHOUSA_NOW_EPOCH` pinned; the selftest PASS set has none; the manifest surface is revision-bound via `gate_sha256`), the five scratch mutants on the entering `3ba718bf…` bytes (m1 weakened assertion and m3 dropped header field pass both surfaces byte-identically; m4 renamed tally token and m5 skipped mode keep `CLEAN`/exit 0 while their bytes move; a claim `at=line:1`→`2` shift is invisible to the composed pin but named by solo `verify-claims`), the landed mechanism verified at `30d89dbf…` with spot-checks at `46f5ddb3…`, the two transient fail-closed selftest FAILs under 32-seat `/tmp` load (non-reproduced), and the applying rules (record the invocation; pin surfaces deliberately; pair the drift ritual with a source diff; never export a mask across gates) | gate sha `3ba718bf…` (surface measurements), `30d89dbf…`–`46f5ddb3…` (landed mechanism); probes summarized in the lesson; `evidence/README.md` and `evidence/pin-r8-20261016T033757Z-*.log` |

| `lessons/2026-10-16-verifying-conversion-not-original.md` | Round-9 lesson: verifying a conversion is not verifying the original — six measurements (the same bytes DRIFT raw and CLEAN converted; the conversion authors structure the source cannot supply — zero `#`/pipe-table lines in the archives vs 9 headings + 44/45/48 table rows per record, so only `quote`/`line` anchors can resolve; the chain of custody stops at the export — zero `http` strings, citation chips as exempt `blocked-no-fetch` hops; coverage is a selection — 27 gate-checked spans over 23 distinct source lines, union 31 of 109 prose lines; row anchors only partially checked — a nonexistent-line pointer probe composes CLEAN, and the round's own `A-r9.md:50` row C3 misses its line (18/19 audit); derived structure adds claims the source never made and cuts remove answers), the durable rules (ship the raw-DRIFT control beside any conversion-CLEAN; report spans-over-lines; record which anchor kinds the source supports; selection is the conversion's unchecked act; pair row anchors with span companions; keep derived artifacts at their true tier) | gate sha `46f5ddb3…` (unchanged); probes summarized in the lesson; fixture pins in `fixtures/archives-r9/README.md`; `evidence/archives-r9-20261016T045404Z-*.log` |
| `lessons/2026-10-16-archive-scale-controls-and-ledger.md` | Round-10 lesson: a defect class is proven at the scale you certify — six measurements (the production-shape mutants, with the silence of the other four sections as part of the evidence — `drift-sections=1 findings=1` is two-sided; minimal shape-preserving mutations shipped with their provenance trio — parent sha, control sha, byte-delta, same-window CLEAN re-derivation; the counted-but-never-verified exempt set audited instance-by-instance against source bytes (6/6), class-level limit kept named; the ledger as terminal disposition so carried residuals stop being re-narrated; when the canonical finding cannot fire alone, pick the smallest edit that isolates one finding — `NO_QUESTION` over `RECORD_SCHEMA_INVALID`) and the durable rules (mutate a production record, one defect per control; keep mutations minimal and shape-preserving; enumerate the counted-but-never-verified items; give every limit a terminal disposition in ONE ledger; a hardening round should end by producing the next audit's starting map) | gate sha `46f5ddb3…` (unchanged); probes summarized in the lesson; control/record/archive pins in `fixtures/archives-r9/controls/README.md`; the lesson pins the note's interim revision (`f5dc8889…`, 68 rows / 27-item queue) and the note's §5 maps its spot-check rows to the final (71/30); see Round-10 evidence |

Count: 20 entries, ten knowledge notes and ten lessons — `functions.glob`
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

## Round-8 evidence

- `evidence/README.md`: index extended to round 8 with the pinned gate/baseline shas, the baseline contract table, the six baseline controls and the mutant-gate arm, and a self-contained re-run recipe (`--pin`/`--drift`/`--selftest`).
- `evidence/gate-baseline-r8-20261016T033757Z.json`: the lane's committed behavioral baseline (sha256 `1c81a6cb…`, 2988 B, 19 lines) — the `chousa-gate drift baseline v1` text format: header (`pinned_ts=2026-10-16T03:38:57Z`; the filename stamp is `20261016T033757Z`; `gate_sha256=46f5ddb3…`; `volatile_fields=ts gate_sha256`; the canonical command line), then the normalized canonical capture (five `SECTION` lines including the deliberate integrity `FINDING REF_UNRESOLVED … id=C9` and the composed DRIFT roll, `ts`/`gate_sha256` masked `<V>`, `record_sha256` unmasked), then the masked `--json` manifest line.
- `evidence/pin-r8-20261016T033757Z-pin.log`: before-state (0 baselines committed; the r7 gate rejects both flags — exit 2, no file); the committed pin (`GATE_PIN: ok …`, exit 0); the header and body verbatim; hermetic re-pins (`cmp` IDENTICAL for pin1 = pin2 and pin1 = pin3, the latter cut after 75 s of live churn); CLI refusals (no PATH ×2, both flags, unwritable directory) each exit 2.
- `evidence/pin-r8-20261016T033757Z-drift.log`: `GATE_DRIFT: none` exit 0 on the committed baseline and again after 75 s of live churn; the baseline controls (severity mutant → `GATE_DRIFT: severity` exit 1; missing/empty/junk/marker-deleted → exit 2; volatile-list rewrite → `GATE_DRIFT: volatile_fields` exit 1); the sweeps-silently-skipped mutant gate (its `SECTION sweeps` line still reads `state=run verdict=CLEAN` under a stale tally) → exit 1 naming `-REJECTIONS_OK -hit -rejections-ok anchor-missing native rejections tallies tally`.
- `evidence/pin-r8-20261016T033757Z-live.log`: cross-round no-harm (14/14 mode pairs byte-identical after ts-normalization with matching rc), `VERDICT_BEARING_EXPORTS=3/3`, zero network (strace: 3759 trace lines, 0 network syscalls under `--pin`), `verify-all-manifest.jsonl` untouched (`9620946f…` before/after), gate sha stable across the battery (`46f5ddb3…` → `46f5ddb3…`).
- `evidence/pin-r8-20261016T033757Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (85 cases)`, exit 0; the first 74 case lines byte-identical to the round-7 receipt (`cmp` YES); new cases 75–85 = `pin-clean`, `drift-clean`, `drift-volatile-churn`, `drift-one-field-mutant`, `drift-missing`, `drift-malformed`, `drift-volatile-list`, `setup-pin-no-path`, `setup-drift-no-path`, `setup-pin-unwritable`, `setup-pin-drift-exclusive`.

## Round-9 evidence

- `evidence/README.md`: index extended to round 9 with the pinned gate/fixture shas, the receipt table (receipt shas included), the manifest before → after and a self-contained re-run recipe — "no gate file changed" measured (working-tree sha equals the HEAD blob, `git diff --numstat` empty).
- `evidence/archives-r9-20261016T045404Z-live.log`: before-state (each raw archive under `verify-all` DRIFT `run=2 absent=3 drift-sections=1 findings=6`, exit 1 — an export is not a record), the no-gate-change evidence (gate `46f5ddb3…` == HEAD blob), `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0 with case lines 1–85 byte-identical to the r8 receipt, `GATE_DRIFT: none` exit 0 on the committed r8 baseline, the r1 observable `VERDICT_BEARING_EXPORTS=3/3`, prior fixtures held (claims-r2 17/17; chain-r3 17/22 and broken 1/2; sweeps-r5 1/2 + broken DRIFT; full-r6 CLEAN + twin `drift-sections=2`; integrity-r7 `16/15/0` and twin `16/13/2`), the manifest 5 → 8 lines (first 5 preserved byte-for-byte) with all three appended `chousa-verify-all/v1` lines verbatim, zero network (`strace`: 43799 trace lines, 0 network syscalls), inter-archive crossing counters (A→B:1 A→C:1, B→A:1, C→A:1 C→B:1), and pin stability across the battery (gate/records/claims/archives `STABLE: YES`).
- `evidence/archives-r9-20261016T045404Z-A.log` / `-B.log` / `-C.log`: per-record receipts — README-declared vs measured shas MATCH (record + archive source); a gate-free checker re-derives each record's claim spans (A 5/5, B 6/6, C 8/8 verbatim and boundary-delimited, with occurrence lines) and each chain hop with `RECONCILE: EMPTY` against solo `verify-chain`; the `verify-all` run (claims 10/10 each; chains 6/7·6/7·7/8; sweeps 1/1 with rejections 4/4·3/3·4/4; integrity 13/12/0·14/13/0·15/14/0) exit 0 with its manifest append; all contract assertions pass; 0 `FINDING` lines per record.
- `evidence/archives-r9-20261016T045404Z-claims.log`: claims surface — gate-free 10/10 and `RECONCILE: EMPTY` against solo `verify-claims`; live run `VERDICT_BEARING_CLAIMS=10/10` CLEAN exit 0 with the at=line values (54, 71, 78, 82, 86, 57, 68, 75, -, 92) matching the README's declaration; the r2 non-overlap cross-product `containment_pairs=0`; stats (10 = A 5 · B 3 · C 2; supported 7 / contradicted 2 / unsupported 1; duplicate-ids 0).
- `evidence/verify-all-manifest.jsonl`: lines 5 → 8 — the five prior lines byte-preserved (prefix compare YES); the three appended `chousa-verify-all/v1` lines (04:54:11/19/27Z, records A/B/C at their pinned shas, gate `46f5ddb3…`) each parse, pin per-section tallies and compose CLEAN `sections_run=5 sections_absent=0 drift_sections=0`.

## Round-10 evidence

- `evidence/README.md`: index extended to round 10 (stamp `20261016T055530Z`) with the receipt table and shas, the six-control class table, the exempt-audit table, the ledger summary and a self-contained re-run recipe — "no gate file changed" measured (working-tree sha equals the HEAD blob); it also records the withdrawn first cut (stamp `054941Z`) and its comparator artifact (the case-line comparison had run against the r9 live receipt, which embeds no case lines; the standing comparator is the r8 selftest receipt's embedded case list, and the re-run reads byte-identical).
- `evidence/controls-r10-20261016T055530Z-controls.log`: before-state (controls/ absent at HEAD; the pre-r10 negatives were the small `chain-r3-broken.md`/`sweeps-r5-broken.md`/`full-r6-broken.md`/`integrity-r7-broken.md` records), README-declared vs measured pins (all MATCH), and per-class diff + verify-all + assertions for five of the six classes — span-not-found `CLAIM_SPAN_NOT_FOUND` (`9/10`), anchor-missing `CHAIN_ANCHOR_NOT_FOUND` (`5/7`), false-sweep `SWEEP_CLAIM_FALSE` (`0/1`), rejection-missing-flip `SWEEP_REJECTION_INCOMPLETE` (`2/3`), dangling-ref `REF_UNRESOLVED` (`15/13/1`) — each exit 1 with exactly one `RESEARCH_GATE: DRIFT` summary and `drift-sections=1`; plus the positive arm (parents A/B/C still CLEAN in the same window). The sixth control (`C-r9-structure-break` → `NO_QUESTION`) is pinned and MATCHed here, but its run section is absent from the receipt body while the closing line reads "all six" — the run itself is carried by `controls/README.md` §Measured outputs, `knowledge/hardening-r10.md` §1 and the lesson §1 (see Known gaps).
- `evidence/controls-r10-20261016T055530Z-exempt.log`: solo `verify-chain`/`verify-integrity` lines for A/B/C (chains 6/7·6/7·7/8; integrity 13/12/0·14/13/0·15/14/0, each CLEAN with the exempt item counted), the gate-free byte justification of all six items (`EXEMPT-AUDIT … items=2 justified=2 findings=0` per record) and the raw grep witnesses (A:68/:72 `コトバンク`; B:51/:72 `arxiv.org`; C:103 `jstage.jst.go.jp`).
- `evidence/controls-r10-20261016T055530Z-ledger.log`: the note pin `3845709b…` and every cited pin MATCH; the ledger's own tables re-derived gate-free (`LEDGER rows=71 numbering=1..71`; `by-design=38 carried=25 closed=3 finding=1 operator=4`; `queue claimed=30 computed=30` — MATCH) and the single finding re-derived from bytes (`ROW id=C3 pointer-line=76 span-line=86 MISMATCH`; all three records 19 rows, 18 MATCH / 1 MISMATCH); closed-row evidence re-run (row 12 r4 boundary holds in both modes; rows 31/37 in-wave) and the holds (selftest 85 PASS; `GATE_DRIFT: none`).
- `evidence/controls-r10-20261016T055530Z-live.log`: gate == HEAD blob (`46f5ddb3…`; `git diff --numstat` 0 lines); `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0 with case lines 1–85 byte-identical to the r8 selftest receipt (0 FAIL-case lines; re-verified here by an independent byte compare); `GATE_DRIFT: none` exit 0 on the committed baseline; `VERDICT_BEARING_EXPORTS=3/3`; prior fixtures held (claims-r2 17/17; claims-r9 10/10; chain-r3 17/22 and broken 1/2; sweeps-r5 1/2 `REJECTIONS_OK=3/3` and broken DRIFT; full-r6 CLEAN and twin `drift-sections=2`; integrity-r7 `16/15/0` and twin `16/13/2`); the controls summary and the exempt summary; `verify-all-manifest.jsonl` untouched (8 lines, sha `78627e6d…` before = after); zero network (`strace`: 108440 trace lines, 0 network syscalls); pin stability across the battery (`STABLE: YES`); identity footer (lane-local logs; no `task_…` invented).

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
- The r8 `--pin`/`--drift` baseline is a gate-self check, not a record mode:
  it freezes the canonical invocation's output (the gate-written fixture's
  composed `verify-all` bytes plus the manifest line; `ts` and `gate_sha256`
  masked) and nothing else. Measured blind to exit-code-only regressions (a
  copy whose `verify_all` always returns 0 reads `none`), behavior outside
  the canonical invocation (an `AGG_ERE` default edit reads `none`), oracle
  strength (weakened selftest assertions and dropped unasserted fields pass
  byte-identically — the PASS set carries case names and exits only), and
  per-row movement outside the composed surface (a claim `at=line:1`→`2`
  shift is invisible to the pin while solo `verify-claims` names it); the
  masked fields are declared blind spots, and a changed volatile list is
  itself drift. The baseline does not age with the host (the gate reads no
  host state), so a red result is a gate behavior change: re-pin is a
  recorded act with a reason, deliberately paired with a source review of
  the gate at the same SHA (`knowledge/gate-baseline-r8.md`,
  `lessons/2026-10-16-gate-behavioral-baseline.md`).
- Two selftest runs during the r8 writing window reported `FAIL (1/84)` at
  the new pin/drift arms, on different cases with transient signatures (a
  capture `rc=2` while the wave's `/tmp` was under 32-seat load; an `rc=127`
  while the gate file was being rewritten mid-run) — both fail-closed,
  neither reproduced, and the committed receipt reads `PASS (85 cases)`
  (`lessons/2026-10-16-gate-behavioral-baseline.md` §Limits).
- The round-9 composed CLEAN is a property of the conversion and its span
  selection, not of the archive bytes: the same bytes DRIFT raw
  (`run=2 absent=3 drift-sections=1 findings=6`, exit 1) and compose CLEAN
  converted, so the raw-DRIFT control must travel with any conversion-CLEAN
  claim. Coverage is a selection — 27 gate-checked spans over 23 distinct
  source lines, union 31 of 109 prose lines (roughly one line in five) — and
  the in-record claims-table `span` column and row `pointer` lines sit outside
  every gate check: a nonexistent-line pointer probe composes CLEAN, and the
  round's own `A-r9.md:50` (row C3) points at `A:76` while its span occurs at
  `A:86` (closed at round 12: the pointer was corrected and the live record sha moved to `dfd2ae1a…`; the class — no mode pairs a pointer line with its span's occurrence line — stays a named non-coverage)
  (`knowledge/hardening-r10.md`).
  The conversion authors what the source cannot supply (the archives hold zero
  `#`/table lines; each record carries 9 headings and 44/45/48 table rows),
  `text` cells paraphrase, the exports are cut mid-response, and the chain of
  custody stops at the export — an absent section in an archive is not an
  answer of "no", and no CLEAN on these records speaks about the sources the
  archives cite (`knowledge/archives-verified-r9.md`,
  `lessons/2026-10-16-verifying-conversion-not-original.md`,
  `fixtures/archives-r9/README.md`).
- A `to` cell written as `path#quote:text` drifts structure mode
  (`CHAIN_HOP_UNRESOLVED` — the structure pointer check cuts a pointer at its
  first `:`); the round-9 records use a declared source id or a clean local
  path plus `anchor_kind`/`anchor` columns instead (measured in the round's
  authoring probe; documented, deliberately unfixed — no gate change this
  round) (`fixtures/archives-r9/README.md` §Authoring notes).
- The r2–r9 limit trail now has one terminal disposition per named limit:
  `knowledge/hardening-r10.md` §3 dispositions every limit named across
  rounds 2–9 plus the r1-origin debts in 71 rows (by-design 38 · carried 25 ·
  closed 3 · finding 1 · operator 4; nothing silently reclassified), reconciled
  item-by-item against the wave's enumeration, and hands round 11 a 30-item
  cheapest-first audit queue (mid-wave revisions before settling: the interim
  revision missed three r2 carried residuals, added as rows 8–10 — the counts
  re-derived here). This
  maps the gaps, it does not close them: carried items keep their named status
  and their nine-notes evidence, and the round's new named non-coverage lands
  as ledger rows 63–66 (one class per record / no multi-defect interaction;
  refusal classes not exercised at archive scale; existence proof ≠
  defect-space fraction; false-sweep `hits=`/`listed=` are
  directory-at-runtime values) (`knowledge/hardening-r10.md`,
  `lessons/2026-10-16-archive-scale-controls-and-ledger.md`).
- Receipt coverage slipped one of the round's own classes: the round-10
  receipts and `evidence/README.md` say six controls, but the receipt bodies
  carry five class runs — `C-r9-structure-break.md` is pinned and MATCHed
  while its verify-all run (→ `NO_QUESTION`) appears only in
  `fixtures/archives-r9/controls/README.md` §Measured outputs,
  `knowledge/hardening-r10.md` §1 and the lesson §1. Root cause measured in
  the cut scratch: `controls.tsv` has no trailing newline and the cut
  script's `while IFS… read` loop drops an unterminated final line (bash
  skips it — re-verified with a two-line probe). Flagged for the capstone
  audit / a receipts regeneration (`evidence/README.md:822`,
  `evidence/controls-r10-20261016T055530Z-controls.log:297`).
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
- Carried residuals stand from rounds 2–3: all three landed — in-root hardlinks bypass path canonicalization closed at round 13 (`CLAIM_SOURCE_MULTILINKED` refuse-unread, `knowledge/hardlink-alias-r13.md`), cross-device mount aliases at round 14 (`CLAIM_SOURCE_CROSS_DEVICE` refuse-unread against the resolving root's device, `knowledge/mount-alias-r14.md`), and the other two at round 12: the 8 MiB source-read cap (`CLAIM_SOURCE_READ_TOO_LARGE` / `CHAIN_SOURCE_READ_TOO_LARGE`, refused before any read, at the shared `claim_source_path` chokepoint) and the banner contract (`VERSION=v2`; r12 baseline re-pinned, `knowledge/gate-baseline-r12.md`).
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

Round 8 ran the r7-registered freshness/operability move on the same
direct-dispatch routing: at `3ba718bf…` no behavioral baseline existed and
`--pin`/`--drift` were unknown flags (exit 2, no file), so a gate regression (a
mode silently skipped, an output field changed) was only catchable by reading
receipts after the fact — while at `46f5ddb3…` the gate pins and re-checks its
own canonical behavior: `--pin` writes a `chousa-gate drift baseline v1` file
(header `volatile_fields=ts gate_sha256`, `pinned_ts`, the canonical
invocation) and `--drift` reports `GATE_DRIFT: none` exit 0 on the committed
baseline (`1c81a6cb…`) — including after 75 s of live churn — names changed
tokens exit 1 (a mode-skip copy still closes CLEAN at the verdict line with
exit 0 while the pin names the vanished `SECTION:integrity`, the vanished
`FINDING:REF_UNRESOLVED` and the counters that moved; an output-field rename
names `-refs native tally`; a volatile-list rewrite names `volatile_fields`),
and exits 2 on missing or malformed baselines; the pinned observables hold
(selftest 74 → 85 with case lines 1–74 byte-identical; claims 17/17; chain
17/22; broken control 1/2; sweeps 1/2 `REJECTIONS_OK=3/3`; r1 archives 3/3;
14/14 cross-round mode pairs byte-identical after ts-normalization; a pin leg
under strace carries 0 network syscalls). That observable is not saturated
either: the pin freezes an output surface, not an oracle — exit-code-only
regressions, behavior outside the canonical invocation, weakened selftest
assertions, per-row movement outside the composed surface, and the masked
`ts`/`gate_sha256` fields stay invisible by measurement or by design — so the
drift ritual pairs with a source review of the gate at the same SHA, and
re-pin is a recorded act with a reason. The r8 receipts are lane-local logs
(no queue taskKey), so the receipt-identity debt is unchanged.

Round 9 ran the r8-registered fixture-depth coverage move on the same
direct-dispatch routing: at `46f5ddb3…` the archives had only structural
verification (r1's 3/3) and pointwise fixtures (r2's 17 claims, r3's 22 hops)
— no record-format encoding existed, so `verify-all` on a raw archive
composes DRIFT `run=2 absent=3 drift-sections=1 findings=6` (nothing to
compose) — while at the same unchanged gate the three converted records under
`corpus/fixtures/archives-r9/` each compose CLEAN `sections=5 run=5
absent=0 drift-sections=0 findings=0` exit 0 (claims 10/10; chains
6/7·6/7·7/8 with one exempt chip hop each; sweeps 1/1; integrity 13/12/0 ·
14/13/0 · 15/14/0), the five inter-archive convergence hops resolve, the
shared claims companion closes `VERDICT_BEARING_CLAIMS=10/10` (r2
containment pairs 0), claim coverage over the archive corpus measures
17 → 46 claim-surface rows (delta 29; roughly one prose line in five under a
span check), and the manifest gains three lines (5 → 8, prefix preserved).
That observable is not saturated: a conversion-CLEAN certifies the record's
fidelity to chosen spans of the archive bytes — not the archives' external
truth or argument completeness — the in-record `span` column and row pointers
are outside every gate check (the round's own `A-r9.md:50` miss is the
measured instance), the chain of custody stops at the export, and the round's
"modulo documented integrity findings" prediction measured out to zero
findings on every record. The r9 receipts are lane-local logs (no queue
taskKey), so the receipt-identity debt is unchanged.

Round 10 ran the r9-registered residual-hardening move on the same
direct-dispatch routing: at `46f5ddb3…` no broken archive record existed
(the lane's negatives were small-fixture scale — `chain-r3-broken.md`,
`sweeps-r5-broken.md`, `full-r6-broken.md`, `integrity-r7-broken.md`), the
archive records' six exempt items (three `blocked-no-fetch` chip hops and the
three integrity tokens on those rows) were counted but never audited, and the
r2–r9 named limits had no single disposition — while the round lands six
archive-scale negative controls under `corpus/fixtures/archives-r9/controls/`
(each a single-defect mutant of a production record; every one composes DRIFT
`drift-sections=1 findings=1` exit 1 naming exactly its class and nothing else
— `CLAIM_SPAN_NOT_FOUND` `9/10`, `CHAIN_ANCHOR_NOT_FOUND` `5/7`,
`SWEEP_REJECTION_INCOMPLETE` `2/3`, `SWEEP_CLAIM_FALSE` `0/1`,
`REF_UNRESOLVED` `15/13/1`, `NO_QUESTION` crit — together exercising all five
composed sections), audits the records' exempt set to 6/6 justified by source
bytes with 0 findings, and lands `knowledge/hardening-r10.md` — every r2–r9
named limit plus the r1 debts in 71 dispositioned rows (by-design 38 ·
carried 25 · closed 3 · finding 1 · operator 4) with the 30-item
cheapest-first round-11 audit queue; the holds are green (selftest 85;
`GATE_DRIFT: none`; records CLEAN; claims-r2 17/17, claims-r9 10/10, chain-r3
17/22, sweeps-r5, full-r6, integrity-r7 held; r1 `3/3`; manifest untouched;
zero network; gate sha == the HEAD blob, diff empty). That observable is not
saturated: the controls are one existence proof per class, not a measured
fraction of defect space; refusal classes, multi-defect interaction and
semantic drift stay outside the set; the `A-r9.md:50` instance was corrected at round 12 (the class remains invisible to every mode); exemption truthfulness stays author-declared beyond the audited
instances; and the standing receipts carry five of the six class runs (the
sixth's run lives in the controls README, the note and the lesson — a
receipt gap flagged for the capstone audit; see Known gaps). The r10
receipts are lane-local logs (no queue taskKey), so the receipt-identity debt
is unchanged.

Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0; operator target at least 100), the non-author admit/reject spot-check, and frozen-replay conformance. The scope-refusal gate findings landed at round 12 (`knowledge/scope-refusal-r12.md`). Semantic and
external-source verification remain out of scope by design.
