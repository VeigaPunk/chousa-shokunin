# ScribeQuality64 — ground/plumbing tag proposal grounded through rounds 35–44

## Item
Ground the operator proposal "Tag each round as research ground or plumbing"
(`chousa-shokunin/considerthese/2026-10-24.md:58`, section "Self-improvement proposals
(not acted on)"; doc dated 2026-10-24) through the lane's bar: read each round 35–44
claim in `chousa-shokunin/SCORECARD.md` verdict sections, classify as `ground` or
`plumbing` with the evidence line, give per-round ratios, and draft QUALITY.md criterion
64 (style of 62/63).

## Classification rule (applied)
- `ground` = the claim adds research coverage: admits a source opened that round on a
  subject OUTSIDE the lane's own tooling, or a knowledge entry on such a subject.
- `plumbing` = the claim hardens the lane's own tool/gate/counter/receipt/registry.
  Sources opened solely to support that work (man/info pages for pin design, capture-form
  rows, registry supersede rows) and knowledge entries recording tool mechanics count as
  part of the plumbing claim, not as separate ground. This follows the calibration note
  in `considerthese/2026-10-24.md:50-54`: "research reach, meaning new sources and
  knowledge on new subjects".

## Table (Claim = SCORECARD.md verdict row; evidence = before → after line)
| R | Claim (row) | Class | Evidence line |
|---|---|---|---|
| 35 | C1 operability, grep pin (1995) | plumbing | `GREP_PIN_MATCH=0/9`→`9/9` (gate `a47688518e…f0c38ad`); S067/S068 opened as pin-design support |
| 35 | C2 calibration, routing witness (1996) | plumbing | `WITNESS_SEPARATED=0/2`→`2/2` (`tools/mechanism-witness.py`; knowledge keyed-engine-output-equivalence-r35.md) |
| 36 | C1 operability, engine-swap canary (2045) | plumbing | `ENGINE_SWAP_CANARY=10/14`→`14/14` (knowledge engine-swap-canary-r36.md; S069/S070 opened as tool-design support) |
| 36 | C2 calibration, per-record attribution (2046) | plumbing | `WITNESS_PER_RECORD=2/5`→`5/5` (`tools/argv-witness.py`; knowledge per-record-argv-attribution-r36.md) |
| 37 | C1 operability, claim-pin provenance (2088) | plumbing | `CLAIM_PIN_PROVENANCE_MATCH=2/7`→`7/7` (knowledge claim-pin-provenance-r37.md; claim text falsified via LD_PRELOAD) |
| 37 | C2 freshness, pin-capture env (2089) | plumbing | `PIN_CAPTURE_ENV_MATCH=3/7`→`7/7` (S071 mechanism source pinned; knowledge pin-capture-env-r37.md) |
| 38 | C1 operability, env-pin capture (2151) | plumbing | `ENV_PIN_CAPTURE_MATCH=2/7`→`7/7` (knowledge env-pin-capture-r38.md) |
| 38 | C2 calibration, receipt binding (2152) | plumbing | `RECEIPT_BINDING_MATCH=0/7`→`7/7` (knowledge receipt-binding-r38.md; verifier binding) |
| 39 | C1 operability, capture bash pin (2217) | plumbing | `ENV_PIN_CAPTURE_MATCH=7/8`→`8/8` (knowledge capture-bash-pin-r39.md; S071 re-opened) |
| 39 | C2 calibration, verifier/subject binding (2218) | plumbing | `RECEIPT_BINDING_MATCH=8/8` (verifier_sha256 + subject_counter_sha256; knowledge receipt-verifier-subject-r39.md) |
| 40 | C1 operability, receipt evidence integrity (2268) | plumbing | active receipts `3/6`→`6/6` verify (knowledge receipt-expectation-digest subground; S059 re-opened/used-by updated) |
| 40 | C2 calibration, R2–R5 disposition alignment (2269) | plumbing | evidence-backed dispositions `0/4`→`4/4` |
| 41 | C1 operability, canonical-capture invocation surface (2286) | plumbing | `CAPTURE_PIN_MATCH=1/12`→`12/12` (knowledge capture-path-pin-r41.md; S075/S076 opened as invocation-pinning subground — tool subject) |
| 41 | C2 calibration, W04 duplicate-URL disposition (2287) | plumbing | `W04_DISPOSITIONED=0/5`→`5/5` (registry semantics; S073/S074 are registry rows) |
| 42 | C1 operability, quarantine-scope command (2313) | plumbing | `SLICE_REDERIVE_MATCH=24/24` (`tools/quarantine-check.py`; S077 opened as capture-form ground — tool subject) |
| 42 | C2 calibration, slice adjudication (2314) | plumbing | `VERDICTED=24/24`, `CLASS_CONSISTENT=24/24` |
| 43 | C1 operability, absent-class split (2361) | plumbing | `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15` |
| 43 | C2 calibration, split agreement (2362) | plumbing | `SPLIT_AGREES=15/15` |
| 43 | C3 depth, search-log source (2363) | ground | entry cites S078, quote in committed capture, row URL matches (S078 opened from a committed capture; a search-log fact the lane did not hold) |
| 44 | C1 operability, launcher receipt (2387) | plumbing | `N_SPAWNED=64/64`, `N_REAPED=64/64` (`tools/parent-lifetime.sh`) |
| 44 | C2 calibration, inherited-tree sweep (2388) | plumbing | `CONSISTENT=39/39`, `REVERIFIED=36/36`, `LEFT_NAMED=3/3` |
| 44 | C3 depth, citation-to-prior-state binding (2389) | ground | entry cites S079; S079 row URL = RFC 7089 URL; located quote in that URL's committed capture (two entries, three mined rows on Memento/WARP/timestamped-URL theme) |

## Per-round ratio
| Round | ground | plumbing | ratio |
|---|---|---|---|
| 35 | 0 | 2 | 0/2 |
| 36 | 0 | 2 | 0/2 |
| 37 | 0 | 2 | 0/2 |
| 38 | 0 | 2 | 0/2 |
| 39 | 0 | 2 | 0/2 |
| 40 | 0 | 2 | 0/2 |
| 41 | 0 | 2 | 0/2 |
| 42 | 0 | 2 | 0/2 |
| 43 | 1 | 2 | 1/3 |
| 44 | 1 | 2 | 1/3 |
| total | 2 | 20 | 2/22 |

The data confirms the proposal's premise: rounds 35–41 are 100% plumbing (the "seven
rounds in a row" of the calibration note); the first ground claims are rounds 43/44 C3.

## Draft QUALITY.md criterion 64 (appended after 63; style of 62/63)
64. **Every round verdict tags each claim as research ground or plumbing.** A claim adds
    research coverage (`ground`) when it admits a source opened that round on a subject
    outside the lane's own tooling, or a knowledge entry on such a subject; it hardens
    the lane's tools (`plumbing`) when it changes a gate, counter, receipt pipeline or
    registry mechanism — even when sources were opened to support that work. Each claim
    row in the round's `SCORECARD.md` verdict table ends with a `ground` or `plumbing`
    cell. Check: `python3 corpus/evidence/round45/q64-count.py --scorecard
    SCORECARD.md` prints tagged/untagged claim rows and exits 0 only when every claim
    row of round ≥45 carries the cell and every `ground` cell names a source row opened
    that round whose topic is outside the lane's tooling. Shown able to fail: the
    committed rounds 35–44 rows carry no tag → `TAGGED=0/22`, exits 1
    (`SCORECARD.md:1995-2389`); history stays untagged and the rule binds forward. A
    false `ground` cell also fails: round-41 C1's S075/S076 are invocation-pinning
    subground opened for the capture tool, so tagging that row `ground` would misread
    the round. Operator proposal mined from `considerthese/2026-10-24.md`
    (2026-10-24), "Tag each round as research ground or plumbing". —
    `lessons/round-44.md`.
(Note: `q64-count.py` does not exist — the check line is draft text; a counter with
do-nothing/false-tag controls must be built and frozen before criterion 64 is admitted.)

## Commands run (verbatim, decisive lines)
- `read chousa-shokunin/considerthese/2026-10-24.md` — proposal text at line 58; the
  calibration note at lines 50-54.
- `read chousa-shokunin/corpus/QUALITY.md` — criteria 62/63 at lines 556-579.
- `wc -l SCORECARD.md` → `2406`.
- `grep -nE '^\| (C1|C2|C3) ' SCORECARD.md` — claim rows at lines 1995/1996 (r35),
  2045/2046 (r36), 2088/2089 (r37), 2151/2152 (r38), 2217/2218 (r39), 2268/2269
  (r40), 2286/2287 (r41), 2313/2314 (r42), 2361-2363 (r43), 2387-2389 (r44).
- `read SCORECARD.md:1983-2406` (raw ranges) — full verdict sections for rounds 35-44.
- `grep -n -i -E 'ground|plumbing|tag each round|research reach' corpus/lessons/round-44.md`
  — no prior handling of the proposal (one unrelated "ground" hit at line 67).
- `mkdir -p .ufo/waves/round-45/w1` — report directory.

## Verdict
Proposal implementable as criterion 64; the round ledger (above) is the tag column the
proposal asks for. The ratio classification is my reading of the scorecard evidence;
borderline source openings (S071, S075/S076, S077, S059 re-open) are counted as
tool-support per the calibration note's "new subjects" phrasing. No production file was
touched, no tool installed, no fetch performed; the only write is this report.
