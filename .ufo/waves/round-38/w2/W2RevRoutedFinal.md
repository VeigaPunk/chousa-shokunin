# W2RevRoutedFinal

## Verdict

At `8e93bc9165…`: the counter-strength candidates LANDED-NARROWED (F1 pre/post gate binding + `counter_sha256` landed; the F2 gate-self-report half explicitly open), the exported-`env` witness LANDED-NARROWED per Erratum 6, every gate-side planned candidate NOT-ADDRESSED (gate bytes still equal the freeze hash `37e2b996…`), the S070 anchor-label supersede row was never landed and its routed pointer drifted to a wrong row id (S068); RevF1Disposition CLOSED — both r37 knowledge-doc corrections are present and accurate against committed receipt bytes.

## Evidence

Lane tip: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699` (matches dispatch tip). No counter runs, no seeds (disposition review; wave executors hold the 7/7 runs). No tool installs.

1. `sha256sum tools/research-gate.sh` → `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` = the frozen candidate hash in `corpus/evidence/round38/claims.md` header. The wave-1 integration touched counters/verifier/docs/receipts only; gate-side candidates are mechanically not addressed.
2. Verifier re-execution (all under the repo above): each of the 9 `corpus/evidence/round38/receipts/*.json` vs `--gate tools/research-gate.sh` and both counters → `c1-after-s38{001,011,351}` rc=0 under c1-count only; `c2-after-s38{101,111,371}` and `c2-base-s38101` rc=0 under c2-count only (cross-family = rc=1: the Erratum-2 identity-reroute kill re-observed); `c1-base-s38001`/`c1-base2-s38003` rc=1 vs the landed gate but rc=0 against their own bound control gates (`base-gate-r37.sh`, `base-gate-r38.sh`) — reconciling 8e93bc9's "verified (9/9)" as per-receipt-bound-gate verification.
3. Legacy fail-closed: `python3 corpus/evidence/round38/verify-receipts.py --receipt corpus/evidence/round37/receipts/c1-after-s37001.json …` → `VERIFY-FAIL: missing-field counter_sha256`, rc=1.
4. Receipt fields (grep over the 9): every receipt carries `counter_sha256` (79040790…/414a7a10…, equal to the on-disk counters' sha256), `expect_sha256` d34f1735…, `receipt_sha256`, `gate_sha256_pre == gate_sha256_post`; after-receipts `matched=7` @ `37e2b996…`; `c1-base*` `matched=2` @ `a7d3922c…`/`9fcac047…`; `c2-base-s38101` `matched=0` with `subject_counter` = the r37 counter.
5. r37 receipts (grep over `corpus/evidence/round37/receipts/`): all 8 after-receipts `matched=7` @ `9fcac047…`; `c1-base-s37001` `matched=2`, `c2-base-s37021` `matched=3`, both @ `a7d3922c…`.
6. Doc corrections re-read: `corpus/knowledge/claim-pin-provenance-r37.md:37-40` and `corpus/knowledge/pin-capture-env-r37.md:44-47` — both now read "scores 7/7 on every committed after-receipt (the committed base receipt … scores 2/7 [resp. 3/7] against the base gate by design; corrected round 38 after the round-37 receipt audit finding L1)".
7. Negative checks on final bytes: dead fields still in `tools/argv-witness.py` (`channel`, `fixture_root_prefix` :312; `_stderr.log` :326); locale-exposed sites remain in `tools/research-gate.sh` (:762 sed trim, :1007-1010 mixed trim/norm, :1092/:1096 `grep -qiE`) while other functions pin `local LC_ALL=C` (:1330, :3155, :3277); `corpus/SOURCES.md:80` S070 row still labels lines 19-20 "SYNOPSIS `-c, --check`" and the only `supersedes` rows are the r25 S029–S033 class (grep); `c2-count.py` contains no `verifier_sha256` binding (grep: comment text only).

## Findings

### A. r37 closure routed-defects list (6 items; `corpus/lessons/round-37-verifier-spotcheck.md:81-95`) vs `8e93bc9…`

| # | item | disposition |
|---|---|---|
| 1 | Counter-strength debt (`gate_sha256` post-run only; gate self-report scoring — r37 residual F1/F2) | **LANDED-NARROWED.** F1: receipts bind `gate_sha256_pre`/`gate_sha256_post`, refuse with no receipt on change (`verify-receipts.py:13-19,38-40`; claims §C2). F4's counter identity landed as `counter_sha256` (all 9 receipts). F2 (black-box gate self-report; receipt cannot prove the mechanism) NOT addressed — re-named as a live limit in claims §Limits and the verifier docstring "Limits" paragraph; Erratum 2 carries only `verifier_sha256` (r39). |
| 2 | "S068 anchor-label supersede row (r36 spot-check defect 8)" | **NOT-ADDRESSED — and the pointer is wrong.** The on-record nit is S070 (`corpus/lessons/round-36-verifier-spotcheck.md:160-161`, fix item 4; the r38 claims' routed-work paragraph correctly says S070). S068 is the bash(1) BASH_ENV row, not implicated; no "D8"/"defect 8" row exists in the r36 lesson (grep). `SOURCES.md:80` still carries the SYNOPSIS mislabel; no supersede row landed. |
| 3 | Witnessed `SHELLOPTS=noexec` false pin success | **NOT-ADDRESSED** as a fix. Re-demonstrated on the landed gate (claims §Limits: pin exits 0, no baseline); "a pre-startup boundary would be a separately specified tool, carried debt". Erratum 5's `SHELLOPTS` scrub is measurement-harness hygiene only; the gate defect stands. |
| 4 | Seats' answering models not individually recorded | **NOT-ADDRESSED** — disclosure/process note, operator-side; no round-38 artifact at this tip claims it (claims.md, SCORECARD r38 sections checked). [INFERENCE: negative, grep-based] |
| 5 | SHONEN boxes remain `[~]`; promotion operator-owned | **NOT-ADDRESSED** — process note, not lane work; nothing to land in r38's claim surface. |
| 6 | Tool installs this round: none | **NOT-ADDRESSED** — vacuous record (records an absence); nothing to land. This seat also installed nothing. |

### B. SCORECARD §Planned — round 38 (`SCORECARD.md:2117-2136`) vs `8e93bc9…`

| # | candidate | disposition |
|---|---|---|
| 1 | prefix-64 attribution bypass (stricter span rule + V7 variant; r36 Err. 8) | **NOT-ADDRESSED** — gate bytes unchanged since freeze (hash equality, Evidence 1); no r38 artifact names prefix-64. |
| 2 | per-scenario counter assertions tightened to their names (S7-S9, QUALITY 52) | **NOT-ADDRESSED** — the r35/r36 counters are untouched. Adjacent-but-different: Erratum 3 landed named-refusal assertions (`counter-sha256-mismatch` etc.) in the r38 c2 tamper cells, not the S7-S9 item. |
| 3 | three dead fields in `tools/argv-witness.py` (SimpDiff D1-D3) | **NOT-ADDRESSED** — `channel`/`fixture_root_prefix` :312, `_stderr.log` :326 still present. |
| 4 | verdict-flipping locale seam in the metadata screener (r36 Err. 13) | **NOT-ADDRESSED** — locale-exposed `[[:space:]]` trims and `grep -qiE` remain at :762, :1007-1010, :1092, :1096. |
| 5 | `counter_sha256` bound into every receipt | **LANDED** — all 9 receipts bind it and verify-receipts re-derives it plus the counter family; cross-counter verify rc=1 (Evidence 2). |
| 6 | call-for-show engine measurement (r36 §Erratum 9 limit) | **NOT-ADDRESSED.** |
| 7 | "S068" anchor-label supersede row | **NOT-ADDRESSED** — same row as A-2; still open, pointer id still wrong in SCORECARD. |
| 8 | `SHELLOPTS=noexec` witness + exported-`env` function witness | **LANDED-NARROWED** — exported-`env` witness is C1 (frozen 7/7; base gates 2/7). Erratum 6 narrows: only the NAME `env` at the capture's one absolute call site; parent-function class (bash-name vectors, sibling-name witnesses) is named limit; the noexec half is A-3, open. |
| 9 | r37 claim-text kills: loader-env scrub (`env -u LD_PRELOAD …`) + LD_PRELOAD cell; `BASH_FUNC_*` scrub (or `env -i`) + genuinely-exported scenario | **LANDED-NARROWED** — C1 closes function-export interposition on the capture's `env` invocation + override refusal shape only. Erratum 6(a): the `BASH_FUNC_*` channel itself untouched (parent-exported `date` function still embeds `GATE_GREP:` + phantom drift, demonstrated). The env-child loader scrub and an LD_PRELOAD counter cell are carried debt (claims §Limits bullet 2); Errata 5/6 declared "never re-litigated" — narrowing is by design, not omission. |
| 10 | counter-strength debt (post-run binding; self-report; `counter_sha256` carried) | **LANDED-NARROWED** — see A-1. |
| 11 | carried C1 debt (spans ≥ 32768) | **NOT-ADDRESSED** — "stays open" by declaration. |

### C. RevF1Disposition OPEN item — CLOSED

The r37 docs' "7/7 on every committed receipt" was false as written (the base receipts score 2/7 and 3/7). The round-38 integration corrected both files (`claim-pin-provenance-r37.md:37-40`, `pin-capture-env-r37.md:44-47`, commit `1f0add7` "r37 knowledge L1 repair") to "7/7 on every committed after-receipt" with the base exceptions named, attributed to the round-37 receipt audit finding L1. Re-read both files; re-derived against committed receipt bytes: 8/8 after-receipts `matched=7` @ `9fcac047…`; bases `matched=2` (c1) / `matched=3` (c2) @ `a7d3922c…` (Evidence 5). The corrected sentences are exactly accurate. Additionally, the corrected scoping is now load-bearing: the legacy receipts fail the r38 verifier (`missing-field counter_sha256`, Evidence 3), so the old universal wording would have contradicted the r38 fail-closed record. No residual open text remains in either file (grep "7/7 on every committed receipt" over `corpus/knowledge` → no matches).

### Extra findings

4. Routing-pointer id drift: the same carried row is "S068" in `round-37-verifier-spotcheck.md` and SCORECARD's planned list, "S070" in the r36 lesson's fix list and the r38 claims. A r39 seat working from the S068 pointer would supersede the wrong row.
5. "Verified (9/9)" (8e93bc9 message) is correct only as per-receipt-bound-gate verification: the two c1 base receipts verify against their control gates, not the landed gate (Evidence 2). Fine as regenerated; a future aggregate phrasing should say so.
6. Erratum 2's carried debt confirmed open on final bytes: `c2-count.py` binds no verifier identity, so a replaced verifier still re-adjudicates old receipts silently (matches claims Erratum 2's r39 carry).

## Limits

No counter re-execution with fresh seeds — the frozen 7/7 predicates are wave-executor evidence; my slice was disposition, verified via the committed verifier and receipt bytes only. Negative dispositions ("no r38 artifact names X") rest on greps of claims.md, SCORECARD.md and SOURCES.md, not every wave file; `.ufo/waves/round-38/` content is mutable workspace and wave-2 reports were still landing, so dispositions name the tip commit's corpus/committed bytes as the record. Time-boxed; no installs performed.
