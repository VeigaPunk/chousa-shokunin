# R82ExecTrial — end-to-end trial of the lane's method through the landed checklist

Seat: leaf executor, round 82 wave 1. No subagent, no network, no lane or fleet git mutation, no production edits.
Tree under test: `git archive b4a41d251b488f06b4a6ab01a11bc12ce72edd20` extracted to
`/fast/scratch/hyaku/chousa-r82/R82ExecTrial/tree` (deleted before yield). Scratch passed explicitly
(`TMPDIR`/`HYAKU_SCRATCH`), nothing written under `/tmp`. No tool installed or upgraded (pacman paused host-wide;
nothing was needed). Host sysctls and services untouched.

Artifacts (all under this folder):

| path | sha256 | what |
|---|---|---|
| `record.md` | `01c7916bc2446d17aff2184b5094cc792b2e0a3f0a41199dd5258d9a88ef0a3e` | the research record, record v1 grammar, written at `<tree>/corpus/evidence/round82/trial/record.md` |
| `trial-claims.jsonl` | `34fcf540e3ec7ec1e5616a08a34ae7ea87771d885290ca5ecf6514444dca6170` | claims companion for item 1, six observation claims, each with a `sha256` pin and a `line` |
| `twins/twin-rejection-flip-tbd.md` | `6e25c0bdad86856da6a2328247faf80dab5d317b1730541b7c79b3a52cc32578` | mutant 1: R1 `flip_condition` = `TBD` |
| `twins/twin-sweepcell-undeclared.md` | `71fa0784d0bad9a75909e232bf08676c600a3f78237566b2f156316146f5e57c` | mutant 2: N1 `sweep` = `W9` (undeclared) and SW1 `claim_id` = `N9`, so no row names N1 |
| `twins/twin-where-na.md` | `29f95992daf5c030edd80ebc9d3a1e81b0d807a1bdd9fc269c58fa77cc472bdc` | mutant 3: SW1 `where` = `N/A` |
| `twins/probe-flip-never.md` | `ae4311d9a42bae09ab8ec41b747f8ade368d6f79de440ccda4bcae8c9d6c145c` | fourth probe (not one of the three): R1 flip = prose "never: …", same meaning as `n/a` |

Receipts in `receipts/`. Paths inside receipts name the scratch tree, which is deleted; the tree is reproducible with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive b4a41d251b488f06b4a6ab01a11bc12ce72edd20 | tar -x -C <dir>`,
and the record/twins are copied here byte-identical.

## 1. The record answers the question

Question: *for a chousa record whose question maps what exists (not a test of an effect), what frame applies and what
must it keep separate?*

The record's answer, every row grounded in committed capture bytes:

- **Frame**: population, concept and context (PCC), stated as hypothesis-generating rather than hypothesis-testing
  (C4, C5 ← S210 `bcb4a695…`, capture lines 838). A PICO/PECO frame is admissible only when the map is a precursor to a
  structured effect question; the record cites that rule through the entry read for this trial, not through a quote it
  invents.
- **Keep separate** (three records, not one): the planned frame, which *is* the eligibility boundary (C1 ← S008
  `fd7eed5e…`:560); the question each planned synthesis answers (C2 ← :561); and the frame of what was actually
  investigated in the included sources, taken at the review stage (C3 ← :562). Plus observation vs the lane's inference
  (C7, kind=`inference`) and an explicit unknown (C8, kind=`unknown`: neither capture states a frame for a record whose
  unit is a claim rather than a study population).

`verify` tallies: `questions=1 sources=2 chains=5 claims=9 negatives=1 rejections=1 approvals=1`, CLEAN.

## 2. Every applicable Run line, from the tree root

All commands `cd <tree>` (lane root of the archive; the SKILL.md `--root ..` form has no fleet parent here, so `--root .`
is used and every pointer is lane-root-relative — a deviation from the literal line, recorded not hidden).

| item | command | observed line | rc | receipt |
|---|---|---|---|---|
| 1 | `bash tools/research-gate.sh verify-claims corpus/evidence/round82/trial/trial-claims.jsonl --root .` | `VERDICT_BEARING_CLAIMS=6/6`, `RESEARCH_GATE: CLEAN (claims=6 supported=6 … findings=0 drift=0)` | 0 | `receipts/run-1.txt` |
| 2 | `f=…/record.md; ! bash tools/research-gate.sh verify "$f" --root . \| grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1`, `RESEARCH_GATE: CLEAN (sweeps=1 verified=1 exempt=0 hit=0 … findings=0 drift=0)`, `compound_rc=0`; `verify` leg `NEGATIVE_WITHOUT_SWEEP` count = 0 | 0 | `receipts/item2-literal.txt` |
| 3 | `python3 tools/inference-ground.py --entry corpus/knowledge/question-framing-frames-r82.md --spans corpus/evidence/round46/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .` | `FINDING INF_SECTION_ABSENT bullet=0 token=''` / `GROUND: FAIL` | 1 | `receipts/run-3-item3.txt`, `receipts/run-4-item3b.txt` |
| 3 control | same line on `corpus/knowledge/evidence-pool-versioning-r39.md` (the entry whose quotes live in that spans file) | `GROUND entry=… section=1 bullets=4 tokens=7 grounded=7` / `GROUND: PASS` | 0 | `receipts/run-4-item3b.txt` |
| 4 | `bash tools/research-gate.sh verify-sweeps "$f" --root .` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1`, `RESEARCH_GATE: CLEAN (… rejections=1 rejections-ok=1 …)` | 0 | `receipts/run-2.txt` |
| 6 | `CHOUSA_GREP_PIN_ECHO=1 bash tools/research-gate.sh --selftest` | `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` (exact match to the SKILL.md pin) … `RESEARCH_GATE_SELFTEST: FAIL (2/280 cases)` | 1 | `receipts/item6-selftest.txt` |
| 6 control | `env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV bash tools/research-gate.sh --selftest` | `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, 0 `FAIL-case` | 0 | `receipts/item6-selftest-clean.txt` |
| composed | `bash tools/research-gate.sh verify-all "$f" --root .` | `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0`, `RESEARCH_GATE: CLEAN (…)`; chain leg `RESOLVED_HOPS=5/5` | 0 | `receipts/run-2.txt` |

The selftest was run exactly twice (the stated budget): once through the item-6 line as written, once with that variable
removed. Item 5 (`quote-reopen verify`) is **not applicable**: the record cites no live web quote — only committed
capture bytes — and this seat's wave item names no re-open, so no GET was made and none is authorised
(`corpus/evidence/round82/egress-approval.md`, seat row).

## 3. Twins — the frozen forms are refused under the landed Run lines

Diffs are in `receipts/twins.txt` (one line changed in twin 1, one in twin 3, two in twin 2 — the second is required for
K2's form: the claim cell names no declared row *and* no row's `claim_id` names the claim).

| twin | item 2 | item 4 | finding line (verbatim) |
|---|---|---|---|
| 1 flip `TBD` | rc 1 | rc 1 | `FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip placeholder=reason:present,flip:placeholder` |
| 2 sweep cell `W9`, row link moved | rc 1 | rc 1 | `FINDING SWEEP_NEGATIVE_UNRESOLVED severity=warn surface=sweeps obs=claim=N1 sweep=W9 names no sweep row this mode re-ran` |
| 3 `where` = `N/A` | rc 1 | rc 1 | `FINDING SWEEP_LOCATION_ABSENT severity=warn surface=sweeps obs=id=SW1 unclassifiable location naming` |

Structure mode stays CLEAN on all three (`RESEARCH_GATE: CLEAN (… findings=0 …)`, `receipts/twin-*.verify.txt`): the
defects live only in the sweeps mode, which is the point of the round-81 K2 forms. Twin 2 keeps
`VERIFIED_SWEEPS=1/1` and still drifts, so the unresolved-negative leg is independent of sweep verification.

The record's own negative sweep is falsifiable, not vacuous (my own check, not a frozen rule): planting
`corpus/knowledge/question-frame-probe-r80.md` makes the line print
`SWEEP id=SW1 … hits=2 … observed=hit verdict=mismatch` and `FINDING SWEEP_CLAIM_FALSE … hits=2 first=corpus/knowledge/question-frame-probe-r80.md`,
rc 1; removing it returns CLEAN (`receipts/sweep-falsification.txt`). Two of the four globs catch the planted name
independently.

## 4. Which checklist lines are awkward, wrong, or too strict in practice

Measured, not guessed.

1. **Item 6 is wrong as written — and it fails loudly.** `CHOUSA_GREP_PIN_ECHO=1 bash tools/research-gate.sh --selftest`
   runs the whole battery with that variable exported, and two battery cases inherit it: `pin-bashenv-root`
   (`receipts/item6-selftest.txt:274`) and `pin-env-fn-root` (`:281`), each `pin_rc=0 drift_rc=0`. Their drift legs are
   `env -u BASH_ENV …` and `env -u CHOUSA_ROOT …` — neither unsets `CHOUSA_GREP_PIN_ECHO` — so the drift run prints its
   own `GATE_GREP:` echo line and the case's exact-output assertion (`[[ $dout == 'GATE_DRIFT: none' ]]`) fails. Result
   at the landing revision: `RESEARCH_GATE_SELFTEST: FAIL (2/280 cases)`, exit 1, versus `PASS (280 cases, 0 skipped)` with the
   variable removed, same tree, same host, back to back. The line also pipes through `grep -m1`, so it reports the
   filter's status, not the battery's, and truncates the battery it started. **This is a checklist-line defect, not a K4
   firing**: C1's own predicate runs `bash tools/research-gate.sh --selftest` without the variable and passes (my clean
   run, and the L1's committed `corpus/evidence/round82/after/c1-selftest-after.txt`: `PASS (280 cases, 0 skipped)`,
   `rc=0`).
2. **Item 3 false-refuses a reasonable entry, and is pinned to one round's spans.** The landed entry
   `corpus/knowledge/question-framing-frames-r82.md` heads its section `## Inference (lane's, not stated by the sources)`;
   the tool wants `#### Inference`, so the line prints `FINDING INF_SECTION_ABSENT` and exits 1 on an entry whose eleven
   quotes I independently re-derived as present (below). The `--spans corpus/evidence/round46/spans.tsv` argument is a
   fixed round-46 path, so no entry whose spans live in another round's file can be checked by this line at all. The
   control leg on the entry the line was written for still passes (`GROUND: PASS`, exit 0), so the refusal is the
   heading level plus the span file, not the entry's grounding.
3. **Item 1 does not enforce its own prose.** The prose says every claim needs an `sha256` pin and "a claim without a pin
   is not checked for revision"; the Run line exits 0 both ways. Measured: the same six claims with the `sha256` field
   removed → `VERDICT_BEARING_CLAIMS=6/6`, `RESEARCH_GATE: CLEAN`, exit 0 (`receipts/item1-pin-probe2.txt`); a
   comment-only companion → `VERDICT_BEARING_CLAIMS=0/0`, `RESEARCH_GATE: CLEAN`, exit 0 — the same 0/0-CLEAN shape
   round 81 named for sweeps, still open on claims. A wrong pin does fire (`CLAIM_SOURCE_REVISION_MISMATCH`, `3/6`,
   exit 1), so the pin works when present; nothing requires it. And nothing binds the record's claim table to its
   companion: my record's C7, C8 and N1 are deliberately absent from the companion and no Run line notices.
4. **Item 2's compound discards its first half and inherits item 4's subject.** `! … | grep -q` inverts the *filter's*
   status, so the structure leg's exit is thrown away, and any record the gate cannot read still reaches the second
   half. Measured: on twin 1 — a rejection defect, which is item 4's subject — item 2's line exits 1
   (`compound_rc=1`, `receipts/item2-literal.txt`), so a failure under item 2 cannot be attributed to item 2.
5. **Items 2 and 4 are the same command**, so neither can discriminate which defect class fired; twins 2 and 3 exit 1
   under both items, and only the finding id tells them apart.
6. **Item 4 is keyed on vocabulary, not on meaning** (disclosed in the checklist prose, but a trap in practice):
   `TBD` → `flip=placeholder`, `REJECTIONS_OK=0/1`, exit 1; the same rejection with the same meaning written as
   "never: the page is a metadata service and cannot state a framing rule, so no paragraph on it can flip this
   rejection" → `flip=present`, `REJECTIONS_OK=1/1`, exit 0 (`receipts/probe-flip-wording.txt`). Two records that say
   the same thing score differently.
7. **Receipts cannot reconstruct a sweep.** `verify-sweeps` prints `where=` cut at 80 characters, so my four-glob cell
   appears as `…,corpu` in every receipt; a citable receipt for item 2/4 has to travel with the record bytes. Cosmetic
   for the verdict, but it means the sweep cell itself is never quotable from a receipt.

## 5. What this trial does and does not say about the frozen claims

- **C2 (depth), K2 grounding leg, re-derived by this seat**: all eleven `Located quotes` of
  `corpus/knowledge/question-framing-frames-r82.md` occur exactly once in their named committed capture —
  `QUOTES_PARSED=11 QUOTES_LOCATED=11/11`, `ENTRY_QUOTE_CHECK=PASS` (`receipts/c2-entry-quotes.txt`), with the four
  capture sha256s printed there (`598abc09…`, `8581ca18…`, `fc857da3…`, `b8b542d9…`). No counted quote is absent from
  its capture. I did not re-derive the refetch-table pins or review the decision rows for support (C2 K3 is a reviewer
  check, not mine).
- **C1 (operability)**: my trial's reasonable record passes items 1, 2, 4 and composes CLEAN (`verify-all`, 5 sections),
  so I found **no K3 harm** — no record the base gate would pass is refused by the landed Run lines. I did not re-run
  the frozen K2 counter (`k2-gate-r82.py`); that is other seats' measurement, not this seat's.
- The item-6 defect above is the one place where the round's own instrument can be made to look red by following the
  checklist literally. Whoever writes the round's operability verdict should run C1's K4 leg with the plain
  `bash tools/research-gate.sh --selftest` and not through the item-6 line.

Risks / blockers: none blocking. Residuals worth routing: items 1 and 3 as above (weak pin enforcement, 0/0 CLEAN; a
heading-level and span-file binding that refuses the round's own entry), item 2/4 attribution blur, and the item-6
line's interaction with its own battery.

VERDICT: R82ExecTrial C1 operability held — a record written to the landing's own grammar (9 claim rows incl. one negative with a falsifiable local sweep, one complete rejection, 5 resolved hops, a sha256-pinned claims companion) passes items 1, 2, 4 and verify-all CLEAN, and the three frozen K2 mutant forms are refused with the expected finding ids; the only red I could produce is the checklist's own item-6 line dirtying the battery it runs.
VERDICT: R82ExecTrial C2 depth n/a — this seat authored a research record, not a knowledge entry; it read the landed entry only to re-derive its quotes (11/11 present in their captures), and the item-3 line's refusal of that entry is a heading-level/span-file binding, not a grounding failure.
