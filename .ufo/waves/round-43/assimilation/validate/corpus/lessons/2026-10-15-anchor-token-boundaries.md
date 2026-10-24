# Round-4 lesson — a quote is not any substring: token-boundary matching, and the class it chooses (2026-10-15)

Round: chousa-shokunin round 4, one calibration move: token-boundary hardening of
the substring matching shared by `verify-claims` spans and `verify-chain` quote
anchors. Lane HEAD `09153d1` (unchanged; no commits by this seat). Gate under
test — before: `tools/research-gate.sh` sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084` (committed at
HEAD; re-staged as `/tmp/chousa-lessons-r4/frozen/tools/gate-before.sh` and
sha-verified there); after: sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2` (mtime
2026-10-16T00:16:32Z; settled — 8 identical 30-second samples 00:16:57Z →
00:20:57Z in `poll.log`, and identical again after my whole battery). Fixtures
under test: `corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`,
`corpus/fixtures/chain-r3.md` sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`, control
`corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`.
verified-at: 2026-10-15/16, from the lane cwd; fresh-process CLI runs; read-only
local opens only; nothing was fetched or executed.
recheck:
`bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..`
· `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..`
· `bash tools/research-gate.sh --selftest`

Raw probe outputs and the frozen before gate: `/tmp/chousa-lessons-r4/`
(`poll.log`, `logs/`, `root/src.md`, `claims-scratch.jsonl` = 18 probe claims,
`chain-scratch.md` = 17 probe hops, `claims-real.jsonl`, `chain-real.md`,
`boundary-check.py`, `rederive-boundary.py`, `frozen/tools/gate-before.sh`).
This seat wrote no lane file outside `corpus/lessons/`; all script line numbers
below are relative to the after revision `6b83705b…` unless stated otherwise.

## The claim, and the hole it names

Round 3 closed by naming its own limit: anchors and claim spans were checked by
byte SUBSTRING containment, so a truncated quote still resolved
(`corpus/knowledge/chain-resolution-r3.md`, "Anchor semantics"). Round 4's
falsifiable claim: before the move a citation span/anchor that is a truncated or
padded variant of real source text passes verification; after it, matching
happens only at token boundaries (documented class: line edges, whitespace,
ASCII punctuation; word-internal hyphens/apostrophes are not boundaries) with the
line-aware miss reports; legitimate spans, including those followed by
punctuation, still pass; r1–r3 selftest cases and fixture CLEAN results hold; the
rule is identical across both modes; the selftest gains truncation/padding/
punctuation/line-edge cases.

Measured BEFORE at `67daf85e` (probe files as above; every probe claim is
`expect=supported`, so "match" means "the gate accepted it"):

```text
$ bash frozen/tools/gate-before.sh verify-claims claims-scratch.jsonl --root <scratch>
CLAIM id=S02 expected=supported observed=supported source=src.md at=line:1 verdict=match
CLAIM id=S03 expected=supported observed=supported source=src.md at=line:1 verdict=match
CLAIM id=S06 expected=supported observed=supported source=src.md at=line:3 verdict=match
CLAIM id=S08 expected=supported observed=supported source=src.md at=line:1 verdict=match
CLAIM id=S16 expected=supported observed=supported source=src.md at=line:11 verdict=match
CLAIM id=S17 expected=supported observed=supported source=src.md at=line:2 verdict=match
VERDICT_BEARING_CLAIMS=18/18
RESEARCH_GATE: CLEAN (claims=18 supported=18 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit 0
```

with `S02` = `line-one alpha marke` (truncated inside the final token), `S03` =
`ine-one alpha marker` (glued past the first character), `S06`/`S07` = `well`
and `known marker` (inside/after `well-known`), `S08` = `l` (inside `l'ecole`),
`S16` = `mwalpha` reported `at=line:11` where it is glued inside
`xxmwalphayy` — not the clean occurrence at line 12, `S17` = `gluezone bravo 12`
(padded into the following token). The same bytes as `verify-chain` quote
anchors: 17/17 hops `observed=verified`, `RESOLVED_HOPS=17/17`, CLEAN, exit 0.
Real-corpus probes: claims 5/5 (`R02` `…tokens to 12` truncating `122`; `R03`
`…sources searche` truncating `searched.`; `R04` `…and transmissi` truncating
`transmission.”`), chain 6/6 (hop 2 `he strongest historical model…` glued past
`T`; hop 3 the same `to 12` truncation of a real B:79 span). All three rounds'
fixtures were CLEAN as recorded: claims 17/17, chain 17/22, selftest 40.

## Observation — the rule that landed

The after revision documents the class in the file header (`:68-86`) and
implements it once for both modes: `TOK_WS`/`TOK_PUNCT` (`:772-773`),
`tok_word_char`/`tok_left_ok`/`tok_right_ok` (`:775-810`), and
`tok_span_at` (`:812`) which returns the first DELIMITED occurrence and skips
glued substrings. `verify-claims` calls it for the span (`:907`); the chain
`quote` anchor uses it inside `chain_anchor_at` (`:1045`, call `:1060`).
Boundary = file/line edge, ASCII whitespace, or ASCII punctuation; `-`/`'` are
boundaries only when they do not join two word characters; word character =
ASCII alnum or any non-ASCII byte; `_` is in the punctuation set (a boundary).
`heading` and `line` anchors keep their trimmed-equality semantics.

Measured AFTER at `6b83705b`, same probe files:

```text
$ bash tools/research-gate.sh verify-claims claims-scratch.jsonl --root <scratch>
CLAIM id=S02 expected=supported observed=unsupported source=src.md at=- verdict=mismatch
CLAIM id=S16 expected=supported observed=supported source=src.md at=line:12 verdict=match
VERDICT_BEARING_CLAIMS=8/18
RESEARCH_GATE: DRIFT (claims=18 supported=8 contradicted=0 unsupported=10 mismatched=10 unproven=0 refused=0 invalid=0 findings=10 drift=10)
exit 1

FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=S02 nearest_line=1 context=line-one alpha marker
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=S03 nearest_line=1 context=line-one alpha marker
```

The 10 misses are exactly the 10 glued/truncated/non-ASCII-neighbour probes:
`S02 S03 S06 S07 S08 S11 S12 S13 S14 S17`; the 8 hits are `S01 S04 S05 S09 S10
S15 S16 S18` — note `S16` now resolves at `line:12` (the first delimited
occurrence), and `S18` (`snake` before `_`) passes because `_` is a boundary.
The chain mode on the byte-identical anchors:

```text
$ bash tools/research-gate.sh verify-chain chain-scratch.md --root <scratch>
CHAIN hop=2 status=resolved observed=anchor-missing source=src.md anchor=quote:"line-one alpha marke" at=- verdict=mismatch
CHAIN hop=14 status=resolved observed=verified source=src.md anchor=quote:"mwalpha" at=line:12 verdict=match
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=src.md anchor=quote:"line-one alpha marke" nearest_line=1 context=line-one alpha marker
RESOLVED_HOPS=8/17
RESEARCH_GATE: DRIFT (hops=17 verified=8 exempt=0 anchor-missing=9 refused=0 invalid=0 findings=9 drift=9)
exit 1
```

`anchor-missing` = hops 2, 3, 5, 6, 9, 10, 11, 12, 16; verified = 1, 4, 7, 8,
13, 14, 15, 17. **The partition is identical to the claims partition on the same
bytes** — hops 2/3/5/6/9–12/14/16/17 carry byte-identical anchors to
S02/S03/S06/S08/S11–S14/S16/S17/S18 respectively — which is the round's
"identical rule across both modes", measured rather than asserted. Real-corpus
probes flip the same way: claims 2/5 (`R01`, `R05` legit; `R02/R03/R04` now
`unsupported`), chain 4/6 (hop 2 glue and hop 3 digit-truncation now
`anchor-missing`; hops 1/4/5/6 legitimate and verified).

What held unchanged:

- Fixtures at the after gate: `VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE:
  CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 …)`,
  exit 0; `RESOLVED_HOPS=17/22`, `RESEARCH_GATE: CLEAN (hops=22 verified=17
  exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)`, exit 0;
  broken control `RESOLVED_HOPS=1/2`, `DRIFT (… anchor-missing=1 …)`, exit 1 —
  stdout byte-identical to the frozen before logs (normalizing the `ts=` field
  and the command path only).
- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (44 cases)`, exit 0; the first 40
  `ok-case` lines are byte-identical to the round-3 selftest, so every r1/r2/r3
  case still passes verbatim; cases 41–44 are `claims-boundary-pass`,
  `claims-boundary-fail`, `chain-pass-boundary`, `chain-fail-boundary`
  (`:2014-2075`, fixture `lib/boundary.md` `:1268-1275`).
- Round-1 regression: `verify` on A/B/C under the frozen clock is byte-identical
  to the before run (mod `ts=`), the intake note stays exit 0 and
  byte-identical, and `verify` on `chain-r3.md` still closes CLEAN — the
  structural mode is untouched, so the r1 hole it has is neither widened nor
  papered over by this move.
- No-fetch bound: `strace -f -e trace=network` around the after
  `verify-chain corpus/fixtures/chain-r3.md` run → 0 `socket(`/`connect(`
  syscalls in a 5,300-line trace; exit 0.
- Independent re-derivation: `rederive-boundary.py` (this seat, python, reads
  only) re-implements the header rule literally against the same probe inputs
  and reproduces the gate's after disposition for all 18 + 17 scratch probes and
  all 6 real anchors, including `at=line:` positions (T16 → line 12). The
  fixtures' pre-registered CLEANs therefore do not depend on trusting the
  implementation's own summary.

## Independent boundary analysis of the fixtures (gate-free)

`boundary-check.py` locates every matched r2 claim span and every resolved r3
quote/line anchor in its cited source and reports the byte classes at the two
outer edges. Result: all 21 matched entries sit on line-edge / whitespace /
ASCII punctuation at both ends (B03 and chain hops 3/9 end before `;` and `)`).
No fixture entry has a non-ASCII or word-character neighbour, so the documented
class cannot break a fixture entry — which is why 17/17 and 17/22 survived.

## Bounds measured this round (name them wherever the new CLEAN is cited)

- **Truncation at a token boundary still passes.** `S04` (`gluezone bravo`,
  line continues ` 122 units`) and every whole-line anchor still resolve: the
  move closes glue games, not "quoted less than the sentence" games. Interior
  paraphrases still cannot pass (bytes must occur), but dropping whole words
  can. Location binding and uniqueness remain unverified (round-3 bounds).
- **Non-ASCII neighbours fail closed.** `S11`–`S14` (occurrence ending or
  starting right before/after `”`, `。`, `→`, `“`) are rejected although the
  span bytes are real. This is the documented class, not a bug: the class is
  ASCII-anchored deliberately, and widening it is a future move with its own
  falsifiable claim (my probes above would measure it directly).
- **`_` is a boundary, `-`/`'` are conditional.** `S18` (`snake` before
  `_`) passes; `S06`–`S08` (`well`, `known`, `l` cut at a hyphen/apostrophe)
  fail; the selftest's `delta boundary word-` at a line break passes (the joiner
  check sees the newline). These are class choices with visible consequences on
  identifier-like and possessive text.
- **First DELIMITED occurrence is what is reported.** `S16` moved from
  `at=line:11` (glued) to `at=line:12` (clean) rather than failing on the first
  substring hit — the right call, and the reason a glued first hit does not
  create a false miss.
- **Outer edges only.** A multi-line span is delimited by its first and last
  character (selftest `BP4` → `at=lines:1-2`); it may cut mid-token inside, as
  before.
- **Methodology trap (this seat's own, measured).** The gate derives `LANE_ROOT`
  from its own location (`dirname(script)/..`). A "before" copy staged at
  `/tmp/chousa-lessons-r4/gate-before.sh` silently made `/tmp` the lane root:
  three selftest cases failed because the out-of-corpus fixture (`/tmp/…`) was
  suddenly in-boundary, and the intake note drifted on lane-relative pointers.
  Re-staging at `<scratch>/frozen/tools/gate-before.sh` (so `dirname/..` is a
  dedicated directory) reproduced the frozen revision's behavior exactly. Any
  frozen-revision re-run must preserve that layout.

## Method statement

A token-boundary CLEAN establishes: for every claim read and every unmarked
`resolved` hop, the literal span/anchor bytes occur in the cited local source at
a position whose two outer edges are delimited by the documented class (file
edge, line edge, ASCII whitespace, ASCII punctuation; `-`/`'` only when not
joining two word characters), at the first delimited occurrence reported as
`at=`; interior bytes stay byte-exact and multi-line spans are delimited by
their outer characters alone. What that does not prove, stated wherever such a
CLEAN is cited:

- **Not location binding or uniqueness.** `at=` is the first delimited
  occurrence; duplicates elsewhere are neither reported nor required.
- **Not semantics, agreement, authorship, or source truth.** Rounds 2–3 bounds
  stand unchanged: the bytes exist; nothing follows about what they mean or
  whether the citing statement agrees.
- **Not full quote integrity.** Token-boundary truncation (whole words dropped)
  still passes; only truncation/padding landing inside a token is refused.
- **Not exemption truth.** Marked hops stay unexamined and counted.
- **Text files only**, read whole into memory; the round-1/2 residuals (in-root
  hardlinks, no source size cap, the `research-gate-r1` banner) are untouched by
  this move.

## Defects and follow-ups noted (outside this seat's write scope)

- `corpus/knowledge/chain-resolution-r3.md:118` cites
  `chain-r3-20261015T235411Z-live.log` as a standing receipt; that file does not
  exist on disk or in git history (committed receipts are `…235623Z…`).
  `corpus/README.md:42` records that the earlier cut was superseded and removed
  in-wave, and the surviving live receipt's "negative control 1" is a padded
  `semanticsX` that DRIFTED — not the truncated form the note describes. The
  underlying substring-truncation fact is true and reproduced by my before
  probes; the citation should point at the removal note or a fresh receipt
  (receipts-writer scope).
- Residual limits above (token-boundary truncation, non-ASCII fail-closed,
  `_` boundary) are named for the gate owner; none is a defect against the
  round's documented class.
- Round-1 **receipt identity remains open**; nothing in this lesson mints or
  counts a receipt.

## Gate

### Candidates

1. This lesson.
2. The reading "the gate now verifies quotation" as a truth or location claim.
3. Adopting fixture anchors or the exports' content as domain knowledge.
4. A new `corpus/QUALITY.md` criterion from this round's rejections.
5. Promotion marks / SHONEN boxes.
6. Widening the boundary class to non-ASCII punctuation inside this round.

### Admitted

- Candidate 1, this note (`corpus/lessons/2026-10-15-anchor-token-boundaries.md`;
  the lane convention is `round-<N>.md`, `LEARNING.md:61`, so the integrating
  parent may rename).

### Rejected, with reasons

- Candidate 2 — overclaim; the probes falsify it: `S16` resolves at the first
  delimited occurrence, not at the quoted line; token-boundary truncation passes;
  no location or uniqueness binding.
- Candidate 3 — byte controls, not knowledge (`claims-r2.README.md`,
  `chain-r3.README.md`); nothing is adopted here.
- Candidate 4 — no QUALITY-bar miss produced this round's rejections.
- Candidate 5 — refused; this seat grants nothing and no non-author spot-check
  exists.
- Candidate 6 — the class is documented and the fixtures have no non-ASCII
  neighbours; widening is its own move with its own claim, not a fix to smuggle
  into a calibration round.

### Spot-check

**Unavailable — measured outcome, not omission** (as in rounds 1–3: every
reviewer is a lane seat, `LEARNING.md:41-43`; no non-author sampled an admit and
a reject). Discernment remains unchanged.

## Verification boundary (parent-owned)

Integration counts, commit hashes, the round report/SCORECARD/LOG entries and any
frozen-replay evidence are parent-owned; nothing here pre-claims them. The
before/after pair measured here is: `67daf85e…` (committed) → `6b83705b…`
(working tree, uncommitted at this writing, sha-stable across the full battery).
Mission acceptance remains blocked on round-1's receipt identity (still open);
no `task_…` value is invented and no receipt was counted. Later corrections land
as append-only errata blocks (`QUALITY.md:4`).