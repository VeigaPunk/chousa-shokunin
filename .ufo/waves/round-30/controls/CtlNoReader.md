# CtlNoReader — C1 v2 / C2 v3 controls

Paths below are relative to `.ufo/waves/round-30/controls/CtlNoReader/`; `{1,2}` denotes both runs. All 28 runs used distinct fresh seeds. Frozen hashes matched the respective assignments before scoring; current C2/harness freeze is lane `7908ce2a6413522fc6fab63f284327693f70eec6` (`f68a2abc…c0e69fe` / `16f17d60…6797ab7`).

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| `fail-closed.py` | all DNS, fetching, parsing and matching; retains NO_SOURCE before TOO_LONG | 6/106, 6/106 | v3: 11/27, 11/27 | `receipt-fail-closed-c1-run{1,2}.json`; `receipt-fail-closed-c2-v3-run{1,2}.json` |
| `shape.py` | all DNS and page reading; guesses from quote length and interior capitals, singleton UNREACHABLE | 97/106, 89/106 | v3: 11/27, 11/27 | `receipt-shape-c1-run{1,2}.json`; `receipt-shape-c2-v3-run{1,2}.json` |
| `eight-absent.py` | same; singleton eight-word quotes guessed ABSENT | 91/106, 98/106 | v3: 8/27, 10/27 | `receipt-eight-absent-c1-run{1,2}.json`; `receipt-eight-absent-c2-v3-run{1,2}.json` |
| `relational.py` | all DNS/page reading; infers two body windows from within-source overlap, case, length and static fixture priors | 104/106, 102/106 | v3: 11/27, 11/27 | `receipt-relational-c1-run{1,2}.json`; `receipt-relational-c2-v3-run{1,2}.json` |

META-CHECK: none met

C1 was additionally scored once per control under the new harness: fail-closed **6/106**, shape **96/106**, eight-absent **96/106**, relational **104/106**. Receipts: `receipt-<control>-c1-h3.json`.

Historical C2 v2 scores: fail-closed 10/20, 10/20; shape 10/20, 10/20; eight-absent 10/20, 11/20; relational 10/20, 10/20. Receipts: `receipt-<control>-c2-v2-run{1,2}.json`; renamed only, with original argv preserved.

- **Best C1: 104/106**, `relational.py`, including the new harness (`CtlNoReader/receipt-relational-c1-h3.json:100-114`). It still confuses short body and script windows; the earlier second run also confuses headless-body body/title. The new-harness run nevertheless gets all **28/28 headless body windows** with zero connections (`:27-61,112-114`). Impacted axis: **coverage**; this is a fixable fixture-leak caution, not a met frozen predicate. Body lengths 6–15 versus head lengths 4–8, guaranteed interior capitals in case flips, and companion-window overlap expose labels (`corpus/evidence/round30/c1-count.py:186-194,223-229`). [INFERENCE] Smallest safe counter-design correction: equalize observable quote shapes and remove companion-window answer leakage; do not lower or rescale the target.
- **Best current C2: 11/27**, tied by fail-closed, shape and relational in both runs (`CtlNoReader/receipt-relational-c2-v3-run1.json:481-485`). These singleton-UNREACHABLE policies miss all 16 fetchable items: rebind-loop/private/redirect, stable, slow-ok and multi-address. Eight-absent can guess some ABSENT labels but emits no singleton VERBATIM at all. Impacted axis: **operability**. v3 gives both quote labels the same 6–12-word generator and randomizes their truth independently of transport class (`corpus/evidence/round30/c2-count.py:119-128`); without page/DNS observations, these controls cannot establish those outcomes. No C2 v3 defect was demonstrated by this seat.

All 28 scored runs exited 1 with `predicate_holds: false`; no harness failure was scored as success. All C1 receipts log zero connections. Controls only open the supplied registry/items files and implement none of contract v2 items 1–3; their code stayed unchanged across freezes. No tool installs, git/jj writes, or network fetches. TMPDIR confined scratch, bytecode writes were disabled, and all started scoring processes completed.
