# LOG.md — round-4 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT. Measured values: before-state at lane HEAD 09153d1's gate
     sha256 67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084;
     after-state at the settled gate sha256
     6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
     (4 identical 30 s samples before the battery, re-checked around and after
     it). Scribe scratch /tmp/chousa-scribe-r4/ (declared ephemeral, cleaned at
     end of run). [PARENT] marks parent-only bindings (commits, admission,
     wave counts). The debts section keeps the receipt-identity debt OPEN per
     the mission contract. -->

## 2026-10-15 — round-4 calibration: token boundaries for claims spans and chain quotes

Round 4 executes the move round 3 registered: token-boundary hardening so
truncated-quote games cannot resolve (plus the claim-span truncation class from
round 2's note). The operator dispatched this wave directly in-session (same
routing as rounds 2–3; **no Sighting step was invoked**); receipt identity from
round 1 remains open and untouched by this round.

**Before.** At the round-3 revision (sha256 `67daf85e…`, lane HEAD `09153d1`),
matching is substring semantics in both modes. Measured by this seat at that
revision, fresh-process CLI runs:

- Claims: a probe file with three attack variants of real source text on line
  86 of `research/deep-research-2026-09-28/A-shokunin-tradition.md` — X1
  `apprenticeship is an economic and social institu` (cut mid-word), X2
  `pprenticeship is an economic and social institution` (glued left), X3
  `hey show that apprenticeship is an economic and social institution a`
  (glued both edges) — closed `VERDICT_BEARING_CLAIMS=5/5`,
  `RESEARCH_GATE: CLEAN`, exit 0, together with the legitimate controls
  X4 `common final examination` (followed by `.`) and X5 `These examples
  matter because they show that apprenticeship` (line start).
- Chain: a four-hop record whose hops 1–2 cite `customary apprenticeship
  periods of approximate` (cut mid-word) and `pproximately seven years for
  carvers` (glued left) closed `RESOLVED_HOPS=4/4`, `RESEARCH_GATE: CLEAN`,
  exit 0, alongside the legitimate hops 3–4 (same controls as X4/X5).
- The round-3 note's documented residual reproduced exactly: a record whose
  hop 1 cites the one-byte-truncated `minarai/deshi/shokunin/jin'i-ryu/kiwami
  semantic` closed `RESOLVED_HOPS=2/2` CLEAN, exit 0, because the truncation
  stayed a substring (`corpus/knowledge/chain-resolution-r3.md`, "Anchor
  semantics").
- Baseline for "unchanged": selftest `PASS (40 cases)`; `verify-claims
  corpus/fixtures/claims-r2.jsonl --root ..` → 17/17 CLEAN; `verify-chain
  corpus/fixtures/chain-r3.md --root ..` → `RESOLVED_HOPS=17/22` CLEAN and
  `chain-r3-broken.md` → 1/2 DRIFT exit 1; A/B/C each exit 1 →
  `VERDICT_BEARING_EXPORTS=3/3`; intake `CLEAN (… chains=8 …)` exit 0.

**The move.** `tools/research-gate.sh` (uncommitted working tree): one shared
token-boundary rule (header `:68-85`, usage `:143-148`) implemented by
`TOK_WS`/`TOK_PUNCT` `:772-773`, `tok_word_char` `:775-782`,
`tok_left_ok` `:784-796`, `tok_right_ok` `:798-810`, and `tok_span_at`
`:812-831`, which iterates occurrences, skips glued ones and reports the first
boundary-delimited hit (`at=line:N` / `lines:N-M`). Both substring call sites
now route through it — claims spans `:907` and the chain quote branch
`:1060-1061` (`heading`/`line` anchor kinds unchanged). A boundary is a
file/line edge, ASCII whitespace or ASCII punctuation at the match's outer
edges; a `-` or `'` is a boundary only when it does not join two word
characters, a word character is ASCII alnum or any non-ASCII character (so
`—`, `。`, curly quotes are NOT boundaries and undecidable edges fail closed),
`_` is a boundary; only the outer edges are checked, so a multi-line span may
cut mid-token inside.

**Selftest.** 40 → 44 cases, all PASS; the first 40 case lines byte-identical.
Cases 41–44: `claims-boundary-pass` (exit 0), `claims-boundary-fail` (exit 1),
`chain-pass-boundary` (exit 0), `chain-fail-boundary` (exit 1). The claims pair
and the chain pair run the same fixture bytes (`lib/boundary.md`) through both
modes — punctuation edge, non-word-internal hyphen at line end, line edge,
multi-line span pass; mid-token truncation, padded extra word into a
hyphenated compound, possessive apostrophe fail — in-selftest evidence that one
rule governs both modes.

**Measurements after the move** (gate `6b83705b…`, lane HEAD `09153d1`, all
fresh-process by this seat; regression outputs byte-identical modulo `ts=`):

```text
selftest                                   RESEARCH_GATE_SELFTEST: PASS (44 cases), exit 0
claims fixture  claims-r2.jsonl            VERDICT_BEARING_CLAIMS=17/17 ; CLEAN ; exit 0
chain fixture   chain-r3.md                RESOLVED_HOPS=17/22 ; CLEAN ; exit 0
broken control  chain-r3-broken.md         RESOLVED_HOPS=1/2 ; DRIFT ; exit 1
r1 archives A/B/C                          each exit 1, one DRIFT line → 3/3 ; intake CLEAN exit 0
attack claims X1–X3                        observed=unsupported (CLAIM_SPAN_NOT_FOUND nearest_line=86) ; X4/X5 still supported ; VERDICT_BEARING_CLAIMS=2/5 ; DRIFT ; exit 1
attack chain hops 1–2                      observed=anchor-missing (CHAIN_ANCHOR_NOT_FOUND nearest_line=80) ; hops 3–4 verified ; RESOLVED_HOPS=2/4 ; DRIFT ; exit 1
kiwami pair                                truncated hop anchor-missing nearest_line=35 ; real anchor verified ; RESOLVED_HOPS=1/2 ; DRIFT ; exit 1
boundary probes H1–H4 / L1–L3 / D1–D2     9/9 : word-internal hyphen/apostrophe truncations unsupported ; punctuation-followed, line-start, paren-bounded and slash-delimited spans supported ; CLEAN ; exit 0
cross-mode matrix (same bytes both modes)  miss→miss, hit→hit (e.g. "minarai/deshi" supported/verified at=line:35 in both)
```

**Residual boundary classes named (documented consequences, not defects):**
truncation at a boundary character that is ASCII punctuation still resolves
(e.g. `minarai/deshi`, slash-delimited); occurrences bounded by non-ASCII
punctuation (`—`, `。`, `’`) fail closed, including legitimate ones adjacent to
a non-ASCII byte (not exercised by any current fixture: every existing fixture
match edge is a line edge, whitespace or ASCII punctuation); the `contradicted`
marker co-occurrence check stays a plain substring inside the span's lines
(`:923`) — the round-4 rule covers span/quote outer edges only.

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-4 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned, no
`task_…` value was invented, proven receipt-backed completed rounds remain 0,
operator target unchanged (≥100). Round-4 artifacts uncommitted at draft time
([PARENT] commit). Landed during the draft: note
`corpus/knowledge/anchor-boundaries-r4.md` (`668c1d1f…`, pins and results
re-checked against this seat's runs — they agree) and lesson
`corpus/lessons/2026-10-15-anchor-token-boundaries.md` (`5bd90e21…`). Not
landed at draft time: an attack-class fixture + README, round-4 receipts in
`corpus/evidence/`, SKILL.md/`corpus/README.md` round-4 rows — integrate only
what lands. Lane hygiene: six untracked `corpus/fixtures/probe-*.md` scratch
files appeared mid-wave and were removed again in-wave (no action needed;
recorded because a mid-wave sample listed them).