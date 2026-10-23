---
name: chousa-shokunin
description: "Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification. Triggers: 'research this', 'deep research', 'verify this claim', 'primary source', 'citation chain'. Anti-trigger: NOT bounty-program scope (kasegi), NOT model-quality claims (kengaku), NOT external live-target fetching without operator approval. Rank: shonen."
---

# chousa-shokunin — deep-research method (調査)

Domain: the reusable METHOD of source research — how a question is framed, which
sources outrank which, how a citation chain is followed, and how a claim is
verified against its source. Not the bounty programs (kasegi) and not model
quality (kengaku).

## Decision table

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| Research a question | question framing → source hierarchy → chain → claim check | starting from a search box with no question | a research record with a declared question |
| Rank sources | primary > secondary > aggregator > unsourced claim | treating an aggregator as a primary source | hierarchy row per source |
| Follow a citation chain | follow each hop to the cited artifact and resolve its anchor there | stopping at a summary of the citation | chain with each hop's anchor verified or marked unresolved |
| Verify a claim | claim → source → the source's own evidence | accepting a restatement as the source | verified / contradicted / unresolved |
| Reuse a finding | cite the artifact + the revision read | citing a memory of it | resolvable pointer |
| Admit a source for one claim (r24) | per-claim admission row — role, provenance, method fit, recency, interests, independence, availability; the ladder above is the default ordering, the row overrides it with a stated reason | treating a source label as authority for every claim | tier-for-this-scope + suitability reason (`corpus/knowledge/contextual-source-admission-r24.md`) |
| Report claim support (r24) | four separate observations: opens · on-topic · states the claim at a named anchor · true | `verified` from access or relevance alone; truth from support alone | the four states recorded; `verified` requires state 3 (`corpus/knowledge/claim-support-states-r24.md`) |
| Cite a located quote from a registered web source (r29) | from the lane root run `python3 tools/quote-reopen.py verify --items <tsv>` (`id`, `source_id`, `quote`) before citing; `corpus/knowledge/quote-reopen-r29.md` | citing a quote not re-opened this round; reading `VERBATIM` as support or truth; dropping an `ABSENT`/`UNREACHABLE` | one verdict per quote (`VERBATIM`/`ABSENT`/`TOO_LONG`/`NO_SOURCE`/`UNREACHABLE`); a non-`VERBATIM` quote is re-opened by hand and recorded (QUALITY 25) |
| Re-open a quote on a page whose HTML omits `</head>` (r30) | `python3 tools/quote-reopen.py verify --items <tsv>`; contract v2 item 1 ends the head at `</head>`, `<body>`, the first start tag that cannot be in `head`, or non-whitespace text (`corpus/knowledge/quote-reopen-r30.md`, S050, S051) | treating a missing `</head>` as the end of the page; reading `VERBATIM` as support or truth | one verdict per quote; a page without a `<head>` start tag is still out of scope |

**Provenance of the table above (appended 2026-10-15).** The primary > secondary >
aggregator > unsourced tiers are **this lane's own construction**, not a rule
inherited from another lane and not a statement the survey exports make — an
independent audit measured zero `proposal` tokens and zero independently cited
admissions in this skill at mint. Treat the hierarchy as the lane's working
standard, and any row whose only warrant is this table as a `proposal` until it
carries a `path:line` from a real artifact. The exports state no tier system; the
fleet gates state citation *mechanics* (resolvable, pinned, labelled), not this
ranking.

Where the lane learns: `corpus/SOURCES.md` (opened rows, scoped A/B/C tiers, study paths, search log); admission stays in `corpus/QUALITY.md`.

## Error patterns

| Observation | Reading |
|---|---|
| source cited but not read | the claim is unsupported; record as unresolved |
| aggregator quoted as primary | hierarchy violation — re-derive from the primary |
| chain ends at a dead link | chain broken; record the hop and stop |
| two sources disagree | report both; do not average them |
| hop anchor resolves but the relay drops a qualifier | altered hop — `resolved` is not faithful; compare proposition, scope, quantity, hedge, date at that hop (`corpus/knowledge/citation-chain-fidelity-r24.md`) |
| body quote `ABSENT` on a page that omits `</head>` (r30) | a head boundary that waits for `</head>` drops the whole page; contract v2 item 1 ends the head at the first token the HTML in-head rules do not handle (S051) |
| a fetch outlives its stated deadline under a slow sender (r30) | a socket timeout bounds each operation, not the transfer (S052, S054); bound the whole fetch with one deadline and read an end of stream at the deadline as `UNREACHABLE`, not as a full page |
| the address check passes and the connection goes elsewhere (r30) | the name was resolved twice, once to check and once inside `create_connection` (S053); resolve once per hop, connect to a validated address, keep the host name for `Host` and TLS (S055) |

## Boundaries (hard)

- **Refuses external live-target research without operator approval.** A window
  without an approval table is loopback-only. The approval table is itself a
  chousa deliverable.
- **Refuses bounty-program scope** — that is kasegi (program rules, claim packages).
- **Refuses model-quality claims** — that is kengaku.
- **Refuses orchestration and multi-agent dispatch** — swarm waves, agent
  lifecycle, dispatch mechanism are kumitate; a survey that finds such material
  routes it out rather than absorbing it.
- Credentials/session material shape-only; no secret values in any record.

## Checklist (executable)

- [ ] Every claim carries a resolvable pointer to the artifact and revision read.
  - Run: `bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` with a `"sha256"` pin (the SHA-256 of the exact source bytes read) on each claim; a changed source reads `stale` (`CLAIM_SOURCE_REVISION_MISMATCH`). A claim without a pin is not checked for revision.
- [ ] A negative claim carries its search sweep, naming where it looked.
- [ ] Observation, inference and unknown stay separate.
- [ ] A rejected source is kept with its rejection reason and flip-condition.
- [ ] Every web quote a round cites was re-opened with `python3 tools/quote-reopen.py verify` and every non-`VERBATIM` verdict is recorded with its quote (an `ABSENT` on a page whose text the tool cannot extract, such as one without `</head>`, is a tool limit).

## Gates

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `research-gate` | gate | `bash tools/research-gate.sh verify <record> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`) · `1` failed (`DRIFT`) · `2` could-not-evaluate (setup/usage) | `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (228 cases)` | expected exits/finding IDs in `tools/research-gate.sh`; archive digests/expected verdicts in `corpus/evidence/round-1/expected.json` | verify: zero writes; selftest: its own temp dir; no network | chousa |
| `research-gate verify-claims` | gate | `bash tools/research-gate.sh verify-claims <claims-file> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`; every claim matches its pre-registered `expect`) · `1` drift (`DRIFT`; any `observed` ≠ `expect`, or refused/invalid records) · `2` could-not-evaluate (setup/usage) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, claims cases 21–30 and 41–42, r31 line-binding cases 216–219 and revision-pin cases 220–228 | per-claim `expect`s and counts in `corpus/fixtures/claims-r2.README.md` (`claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0`); finding IDs in `tools/research-gate.sh` | opens cited local sources only (canonical files under `CHOUSA_ROOT` or the lane root); URLs, session and out-of-corpus paths refused, never fetched; zero writes | chousa |
| `research-gate verify-chain` | gate | `bash tools/research-gate.sh verify-chain <record> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`; every non-exempt hop `verified`) · `1` drift (`DRIFT`; any `anchor-missing`/`refused`/`invalid` hop or finding) · `2` could-not-evaluate (setup/usage) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, chain cases 31–40 and 43–44 | pre-registered hop ground truth in `corpus/fixtures/chain-r3.README.md`: `chain-r3.md` 22 hops → `RESOLVED_HOPS=17/22` CLEAN, control `chain-r3-broken.md` → `RESOLVED_HOPS=1/2` DRIFT; finding IDs `CHAIN_SOURCE_*`/`CHAIN_ANCHOR_NOT_FOUND`/`CHAIN_CITATION_INVALID` in `tools/research-gate.sh` | opens cited local sources only (same canonicalization and boundary as `verify-claims`); URLs, session and out-of-corpus paths refused unopened, never fetched; zero writes | chousa |
| `research-gate verify-sweeps` | gate | `bash tools/research-gate.sh verify-sweeps <record> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`; every sweep verified or exempt and every rejection complete) · `1` drift (`DRIFT`; any incomplete rejection, any false/unnamed/unresolved/out-of-corpus sweep, or finding) · `2` could-not-evaluate (setup/usage) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, sweeps cases 45–54 | pre-registered ground truth in `corpus/fixtures/sweeps-r5.README.md`: `sweeps-r5.md` → `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN exit 0; control `sweeps-r5-broken.md` → `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE` DRIFT; finding IDs `SWEEP_REJECTION_INCOMPLETE`/`SWEEP_LOCATION_*`/`SWEEP_CLAIM_FALSE` in `tools/research-gate.sh` | opens the local path/glob sets sweeps name only (same canonicalization and boundary as `verify-claims`); URLs, session and out-of-corpus paths refused unopened, never fetched; zero writes | chousa |
| `research-gate verify-integrity` | gate | `bash tools/research-gate.sh verify-integrity <record> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`; every extracted reference token resolves or is exempt) · `1` drift (`DRIFT`; any `REF_UNRESOLVED`) · `2` could-not-evaluate (setup/usage) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, integrity cases 65–73 | pre-registered ground truth in `corpus/fixtures/integrity-r7.README.md`: `integrity-r7.md` → `INTEGRITY refs=16 resolved=15 unresolved=0` CLEAN exit 0; control `integrity-r7-broken.md` → `INTEGRITY refs=16 resolved=13 unresolved=2` DRIFT naming `REF_UNRESOLVED` ×2 (`S9` chain row 4 `from`; `C9` sweeps row SW3 `claim_id`); finding id `REF_UNRESOLVED` in `tools/research-gate.sh` | reads the record's own cells only (declared ids and reference cells; no cited source ever opened); zero writes; no network | chousa |
| `research-gate verify-all` | gate | `bash tools/research-gate.sh verify-all <record> [--claims PATH] [--json PATH] --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`; composed — every run section clean, absent sections reported) · `1` drift (`DRIFT`; composed — any run section dirty) · `2` could-not-evaluate (setup/usage) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, verify-all cases 55–64 and 74, integrity cases 65–73, `--json` manifest delimiter cases 134–136 | pre-registered ground truth in `corpus/fixtures/integrity-r7.README.md` (r7, five sections) and `corpus/fixtures/full-r6.README.md` (r6 revision, `sections=4`): `integrity-r7.md` → composed CLEAN `run=5 absent=0` with `INTEGRITY refs=16 resolved=15 unresolved=0`; `integrity-r7-broken.md` → composed DRIFT `drift-sections=1` with only `integrity` dirty, exactly two `REF_UNRESOLVED` (`S9` chain row 4 `from`, `C9` sweeps row SW3 `claim_id`); the r6 trio at this revision composes `full-r6.md` CLEAN `run=5`, `full-r6-broken.md` DRIFT `drift-sections=2` naming `chain`+`sweeps`, `full-r6-absent.md` CLEAN `run=4 absent=1`; archive-scale negative controls, pre-registered in `corpus/fixtures/archives-r9/controls/README.md` (r10, gate at that revision `46f5ddbf…`): six broken copies of the r9 archive records, one per defect class — span-not-found `CLAIM_SPAN_NOT_FOUND` (`VERDICT_BEARING_CLAIMS=9/10`), anchor-missing `CHAIN_ANCHOR_NOT_FOUND` (`RESOLVED_HOPS=5/7`), rejection-missing-flip `SWEEP_REJECTION_INCOMPLETE` (`REJECTIONS_OK=2/3`), false-sweep `SWEEP_CLAIM_FALSE` (`VERIFIED_SWEEPS=0/1`), dangling-ref `REF_UNRESOLVED` (`refs=15 resolved=13 unresolved=1`), structure-break `NO_QUESTION` — each composed DRIFT `drift-sections=1 findings=1`, exit 1, with the A/B/C records CLEAN | runs the solo modes as fresh CLI calls over the same canonicalized local files; absent optional sections reported, never drift; `--json` appends one state line to PATH (append-only; refused outside `verify-all`; a non-`\n` last byte is terminated first and a non-empty unreadable manifest is refused before any write — r24, `knowledge/json-delimiter-r24.md`); no network | chousa |
| `research-gate verify-metadata` | gate | `bash tools/research-gate.sh verify-metadata <entry-or-dir> --root .` | `0` clean (`RESEARCH_GATE: CLEAN`; every screened entry carries `source:`, a dated `verified-at:` and a `recheck:` in its header) · `1` drift (`DRIFT`; any `META_SOURCE_ABSENT`/`META_VERIFIED_AT_ABSENT`/`META_VERIFIED_AT_UNDATED`/`META_RECHECK_ABSENT` warn or `META_ENTRY_REFUSED` crit; `META_RECHECK_UNSCHEDULED`/`META_RECHECK_ROOT_PARENT` info drift only under `CHOUSA_STRICT=1`) · `2` could-not-evaluate (no path, missing path, directory without `.md`) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, metadata cases 137–154 | spec v1 `corpus/evidence/round25-claims.md` (Claim 1); fixtures `corpus/fixtures/metadata-r25/` (27 files, README table) agree with the gate and the oracle `corpus/evidence/round25-meta-oracle.py` in 54/54 cells (`bash corpus/evidence/round25-meta-differential.sh`); the lane corpus screen (round 25) → `METADATA_COMPLETE=25/28` naming `archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md` (`META_RECHECK_ABSENT`) | parses the header region (lines before the first unfenced `## `) of each direct `*.md` child; denylisted/over-8-MiB entries refused unread, NUL-bearing entries read for the NUL probe then refused unparsed; never fetches; writes nothing | chousa |
| `research-gate --pin / --drift` | gate | `bash tools/research-gate.sh --pin PATH` · `bash tools/research-gate.sh --drift PATH` | `0` none (`GATE_DRIFT: none` — compared and equal) · `1` drift (`GATE_DRIFT: <changed tokens>`, incl. `volatile_fields` when the baseline's declared contract differs from the current one) · `2` could-not-evaluate (baseline missing/unreadable/malformed, or the canonical capture/write failing) | shared `bash tools/research-gate.sh --selftest` → `PASS (228 cases)`, pin/drift cases 75–85 | the canonical invocation (`verify-all record.md --claims claims.jsonl --json manifest.jsonl --root .`, cwd = a fresh temp fixture the gate writes itself and never commits) and the volatile contract `ts gate_sha256` recorded verbatim in every baseline header; the lane's committed baseline `corpus/evidence/gate-baseline-r12-20261019T115519Z.json` (sha256 in `knowledge/gate-baseline-r12.md`; header `gate_sha256=91a01695…`; `--drift` against it at this revision measures `GATE_DRIFT: none`, exit 0) and its re-run recipe; the superseded r8 baseline stays committed as history (`--drift` against it names `GATE record_sha256`, exit 1, by the recorded r12 re-pin reason) | `--pin` writes PATH only; `--drift` zero writes; neither prints a `RESEARCH_GATE` line; a record/claims/`--json`/`--root` argument is refused (exit 2); no network | chousa |
| `quote-reopen verify` (r29) | tool | `python3 tools/quote-reopen.py verify --items <tsv> [--registry corpus/SOURCES.md]` | per item `NO_SOURCE` > `TOO_LONG` (over 25 words) > `UNREACHABLE` > `VERBATIM`/`ABSENT`; exit `0` all `VERBATIM` · `1` any other verdict · `2` usage/IO | frozen counter `python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify` → `QUOTE_REOPEN_MATCH=130/130` (40 fixture items, 42 derived variants, 48 page-sampled items; fresh seed each run) | contract `corpus/evidence/round29/claims.md` (design v3); fixture `corpus/fixtures/quote-reopen-r29/` | GET only to http(s) URLs of registry rows; non-global addresses, non-http(s) redirects and userinfo refused; 30 s total per URL, 8 MiB wire and inflated cap; memory only, zero writes | chousa |
| `quote-reopen` round-30 counters | gate | `python3 corpus/evidence/round30/c1-count.py` · `python3 corpus/evidence/round30/c2-count.py` (lane root; `--tool PATH`, `--receipt OUT.json`) | `QUOTE_REOPEN_HEADLESS_MATCH=106/106` · `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` exit `0`; any other count exit `1`; harness error exit `2` | before on the round-29 tool: 78/106, 12/27; tool absent: 0/106, 0/27 | contract `corpus/evidence/round30/claims.md` (design v4, tool contract v2); harness `corpus/evidence/round30/qr_harness.py` | loopback harness only, no network; writes a receipt only when `--receipt` is given | chousa |

**Round-25 final registry correction.** (Round 31: the rows above now read `PASS (228 cases)`.) The shared `154 cases` tally in the
rows above records checkpoint `d8c8cff`; the final shared selftest is
`PASS (161 cases, 0 skipped)` (metadata cases 137–161).
`corpus/evidence/round25-final-measure.log` and `round25-final-holds.log`
supersede that tally without relabelling the historical checkpoint.
For `verify-metadata`, the first literal unfenced `## ` ends the header;
scheduled recheck dates must be calendar-valid (`verified-at` stays shape-only).
The final reader binds a bounded snapshot to an opened fd, refuses
multilinks/stat failure and rechecks its resolved path.
Structured-result paths are shell-quoted and recheck tokens never emitted;
shared setup/open diagnostics can still contain raw pathnames.
The original 27-fixture differential remains 54/54; case 154 was revised
and seven further case slots added. See
`corpus/knowledge/metadata-screen-r25.md` final-reader correction for limits.

**Scope screen (rounds 12, 17).** The structure check screens a record's DECLARED scope: `## Meta` rows keyed `domain`/`scope` (table and `key: value` forms), never prose. A declaration naming a refused province — `bounty program(s)`/`claim package(s)`/`kasegi`; `model quality`/`model evaluation(s)`/`kengaku`; `orchestration`/`dispatch mechanism`/`multi agent dispatch`/`swarm wave(s)`/`agent lifecycle(s)`/`kumitate` (full lists in the header) — emits its `SCOPE_*_ABSORBED` finding at warn (drifts, exit 1), one per matched province per declaration row. Bare `dispatch`/`swarm`/`evaluation`/`bounty`/`model` are NOT triggers (B-archive vocabulary); negations are not parsed (named limit). Selftest cases 86-92 pin the three provinces, both clean grammars, the declared near-miss, and the prose decoy; measured `verify` on B-r9 → 0 `SCOPE_` findings. Round 17 closed the fenced-heading shadow: a `## ` line inside a fenced code block is literal text, not a heading — a fenced `## Meta` can no longer shadow the real declaration. The `load_sections` parser pairs fences in two passes (same char, closing length >= opening, 0–3 literal-space indent; unclosed opener = fence to EOF, fail closed). Cases 112–116 pin the five shadow variants.

**Size cap (round 12).** Claim/chain sources over 8 MiB (`SOURCE_READ_MAX_BYTES`) are refused BEFORE any read at the shared `claim_source_path` chokepoint — `CLAIM_SOURCE_READ_TOO_LARGE` / `CHAIN_SOURCE_READ_TOO_LARGE` (warn), per-item `observed=refused`, never partially searched. Record reads (`load_sections`, `scan_secrets`) and the verify-all claims-surface binding stay uncapped (ledger row 9 partial closure). Selftest cases 95-98 straddle the boundary (8388608 reads / 8388609 refuses). Companion fix: `count_nl` is linear (was quadratic: >60 s at 8 MiB).

**Banner contract (round 12).** `VERSION=v2` — the revision token alone, no program-name stutter — at all six banner sites; the token is a declared non-volatile contract word, so renaming it is drift and the selftest pins both the literal (case 93) and the drift behavior (case 94: a VERSION mutant reads `GATE_DRIFT: GATE`). The r8 baseline was re-pinned at final bytes with the recorded reason (`knowledge/gate-baseline-r12.md`).

**Multi-link refusal (round 13).** Sources with `st_nlink != 1` are refused unread at the same chokepoint (one `stat -c '%s %h'` probe serves this and the size cap): `CLAIM_SOURCE_MULTILINKED` / `CHAIN_SOURCE_MULTILINKED`, crit. Live bypass receipts `corpus/evidence/alias-r13-20261019T123621Z-bypass-{before,after}.log` (an in-root hardlink alias of an out-of-corpus file read CLEAN before; refused after). Named limits (`corpus/knowledge/hardlink-alias-r13.md`): TOCTOU, same-device bind mounts, unmeasurable-stat fallback, and legit in-root multi-link families refusing (selftest case 101 pins the trade). Selftest cases 99-102.

**Cross-device refusal (round 14).** Sources whose st_dev differs from the resolving root's device (the root whose prefix matched, longest wins) are refused unread at the same chokepoint: `CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`, crit — one `stat -c '%s %h %d'` probe now serves the r13 nlink check, the r12 size cap, and this device check, in that order (a combined source reports the earliest class). Live receipts `corpus/evidence/mount-r14-20261019T132025Z-bypass-{before,after}.log`; selftest cases 103-106 (namespace-mounted fixtures; case 106 is the lane-fallback control that defeats a naive ROOT-only compare). Named limits (`corpus/knowledge/mount-alias-r14.md`): same-device binds (stat-invisible), overlay roots, TOCTOU, unmeasurable-stat fallback.

**Root-slash boundary (rounds 15–16).** The `--root /` prefix test was dead: `"$root_r"/*` rendered `//*` when `root_r=/`, matching nothing, so every absolute source refused `OUT_OF_CORPUS` crit. One `in_root()` helper (`tools/research-gate.sh` ~:612) strips all trailing slashes for the prefix test only — `//` → `/` → `""`, `""/*` renders `/*` — and all three same-class sites converted (`claim_source_path`, `ptr_resolves_meta`, `sweep_path_guarded`). `src_root` keeps the un-normalized root so the r14 device probe still stats the declared root. A materialized helper is mandatory: inline `case "$canon" in "${root_r%/}"/*)` is itself dead when the expansion strips to empty (measured, bash 5.3.15). The r16 verification wave found `--root //` still refused (single-strip left `/`); the loop strips all trailing slashes. Selftest cases 107–111 pin the healed arms via a `CHOUSA_ROOT=` env-override channel in the harness. Receipts `corpus/evidence/root-r15-20261019T152000Z-*.log`. Named limits (`corpus/knowledge/root-slash-boundary-r15.md`): with `root_r=/` the sweeps guard is vacuous by declaration; the inline-strip quirk is measured on bash 5.3.15 only.

**Verified scope, not field readiness.** At gate revision
`31b46832e56a7f095092a4a6d62b74bfaf6933e8`, the real CLI emits exactly one
DRIFT summary and exits 1 on each pinned A/B/C archive. The locally sourced
intake emits CLEAN and exits 0. Full output, exit codes and input/script
digests: `.ufo/evidence/round-1/acceptance.json` and `acceptance.txt`.

The old “unchecked grep” diagnosis is superseded: the non-strict informational
branch of `emit_finding` returned false under CLI errexit. Recording a finding
now returns success; counters determine the verdict. Informational findings
remain non-fatal unless strict mode promotes them; warn/crit findings still
drift. Selftests invoke fresh CLI processes rather than suppressing errexit
around a function call (`corpus/lessons/round-1.md`, integration errata).

**Claims mode (round 2).** `verify-claims <claims-file>` reads one JSON claim per
line — `{"id","source","span","expect"[, "marker"]}`; blank lines, `#` comments
and a `{"marker_default":…}` line are allowed — and matches each `span` as a
byte-exact occurrence of its cited local source delimited at token boundaries
(a substring glued into a longer word is a miss with the line-aware
`nearest_line` report). Per claim it prints
`CLAIM id=… expected=… observed=… source=… at=… verdict=…` (`observed`
supported|contradicted|unsupported|unproven|refused|invalid; `verdict`
match|mismatch|refused|invalid), then `VERDICT_BEARING_CLAIMS=N/M` and the
verdict summary. `contradicted` is structural, never semantic: the named
`marker` must co-occur inside the span's source lines or the claim reads
`unproven`; a marker on any other `expect` is a record violation. CLEAN iff
every observed status equals its pre-registered `expect` (N=M).

Measured at the round-2 working gate (content sha256 `03a332445585…`): the
pre-registered `corpus/fixtures/claims-r2.jsonl` emits 17/17 and
`RESEARCH_GATE: CLEAN`, exit 0; a one-word span tamper emits
`CLAIM_SPAN_NOT_FOUND` with `VERDICT_BEARING_CLAIMS=16/17` and DRIFT, exit 1; an
URL source and a path outside the corpus read `refused` with crit findings and
no fetch attempt. `--selftest` is `PASS (30 cases)` with the round-1 20 case
lines byte-identical, and `verify` stdout on the three pinned archives is
byte-identical to the round-1 run.

**Token boundaries (round 4).** The span and quote checks above and below share
one matching rule: a byte-exact occurrence counts only at token boundaries, so
a truncated or padded fragment glued into a longer word is a miss with the
line-aware report. A boundary is a file or line edge, ASCII whitespace
(space tab CR LF VT FF) or ASCII punctuation — `_` included; a `-` or `'`
joining two word characters is not a boundary, so a word-internal joiner keeps
its word as one token; bytes outside those ASCII classes fail closed, so an
occurrence whose edge character is `—`, `’` or any other non-ASCII byte is a
miss. Only the outer edges are checked, so a multi-line span may cut
mid-token inside. Matching stays byte-exact and case-sensitive, and the hit
reported is the first delimited occurrence.

The rule errs toward missing, not toward accepting: probes outside the
selftest (mid-token fragments beside `—` or curly quotes, a possessive
`workers' queue`) all miss, and no probe shape was found to resolve a
mid-token fragment, while the selftest's boundary-pass cases keep complete
spans — punctuation-adjacent, line-edge, multi-line — resolving.

Measured at the round-4 gate revision (content sha256 `6b83705b02fe…`), same
rule in both modes: `--selftest` is `PASS (44 cases)` with cases 1–40
byte-identical to the round-3 run and cases 41–44 adding the boundary classes
(claims: punctuation, non-word-internal hyphen, line edge, multi-line span all
resolve; mid-token truncation, padded compound and possessive join all miss —
`claims-boundary-pass`/`claims-boundary-fail`; chain: the same via quote
anchors — `chain-pass-boundary`/`chain-fail-boundary`). The pre-registered
fixtures hold unchanged: `claims-r2.jsonl` 17/17 CLEAN and `chain-r3.md`
`RESOLVED_HOPS=17/22` CLEAN both exit 0 under `--root ..`; the broken controls
(`claims-fail-*`, `chain-r3-broken.md` → `RESOLVED_HOPS=1/2`) still DRIFT, and
the r1 archive observable stays 3/3 DRIFT with the intake CLEAN.

**Chain mode (round 3).** `verify-chain <record>` resolves the `## Chain` table:
every hop marked `resolved` must cite a source (an `## Sources` id or a local
path, same boundary as `verify-claims`) plus an anchor —
`anchor_kind`+`anchor` columns (`heading`|`quote`|`line`) or a `to` fragment
`path#kind:text` — and the anchor must exist in the target (heading text
equality, verbatim quote at token boundaries with a line-aware `at=`, whole
line with trailing whitespace trimmed). Per hop it prints
`CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…` (`observed`
verified|anchor-missing|refused|invalid|exempt), then `RESOLVED_HOPS=N/M` and
the verdict summary; `unresolved`/`blocked-no-fetch`/`rejected`/`labelled-dead`/
`not-applicable` hops stay exempt but counted. CLEAN iff every non-exempt hop
verified (N = M − exempt) and no finding drifts.

Measured at the settled round-3 gate (content sha256 `67daf85ecc49…`): the
pre-registered 22-hop fixture `corpus/fixtures/chain-r3.md` (17 resolved anchors
in the three pinned archives, 2 `blocked-no-fetch`, 3 `unresolved`) emits
`RESOLVED_HOPS=17/22` and
`RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)`,
exit 0; the tampered control `corpus/fixtures/chain-r3-broken.md` — a hop
claiming `resolved` while citing `人為 — jin’i-ryū`, a string the target never
carries — emits `CHAIN_ANCHOR_NOT_FOUND` with `RESOLVED_HOPS=1/2` and DRIFT,
exit 1, while the same record still passes round-1 `verify` CLEAN, exit 0.
`--selftest` is `PASS (40 cases)` with cases 1–30 byte-identical to the
round-2 run; the `verify-claims` fixture output and `verify` stdout on the
three pinned archives are byte-identical to their round-2 counterparts except
the `ts=` field; a strace run observes zero network syscalls.

**Sweeps mode (round 5).** `verify-sweeps <record>` makes kept rejections and
negative sweeps verdict-bearing. Every `## Rejections` row needs a non-empty
`reason` and a non-empty flip-condition (a `flip`/`flip_condition` column, or
any column name containing flip/falsif/reversal); a row missing either emits
`SWEEP_REJECTION_INCOMPLETE` and reads `observed=incomplete`. Every negative
sweep — a `## Sweeps` row, or a `Negatives` row carrying a `where`/`looked_at`
column or a sweep cell — must name where it looked: a local path set (a
comma/semicolon list, or the path/URL/`S…` words extracted from a
command-shaped value) is re-measured under the root, and any path the glob set
selects is `SWEEP_CLAIM_FALSE` naming it (zero selections verify); URLs,
`external:`/`web:`/`session:` names and declared source ids stay exempt but
counted; an out-of-root or `..` path is refused unopened
(`SWEEP_LOCATION_OUT_OF_CORPUS`), an undeclared source id is
`SWEEP_LOCATION_UNRESOLVED`, and a sweep naming nowhere is
`SWEEP_LOCATION_ABSENT`; a row marked
`unresolved`/`blocked-no-fetch`/`labelled-dead`/`not-applicable` is exempt.
Per item it prints `SWEEP id=… where=… looked=… hits=… at=… observed=…
verdict=…` and `REJECTION id=… ref=… reason=present|absent flip=present|absent
observed=complete|incomplete verdict=…`, then
`VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L`; CLEAN iff every sweep verified or
exempt and every rejection complete (N + exempt = M, K = L) and no finding
drifts.

Measured at the round-5 working gate (content sha256 `55adb92d…`): the
pre-registered `corpus/fixtures/sweeps-r5.md` (3 complete rejections; W1 a
local path set re-measured empty, W2 non-local exempt) emits
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` and
`RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 …)`, exit 0; the broken
control `corpus/fixtures/sweeps-r5-broken.md` (R1 without a flip-condition,
W1 naming a file that exists) emits `SWEEP_REJECTION_INCOMPLETE` and
`SWEEP_CLAIM_FALSE` with `VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1` and DRIFT,
exit 1 — while both still pass round-1 `verify` CLEAN, exit 0 (the pre-move
hole). `--selftest` is `PASS (54 cases)` with the first 44 lines
byte-identical to the round-4 run; cases 45–54 add the sweeps classes
(positive, planted hit, incomplete rejection, unnamed location, out-of-corpus
path, undeclared id, counting, cell-command form, two setup exits). The
pre-registered `claims-r2.jsonl` 17/17 and `chain-r3.md` 17/22 runs stay
byte-identical to their round-4 outputs, the broken chain control still
DRIFTs at 1/2, and a strace of the positive run observes zero network
syscalls.

**Composition mode (round 6).** `verify-all <record> [--claims PATH] [--json
PATH] --root PATH` runs every applicable mode over one input as a fresh CLI
call and composes ONE verdict. `structure` runs for a Markdown record;
`claims` runs when a claims surface is bound — `--claims PATH`, a `## Meta`
row named `claims`/`claims_file`/`claims-file`/`claimset`, or the input itself
when it is a claims JSONL (no `##` section line, at least one JSON-object
line); `chain` runs when the record declares `## Chain`; `sweeps` runs when it
declares `## Sweeps`, `## Negatives` or `## Rejections`. Per section it prints
`SECTION <name> state=run verdict=… findings=N drift=N [tally=…]` — the
`tally` is that section's own solo summary line
(`VERDICT_BEARING_CLAIMS` / `RESOLVED_HOPS` /
`VERIFIED_SWEEPS=… REJECTIONS_OK=…`) — then echoes that section's `FINDING`
lines; an absent section prints `SECTION <name> state=absent` and never drifts
by itself. Then `VERIFY_ALL sections=4 run=N absent=N drift-sections=N
findings=N drift=N` and one composed `RESEARCH_GATE: CLEAN|DRIFT`; the verdict
is DRIFT iff any run section drifts, exit 0/1/2 as elsewhere. A section whose
fresh call cannot be evaluated (rc ∉ {0,1}, or no single verdict line) is
`VERIFY_ALL_SECTION_UNAVAILABLE` (crit — it drifts); a declared claims surface
that does not resolve under the corpus boundary is
`VERIFY_ALL_CLAIMS_UNRESOLVED` (warn — it drifts that section only). `--json
PATH` appends (`>>`, never rewrites) one JSON line —
`{"schema":"chousa-verify-all/v1","ts":…,"record":…,"record_sha256":…,"gate_sha256":…,"sections":[…],"verdict":…,"sections_run":…,"sections_absent":…,"drift_sections":…}`
— so a record's verification state (record and gate SHA-256, UTC, per-section
tallies, composed verdict) becomes durable instead of eyeballed.
`--claims`/`--json` are refused (exit 2) outside `verify-all`, and companion
files are bound by declaration only: no filename is guessed.

Measured at the round-6 gate (content sha256 `0c3d51ed…`): `full-r6.md`
composes `CLEAN run=4 absent=0` with per-section tallies equal to the solo
modes (`claims 3/3`, `hops 3/3`, `sweeps 1/2 rejections 2/2`); the twin
`full-r6-broken.md` composes `DRIFT drift-sections=2 findings=2`, exit 1,
naming exactly `chain` (`CHAIN_ANCHOR_NOT_FOUND`, `RESOLVED_HOPS=2/3`) and
`sweeps` (`SWEEP_REJECTION_INCOMPLETE`, `REJECTIONS_OK=1/2`) while `structure`
and `claims` stay CLEAN; `full-r6-absent.md` composes `CLEAN run=3 absent=1`
(`claims state=absent`) and `claims-r2.jsonl` passed as the input composes
`CLEAN run=1 absent=3`. `--json` appended well-formed lines whose `gate_sha256` is
the gate's own sha256 and whose first line stayed byte-stable under a second
append; setup refusals exit 2 without touching the manifest (`/dev/null` is
refused as a manifest path). `--selftest` is `PASS (64 cases)` with cases 1–54
byte-identical to the round-5 run; cases 55–64 cover verify-all (composed
positive with a claims binding and without one, a tampered claims run, a
structure-dirty run, a claims-JSONL input, two manifest appends, the Meta-bound
claims row, an unresolvable declaration, a setup exit). The solo modes' fixture
outputs stay byte-identical modulo `ts=`, and a strace of the composed positive
run observes zero network syscalls.

**Integrity mode (round 7).** `verify-integrity <record>` resolves every
cross-section reference token against the rows that declare it. Declared ids:
source ids from `## Sources`, claim ids from `## Claims` and `## Negatives`,
sweep ids from `## Sweeps`; reference cells: chain `from`/`to`/`claim` (a `to`
fragment after `#` is stripped), claims `sweep`/`source`/`src`/`ref`/`cite`/
`pointer`, negatives `sweep`/`where`, sweeps `claim_id`/`where`, rejections
`ref`/`reference`. Each whitespace/comma/semicolon-separated token of a
reference cell is classified once: a token equal to a declared id resolves
(`kind=source|claim|sweep`); a token in an undeclared id shape (`S<digit>…`,
`C|N<digit>…`, `SW<digit>…`) is `REF_UNRESOLVED` severity=warn (drift); a
non-local naming (URLs; `local://`-style and `external:`/`web:`/`live:`/`chat:`/
`session:` names) is exempt (`reason=non-local`); local paths/globs, prose and
sentinels are not integrity tokens and are not counted. Exempt-but-counted
keeps the hop/sweep idiom: the reference tokens of an exempt-status row are
counted exempt rather than required to resolve — chain rows with status
`unresolved`/`blocked-no-fetch`/`rejected`/`labelled-dead`/`not-applicable`,
sweeps/negatives rows with
`unresolved`/`blocked-no-fetch`/`labelled-dead`/`not-applicable`. Per reference it prints
`REF kind=… id=… section=… row=… cell=… observed=resolved|unresolved|exempt
verdict=match|mismatch|exempt [status=…|reason=…]`, then
`INTEGRITY refs=N resolved=M unresolved=K` (N counts every extracted token
including exempts, exempt = N−M−K); CLEAN iff K=0 and no finding drifts. In
`verify-all` the `integrity` section runs whenever at least one other section
runs — its tally is the solo mode's `INTEGRITY` summary, and a claims-JSONL
input composes `run=2 absent=3` with `refs=0` — and its `REF_UNRESOLVED`
findings drift the composition like any other section; the `--json` manifest
keeps schema `chousa-verify-all/v1` with the integrity entry in `sections`.

Measured at the round-7 gate (content sha256 `3ba718bf…`): the
pre-registered `corpus/fixtures/integrity-r7.md` composes CLEAN `run=5` with
`INTEGRITY refs=16 resolved=15 unresolved=0`; its twin `integrity-r7-broken.md`
— two single-cell dangles (`S9` in chain row 4's `from`, `C9` in sweeps row
SW3's `claim_id`) that every r1–r6 mode passes — composes DRIFT
`drift-sections=1 findings=2` naming exactly the `integrity` section and the
two ids, while structure/claims/chain/sweeps stay CLEAN with the positive's
tallies (`RESOLVED_HOPS=4/4`, `VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2`,
`VERDICT_BEARING_CLAIMS=3/3`). `--selftest` is `PASS (74 cases)` with cases
1–64 byte-identical to the round-6 run; cases 65–74 are the integrity family
(positive; dangling claim, source, chain-claim and sweep classes;
exempt-but-counted; counting; two setup exits) plus one composed case where a
dangling sweep binding alone drifts a verdict all four r6 sections call CLEAN.
The r6 trio regresses unchanged (`full-r6.md` CLEAN `run=5`,
`full-r6-broken.md` DRIFT `drift-sections=2`, `full-r6-absent.md` CLEAN
`run=4 absent=1`); the solo pins hold (`VERDICT_BEARING_CLAIMS=17/17`,
`RESOLVED_HOPS=17/22`, `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`); a strace of
the composed DRIFT run observes zero network syscalls.

**Baseline mode (round 8).** `--pin PATH` runs the gate's canonical reference
invocation — `verify-all record.md --claims claims.jsonl --json manifest.jsonl
--root .` with cwd set to a fresh temp fixture the gate writes itself (never
committed; every printed path is relative, so the capture is byte-stable
wherever the gate is run) — normalizes that capture and writes it as a
baseline text file (`chousa-gate drift baseline v1`), printing
`GATE_PIN: ok path=… gate_sha256=…`. `--drift PATH` re-runs the same
invocation, re-normalizes with the **current** rules and byte-compares: equal
prints `GATE_DRIFT: none` exit 0, differ prints `GATE_DRIFT: <changed tokens>`
exit 1, and a baseline that is missing, unreadable, malformed (no magic line,
no canonical marker, no volatile contract, empty block) — or a capture that
fails — prints one message on stderr, exit 2. The volatile contract travels in
every baseline header (`# volatile_fields=ts gate_sha256`, values masked to
`<V>`): `ts` is masked shape-scoped (only `ts=<YYYY-MM-DDTHH:MM:SSZ>` and
`"ts":"…"` match, so a malformed timestamp keeps its bytes and surfaces as
drift) and `gate_sha256` is informational, so the pin compares behavior rather
than revision; everything else, `record_sha256` included, is compared
unmasked, and rewriting the declared list is itself drift. Drift tokens are
`LC_ALL=C` sorted and space-joined: `<key>` a changed non-volatile value,
`-<key>`/`+<key>` a field a changed line dropped/added, `-<id>`/`+<id>` a line
removed/added (`GATE` `MANIFEST` `VERIFY_ALL` `VERDICT` `SECTION:<name>`
`FINDING:<id>` `LINE`), `output-order` a pure reorder, `volatile_fields` a
changed volatile contract.

Measured at the round-8 gate (content sha256 `46f5ddbf…`): `--pin` wrote a
2988-byte / 19-line baseline and exited 0 although its own fixture rolls
`RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1
drift=1)` — pinning a DRIFT run is still a pin; `--drift` against it read
`GATE_DRIFT: none` exit 0, immediately and again after 35 s of wall clock (the
mask absorbs the invocation's only live input); a one-token baseline edit read
`GATE_DRIFT: state` exit 1, a rewritten volatile list `GATE_DRIFT:
volatile_fields` exit 1, a missing baseline exit 2, an empty file `malformed
(magic line absent)` exit 2, and `--pin … --root .` `--pin/--drift take only a
baseline path` exit 2. The falsifying pair at gate level: a copy whose
`integrity` section is silently skipped reads `GATE_DRIFT:
-FINDING:REF_UNRESOLVED -drift -findings -refs -resolved -tally -unresolved
-verdict absent drift drift-sections drift_sections exempt findings native run
sections_absent sections_run state tallies verdict`, exit 1; a copy whose
output mode word changed reads `GATE_DRIFT: mode`, exit 1 — and both mutants
also drift against the committed lane baseline, so the committed artifact
detects rather than merely prints `none`. `--selftest` is
`PASS (85 cases)` exit 0 with cases 1–74 byte-identical to the round-7 run —
compared against a `git clone` of the committed r7 gate run from its own root,
because running the gate script from outside the lane mis-fails three
out-of-corpus/chain-counting cases — and cases 75–85 are the pin/drift family
(pin; clean drift; drift after live churn; one-field mutant; missing;
malformed; volatile-list mismatch; four setup exits). A strace of the drift
run observes zero network syscalls.

**Archive-scale controls and the limit ledger (round 10).** The gate stayed
unchanged at sha256 `46f5ddbf…` (`GATE_DRIFT: none` against the committed r8
baseline; the working-tree gate equals its HEAD blob).
`corpus/fixtures/archives-r9/controls/` holds six negative controls — one
broken byte-copy of an archive record per defect class (span-not-found,
anchor-missing, rejection-missing-flip, false-sweep, dangling-ref,
structure-break), the defect isolated to one section — and each DRIFTs
`verify-all` with exactly one drifting section and one finding naming its
class (ids and tallies in the gate row above), exit 1 with
`drift-sections=1 findings=1`, while the A/B/C records stay CLEAN in the same
window. Expected verdicts, per-control sha256 pins and the re-run recipe are
pre-registered in the controls README. The archive records' six exempt items —
one `blocked-no-fetch` hop and one exempt `from` token per record — are
audited against the archive bytes (6/6 justified, 0 findings, under the
unchanged exemption rule), and every limit named across rounds 2–9 stands
dispositioned in `corpus/knowledge/hardening-r10.md` (that set plus the
r1-origin debts and the rows this round surfaced; current counts: the
limits paragraph below).

**Limits.** `verify` CLEAN is declared record structure and file-pointer
identity only — that path never opens the source a pointer resolves to.
`verify-claims` does open cited sources, but only canonicalized local files
under `CHOUSA_ROOT` or the lane root; URLs and session/denylist paths are
refused before any read, and no path ever fetches. It judges span identity, not
meaning: a matching span does not make the claim true, and `contradicted` is a
literal-marker check, not source semantics or domain truth. `verify-chain`
opens only the same canonicalized local files and judges anchor existence in
the cited target: a `verified` hop proves the anchor bytes occur there, not
that the hop's reading or the target's own assertions are true; exempt
(`unresolved`/`blocked-no-fetch`/…) hops are counted, never verified. It too is
text-only and reads whole files. Both match paths judge byte identity at token
boundaries, not meaning: a delimited span still proves nothing about the
claim's truth, and a span that stops at a legitimate token edge while omitting
most of a sentence still passes. `verify-sweeps` re-measures only what a
sweep names: a local path/glob set is re-checked for emptiness (a path it
selects is the hit), so its CLEAN proves the named set selects nothing on
disk — not that the claimed pattern is absent from unnamed content, not that
the flip-condition is meaningful (a placeholder string passes), not that a
non-local sweep was ever run, and not that the named set is the right set.
`verify-all` composes exactly the section verdicts above and adds no assertion
of its own: each run section executes the same mode the solo entry does, an
absent section is reported, never verified, and how omission should compose
(including what a Chain-less record can do) is a named open limit, not a
settled rule. The manifest records a state at a revision: it appends, never
rewrites or compares revisions, so a line is evidence a run happened, not
proof the record bytes stayed unchanged after it.
`verify-integrity` judges declaration, not truth: a reference resolves when
the named row exists, so a binding to a wrong-but-declared row passes, and
only the three id shapes above are tokens — an undeclared id in any other
shape (measured: `Z9`, `X9`), a reference carried in prose, or one in a column
outside the extraction list is invisible; exempt-status rows' tokens and
non-local namings are counted, never resolved.
`--pin`/`--drift` compare exactly one canonical invocation's normalized output
and nothing else: the two masked fields (`ts`, `gate_sha256`) are declared
blind spots, so a change that moves only a masked value — a comment-only gate
edit, for instance — reads `none` by design, and a behavior change the
canonical fixture never exercises stays invisible; the comparison is
behavioral, not revision-bound, so a red result may be baseline aging (a
legitimate contract or fixture edit) rather than a regression, and re-pinning
is a recorded act with a reason, never a way to turn red green; the fixture's
own bytes are compared too — its sha256 appears unmasked in the capture — so
an edited fixture drifts rather than silently re-baselining.
The documented
the refused provinces above are enforced by scope finding IDs since round 12 (declared-scope screen, `SCOPE_*`; `corpus/knowledge/scope-refusal-r12.md`); the original
landing requirement is named debt in `LOG.md`'s interactive round-1 entry. No
non-author corpus spot-check or promotion is implied by a passing selftest.

The limits named across rounds 2–9 are collected with one disposition each in
`corpus/knowledge/hardening-r10.md`; a disposition is a record, not a gate
change. The disposition counts and the round-11 audit-queue size are owned by
that file's latest counts line (round-25 erratum: 71 rows, re-derive with
`python3 corpus/evidence/round25-ledger-recount.py` from the lane root) and
are not restated here. The A-r9 C3 pointer finding (`A-r9.md:50` cited `A:76`
for a span at `A:86`; ledger row 56) was closed at round 12 by correcting the
record (`hardening-r10.md` E1; receipt
`corpus/evidence/scope-r12-20261019T115519Z-A-fix.log`); the class stays
uncovered — no mode pairs a row's `path:line` with its span's occurrence line.

## Round26 metadata options and resource qualification

The existing `verify-metadata` gate is extended, not replaced:

```sh
# cwd: this lane root. All reads remain local; no entry text is executed.
bash tools/research-gate.sh verify-metadata corpus/knowledge --root . \
  --as-of 2026-10-21 --registry corpus/SOURCES.md
```

Both flags are optional and metadata-only; missing/invalid option arguments
or a refused/headerless registry are setup/usage exit2. Without either flag,
the round25 output contract remains in force. With both flags, both sets of
observations/findings apply to one verdict; neither option is ignored.
The existing gate registry's code map, zero-write verification scope, owner
and shared `--selftest` command remain unchanged. Round26's exact suite tally
and landed executable are owned by `SCORECARD.md`'s Round26 measurement.

| Option / observation | Interpretation and limit | Source |
|---|---|---|
| `--as-of YYYY-MM-DD` | Add `due=` and `freshness=` before the entry verdict. Calendar-valid explicit dates or verified-at plus decimal Nd define deadlines; equality is current, strictly later is overdue. `on-release` is event; unavailable/out-of-range computation is unknown. | `corpus/knowledge/recheck-due-r26.md`; frozen spec `corpus/evidence/round26-claims.md` C2 |
| `META_RECHECK_OVERDUE` warn | The declared assessment deadline passed. It does not establish that the entry is false, nor that a current/event entry was actually rechecked. | same note, source-grounded distinction and limits |
| `--registry FILE` | Check standalone S+three-or-more-digit IDs against the first table with id/status/used-by columns; first duplicate ID wins. Require a mined row whose comma-separated used-by token names the exact rooted entry path (leading `./` normalized). | `corpus/knowledge/registry-link-r26.md`; C3 contract correction |
| `META_SOURCE_ROW_MISSING`, `META_SOURCE_NOT_MINED`, `META_SOURCE_USEDBY_MISSING`, `META_VERIFIED_AT_BARE` warn | Local declaration errors; the last means a leading dated verified-at value says nothing nonblank about what was checked. `META_SOURCE_NO_ROW_ID` is legacy-compatible info, promoted only in strict mode. | registry-link note, disposition table |

Apply the prospective criterion6 rollup only to r24+ entries; a manual scan
of legacy notes can emit findings without retroactively declaring their
original admission invalid. This screen is not complete criterion6:
URL/anchor sufficiency, source tier/scope, actual opening, citation support
and truth still require QUALITY6–8 and a reviewer.

The metadata header now traverses the fd-bound bounded snapshot directly,
without a whole-snapshot per-line array. Full-file NUL/size/refusal checks
precede header cutoff and must not be replaced by a prefix-only read.
The four-shape RSS result is not a universal memory/time budget: headerless
and very long-line/continuation inputs retain time risks, and other gate
readers are not repaired. See `corpus/knowledge/reader-allocation-r26.md`
and QUALITY18. The operability scalar remains the original r1 construct,
not a resource-safety or readiness score.

### Round26 recovery safety/status correction — 2026-10-21

The options above describe the intended policy, **not a verified current
capability**. At production revision
`0e9784bd52eca456b24d0bc40921480a47f91a2b`, the cumulative selftest is
`FAIL (3/187 cases)`, exit1; do not read the old passing tally or a counting
probe's exit0 as current PASS. C2's new mode has input-domain failures; C3's
new mode has table/tokenization/refusal defects. Their knowledge notes carry
withdrawal addenda and exact falsifier pointers. They are not reliable
automated admission/freshness decisions; manual QUALITY checks remain needed.

C1's four plain-reader shapes improve4/4→0/4 amplified, but the round is
**not admitted**, and the new registry parser separately amplifies allocation.
Any earlier “bounded registry” wording means an input-byte snapshot cap,
not a resource budget. SCORECARD's Round26 recovery section owns the observed
counts, no-harm failure and remaining verification gaps. No new capability
or SHONEN promotion is claimed.

### Round27 repair/status correction — 2026-10-21

Round26's rejected verdict remains historical, not retrospectively admitted.
Round27 repairs the usage-record predicate, ASCII date parsing, nonrecursive
leading-zero cadence normalization, registry header reset/width and S-id
occurrence scanning. Full selftest at checkpoint cb895a2 is
`PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187
identities and legacy161 output are retained. SCORECARD's Round27 section
owns final revisions and receipts; local synthetic passes are not an
outside closure or general source-verification guarantee.

**C3 remains partially falsified.** The filesystem predicate still checks a
citation-normalized prefix beside the complete path. That over-refuses some
benign colon/backtick filenames; the new canonical claims check extends the
over-refusal to a benign alias. The frozen requirement to use complete
filesystem paths, not citation prefixes, is not met. Original negative
controls were retained rather than weakened. See
`.ufo/waves/round-27/residual/ResC3Clause.md`, the round27 lesson and L0.
No registry/knowledge capability is newly admitted; manual QUALITY checks
remain required. The full selftest also retains inherited locale dependence:
exported `LC_ALL=C` breaks ten claims/verify-all cases on both round27
checkpoints; use the host UTF-8 locale for the recorded selftest comparison.

Final round27 production revision4f48419425f5165a8f950e1db4c0a781cf845d40
also uses a single shared escaped-cell split (not just an adjusted width)
and separately checks both ASCII scanner stages. `META_SOURCE_SCAN_FAILED`
is a crit finding and yields DRIFT/exit1, never an informational no-S-id
substitute for a dependency failure. Final immutable receipts are
`.ufo/waves/round-27/final/`; full selftest215 and controls58+32 pass there.
The inherited requirement for at least three delimiter dashes and raw
versus rendered Markdown cell-text limitations remain explicit; this is
not a complete GFM parser.

### Round28 DERIVED honest-negative status — no policy change

Full C1, canonical claim-source ancestor over-refusal plus actual complete
denied-path attribution and its original holds, is **not achieved /
unprovable**. Parent did not approve the proposed default/nested-root
relaxation; denylist not waived. No implementation or new measurement
was authorised, and no smaller passing clause replaces the target.

Production/original controls and the prior metric/ordinals remain held.
The original R27 C3 clause/current red is not reversed. No new scalar,
capability, Core graduation, promotion or admission is claimed.
`corpus/evidence/round28-safe/claims.md` and the round28 lesson record the
negative scope. S045 is historical/rejected diagnosis, not an instruction
to exempt/select roots. Raw report/tool bodies, the proposed oracle and
the unexecuted/unapproved ruler remain private, not live teaching.
Only separately hashed DERIVED metadata/summaries are proposed for
publication; custody/exclusions are in `corpus/evidence/round28-safe/provenance.json`.
Seat spending is not a read-only, source-behaviour or safety certificate.
Outside closure and later census/report/continuation remain Parent-owned.
