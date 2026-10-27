# QualityGate — round-60 gate adjudication (axes: operability, depth)

Bounded analysis of the two frozen claims (`corpus/evidence/round60-claims.md`) against the
current counters, the current source/builder bytes, and prior committed evidence. No live
fetch, no writes outside this file, no commits or git/jj mutations. Scratch:
`/fast/scratch/hyaku/chousa-r60/QualityGate` (created, used, removed).

Artifacts read (uncommitted at claim base `b379919a873e7080a31ef92c7002f55f5374e2c6`;
`git status --porcelain` shows `?? corpus/evidence/round60/` and `?? corpus/evidence/round60-claims.md`):

```
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
```

`diff -u corpus/evidence/round58/controls/build-spans-r55.py tools/build-spans.py` exits 0: the
round-60 candidate builder is currently byte-identical to the pinned r55 "known unsafe" control.

## Receipts (all runs this seat, this round)

| id | command | output | exit |
|---|---|---|---|
| B0a | `python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work /fast/scratch/hyaku/chousa-r60/QualityGate/c1 --seed 6001` | `INJECTION_REJECTED=1/1` `BASELINE_DISCRIMINATES=1/1` `CANDIDATE_REFUSAL=0/1` `C1=FAIL` | 1 |
| B0b | `python3 -B corpus/evidence/round60/c2-count.py --root . --work /fast/scratch/hyaku/chousa-r60/QualityGate/c2` | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` `C2=PASS` | 0 |
| T1 | C1 counter with `--builder` = 3-line script `print('=PASS'); print('all seven hazards accepted'); sys.exit(0)`, fresh `--work` | `INJECTION_REJECTED=1/1` `BASELINE_DISCRIMINATES=1/1` `CANDIDATE_REFUSAL=1/1` `C1=PASS` | 0 |
| T2 | same token, `sys.exit(1)` | `CANDIDATE_REFUSAL=0/1` `C1=FAIL` | 1 |
| T3 | import `c1-count.run`, score a printer and a destructive printer directly | `forged-printer: rc=0 state='candidate_safe'`; `forged-destructive: rc=0 state='baseline_bad'`; label `forged_safe` never returned | — |
| T6 | C1 counter with `--builder` = script that writes `out/spans.tsv`=`junk` and `out/spans/S601-1.txt`=`not the span`, exits 0, never reads the quote table | `CANDIDATE_REFUSAL=1/1` `C1=PASS` | 0 |
| T7 | B0a re-run with the same `--work` dir | `FileExistsError: [Errno 17] File exists: …/c1/forge/cache` traceback, no `C1=` line | 1 |
| T4 | C2 counter against a scratch root whose `corpus/knowledge/citation-count-semantics-r37.md` appends an explicit overreach paragraph (`This document proves the GB/T 7714 reference format remains the binding standard today and that CNKI tokenises 文献类型 and 载体类型 separately in its index.`); that root contains **no** `SCORECARD.md` | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` `C2=PASS` | 0 |
| T5b | C2 counter against a root whose entry is byte-identical except the leading blank line is stripped | `METADATA=0/1` `C2=FAIL` | 1 |

## C1 gate inventory

Frozen predicate: `C1=PASS` and exit 0 iff (a) candidate reaches the safe path without deleting the
foreign file, (b) the pinned r55 builder deletes it, (c) the output-injection mutant prints `=PASS`
but is scored as a failure.

| gate | clause | implementation | verdict |
|---|---|---|---|
| G1.a | safe path + foreign file preserved | `candidate_safe = returncode == 0 and intact` (`c1-count.py:41`). Nothing checks that a span or `spans.tsv` row was produced, or that `spans/S601-1.txt` holds the derived bytes. | **NOT A GATE.** Any exit-0 no-op passes (T1). A junk writer that never reads the quote table passes (T6). The claim's "independently observed safe path" is observed in name only. |
| G1.b | pinned r55 control deletes the file | `baseline_bad = returncode == 0 and not intact` over `corpus/evidence/round58/controls/build-spans-r55.py` (`:42`). | **HOLDS** as a measurement (B0a). Note the consequence: with candidate bytes == control bytes (sha `1ed2650a…`), legs (a) and (b) are complementary by construction, so C1 cannot pass while the candidate is unmodified — although T1 shows the pass state needs no builder work at all. The gate is simultaneously too weak (no-op passes) and conditioned on builder bytes the claim explicitly disclaims ("does not claim the builder itself meets all hazard legs"). |
| G1.c | injection mutant printed `=PASS`, scored as a failure | `forged_safe` (`:43`) is the *same expression* as `baseline_bad` (`:42`), and `:44` tests `baseline_bad` first, so `forged_safe` is unreachable. `forge_blocked = forge_state != "forged_safe"` (`main`) is therefore always true. | **VACUOUS.** `INJECTION_REJECTED=1/1` is a tautology that cannot fail on any input (T3: neither a printer nor a destructive printer produces the label). There is also no failure state in the counter at all, so the frozen phrase "is scored as a failure" has no implementing branch. |
| G1.d | output bytes cannot establish a leg state | stdout/stderr captured (`:37`) but never referenced; verdicts use return code plus one file digest (`:38`, `:41`). | **HOLDS** as stated, but the substitute signal is under-specific (G1.a): the counter swapped a forgeable token scan for a test that a forgery passes. |
| G1.e | exit 0 iff all three legs | `return 0 if passed else 1`. | **HOLDS on first invocation**; **BROKEN on re-derivation**: a second run with the same `--work` raises `FileExistsError` and exits 1 with no `C1=` line (T7), so a closure cannot distinguish "counter says FAIL" from "counter crashed". |

Smallest sufficient correction set for C1 (gate-level, no product edit made here):
1. Make the safe leg specific: assert the expected `spans.tsv` row and the derived `spans/S601-1.txt`
   bytes from the fixture cache text. A return code alone must not earn the leg (kills T1 and T6).
2. Give the injection leg its own predicate and its own state; assert that state. Delete the dead
   `forged_safe` branch and the clause that compares a state to itself.
3. Make `run()` tolerate or refuse a non-empty `--work` rather than traceback, so re-derivation prints
   a verdict line.
4. `--seed` is parsed and never used (`:53`), while the frozen predicate pins `--seed 6001`: either
   drop the flag from the counter and the claim, or use it.

## C2 gate inventory

Frozen predicate: source digest and quote location from the committed S101 raw capture via the pinned
capture-text form; verify the new entry's exact observation and no overreach; verify citation and
metadata; require the scorecard's declared disposition; base must fail because no round-60 entry exists.

| gate | clause | implementation | verdict |
|---|---|---|---|
| G2.a | base must fail (no round-60 entry) | `ENTRY` is the pre-existing `corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8,13`). `git show b379919:…r37.md` already carries `#### Unknown` at line 74 and the exact phrase at line 79; `git diff b379919 -- …r37.md` is empty. | **FAILS its own control.** A do-nothing control reaches `C2=PASS` at the frozen claim base (B0b). Per the round contract's §9 sizing rule the target must be one a do-nothing control cannot reach; as frozen, C2 cannot be admitted whatever the target verdict, and no new round-60 note is required to pass it. |
| G2.b | verify the new entry's exact observation | No entry text is ever compared to the located quote. `scoped` (`:18`) only tests presence of the heading string `#### Unknown` and one canned sentence. | **UNIMPLEMENTED.** A note that misstates the S101 item passes as long as it keeps those two substrings. |
| G2.c | no overreach against the source bytes | No negative scan exists; the counter never searches for validity/implementation claims. | **UNIMPLEMENTED** — T4 appends an explicit "remains the binding standard today … CNKI tokenises" paragraph and still gets `C2=PASS`. |
| G2.d | require the scorecard's declared disposition | `SCORECARD.md` is never opened, and no path to it is constructed. | **UNIMPLEMENTED** — T4's root has no `SCORECARD.md` and still passes. |
| G2.e | digest and quote location from committed capture | `RAW_PIN`/`QUOTE`/line 245 hold (B0b). But `form` is `ROOT/.ufo/waves/round-60/s101-open.txt` (`:7,13`) with script-global `ROOT`, not the `--root` under test; and `git ls-files .ufo/waves/round-60` is empty, so the `FORM_SHA` pin resolves against an uncommitted derived artifact. | **PARTIAL.** The source-line half holds. The form half is not re-derivable from the claim base and `--root` does not isolate it (T4 read the lane form while `--root` was a scratch tree). Corroborates `C2CounterAudit.md`. |
| G2.f | metadata (criterion 6 shape) | `body.startswith('\n# ')` requires a leading blank line before the H1. | **BRITTLE (false negative)** — T5b: a content-correct entry without the leading blank line scores `METADATA=0/1` and `C2=FAIL`. |
| G2.g | `--work <fresh-absolute-dir>` | parsed at `:13` and never used; no isolation, no cleanup. | **DEAD PARAMETER.** |

Smallest sufficient correction set for C2: point `ENTRY` at a named round-60 note (or a
round-60 marker plus diff against base); require that note's quote to be the located capture line and
scan it for the forbidden overreach classes; read the SCORECARD disposition; derive `form` from
`--root`; use `--work`; anchor the header gate on the H1 line rather than byte zero. With the current
state the only honest disposition is **unprovable / do not admit C2** — not "repair by weakening".

## Cross-cutting gates

1. **Freeze identity — UNVERIFIED.** The assignment-stated immutable SHA
   `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` is not the SHA-256 of the
   file's bytes (`65721569…`, 3355 bytes, mtime `2026-10-27 17:51:18 -0300`). Raw, CRLF-normalized
   and no-trailing-newline variants all hash to `65721569…`/`cae804fa…`; none matches. The file is
   untracked, so there is no committed baseline to diff against. The same mismatch is reported
   independently by `ClaimPlanner.md`, `C2CounterAudit.md`, `C2Critic.md`, `CarryDebtCritic.md`,
   `IntegrityCritic.md`, `RegistryScan.md` (which also dropped a hex digit), `S101Reopen.md`,
   `SourceCaptureScout.md`, `FreshnessScout.md`, `DataWalk.md`, `PatternConnector.md`,
   `SiblingOverlap.md`, `HandoffCritic.md`, `C1AlternateControl.md`. This seat did not modify the file.
   Gate verdict: the on-disk text may be used as the visible specification, but it is not the
   assignment's frozen artifact until the freeze owner reconciles the digest. Admission that cites
   "frozen bytes" must name the discrepancy.
2. **Committed-bytes re-derivation — UNMET.** Both counters, the claims file, and the C2 form are
   untracked; `git ls-files corpus/evidence | grep round60` is empty. Until the round commits, no
   closure can re-derive either verdict from `b379919` alone. The round contract requires one command
   over committed bytes; at this reading the command resolves against working-tree-only files.
3. **Claim↔counter predicate agreement — C1 partial, C2 broken.** C1's counter does not implement
   predicate clause (c) as written (no failure state, dead branch). C2's counter implements one of the
   predicate's five clauses (quote location) plus a substring proxy for two others, and omits two
   outright (no overreach, scorecard disposition).
4. **Do-nothing control — C1 passes, C2 fails.** C1's base run is `C1=FAIL` (B0a), so the C1 target is
   not pre-satisfied. C2's base run is `C2=PASS` (B0b), so the C2 target is pre-satisfied and cannot
   be claimed this round.

## Disposition requested from the integrator

1. Hold C1 unadmitted: the injection leg is a tautology and the safe leg is satisfiable by a 3-line
   printer (T1) and by an artifact-junk writer (T6). The claim's stated repair is not implemented.
2. Hold C2 unprovable: a do-nothing control reaches its exact PASS predicate at the frozen base
   (B0b), and three of its clauses have no code (T4). Do not amend the claim after data; report the
   honest stop and re-declare a base-failing target next round.
3. Reconcile the claims-file digest before any landing cites "frozen bytes".
4. Commit the counters and the S101 form so the verdicts are re-derivable, then re-run both commands
   on the committed tree and attach the transcripts.

## Scope statement

No product, counter, claim, SCORECARD, LOG, SOURCES or knowledge file was edited; no commits, pushes,
git/jj mutations, installs or external fetches. Peer seat reports in this wave were read but not
modified. All receipts above are this seat's own runs in `/fast/scratch/hyaku/chousa-r60/QualityGate`,
which was removed before this file was written.
