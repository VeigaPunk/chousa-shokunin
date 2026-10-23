# C1 shortcut controls — round 31 (seat CtlShortcutC1)

Scope: C1 counter only. Ten gate substitutes that **read the sources** but implement the
line check wrongly or cheaply, each scored on three fresh seeds. No lane file edited, no
network, no tool installs. Sandbox: `/fast/scratch/hyaku/chousa-r31/CtlShortcutC1/`.

## Pinning (matters for the whole wave)

While this seat ran, other seats were rewriting the lane files in place:

- `corpus/evidence/round31/c1-count.py` — frozen at d78d188: 253 lines, sha256
  `154e09e7f73b…b555d`. Observed in the working tree mid-wave: 296 lines, sha256
  `c0a0908c88b9…28f56a` (extra `sub` variants in B1/B2).
- `tools/research-gate.sh` — frozen `ac1315ddaa12…35765`. Observed in the working tree
  mid-wave: a version that calls an undefined `line_range_ok` (`line 1442: command not
  found`) and emits `observed=mislocated`/`invalid`.

Every receipt below was produced with **sandbox copies of the frozen files**:
counter `154e09e7f73b…`, gate `ac1315ddaa12…`; each receipt's `counter_sha256` confirms
it. A receipt carrying `counter_sha256=c0a0908c…` did not run the frozen counter.

Harness validation: the controls' shared base layer (delimiter classes from
`tok_left_ok`/`tok_right_ok`, span-absent → `unsupported`, absent `"line"` → unchanged)
reproduces the frozen gate's **120/120 CLAIM lines byte-identically** on a frozen fixture
(seed 931000; `harness-base-keep-931000.json`, 50/120). Control scripts are
self-contained (bash + embedded Python); each receipt's `gate_sha256` covers the whole
control, not just a wrapper.

## Controls, counter, seeds, scores

Counter: frozen `c1-count.py` (`154e09e7…`). Seeds 931011 / 931012 / 931013 (fresh;
931000 was the harness fixture). Receipts: `CtlShortcutC1/<control>-seed<seed>.json`.

| control | shortcut rule (sources read; base occurrence check kept) | scores | receipt |
|---|---|---|---|
| `first-occ` | bind only the **first** boundary-delimited occurrence | 108 / 108 / 108 | `first-occ-seed9310{11,12,13}.json` |
| `raw-substr` | span is a raw substring of lines N..M (no token boundaries) | 105 / 105 / 106 | `raw-substr-seed9310{11,12,13}.json` |
| `first-token` | first span token delimited somewhere in lines N..M | 99 / 100 / 101 | `first-token-seed9310{11,12,13}.json` |
| `first2-token` | first two span tokens delimited somewhere in N..M | 99 / 100 / 101 | `first2-token-seed9310{11,12,13}.json` |
| `occur-in-file` | span occurs delimited anywhere **and** N..M inside the file | 68 / 68 / 68 | `occur-in-file-seed9310{11,12,13}.json` |
| `count-ge2` | ≥2 delimited occurrences ⇒ supported | 112 / 112 / 112 | `count-ge2-seed9310{11,12,13}.json` |
| `range-ignored` | `"N-M"`: check only the start line N, ignore the end | 117 / 116 / 117 | `range-ignored-seed9310{11,12,13}.json` |
| **`endpoint-exact`** | **first token line == N and last token line == M (no occurrence needed)** | **120 / 120 / 120** | `endpoint-exact-seed9310{11,12,13}.json` |
| `endpoint-contain` | first and last token delimited somewhere in N..M | 117 / 117 / 118 | `endpoint-contain-seed9310{11,12,13}.json` |
| `line30-leak` | named line > 30 ⇒ mislocated, else base result (fixture statistic) | 67 / 67 / 66 | `line30-leak-seed9310{11,12,13}.json` |

`endpoint-exact` receipts: `matched=120`, `predicate_holds=true`, `misses=[]`, all twelve
classes 12/12 or 8/8, on all three seeds. (The control's own exit code is 1 because it
compares to `expect=supported`, which is constant; the counter only needs 0 or 1.)

## Findings

### F1 — 120/120: endpoint-only binding without any occurrence (design-breaking)

Rule: `supported` iff the span's **first** token occurs boundary-delimited on line N and
its **last** token occurs boundary-delimited on line M (single-line value: both on N),
after the base check that the span occurs somewhere. It never requires the span's
interior to sit contiguously at N..M, and it pairs the two token positions independently.

Why the frozen fixture cannot see it — **the exact leak**: no mislocated class produces
an endpoint coincidence while the span is absent from the named lines.

- `M1`, `M5`, `M6`: the named line holds **no** span word (words are globally unique, see
  F3), so both endpoints are absent.
- `M2`: glue hits **exactly one** endpoint (prefix-glue glues the first token, suffix-glue
  the last), so the other endpoint line check fails.
- `M3`: places only a **prefix** of ≥2 words; `k = rng.randint(2, len(words)-1)` guarantees
  the last token is never on the named line.
- `M4`: all four wrong-range shapes are caught (`start`/`wide` keep N but move the end;
  `end`/`late` move the start), so it scores 8/8.
- `U1`: the full span is absent **everywhere**, so the base check short-circuits to
  `unsupported` before any line check.

The missing shape is: *first and last token at exactly the named start/end line, interior
missing/substituted/reordered, true delimited span elsewhere.* Counterexamples (artifact
`CtlShortcutC1/leak-demo/`, outputs in `demo-output.txt`; contract truth recomputed with
the same delimiter code and confirmed by hand):

| record | named | contract (frozen C1) | `endpoint-exact` |
|---|---|---|---|
| `demo-a` (interior word substituted on line 2; span on line 4) | `"2"` | `mislocated` | **`supported`** |
| `demo-b` (first token line 2, last token line 4, span only on line 5) | `"2-4"` | `mislocated` | **`supported`** |
| `demo-c` (real 2-line span on 4-5, named wide 4-7) | `"4-7"` | `mislocated` | `mislocated` |

The frozen base gate prints `supported` for all three, but that is the already-declared
base gap; `endpoint-exact` is a *binding* implementation that still gets them wrong, so
P1 would mark C1 "met" for a tool that violates the contract.

Second-order: `endpoint-contain` (last token merely somewhere in N..M) scores 117–118 —
it misses only the 2–3 `M4` wide items.

### F2 — 116–117: start-line-only check (`range-ignored`)

`M4` has eight items over four wrong-range shapes. `start` (single value N) and `wide`
(N-M with M too large) keep the **true start line**; `end`/`late` move it. A check that
compares only the start line passes every `start`/`wide` item drawn in a seed (3, 4, 3 of
the 8 here) and fails the rest: 117/116/117. Demo `demo-c` is the violation: occurrence
4–5, named 4–7 → contract `mislocated`, `range-ignored` `supported`.

### F3 — distribution observations (no pass, but they feed F1/F2)

- `Gen.used` makes **every word unique across the run**. A span token's occurrence lines
  are therefore exactly its placement — token-position shortcuts get a noise-free signal.
  This is what makes `endpoint-exact` exact; it is not a leak by itself.
- File line counts are `randint(14,30)` and `M5`'s named line is `n + randint(1,40)`, so
  ~80% of the six `M5` items have named > 30: a no-reader ">30 ⇒ mislocated" rule banks up
  to 6 without opening a file (`line30-leak` 66–67 total, including invalid detection).
  A "named > line count" test is the correct rule, so this is cosmetic.
- Span shapes carry no class signal: on the seed-931000 fixture span lengths are
  4/5/6/7 words = 31/19/31/39, spread across every class.
- Range widths do not separate: valid width-1 ranges are 14 items (12 `B3` bound + 2
  `M4` late), width-2 ranges 1 item (`M4` wide), the rest single values. The two invalid
  values that *look* like ranges are exactly width −2 (`5-3`) and width 0 (`4-4`), i.e. the
  grammar's `M > N` arms; a width-only rule has no usable split.
- The 12 invalid values are each used once per run (shuffled round-robin), but the value
  grammar classifies them exactly; hardcoding the list buys nothing over validating the
  field, which the contract requires.

### F4 — what the design already tolerates

`count-ge2` = 112 (misses `M6` only). With class sizes 12/8/6, a shortcut that misses one
whole class scores 108/112/114, so 112 is the frozen design's own ceiling for
whole-class misses — useful context for judging the fix margin below.

## Smallest safe correction (v2; pre-data, predicate and TOTAL untouched)

Two class edits, no gate change, no count rebalance (12 items stay 12):

1. **Split `M3_partial_on_named_line` 4 + 8**: keep 4 prefix items; add 8
   `M3b_interior_damaged_endpoints_intact` — the named line holds the span's first **and**
   last token while a middle word is substituted (4) or the middle two are reordered (4),
   with the true delimited span placed on another line. Truth `mislocated`.
   ```python
   if cls == "M3b_interior_damaged_endpoints_intact":
       L, O = rng.sample(range(n), 2); put(L, span)
       words = span.split(" ")
       if rng.random() < 0.5:
           mid = rng.randrange(1, len(words) - 1)
           damaged = words[:mid] + [gen.word()] + words[mid+1:]
       else:
           damaged = list(words); damaged[1], damaged[2] = damaged[2], damaged[1]
       lines[O] = gen.word() + " " + " ".join(damaged) + " " + gen.word() + "."
       return lines, span, str(O + 1)
   ```
2. **`M4` shapes: `{"start","wide"}` only** (every item keeps the true start line and
   gets a wrong/absent end). `end`/`late` duplicate the wrong-start-line coverage of
   `M1`/`M6`.

Simulated with a sandbox copy of the frozen counter (`c1-count-v2sim.py`, sha256
`48a907aa02ff…3db19`; not the frozen counter, not a lane edit), seeds 931011–13:

| control | frozen | v2sim |
|---|---|---|
| `endpoint-exact` | 120 / 120 / 120 | **112 / 112 / 112** (all 8 misses in M3b) |
| `range-ignored` | 117 / 116 / 117 | **112 / 112 / 112** (all 8 in M4) |
| `endpoint-contain` | 117 / 117 / 118 | 108 / 106 / 109 |
| `count-ge2` | 112 / 112 / 112 | 112 / 112 / 112 |
| `first-occ` | 108 / 108 / 108 | 108 / 108 / 108 |
| other five | ≤ 106 | ≤ 105 |

Max across all ten controls after the two edits: **112/120**, below the 115 bar. Checks on
the v2sim: do-nothing base stays **50/120** on all three seeds; the hidden truth still
equals the contract's own judgment on every seed (bound 36 + no-line 6 = 42 supported,
mislocated 58, invalid 12, absent 8). Residual: 112 is the arithmetic ceiling for a
shortcut that misses exactly one 8-item class; to go lower, grow M3b/M6 (needs rebalance).

## Artifacts

- Gates (sandbox): `g-<mode>.sh`; sha256 in receipts, e.g. `endpoint-exact`
  `d1193ff540be…a62b6`, `range-ignored` `68ee6a7319d1…fd9823`.
- Frozen copies: `c1-count-frozen.py` `154e09e7…`, `base-gate-frozen.sh` `ac1315dd…`.
- Counterexample: `.ufo/waves/round-31/controls/CtlShortcutC1/leak-demo/` (`claims.jsonl`,
  `src/demo-{a,b,c}.md`, `demo-output.txt`).
- Simulation: `c1-count-v2sim.py` `48a907aa…`, sim receipts/logs in the sandbox only.

## Verdict

**design broken**: the frozen C1 counter admits a **120/120** shortcut
(`endpoint-exact`: first/last span-token line equality, no occurrence of the span) on three
fresh seeds with zero misses, because no mislocated class keeps both endpoints on the named
lines while the span is absent there; and a second shortcut (`range-ignored`, start line
only) scores 116–117 because only half of `M4`'s items keep the true start line. Adding the
8-item endpoint-intact interior-damaged class and making every `M4` item keep the true start
line drops the maximum of all ten controls to 112/120 with the predicate, TOTAL and the
do-nothing baseline unchanged.

## v2 re-score (commit `8070f92b…`, counter `c3aca35d…`)

Design v2 froze fixed sub-variants (M3 `prefix` 4 / `mid_sub` 4 / `mid_swap` 4; M4
`start`·`wide`·`end`·`early` ×2; B1 2/2/8; B2 6/3/3; M1 3+3/6; M2 6/6), the finding rule,
`CHOUSA_*` scrubbing and the duplicate-line rule; the gate is unchanged (`ac1315…`).

All twelve controls now print, for every claim they label `mislocated` (and only those),
`FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<id> at=<at> control=<mode>`;
the counter's `FINDING_RE` parses it. Harness: the v2 counter on the frozen gate still
gives **50/120** (seed 933011), and the controls' shared base layer reproduces the frozen
gate's 120 CLAIM lines byte-identically on that v2 fixture (B1 first/last-line, M3
mid_sub/mid_swap and M4 end/early included).

Counter v2 `c3aca35d…`; seeds 934011 / 934012 / 934013; receipts
`CtlShortcutC1/v2/<control>-seed<seed>.json`. **All 40 receipts in `v2/` carry
`counter_sha256=c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`**
(36 scored + 3 diagnostic + 1 harness).

| control | rule (sources read; base occurrence check kept; finding for own mislocated) | scores | receipt |
|---|---|---|---|
| `first-occ` | bind only the first delimited occurrence | 108 / 108 / 108 | `v2/first-occ-seed9340{11,12,13}.json` |
| `raw-substr` | span is a raw substring of lines N..M | 104 / 104 / 104 | `v2/raw-substr-seed9340{11,12,13}.json` |
| `first-token` | first span token delimited somewhere in N..M | 96 / 96 / 96 | `v2/first-token-seed9340{11,12,13}.json` |
| `first2-token` | first two span tokens delimited somewhere in N..M | 97 / 96 / 98 | `v2/first2-token-seed9340{11,12,13}.json` |
| `occur-in-file` | span occurs delimited anywhere and N..M inside the file | 68 / 68 / 68 | `v2/occur-in-file-seed9340{11,12,13}.json` |
| `count-ge2` | ≥2 delimited occurrences ⇒ supported | 112 / 112 / 112 | `v2/count-ge2-seed9340{11,12,13}.json` |
| **`range-ignored`** | **`"N-M"`: check only the start line N, end ignored** | **116 / 116 / 116** | `v2/range-ignored-seed9340{11,12,13}.json` |
| `endpoint-exact` | first token line == N and last token line == M | 112 / 112 / 112 | `v2/endpoint-exact-seed9340{11,12,13}.json` |
| `endpoint-contain` | first and last token delimited somewhere in N..M | 108 / 108 / 108 | `v2/endpoint-contain-seed9340{11,12,13}.json` |
| `end-only` | last token delimited on line M (single: N) | 102 / 102 / 102 | `v2/end-only-seed9340{11,12,13}.json` |
| `bag-of-words` | every span token delimited somewhere in N..M, order ignored | 112 / 112 / 112 | `v2/bag-of-words-seed9340{11,12,13}.json` |
| `line30-leak` | named line > 30 ⇒ mislocated, else base result | 66 / 68 / 68 | `v2/line30-leak-seed9340{11,12,13}.json` |
| *diagnostic* `endpoint-exact` **without findings** | same classifier, finding suppressed | 62 / 62 / 62 | `v2/_diagnostic-endpoint-exact-nofind-seed9340{11,12,13}.json` |

### What v2 fixed, and what it did not

1. **The v1 120 is closed.** `endpoint-exact` drops 120 → **112/112/112**. M3's
   `mid_sub` + `mid_swap` (8 items) keep both endpoint tokens on the named line, so the
   endpoint-pair binder misses all 8 and is now capped by class M3, not by luck.
2. **v2 still admits 116.** `range-ignored` (start-line-only) scores **116/116/116**.
   M4's eight items split 4 start-keeping (`start`, `wide`) + 4 end-keeping
   (`end`, `early`); a check that compares only N passes `start`/`wide` (prints
   `supported`, truth `mislocated`) and fails `end`/`early`. M4 is the *only* class that
   catches a start-only binder (M1/M5/M6 move the start line; M2/M3 break endpoints or the
   span), so the ceiling is 120 − 4 = 116. The mirror orientation is harmless: `end-only`
   = 102 (M2 `prefix` 6, M3 `prefix`+`mid_*` 12, M4 `end`/`early` 4).
3. `bag-of-words` = 112 (M3 `mid_swap` 4 — all tokens present, order ignored — plus M4
   `wide`+`early` 4). `count-ge2` 112 (M6). `first-occ` 108 (the named B2 occurrence is
   never the first). Everything else ≤ 108.
4. **The finding rule bites when ignored and is free when obeyed.** The same endpoint-exact
   classifier with findings suppressed scores **62/120** (all 58 mislocated claims fail),
   while emitting the finding for its own `mislocated` verdicts costs nothing: no shortcut's
   score changed relative to its observed classification. It forces the `CLAIM_LINE_MISMATCH`
   drift line, it does not make the line check harder — so the remaining leak is unchanged
   by it.

### Smallest safe correction (v2.1 — one line)

In `SUBVARIANTS`, `"M4_multiline_wrong_range": ["start", "wide"] * 4` (all eight items keep
the true start line). A start-only check then fails all 8 → 112; `end-only` stays 106 (it is
already caught by M2 `prefix` and M3 `mid_*`); every other control is unchanged. The
"named equals the true end line" shape disappears, but the end orientation is already tested
twice while the start orientation is tested only by M4.

Simulated with a sandbox copy of the v2 counter (`c1-count-v2sim2.py`, sha256
`afe30505…7d9`; one-line `SUBVARIANTS` edit, no lane edit), seeds 934011–13: max across the
twelve controls **112/120** on every seed (`range-ignored` 112, `endpoint-exact` 112,
`bag-of-words` 112, `count-ge2` 112, `end-only` 106, rest ≤ 108); base gate still 50/120;
labels unchanged (bound 36 + no-line 6, mislocated 58, invalid 12, absent 8).

**v2 verdict**: **still broken at 116/120** — start-line-only binding stays above the 115
bar because M4 keeps the true start line on only 4 of its 8 items; the one-line M4 change
(`["start","wide"]*4`) drops the maximum to 112/120 with the finding rule, the 50/120
baseline and the label counts untouched.
