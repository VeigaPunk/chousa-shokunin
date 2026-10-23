# CtlNoReader — control evidence

## Historical C1 v2 / C2 v3

Paths are relative to `.ufo/waves/round-30/controls/CtlNoReader/`; `{1,2}` denotes both runs. This first section records 28 historical runs with distinct fresh seeds. Their hashes matched the respective assignments before scoring; C2/harness freeze was lane `7908ce2a6413522fc6fab63f284327693f70eec6` (`f68a2abc…c0e69fe` / `16f17d60…6797ab7`). The current v4 re-score is appended below.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| `fail-closed.py` | all DNS, fetching, parsing and matching; retains NO_SOURCE before TOO_LONG | 6/106, 6/106 | v3: 11/27, 11/27 | `receipt-fail-closed-c1-run{1,2}.json`; `receipt-fail-closed-c2-v3-run{1,2}.json` |
| `shape.py` | all DNS and page reading; guesses from quote length and interior capitals, singleton UNREACHABLE | 97/106, 89/106 | v3: 11/27, 11/27 | `receipt-shape-c1-run{1,2}.json`; `receipt-shape-c2-v3-run{1,2}.json` |
| `eight-absent.py` | same; singleton eight-word quotes guessed ABSENT | 91/106, 98/106 | v3: 8/27, 10/27 | `receipt-eight-absent-c1-run{1,2}.json`; `receipt-eight-absent-c2-v3-run{1,2}.json` |
| `relational.py` | all DNS/page reading; infers two body windows from within-source overlap, case, length and static fixture priors | 104/106, 102/106 | v3: 11/27, 11/27 | `receipt-relational-c1-run{1,2}.json`; `receipt-relational-c2-v3-run{1,2}.json` |

META-CHECK: none met

C1 was additionally scored once per control under the new harness: fail-closed **6/106**, shape **96/106**, eight-absent **96/106**, relational **104/106**. Receipts: `receipt-<control>-c1-h3.json`.

Historical C2 v2 scores: fail-closed 10/20, 10/20; shape 10/20, 10/20; eight-absent 10/20, 11/20; relational 10/20, 10/20. Receipts: `receipt-<control>-c2-v2-run{1,2}.json`; renamed only, with original argv preserved.

- **Best historical C1: 104/106**, `relational.py`, including h3 (`CtlNoReader/receipt-relational-c1-h3.json:100-114`). It still confused body/script windows but got all 28/28 headless body windows with zero connections (`:27-61,112-114`). Impacted axis: **coverage**. The pre-v4 shape/overlap leaks and their subsequent counter redesign are recorded in `corpus/evidence/round30/claims.md:5-15`; this historical control did not meet the frozen predicate.
- **Best historical C2 v3: 11/27**, tied by fail-closed, shape and relational in both runs (`CtlNoReader/receipt-relational-c2-v3-run1.json:481-485`). These singleton-UNREACHABLE policies missed all 16 fetchable items: rebind-loop/private/redirect, stable, slow-ok and multi-address. Eight-absent could guess some ABSENT labels but emitted no singleton VERBATIM. Impacted axis: **operability**. No C2 v3 defect was demonstrated by this seat.

Those 28 historical runs exited 1 with `predicate_holds: false`; no harness failure was scored as success. All C1 receipts logged zero connections. The four original controls stayed unchanged across freezes and implement none of contract v2 items 1–3. No tool installs, git/jj writes, or network fetches; scratch was confined with TMPDIR and bytecode writes disabled.

## Current design v4

Freeze: lane `abfdf93274d0c70e02465e22abcf029dea59efb9`. Before scoring, SHA-256 matched C1 `5b312d84…9d6e6`, C2 `0a59e373…f88f`, harness `e2be0dd1…50d4`. The original `relational.py` is preserved for historical hash provenance; the strengthened item-only posterior is a separate `relational-v4.py`.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| `fail-closed.py` | all DNS, fetching, parsing and matching; only local NO_SOURCE/TOO_LONG, then UNREACHABLE | 6/106, 6/106 | 11/27, 11/27 | `receipt-fail-closed-c1-v4-run{1,2}.json`; `receipt-fail-closed-c2-v4-run{1,2}.json` |
| `shape.py` | all reading; original length/interior-capital guesses | 63/106, 66/106 | 11/27, 11/27 | `receipt-shape-c1-v4-run{1,2}.json`; `receipt-shape-c2-v4-run{1,2}.json` |
| `eight-absent.py` | same; singleton eight-word quotes guessed ABSENT | 65/106, 66/106 | 14/27, 10/27 | `receipt-eight-absent-c1-v4-run{1,2}.json`; `receipt-eight-absent-c2-v4-run{1,2}.json` |
| `relational.py` | all reading; unchanged pre-v4 overlap/shape posterior | 70/106, 69/106 | 11/27, 11/27 | `receipt-relational-c1-v4-run{1,2}.json`; `receipt-relational-c2-v4-run{1,2}.json` |
| `relational-v4.py` | all reading; v4 body/head/case-toggle posterior using quote-only case/length priors and supplied overlong-quote overlap | 79/106, 84/106 | 11/27, 11/27 | `receipt-relational-v4-c1-v4-run{1,2}.json`; `receipt-relational-v4-c2-v4-run{1,2}.json` |

META-CHECK: none met

- **Best v4 C1: 84/106**, strengthened relational run 2 (`CtlNoReader/receipt-relational-v4-c1-v4-run2.json:212-220`), zero connections. It still misses body windows in all four document classes and confuses title/script/case-flip items (`:100-210`); only 18/28 headless body windows match. **Coverage** caveat, not a met predicate: v4 retains different body/head span lengths (50–60 versus 10–14), so initial-capital and 11/12-word sampling probabilities differ (`corpus/evidence/round30/c1-count.py:92-95,148-151,183-186`). A case swap can also produce case patterns impossible for ordinary generated words (`:80-87,209-215`), and the overlong reachable-body quote can overlap ordinary windows despite their mutual disjointness (`:269-290`). [INFERENCE] Smallest safe correction, if further hardening is wanted: equalize complete observable quote-generation distributions and isolate the overlong companion; do not rescale the target.
- **Best v4 C2: 14/27**, eight-absent run 1 (`CtlNoReader/receipt-eight-absent-c2-v4-run1.json:481-487`); run 2 is 10/27. The 14 consists of all 11 fixed UNREACHABLE items plus three ABSENT guesses, not observed page outcomes. No control emits singleton VERBATIM, so none can reach VERBATIM items in rebind-loop/private/redirect, stable, slow-ok or multi-address. **Operability**: no v4 target-met counterexample demonstrated.
- **Provenance note:** frozen v4 C2 still writes `design: \"v3\"` (`corpus/evidence/round30/c2-count.py:218`). Receipts are unmodified; their exact counter/harness hashes and `*-v4*` filenames identify this re-score. Smallest safe correction is to label this discrepancy in downstream evidence rather than silently treating that field as v4.

All 20 v4 runs used distinct fresh seeds and exited 1 with `predicate_holds: false`; no harness failure was scored. All ten v4 C1 receipts log zero connections. All controls open only the two supplied text inputs, never resolve/connect, and implement none of contract v2 items 1–3. All started processes completed; no installs or writes outside the permitted seat/report/scratch locations.

