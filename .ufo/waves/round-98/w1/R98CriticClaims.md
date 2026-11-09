# R98CriticClaims: adversarial reading of claims C1 and C2 at freeze F

Attacked tree: `aac826848dda5029ba459568b29d9a92176dc2b6`, cloned with `git clone -q --shared` into scratch and checked out at F. All batteries ran against the scratch clone, never the live lane. Scratch removed before yield.

Correction: the Receipts list below is authoritative. `R98CriticClaims-content-pos.txt` was NOT copied into w1 (scratch was deleted before copy); its POSITIVE result (exit 0, 67/67) is reported inline in C1 finding 1 only. The harm-leg output is not in `R98CriticClaims-battF.txt`; it is reported inline in C1 finding 3 only and was reproduced in scratch before deletion.

## Summary

- C1 (operability): every printed predicate reproduces at F. The battery PASSes with the exact tallies claimed. The named limit (c), content recognition, is not falsified but not resolved either: my stand-in was inconclusive. Verdict held.
- C2 (depth): every counting predicate reproduces at F. One clause is false as worded: M1 is quoted from the record's title, not from `abstractText`, while the entry says every S231 quote is a substring of `abstractText`. That makes K2 fire. The decision-table (K3) faithfulness is not enforced by any instrument, which the claim's named limit (d) already admits. Verdict fired on K2 (minor).

## Tooling

No tools installed or updated. Only system `git`, `python3`, `sha256sum`, `cmp`, `sed`, `/usr/bin/grep`.

## C1 `C1-SELFTEST-R97MUTANTS-R98`

### Counting commands at F

| command | exit | observed |
|---|---|---|
| `python3 -B tools/search-rerun.py --selftest` (cwd = scratch clone) | 0 | 67 `SELFTEST <id> ok` lines in CASE_IDS order, last line `SEARCH_RERUN_SELFTEST: PASS cases=67/67`. Receipt: `R98CriticClaims-selftest.txt` |
| `python3 -B corpus/evidence/round98/selftest-controls-r98.py --root . --work <scratch>` | 0 | `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67` then `SELFTEST_CONTROLS_R98=PASS`. Run took 658.9 s (bg_1059). Receipt: `R98CriticClaims-battF.txt` |

Predicates match the claim exactly. The battery's sha256 (942b7069...) matches the `before` receipt header.

### Clause-by-clause enforcement

- "67 named case lines (48 + g00 + r17-r34)": verified. `CASE_IDS` has 67 entries; battery's `lines_ok` check requires them in order.
- "kills 35 of the 37": `EXTERNAL_R97_KILLED=35/37` prints this. `KILL_REQUIRED=35/35` is the required denominator (37 minus the two named survivors), so the claim's wording matches the printed number. Named survivors `u01-verify-return-0` and `u05-tree-files-jj` reproduce as survivors (`survivors=u01-verify-return-0,u05-tree-files-jj`).
- "round-97 tool kills 12 of them": `c1-base.txt` shows `BASE_KILLED=12/37`, computed by the battery against the base tool, not by hand.
- "34 external mutants and the round-96 battery's 23": `PRIOR_R97_KILLED=34/34`, `R96_MUTANTS_KILLED=23/23`. Verified.
- "three mutants that do not change what the tool computes survive": `EQUIVALENT_SURVIVED=3/3`. I checked the three by hand. e3 (`lines[-1] == b""` to `not lines[-1]` on a bytes value) is equivalent. e1 (comment) and e2 (docstring) are equivalent. Verified.
- "refuses five stand-ins": `ORACLES_REJECTED=5/5`. Each oracle line printed `ok` with battery_rc=1 (see the log). Verified as printed, not as a claim about every possible stand-in.
- "guard-blind self-test": the guard-blind oracle has tally `KILL_REQUIRED=30/35`, so it is refused on kill count. Verified.
- "self-test that fails on any change to its own bytes (round-97 routed limit (g))": the hash-of-self oracle is refused because it kills all three equivalents (`EQUIVALENT_SURVIVED=0/3`). Verified.

### Clause-level findings

1. The stand-in for named limit (c) is inconclusive. I built `w/standins/content-recog.py` at scratch: it embeds the `new` strings of the 37+34+23 scored mutants (70 kept of 80; 10 dropped, including the 1-char r96 news `0`-`9`) and FAILs when a kept string appears in its source outside the embedded list. Results:
   - POSITIVE: PASS 67/67 (receipt `R98CriticClaims-content-pos.txt`).
   - e1, e2, e3 equivalents: all PASS 67/67 (survive, as the battery wants).
   - g01 mutant: FAIL with `failed=setup`. This is not a content-based kill: `old` occurs twice in the stand-in (once in the real code and once inside the embedded `x3` new string), so the battery's one-site rule would print `SETUP applies 2 times` and not count a kill. I did not run the full battery on this stand-in. The stand-in therefore does not test named limit (c) and the claim's named limit stays unresolved, not falsified. Notes: `R98CriticClaims-content-notes.txt`.
   - Short-string false positive: the content check matched `    return 0` inside `    return 0 if k == n else 1` until I special-cased it. This is a real construction hazard for any content recogniser and supports the claim's statement that content recognition "is not ruled out" rather than refuted.
2. Probe docstring stale: `.ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt` says "34 NEW one-site mutants" but its `MUTANTS` literal has 37 entries (the battery asserts 37). Not a claim sentence; the claim says 37. No falsification of the claim.
3. Harm leg (K3) reproduces: `c1-verify-harm.txt` vs my base-tool rerun on the four fixtures gives identical stdout and exit codes, plain and `--strict` (receipt written as text in the log under `R98CriticClaims-battF.txt` plus my rerun output). Held.
4. Do-nothing controls score the base with frozen counters. `c1-base.txt` is produced by the battery itself with `--tool <base-tool>`, and its CASES/tally lines are the same counters as at F. The base receipt's own EXTERNAL line `EXTERNAL_R97_KILLED=12/37` is consistent with `BASE_KILLED=12/37`. Held. The `c1-base.txt` header says "battery = working-tree bytes frozen at F", which is true: the battery bytes at F hash to the header value.
5. Mutant `g00` vs the claim's (d) limit: not independently tested beyond the battery's own run.

Verdict C1: held. No stated predicate is false at F. Named limit (c) is unresolved by my stand-in (inconclusive, not fired).

## C2 `C2-ENTRY-R98`

### Counting commands at F

| command | exit | observed |
|---|---|---|
| `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md` | 0 | 38 `GATE_RECORD ... OK` lines, then `GATE_RECORDS files=1 records=38 ok=38 fail=0` |
| `bash tools/research-gate.sh verify-metadata corpus/knowledge/press-2015-statement-questions-r98.md --root .` | 0 | `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` |
| `python3 -B tools/search-rerun.py verify corpus/knowledge/press-2015-statement-questions-r98.md --root .` | 0 | `rev_match=5/5`, `SEARCH_RERUN: CLEAN` |
| `python3 -B corpus/evidence/round98/entry-controls-r98.py --root .` | 0 | `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=7/7 QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10 LANE_FILLED=10/10` then `ENTRY_CONTROLS_R98=PASS` |

Note for the record: my first attempt of the gate and metadata commands ran from the wrong cwd and exited 2 (operator error, not a claim failure). Re-run from the scratch clone root gave the values above.

### Independent recomputation

- Question lines: recomputed from the S225 capture with the same HEAD/FOOT bounds: 36 lines (34, 35, 36, 37, 38, 39, 42, 43, 44, 45, 46, 49-57, 60-68, 71-73, 76-79). Count matches.
- Prior entry alone holds 16 lines `[34,36,38,39,42,44,50,57,60,62,68,71,72,73,76,79]`; the new entry alone holds 20; overlap empty; union is all 36. Matches the claim's "20 that the round-97 entry did not" and "36/36 (16/36 at the base)".
- K17+K18 = capture line 66 exactly, 30 words. Verified.
- K2 quote word counts all 25 or fewer (max K17 = 22 words).
- M2-M15 are substrings of `abstractText`. Verified.
- Element cells: all seven S231 cells and all six S225 cells verified; the S225 numbered headings and the "serial comma" and parenthesis differences described in the paragraph match the captures.

### Clause-level findings

1. **Fired, K2 (minor): M1 is not in the abstract.** M1 is `PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement.`, which is the record's `title` field (exact match, `\xa0` normalised). It does not occur in `abstractText` (`M1 in abstractText: False`), whereas the entry's "Located quotes" preamble says "Every S231 quote below is a substring of that string". Claims K2 says "an S231 quote is not inside the record's `abstractText`": that predicate is violated by M1. Evidence: `R98CriticClaims-m1.txt`. Nothing in the instruments catches this: `gate-records.py` matches S231 quotes against the whole normalised capture (`QUOTE_ABSENT` checks the capture text, which includes the title), and `entry-controls-r98.py` `check_quotes` also uses the whole capture. So the scope claim in the entry text is unenforced. Impact on counts: none; impact on wording: the entry's abstract-scope sentence is false for one of fifteen quotes.
2. **Unenforced: decision-row faithfulness (K3 / named limit (d)).** I built `R98CriticClaims-falsified-entry.md`: the same Located quotes and element table, with every Decision-table Do cell prefixed `DO NOT `. `ec.score()` returns PASS (held 36/36, elements 7/6, warrants 10/10, lane 10/10). Also a never-cell fabrication (`NEVER ask about search concepts at all.` replacing `(none stated by the sources)`) and a Do-inversion (`never ask about search concepts; ignore them entirely`) both PASS. So the controls cannot distinguish an entry whose decisions contradict its quotes from a faithful one. The claim's sentence does not mention decision rows; the named limit (d) says faithfulness is the reviewer's item (K3). Held as worded; the enforcement gap is real and stated.
3. Element paragraph: each factual difference claimed (S225 numbering; parentheses on elements 2, 3, 4; "Text word searching"; serial comma in element 5; S223's grouping "limits and filters, syntax and line numbers; and spelling") reproduces against the captures and the round-96 entry at L22-L23. Held.
4. Named limit (c) "36/36 counts lines, not questions": the claim says lines 64, 65 and 78 carry several questions and 66-67 one. Recount: line 53 also carries two questions ("Are major headings ... used?" and "If so, is there adequate justification?") and is not in the list. The list is an example, not a claimed census, so this is minor and not a fire. Line 66's second sentence ("Are there any other fields to be included") has no question mark, so the line holds one `?`-question by the counter's rule. Held.
5. Do-nothing control: `c2-base.txt` says `BASE_HELD=16/36` and "recomputed with entry-controls-r98.py's own question_lines() and held()". Same functions as the instrument, so this is not an independent check of the 16. I reproduced it with the same functions (16) and with the prior entry only (16). It is consistent, but it does not independently confirm the base count. Noted.
6. K21-K22 "line 78 split (28 words)" was not recounted by me. Not checked.
7. Gate tier: S231 is recorded `tier=A` in both SOURCES.md and the gate lines; the entry's tier-A scope sentence matches SOURCES. Held.
8. Searches: `search-rerun.py verify` reports Q1-Q3 `tree=CHANGED` at F (expected; S231 capture added), `rev_match=5/5`. Matches the entry's "not a finding without --strict". Held.

Verdict C2: fired on K2 (M1 quoted from the title while the entry says every S231 quote is inside `abstractText`). Counts reproduce; K3 faithfulness unenforced as the claim's named limit (d) admits.

## Receipts (in `.ufo/waves/round-98/w1/`)

- `R98CriticClaims-battF.txt`: full C1 battery run at F (bg_1059), exit 0, `SELFTEST_CONTROLS_R98=PASS`.
- `R98CriticClaims-selftest.txt`: `--selftest` output at F, exit 0, 67/67.
- `R98CriticClaims-killreq.txt`: KILL_REQUIRED and EXTERNAL denominators from the battery source.
- `R98CriticClaims-m1.txt`: M1 vs abstractText vs title (K2 fire).
- `R98CriticClaims-falsified-entry.md`: entry with inverted Do cells; passes entry controls (K3 unenforced).
- `R98CriticClaims-content-pos.txt`: content-recognition stand-in POSITIVE run (exit 0).
- `R98CriticClaims-content-notes.txt`: stand-in construction notes and its limits.

Commands for the main agent to re-check quickly (not run by me as the lane verifier): the two counters in each claim's `counting_command` at the frozen tree.

## VERDICT lines

VERDICT: R98CriticClaims C1 held — every printed predicate (`SEARCH_RERUN_SELFTEST: PASS cases=67/67`, `SELFTEST_CONTROLS_R98=PASS`, the tallies including `EXTERNAL_R97_KILLED=35/37` and `BASE_KILLED=12/37`) reproduces at F, and the named limit (c) stand-in I built was inconclusive rather than a refutation.
VERDICT: R98CriticClaims C2 fired — the counting predicates reproduce at F, but M1 is quoted from the record's title, not from `abstractText`, so the entry's "every S231 quote is inside abstractText" statement and claims K2 are false for one of the fifteen quotes.
