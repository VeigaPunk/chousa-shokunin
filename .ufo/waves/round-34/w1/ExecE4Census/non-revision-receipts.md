# Non-revision receipts (E4) — round-33 and round-32 unbound census

Draft for the E4 repair (`corpus/lessons/round-33-verifier-spotcheck.md:168-171`): "never cite a receipt whose `gate_sha256` is not a committed blob, and re-run any measurement after a scratch edit".

Every receipt listed below records a `gate_sha256` that matches **no committed blob** in `/home/vgpnk/Projects/shokunin/chousa-shokunin` (gate revisions across `git rev-list --all` plus every committed `*.sh` under `.ufo/waves/`). Each such receipt was measured on scratch/worktree bytes that were never committed, so it is **non-revision (uncommitted gate bytes); not evidence for any landed claim**.

Census tool: `.ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py` (sha256 `230441acc1103d350780507c36993d87d550ea4b6602a373ad081dcf744c5943`). Outputs: `census-round33.txt` (exit 1), `census-round32.txt` (exit 1), `census-round33.json`.

## Round 33 — 9 unbound receipts (exit 1: 6 carry a landed/final label)

| receipt | gate_sha256 | gate path | label | counter_sha256 | utc | disposition |
|---|---|---|---|---|---|---|
| `.ufo/waves/round-33/measure/final/fz-90212.json` | `b2c07edae3a4…` | `—` | `—` | `—` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/measure/final/fz-90213.json` | `b2c07edae3a4…` | `—` | `—` | `—` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/measure/final/fz-90214.json` | `b2c07edae3a4…` | `—` | `—` | `—` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34101.json` | `fc08410ea00f…` | `tools/research-gate.sh` | `TOPLEVEL_FIELD_MATCH=156/156` | `cb354dd1b5bd` | 2026-10-23T09:10:09Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34102.json` | `45d76b4fc7c5…` | `tools/research-gate.sh` | `TOPLEVEL_FIELD_MATCH=156/156` | `cb354dd1b5bd` | 2026-10-23T09:10:31Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/ProbeTypes33/c1-landed-s4202.json` | `45d76b4fc7c5…` | `tools/research-gate.sh` | `TOPLEVEL_FIELD_MATCH=156/156` | `cb354dd1b5bd` | 2026-10-23T09:10:27Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/FuzzDiff33/full-90214.json` | `45d76b4fc7c5…` | `—` | `—` | `—` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/ProbeLongLines33/c1-v2-seed5187.json` | `45d76b4fc7c5…` | `tools/research-gate.sh` | `TOPLEVEL_FIELD_MATCH=156/156` | `cb354dd1b5bd` | 2026-10-23T09:10:30Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json` | `b808e9b5e6d3…` | `tools/research-gate.sh` | `TOPLEVEL_FIELD_MATCH=0/156` | `cb354dd1b5bd` | 2026-10-23T09:10:50Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |

### Round-33 notes, per receipt

- `.ufo/waves/round-33/measure/final/fz-90212.json` — The E1 able-to-fail case. `b2c07eda…` is a scratch state of the L1 gate overwritten at 06:23:31-03:00 by the bytes that became `43a1af35`; the receipt carries no `gate` path at all, only the orphan digest. Cited by the round-33 report (§Before → after), the SCORECARD capability row and `corpus/knowledge/claim-record-fields-r33.md:65-66` as "on the final gate".
- `.ufo/waves/round-33/measure/final/fz-90213.json` — Same orphan digest `b2c07eda…`; same defect as E1.
- `.ufo/waves/round-33/measure/final/fz-90214.json` — Same orphan digest `b2c07eda…`; same defect as E1.
- `.ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34101.json` — Gate path is the live worktree `tools/research-gate.sh`; the worktree held `fc08410e…` at 09:10:09Z, a state in no commit. File name carries the `c1-landed` label the E4 defect names.
- `.ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34102.json` — Live-worktree run at 09:10:31Z on `45d76b4f…`, a state in no commit. `c1-landed` label.
- `.ufo/waves/round-33/w2/ProbeTypes33/c1-landed-s4202.json` — Live-worktree run at 09:10:27Z on `45d76b4f…`; `ProbeTypes33.md:34` already prints the digest in bold. `c1-landed` label.
- `.ufo/waves/round-33/w2/FuzzDiff33/full-90214.json` — Fuzz receipt on `45d76b4f…`; `FuzzDiff33.md:60` already discloses it as a working-tree state in no commit. Attack evidence only.
- `.ufo/waves/round-33/w2/ProbeLongLines33/c1-v2-seed5187.json` — Live-worktree run at 09:10:30Z on `45d76b4f…`; `ProbeLongLines33.md:105-120` (F2) already discloses the defect. The pinned sibling `c1-v2-seed5188-pinned.json` binds `94a7be5a…` and is bound.
- `.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json` — Gate digest `b808e9b5…`, a state in no commit; `ReviewC1Diff.md:15` already marks it "(NOT landed)".

### Round-33 receipts that are bound (no action)

Of the 1060 JSON receipts under `.ufo/waves/round-33/`: 634 carry a `gate_sha256` field (625 bound, 9 unbound — the table above); 341 carry only `gate_sha256_before`/`gate_sha256_after` (every one of those digests is bound, so no action); 42 carry no gate digest at all; 43 are non-receipt JSON objects (lists or objects without digest fields). Bound total 966. The landed-evidence receipts `measure/final/c1v2-s370{1,2}.json` and `measure/final/c2v3-s370{3,4}.json` bind `43a1af35…`, which **is** the committed tip blob (`git rev-list --all` → blob `eebec67f13…`), so they are bound and remain citable.

## Round 32 — 381 unbound receipts (exit 1: 18 carry a landed/final label)

Same census over `.ufo/waves/round-32/`; only 19 `*.sh` files under that round were ever committed, so nearly every wave-2 mutant/probe gate copy lives in scratch only. The 18 landed/final-labelled rows are listed individually; the remaining 363 rows are mutant/attack evidence and are enumerated by digest in the appendix.

| receipt | gate_sha256 | gate path | label | counter_sha256 | utc | disposition |
|---|---|---|---|---|---|---|
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322228.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=24/24` | `9a61b1578221` | 2026-10-23T06:56:26Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322228.run.json` | `cf1f234e2dff…` | `—` | `—` | `9a61b1578221` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322229.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=24/24` | `9a61b1578221` | 2026-10-23T06:56:26Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322229.run.json` | `cf1f234e2dff…` | `—` | `—` | `9a61b1578221` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322228.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=0/24` | `9e787e80b215` | 2026-10-23T06:54:01Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322228.run.json` | `cf1f234e2dff…` | `—` | `—` | `9e787e80b215` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322229.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=0/24` | `9e787e80b215` | 2026-10-23T06:54:02Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322229.run.json` | `cf1f234e2dff…` | `—` | `—` | `9e787e80b215` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322228.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=0/24` | `9e787e80b215` | 2026-10-23T06:57:43Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322228.run.json` | `cf1f234e2dff…` | `—` | `—` | `9e787e80b215` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322229.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/gate-final-newline.sh` | `APPEND_SERIALIZED=0/24` | `9e787e80b215` | 2026-10-23T06:57:44Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322229.run.json` | `cf1f234e2dff…` | `—` | `—` | `9e787e80b215` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322518.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/v2-final-newline/tools/research-gate.sh` | `APPEND_SERIALIZED=0/24` | `e6bf95313ad6` | 2026-10-23T07:13:55Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322518.run.json` | `cf1f234e2dff…` | `—` | `—` | `e6bf95313ad6` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322519.json` | `cf1f234e2dff…` | `/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/v2-final-newline/tools/research-gate.sh` | `APPEND_SERIALIZED=0/24` | `e6bf95313ad6` | 2026-10-23T07:13:56Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322519.run.json` | `cf1f234e2dff…` | `—` | `—` | `e6bf95313ad6` | — | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC2b/c2-landed-runA.json` | `3ceb0a80f04f…` | `tools/research-gate.sh` | `EXEMPT_AUDIT_MATCH=132/132` | `8ec1a1ed44f1` | 2026-10-23T07:34:01Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC2b/c2-landed-runB.json` | `3ceb0a80f04f…` | `tools/research-gate.sh` | `EXEMPT_AUDIT_MATCH=132/132` | `8ec1a1ed44f1` | 2026-10-23T07:34:01Z | non-revision (uncommitted gate bytes); not evidence for any landed claim |

### Round-32 appendix — all 381 unbound receipts (every row carries the same disposition)

| receipt | gate_sha256 | disposition |
|---|---|---|
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322228.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322228.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322229.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-mutant-counter-s322229.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322228.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322228.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322229.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-pristine-s322229.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322228.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322228.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322229.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/final-newline-restored-s322229.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322518.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322518.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322519.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/final-newline-s322519.run.json` | `cf1f234e2dff…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC2b/c2-landed-runA.json` | `3ceb0a80f04f…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC2b/c2-landed-runB.json` | `3ceb0a80f04f…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CriticPredicateGaps32b/c1-label-s320201.json` | `101afefc4f61…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CriticPredicateGaps32b/c1-label-s320202.json` | `101afefc4f61…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CriticPredicateGaps32b/c2-presentation-isolated-s320212.json` | `c9d2eee907cd…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CriticPredicateGaps32b/c2-presentation-isolated-s320213.json` | `c9d2eee907cd…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CriticPredicateGaps32b/c2-presentation-s320211.json` | `ac7bedd52121…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/always-newline-s3365157087.json` | `61e2e1122c0d…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/always-newline-s709508655.json` | `61e2e1122c0d…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/junk-line-s1772269673.json` | `6c2053e16366…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/junk-line-s4002894681.json` | `6c2053e16366…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/no-append-s1849101119.json` | `7e98299ae624…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/no-append-s660714253.json` | `7e98299ae624…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/rewrite-rename-s2735497235.json` | `162396737667…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/rewrite-rename-s2769961969.json` | `162396737667…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/always-newline-s4091295572.json` | `61e2e1122c0d…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/always-newline-s668434059.json` | `61e2e1122c0d…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/junk-line-s2660296547.json` | `6c2053e16366…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/junk-line-s3208011672.json` | `6c2053e16366…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/no-append-s1571745372.json` | `7e98299ae624…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/no-append-s3031817921.json` | `7e98299ae624…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/rewrite-rename-s2712189448.json` | `162396737667…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/rewrite-rename-s3169471396.json` | `162396737667…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/a-s20261023320121.json` | `2b1f52fdf528…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/a-s20261023320122.json` | `2b1f52fdf528…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/b-s20261023320131.json` | `591cc341c508…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/b-s20261023320132.json` | `591cc341c508…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/c-s20261023320141.json` | `46a6e487a423…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1JitterB/c-s20261023320142.json` | `46a6e487a423…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/a-s32471011.json` | `4a39b99728ec…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/a-s32471012.json` | `4a39b99728ec…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/c-s32471033.json` | `59ea2a22bc72…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/c-s32471034.json` | `59ea2a22bc72…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/d-s32471043.json` | `76c4c073bb59…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/d-s32471044.json` | `76c4c073bb59…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-a-append-only-s32472011.json` | `4a39b99728ec…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-a-append-only-s32472012.json` | `4a39b99728ec…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-c-cached-probe-s32472031.json` | `59ea2a22bc72…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-c-cached-probe-s32472032.json` | `59ea2a22bc72…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-d-shared-lock-s32472041.json` | `76c4c073bb59…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-d-shared-lock-s32472042.json` | `76c4c073bb59…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/mkdir-spin-s5985335950195587660.command.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/mkdir-spin-s5985335950195587660.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/mkdir-spin-s9091431053534308447.command.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/mkdir-spin-s9091431053534308447.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/per-process-flock-s1519897881203437156.command.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/per-process-flock-s1519897881203437156.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/per-process-flock-s4661176348059719223.command.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/per-process-flock-s4661176348059719223.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/posix-lockf-s7774156660351681216.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/posix-lockf-s7774156660351681216.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/posix-lockf-s8068104468809364743.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/posix-lockf-s8068104468809364743.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/sibling-flock-s6215270098090743748.command.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/sibling-flock-s6215270098090743748.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/sibling-flock-s7199539608062276134.command.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/sibling-flock-s7199539608062276134.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/mkdir-spin-s2446386726986300289.command.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/mkdir-spin-s2446386726986300289.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/mkdir-spin-s6013957116027521829.command.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/mkdir-spin-s6013957116027521829.json` | `13f387cf3095…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/per-process-flock-s4497807281718331427.command.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/per-process-flock-s4497807281718331427.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/per-process-flock-s8813274439468374557.command.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/per-process-flock-s8813274439468374557.json` | `f02db76766f2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s115068134866061245.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s1611102174911494980.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s1611102174911494980.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s2301002376000482972.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s3931168057388379246.command.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/posix-lockf-s3931168057388379246.json` | `bf1b9c06f050…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/sibling-flock-s1164394067745934815.command.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/sibling-flock-s1164394067745934815.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/sibling-flock-s3654444391053792470.command.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/sibling-flock-s6942719030958574319.command.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/sibling-flock-s6942719030958574319.json` | `cddd8cae7556…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/ExecR2CounterV3/mutC2Parse.c1.json` | `f9da8257da57…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/ExecR2CounterV3/mutC2Parse.c2.json` | `f9da8257da57…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/ExecR2CounterV3/mutC2Parse.c2.s2.json` | `f9da8257da57…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-mutant-counter-s322222.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-mutant-counter-s322222.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-mutant-counter-s322223.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-mutant-counter-s322223.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-pristine-s322222.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-pristine-s322222.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-pristine-s322223.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-pristine-s322223.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-restored-s322222.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-restored-s322222.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-restored-s322223.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/blank-line-restored-s322223.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-mutant-counter-s322210.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-mutant-counter-s322210.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-mutant-counter-s322211.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-mutant-counter-s322211.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-s322210.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-s322210.run.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-s322211.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-s322211.run.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-v2-s322210.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-v2-s322210.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-v2-s322211.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-pristine-v2-s322211.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-restored-s322210.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-restored-s322210.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-restored-s322211.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/hold-restored-s322211.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-mutant-counter-s322216.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-mutant-counter-s322216.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-mutant-counter-s322217.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-mutant-counter-s322217.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-s322216.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-s322216.run.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-s322217.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-s322217.run.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-v2-s322216.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-v2-s322216.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-v2-s322217.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-pristine-v2-s322217.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-restored-s322216.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-restored-s322216.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-restored-s322217.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/inode-restored-s322217.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-mutant-counter-s322224.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-mutant-counter-s322225.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-pristine-s322224.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-pristine-s322224.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-pristine-s322225.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-pristine-s322225.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-restored-s322224.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-restored-s322224.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-restored-s322225.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/json-object-restored-s322225.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-mutant-counter-s322220.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-mutant-counter-s322220.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-mutant-counter-s322221.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-mutant-counter-s322221.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-pristine-s322220.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-pristine-s322220.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-pristine-s322221.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-pristine-s322221.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-restored-s322220.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-restored-s322220.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-restored-s322221.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/line-count-restored-s322221.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/oracle-s322201.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/oracle-s322201.run.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/oracle-s322202.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/oracle-s322202.run.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-mutant-counter-s322226.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-mutant-counter-s322226.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-mutant-counter-s322227.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-mutant-counter-s322227.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-pristine-s322226.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-pristine-s322226.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-pristine-s322227.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-pristine-s322227.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-restored-s322226.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-restored-s322226.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-restored-s322227.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/schema-restored-s322227.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-mutant-counter-s322218.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-mutant-counter-s322218.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-mutant-counter-s322219.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-mutant-counter-s322219.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-pristine-s322218.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-pristine-s322218.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-pristine-s322219.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-pristine-s322219.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-restored-s322218.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-restored-s322218.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-restored-s322219.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/seed-prefix-restored-s322219.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-mutant-counter-s322212.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-mutant-counter-s322212.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-mutant-counter-s322213.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-mutant-counter-s322213.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-pristine-s322212.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-pristine-s322212.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-pristine-s322213.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-pristine-s322213.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-restored-s322212.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-restored-s322212.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-restored-s322213.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/waiter-restored-s322213.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-mutant-counter-s322214.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-mutant-counter-s322214.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-mutant-counter-s322215.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-mutant-counter-s322215.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-pristine-s322214.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-pristine-s322214.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-pristine-s322215.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-pristine-s322215.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-restored-s322214.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-restored-s322214.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-restored-s322215.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/writer-rc-restored-s322215.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/blank-line-s322512.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/blank-line-s322512.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/blank-line-s322513.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/blank-line-s322513.run.json` | `016bca0b7fe5…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-initial-s322520.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-initial-s322520.run.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-initial-s322521.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-initial-s322521.run.json` | `dfbb56686ce7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-s322500.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-s322500.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-s322501.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/hold-s322501.run.json` | `971cdda669e0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-initial-s322522.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-initial-s322522.run.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-initial-s322523.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-initial-s322523.run.json` | `25114e4695f7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-s322506.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-s322506.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-s322507.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/inode-s322507.run.json` | `5096cf85d9ce…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/json-object-s322514.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/json-object-s322514.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/json-object-s322515.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/json-object-s322515.run.json` | `e712c76c5723…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/line-count-s322510.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/line-count-s322510.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/line-count-s322511.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/line-count-s322511.run.json` | `daf9cd007034…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/oracle-s322524.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/oracle-s322524.run.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/oracle-s322525.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/oracle-s322525.run.json` | `b00c40d4d6be…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/schema-s322516.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/schema-s322516.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/schema-s322517.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/schema-s322517.run.json` | `719064c35276…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/seed-prefix-s322508.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/seed-prefix-s322508.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/seed-prefix-s322509.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/seed-prefix-s322509.run.json` | `1b3cf2838cf0…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/waiter-s322502.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/waiter-s322502.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/waiter-s322503.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/waiter-s322503.run.json` | `62d9b76cc532…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/writer-rc-s322504.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/writer-rc-s322504.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/writer-rc-s322505.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC1CounterB/v2/writer-rc-s322505.run.json` | `d2aeebf79ed2…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-clean-exit-s320260230271.json` | `cf0bc25d1730…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-clean-exit-s320260230283.json` | `cf0bc25d1730…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-duplicate-finding-s320260230271.json` | `bc0381068b70…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-duplicate-finding-s320260230283.json` | `bc0381068b70…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-exit-s320260230271.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-exit-s320260230283.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-findings-s320260230271.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-findings-s320260230283.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-no-verdict-s320260230271.json` | `447f38015ca9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-no-verdict-s320260230283.json` | `447f38015ca9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-observed-s320260230271.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-observed-s320260230283.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-scrub-s320260230271.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-scrub-s320260230283.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-stray-known-s320260230271.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-stray-known-s320260230283.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-stray-unknown-s320260230271.json` | `5b503e64c0af…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-stray-unknown-s320260230283.json` | `5b503e64c0af…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-unique-s320260230271.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/frozen-unique-s320260230283.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-exit-s320260230271.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-exit-s320260230283.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-findings-s320260230271.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-findings-s320260230283.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-observed-s320260230271.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-observed-s320260230283.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-scrub-s320260230271.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-scrub-s320260230283.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-stray-known-s320260230271.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-stray-known-s320260230283.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-unique-s320260230271.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/mutant-unique-s320260230283.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-exit-s320260230271.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-exit-s320260230283.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-findings-s320260230271.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-findings-s320260230283.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-observed-s320260230271.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-observed-s320260230283.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-scrub-s320260230271.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-scrub-s320260230283.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-stray-known-s320260230271.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-stray-known-s320260230283.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-unique-s320260230271.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/pristine-unique-s320260230283.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-exit-s320260230271.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-exit-s320260230283.json` | `3e6c2a5a52c6…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-findings-s320260230271.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-findings-s320260230283.json` | `7dee91472997…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-observed-s320260230271.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-observed-s320260230283.json` | `1521524ace0a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-scrub-s320260230271.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-scrub-s320260230283.json` | `2303d3a7931a…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-stray-known-s320260230271.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-stray-known-s320260230283.json` | `9a4f6461b12e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-unique-s320260230271.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/restored-unique-s320260230283.json` | `6596225e40c3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/clean-exit-s320260230401.json` | `d1da62bebfbe…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/clean-exit-s320260230419.json` | `d1da62bebfbe…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/duplicate-finding-s320260230401.json` | `c70319a925c8…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/duplicate-finding-s320260230419.json` | `c70319a925c8…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/exit-s320260230401.json` | `f8576812142e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/exit-s320260230419.json` | `f8576812142e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/findings-s320260230401.json` | `a3aebd9a8083…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/findings-s320260230419.json` | `a3aebd9a8083…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/no-verdict-s320260230401.json` | `5b77f3380fba…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/no-verdict-s320260230419.json` | `5b77f3380fba…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/observed-s320260230401.json` | `cc16c479e920…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/observed-s320260230419.json` | `cc16c479e920…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/scrub-s320260230401.json` | `346de1ab5331…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/scrub-s320260230419.json` | `346de1ab5331…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/stray-known-s320260230401.json` | `d5022219705f…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/stray-known-s320260230419.json` | `d5022219705f…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/stray-unknown-s320260230401.json` | `097adc9a9656…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/stray-unknown-s320260230419.json` | `097adc9a9656…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/unique-s320260230401.json` | `77033ae59a13…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/MutC2CounterB/v2/unique-s320260230419.json` | `77033ae59a13…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/A-load-s103.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/A-load-s104.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/A-s101.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/A-s102.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/B-s201.json` | `917c9f41b5f9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/B-s202.json` | `917c9f41b5f9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/C-s301.json` | `dfee84804c07…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/C-s302.json` | `dfee84804c07…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/A-s4001.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/A-s4002.json` | `777ac24e694e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/B-s4011.json` | `917c9f41b5f9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/B-s4012.json` | `917c9f41b5f9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/C-s4021.json` | `dfee84804c07…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w1/OracleC1B/v2/C-s4022.json` | `dfee84804c07…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-a-counter.json` | `f17c77bb7783…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-a-counter.run.json` | `f17c77bb7783…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-a-selftest.run.json` | `f17c77bb7783…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-b-counter.json` | `409bf38f1110…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-b-counter.run.json` | `409bf38f1110…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-b-selftest.run.json` | `409bf38f1110…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-c-counter.json` | `2ca13c48873b…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-c-counter.run.json` | `2ca13c48873b…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-c-selftest.run.json` | `2ca13c48873b…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-d-counter.json` | `a86cb5198da4…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-d-counter.run.json` | `a86cb5198da4…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-d-selftest.run.json` | `a86cb5198da4…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-e-counter.json` | `eb3038655142…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-e-counter.run.json` | `eb3038655142…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-e-selftest.run.json` | `eb3038655142…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-f-counter.json` | `3746d9e0baa7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-f-counter.run.json` | `3746d9e0baa7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC1Gate/mutated-f-selftest.run.json` | `3746d9e0baa7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/a-mutated.json` | `4e9008634227…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/b-mutated.json` | `35531fd675c9…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/c-mutated.json` | `625df9b83764…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/d-mutated.json` | `803a3e04ab7e…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/e-mutated.json` | `35102b0acac3…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/f-mutated.json` | `15fecf0d241f…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutC2Gate/g-mutated.json` | `9cdc48037eb7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/MutResolvedArm/mutated-c2-control.json` | `86b0ad3397d7…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC1b/rerunc1b-load1b.json` | `d13a76e37226…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/RerunC1b/rerunc1b-load2b.json` | `d13a76e37226…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/ReviewC2Probe32/c2-r777001.json` | `d13a76e37226…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |
| `.ufo/waves/round-32/w2/ReviewIntegration32/c2-s773311.json` | `d13a76e37226…` | non-revision (uncommitted gate bytes); not evidence for any landed claim |

## Recommended repair text (for the lane's own commit)

> Every receipt whose `gate_sha256` does not match a committed blob of `tools/research-gate.sh` (any revision) or of any committed `*.sh` under `.ufo/waves/` is a **non-revision**: it was measured on scratch or worktree bytes that were never committed. It is **not evidence for any landed claim**, must not be cited as "the final gate", and must be re-run (or dropped) after any scratch edit. Run `python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py . .ufo/waves/round-33` to re-check; it exits 1 while any landed/final-labelled receipt is unbound.

