# Round 30 — frozen claims (design v2, frozen before any control or data seat)

**Design v2.** Design v1 was committed at `f42906d7b96e5b219aaa74a5ce4ce407a80cee62`.
Before any control or data seat ran, the L1's own read of the v1 counters found that item
URLs showed their class: C2 paths named the server behavior (`/drip-head/`, `/stall/`,
`/slow-ok/`, `/redir/`), and C1 host names carried the document index while the class plan
was in a fixed order. A candidate could then key the deadline on the path (round-29
lesson: a counter met from labels). v2 makes every path `/x/<random hex>`, every host
`h<hex>.test` or `q<hex>.test`, shuffles the document plan and the registry rows, draws
registry ids from a shuffled pool, and has the harness child delete its run map before the
candidate loads. The predicates, items, labels, totals, bounds and contract are unchanged.
Counter SHA-256 at v2: `c1-count.py` `9a0a3bd7…c13131c`, `c2-count.py` `7823eef5…f1674`,
`qr_harness.py` `06237f36…f54764`. Before receipts at v2:
`.ufo/waves/round-30/controls/before-c1-v2-run{1,2}.json` (78/106 twice) and
`before-c2-v2-run{1,2}.json` (9/20 twice); tool-absent `tool-absent-c{1,2}.json` (0/106,
0/20). The v1 receipts stay as history.

## Design v1 text (unchanged except where v2 above overrides)

Base `a3a3710e3d0adf2f95882292f17b5093e3baf97c`. Written by the L1 before any data seat.
This round works only items from the round-29 outside spot-check's routed list
(`corpus/lessons/round-29-verifier-spotcheck.md` D1 to D7). C1 is the D7 missing-`</head>`
limit, and its counter also carries the D3 classes. C2 is the D7 sentinel findings T1 (DNS
rebinding) and T4 (slow-drip read). D1, D2, D4, D5 and D6 are repairs, not claims.

Both counters run the candidate inside a loopback harness
(`corpus/evidence/round30/qr_harness.py`). They fetch nothing from the network, so a
non-author can re-execute them. Every run draws a fresh 64-bit seed from `os.urandom`; no
caller can choose a seed (round-29 lesson, design v2 void). All documents, words, ids,
paths, host names and addresses are generated per run, so no committed byte holds an item
or a label.

The rule from the round-29 lesson and addendum §9 binds: a control wave scores the
do-nothing, junk, all-false, no-reader and shortcut controls on these counters before any
data seat. If any control meets a counter, that claim is re-designed before data or
declared exploratory. It is never re-scaled. No control seat may build a candidate that
implements the full contract v2 change on these counters (routed D5): controls skip the
work; they do not do it.

## Claim C1 — coverage: the edge class of HTML documents that omit `</head>`

**Axis by surface:** coverage. The surface is one new edge class of the quote re-open
tool's HTML-to-text step: documents that open `<head>` and never close it, which HTML
allows. The round-29 tool drops every byte after `<head>` in such a document, so it reports
`ABSENT` for any body quote (S047 is one such registry page;
`.ufo/waves/round-29/falsify/CriticHeadOmission.md`). The command that shows the surface
unmoved is the C1 counter on the round-29 tool: it prints 78/106 at the base.

**Predicate (one sentence, frozen):** C1 holds iff
`python3 corpus/evidence/round30/c1-count.py`, run from the lane root, prints
`QUOTE_REOPEN_HEADLESS_MATCH=106/106`: every one of the 106 run-time items gets a verdict
equal to its construction label.

- Counter code: `holds = (n_ok == t == FROZEN_TOTAL)` with `FROZEN_TOTAL = 106` in
  `c1-count.py`.
- Receipt label: `QUOTE_REOPEN_HEADLESS_MATCH`; receipt field `predicate_holds`.
- Before (round-29 tool at base, the do-nothing control): `QUOTE_REOPEN_HEADLESS_MATCH=78/106`,
  exit 1 (receipts `.ufo/waves/round-30/controls/before-c1-run{1,2}.json`). Every miss is
  a body window of a headless document (28 of 28).
- Target after: 106/106, exit 0, on the landed tool.
- Kill rule: any other value on the measured lane revision is a miss. A harness failure
  (exit 2) is a failed measurement; it is re-run, never scored as a pass.
- Items and classes: the `c1-count.py` docstring. 20 documents (5 head-and-body-tag,
  5 no-body-tag, 4 bare-text-after-head, 6 closed-head regression) with 5 items each:
  two body windows (VERBATIM), a title window, a script window and a case-flipped body
  window (ABSENT); plus 6 verdict-order items (TOO_LONG on an unreachable source,
  NO_SOURCE on over-long quotes, UNREACHABLE, TOO_LONG on a reachable source).
- D3: the script windows, case flips and verdict-order items are the fixture classes the
  spot-check routed (`round-29-verifier-spotcheck.md:151-153`). The round-29 mutants
  MutSkipScript, MutCasefold and MutOrder must each score below 106 on this counter; the
  falsify wave re-applies them to the landed tool and commits the receipts. That kill
  result is evidence for D3, not a second predicate.

**Sourced:** the HTML rule that a `head` end tag may be omitted, and that head content ends
at the first element that cannot be in `head`, is opened this round from a W3C HTML
specification page on `www.w3.org` (a registered host) and lands as a new `SOURCES.md` row
cited by `corpus/knowledge/quote-reopen-r30.md`.

## Claim C2 — operability: the fetch bounds the tool states hold under drip and rebinding

**Axis by surface:** operability, the lowest scored axis (SCORECARD.md line 7, score 3). The
surface is the fetch layer of `tools/quote-reopen.py`. Its docstring and the round-29
contract state "a 30 s total deadline per URL shared with the single retry" and that a host
resolving to a non-global address is refused. Neither statement holds at the base: a
server that drips bytes keeps a fetch open without bound (sentinel T4), and the tool
resolves the host a second time when it connects, so a host can pass the check with a
global address and then connect to loopback (sentinel T1;
`.ufo/waves/round-29/falsify/SentinelTool.md`). A command whose stated bound does not hold
does not produce its stated outcome. The command that shows the surface unmoved is the C2
counter on the round-29 tool: 13/27 at the base (design v3; 9/20 under v2).

**Predicate (one sentence, frozen, design v3):** C2 holds iff
`python3 corpus/evidence/round30/c2-count.py`, run from the lane root, prints
`QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`: every one of the 27 items gets a verdict equal to its
label, within its own DEADLINE plus 1.5 s of wall time, with no connection to an address
outside the validated set.

- Counter code: `holds = (n_ok == t == FROZEN_TOTAL)` with `FROZEN_TOTAL = 27`; an item
  matches iff `got == label`, `wall <= bound` (`bound = DEADLINE + SLACK`, `SLACK = 1.5`,
  each item's `DEADLINE` uniform in [2.0, 6.0] s, not killed at `CAP = 20`) and every logged
  connect destination is a routed global address of that item.
- Receipt label: `QUOTE_REOPEN_FETCH_BOUND_MATCH`; receipt field `predicate_holds`;
  receipt field `design: "v3"`.
- Before (round-29 tool at base): `QUOTE_REOPEN_FETCH_BOUND_MATCH=13/27`, exit 1, twice
  (receipts `.ufo/waves/round-30/controls/before-c2-v3-run{1,2}.json`). The drip-head and
  drip-body items are killed at 20 s; the rebinding items connect to 127.0.0.1 or 10.x; one
  drip-steady item overshoots its bound in run 1 and not in run 2 (the round-29 tool checks
  its deadline between 64 KiB reads).
- Target after: 27/27, exit 0, on the landed tool.
- Kill rule: as C1.
- Items: the `c2-count.py` docstring (drip-head, drip-body, drip-steady, stall-body,
  mixed-address, no-resolve, redirect-loop labelled UNREACHABLE; rebind-loop,
  rebind-private, rebind-redirect, stable, slow-ok, multi-address labelled VERBATIM or
  ABSENT by a fair coin per item).

**Sourced:** the Python documentation of socket timeouts on `docs.python.org` (a registered
host) is opened this round. It states the per-operation timeout semantics behind T4. It
lands as a new `SOURCES.md` row cited by the same knowledge entry.

## Separability

C1 changes only the HTML-to-text step; C2 changes only the fetch layer. The C1 counter
serves every page fast from one stable address, so C2's change cannot move it. The C2
counter serves one closed-head page shape, so C1's change cannot move it. The build lands
C2 first and C1 second as separate lane commits, and each counter is run on both
revisions.

## Tool contract v2 (changes to round-29 `claims.md` "Tool contract"; everything else stands)

1. **Head boundary (C1).** Content inside `head` is dropped. The head starts at a `<head>`
   start tag. It ends at the first of: a `</head>` end tag; a `<body>` start tag; any start
   tag other than `base basefont bgsound link meta noframes noscript script style template
   title`; or character data outside those elements that is not only whitespace (that data
   is page text). The content of `title`, `script`, `style`, `noscript` and `template` is
   dropped wherever it appears. The block-element list and every other rule are unchanged.
   HTML allows only text-dropping or empty elements in `head`, so a design that drops
   `title` content wherever it appears and ignores head boundaries yields the same text on
   every document the C1 counter generates. Such a design is an implementation of this
   item, not a control that skips it, and the control wave must not build it.
2. **Total deadline (C2).** `DEADLINE` (module constant, seconds, default 30) bounds the
   whole fetch of one registry URL: every redirect hop, header read, body read and the one
   retry. When it passes, the fetch stops and the item is `UNREACHABLE`. A slow but steady
   sender cannot extend it.
3. **One resolution (C2).** Each hop's host is resolved once. If any returned address is not
   global, the hop is refused (`UNREACHABLE`). Otherwise the connection goes to one of those
   validated addresses, and the host name is still used for the `Host` header and for TLS
   (SNI and certificate check). The tool never resolves the name again for that hop and
   never checks the address only after connecting.
4. The tool still exposes `main(argv)` and `DEADLINE` at module level (the harness imports
   it).

## Not claimed

Liveness: neither counter shows that the tool reaches the real network; both run on
loopback. Pages that omit the `<head>` start tag itself, 2xx challenge pages (S021, S022),
PDF sources, prefix and suffix disambiguation and pages rendered by JavaScript stay out of
scope. Whether a quote supports a claim or a source is true is never claimed. The round-1
operability score stays 3 on its scale; C2's observable sits beside it.

## Pre-freeze controls (filled by the control wave before data)

Receipts: `.ufo/waves/round-30/controls/<Control>/receipt*.json`, each carrying the counter
and harness SHA-256. Expected ceilings, before scoring:

| control | what it skips | C1 ceiling | C2 ceiling |
|---|---|---|---|
| do-nothing (round-29 tool) | the whole round | 78/106 (measured) | 9/20 (measured) |
| tool absent | everything | 0/106 | 0/20 |
| always-ABSENT (all-false) | reading and judging | below 106 | below 20 |
| always-VERBATIM | reading and judging | below 106 | below 20 |
| always-UNREACHABLE, fast | fetching | below 106 | 10/20 |
| junk verdicts | everything | about 1/5 | about 1/5 |
| no-reader (never fetches) | fetching | below 106 | below 20 |
| raw-grep shortcut (substring over raw HTML) | parsing | below 106 | n/a |
| skip-nothing (drop `head` from the skip set) | the head rule | below 106 | n/a |
| tiny deadline (0.5 s) | the bound | n/a | below 20 |
| refuse-on-rebind (refuse when lookups differ) | contract item 3 | n/a | below 20 |
| item-shape keyed shortcut (verdict from quote shape: capitals, length) | reading | below 106 | below 20 |
