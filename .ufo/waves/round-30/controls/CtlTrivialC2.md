## C2 design v3 — historical seat results (v4 appended below)

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| always-ABSENT | registry, fetching, text reading and judgment | not run, not run | 7/27, 6/27 | [run1](CtlTrivialC2/receipt-always-absent-c2-run1-v3.json), [run2](CtlTrivialC2/receipt-always-absent-c2-run2-v3.json) |
| always-VERBATIM | registry, fetching, text reading and judgment | not run, not run | 7/27, 9/27 | [run1](CtlTrivialC2/receipt-always-verbatim-c2-run1-v3.json), [run2](CtlTrivialC2/receipt-always-verbatim-c2-run2-v3.json) |
| always-UNREACHABLE, instant | all fetching; no waiting or source reading | not run, not run | 11/27, 11/27 | [run1](CtlTrivialC2/receipt-always-unreachable-c2-run1-v3.json), [run2](CtlTrivialC2/receipt-always-unreachable-c2-run2-v3.json) |
| junk five-way random | registry, fetching, text reading and judgment | not run, not run | 5/27, 4/27 | [run1](CtlTrivialC2/receipt-junk-c2-run1-v3.json), [run2](CtlTrivialC2/receipt-junk-c2-run2-v3.json) |
| do-nothing, byte-identical round-29 tool | the entire round-30 change | not run, not run | 12/27, 14/27 | [run1](CtlTrivialC2/receipt-do-nothing-c2-run1-v3.json), [run2](CtlTrivialC2/receipt-do-nothing-c2-run2-v3.json) |

META-CHECK: none met

Detector: frozen v3 `c2-count.py`, target `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`. All ten runs printed that label with their table score, exited 1, recorded `design: v3` and `predicate_holds: false`, and used distinct fresh seeds. No measurement failure. Every no-fetch-control item completed within 0.518 s with `bound_ok` and `validated_only` true.

**Fixture finding, reported to parent:** chunked `slow-ok` can exceed the injected DEADLINE. `_frame` appends a seventh terminal-zero chunk (`corpus/evidence/round30/qr_harness.py:205-212`); `slow-ok` sleeps before every wire piece at `(DEADLINE - 0.8) / 6` (`:252-259`). Thus its seven waits take `7*(D-0.8)/6 > D` when `D > 5.6`, despite its in-deadline label claim (`corpus/evidence/round30/c2-count.py:43`). Run1 contains a `slow-ok` miss: DEADLINE 5.65, label VERBATIM, got UNREACHABLE, wall 5.82 (`CtlTrivialC2/receipt-do-nothing-c2-run1-v3.json:390-404`). [INFERENCE] That observed miss is consistent with the terminal-chunk timing defect; framing is not recorded in the receipt. No repair or extra runtime probe was built.

Do-nothing failing item kinds from `items`:
- Both runs: `drip-body` 3 and `drip-head` 2, no verdict, killed at 20.021–20.029 s, `bound_ok: false` (both v3 baseline receipts, `:75-148`).
- Both runs: `rebind-loop` 4 and `rebind-redirect` 2, correct verdict but connection to `127.0.0.1`; `rebind-private` 2, wrong UNREACHABLE verdict plus connection to `10.x`. All eight have `validated_only: false` (both receipts, `:240-373`).
- Run1 only: `drip-steady` 1, correct UNREACHABLE but wall 7.954 > bound 6.26 (`:164-178`); `slow-ok` 1 as above. Run2 has no misses in those two kinds. Accordingly the do-nothing result is 12/27 then 14/27, not a constant 13/27.

Restoration: no original or control code was changed. Pristine run1 preceded the other controls; unchanged-baseline run2 followed them. The original/copy and all four control hashes remain exactly the v2 hashes listed below. Formal killed-mutant classification is inconclusive because pristine already fails. Frozen v3 counter/harness hashes matched before and after scoring:

```text
c2-count.py    f68a2abc0139edcb87986334545a2d08711f150342ea77f667e11529fc0e69fe
qr_harness.py  16f17d60708952f9ba3d015eae306a075b37691deebf1e5c2c126137c6797ab7
```

All v3 counters were capped with `timeout 300`, seat-local TMPDIR and bytecode disabled. Scratch is empty; the final owned-process search found no counter/harness processes. No git/jj writes, source edits, external network fetches or installations.

## C2 design v2 — historical seat results

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| always-ABSENT | registry, fetching, text reading and judgment | not run, not run | 1/20, 1/20 | [run1](CtlTrivialC2/receipt-always-absent-c2-run1-v2.json), [run2](CtlTrivialC2/receipt-always-absent-c2-run2-v2.json) |
| always-VERBATIM | registry, fetching, text reading and judgment | not run, not run | 9/20, 9/20 | [run1](CtlTrivialC2/receipt-always-verbatim-c2-run1-v2.json), [run2](CtlTrivialC2/receipt-always-verbatim-c2-run2-v2.json) |
| always-UNREACHABLE, instant | all fetching; no waiting or source reading | not run, not run | 10/20, 10/20 | [run1](CtlTrivialC2/receipt-always-unreachable-c2-run1-v2.json), [run2](CtlTrivialC2/receipt-always-unreachable-c2-run2-v2.json) |
| junk five-way random | registry, fetching, text reading and judgment | not run, not run | 5/20, 5/20 | [run1](CtlTrivialC2/receipt-junk-c2-run1-v2.json), [run2](CtlTrivialC2/receipt-junk-c2-run2-v2.json) |
| do-nothing, byte-identical round-29 tool | the entire round-30 change | not run, not run | 9/20, 9/20 | [run1](CtlTrivialC2/receipt-do-nothing-c2-run1-v2.json), [run2](CtlTrivialC2/receipt-do-nothing-c2-run2-v2.json) |

META-CHECK: none met

This META-CHECK covers only this seat's v2 controls. The parent subsequently reported that `CtlShapeKeyed` met C2 v2; these results are history, not approval of that design. Receipts were renamed with `-v2` without changing their bytes (their `argv` retains the original output name). The v3 rescoring is recorded above.

Detector: frozen v2 `c2-count.py`, target `QUOTE_REOPEN_FETCH_BOUND_MATCH=20/20`. Every listed run printed that label with its table score, exited 1 and recorded `predicate_holds: false`; all ten seeds differ. No measurement failure. All four no-fetch controls completed every item within 0.146 s. The instant-UNREACHABLE control matches its frozen 10/20 ceiling; no design falsification was observed by this seat's controls.

Do-nothing failures from both receipts' `items` fields (same eleven misses in each):
- `drip-body`, `drip-chunked`, `drip-head`: two each; `got: null`, `killed: true`, `rc: -9`, wall 15.015–15.020 s, `bound_ok: false`. Evidence: `CtlTrivialC2/receipt-do-nothing-c2-run1-v2.json:76-151` and `receipt-do-nothing-c2-run2-v2.json:76-151`.
- `rebind-loop`: three; `rebind-redirect`: one. Correct `VERBATIM`, but `validated_only: false`, connecting to `127.0.0.1`. Evidence in both receipt files: `193-236` and `253-266`.
- `rebind-private`: one. `UNREACHABLE` instead of `VERBATIM`, plus `validated_only: false`: destination `10.118.218.165` in run1 and `10.43.172.233` in run2. Evidence in both receipt files: `238-251`.
The other nine items matched. Each receipt records the three required conditions separately as `verdict_ok`, `bound_ok` and `validated_only`.

Verdict: all five controls rejected. Formal killed-mutant classification is inconclusive, not killed, because the pristine baseline itself fails. The original was never modified: baseline run1 preceded the other controls, and unchanged-baseline run2 followed them. No contract-v2 repair was built.

Restoration evidence: SHA-256 before = after for every entry below; the original and do-nothing copy are byte-identical. Each run also records its candidate, counter and harness hashes.

```text
tools/quote-reopen.py = control-do-nothing.py  72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea
control-always-absent.py                     9eb7b25e726b8de619e3a02605c8720f0e5275b4bc2190221955062c1cb2ebea
control-always-verbatim.py                   4046dc4537332b7257518f6d1b90499a7e5e8e950dc1d498c6b4fd552a6e77f7
control-always-unreachable.py                709577c64a9514a251687bf4bede82f7181a6f23989d44fe89f18295d75e1188
control-junk.py                              bc4fbed65b56d5180dbc5ac36907b291ffe96723de482694499347df4b72a2da
c1-count.py                                 9a0a3bd7174be5772b9ea5af1667e6ec59e1583572f0776f93dac2a80c13131c
c2-count.py                                 7823eef53390a602f1d910117760649401e15c5fccb6f64e43f03d4e945d1674
qr_harness.py                               06237f36fb777d3e0bedf436be1f99507cc977188c4ac7767aa74374fff54764
```

Containment: all counters used `timeout 300`, seat-local `TMPDIR`, and `PYTHONDONTWRITEBYTECODE=1`. Scratch is empty; the final owned-process search found no remaining counter/harness processes. No git/jj writes, source edits, network fetches or tool installations.

## C2 design v4 — current seat results

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| always-ABSENT | registry, fetching, text reading and judgment | not run, not run | 14/27, not run | [run1](CtlTrivialC2/receipt-always-absent-c2-run1-v4.json) |
| always-VERBATIM | registry, fetching, text reading and judgment | not run, not run | 10/27, not run | [run1](CtlTrivialC2/receipt-always-verbatim-c2-run1-v4.json) |
| always-UNREACHABLE, instant | all fetching; no waiting or source reading | not run, not run | 11/27, not run | [run1](CtlTrivialC2/receipt-always-unreachable-c2-run1-v4.json) |
| junk five-way random | registry, fetching, text reading and judgment | not run, not run | 4/27, not run | [run1](CtlTrivialC2/receipt-junk-c2-run1-v4.json) |
| do-nothing, byte-identical round-29 tool | the entire round-30 change | not run, not run | 12/27, not run | [run1](CtlTrivialC2/receipt-do-nothing-c2-run1-v4.json) |

META-CHECK: none met

Exactly one run per control, as requested by the parent's v4 instruction. Detector target: `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`. All five counters printed that label with their table score, exited 1 and recorded `predicate_holds: false`; all five fresh seeds differ. No measurement failure. Every no-fetch-control item completed within 0.538 s with `bound_ok` and `validated_only` true.

Do-nothing failures from `receipt-do-nothing-c2-run1-v4.json`:
- `drip-body` 3 and `drip-head` 2: no verdict, killed at 20.025–20.031 s; `bound_ok: false` (`:75-148`).
- `drip-steady` 2: correct UNREACHABLE but wall 7.986/7.965 s exceeds bounds 6.36/6.54 s (`:149-178`).
- `rebind-loop` 4 and `rebind-redirect` 2: correct verdict, but connected to `127.0.0.1` (`:240-307`, `:342-373`).
- `rebind-private` 2: wrong UNREACHABLE instead of ABSENT, plus connections to `10.93.37.25` and `10.197.73.159` (`:308-341`).
All twelve other items matched, including both `slow-ok` items (`:390-419`). The v4 source sends the terminal chunk with the sixth body piece (`corpus/evidence/round30/qr_harness.py:252-263`) and uses `DEADLINE - 1.0` (`corpus/evidence/round30/c2-count.py:131-132`), replacing the v3 timing design.

Metadata caveat: the frozen v4 counter still emits the literal `design: v3` (`c2-count.py:218`). These are v4 measurements by their verified counter/harness hashes and `-v4` filenames; no receipt or counter bytes were corrected.

Restoration: original and all five control hashes matched their unchanged values above before and after v4 scoring; the original and do-nothing copy remain byte-identical (`72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`). No source/control mutation occurred. Formal mutation-kill classification remains inconclusive because pristine fails. Frozen v4 input hashes matched before and after:

```text
c1-count.py    5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6
c2-count.py    0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f
qr_harness.py  e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4
```

All five processes used `timeout 300`, seat-local TMPDIR and disabled bytecode. Scratch is empty and the owned-process search found no remaining counter/harness processes. All 25 versioned receipts are retained. No git/jj writes, source edits, external network fetches or installations.
