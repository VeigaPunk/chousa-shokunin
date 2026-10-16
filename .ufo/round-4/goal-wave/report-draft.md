# chousa — round 4: token-boundary hardening (calibration move)

<!-- SCRIBE DRAFT for parent integration. Measured values are from the settled
     gate revision sha256
     6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
     (4 identical 30 s samples before the battery, sha re-checked around it;
     an earlier mid-write sample is NOT a result — see Defects 1) and lane HEAD
     09153d19871158380f64b6f58a14b6912aab676f, whose gate is the round-3
     revision 67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084.
     [PARENT] marks fields only the integrating parent may bind (commit hashes,
     acceptance, wave report count, final scorecard call). Scribe scratch:
     /tmp/chousa-scribe-r4/ (declared ephemeral, cleaned at end of run; every
     value cited here is reproduced verbatim inline). -->

## Work performed

- Round 4 ran as the operator's **in-session direct dispatch** of a 32-seat
  flash wave (same routing as rounds 2–3: no fleet-rendered wave, no
  role-alias overlay, **no Sighting step**; receipt identity untouched — see
  Debts). Starting lane HEAD `09153d1`; round-4 artifacts were uncommitted at
  draft time ([PARENT] commit). Wave seat reports: `[PARENT: N/N reports]`.
- Selected axis: **calibration** — matching semantics are hardened so a
  passing verdict tracks real citation fidelity. [PARENT: confirm the axis
  label; the dispatch text read "one move, calibration of matching semantics".]
- Declared move: **token-boundary hardening** — both `verify-claims` span
  matching and `verify-chain` quote-anchor matching accept a match only when
  both outer edges of the match sit at a token boundary (file/line edge, ASCII
  whitespace, ASCII punctuation; a word-internal hyphen/apostrophe is not a
  boundary), so truncated/padded/glued citation variants fail with the
  existing line-aware reports while legitimate spans — including ones followed
  by punctuation — still pass.
- Landed impl (`tools/research-gate.sh`, uncommitted working tree): header
  rule `:68-85`; usage text `:143-148`; shared helpers
  `:765-831` — `TOK_WS`/`TOK_PUNCT` `:772-773`, `tok_word_char` `:775-782`,
  `tok_left_ok` `:784-796`, `tok_right_ok` `:798-810`, `tok_span_at`
  `:812-831` (iterates occurrences, skips glued ones, reports the first
  boundary-delimited hit with line numbers); claims call site `:907`; chain
  quote branch call site `:1060-1061` (`heading`/`line` kinds unchanged).
  One helper, two call sites — the boundary rule is shared, not duplicated.
- Selftest grew 40 → **44 cases** (cases 41–44: `claims-boundary-pass`,
  `claims-boundary-fail`, `chain-pass-boundary`, `chain-fail-boundary`); the
  round-1–3 40 case lines are byte-identical. The claims pair and the chain
  pair run the **same fixture bytes** (`lib/boundary.md`) through both modes,
  so the delimited passes (punctuation edge, non-word-internal hyphen at line
  end, line edge, multi-line span) and the glued misses (mid-token
  truncation, padded extra word into a hyphenated compound, possessive
  apostrophe) are in-selftest evidence that one rule governs both modes.
- This scribe independently measured the before→after pair on real corpus
  text (all runs fresh-process from the lane cwd, read-only local opens) and
  built a cross-mode identity matrix with identical bytes through both modes
  (see below).
- Other seats' artifacts landed after the after-state battery: note
  `corpus/knowledge/anchor-boundaries-r4.md` (sha256 `668c1d1f…`) and lesson
  `corpus/lessons/2026-10-15-anchor-token-boundaries.md` (sha256 `5bd90e21…`).
  Their pins and results were re-checked against this seat's own runs and
  agree: same gate sha, selftest PASS (44 cases), claims 17/17, chain 17/22,
  broken control 1/2 DRIFT, r1 archives byte-identical modulo `ts=`, and the
  same claims before→after pair (5/5 CLEAN → 2/5 DRIFT); their chain attack
  record uses 8 hops (8/8 → 5/8) where this seat's uses 4 (4/4 → 2/4), same
  pattern, different probe set. Still unlanded at draft time: an attack-class
  fixture + contract README, `corpus/evidence/*r4*` receipts, SKILL.md and
  `corpus/README.md` round-4 rows.

## Landed changes

[PARENT] Work HEAD when this report is integrated: `[PARENT: commit hash]`.
Lane commits integrate under identity `chousa-shokunin <chousa@shokunin.local>`.

| Commit | Landed work | LOG connection |
|---|---|---|
| `[PARENT: commit hash]` | `tools/research-gate.sh`: token-boundary helpers + both call sites + header rule + 4 selftest cases (40 → 44); `corpus/knowledge/anchor-boundaries-r4.md` (`668c1d1f…`); `corpus/lessons/2026-10-15-anchor-token-boundaries.md` (`5bd90e21…`); [PARENT: plus whatever of fixture/README/receipts/SKILL/README-rows landed by integration time] | `LOG.md:[PARENT]` |

## Before → after measurements

**One axis move: calibration — token-boundary matching semantics.**
Falsifiable claim (as dispatched): before, a citation span that is a truncated
or padded variant of real source text passes verification; after, both
`verify-claims` spans and `verify-chain` quote anchors match only at token
boundaries, so truncation/padding/glue games fail with the line-aware reports
while legitimate spans (including those followed by punctuation) still pass;
all round-1–3 selftest cases and fixture CLEAN results hold unchanged; the
boundary rule is identical across both modes; the selftest adds
truncation/padding/punctuation/line-edge cases.

**Before** (round-3 revision, sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`, still the
lane gate at that time; fresh-process CLI runs by this seat):

Cross-mode attack class — **truncation and glue pass today**. Claims probes
(`/tmp/chousa-scribe-r4/before/attack-claims.jsonl`), three attack variants of
line 86 of `research/deep-research-2026-09-28/A-shokunin-tradition.md` plus two
legitimate controls, all `expect=supported`:

```text
$ bash tools/research-gate.sh verify-claims /tmp/chousa-scribe-r4/before/attack-claims.jsonl --root ..
CLAIM id=X1 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
CLAIM id=X2 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
CLAIM id=X3 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
CLAIM id=X4 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
CLAIM id=X5 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
VERDICT_BEARING_CLAIMS=5/5
RESEARCH_GATE: CLEAN (claims=5 supported=5 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0
```

X1 `apprenticeship is an economic and social institu` (cut mid-word),
X2 `pprenticeship is an economic and social institution` (glued left mid-word),
X3 `hey show that apprenticeship is an economic and social institution a`
(glued both edges) — all pass. X4 `common final examination` (followed by `.`)
and X5 `These examples matter because they show that apprenticeship` (line
start) are the legitimate controls the after-state must keep passing.

Chain probes (`/tmp/chousa-scribe-r4/before/attack-chain.md`), same revision:

```text
$ bash tools/research-gate.sh verify-chain /tmp/chousa-scribe-r4/before/attack-chain.md --root ..
CHAIN hop=1 … anchor=quote:"customary apprenticeship periods of approximate" at=line:80 verdict=match
CHAIN hop=2 … anchor=quote:"pproximately seven years for carvers" at=line:80 verdict=match
CHAIN hop=3 … anchor=quote:"common final examination" at=line:86 verdict=match
CHAIN hop=4 … anchor=quote:"These examples matter because they show that apprenticeship" at=line:86 verdict=match
RESOLVED_HOPS=4/4
RESEARCH_GATE: CLEAN (hops=4 verified=4 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
exit=0
```

Hops 1–2 are the truncated/glued attacks (both resolve); hops 3–4 are the
legitimate controls. The round-3 note recorded the same class live: a
one-byte-truncated anchor (`…kiwami semantic`) closed CLEAN
(`corpus/knowledge/chain-resolution-r3.md`, "Anchor semantics"). This seat
reproduced that exact case at the before revision
(`/tmp/chousa-scribe-r4/before/kiwami-chain.md`): hop 1 (`…kiwami semantic`)
`verified at=line:35`, hop 2 (real bytes `…kiwami semantics`) `verified`,
`RESOLVED_HOPS=2/2` CLEAN, exit 0.

**Before-state regression baselines** at the same revision (re-measured by
this seat; this is what "hold unchanged" is checked against):

```text
$ bash tools/research-gate.sh --selftest                     → PASS (40 cases), exit 0
$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
  → VERDICT_BEARING_CLAIMS=17/17 ; CLEAN ; exit 0
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
  → RESOLVED_HOPS=17/22 ; CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0) ; exit 0
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
  → RESOLVED_HOPS=1/2 ; DRIFT (hops=2 verified=1 anchor-missing=1) ; exit 1
$ CHOUSA_NOW_EPOCH=1760000000 bash tools/research-gate.sh verify ../research/deep-research-2026-09-28/<A|B|C>.md --root ..
  → each exit 1, exactly one RESEARCH_GATE: DRIFT line → VERDICT_BEARING_EXPORTS=3/3
$ bash tools/research-gate.sh verify corpus/knowledge/archived-export-intake.md --root ..
  → CLEAN (findings=0 drift=0 questions=1 sources=8 chains=8 claims=9 negatives=2 rejections=10 approvals=3) ; exit 0
$ grep -cE '\b(curl|wget|nc|ssh|scp|ftp|dig|nslookup|telnet)\b' tools/research-gate.sh  → 0
```

**Fixture edge-character pre-analysis** (gate-free, this seat's python over the
pinned fixtures): every existing match edge in both fixtures is a line edge,
whitespace, or ASCII punctuation — claims-r2 spans: before ∈ {`\n`,` `,`\t`},
after ∈ {`\n`,` `,`\t`,`;`}; chain-r3 quote anchors: before ∈ {`\n`,` `,`\t`|`(`},
after ∈ {`\n`,` `,`\t`,`;`,`)`}. No fixture span or anchor is adjacent to a
non-ASCII character at its match edge, so the documented ASCII boundary class
is sufficient for the r2/r3 regressions; the riskiest existing case is
chain-r3 hop 3 (parenthesis-bounded).

**After** (gate sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`; identical
across 4 × 30 s samples before the battery and re-checked after it; lane HEAD
`09153d1`; all runs below by this seat):

```text
$ bash tools/research-gate.sh --selftest
ok-case  41 claims-boundary-pass         exit=0
ok-case  42 claims-boundary-fail         exit=1
ok-case  43 chain-pass-boundary          exit=0
ok-case  44 chain-fail-boundary          exit=1
RESEARCH_GATE_SELFTEST: PASS (44 cases)
exit=0
# first 40 ok-case lines cmp-verified byte-identical to the before capture
# (which is itself the round-3 receipt, selftest PASS 40)

$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
  → VERDICT_BEARING_CLAIMS=17/17 ; CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0) ; exit 0
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
  → RESOLVED_HOPS=17/22 ; CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0) ; exit 0
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
  → RESOLVED_HOPS=1/2 ; DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1) ; exit 1
$ CHOUSA_NOW_EPOCH=1760000000 … verify A/B/C → VERDICT_BEARING_EXPORTS=3/3, each exit 1, exactly one DRIFT line; intake CLEAN exit 0
```

All four regression outputs (selftest first-40 lines, both fixtures, the broken
control, the three archives, the intake record) are **byte-identical modulo the
`ts=` field** to the before-state captures — cmp-verified by this seat.

**After** — attack class now fails in both modes (same probe bytes as the
"before" run):

```text
$ bash tools/research-gate.sh verify-claims /tmp/chousa-scribe-r4/after/attack-claims.jsonl --root ..
CLAIM id=X1 expected=supported observed=unsupported source=…/A-shokunin-tradition.md at=- verdict=mismatch
CLAIM id=X2 expected=supported observed=unsupported source=…/A-shokunin-tradition.md at=- verdict=mismatch
CLAIM id=X3 expected=supported observed=unsupported source=…/A-shokunin-tradition.md at=- verdict=mismatch
CLAIM id=X4 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
CLAIM id=X5 expected=supported observed=supported source=…/A-shokunin-tradition.md at=line:86 verdict=match
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=X1 nearest_line=86 context=These examples matter because they show that apprenticeship is an economic and s
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=X2 nearest_line=86 context=…
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=X3 nearest_line=86 context=…
VERDICT_BEARING_CLAIMS=2/5
RESEARCH_GATE: DRIFT (claims=5 supported=2 contradicted=0 unsupported=3 mismatched=3 unproven=0 refused=0 invalid=0 findings=3 drift=3)
exit=1

$ bash tools/research-gate.sh verify-chain /tmp/chousa-scribe-r4/after/attack-chain.md --root ..
CHAIN hop=1 status=resolved observed=anchor-missing source=…/A-shokunin-tradition.md anchor=quote:"customary apprenticeship periods of approximate" at=- verdict=mismatch
CHAIN hop=2 status=resolved observed=anchor-missing source=…/A-shokunin-tradition.md anchor=quote:"pproximately seven years for carvers" at=- verdict=mismatch
CHAIN hop=3 status=resolved observed=verified source=…/A-shokunin-tradition.md anchor=quote:"common final examination" at=line:86 verdict=match
CHAIN hop=4 status=resolved observed=verified source=…/A-shokunin-tradition.md anchor=quote:"These examples matter because they show that apprenticeship" at=line:86 verdict=match
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=1 … nearest_line=80 context=Woodblock printing: Adachi’s own account gives customary apprenticeship period
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 … nearest_line=80 context=…
RESOLVED_HOPS=2/4
RESEARCH_GATE: DRIFT (hops=4 verified=2 exempt=0 anchor-missing=2 refused=0 invalid=0 findings=2 drift=2)
exit=1
```

Both attacks now fail with the existing line-aware reports
(`nearest_line`/`context`), both legitimate controls still pass, and the
verdict/exit contract is unchanged. The round-3 residual pair closes the same
way: `kiwami-chain.md` at the after revision → hop 1 (`…kiwami semantic`)
`anchor-missing` with `nearest_line=35`, hop 2 (real bytes) `verified`, 
`RESOLVED_HOPS=1/2`, DRIFT, exit 1 — the earlier CLEAN rested on substring
semantics and is now correctly re-judged.

**After — boundary probes** (`/tmp/chousa-scribe-r4/after/boundary-probes.jsonl`,
this seat's independent probes, not the wave's fixture; 9/9 CLEAN, exit 0):

```text
CLAIM id=H1 expected=unsupported observed=unsupported at=- verdict=match   # "ryu" from jin'i-ryu (word-internal hyphen)
CLAIM id=H2 expected=unsupported observed=unsupported at=- verdict=match   # "jin'i" ending on word-internal hyphen
CLAIM id=H3 expected=unsupported observed=unsupported at=- verdict=match   # "jin" before word-internal ASCII apostrophe
CLAIM id=H4 expected=unsupported observed=unsupported at=- verdict=match   # "AI" from multi-AI-agent (hyphens both sides)
CLAIM id=L1 expected=supported observed=supported at=line:86 verdict=match # followed by "."
CLAIM id=L2 expected=supported observed=supported at=line:86 verdict=match # line-start span
CLAIM id=L3 expected=supported observed=supported at=line:35 verdict=match # paren-bounded (= r3 fixture hop-3 anchor bytes)
CLAIM id=D1 expected=supported observed=supported at=line:35 verdict=match # "minarai/deshi" — ASCII "/" is a boundary
CLAIM id=D2 expected=supported observed=supported at=line:35 verdict=match # "deshi", glued first occurrence still resolves
```

`H1–H4` are the guarded attack classes (word-internal hyphen/apostrophe and
glue into a hyphenated compound), all refused; `L1–L3` are legitimate spans
that must keep passing, all resolved; `D1`/`D2` show two documented
consequences rather than defects: an occurrence delimited by **ASCII
punctuation** (`/`) is a boundary, and `tok_span_at` retries past a glued
occurrence to a later delimited one (`deshi` is found inside
`minarai/deshi/shokunin` because the slashes bound it).

**After — cross-mode identity matrix** (identical bytes run as a claims span and
as a chain quote anchor; this seat's probes):

| bytes | claims (`verify-claims`) | chain (`verify-chain`) |
|---|---|---|
| `apprenticeship is an economic and social institu` (mid-word truncation) | `observed=unsupported` `verdict=mismatch` | `observed=anchor-missing` `verdict=mismatch` |
| `hey show that … social institution a` (glued both edges) | `observed=unsupported` `verdict=mismatch` | `observed=anchor-missing` `verdict=mismatch` |
| `minarai/deshi` (ASCII punctuation delimiter) | `observed=supported` `at=line:35` `verdict=match` | `observed=verified` `at=line:35` `verdict=match` |
| `common final examination` (punctuation-followed) | `observed=supported` `at=line:86` `verdict=match` | `observed=verified` `at=line:86` `verdict=match` |
| `These examples matter because they show that apprenticeship` (line start) | `observed=supported` `at=line:86` `verdict=match` | `observed=verified` `at=line:86` `verdict=match` |
| `jin'i` (word-internal hyphen) | `observed=unsupported` `verdict=mismatch` | `observed=anchor-missing` `verdict=mismatch` |
| `ryu` (word-internal hyphen) | `observed=unsupported` `verdict=mismatch` | `observed=anchor-missing` `verdict=mismatch` |

Claims run `VERDICT_BEARING_CLAIMS=3/3` CLEAN exit 0; chain run
`RESOLVED_HOPS=1/3` DRIFT exit 1 — the same bytes pass or fail together, and
one shared helper (`tok_span_at`) serves both call sites.

## Defects found by the scribe seat

1. **Mid-write gate sample (environmental / process).** This seat's first
   after-state battery (2026-10-16T00:16:32Z, gate content then `371a6ce5…`)
   hit the file while a seat was still writing it: the chain-fixture run
   returned `tools/research-gate.sh: line 2097: syntax error near unexpected
   token `('` and exit 2, while the very next run in the same battery (a later
   revision) succeeded. Nothing in that sample is a result; the settled
   revision `6b83705b…` (4 × 30 s identical samples, re-checked around and
   after the battery) is what every after-state value above is measured at.
   The round-2 note has the precedent: runs taken while the file is being
   written are not results.
2. **Lane hygiene — probe scratch in the fixtures tree (transient; resolved in-wave).** During the wave, six untracked probe files appeared in `corpus/fixtures/`: `probe-src.md`, `probe-src2.md`, `probe-src3.md`, `probe-src4.md`, `probe-src5.md`, `probe-emdash.md` (boundary probe sources with hyphen/apostrophe/dash/curly-quote cases, e.g. `Dash alpha-one beta.`, `Possessive workers' queue gamma.`, `Alpha—beta gamma.`, `The wor—kers song.`). They were another seat's in-wave scratch, not fixtures with a contract README, and **they were gone again by the time this draft closed** (removed by the wave, consistent with the note's header recording a scratch cleanup and regeneration). Nothing to integrate; recorded because a mid-wave sample listed them.
3. **Artifacts not landed at draft time** (integrator must only claim what
   landed): the note (`corpus/knowledge/anchor-boundaries-r4.md`, `668c1d1f…`)
   and lesson (`corpus/lessons/2026-10-15-anchor-token-boundaries.md`,
   `5bd90e21…`) landed mid-draft and their pins match this report's
   measurements; still absent: an attack-class fixture + contract README,
   `corpus/evidence/*r4*` receipts, SKILL.md and `corpus/README.md` round-4
   rows. `SKILL.md` and `corpus/lessons/2026-10-15-chain-hop-resolution.md`
   diffs in the lane are still round-3 edits (they pin selftest 40 / r3 shas).
   The after-state evidence in this report is therefore the scribe's own
   fresh-process runs plus the landed selftest cases and the note's receipts,
   not a wave fixture.
4. Cosmetic residual carried from rounds 2–3: `tools/research-gate.sh`
   `VERSION=research-gate-r1` — every mode still banners `research-gate-r1`
   (observed at the landed revision; `mode=claims`/`mode=chain` banners are
   correct).
5. Carried structural residuals: in-root hardlinks still bypass path
   canonicalization; no size cap on source reads; the `contradicted` marker
   co-occurrence check (`:923`) is still a plain substring inside the span's
   lines — the round-4 boundary rule covers the span/quote **outer edges**,
   not the marker (named scope, not a defect of this move).

## SHONEN

Author assertions only; a `[x]` requires a named non-author verifier, which
this round did not have. No promotion is implied. [PARENT: mirror the round-3
treatment — all four items remain `[~]`/`[ ]` unless a non-author verifier is
named.]

## Per-axis and learning verdicts

Verdict vocabulary only; no scalar. The declared round move is **calibration**;
other axes are judged separately with their own evidence boundaries.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| calibration | **improved** | Before (r3 gate `67daf85e…`, measured by this seat): the attack class passes — truncated/glued claims 5/5 CLEAN, truncated/glued chain anchors 4/4 CLEAN, and the round-3 truncated-anchor CLEAN (`…kiwami semantic`) reproduces. After (`6b83705b…`): the same bytes fail in both modes (`2/5` and `2/4`, DRIFT, exit 1) with the existing line-aware reports, the word-internal hyphen/apostrophe probes are refused, the legitimate controls (punctuation-followed, line-edge, paren-bounded, ASCII-punctuation-delimited) still pass, and the same bytes verdict the same in both modes. Boundary: matching semantics only — no semantic support, no source truth, no external verification is claimed, and edges that are non-ASCII/undecidable fail closed |
| coverage | unchanged | No new corpus ground: the same claims/chain surfaces are re-judged under the hardened rule; the new selftest cases are generated-fixture coverage, not corpus coverage |
| operability | improved | Selftest 40 → 44 cases, all PASS, first 40 case lines byte-identical; both fixtures, the broken control, the r1 archives and the intake record byte-identical modulo `ts=`; exit contract 0/1/2 unchanged; four new cases run end-to-end through the public CLI |
| depth | improved [PARENT: r3 precedent — its admitted scorecard credited the landed note under depth; the scribe's stricter reading would be unchanged] | `corpus/knowledge/anchor-boundaries-r4.md` (`668c1d1f…`) documents the boundary class, both call sites and the exact residual classes, and the lesson `corpus/lessons/2026-10-15-anchor-token-boundaries.md` (`5bd90e21…`) distils it; their pins match this seat's independent measurements. No independently verified domain fact was added — fixture spans/anchors remain byte controls |
| freshness | unchanged | Pins re-checked at fixed revisions only; no cross-revision drift detector |
| adjacency | unchanged | Zero network (fetch-primitive scan = 0 matches); research corpus read-only; boundary/refusal classes untouched |

Learning trends: **quality improved** — an earlier CLEAN that rested on
substring semantics is now correctly re-judged (the round-3 documented
`…kiwami semantic` anchor: CLEAN before → `anchor-missing` DRIFT after), and
the gate's own documented limit is closed rather than carried.
**expansion unchanged** — no new admitted fixture/contract README landed at
draft time (the selftest cases are generated fixtures; `[PARENT: re-judge if a
wave fixture lands before integration]`).
**discernment unchanged** — no non-author admit/reject spot-check.

## Debt, cross-domain handoff and admission

| Debt | Owner / concrete unblock |
|---|---|
| **Receipt identity (round 1) — STILL OPEN** | The direct interactive launch supplies no authentic queue taskKey or stored expected receipt bag (`.ufo/evidence/round-1/receipt-blocker.json`). Mission acceptance remains integrator-owned: bind this mission/identity to an authentic dispatcher task and validate the six expected fields before any Sighting completion. No `task_…` value was invented; proven receipt-backed completed rounds remain **0**; operator target remains at least 100. |
| Round-4 artifact gaps | Landed at draft time: `tools/research-gate.sh` boundary hardening, note `corpus/knowledge/anchor-boundaries-r4.md` (`668c1d1f…`), lesson `corpus/lessons/2026-10-15-anchor-token-boundaries.md` (`5bd90e21…`) — all uncommitted. Not landed: attack-class fixture + README, `corpus/evidence/*r4*` receipts, SKILL.md round-4 rows, `corpus/README.md` round-4 rows — integrate only what lands, and re-check the after-state if the gate moves past `6b83705b…`. |
| Boundary-class residuals | (a) an occurrence delimited by ASCII punctuation resolves — `minarai/deshi` (slash-delimited) passes by the documented class, so truncation at any class boundary character is still a hit; the note names the larger case, token-aligned shortening (a sub-quote whose edges land on boundaries) — the larger half of the r3 limit; (b) occurrences bounded by non-ASCII punctuation (`—`, `。`, `’`, `→`) fail closed, including legitimate ones adjacent to a non-ASCII byte — not exercised by any current fixture (edge pre-analysis above), named in the note as a deliberate false-negative trade; (c) the `contradicted` marker co-occurrence stays a substring check inside the span lines (`:923`); (d) `_` is a boundary by decision (Markdown emphasis). All are documented consequences, not defects of the declared rule. |
| Scope-refusal finding IDs (round-1 debt) | Still open — documentary refusals only. |
| Non-author spot-check (discernment) | Integrator/operator samples ≥1 admit and ≥1 reject; until then no discernment gain or promotion. |
| Frozen replay gate conformance | `corpus/evidence/round-1/expected.json` pins inputs but is not a rerunnable comparator; still open. |
| Fleet `/tmp` quota | Not observed this round: `/tmp` accepted all scribe writes; the scribe scratch `/tmp/chousa-scribe-r4/` was removed at end of run (every value it held is quoted verbatim in this report and in the note's receipts). |

Cross-domain: no host/source/sibling/shared-ledger mutation; the archived
research corpus was read-only; native session material excluded from commits.

## Fresh-session continuation

[PARENT] Bind a round-4 successor continuation file to this report and the
integrated work HEAD. Acceptance stays separate from local craft results: this
report claims local evidence only, no receipt and no Sighting.