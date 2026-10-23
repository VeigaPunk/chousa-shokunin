# CtlC1LineGame — C1 line-binding controls

Date/access date: 2026-10-23. Axis: **operability**. Constraints: frozen-counter integrity, isolated control bytes, exact restoration. This is a time-boxed partial control probe, not a candidate assessment or a completed two-seed census of every control.

## Result

Let `A = .ufo/waves/round-34/w1/CtlC1LineGame/` (lane-relative) and `S = /fast/scratch/hyaku/chousa-r34/w1/CtlC1LineGame/`.

| Control | Defect after exact literal existence search | Seed 34273111 | Seed 34273112 | Observed target verdict |
|---|---|---|---|---|
| A / `a.sh` | Bind when span newline count equals M−N; ignore position | 28/30 | 28/30 | **MISSES** |
| B / `b.sh` | Bind only when N equals the first delimited occurrence's start; ignore M | 28/30 | interrupted, no count | **MISSES** on completed seed; second-seed requirement incomplete |
| C / `c.sh` | Bind when N is within ±1 of any delimited occurrence's start; ignore M | 28/30 | interrupted, no count | **MISSES** on completed seed; second-seed requirement incomplete |
| D / `d.sh` | Trust a present, already well-formed line field | interrupted, no count | interrupted, no count | **INCONCLUSIVE**; neither MEETS-TARGET nor MISSES is established |

No completed control run printed 30/30. D cannot be counted as rejected from an interrupted run. Both pristine runs printed 19/30, so the generic mutation-kill verdict is **inconclusive**, not “killed”; the baseline itself fails the target. The completed A/B/C runs nevertheless directly demonstrate their respective below-target scores.

Evidence: `A/a-s34273111.json:3-29`, `A/a-s34273112.json:3-29`, `A/b-s34273111.json:3-29`, `A/c-s34273111.json:3-29`; interrupted process outcomes are recorded in `A/run-evidence.json`. Completed receipts all record gate rc 1, no gate timeout, empty gate stderr, and `predicate_holds=false`.

## Actual per-class output

The following is the complete per-class output of every completed run, in the frozen counter's print order. A has this same output on both seeds; B and C have one completed seed each. Pristine has this same output on both seeds. A dash is not a zero: D produced no count or per-class lines before interruption.

```text
class                  pristine  A       B       C       D
long-verbatim-ml        0/3       3/3     3/3     3/3     —
long-verbatim-1l        0/2       2/2     2/2     2/2     —
long-edge              0/2       2/2     2/2     2/2     —
long-mut-head          2/2       2/2     2/2     2/2     —
long-mut-tail          2/2       2/2     2/2     2/2     —
long-mut-mid           3/3       3/3     3/3     3/3     —
long-split             2/2       2/2     2/2     2/2     —
long-glued-left        2/2       2/2     2/2     2/2     —
long-glued-right       2/2       2/2     2/2     2/2     —
long-line-bound        0/2       2/2     0/2     2/2     —
long-line-wrong        0/2       0/2     2/2     0/2     —
short-verbatim         3/3       3/3     3/3     3/3     —
short-mut              3/3       3/3     3/3     3/3     —
LONGSPAN_MATCH          19/30     28/30   28/30   28/30   —
```

The full B/C stdout is preserved in `A/b-s34273111.log` and `A/c-s34273111.log` (285 bytes each). Every interrupted log is empty, not a successful run. The receipts above also retain every missed id and its observed/truth pair.

## Why the completed shortcuts miss

Frozen generator locations: `corpus/evidence/round34/c1-count.py:188-199`, opened 2026-10-23. Its bound records name the second of two occurrences. Its wrong range shifts the first occurrence's start and end by one line; the exact source line is `wrong = (a1[0] + 1, a1[1] + 1)` (:197).

- A accepts both wrong ranges because shifting both endpoints leaves the height unchanged. Seed 34273111: `c8b40aa7436`, `ce86876fd0f` become supported instead of mislocated (`A/a-s34273111.json:31-43`). Seed 34273112: `c338186aece`, `c6c12e8424e` do likewise (`A/a-s34273112.json:31-43`).
- B rejects the two correctly bound second occurrences: `c102fe88dc5`, `cd6e10e2285` become mislocated instead of supported (`A/b-s34273111.json:31-43`).
- C accepts the two +1 wrong starts: `c8b40aa7436`, `ce86876fd0f` become supported instead of mislocated (`A/c-s34273111.json:31-43`).
- [INFERENCE] D should also accept both wrong ranges, predicting 28/30. No completed D output verifies that prediction, so it is not a scored finding.

Thus the observed A/B/C results do not expose a 30/30 line-binding escape. No conclusion about D's actual counter score is justified. This probe does not establish coverage of other line-field error shapes.

## Control construction and immutable artifacts

Read `corpus/evidence/round34/claims.md` first, then the counter docstring and generator. The production base and frozen counter hashes were checked before execution. Only scratch gate copies were edited. No ExecC1Build patch or candidate implementation was opened or scored.

Shared control apparatus replaces `tok_span_at`'s hex-PCRE argv construction with quoted Bash literal matching, advancing one byte past a rejected occurrence and retaining the base `tok_left_ok`/`tok_right_ok` boundary predicates. C also replaces `tok_span_all` with the same literal enumeration; A/B/D do not call the old all-occurrence helper. Deliberate shortcut changes are confined to the existing line-binding block. The archived controls are complete gates, not helper stubs:

| Artifact | Changed binding location | SHA-256 | Bytes |
|---|---|---|---|
| `A/a.sh` | :1809-1815 | `83dafafb5eece09b3bbecd3335db3f1f9ea4880ff1e3a81510bc1ed0f08d7a9b` | 356839 |
| `A/b.sh` | :1809-1815 | `9ccd8bcfd3179c890175c1f390c053a9cd1e63608d34f303d0a886485f0e291d` | 356817 |
| `A/c.sh` | :1808-1821 | `be6bb1beba80c0983a6e0b44b441dfa86efe8ae476fb5044c61022a95a1f1b99` | 357043 |
| `A/d.sh` | :1809-1812 | `c285f0cefd2761bc9968b937aa9187503950994774f908e6a318b095f3d56f94` | 356742 |

Construction commands, all rc 0: bounded `mkdir -p S A`; `timeout 30s cp tools/research-gate.sh S/base.sh`; bounded copies to S/a.sh through S/d.sh; surgical scratch-only edits; `timeout 30s cp S/{a,b,c,d}.sh A/`; `timeout 30s sha256sum S/{base,a,b,c,d}.sh`; `timeout 30s wc -c A/{a,b,c,d}.sh`. The shared existence helper is at archived controls :1553-1578; C's all-occurrence helper is :1580-1604. Existing field validation remains in the base `tools/research-gate.sh:1701-1710,1753-1770`.

## Commands, bounded execution, and receipts

All commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Exact common command, with the explicit paths above substituted for S and A:

```sh
C1_TMP=S TMPDIR=S timeout 1700s prlimit --as=2147483648 --nproc=65536 \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py \
  --gate S/CONTROL.sh --seed SEED --receipt A/NAME.json
```

CONTROL/SEED/NAME and actual process outcomes are in `A/run-evidence.json`. Pristine used CONTROL=base and NAME=pristine-sSEED; mutants used CONTROL=a/b/c/d and NAME=CONTROL-sSEED. Both seeds, 34273111 and 34273112, were new for this probe, neither in 3401–3409; the same generated inputs were intentionally reused across pristine and mutant phases for comparability. No more than four counters ran concurrently. All heavy child commands had finite memory/process limits and a 1700-second outer timeout, retaining the frozen counter's own 1500-second gate timeout.

Completed receipts (counter rc 1 for each):

- `A/pristine-s34273111.json`: 19/30, 1028.160 s, gate rc 1.
- `A/pristine-s34273112.json`: 19/30, 1087.106 s, gate rc 1.
- `A/a-s34273111.json`: 28/30, 841.580 s, gate rc 1.
- `A/a-s34273112.json`: 28/30, 759.725 s, gate rc 1.
- `A/b-s34273111.json`: 28/30, 1012.918 s in receipt, gate rc 1.
- `A/c-s34273111.json`: 28/30, 995.445 s in receipt, gate rc 1.

The pristine stderr tails report `/usr/bin/grep: Argument list too long` (`A/pristine-s34273111.json:11`, `A/pristine-s34273112.json:11`). Initial pristine attempts with `--nproc=2000` failed before starting the gate, with `BlockingIOError: [Errno 11] Resource temporarily unavailable`; commands and actual exception are preserved in `A/initial-harness-errors.txt`. They produced no receipt and are not kills. Raising the finite process ceiling allowed later pristine runs. A later async tool launch hit the host's 100-background-job cap and started nothing; subsequent runs used directly supervised bounded subprocesses, with recorded PID/PGID.

The four remaining mutant runs were stopped at the seat time-box cutoff: D seed 34273111 after 939.490 s; B seed 34273112 after 840.059 s; C seed 34273112 after 109.903 s; D seed 34273112 after 86.908 s. Each process return code was −15 (SIGTERM), with no receipt/count. These are inconclusive execution cutoffs, not gate timeouts, scores of zero, or failed mutants. Completed runs took roughly 13–18 minutes rather than the task's estimated 3–6; the time box therefore prevented completion of the entire requested two-seed matrix.

## Restoration and cleanup evidence

Every scratch control was restored using a bounded `cp S/base.sh S/CONTROL.sh`. A was restored after its two completed runs; B/C/D were restored only after all their running probes had been stopped and waited. The resulting command `timeout 30s sha256sum S/{base,a,b,c,d}.sh tools/research-gate.sh corpus/evidence/round34/c1-count.py` exited 0 and produced the exact values in `A/restoration.sha256`:

- base plus **all four restored scratch controls**, and the untouched production gate: `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
- untouched frozen counter: `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`.

The same frozen detector was invoked on each restored scratch control with seed 34273111, using NAME=restored-CONTROL-s34273111. All four were stopped after a 15-second cleanup bound, returned −15, printed nothing, and produced no receipt. This is an attempted restored-byte behavioral phase, **not** a completed restored score. Exact-byte restoration is proven by the hashes independently of that inconclusive phase. The archived A/a.sh through A/d.sh deliberately retain the tested mutant bytes; the receipt's original scratch pathname now identifies restored bytes, so replay must use the archived hash-matching control copy in isolated scratch.

Recorded restored-run PID/PGIDs: 638263, 638270, 638347, 638354. Other interrupted PID/PGIDs: 3418220, 3558706, 3331575, 3561471. Cleanup signalled only these recorded own process groups and waited for each owned process; all originally tool-managed baseline/A jobs had already completed. No sibling processes were signalled. No network, installs, git/jj write commands, lane production edits, or counter edits were performed. `timeout 30s df -h /fast` exited 0 before fixture generation and showed 88 GiB available. Every archived gate is below 1 MiB; all archived execution logs together contain 570 bytes.

## Explicit limits / unmet acceptance

A has two completed fresh-seed scores. B and C have one completed score each, sufficient to establish their observed MISSES but not to satisfy the requested two completed seeds per control. D has no completed score and remains INCONCLUSIVE. Restored behavioral runs were attempted but not completed. All source bytes are restored, immutable control artifacts and six complete receipts are retained, and no surviving/killed-mutant claim is made from the failing pristine baseline.
