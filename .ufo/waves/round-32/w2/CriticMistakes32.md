# CriticMistakes32 — round-32 mistake-mining falsification

**Scoped verdict: BROKEN — the R1 check does not accept the landed append-only correction, and the C1 mistake row cites a base-gate receipt as probe-only evidence.** The sampled landed C1/C2 counters did not miss their targets. These are fixable evidence/recheck defects, not a canonical round judgment or an axis tradeoff.

**Axes:** operability (a runnable check separates the mistake from its correction); coverage (negative controls cover multiplicity, record verdicts, locking and fixture layout).

All paths below are lane-relative. Let `A=.ufo/waves/round-32/w2/CriticMistakes32/`. Exact commands, observed exits and key output are retained in `A/commands-results.md`; C1/R1/layout argv and outputs also have individual `*.log.json` files. No production files, index, jj state, fleet files or sibling files were changed.

## F1 — the R1 fix fails its own cited focused check

- Target: `corpus/lessons/round-32.md:50`, `corpus/QUALITY.md:252-257`, and the executable check at `.ufo/waves/round-32/w1/ScribeQualityR1/quality.md:11`.
- Ran that check's logic on a scratch copy of base `7a7259f0`'s uncorrected round-31 lesson and receipts, then on the landed append-corrected copy. The positive fixture was byte-bound to `5d8a1707:corpus/lessons/round-31.md`: both SHA-256 values were `a437466e7ec2135b9e19ae6b0e60de93d5e53a69f8c06c092a7d0676948628ac` (`A/commands-results.md`, Identity commands).
- Both runs exited **1** with identical output: `FAIL: round-31.md:98 calls fail-open counter-killed; receipt citations missing; all-match receipts: …=120/120, …=120/120`. Each was repeated once to retain logs; all four R1 executions are disclosed in `A/r1-before.log.json:20-22`, `A/r1-after.log.json:20-22`, and `A/commands-results.md`.
- The correction is real and explicit (`corpus/lessons/round-31.md:118-129`), but the checker still treats the preserved historical bullet at lines 95-100 as an active kill claim. Its selection never resolves the appended correction. `corpus/QUALITY.md:6` requires append-only errata, so rewriting away that old bullet is not a safe positive-path fix.
- **Smallest safe correction:** retain the historical bytes, make this focused check recognize and validate the named R1 supersession against its exact receipts, and retain a failing uncorrected fixture plus a passing append-corrected fixture. The current evidence truly demonstrates a negative failure; it does **not** demonstrate a discriminating post-fix recheck. The scribe already limits its parser's generality (`quality.md:25-27`); this finding concerns its exact R1 case, not a new generic Markdown requirement.

## F2 — the cited C1 proof has false control provenance

- `corpus/lessons/round-32.md:51` and `corpus/QUALITY.md:258-264` point to `controls/L1-design-v2/c1-probeonly-s3201.json` as evidence that the **same probe-only control** scores 0/24 under v2.
- That receipt's `gate_sha256` is **BASE `0bc318b3…1258`**, not the probe-only mutant (`.ufo/waves/round-32/controls/L1-design-v2/c1-probeonly-s3201.json:5-15`). A read-only `git show 5d8a1707:.ufo/waves/round-32/controls/L1-design-v2/c1-probeonly-control-gate.sh | sha256sum` also produced BASE, exit 0. Thus this particular receipt cannot establish the claimed probe-only discrimination.
- Reconstructed the genuine control from `w1/CtlC1PartialLockB/b-probe-only.patch:3-25` in this seat's scratch tree. Its SHA-256 was `034f786be1570136b27d72ec630e24be1c6a673ce53434d476af94f4bb5f0340`, matching the genuine historical mutant. The unmodified v2 counter rejected it **0/24**, exit 1; the landed gate passed **24/24**, exit 0 (`A/control-probeonly-c1-v2-s323211.json`, `A/candidate-c1-v2-s323212.json`).
- **Smallest safe correction:** repoint the lesson and QUALITY 34 proof to genuine existing receipts, e.g. `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-b-probe-only-s32472021.json:5-15` (hash `034f786b…`, 0/24), and explicitly reject the mislabeled L1 receipt as probe-only evidence. Do not change the frozen counter or target. The mechanism works in this check; its selected provenance is wrong. Existing QUALITY 15 already requires byte/revision binding (`corpus/QUALITY.md:77-84`).

## F3 — existing QUALITY criteria already cover the C2 v1 mistake

**Yes for the C2 construction defect, but not as a claim that v1 freezing itself violated the control-wave timing rule.** Read-only `git show 4111607c:corpus/QUALITY.md` exited 0; its unmodified file is preserved as `A/quality-at-v1.md`.

- **QUALITY 20**, already at v1 freeze, explicitly requires finding multiplicity and says a code-set comparison cannot detect invented duplicates (`A/quality-at-v1.md:124-131`). This directly covers C2 v1's de-duplication mistake.
- **QUALITY 19**, likewise pre-existing, keeps expected exit, diagnostics and verdict-record checks separate and requires negative controls for wrong exits/absent records (`A/quality-at-v1.md:117-123`). This covers the omitted record-verdict checks. The lesson's captured-by cell mentions only QUALITY 32's finding-set limit (`corpus/lessons/round-32.md:52`), omitting the stronger applicable criteria.
- **QUALITY 24** requires frozen-counter control scoring and redesign **before data**, not before the first provisional freeze (`A/quality-at-v1.md:159-168`). The recorded v1→v2 control-wave redesign follows that timing (`corpus/evidence/round32/claims.md:119-140,184-189`); a bad provisional v1 is not by itself a violation of 24. QUALITY 17 is also a broad pre-existing negative-control requirement (`A/quality-at-v1.md:93-100`), while QUALITY 34 adds the specifically forced race window.
- Reproduced the C2 issue independently: duplicate-only scored **120/120** under v1 but **96/132** under v2; a review-only wrapper stripping just the verdict summary scored **120/120** under v1 but **0/132** under v2 with `drift-summary-lines=0`. The underlying landed output scored **132/132** (`A/commands-results.md`; receipt inventory below).
- **Smallest safe correction:** identify 19/20 as existing criteria that should have rejected the incomplete C2 counter at design review, distinguish that missed application from QUALITY 24's successfully operating pre-data control wave, and do not invent a duplicate new criterion for multiplicity/verdict checking.

## All fix checks and every counter invocation

| Mistake/fix | Observed bad/control input | Corrected input | Result |
|---|---|---|---|
| R1 receipt-backed attribution | Historical text: exit 1 | Append-corrected text: exit 1, identical diagnostic | Not discriminating; F1 |
| C1 forced write window | Genuine probe-only gate: v2 0/24, exit 1 | Landed gate: v2 24/24, exit 0 | Mechanism discriminates; cited provenance fails F2 |
| C2 finding multiplicity + verdict | Duplicate v2 96/132; no-verdict v2 0/132; both exit 1 | Landed gate: v2 132/132, exit 0 | Discriminates both named defects |
| C2 layout guard | C2_TMP deliberately inside scratch lane root: exit 2, no count | External temp directory: 132/132, exit 0 | Guard discriminates layout; it does not validate a receipt's gate identity |

All counter receipts below are in `A/`. V1 counters and all controls are **not** candidate measurements.

| Receipt / log basename | Gate class | Seed | Counter | Count | Exit |
|---|---|---:|---|---:|---:|
| `control-duplicate-c2-v2-s323201.json` | duplicate-only control | 323201 | C2 v2 | 96/132 | 1 |
| `control-duplicate-c2-v1-s323201.json` | same control | 323201 | C2 v1 | 120/120 | 0 |
| `candidate-c2-v2-s323202.json` | landed `10f2fe12…` | 323202 | C2 v2 | 132/132 | 0 |
| `control-probeonly-c1-v2-s323211.json` | genuine probe-only control | 323211 | C1 v2 | 0/24 | 1 |
| `candidate-c1-v2-s323212.json` | landed `10f2fe12…` | 323212 | C1 v2 | 24/24 | 0 |
| `candidate-c2-v2-layout-refusal-s323203.log.json` | landed, intentionally invalid harness layout | 323203 | C2 v2 | none; harness refusal, no receipt emitted | 2 |
| `control-probeonly-c1-v1-s323211.json` | genuine probe-only control | 323211 | C1 v1 | **23/24** | 1 |
| `control-no-verdict-c2-v1-s323204.json` | verdict-stripping control | 323204 | C2 v1 | 120/120 | 0 |
| `control-no-verdict-c2-v2-s323204.json` | same control | 323204 | C2 v2 | 0/132 | 1 |

The fresh C1 v1 control run scored 23/24, not the historical 24/24. It does not independently reproduce that historical accidental pass; it is disclosed without rerolling. The valid landed runs are one seed per counter, so this seat does not establish the full two-fresh-seed round predicates or census every other seat's runs. The deliberate layout refusal is not a below-target P2 receipt.

## Limits and safety

Scope was the four current Mistakes rows and their cited QUALITY fixes. No source URL was opened; no selftest/build or canonical judge/runtime was invoked. No install or update. Shell experiments were timeout-bounded, scoring used `prlimit --nproc=8000 --fsize=1048576`, and C1 had at most two simultaneous counters. All experiment subprocesses completed; the final targeted `pgrep` returned exit 1 with no output (`A/commands-results.md`). Experiments stayed in this seat's `/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/`; retained evidence stayed in `A/`. No P1/P2 target miss was observed on a valid landed-gate run in this scoped review.
