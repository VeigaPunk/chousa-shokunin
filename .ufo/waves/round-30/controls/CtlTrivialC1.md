# CtlTrivialC1 — C1-only pre-data controls

Axes: control rejection, repeatable evidence, byte containment.

Expected detector: frozen `timeout 300 python3 corpus/evidence/round30/c1-count.py --tool <control.py> --receipt <receipt.json>`; target `QUOTE_REOPEN_HEADLESS_MATCH=106/106`. Each actual stdout was `QUOTE_REOPEN_HEADLESS_MATCH=<score below>`. All ten counter exits were 1, all receipts have `predicate_holds=false` and `tool_killed=false`, and all ten counter seeds differ. C2 was not run.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| always-ABSENT (`always-absent.py`) | source reading and judging; constant all-false verdict | 60/106, 60/106 | unrun, unrun | [run1](CtlTrivialC1/receipt-always-absent-c1-run1.json), [run2](CtlTrivialC1/receipt-always-absent-c1-run2.json) |
| always-VERBATIM (`always-verbatim.py`) | source reading and judging; constant positive verdict | 40/106, 40/106 | unrun, unrun | [run1](CtlTrivialC1/receipt-always-verbatim-c1-run1.json), [run2](CtlTrivialC1/receipt-always-verbatim-c1-run2.json) |
| junk five-way (`junk-five-way.py`) | source reading and judging; independent uniform choice of all five verdicts | 18/106, 18/106 | unrun, unrun | [run1](CtlTrivialC1/receipt-junk-five-way-c1-run1.json), [run2](CtlTrivialC1/receipt-junk-five-way-c1-run2.json) |
| junk binary (`junk-binary.py`) | source reading and judging; independent uniform VERBATIM/ABSENT choice | 49/106, 53/106 | unrun, unrun | [run1](CtlTrivialC1/receipt-junk-binary-c1-run1.json), [run2](CtlTrivialC1/receipt-junk-binary-c1-run2.json) |
| do-nothing (`do-nothing.py`) | all round-30 changes; byte-identical round-29 tool | 78/106, 78/106 | unrun, unrun | [run1](CtlTrivialC1/receipt-do-nothing-c1-run1.json), [run2](CtlTrivialC1/receipt-do-nothing-c1-run2.json) |

META-CHECK: none met

No design finding from these assigned C1 controls. Exact per-item equality and the frozen-total gate are at `corpus/evidence/round30/c1-count.py:303-314`. The four trivial controls made zero connect events; each iterates input items in order and prints one four-field `QUOTE_REOPEN` line. Both junk controls use unseeded `random.SystemRandom().choice`, not fixture labels. No contract-v2 fix or partial fix was built. The pristine baseline itself misses; therefore a causal mutant-kill verdict is **inconclusive**, not a killed mutant.

## Before/after byte and restoration evidence

The three frozen SHA-256 values matched the assignment before scoring and after all runs. Every value below is identical **before = after**; every scored tool hash also matches its receipts. The original lane tool and its seat copy both match the required `72a3ad47...` prefix. Do-nothing run1 preceded the other controls; run2 followed them. No in-place source mutation occurred, so exact original bytes were preserved rather than needing restoration.

| bytes | SHA-256 before = after |
|---|---|
| `corpus/evidence/round30/c1-count.py` | `9a0a3bd7174be5772b9ea5af1667e6ec59e1583572f0776f93dac2a80c13131c` |
| `corpus/evidence/round30/c2-count.py` | `7823eef53390a602f1d910117760649401e15c5fccb6f64e43f03d4e945d1674` |
| `corpus/evidence/round30/qr_harness.py` | `06237f36fb777d3e0bedf436be1f99507cc977188c4ac7767aa74374fff54764` |
| `tools/quote-reopen.py` and `CtlTrivialC1/do-nothing.py` | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| `CtlTrivialC1/always-absent.py` | `108482beac39dd6b96b502babdaacabb510e7d4585c1512d8a1ed76f3d3da9da` |
| `CtlTrivialC1/always-verbatim.py` | `38eadbebf4ce5b229e2a8fab3023ee3a4a8c2ca2ea52d6ff8f99e8ac3cdba889` |
| `CtlTrivialC1/junk-five-way.py` | `d95776ea1a371ee91f69202ba4e4d5f2a188abe8ad9d018b674ad242c6935f0a` |
| `CtlTrivialC1/junk-binary.py` | `a14b0fa4b7823b0d785184118ccbdfb5e3178f9a31c0ce8cde437f89665469ec` |

Containment: scoring used `TMPDIR=/fast/scratch/hyaku/chousa-r30/CtlTrivialC1` and `PYTHONDONTWRITEBYTECODE=1`; scratch was empty afterward. All bounded scoring processes exited, and the final seat-specific Python process search returned no matches. No git/jj writes, network fetches, or tool installs/updates.

## Shared harness v3 re-score

At authorized freeze `7908ce2a6413522fc6fab63f284327693f70eec6`, each unchanged control was re-scored once on C1: always-ABSENT **60/106** ([receipt](CtlTrivialC1/receipt-always-absent-c1-h3.json)); always-VERBATIM **40/106** ([receipt](CtlTrivialC1/receipt-always-verbatim-c1-h3.json)); five-way junk **18/106** ([receipt](CtlTrivialC1/receipt-junk-five-way-c1-h3.json)); binary junk **51/106** ([receipt](CtlTrivialC1/receipt-junk-binary-c1-h3.json)); do-nothing **78/106** ([receipt](CtlTrivialC1/receipt-do-nothing-c1-h3.json)). Actual stdout retained the same `QUOTE_REOPEN_HEADLESS_MATCH=<score>` form; all five counter exits were 1, `predicate_holds=false`, `tool_killed=false`, and seeds were distinct from each other and all earlier runs. C2 remains unrun.

Before/after hashes matched the new freeze: C1 unchanged (`9a0a3bd7...c13131c`), C2 `f68a2abc0139edcb87986334545a2d08711f150342ea77f667e11529fc0e69fe`, harness `16f17d60708952f9ba3d015eae306a075b37691deebf1e5c2c126137c6797ab7`. All five control hashes and the lane tool hash remained exactly as in the earlier ledger; no restoration was needed. Scratch was empty and no seat-specific Python process remained.

META-CHECK: none met
