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
| `knowledge/root-slash-boundary-r15.md` | Round-15 note: the `--root /` boundary dead-arm — `"$root_r"/*` renders `//*` at `root_r=/` and matches nothing, refusing every absolute source `OUT_OF_CORPUS`; the `in_root()` normalized-prefix contract (materialized helper, never inline `${var%/}` in a case word), the three same-class sites converted, the `//`-canon MISSING artifact, and the measured named limits | `evidence/root-r15-20261019T152000Z-{demo,selftest,battery,drift}.log`; selftest cases 107–110 |
| `knowledge/verification-r16.md` | Round-16 note: the 64-seat verification wave's disposition table — every finding classified as fix (landed), absorb (record corrected), or named debt (round-17 queue); the `--root //` in_root strip-all fix; the corrected battery receipt; the named-limit confirmations | `evidence/root-r15-20261019T152000Z-battery.log` (corrected); selftest case 111 |
| `knowledge/fenced-heading-r17.md` | Round-17 note: the `load_sections` fenced-heading shadow — a `## ` line inside a fence is literal, so a fenced `## Meta` must not reset the real Meta body; the measured shape matrix (a single `^``` ` toggle fixes the simple shadow but leaves 4-backtick nesting, indented closers and unclosed openers CLEAN; the landed shape pairs same-char fences with closing length >= opening, 0–3 literal-space indent, and parses an unclosed opener as a fence to EOF = fail closed); selftest cases 112–116; named limits (fenced rows inside a real section are still scanned; the gate is not a Markdown renderer) | `evidence/fence-r17-20261019T171200Z-{demo,selftest,battery,drift}.log`; selftest cases 112–116 |
| `knowledge/scope-phrase-gap-r18.md` | Round-18 note: the `SCOPE_KENGAKU` phrase gap — `llm benchmark(s)`/`llm scoring` were missing despite the model-quality boundary; the minimal conservative fix (3 phrases, not 5 — `ai benchmark(s)` stays named debt for breadth); the audit's other inflection findings dispositioned | `evidence/scope-r18-20261019T173000Z-{demo,selftest,battery,drift}.log`; selftest cases 117–119 |
| `knowledge/sweep-symlink-r19.md` | Round-19 note: the sweeps symlink escape — `sweep_path_guarded` canonicalizes the glob's base but not each match, so a wildcard inside an in-root dir can match a symlink whose target is outside; the per-match canonicalization fix, the two escape shapes (leaf symlink, dir symlink), and the named limits (post-expansion check, TOCTOU) | `evidence/symlink-r19-20261019T174500Z-{demo,selftest,battery,drift}.log`; selftest cases 120–122 |
| `knowledge/html-comment-r20.md` | Round-20 note: the HTML-comment heading shadow — same class as the fenced-heading shadow (r17) but through `<!-- -->`; the comment-state tracking in `load_sections`, and the named limits | `evidence/verify-r20-20261019T180000Z-{demo,selftest,battery,drift}.log`; selftest case 124 |
| `knowledge/pointer-boundary-r21.md` | Round-21 note: the `ptr_resolves_meta` boundary gap — relative pointers checked raw `-f` without canonicalization (traversal and symlink escapes); the canonicalization fix against both roots, the denylist-on-target check, and the named limits | `evidence/ptr-r21-20261019T184000Z-{demo,selftest,battery,drift}.log`; selftest cases 125–128 |
| `knowledge/denylist-r22.md` | Round-22 note: the `.config`/`.omp`/`.local/state` path-start denylist bypass — `*/X/*` needs a leading component; the bare-start patterns fix, the `.config-adjacent` over-refusal control, and the named limits | `evidence/deny-r22-20261019T190000Z-{demo,selftest,battery,drift}.log`; selftest cases 129–132 |
| `knowledge/fenced-anchor-r23.md` | Round-23 note: the chain `heading` anchor false-positive — `chain_anchor_at` matched `^#+` headings inside fences as real anchors; the inline fence tracking fix, the unaffected quote/line kinds, and the named limits | `evidence/fanchor-r23-20261019T192000Z-{demo,selftest,battery,drift}.log`; selftest case 129 |
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
| `knowledge/json-delimiter-r24.md` | Round-24 note: the `verify-all --json` delimiter edge — an append onto a manifest whose last byte is not `\n` glued two objects onto one invalid line; the hex last-byte probe, the unreadable-manifest refusal, cases 134–136, controls, three killed mutants, the measured single-writer limit | `S001`, `S013` (`corpus/SOURCES.md`); `evidence/json-r24-20261019T213117Z-{demo,selftest,battery,drift}.log` |
| `knowledge/claim-support-states-r24.md` | Round-24 method note (current art): access, relevance, support at a named anchor and truth are four separately failable observations; `verified` needs support, truth needs more than support; the gate's span check is support at byte granularity only | `S006` §3.3, `S007` §2.1; this file's §"Known gaps" |
| `knowledge/citation-chain-fidelity-r24.md` | Round-24 method note (current art): a resolved hop proves a locator exists, not that the relay is faithful; the five-item per-hop comparison (proposition, scope, quantity, hedge, date) and the altered-qualifier disposition | `S005` §4, §6, Fig. 1 fn 1; `S003` "Trace claims…"; `knowledge/chain-resolution-r3.md:133` |
| `knowledge/contextual-source-admission-r24.md` | Round-24 method note (current art): source priority is decided per claim — the per-source admission row; the primary > secondary > aggregator ladder stays the default ordering, overridden with a stated reason | `S002` Principle #2, `S004` §24.2.1.3, `S003` "Investigate the source" |
| `lessons/round-24.md` | Round-24 lesson: the lane's own mistakes M-1..M-14 (class · re-verified pointer · capturing criterion · fix), the criteria 6–12 they motivated, the round's source Gate | STATE dossier §4/§5; `corpus/QUALITY.md` |
| `SOURCES.md` | Where the lane learns (contract v1): the opened, scope-tiered registry with kept rejections and flips (counts owned by `SOURCES.md`; re-derive with `bash corpus/evidence/round25-sources-census.sh`), study paths, a bounded search log, unopened leads | `kaika/SOURCES-CONTRACT-v1.md`; each row's own anchor |
| `knowledge/audit-r11.md` | Round-11 capstone audit, a dated snapshot (2026-10-16, HEAD `44cbad6`): findings A1–A28 with verdicts and pins, defects D1–D5 with dispositions, the final debt register, SHONEN readiness ("NOT promotion-eligible"). Its pins are as-of that date: gate `46f5ddb3…` is superseded, and the ledger `3845709b…` is superseded by `hardening-r10.md` §6 and its addenda (counts owner from round 25: the round-25 erratum). Its header has no `recheck:` key (`verify-metadata` → `META_RECHECK_ABSENT`) | `knowledge/audit-r11.md` `:299-344` (pins, errata); `knowledge/hardening-r10.md` §6 + round-25 erratum |
| `lessons/2026-10-19-hardlink-alias-boundary.md` | Round-13 lesson: the hardlink-alias boundary — one `stat -c '%s %h'` probe serves the r12 size cap and the r13 alias check; refuse-on-count chosen over partner enumeration (both enumeration designs BLOCKed as unsound); carry-forwards named (TOCTOU, same-device bind mounts, unmeasurable stat). Gate `6b17e50c…` is the r13 gate, superseded at r14 by `d8bbd0bf…` | `evidence/alias-r13-20261019T123621Z-{selftest,bypass-before,bypass-after,battery}.log`; `knowledge/hardlink-alias-r13.md`; `knowledge/hardening-r10.md` Round-13 addendum |
| `lessons/round-24-verifier-spotcheck.md` | Outside check on round 24, written by the integrator (not lane-owned; never edited here): admit/reject spot-check (4/4 admits, 3/3 rejects agree), ADMITTED after erratum `095b90c`; named debts — concurrent-append blank-line residual, citation-chain recheck needs the fleet root as `--root`, the lesson template should carry a spot-check slot (dispositioned in `lessons/round-25.md` `## Spot-check intake`) | fleet `.ufo/waves/kaika-w3/chousa-review.md`, `chousa-critic.md` |
| `lessons/round-27-verifier-spotcheck.md` | Main's non-author judgment: C1/C2 bounded gains; C3 complete-path clause remains falsified with a new canonical over-refusal, so not admitted/rejected-harmed. Original controls, source checks and open L0 authority are preserved. | original round27 declaration, measured gate identity, retained complete-path falsification and parent-owned census; native accounting separate |
| `knowledge/metadata-screen-r25.md` | Round-25 note: the `verify-metadata` mode — header-region grammar, the `META_*` finding set and severities, the round-25 entry refusals, `METADATA_COMPLETE=N/M`; the lane-corpus result (25/28; the three legacy entries lacking `recheck:`) and its named limits (key presence and date shape, not criterion-6 compliance) | `evidence/round25-claims.md` claim 1; `evidence/round25-measure-after.log`; selftest cases 137–154; `fixtures/metadata-r25/`; `SOURCES.md` S029 |
| `fixtures/metadata-r25/*` (+ `README.md`) | Round-25 metadata-screen fixture set: 18 single-defect mutants, 6 edge cases and 3 clean controls derived from real entry headers, with a hand-derived expectation table (one row corrected after the differential) | `evidence/round25-meta-differential.{sh,log}` (`AGREE=54/54`); `evidence/round25-meta-oracle.py` |
| `lessons/round-25.md` | Round-25 lesson: mined mistakes (class · pointer · captured-by · fix shown able to fail), the round-24 spot-check intake, the sources opened this round | `evidence/round25-measure-{before,after}.log`; `QUALITY.md` criteria 13–14 |
| `evidence/round25-*` | Round-25 pre-registration (`round25-claims.md`), counting script and its before/after outputs (`round25-measure.sh`, `-before.log`, `-after.log`), the metadata oracle and differential, the ledger recount (`round25-ledger-recount.py`) | `SCORECARD.md` `## Round 25 verdict` |
| `knowledge/reader-allocation-r26.md` | Resource-bound method: distinguish input bytes from downstream object allocation, vary shape, and require resource plus output-identity holds; scoped to the metadata reader | `S034`; `evidence/round26-claims.md` C1; `SCORECARD.md` Round26 |
| `knowledge/recheck-due-r26.md` | Schedule-derived deadline semantics, explicit as-of date, event/unknown classifications and the distinction between a due assessment and source truth | `S035`, `S037`, `S038`, reopened `S029`; `evidence/round26-claims.md` C2 |
| `knowledge/registry-link-r26.md` | Local registry identity/status/exact-rooted backlink checks and descriptive verified-at text; a declaration relation is not semantic citation support | `S036`, `S039`; `evidence/round26-claims.md` C3 and contract correction |
| `lessons/round-26.md` | Prior closure intake, allocation-amplification mistake, corrected registry contract, inherited-wave continuity and located source Gate quotes | `evidence/round26-measure-before.log`; `QUALITY.md` criterion18; `.ufo/waves/round-26/` |
| `evidence/round26-*` | Frozen-population pre-registration, baseline and final counting receipts plus independent date/registry differentials | `SCORECARD.md` Round26 owns the final measurements and revision |
| `knowledge/quote-reopen-r30.md` | Round-30 note: `tools/quote-reopen.py` contract v2 — the HTML head ends without `</head>` (C1) and one total `DEADLINE` plus one validated DNS resolution per hop bound each fetch (C2); the loopback counters, their before and after, and what they do not show (liveness, TLS, per-hop provenance, resolver time, IPv6) | `S050`-`S056`; `evidence/round30/claims.md`; `SCORECARD.md` Round 30 |

Count: 20 entries, ten knowledge notes and ten lessons — `functions.glob`
pattern `corpus/knowledge/*.md;corpus/lessons/*.md`, 2026-10-16. Fixture and
evidence files are coverage-listed but not additional knowledge entries.

Round-24 correction (appended; the count above is the dated 2026-10-16
snapshot): 40 entries — 28 knowledge notes and 12 lessons
(`ls corpus/knowledge/*.md | wc -l` → 28; `ls corpus/lessons/*.md | wc -l`
→ 12, 2026-10-19). Two older files are still unindexed above
(`knowledge/audit-r11.md`, `lessons/2026-10-19-hardlink-alias-boundary.md`) —
queued for round 25.

Round-25 correction (appended 2026-10-21; supersedes the round-24 count
as current at this landing): 43 entries — 29 knowledge notes and 14 lessons
(`ls corpus/knowledge/*.md | wc -l` → 29;
`ls corpus/lessons/*.md | wc -l` → 14). The count now includes the
integrator's round-24 verifier spot-check (a new file after the r24 count).
The two older files named above are indexed, along with that spot-check and
the round-25 entry/lesson; no unindexed base file remains.

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
  **Round-25 qualification:** the tuple and 30-item queue in this bullet are
  the round-10 handoff snapshot, not current dispositions. Current totals
  belong to `knowledge/hardening-r10.md`'s Round-25 erratum; re-derive with
  `python3 corpus/evidence/round25-ledger-recount.py` from the lane root
  (`round25-final-ledger.log`). The original snapshot is retained as history.
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
  uniqueness, exemption-truth and external-source limits stand unchanged (exemption-truth: see the Round32 disposition).
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
  (`knowledge/chain-resolution-r3.md`). (Round 32 note: for `unresolved`,
  `blocked-no-fetch` and `labelled-dead` this is no longer true — a locally
  resolvable hop drifts; `knowledge/exempt-hop-audit-r32.md`.)
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

Rounds 11–23 (paragraphs appended at round 25; each drafted by a round-25 seat
from that round's `SCORECARD.md` verdict, `LOG.md` entry, knowledge note,
receipts and read-only git, with a path:line citation for every number in
`.ufo/waves/round-25/build/Frontier*.md`; the integrator kept each draft's
limits, including receipt gaps the drafts found).

Round 11 ran the capstone audit that round 10 registered
(SCORECARD.md:421-423), on the in-session wave routing: one 32-seat flash
call, which the scorecard records as "31/31+ reports" and the wave report as
32 audit seats; the seat count is unverifiable without rosters and was folded
in at admission as a correction. The move re-executed rather than changed
anything: every admitted round's evidence commits and gate blobs were resolved
by command, the battery was re-run at today's bytes, the 71-row limit ledger
and its 30-item queue were re-parsed, and SHONEN readiness was assessed
without self-attestation. The before→after observable on the gate is flat:
gate `46f5ddb3…` at HEAD `44cbad6…` before and after the battery, selftest
`PASS (85 cases)`, `GATE_DRIFT: none` against the r8 baseline `1c81a6cb…`, and
the r1 counting command at `VERDICT_BEARING_EXPORTS=3/3`. What moved is the
record: 28 re-audited findings rows (A1–A28), five audit-layer defects
(D1–D5), and a verdict of ADMIT-with-correction with calibration and depth
improved and freshness unchanged. Holds: selftest case lines identical to the
r8 receipt, the verify-all manifest at 8 lines with sha `78627e6d…` equal to
HEAD, zero network syscalls in the re-run trace, and the fixtures, records and
controls reproducing their verdicts. That observable is not saturated: the
note re-ran the commit, gate and verdict surfaces, but round 2–10 chain
verification is attributed to per-round auditors whose reports the note could
not see, so the 15/15 chain re-execution covers round 2 alone; receipt
identity stays open for the operator at 0 of 10 receipt-backed rounds; SHONEN
is 0/4 with no named non-author verifier; no round-11-named receipt exists
under `corpus/evidence/`, so the battery lives verbatim in the note and the 39
logs it counts are the r2–r10 families; D1, D2, D4 and D5 were open when the
audit landed (D3 closed at round 12), and this paragraph does not verify their
later status. The gate itself moved after this round (round 12, `46f5ddb3…` →
`91a01695…`), so the after-sha here is the round-11 end state only.

Round 12 ran the scope-refusal, operability and calibration move its opening
registered, on one 64-seat AgentSwarm wave (opencode-go-6 /
deepseek-v4.1-flash, 64/64 seat reports). At `46f5ddb3…` the gate had no scope
machinery (`grep -c SCOPE_` → 0), `VERSION=research-gate-r1`, no source-read
cap, and selftest `PASS (85 cases)`; at `91a01695…` the declared-scope screen
emits three `SCOPE_*` warn findings (`grep -c 'id=SCOPE_'` → 3), the banner
reads `VERSION=v2`, claim and chain sources over 8 MiB are refused before any
read, and selftest reads `PASS (98 cases)` with cases 1–85 identical to the
round-8 receipt's case lines. The baseline was re-pinned once at final bytes
with the reason recorded: before the re-pin `--drift` read `GATE_DRIFT: GATE
record_sha256` exit 1 by design, and after it reads `GATE_DRIFT: none` exit 0.
The pinned observables hold: r1 `3/3`, the fixture battery byte-identical
modulo banner and ts, and the A-r9 post-fix `verify-all` CLEAN with
`sections=5`. That observable is not saturated either: the scope screen reads
only declared `## Meta` rows, so undeclared absorbed scope passes and the solo
modes carry no scope teeth; the size cap is bypassed when the stat itself
fails; and the pointer-line versus span-line class stays a named non-coverage.
Receipt identity remains OPEN. The r1 3/3 and any unretained
post-repin/pre-round comparison are round-reported assertions, not a retained
independent receipt in that round's group.

Round 13 ran the coverage and depth move its opening registered — closure of
the last round-2 residual, the in-root hardlink-alias bypass (ledger row 8) —
on one 64-seat AgentSwarm wave (opencode-go-6 / deepseek-v4.1-flash, 64/64
seat reports). Two seats BLOCKed partner enumeration as unsound, so the claim
was re-scoped to a one-probe `nlink != 1` refusal. Before (`91a01695…`, `grep
-c samefile tools/research-gate.sh` → 0), a claim through an in-root hardlink
alias of an out-of-root file read `observed=supported` CLEAN with rc=0; after
(`6b17e50c…`) the same fixture refuses with `CLAIM_SOURCE_MULTILINKED`
severity=crit, `observed=refused`, rc=1. Selftest moved 98 → 102 with cases
1–98 byte-identical to the round-12 receipt, the masked fixture battery was
ALL IDENTICAL against the pre-round gate, drift against the round-12 baseline
stayed `GATE_DRIFT: none` without a re-pin, and r1 held `3/3`. That observable
is not saturated either: the check refuses on link count, so a legitimate
in-root multi-link family refuses too (pinned by case 101 as a named trade);
bind mounts present nlink=1 and stay invisible to stat; TOCTOU and an
unmeasurable stat (alias check skipped) remain named limits. Receipt identity
remains OPEN. The r1 3/3 and any unretained post-repin/pre-round comparison
are round-reported assertions, not a retained independent receipt in that
round's group.

Round 14 ran the bind-alias move its opening registered: the claim and chain
chokepoint now refuses a source whose st_dev differs from the resolving root's
device (`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`, crit), and
one `stat -c '%s %h %d'` probe serves nlink, size and device. The wave was one
64-seat call on alibaba-token-plan / deepseek-v4.1-flash, 63/64 reports (seat
54 failed on a provider content-filter 400; recorded, not backfilled). The
observable moves on the live bypass pair: a tmpfs mounted over an in-root
directory reads `observed=supported` CLEAN (`VERDICT_BEARING_CLAIMS=1/1`,
rc=0) at the pre-round gate `6b17e50c…`, and `observed=refused` with
`CLAIM_SOURCE_CROSS_DEVICE` crit (`0/1`, rc=1) at the landed gate `d8bbd0bf…`.
The selftest moves 102 → 106 (`PASS (106 cases, 0 skipped)`). The r12 drift
baseline and r1 `3/3` are recorded as holding, but the round's own receipts
for those two holds are not on disk. That observable is not saturated: the
bypass pair is `mode=claims` only; the class is cross-device aliases only, so
same-device binds (stat-invisible), overlay roots, the probe-to-read TOCTOU
window and the unmeasurable-stat fail-open remain named limits; freshness is
unchanged. The r1 3/3 and any unretained post-repin/pre-round comparison are
round-reported assertions, not a retained independent receipt in that round's
group.

Round 15 ran the `--root /` dead-arm fix the round-14 wave queued:
`"$root_r"/*` rendered `//*` at `root_r=/`, so every absolute in-`/` source
refused `CLAIM_SOURCE_OUT_OF_CORPUS` crit. The fix is an `in_root()` helper
(`tools/research-gate.sh` ~:612) with a materialized local, applied at the
three same-class sites (`claim_source_path`, `ptr_resolves_meta`,
`sweep_path_guarded`); the opening's one-token form was measured dead on bash
5.3.15 and the pre-registration was corrected before the wave. The wave was
one 48-seat call on zai glm-5.3-flash, 48/48 reports. The observable moves on
the `/etc/hostname` demo under `CHOUSA_ROOT=/`: the pre-round gate `d8bbd0bf…`
refuses `OUT_OF_CORPUS` crit (`0/1`, DRIFT); the landed gate `dd0951d7…` reads
it CLEAN `1/1`. The selftest moves 106 → 110 with cases 1–106 byte-identical
to the r14 receipt, and `--drift` reads `GATE_DRIFT: none`. The r15 battery
receipt on disk does not carry a green hold: it is a `root=.` verify-all run
that reports DRIFT (`drift-sections=3 findings=13`), and it has no identity
line. That observable is not saturated: the fix covers the pattern arm only,
the sweeps guard is vacuous at `/` by declaration, and the r14 limits carry
over; freshness is unchanged.

Round 16 ran the verification move round 15 registered: one 64-seat audit call
on openai-codex gpt-6-luna-max (64/64 seat reports, zero deficit) re-audited
the boundary stack of rounds 12–15 for correctness defects and missed
coverage, and every finding was dispositioned as fix, absorb, or named debt.
The before→after observable is the gate at `dd0951d7…` with selftest 110
versus `2b64a1c8…` with `PASS (111 cases, 0 skipped)`: `in_root` now strips
every trailing slash, so `--root //` no longer refuses in-corpus paths (case
110 pins it (the former sweeps case shifts to 111)), and the r15 battery
receipt was re-run with the correct fixture paths and `--root ..`. The
disposition table holds the two fixes, the absorbed record corrections, and
the named debts queued for round 17. The holds are drift `none` against the
r12 baseline with no re-pin, and the r1 archive observable as asserted by
LOG/SCORECARD, not a retained raw-archive receipt. That observable is not
saturated: the wave verified the refusal classes rather than extending them,
so coverage is unchanged; the case-110 pin covers the `//` edge but not the
`ptr_resolves_meta` root-slash site; the claimed cases 1–110 byte-identity
holds only for 1–109 in the receipts; and the round left no r16-stamped
selftest, drift, or pre-round battery receipt, so its holds rest on the LOG
and SCORECARD statements.

Round 17 ran the round-16 named debt the verification wave had queued:
`load_sections` reset a section on every `## ` line without fence state, so a
fenced `## Meta` could shadow the real declaration and the scope screen
checked the wrong body. The wave was one 32-seat call on opencode-go /
deepseek-v4.1-flash, after xai-oauth failed on quota for all 48 seats and zai
glm-5.3-flash was interrupted at 14/48; it landed 27/32 seat reports, with
five provider-400 `reasoning_content` failures recorded and not backfilled.
The before→after observable is the demo record with a real `domain: bounty
program scope` and a fenced `## Meta` declaring `deep-research method`: at
`2b64a1c8…` it verifies CLEAN, and at `c2915f24…` it raises
`SCOPE_BOUNTY_ABSORBED` (warn) and DRIFT. The two-pass fence pairing (same
character must close, closing length at least the opening, 0–3 spaces of
indent, an unclosed opener fails closed) is pinned by cases 112–116; the
selftest is `PASS (116 cases, 0 skipped)` with cases 1–109 byte-identical to
the r15 receipt, drift `none` against the r12 baseline, and the r1 archive
observable asserted in LOG/SCORECARD, not re-proved by the converted-record
battery. The `LLM benchmarks` phrase gap stays named debt. That observable is
not saturated: the parser is not a Markdown renderer, fenced data rows inside
a real section are still trusted, and the round's "masked battery ALL
IDENTICAL" compares two runs that both carry DRIFT (claims `0/17`, chain
`0/22`, verify-all `drift-sections=3 findings=13` under `root=.`), so the
battery's pinned claims and chain observables do not hold in the receipts.

Round 18 (loop 1, round 7) ran the phrase-gap move that round 16 left as named
debt, on one 16-seat AgentSwarm wave routed to openai-codex gpt-6-luna-max
after the zai glm-5.3-flash quota was exhausted (operator directive; 16/16
seat reports). `SCOPE_KENGAKU` covered `model benchmark(s)` and `model
scoring` but not `llm benchmark(s)` or `llm scoring`, so a record declaring
`domain: LLM benchmarks` passed CLEAN. On the demo record the pre-round gate
(commit `e3c556e`, gate `c2915f24…`) returns CLEAN; the landed gate
(`6e694881…`) adds `llm benchmark|llm benchmarks|llm scoring` and returns a
`SCOPE_MODEL_QUALITY_ABSORBED` warn with DRIFT. Selftest moves 116 → 119,
cases 1–116 byte-identical to the r17 receipt, cases 117–119 pinning the new
phrases and a prose-only control; `--drift` against the r12 baseline reports
`GATE_DRIFT: none` with no re-pin. The r1 archive counting command is recorded
at `VERDICT_BEARING_EXPORTS=3/3` in the round notes, but no r18 receipt
carries that line, so it is asserted here, not receipted. The battery receipt
is an output-identity record over the archive and claim fixtures; its claims,
chain and verify-all sections read DRIFT in that run context, and the round's
"ALL IDENTICAL vs pre-round gate" has no diff in the receipt. That observable
is not saturated: the screen reads only Meta `domain`/`scope` rows, so prose
is never scanned (case 119); `ai benchmark(s)` stays out as too broad; the
inflection gaps (`bug bounties`, `dispatch mechanisms`, `llm evaluations`) and
the camel-case `llmbenchmark` form stay named debt; and the matcher is literal
phrase match, not a judgment that a record is in model-quality scope. Receipt
qualification (round-25 fresh review): r1 3/3 is round-reported, with no
matching raw-archive count line in this round's retained logs; the A/B/C
battery lines concern converted archive-r9 records instead. The retained
battery uses `root=.` and reports DRIFT (claims 0/17, chain 0/22, verify-all
drift-sections=3/findings=13); its stated identity is output identity, not a
green hold, and no pre-round comparison output is retained.

Round 19 (loop 1, round 8) ran the sweep-symlink escape move that round 16
left as named debt, on one 16-seat AgentSwarm wave routed to openai-codex
gpt-6-luna-max under the zai exhaustion directive (16/16 seat reports).
`sweep_path_guarded` canonicalized a sweep glob's literal base but not each
expanded match, so `dir/*.md` matching an outside leaf symlink, or
`dir/*/*.md` traversing an outside directory symlink, reported
`SWEEP_CLAIM_FALSE` instead of a boundary refusal. On the demo the pre-round
gate (commit `5499cef`, gate `6e694881…`) reports a `SWEEP_CLAIM_FALSE` hit
and DRIFT; the landed gate (`9f163807…`) canonicalizes every match against
both allowed roots and refuses the whole sweep with
`SWEEP_LOCATION_OUT_OF_CORPUS` (crit, `observed=refused`, match not opened).
Selftest moves 119 → 122, cases 1–119 byte-identical to the r18 receipt, cases
120–122 pinning the leaf-symlink, directory-symlink and in-root-symlink
control; `--drift` reports `GATE_DRIFT: none`; the battery receipt is
byte-identical to r18 after timestamp normalization (same DRIFT sections, same
reason). That observable is not saturated: the check runs after bash has
already expanded the glob, so a symlinked directory is traversed (names only,
never content) before the refusal; a check-to-use race remains; `--root /`
makes the guard vacuous by declaration; and no r19 receipt carries a strace,
so "zero network" is asserted in the round notes, not receipted. Receipt
qualification (round-25 fresh review): r1 3/3 is round-reported, with no
matching raw-archive count line in this round's retained logs; the A/B/C
battery lines concern converted archive-r9 records instead. The retained
battery uses `root=.` and reports DRIFT (claims 0/17, chain 0/22, verify-all
drift-sections=3/findings=13); its stated identity is output identity, not a
green hold, and no pre-round comparison output is retained.

Round 20 ran an adversarial re-audit of the boundary stack that rounds 15–19
had landed, as one 64-seat AgentSwarm call on openai-codex gpt-6-luna-max
(64/64 seat reports). Its finding was the HTML-comment heading shadow:
`load_sections` parsed a `## Meta` inside `<!-- -->` as a real heading, so a
record whose real Meta declared a refused province plus a commented
in-province Meta closed CLEAN. The before→after observable is the demo pair:
at the pre-round gate `2bb556b` (blob `9f163807…`) the shadowed record closes
`RESEARCH_GATE: CLEAN`; at the landed gate (blob `49b36759…`) it refuses
`SCOPE_BOUNTY_ABSORBED` (warn) and closes `DRIFT (findings=1 drift=1 …)`. The
fix tracks `in_comment` beside `fence_char`, checking fence state first and
comment state before the heading arm. The holds: selftest `PASS (124 cases, 0
skipped)`, up from 122, with cases 1–119 byte-identical to the r18 receipt and
case 124 pinning the new arm; `--drift` against the r12 baseline `GATE_DRIFT:
none` with no re-pin; r1 `VERDICT_BEARING_EXPORTS=3/3`; and the masked
battery, which the round reports identical to the pre-round gate. That
observable is not saturated: the fix closes the comment arm at the class the
wave found and nothing wider — the parser is not a Markdown renderer, so
CDATA, processing instructions and other HTML constructs stay outside the
declared-record contract. The `ptr_resolves_meta` escape, the `.config`
path-start denylist bypass, the fenced-heading chain anchor and about ten
scope/inflection gaps were dispositioned as named debt for round 21, not
closed, and the drift ritual proves the output surface only. Receipt
qualification (round-25 fresh review): r1 3/3 is round-reported, with no
matching raw-archive count line in this round's retained logs; the A/B/C
battery lines concern converted archive-r9 records instead. The retained
battery uses `root=.` and reports DRIFT (claims 0/17, chain 0/22, verify-all
drift-sections=3/findings=13); its stated identity is output identity, not a
green hold, and no pre-round comparison output is retained. Case 123
(`claims-cap-eof`) was prior-session work absorbed by r20; case 124 is the
HTML-comment-shadow pin.

Round 21 ran the round-20 named-debt move on the pointer boundary, as one
32-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash (32/32 seat
reports). `ptr_resolves_meta` tested relative pointers with a raw `-f`, so
`lib/../../r21-outside.txt` passed CLEAN whenever the file existed under the
raw path. The before→after observable is the demo pair: the pre-round gate
`b057245` (blob `49b36759…`) closes CLEAN on the traversal pointer; the landed
gate (blob `bfc291ef…`) refuses it with `POINTER_UNRESOLVED` (warn) and closes
DRIFT. The fix canonicalizes the candidate with `readlink -f`, checks
`in_root` against both roots, and applies the denylist to the canonical
target, so a benign symlink to `.config/passwd` is refused; cases 125–128 pin
traversal, symlink, lane-root absolute pointer (now exit 0) and the `.config`
symlink. The holds: selftest `PASS (128 cases, 0 skipped)`, up from 124, with
cases 1–124 byte-identical to the r20 receipt; `--drift` `GATE_DRIFT: none`
with no re-pin; r1 `VERDICT_BEARING_EXPORTS=3/3`; and the masked battery,
which the round reports identical to the pre-round gate. That observable is
not saturated: canonicalization shows that a pointer resolves to a readable
file inside a root and outside the denylist, not that the file is the cited
source or supports the claim. The `.config` path-start form stayed open at r21
— the r21 note states it as closed in one bullet and still bypassing in the
next — and round 22 closed it (`knowledge/denylist-r22.md`); the
fenced-heading chain anchor stayed named debt until round 23
(`knowledge/fenced-anchor-r23.md`). The round's demo is one traversal
instance, not a measured fraction of the pointer space. Receipt qualification
(round-25 fresh review): r1 3/3 is round-reported, with no matching
raw-archive count line in this round's retained logs; the A/B/C battery lines
concern converted archive-r9 records instead. The retained battery uses
`root=.` and reports DRIFT (claims 0/17, chain 0/22, verify-all
drift-sections=3/findings=13); its stated identity is output identity, not a
green hold, and no pre-round comparison output is retained.

Round 22 (loop 1, round 11) ran the move registered at the round-21 landing:
one 32-seat AgentSwarm call, which fell back from antigravity gemini-3.8-flash
(24 seats on provider errors, 8 aborted) to openai-codex gpt-6-luna-max and
returned 32/32 seat reports, on the claim that `is_denylist_path` misses
path-start citations of `.config/`, `.omp/` and `.local/state/`. Before (gate
`bfc291ef`, selftest 128), `.config/agent-token.txt` closed CLEAN; after (gate
`dfb798b4`), the same citation refuses with `CLAIM_SOURCE_SESSION` crit, the
bare-start alternatives sitting after the existing `*/X/*` forms. The
observables hold: selftest 128 → 132 with cases 1–128 byte-identical to the
r21 receipt, `GATE_DRIFT: none` against the r12 baseline (freshness unchanged,
no re-pin), and the r1 archive observable at `VERDICT_BEARING_EXPORTS=3/3`.
That observable is not saturated: the denylist remains a pattern list, the r21
canonical-target check covers symlink indirection but not the raw path-start
form, and the fix closes only the bare-start class of these three directories;
`.config-adjacent` stays a non-hit by design (case 132). Receipt qualification
(round-25 fresh review): r1 3/3 is round-reported, with no matching
raw-archive count line in this round's retained logs; the A/B/C battery lines
concern converted archive-r9 records instead. The retained battery uses
`root=.` and reports DRIFT (claims 0/17, chain 0/22, verify-all
drift-sections=3/findings=13); its stated identity is output identity, not a
green hold, and no pre-round comparison output is retained.

Round 23 (loop 1, round 12) ran the fenced-heading anchor move directly, with
no wave: the falsifiable before→after had already been measured by the
round-20 reproduction. Before (gate `dfb798b4`), `chain_anchor_at` matched a
`## Phantom Heading` inside a fenced block as a real anchor and verified the
hop at line 4; after (gate `b5d0f93d`), the heading arm tracks fence state
inline, and the same record refuses with `anchor-missing`, a
`CHAIN_ANCHOR_NOT_FOUND` warn, `RESOLVED_HOPS=0/1`, and DRIFT. Selftest 132 →
133 with cases 1–128 byte-identical to the r22 receipt and case 129 pinning
the fenced arm; the r22 path-start cases are renumbered to 130–133. Drift
stays `GATE_DRIFT: none` against the r12 baseline, and the r23 masked battery
receipt is byte-identical to the r22 one. That observable is not saturated:
only the `heading` anchor kind is fence-aware (the `quote` and `line` kinds
match literal text by design), fence state resets per call, and the selftest
counts fixtures, not the defect space. Receipt qualification (round-25 fresh
review): r1 3/3 is round-reported, with no matching raw-archive count line in
this round's retained logs; the A/B/C battery lines concern converted
archive-r9 records instead. The retained battery uses `root=.` and reports
DRIFT (claims 0/17, chain 0/22, verify-all drift-sections=3/findings=13); its
stated identity is output identity, not a green hold, and no pre-round
comparison output is retained.

Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0; operator target at least 100), the non-author admit/reject spot-check, and frozen-replay conformance. The scope-refusal gate findings landed at round 12 (`knowledge/scope-refusal-r12.md`). Semantic and
external-source verification remain out of scope by design.

Round 24 (loop 2, round 1) closed the `--json` delimiter edge (round-20
named debt, seat 24): on `full-r6.md` with a manifest ending `{"prior":true}`
and no final newline, the pre-round gate measured `MANIFEST_LINES=1
INVALID_JSON_LINES=1` and the landed gate `MANIFEST_LINES=2
INVALID_JSON_LINES=0`; the L2 reviewer's write-only and NUL variants were
closed in the same landing (cases 134–136; `knowledge/json-delimiter-r24.md`).
It also moved the frontier off gate-hardening for the first time since
round 2: three method notes from opened current art — claim-support states,
citation-chain fidelity, contextual source admission — each admitted through
`QUALITY.md` and citing `mined` rows of the new `SOURCES.md`. These notes
govern the analyst's method; no gate mode checks semantic support, fidelity
or suitability, and none is claimed. Still open: concurrent appenders to one
manifest (one blank line in 1 of 3 sixteen-writer runs), the remaining
round-20 named debt (SCORECARD `## Planned — round 25`), and the queued
SOURCES rows S008–S012, S017, S018 waiting for an entry that mines them.


Round-25 index errata (2026-10-21, append-only): the round-22 denylist
coverage row's cases 129–132 are historical at r22; after r23 inserted the
fenced-anchor case at 129, the denylist cases are 130–133. Re-derive:
`bash tools/research-gate.sh --selftest`. The r15–r23 battery receipts often
record DRIFT under `root=.`; "ALL IDENTICAL" in their descriptions is an
output-identity assertion, not a CLEAN claim. The new Frontier paragraphs
preserve each receipt gap; the round-25 hold battery uses the explicit fleet
root and is independent of those old assertions.

## Round26 frontier disposition (2026-10-21)

New held ground: shape-sensitive resource verification of the lane's metadata
reader, computed assessment deadlines, and a local registry-link screen.
The three indexed notes cite mined S034–S039 and, for periodic review, reopened
S029. Their gate results and exact measured revision are owned by SCORECARD's
Round26 section, not inferred from source-row growth.

The generic schedule and registry policy are the lane's design, not Cochrane,
Python or PROV requirements. C2 does not reopen sources or certify truth;
C3 does not judge tier/scope, source support, complete URL/anchor metadata,
or whether recorded verification actually happened. Legacy pre-r24 notes
are outside the prospective criterion6 admission rollup.

Still unclosed: concurrent JSON appenders, filesystem races, parent-root
legacy rechecks, receipt gaps, and pairing a span's occurrence with a named
pointer line. No promotion, outside spot-check or province expansion beyond
deep-research method is self-awarded here. Other build source candidates
remain advisory leads unless an actual registry row says otherwise.

### Round26 frontier admission correction — 2026-10-21

The preceding “new held ground” wording is superseded: the three indexed
round26 notes are **qualified/withdrawn candidates, not admitted expansion**.
C1's narrow allocation result is measured, but the shared selftest fails;
C2 and C3 are independently falsified outside the frozen controls. Each note
now has a recovery qualification naming the unsafe implementation and reports.
SCORECARD's Round26 recovery section is the current owner of those verdicts.
Registry rows39 and knowledge files32 are inventory counts, not admission
counts. No new capability, province expansion, outside spot-check or
promotion is inferred from them. Existing carried debts above remain open.

## Round27 frontier disposition (2026-10-21)

Bounded repairs and independently challenged controls are recorded in
`lessons/round-27.md`, `evidence/round27-claims.md`,
`evidence/round27-falsify-controls.py` and SCORECARD's Round27 section.
Opened own-work rows S040–S043 teach usage-record grammar, date input
representation, registry state/occurrence identity and post-falsification
parser/cost corrections. Four added source rows are not admitted expansion.

The round26 candidate notes remain withdrawn/qualified. C3's frozen
filesystem-path clause remains partially falsified by prefix over-refusal,
including a new canonical claims alias refusal; no new capability or
province/frontier area is admitted. Grammar, races, source truth, semantic
QUALITY6 verification and outside discernment remain outside these controls.
Previous round26 frontier admission correction and carried debts stay in force.

## Round28 DERIVED honest-negative frontier status

The full C1 operability target is **not achieved / unprovable**.
Parent did not approve the proposed default/nested-root relaxation;
denylist not waived. No implementation or new measurement occurred.
Original production/oracles/controls, prior metric and ordinals remain
held; no new scalar, capability, Core graduation or promotion is claimed.

`lessons/round-28.md` and `evidence/round28-safe/claims.md` retain the full
negative scope. Opened S044–S045 are scoped API semantics and historical/
rejected diagnosis only; neither authorises the unapproved exception.
Original SOURCE rows/cells are untouched. V1/new-row hashes remain private.

`evidence/round28-safe/native-seats.json` holds per-native-ID terminal,
role, original-report-SHA and separate derived-record metadata.
`evidence/round28-safe/qualifiers.md` preserves VOID categories and available-byte
limits. Full raw report/distillation/tool bodies and executable draft
are private, not committed full bodies or live corpus/gate authority.
`evidence/round28-safe/provenance.json` records original→derived exclusions; no
universal content-safety or conformance certification is made.
Parent alone reviews publication, outside closure and later census/report.

## Round29 frontier disposition (2026-10-23)

New held ground: re-opening located quotes against their live registered
source (`knowledge/quote-reopen-r29.md`, `tools/quote-reopen.py`). This is the
first lane command that reads a source outside the lane corpus. Its scope is
fixed to `SOURCES.md` URLs, and an L0 question on that scope is open. Open
edges: pages without `</head>`, 2xx challenge pages, prefix and suffix
disambiguation, PDF sources, and three surviving mutants
(`lessons/round-29.md`). The round-26 to round-28 path-denylist debts are
carried unchanged.

## Round30 frontier disposition (2026-10-23)

Moved from frontier to held ground, measured on loopback only: pages that omit
`</head>` (C1, `QUOTE_REOPEN_HEADLESS_MATCH` 78/106 to 106/106) and the
quote re-open fetch bounds under slow senders and DNS rebinding (C2,
`QUOTE_REOPEN_FETCH_BOUND_MATCH` 12/27 to 27/27), both at lane revision
`49b2aa30`; `knowledge/quote-reopen-r30.md`, sources S050 to S056. Still open:
pages without a `<head>` start tag, 2xx challenge pages, PDF sources, prefix
and suffix disambiguation, resolver time inside the deadline, IPv6, and the
L0 fetch-scope question. The round-26 to round-28 path-denylist debts are
carried unchanged.

### 2026-10-23 correction — Round30 frontier disposition (routed defect D1)

The Round30 held-ground change is limited to pages that omit `</head>` (C1). C2 fetch bounds did not meet their frozen kill rule and are not held ground: `QUOTE_REOPEN_FETCH_BOUND_MATCH` was 26/27 on 3 of 44 fresh-seed runs. The round-30 spot-check's consolidated tally is `corpus/lessons/round-30-verifier-spotcheck.md:109` (this correction was routed at `:165-168`). The three miss receipts record `n=26`, `t=27`, and `predicate_holds=false`: `.ufo/waves/round-30/falsify/RerunC2B/run2.json:478-480`, `.ufo/waves/round-30/falsify/RerunC2B/run4.json:478-480`, and `.ufo/waves/round-30/falsify/RerunC2B/extra16.json:478-480`. The earlier disposition is retained as history.

## Round31 frontier disposition (2026-10-23)

Moved from frontier to held ground, measured on a synthetic fixture: a claim that names the line
or line range its span sits on (`"line"`; C1, `LINE_BINDING_MATCH` 50/120 to 120/120) and a claim
pinned to the SHA-256 of the exact source bytes it was made against (`"sha256"`; C2,
`REVISION_BINDING_MATCH` 50/120 to 120/120), both in `verify-claims` (round 32 correction, R4: first landed at `6d0ae19f`, superseded by the C2 fixes; the final round-31 gate is at `23536590`/`25c5bb70`, gate SHA-256 `0bc318b3…1258`);
`knowledge/line-binding-r31.md`, `knowledge/revision-binding-r31.md`, sources S057 to S059.
Still open: line binding for records' `## Claims` table pointers (`path:N`) in `verify` mode,
chain hops, uniqueness, and whether the named line is the right one for the claim's meaning; a
claim without a pin is not checked for revision. The quote re-open items of rounds 29 and 30 and
the L0 fetch-scope question stay carried.

## Round32 frontier disposition (2026-10-23)

Moved from frontier to held ground, measured on synthetic fixtures on gate `10f2fe12…`:

- Concurrent `verify-all --json` appenders (carried since round 24): the probe and the append are
  one `flock -x` critical section on the manifest's own open file; a writer that locks the manifest
  excludes the gate's probe and append (C1, `APPEND_SERIALIZED` 0/24 → 24/24 under counter v2;
  `knowledge/manifest-append-lock-r32.md`, S060).
- Exempt chain hops (round 3: "exemption is record-declared and unverifiable"): hops marked
  `unresolved`, `blocked-no-fetch` or `labelled-dead` are read with the resolved-hop rules and a
  resolvable one drifts with `CHAIN_EXEMPT_RESOLVABLE` (C2, `EXEMPT_AUDIT_MATCH` 0/132 → 132/132
  under counter v2; `knowledge/exempt-hop-audit-r32.md`, S061). `rejected` and `not-applicable`
  stay unread.

Still open: non-cooperating writers and network filesystems (C1); URL hops, transitive chains and
whether a local copy is the source the hop meant (C2); line binding for `## Claims` table pointers;
the quote re-open items of rounds 29 and 30 and the L0 fetch-scope question.

Round 33: the round-31 carry "nested `"line"`/`"sha256"` keys read as the record's own" moved to
held ground — `verify-claims` reads every field from the top-level object only, and a repeated
top-level read field is invalid (`TOPLEVEL_FIELD_MATCH` 60/156 → 156/156,
`knowledge/claim-record-fields-r33.md`, S062, S063). The round-32 exempt-hop audit is now verified
by a counter whose fixture metadata carries no truth (`evidence/round32/c2-count-v3.py`: landed
gate 132/132, metadata-order control 96/132). Still open from it: marker_default rows, keys spelled
with escapes, and the per-character cost of the bash reader on very long lines.

Round 34: spans of 32768..65536 bytes, which the matcher could not search at all (one argv pattern
of four bytes per span byte: E2BIG at 32768, PCRE2 size limit from 32765), are located by a 4096-byte
probe and confirmed against the whole span; `json_unescape` is linear (`LONGSPAN_MATCH` 25/42 → 42/42
under counter v3, `knowledge/long-span-argv-r34.md`, S064–S066). Not moved to held ground: the claim
is unverified because its required shortcut controls ended on provider holds. The PCRE dead zone
below the 4N-pattern threshold is **closed**: attempt 2 measured it as exactly the three lengths
32765–32767 bytes and routed them through the chunk matcher (`knowledge/dead-zone-pcre-r34.md`,
S065; the earlier "about 28000–32767" was the pre-data hypothesis, not a measurement). Still open:
spans above 65536 bytes, and long `verify-chain` quote anchors (now verified too, by R34NoHarm's
probe, but not counted).

Round 35: the gate's greps run against one pinned, verified absolute binary
(`knowledge/grep-pin-r35.md`, S067–S068; `GREP_PIN_MATCH` 0/9 → 9/9), the lane gains an
output-vs-routing witness for the keyed-engine class (`knowledge/keyed-engine-output-equivalence-r35.md`;
routing only — the entry's survivor table is the limit), and the `local a=$1 b=${#a}` dynamic-scope
read that shipped in round 34 is repaired with a probe that fails on the old bytes
(`knowledge/bash-local-expansion-r35.md`). It closes no row above; the engine-swap canary, per-record
witness attribution, `verify-chain` count and the fetch-scope answer stay open.

Round 37 (the round-36 canary/witness round's continuation): the claim `sha256` pin is hashed
through one pinned absolute `sha256sum` (`knowledge/claim-pin-provenance-r37.md`,
`CLAIM_PIN_PROVENANCE_MATCH` 2/7 → 7/7 on six seeds, three independent runners), and the
`--pin` capture child scrubs `BASH_ENV` with `env -u` (`knowledge/pin-capture-env-r37.md`,
S071 opened this round; `PIN_CAPTURE_ENV_MATCH` 3/7 → 7/7 on six seeds). Both observables sit
beside the round-1 scale (operability 3/10, delta 0). Still open: the prefix-64 attribution
bypass, the `argv-witness` dead fields, the metadata-screener locale seam, `counter_sha256`
in receipts, and the carried spans-≥-32768 debt.

Round 38 (the routed-debt round): the `--pin` capture's child runs through one pinned absolute
`env` (`knowledge/env-pin-capture-r38.md`, S072 opened this round; `ENV_PIN_CAPTURE_MATCH`
2/7 → 7/7 — 2/7 on BOTH base gates, `a7d3922c…` and the pre-round-38 `9fcac047…`), and
receipts become receipt-bound (`knowledge/receipt-binding-r38.md`, S073 `supersedes S070 —`;
`RECEIPT_BINDING_MATCH` 0/7 → 7/7 with a census-tied verifier; the waves falsified the first
freezing of both surfaces and the errata chain 1–12 records every narrowing). Both observables
sit beside the round-1 scale (operability 3/10, delta 0). Still open, pre-registered for
round 39: the PATH cells (env shim, bash shim), hostile-drift coverage, the positive
override-honoured and relative-refusal witnesses, the loader scrub (`LD_PRELOAD` on env and
on sha256sum), `verifier_sha256`/`subject_counter_sha256` receipt binding (demonstrated live
twice), the refusal-label re-derivation, the SimpCounters dead-field deletions, the
spans-≥-32768 debt, and the metadata-screener locale seam.
Round 40 advanced one narrow frontier subground: expectation-file digest identity. The r39 verifier rejected receipts whose expectation rows still tied but whose `expect_sha256` named older bytes; three active c1 measurements were reissued against the committed table, and the superseded draft stayed excluded. `knowledge/receipt-expectation-digests-r40.md` records the distinction and limits, citing the re-opened S059. This is evidence-provenance method, not a new gate mode or claim-truth proof.


| Entry | What it holds | Evidence |
|---|---|---|
| `knowledge/manifest-append-lock-r32.md` | Round-32 note: the round-24 probe/append race closed by one flock-held critical section on the manifest; why the manifest and not a sibling lock file; why the counter delays writes; limits | `S060`; `evidence/round32/claims.md` (design v2); `.ufo/waves/round-32/measure/after-c1-*.json` |
| `knowledge/exempt-hop-audit-r32.md` | Round-32 note: "could not be followed" audited locally for three statuses; what a `CHAIN_EXEMPT_RESOLVABLE` finding means; the 16 counter classes; limits | `S061`; `evidence/round32/claims.md` (design v2); `.ufo/waves/round-32/measure/after-c2-*.json` |
| `knowledge/claim-record-fields-r33.md` | Round-33 note: claim fields come from the top-level JSON object only; nested members ignored; repeated read fields invalid; why fail closed (RFC 8259 §4, Python `json`); limits | `S062`, `S063`; `evidence/round33/claims.md` (design v2); `.ufo/waves/round-33/measure/candidate/` |
| `knowledge/long-span-argv-r34.md` | Round-34 note: why a 32 KiB+ span failed (argv per-string limit, PCRE2 compiled size, `grep -f` one pattern per line); the probe-and-confirm fix; what counter v3 checks and cannot; limits | `S064`–`S066`; `evidence/round34/claims.md` (design v3); `.ufo/waves/round-34/measure/` |
| `knowledge/dead-zone-pcre-r34.md` | Round-34 attempt-2 note: the two ceilings of the one-pattern span matcher (argv per-string vs PCRE2 compiled size); the measured 32765–32767-byte window; why the planned "about 28000–32767" hypothesis shrank to three lengths; limits | `S065`; `evidence/round34/claims-a2.md` (design v4); `.ufo/waves/round-34/measure-a2/` |
| `knowledge/grep-pin-r35.md` | Round-35 note: why a PATH-resolved grep is a behaviour contract hole (PATH shim, `BASH_ENV` function, host `pi-uu-grep` builtin); the pin's resolution/refusal/echo contract; what self-reported provenance cannot prove | `S067`, `S068`; `evidence/round35/claims.md` §C1 + erratum; `.ufo/waves/round-35/{controls,measure,final}/` |
| `knowledge/keyed-engine-output-equivalence-r35.md` | Round-35 note: the keyed-engine class (fixture-shape, location and label keys); why no output counter can kill a correct alternative engine; fixture unpredictability + trace witness + the stated limit; the three measured survivors and the r36 canary family | `.ufo/waves/round-34/w2a2/MutC2Keyed.md`; `evidence/round35/claims.md` §C2 + erratum; `.ufo/waves/round-35/final/c2-s*.json`; `.ufo/waves/round-35/w2/` (survivor seats) |
| `knowledge/bash-local-expansion-r35.md` | Round-35 note: `local` evaluates every RHS before assigning, so a derived value in the same statement reads the caller's dynamic scope; the shipped `slen` case, the probe, the sweep rule | `tools/research-gate.sh`; `.ufo/waves/round-35/repairs/slen-probe.sh`; `evidence/round35/claims.md` §R1 |
| `knowledge/engine-swap-canary-r36.md` | Round-36 note: fourteen swap/contract scenarios, four new separations (manifest hash shim, C-locale decode, pin echo isolation, drift token); the narrowed S7-S9 reading and the per-record attribution that keeps a no-call gate from scoring | `S070`; `evidence/round36/claims.md`; `.ufo/waves/round-36/measure/` |
| `knowledge/per-record-argv-attribution-r36.md` | Round-36 note: the NUL-delimited argv witness separates the five output-equivalent engines per record, writes the channel outside the gate environment, and does not false-kill a renamed matcher; the recorded limits (global threshold, prefix-64 bypass) | `S069`; `evidence/round36/claims.md`; `.ufo/waves/round-36/measure/c2-*.json` |
| `knowledge/claim-pin-provenance-r37.md` | Round-37 note: the claim `sha256` pin is hashed through one pinned absolute `sha256sum`, never the caller's PATH; the seven scenarios; PATH-independence is not tamper-proof hashing | `S070`; `evidence/round37/claims.md`; `evidence/round37/receipts/c1-*.json` |
| `knowledge/pin-capture-env-r37.md` | Round-37 note: the `--pin` capture child runs `env -u BASH_ENV` (S071), so a startup file cannot move a baseline; the seven scenarios; gate-process `BASH_ENV` and `--posix`/`ENV`/`SHELLOPTS`/`TMPDIR` stay named debt | `S071`, `S068`; `evidence/round37/claims.md`; `evidence/round37/receipts/c2-*.json` |
| `knowledge/env-pin-capture-r38.md` | Round-38 note: the capture's child runs through one pinned absolute `env` (S072), so a caller-exported `env` function cannot interpose; both delivery mechanisms; the narrowed reading (PATH half, sibling names, bash vectors unmeasured but named) and the harness scrub that carries the measurement | `S072`; `evidence/round38/claims.md` (15 errata); `evidence/round38/receipts/c1-*.json` |
| `knowledge/receipt-binding-r38.md` | Round-38 note: receipts bind pre==post gate hashes, counter/expect/receipt digests, verified by a census-tied verifier; the wave-1 kills it closed; integrity-and-self-consistency, NOT authorship (the F2 residual, verify side) | `S073` (supersedes S070); `evidence/round38/claims.md`; `evidence/round38/receipts/c2-*.json` |
| `knowledge/capture-bash-pin-r39.md` | Round-39 note: the capture grandchild and the verify-all section children run through ONE pinned absolute `bash` (override + `BASH_PROVENANCE` refusal); the three pinned call sites; 7/8 → 8/8 with the base and PATH-`env`-mutant discrimination controls; limits (sibling bare names, loader env, noexec) | `S071` (re-opened 2026-10-24), `S072`; `evidence/round39/claims.md`; `evidence/round39/receipts/c1-*.json` |
| `knowledge/receipt-verifier-subject-r39.md` | Round-39 note: receipts bind `verifier_sha256` + `subject_counter_sha256`, re-derived by the verifier with named refusals; the r38 pipeline as before-state control; the three vacuous-fixture self-catches and their fixes (QUALITY 56) | `evidence/round39/claims.md`; `evidence/round39/receipts/c2-*.json`; `lessons/round-39.md` |
| `knowledge/receipt-expectation-digests-r40.md` | Round-40 note: a receipt's `expect_sha256` binds exact expectations-file bytes, not only scenario rows; the three regenerated c1 receipts and superseded draft disposition; hash identity does not establish authorship or semantic truth | `S059` (re-opened 2026-10-24); `evidence/round40/claims.md`; `.ufo/waves/round-40/controls/r1-stale-before.txt`; `evidence/round40/c1-count.py` |
| `knowledge/capture-path-pin-r41.md` | Round-41 note: the canonical capture's full invocation surface — parent capture functions, startup, and the captured verify-all child — resolves through the pinned tool table (r35-wrapper pattern, 14 names) plus a fixed child PATH and loader scrub; 728-call instrumentation run, 1/12 → 12/12; limits (BASH_FUNC_* delivery, noexec, escape hatch) | `S075`, `S076`, `S067`; `evidence/round41/claims.md`; `evidence/round41/receipts/`; `.ufo/waves/round-41/controls/control-before.txt` |
| `knowledge/citation-version-binding-r36.md` | Round-44 note: what binds a citation to a prior state — RFC 7089's Memento-Datetime promise that the reflected resource state will no longer change, the archive-veracity limit the same document puts out of scope, and why a byte-span check against an archived capture checks the capture, not the origin's past output; the staged S082 (GB/T 7714-2025 record) half is not adopted, with its flip | `S079` (RFC 7089 capture, byte offset 14896); `evidence/round44/claims.md` §C3; `lessons/round-44.md` `## Gate`; `.ufo/waves/round-44/w3/W3RevS079.md`; `.ufo/waves/round-44/w3/W3SimpIds.md` |
| `knowledge/citation-version-binding-r37.md` | Round-44 note: a non-Western version anchor — the NDL WARP FAQ's archive cadence for national, public and private institutions, and the NDL current-awareness E2867 move to URLs that embed the capture timestamp (`warp.ndl.go.jp/web/20250102112233`); the cadence is the operator's own statement and not a Memento header, and the example URL is a citation form, not proof of byte identity; the staged S093 (Portico) half is not adopted, with its flip | `S080` (WARP FAQ capture), `S081` (NDL E2867 capture); `evidence/round44/claims.md` §C3; `lessons/round-44.md` `## Gate`; `.ufo/waves/round-44/w2/W2ReviewWarp.md` |
| `knowledge/evidence-archive-field-policy-r41.md` | Round-45 note: what a verification corpus's archive fields document — AVeriTeC's evidence-level `cached_source_url` stated without condition and backed by the paper's caching sentence, the claim-level `cached_original_claim_url` best-effort ("Where possible"), an empty claim archive recording only that no link is stored, and the corpus's own warning that double-archived links return a 404 at archive.org, so a filled archive field is a link to open, not proof of a resolving capture; the staged pool-versioning amendment was refused in round 45 and ADOPTED in round 46 once the base entry was held and its prose ids were re-bound by document (`knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`, round-46 supersession) | `S082` (README capture chars 1027, 1969), `S083` (paper capture chars 14575, 120884); spans `evidence/round45/spans/`; `evidence/round45/claims.md` §C3; `lessons/round-45.md` `## Gate`; `.ufo/waves/round-45/w1/CritFieldPolicyInference.md` |
| `knowledge/evidence-snapshot-coverage-r40.md` | Round-45 note: how much of a verification corpus is bound to a snapshot, counted by value — AVeriTeC train: 6,510 of 6,511 evidence fields filled but 551 of the filled values are not archive links (429 the `Metadata` placeholder), 1,582 sourced answers carry no archive field, 5,959 of 7,572 real-source answers (78.7%) carry a web.archive.org link, 1,145 of 2,531 claim archives filled; the one empty evidence field has no source URL, so counting empty fields finds the wrong case | `S084` (train.json capture sha256 `ae5eda7c…`); `evidence/round45/counts.json`; `evidence/round45/claims.md` §C3; `.ufo/waves/round-45/w1/ExecEmptyEvidenceRecord.md`; `.ufo/waves/round-45/w1/CritSnapshotInference.md` |
| `knowledge/evidence-pool-versioning-r39.md` | Round-46 note: what makes a support verdict durable inside a verification corpus — FEVER binds a verdict to a Wikipedia URL and a sentence id inside a pool dated by the June 2017 dump (no per-page revision field), the deposit is one record whose `conceptdoi` names its version series, with the pool shipped as one `wiki-pages.zip`, and the evidence-selection step has its own measured reliability (annotation precision/recall against super-annotators, 0.6841 inter-annotator agreement, multi-sentence evidence shares); limits — a verdict surviving the pool's own revision history is unaddressed, `grep -c revision` over the page is 0 | `S085`, `S086`, `S087`; `evidence/round46/spans.tsv`; `evidence/round46/c3-count.py`; `lessons/round-46.md` |
| `knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` | Round-46 note: the successor corpus's per-citation binding — `cached_source_url` documented as an archive.org link beside `source_url` (claim-level archive hedged `Where possible`), `claim_date` as a claim property, four labels including conflicting evidence, and the pipeline's operational temporal constraint (evidence `published before the claim's date`); corrections over the staged text — the answer-object pairing is documented practice not a schema invariant, the hedge tracks a missing `original_claim_url`, and the staged restriction sentence is not verbatim in the capture | `S088`, `S089`; `S079`, `S081` (re-bound by document); `evidence/round46/spans.tsv`; `lessons/round-46.md` `## Gate` |
| `knowledge/claim-support-test-r37.md` | Round-47 note: what a support test is — PEOPLEPROFILES' two definitions (supporting/refuting evidence as "greater reason to believe" c true/false, all else equal) and its no-evidence rule (select no sentence), FEVER's declared NEI null tuple `[Annotation ID, Evidence ID, null, null]`, CFEVER's same three labels over 30,012 Chinese-Wikipedia claims, and the measured ∼22% / ∼30% unsupported-claim rates; the support relation is evidential strength, not entailment or similarity; limits — whether the definitions are a decision procedure or an annotator label is open, and the staged "conflation" claim is narrowed against `claim-support-states-r24.md` (contradicted vs unresolved already held) | `S085` (re-bound by document), `S090`, `S091`; `evidence/round47/spans.tsv`; `evidence/round47/c3-count.py`; `lessons/round-47.md` `## Gate` |
| `knowledge/claim-support-test-r37-amendment-2026-10-23.md` | Round-47 note: how the support test is applied and how reliable it is — FEVER's annotator decision rule and evidence boundary (common-sense reasoning, no world knowledge, Skip then "Not enough information"), climate-fever's per-sentence micro-verdicts over 7,675 claim-evidence pairs aggregated to SUPPORTS/REFUTES/DISPUTED/NOT_ENOUGH_INFO, CorFEVER's Cohen's κ 0.792 and its 202 NEI claims relabelled from open-web evidence (NEI is evidence-relative); FEVER's 0.6841 Fleiss κ is cited from the held `evidence-pool-versioning-r39.md`, not re-claimed; corrections over the staged text — the decision-rule quote ("strong … the claim"), the "no evidence-step figure" Unknown (the lane holds recall 72.36%) | `S092`, `S093`, `S094` (re-bound by document); `S086` (held); `evidence/round47/spans.tsv`; `lessons/round-47.md` `## Gate` |
| `lessons/round-48.md` | Round-48 correction and evidence ledger: held-out false-refusal repair, R39/R40 receipt revision-drift disposition, all 24 quarantined chousa register rows, one lesson-bound S095 source, and observed R47 SCORECARD corrections | `S095`; `corpus/evidence/round48/claims.md`; `corpus/evidence/round48/measure-after.txt`; `.ufo/waves/round-48/w1/`; `.ufo/waves/round-48/w2/` |
| `evidence/round48/` | Frozen C1 claim and pre-control; held-out precision count; five refinement fixtures; mutant sensitivity checker; name-keyed composite shortcut control; round-39/40 receipt recheck; after-measurement at code commit `671b096e` | `corpus/evidence/round48/claims.md`; `controls/before.txt` + `controls/before-erratum.txt`; `controls/name-key-control.txt`; `receipt-recheck.txt`; `measure-after.txt` |
| `knowledge/aggregator-vs-source-r36.md` | Round-49 note (adopted by document from `merge/chousa/`): a citation index's reference list and count are derived — CiNii's own statement that its 参考文献 are matched items only (S096), J-STAGE's days-to-two-weeks link creation (S097) and its four-rung resolution ladder ending in reference-text parsing (S098), lateral reading as a tested outside-the-source move (S099, abstract only); the staged NCPSSD homepage row refused | `S096`–`S099`; `corpus/evidence/round49/spans.tsv`; `corpus/lessons/round-49.md` `## Gate` |
| `knowledge/citation-count-semantics-r37.md` | Round-49 note (adopted by document): what a CNKI count is a count of, as copies and third-party guides state it — a co-authorship self-citation rule and zero-count rows not listed (S100), the data specification's 文献标志码 and GB/T 7714 / ISO 690 split (S101), separate citation and download columns (S102), the AI trace panel's source and counter fields (S103) | `S100`–`S103`; `corpus/evidence/round49/spans.tsv`; `corpus/lessons/round-49.md` `## Gate` |
| `lessons/round-49.md` | Round-49 lesson: first package adoption under addendum section 10 (collision check, renumber map, re-opened quotes, register re-checks, admit/refuse table), a05 correction and its check, hollow-quote and replay counter limits, capture-age criterion | `corpus/evidence/round49/`; `QUALITY.md` 69 note, 71, 72 |
| `evidence/round49/` | Frozen C1/C2 claims and counters, controls, the UTF-16LE-aware span builder and its 28-row manifest, a05/quote-substance/capture-age checks, post-freeze disclosure | `corpus/evidence/round49/claims.md`; `claims-erratum.md`; `controls/` |
| `../tools/assimilate-rows.py` | Round-49 section-10 adopter: by-document renumbering with one simultaneous substitution, census-schema rows, 0–3-space collision lists | `corpus/evidence/round49/c1-count.py` |
