# Round 29 — planning data-walk (connector seat)

Seat `ChousaR29.ConnectorPlanWalk`, connector role carrying the bounded planning
data-walk for the L1's §3 planner seat (no `planner` seat was spawned; this is
the mapping the round report must record). Design revision under test:
`12244431d636bfa615d7e8d3a0a48b85b3cba06f` (design v2, frozen).

Date basis: the frozen claim file, the before receipt and every control receipt
stamp UTC (`at` fields end in `Z`). At probe time the local clock read
2026-10-22 22:24 -03:00, which is 2026-10-23 01:24 UTC. One basis must be named
once in the round lesson, or a closure reading 2026-10-22 mtimes against
2026-10-23 rows will call the dates future-dated.

Machine-readable probe: `.ufo/waves/round-29/build/ConnectorPlanWalk/pre-data-probe.json`
(frozen-counter SHA-256, item-set arithmetic, live reachability of the 8 registry
URLs, and the 45 control receipts). No tool was installed or updated; no scratch
directory was used, because every probe was either a read-only import of the
frozen counter or a bounded GET to a registry URL.

## 1. What I ran

| # | command (lane root) | observed |
|---|---|---|
| 1 | `sha256sum corpus/evidence/round29/c1-count.py` | `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd` — equals `counter_sha256` in `before-do-nothing-v2.json` and in all 25 v2 control receipts |
| 2 | python import of the frozen counter + its own `load_tsv`/`registry_url` | 40 items, 40 labels, class counts exactly as the frozen table (9 + 3 + 2 VERBATIM, 3 TOO_LONG, 3 NO_SOURCE, 19 ABSENT); `vsrc` = `S002 S003 S008 S013 S019 S020 S038 S044` = 8 ids; projected page items 48; **projected total 130 = FROZEN_TOTAL** |
| 3 | live probe with the counter's own `fetch_text` and its exact User-Agent | all 8 URLs: status 200, `text/html`, 2 205 to 119 650 bytes, 0.0 to 1.6 s, token counts 393 to 25 125 — no UNREACHABLE class, far under the 8 MiB cap |
| 4 | `grep -cE "html\.parser\|HTMLParser\|urllib\|http\.client\|unicodedata\|NFKC" tools/research-gate.sh` | `0` — the existing gate has no fetch, no HTML-to-text and no Unicode normalization |
| 5 | `grep -nE "isalnum\|verbatim\|token boundar" tools/research-gate.sh` | lines 234, 1267, 1281: `tok_left_ok` / `tok_right_ok` — the token-boundary match rule already exists in the gate |
| 6 | `ls -la tools/` | only `research-gate.sh` (288 151 bytes) — the claimed command is absent at base |
| 7 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `45`; `S046` to `S049` do not exist |
| 8 | `ls corpus/knowledge/ \| grep -i quote`, `ls corpus/lessons/`, `grep -n "round-29" LOG.md` | no `quote-reopen-r29.md`, no `round-29.md` lesson, zero `LOG.md` round-29 lines |
| 9 | `grep -nE '^\| S(001\|045) \|' corpus/SOURCES.md \| grep -cE 'https?://'` | `0` — the two NO_SOURCE rows hold no URL in any cell, so that label survives even a whole-line URL scan |
| 10 | receipt scan over `.ufo/waves/round-29/controls/*/*.json` | 45 receipts: 20 v1 (`fc219ef8…`), 25 v2 (`574ffcad…`, every `total` 130). v2 scores: do-nothing 0, always-VERBATIM 52, always-ABSENT 72, id-keyed 72, no-reader 78, junk 30 / binary 63, raw-grep 100 and 99, casefold-no-boundary 126, label-keyed 106, **receipt-warmed label-keyed 130/130 on seeds 2901 and 2902** |
| 11 | `grep -oE '\b[a-z]+[0-9]{2,}\b' corpus/evidence/round29/claims.md` | only `r29` (twice) and `round29` (once) — path tokens, no run-together prose to route |

## 2. The five questions

**Axis named by the surface it changes — yes.** The claim names the surface
(`tools/quote-reopen.py`, a new runnable command) and the axis by that surface,
not by a number. The score row is explicitly left at 3 with the new observable
reported beside it. Measured basis for "new surface": `ls tools/` (row 6) holds
only `research-gate.sh`, and the gate's own symbol sweep (row 4) is 0 for fetch,
HTML parsing and normalization.

**Lowest scored non-retired axis — yes.** `SCORECARD.md:7` is the only scored
axis row: operability, 3, last-change round 1. `## Retired` (line 32) records
none, and the five other axes are deliberately unscored, so the lowest-axis
obligation stands and the stagnation nudge stays dormant (its condition 1 fails
at line 486). Rotation caveat: operability has now been the claimed axis in
rounds 27, 28 and 29. The defense is the surface delta — round 28 claimed the
gate's ancestor/denylist behavior, round 29 changes no gate byte and adds a
second command. That sentence belongs in the round report, with the gate
SHA-256 before and after as its receipt.

**Sourced-claim requirement — not met yet, and cheaply closable.** The frozen
file says the fixture quotes come from rows `S002`, `S003`, `S008`, `S013`,
`S019`, `S020`, `S038` and `S044`, re-opened for the fixture, and that the rows
the tool's normalization rests on are opened in wave 1. Two constraints decide
this: the registry is append-only, so a re-open cannot rewrite an `opened` cell
(it may only change `status`, `recheck`, `used-by`, each logged old to new in
the lesson); and the round requirement is a claim resting on a row *opened this
round*. So the closure is: write `S046` to `S049` this round, give each a
located quote of at most 25 words with its URL and access date in the lesson's
`## Gate`, cite at least one of them from `corpus/knowledge/quote-reopen-r29.md`
with the provenance trio, and log the 8 re-opens as `used-by` changes. Without
new rows the claim is sourced from rows whose `opened` cells read 2026-10-19 and
2026-10-21, which a strict closure reads as "no row opened this round".

**Universal clause without a full-set enumeration — none inside the predicate;
two outside it.** The predicate's universal is enumerated: the counter derives
`t = len(cases)` from the constructed list and compares `n == t == FROZEN_TOTAL`,
and the arithmetic closes at 40 + 42 + 48 = 130 (row 2). Two negative claims in
the same file carry no sweep: "it does not touch `tools/research-gate.sh`" needs
`sha256sum` of the gate before and after plus `git diff --name-only` over that
path, and "the lane has no such command at the base" needs the `tools/` listing
(row 6) pasted into the report. Both are one-line receipts and both are cheap
insurance against a no-harm challenge.

**Re-score of a rule the lane already holds — partly, and not fatal for
operability if it is recorded as what it is.** The match rule (verbatim span,
token boundary, 25-word cap) already exists in the gate (row 5), and round 2
already landed in-corpus claim-vs-source verification. What is new is live
registry-URL fetch, HTML-to-text with the fixed block list, and Unicode
normalization — all absent from the gate (row 4). That makes the move a
capability acquisition, which `AXES.md` §Capabilities admits independently of
the axis score. It would become fatal in two shapes: recording it as a
depth/coverage gain from re-deriving boundary semantics (the claim-sizing rule
calls that quality work, never coverage or depth), or raising the operability
score on an observable the gate already produced. The capability row must name
the fetch/extract/normalize delta, not "verifies quotes".

## 3. What SCORECARD and the capabilities table must record after data

- A `## Round 29 verdict` section: claim type **capability acquisition**, axis
  **operability**; before `QUOTE_REOPEN_MATCH=0/130` (receipt
  `before-do-nothing-v2.json`, seed 2901, tool exit 2, `predicate_holds` false);
  after the measured value with the counting command verbatim and the **branch
  tip** (not bare `HEAD`) it was measured at.
- `operability 3 → 3, delta 0`, re-derived by the round-1 counting command, with
  the new observable beside it — the pattern round 24 already used.
- The per-class receipt table (all 16 classes with n/n), because the sharpest
  question a closure asks is which classes discriminate.
- The control table with the receipt-warmed row disclosed (see §5), and the
  per-class receipts as the answer to "what does the 126-item residue measure".
- No-harm evidence: gate SHA-256 before and after, `git diff --name-only` over
  `tools/research-gate.sh` empty, and the gate's own selftest or drift arm green.
- A new `## Capabilities (round-29 addition)` table (the lane's append-only
  convention at lines 1272, 1325): name → what it can now do (re-open a located
  quote against the live registry URL: GET, HTML-to-text, normalization,
  boundary-scoped verdict) → evidence pointer (the predicate command and the
  after receipt, plus `corpus/knowledge/quote-reopen-r29.md`) → first-working
  round 29. `## Retired` and the saturation line (8.0, window 3) stay unchanged,
  and the round-30 `## Planned` row is written.
- `LOG.md` round-29 opening and landing lines; `corpus/lessons/round-29.md` with
  `## Gate` (the 8 re-opens logged old to new, the 4 new rows with URL, access
  date and located quote) and `## Mistakes` (one mined mistake whose fix is
  shown able to fail).

## 4. Risks the closure would flag

1. **The frozen void rule is already tripped in letter** — §5 below. Disclose
   before the data seat; never re-scale.
2. **Seed contamination of the after measurement.** `receipt-v2-warmed.json`
   reaches 130/130 by replaying labels from same-seed receipts. Pinning the
   after run to seed 2901 or 2902 hands the same shortcut the same answers. Run
   the predicate command **unseeded** (its default is a fresh 32-bit seed), and
   never re-run an already-published seed as evidence.
3. **Timeout pairing.** The tool's worst case is 8 URLs × 2 attempts × 30 s =
   480 s; the counter's candidate timeout defaults to 900 s. A seat that copies
   the control-wave habit of `--timeout 90` converts one slow page into a scored
   miss. Use `--timeout 480` with an outer bound near 590 s, and record `wall_s`.
4. **Sourced-claim gap** — no `S046` to `S049`, no knowledge entry, no lesson, no
   round-29 `LOG.md` line exists yet (row 8).
5. **Two unswept negatives** in the frozen file (gate untouched; command absent
   at base) — see §2.
6. **Re-score framing** — the capability row must carry the fetch/extract/
   normalize delta, and the axis row must not move.
7. **Date basis** — one basis, stated once; UTC matches the frozen stamps.
8. **Fetch authority.** The lane's mission line forbids external live-target
   fetches without operator approval, while C1 requires 8 registry URLs to be
   fetched. The operator's wave contract for this round authorizes GET to the
   `source` column URLs of `corpus/SOURCES.md` — exactly the fetch set — so the
   report should cite that authorization and the bounds (GET only, registry
   scope, 30 s timeout, no credentials) rather than leave the apparent conflict
   unaddressed.
9. **Discriminating power is concentrated.** The casefold-no-boundary control
   scores 126/130, losing only the 4 `absent-truncated-token` items; raw-grep
   reaches 100/130 and the committed-bytes label cheat 106/130. The predicate is
   therefore sharp against fetch-skipping and raw-HTML cheats, and its boundary
   edge rests on 4 of 130 items. Report the class table instead of implying the
   130 items are uniformly discriminating.
10. **Prose hygiene** — new text must separate digits from words and avoid the
    custody vocabulary the round-28 spot-check routed as defects; the round-28
    SCORECARD tail still carries some of that wording, which is pre-existing and
    not this round's to rewrite.

## 5. Contradiction, stated not smoothed

`claims.md` freezes this rule: "Any control that reaches 130/130 voids v2 too:
C1 would then be declared exploratory, never re-scaled." The control wave has
already produced two receipts at exactly 130/130 against the current counter
(`CtlLabelKeyed/receipt-v2-warmed.json` seed 2901, `receipt-v2-warmed-seed2.json`
seed 2902, both `predicate_holds: true`), and a third at 106/130 on a fresh
unseen seed (`receipt-v2-warmed-freshseed-L1.json`, seed 2848469338). The frozen
control table predicted 106/130 for that control and did not enumerate a variant
that reads prior receipts.

Two readings, both defensible, with different consequences:

- **Literal**: a control reached 130/130, so v2 is void and C1 must be declared
  exploratory. Consequence: no measured after value, and the round reports the
  capability as exploratory or does not land it.
- **Generalizing**: the 130/130 is same-seed answer replay that scores 106/130 —
  the same as the unchanged control — on an unseen seed, so the shortcut does
  not generalize and the frozen target still separates a real re-opener from a
  cheater. Consequence: the measurement stands, with the warmed receipts
  disclosed beside it.

This seat cannot rule on that and will not smooth it. The frozen file cannot be
edited, and a rule re-read after a seat has scored is not the claim's rule. The
clean path is to publish both readings with the three receipts and route the
question to the operator, then run the data seat unseeded so the measured value
is not the one the warmed shortcut already holds.

## 6. Proposed move (one, bounded)

Before the data seat runs, land a **measurement-protocol receipt** as the
round's first artifact: (a) the three warmed-control receipts named above with
their seeds and scores, plus the fresh-seed 106/130, published as a pre-data
disclosure block; (b) the after-measurement protocol fixed in writing — unseeded
run, `--timeout 480`, outer bound 590 s with a 5 s kill grace, one run, receipt
committed with its seed and `wall_s`; (c) the two unswept negatives turned into
one-line receipts (gate SHA-256 before and after; the `tools/` listing); and (d)
the item-set arithmetic 40 + 42 + 48 = 130 recomputed from the frozen counter's
own loaders and pasted. Affected axes: operability (the measurement is valid
rather than merely green), freshness (the after receipt is live-page evidence),
calibration (a control that met the frozen target is disclosed by the lane
instead of found by the closure). No axis is harmed: no production file, no
frozen byte and no gate byte changes, and the move is one committed evidence
file plus a few report lines.

Verification of the move: `python3 -c` recomputation of the item-set arithmetic
prints 130; the disclosure block names three receipt paths whose `match`/`total`
fields read 130/130, 130/130 and 106/130; the gate SHA-256 is identical before
and after; and the after receipt's `seed` is absent from the set of seeds named
in the disclosure block.

## 7. Limits

I did not run the candidate tool (it does not exist), did not re-run the
counter, and did not open the pages beyond one bounded GET per URL for
reachability and content type. The class-level scores I quote are read from the
committed control receipts, not re-measured here. The two readings in §5 are
both derived from committed bytes; the ruling between them is the operator's,
not this seat's. Reachability was measured twice with the same result, but a
page can change after this probe — that is the freshness risk the live-page
items carry by design.

Report: .ufo/waves/round-29/build/ConnectorPlanWalk.md
