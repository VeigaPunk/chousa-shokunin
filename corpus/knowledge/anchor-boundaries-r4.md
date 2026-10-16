# Anchor/span token boundaries — round-4 matching hardening (research-gate)

source: lane HEAD `09153d19871158380f64b6f58a14b6912aab676f`; round-4 gate
`tools/research-gate.sh` sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`
(mtime 2026-10-15T21:16:32-0300 = 2026-10-16T00:16:32Z; observed identical
before and after every run below); the round-3 revision it replaces is
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`, still
recoverable as `git show HEAD:tools/research-gate.sh`; fixtures unchanged —
`corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`,
`corpus/fixtures/chain-r3.md` sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`,
`corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`.
verified-at: 2026-10-15/16, from the lane cwd; fresh-process CLI runs;
read-only local opens only; nothing was fetched or executed. Probe and attack
inputs are this seat's scratch (outside the lane), regenerated after a
wave-mate's cleanup wiped the first scratch tree.
recheck:
`bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..`
· `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..`
· `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..`
· `bash tools/research-gate.sh --selftest`

All script line numbers below are relative to the round-4 revision above
(the round-3 numbers quoted for the before-state are relative to `67daf85e…`).

## The move

Round 3 left a named limit: anchors and claim spans matched by SUBSTRING, so a
truncated or padded variant of real source text resolved
(`corpus/knowledge/chain-resolution-r3.md`, "Anchor semantics"). Round 4's
falsifiable claim: **before**, such a variant passes verification; **after**,
both `verify-claims` spans and `verify-chain` quote anchors match only when
both outer edges of the occurrence sit at a token boundary, so truncation,
padding and gluing games fail while legitimate spans still pass.

Before-state at `67daf85e…`, measured by this seat on purpose-built scratch
fixtures: the claims attack file (mid-token right truncation, mid-token left
padding, intra-token fragment, token-aligned truncation, legit control) closed
`VERDICT_BEARING_CLAIMS=5/5`, `RESEARCH_GATE: CLEAN`, exit 0; the chain attack
record (the same classes as quote anchors) closed `RESOLVED_HOPS=8/8`, CLEAN,
exit 0. The r3 code was `[[ $hay == *"$span"* ]]` for claims (`:813` at that
revision) and `[[ $hay == *"$text"* ]]` for chain quotes (`:968`), with no
notion of an edge.

After-state at `6b83705b…`, same fixtures: claims
`VERDICT_BEARING_CLAIMS=2/5`, `RESEARCH_GATE: DRIFT`, exit 1; chain
`RESOLVED_HOPS=5/8`, DRIFT, exit 1 (verbatim receipts below).

## The token rule (exact)

One implementation, `tok_span_at` (`tools/research-gate.sh:812-831`), is the
only matcher used by either mode: `verify_claims` calls it at `:907-910`
(`start_line`/`end_line`/`at` come from `TOK_L1`/`TOK_L2`/`TOK_AT`) and the
chain `quote` arm calls it at `:1060-1061` (`CITE_AT=$TOK_AT`). The rule is
also stated in the file header (`:68-85`) and in `usage` (`:143-147`).

- **Boundary characters** — the character immediately before the occurrence
  and the character immediately after it must each be one of:
  - an edge: file start/end or a newline (line edge) — `[[ -n $before ]]` /
    `[[ -n $after ]]` short-circuits to OK (`:786`, `:800`);
  - `TOK_WS` = space, tab, LF, CR, VT, FF (`:772`);
  - `TOK_PUNCT` = ``!"#$%&()*+,./:;<=>?@[\]^_`{|}~`` (`:773`).
- **Word character** (`tok_word_char`, `:775-782`): an ASCII letter, an ASCII
  digit, or **any non-ASCII character**. `-`, `'`, whitespace and ASCII
  punctuation are not word characters.
- **Hyphen and apostrophe are conditional boundaries** (`tok_left_ok` `:784-796`,
  `tok_right_ok` `:798-810`): when the adjacent character is `-` or `'`, it is a
  boundary only if it does **not** join two word characters. `cross-check` and
  `workers'` are therefore single tokens: an occurrence that starts or ends
  inside them is not a hit, while `-`/`'` after a space or before a space is.
- **Non-ASCII fails closed**: `—`, `。`, `’`, `”`, `→` are not in either set, so
  they are word characters and are not boundaries. An occurrence abutting one
  without intervening whitespace is a miss.
- **Only the outer edges are checked.** A multi-line span is delimited by its
  first and last character alone and may cut mid-token inside; `TOK_L2` is
  computed from the span's own newline count (`:824`).
- Matching stays **byte-exact and case-sensitive**; no normalization,
  folding or fuzzy matching was added.
- The reported hit is the **first delimited occurrence**. Occurrences that are
  substrings but glued into a word are skipped and the loop keeps absolute line
  accounting (`dropped`, `:828`), so a span whose first occurrence is glued is
  still reported at its later, delimited occurrence — measured: a source with
  `prefoo bar` on line 1 and `foo bar` on line 2 gives `at=line:1` at
  `67daf85e…` (the glued occurrence) and `at=line:2` at `6b83705b…`.
- `heading` and `line` anchor kinds are unchanged: they remain trimmed
  equality, where a "boundary" question does not arise. The rule governs
  `verify-claims` spans and `verify-chain` quote anchors only.

## What the hardening catches

Measured, before → after, same fixtures, gates `67daf85e…` → `6b83705b…`:

- **Mid-token right truncation** (the case round 3 named): chain attack hop 2
  `…kiwami semantic` cut one byte inside `semantics` — CLEAN before,
  `observed=anchor-missing` after. Claims TA1 (`…transmiss`) likewise
  `unsupported`.
- **Mid-token left padding**: chain hop 3 `inarai/…` (one byte glued onto the
  front of the token), claims TA2 (`ssion.” Japanese…`).
- **Intra-token fragment**: claims TA5 (`ransmission` alone).
- **Possessive / joiner cuts**: the selftest's `gamma boundary word` (cut
  before `'s`) and `foo` (cut before `-`) now miss; chain attack hop 6
  `ryu/kiwami` (starting inside `jin'i-ryu`) misses.
- **Padded extra words glued into a compound**: selftest `theta boundary word
  continuation` (the source has `continuation-suffix`) misses.
- **Battery shape**: an 86-probe battery over a synthetic source — one
  question per span (each ASCII punctuation character as left neighbour, the
  same set as right neighbour, line start, line end, tab, the `-`/`'`
  compounds, mid-word cuts) — closed `86/86` CLEAN before and `71/86` after,
  and the 15 failing probes are **the same 15 in both modes** (identical sets
  of probe ids, claims vs chain). That is the evidence for the round's
  "identical rule across both modes" clause; the shared call sites `:907` and
  `:1060` are the mechanism.
- **Legitimate spans still pass**: the full 17-claim fixture, the 17 resolving
  hops of `chain-r3.md`, and every probe whose edges are space, tab, line edge
  or ASCII punctuation — including spans *followed by punctuation* (chain
  attack hop 7 `…semantics)`, claims TA4 ending before `.”` + space) and
  whole hyphenated/apostrophe compounds (`foo-bar`, `jin'i-ryu`).

## What it still cannot (honest limits)

- **Token-aligned shortening still passes.** The hardening refuses an edge that
  is *inside* a token; it does not refuse a shorter span whose edges land on
  boundaries. Claims TA3 (dropping the trailing `.”`, ending at `transmission`)
  and chain attack hop 4 (`minarai/…/kiwami` with ` semantics` dropped) both
  still resolve, exit 0. A sub-quote that begins and ends at legitimate token
  edges is indistinguishable from a complete one — that is the residual
  substring gap, and it is the larger half of the r3 limit.
- **Not semantic support, not agreement, not context.** A boundary-clean span
  can still be contextually misleading; the mode never parses meaning. The r2
  and r3 limits stand verbatim (`corpus/knowledge/claim-verification-r2.md`,
  `chain-resolution-r3.md`): no support adjudication, no location binding or
  uniqueness (the first delimited occurrence is informational), no source
  truth, no external verification, no transitivity across hops.
- **Non-ASCII "fails closed" is also a false-negative risk.** A legitimate span
  whose outer edge abuts a typographic character with no space — immediately
  after `”`, `—`, `。`, `→` — is a MISS. Ten of the fifteen probe failures are
  exactly this class (left and right neighbours `”`, `’`, `—`, `→`, `。`). No
  fixture anchor is affected at `6b83705b…` (all r1-r3 fixtures hold), but a
  source that sets a quote tight against a curly quote or an em dash would
  report `anchor-missing` for a span that is really there. The trade is
  deliberate (an undecidable edge fails closed) and is named here rather than
  hidden.
- **`_` is a boundary by decision.** It is in `TOK_PUNCT` (documented as
  Markdown emphasis, `:77-78`), so a span glued to `_` still resolves — a
  residual gluing class for identifier-like text.
- **Not a diff or a normalizer**: text files only, read whole into memory after
  the same canonicalization and boundary checks as before; the in-root hardlink
  bypass and the missing source size cap from rounds 2-3 remain; the banner
  string still reads `research-gate-r1` (cosmetic).
- **Only resolved hops are affected**: exempt hops are still exempt and
  counted, and an exemption remains the author's declaration, not a
  resolution. The rule makes claims/hops *harder to satisfy*; it cannot make a
  wrong citation disappear, only a glued one.

## Receipts (round-4 revision, run by this seat)

All runs at gate sha256 `6b83705b…`, identical before and after each run
(`sha256sum` sampled pre/post); lane cwd; fixtures at the shas in the header;
attack/probe inputs in this seat's scratch; ambient locale `LANG=en_US.UTF-8`
(LC_ALL unset), under which bash slices `${var: -1}` per character. The
classification is locale-stable for UTF-8 input: under a C/POSIX locale the
slice yields a UTF-8 byte ≥ 0x80, which is not in `TOK_WS`/`TOK_PUNCT` and is
therefore still a word character — the same answer either way.

- Selftest: `bash tools/research-gate.sh --selftest` → 44 ok-cases, exit 0,
  closing `RESEARCH_GATE_SELFTEST: PASS (44 cases)`. A line-diff against the
  40-case run shows **only** four added `ok-case` lines and the changed closing
  line — cases 1-40 are byte-identical. New cases: `claims-boundary-pass`
  (`:2020`), `claims-boundary-fail` (`:2027`), `chain-pass-boundary`
  (`:2048`), `chain-fail-boundary` (`:2068`), all over the same generated
  fixture bytes `lib/boundary.md` (`:1268-1272`) so both modes are exercised
  on one rule: passes = punctuation edge, non-word-internal hyphen, line edge,
  multi-line span (`lines:1-2`); misses = mid-token truncation, padded extra
  word into a hyphenated compound, possessive apostrophe join.
- Claims fixture (regression): `bash tools/research-gate.sh verify-claims
  corpus/fixtures/claims-r2.jsonl --root ..` → `VERDICT_BEARING_CLAIMS=17/17`,
  `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2
  mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)`, exit 0 —
  stdout byte-identical to the same run under `67daf85e…` after normalizing
  the `ts=` field.
- Chain fixture (regression): `verify-chain corpus/fixtures/chain-r3.md
  --root ..` → `RESOLVED_HOPS=17/22`, `RESEARCH_GATE: CLEAN (hops=22
  verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0
  drift=0)`, exit 0, the same 17 `at=` values as round 3 (74, 64, 35, 107, 109,
  57, 71, 67, 79, 88, 67, 87, 89, 52, 63, 55, 107); byte-identical to the
  `67daf85e…` run modulo `ts=`. No r3 anchor was reclassified.
- Broken control (regression): `verify-chain corpus/fixtures/chain-r3-broken.md
  --root ..` → exit 1, `RESOLVED_HOPS=1/2`, `RESEARCH_GATE: DRIFT (hops=2
  verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1
  drift=1)`, byte-identical to the `67daf85e…` run modulo `ts=`; the
  `人為 — jin’i-ryū` anchor still misses (it is absent from the target, not
  merely ill-edged).
- Round-1 observable (regression): A/B/C under `CHOUSA_NOW_EPOCH=1760000000`
  and `--root ..` → each exit 1 with `RESEARCH_GATE: DRIFT (findings=6
  drift=5 …)`, byte-identical to the `67daf85e…` runs.
- Claims attack (before → after), verbatim after-side lines:

  ```text
  CLAIM id=TA1-midword-right-trunc expected=supported observed=unsupported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=- verdict=mismatch
  CLAIM id=TA2-midword-left-pad expected=supported observed=unsupported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=- verdict=mismatch
  CLAIM id=TA3-token-aligned-trunc expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:52 verdict=match
  CLAIM id=TA4-legit-control expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:52 verdict=match
  CLAIM id=TA5-intra-token-fragment expected=supported observed=unsupported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=- verdict=mismatch
  FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=TA1-midword-right-trunc nearest_line=52 context=The strongest historical model for your roster is “earned responsibility withi
  VERDICT_BEARING_CLAIMS=2/5
  RESEARCH_GATE: DRIFT (claims=5 supported=2 contradicted=0 unsupported=3 mismatched=3 unproven=0 refused=0 invalid=0 findings=3 drift=3)
  ```

  (`TA3` passing is the residual limit above, not a defect; `TA4` is the
  control.) Before: `VERDICT_BEARING_CLAIMS=5/5`, CLEAN, exit 0.
- Chain attack (before → after), verbatim after-side lines:

  ```text
  CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"minarai/deshi/shokunin/jin'i-ryu/kiwami semantics" at=line:35 verdict=match
  CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"minarai/deshi/shokunin/jin'i-ryu/kiwami semantic" at=- verdict=mismatch
  CHAIN hop=3 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"inarai/deshi/shokunin/jin'i-ryu/kiwami semantics" at=- verdict=mismatch
  CHAIN hop=4 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"minarai/deshi/shokunin/jin'i-ryu/kiwami" at=line:35 verdict=match
  CHAIN hop=5 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"kiwami semantics" at=line:35 verdict=match
  CHAIN hop=6 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"ryu/kiwami" at=- verdict=mismatch
  CHAIN hop=7 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"shokunin/jin'i-ryu/kiwami semantics)" at=line:35 verdict=match
  CHAIN hop=8 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"minarai/deshi/shokunin/jin'i-ryu/kiwami semantics" at=line:35 verdict=match
  RESOLVED_HOPS=5/8
  RESEARCH_GATE: DRIFT (hops=8 verified=5 exempt=0 anchor-missing=3 refused=0 invalid=0 findings=3 drift=3)
  ```

  Before: `RESOLVED_HOPS=8/8`, CLEAN, exit 0. Hop 5 (`kiwami semantics`,
  starting after `/`) and hop 7 (ending with `)`) pass, i.e. ASCII punctuation
  is a boundary in both directions; hop 6 (`ryu/kiwami`, starting after `'`)
  fails, i.e. the apostrophe joiner clause.
- Probe battery (86 probes, synthetic source; one boundary question per span):
  `86/86` CLEAN before in both modes; after, `VERDICT_BEARING_CLAIMS=71/86`
  and `RESOLVED_HOPS=71/86`, both DRIFT exit 1, and the failing id sets are
  identical across modes. The 15: `left-”`, `left-’`, `left-—`, `left-→`,
  `left-。`, `right-”`, `right-’`, `right-—`, `right-→`, `right-。`,
  `compound-hyphen-cut-tail` (`foo` before `-`), `compound-hyphen-cut-head`
  (`bar baz` after `-`), `compound-apos-cut-head` (`i-ryu semantics` after `'`),
  `midword-right-trunc` (`transmiss`), `midword-left-pad` (`ansmission
  complete`). Every ASCII punctuation neighbour, both line edges, the tab
  neighbour, whole compounds and the full-span control pass.
- Later-occurrence accounting: the two-line source above → `LX1` (`foo bar`)
  `at=line:1` at `67daf85e…` (first occurrence, glued) and `at=line:2` at
  `6b83705b…` (first *delimited* occurrence), `LX2` (`prefoo bar`) `at=line:1`
  in both; `VERDICT_BEARING_CLAIMS=2/2`, CLEAN, exit 0 in both.
- Independent check without the gate (this seat's own python, scratch only:
  the documented rule re-implemented from the header — boundary sets, word
  character, joiner clause, first-delimited-occurrence scan): compared against
  the gate's own verdicts on all 86 probes, `agreements: 86`,
  `disagreements: []`, `INDEPENDENT_CHECK: AGREE`. Disposition *and* reported
  line were compared, not just the pass/fail set.
- Zero network: `strace -f -e trace=network` around the positive
  `verify-chain` run recorded 0 socket/connect/sendto/recvfrom lines (8347
  trace lines, all process/signal noise); exit 0, `RESOLVED_HOPS=17/22`.
- Reproducibility of the pair: the r3 side is recoverable from the lane
  (`git show HEAD:tools/research-gate.sh`, sha256 `67daf85e…`); re-running it
  on the same scratch fixtures reproduces every before-state number above, so
  the contrast does not depend on this seat's discarded logs. The attack and
  probe inputs themselves are scratch, not lane material (the lane's own
  round-4 fixtures are other seats' artifacts); the durable, lane-local
  reproduction of the rule is the gate's own selftest cases 41-44, which
  generate their fixtures (`lib/boundary.md`, `:1268-1272`) and run them
  through both modes.

## Open items

- **Receipt identity (round 1) — STILL OPEN.** These are lane-local evidence
  runs, not queue taskKey/expected-receipt bags; mission acceptance remains
  integrator-owned and no `task_…` value may be invented. Proven
  receipt-backed completed rounds remain 0; the operator target (≥100) is
  unchanged, routing supplied by the operator's in-session direct dispatch.
- **Token-aligned shortening remains a pass** (named above). A follow-up could
  require the span to be a whole-line prefix/suffix or to carry its terminal
  punctuation, but nothing of the sort is built here and no claim is made that
  it would be safe.
- **Non-ASCII boundary false negatives** (named above): promoting typographic
  punctuation (`” ’ — 。 →`) to boundary characters while keeping `-`/`'`
  word-internal would close the false-negative class without reopening the
  joiner games — not done in this round, and not asserted as correct without
  a fixture that exercises it.
- **`_`-adjacent gluing remains** (deliberate: `_` is ASCII punctuation here).
- No commits by this seat; the gate is an uncommitted working-tree change at
  lane HEAD `09153d1` (` M tools/research-gate.sh`). `SKILL.md` gate rows are
  the skill-row-updater seat's write, and the lane's own round-4 fixtures are
  other seats' artifacts — nothing here should be read as a promotion,
  field-readiness claim, or admission verdict.
- By design, not debt: semantic support, source truth, transitive chaining and
  external-source verification stay outside the mode.
