# Isolated-layout correction artifact — CtlC2NoReaderB

Read with the once-written scoped report at `.ufo/waves/round-32/w1/CtlC2NoReaderB.md`. **Use the six `*-isolated-*.json` receipts below as the placement-corrected evidence.** The original six receipts remain disclosed flat-layout observations; none is being silently replaced. The original report was not rewritten.

## Why a correction was necessary

After the first report, peer `ChousaR32A2.CtlC2WeakReaderB` warned that a scratch gate's location changes its allowed lane root. I opened `tools/research-gate.sh:287-291,1190-1228`: `LANE_ROOT` is the script directory's parent, and source policy accepts either canonical `ROOT` or canonical `LANE_ROOT` containment. The frozen counter puts its `outside` directory beside `root` under `C2_TMP` (`corpus/evidence/round32/c2-count.py:148-154,208-210,247-249`).

[INFERENCE from those opened lines] The original flat gates made `LANE_ROOT=/fast/scratch/hyaku/chousa-r32/w1`, encompassing both fixture directories, so the counter's E7 hidden truth did not agree with an unchanged resolved comparator in that layout. The no-reader controls themselves did not call `claim_source_path` and their original counts were literal, but this layout disagreement should not be used as canonical placement evidence.

Smallest correction: copy the unchanged control bytes into disjoint mock lane layouts:

- A: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/a/tools/research-gate.sh`.
- B: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/b/tools/research-gate.sh`.
- C: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/c/tools/research-gate.sh`.

Their `LANE_ROOT` values are respectively `.../gates/a`, `.../gates/b`, `.../gates/c`, none containing the counter's temporary fixtures. `C1_TMP`, `C2_TMP`, and `TMPDIR` remain this seat's scratch directory. No code or counter change was made. B still uses canonical `ROOT` containment; the new fixture layout removes the accidental alternative containment that made the old resolved comparator disagree.

Construction commands, all exit 0:

```sh
timeout 15s mkdir -p /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/a/tools /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/b/tools /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/c/tools
timeout 15s cp /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-a-existing-file.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/a/tools/research-gate.sh
timeout 15s cp /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-b-inside-boundary.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/b/tools/research-gate.sh
timeout 15s cp /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-c-anchor-cell.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/c/tools/research-gate.sh
```

All six corrected receipts carry frozen `counter_sha256=b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c` and these unchanged gate hashes:

| Control | SHA-256 |
|---|---|
| A | `308dab5001553e04f83fe850455e50527bd5da1547697a634b4806c5a66b9b08` |
| B | `0cdc8cb738b957f12c2a5b6409930e50b2b48fd48d4ca5ce397665c07356b533` |
| C | `afa7bfdeab02ef9815adc76649325d72d63c2c5f04b2264fde2d6d915a1448e9` |

## Interrupted launch attempts (not scores)

Six new seeds came from `timeout 10s shuf -i 100000000000000-999999999999999 -n 6` (exit 0): 992342902154812, 996686887343339, 164723748095110, 115803520396841, 247695042450311, 818197653177554.

The first isolated-layout batch used the exact scoring commands below except `--nproc=2000`. All six aborted at counter line 263 while launching the gate, with `BlockingIOError: [Errno 11] Resource temporarily unavailable`, process exit 1, no count output, and no receipt. A glob for `*isolated*.json` immediately afterwards found none. These are harness-launch failures, not valid gate scores. The counter was not patched or suppressed.

A diagnostic command `timeout 15s ps -u vgpnk -L -o lwp= | timeout 15s wc -l` printed `ps: unsupported option '-L'` followed by 0; its pipeline exit 0 was not treated as a valid thread measurement. Using the actual binary, `timeout 15s /usr/bin/ps -u vgpnk -L -o lwp= | timeout 15s wc -l`, exited 0 and returned 1765. [INFERENCE] The shared-user process/thread limit was too low at launch. For the next batch I raised only the finite process cap to 8192; retained 1 GiB address-space and wall-time caps. All six then launched and completed normally.

## Corrected result and receipts

Axes remain **coverage** and **operability**. Every completed isolated-layout trial is **MISSES**, with the same per-class pattern as its original flat-layout control. None meets 120/120, so there is no observed no-reader let-through. All six corrected receipts report `gate_rc=1`, `gate_timed_out=false`, `predicate_holds=false`; every completed scoring command exited 1. Tool wall times were 3.78–4.21 seconds.

Receipt paths below are relative to `.ufo/waves/round-32/w1/CtlC2NoReaderB/`:

| Control | Seed | Counter count | Verdict | Receipt |
|---|---:|---|---|---|
| A | 992342902154812 | 78/120 | MISSES | `a-isolated-s992342902154812.json` |
| A | 996686887343339 | 78/120 | MISSES | `a-isolated-s996686887343339.json` |
| B | 164723748095110 | 84/120 | MISSES | `b-isolated-s164723748095110.json` |
| B | 115803520396841 | 84/120 | MISSES | `b-isolated-s115803520396841.json` |
| C | 247695042450311 | 60/120 | MISSES | `c-isolated-s247695042450311.json` |
| C | 818197653177554 | 60/120 | MISSES | `c-isolated-s818197653177554.json` |

Every receipt was opened. First-trial metadata/counts are at lines 3-14; per-class results at lines 15-29. Second-trial metadata was opened by a JSON query.

### Per-class/per-trial printed values

| Printed line/class | A / 992342902154812 | A / 996686887343339 | B / 164723748095110 | B / 115803520396841 | C / 247695042450311 | C / 818197653177554 |
|---|---|---|---|---|---|---|
| `EXEMPT_AUDIT_MATCH` | 78/120 | 78/120 | 84/120 | 84/120 | 60/120 | 60/120 |
| `R1_U_fragment_quote` | 12/12 | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| `R2_U_path_anchor_cols` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `R3_U_declared_id` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `F1_resolved_verifiable` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `E1_U_anchor_absent` | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| `E2_U_missing_file` | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E3_U_external_url` | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| `E4_U_no_citation` | 0/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |
| `E5_J_resolvable` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `E6_U_undeclared_id` | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E7_U_out_of_corpus` | 0/6 | 0/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E8_U_quote_glued` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| `E9_U_heading_as_plain_line` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| `E10_U_line_partial` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |

### Executed successful-launch commands

All ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` and exited 1. The initial aborted commands were identical except for `--nproc=2000`, as disclosed above.

```sh
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/a/tools/research-gate.sh --seed 992342902154812 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/a-isolated-s992342902154812.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/a/tools/research-gate.sh --seed 996686887343339 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/a-isolated-s996686887343339.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/b/tools/research-gate.sh --seed 164723748095110 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/b-isolated-s164723748095110.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/b/tools/research-gate.sh --seed 115803520396841 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/b-isolated-s115803520396841.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/c/tools/research-gate.sh --seed 247695042450311 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/c-isolated-s247695042450311.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/c/tools/research-gate.sh --seed 818197653177554 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/c-isolated-s818197653177554.json
```

## Corrected counterexamples and safe correction

- A: existing-file hop `h836671cb` is truth `exempt`, observed `resolvable` (`a-isolated-s992342902154812.json:32-37`).
- B: canonical-boundary-checked hop `hadeb9b76` still has absent-anchor truth `exempt`, observed `resolvable` (`b-isolated-s164723748095110.json:32-37`). All 30 E1/E8/E9/E10 hops fail even after boundary isolation.
- C: fragment-citation hop `hb462cf4e` is truth `resolvable`, observed `exempt` (`c-isolated-s247695042450311.json:32-37`), while missing-file and invalid-anchor classes produce false positives.

The original safe-correction recommendation is unchanged [INFERENCE, not implemented]: reuse the exact resolved citation/source/anchor verification for U hops, finding only successful verifications, retaining other U hops and both judgment statuses as exempt. These are correctness defects, not a coverage/operability tradeoff. This artifact additionally establishes the necessary experimental correction: isolate gate-derived lane roots from generated fixture siblings.

No candidate, counter edit, install, source fetch, production edit, or background job was introduced by this correction. No broader no-reader saturation or candidate acceptance claim is made. The corrected scoring commands all completed before this artifact was written.
