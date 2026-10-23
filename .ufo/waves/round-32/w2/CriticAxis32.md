# CriticAxis32 — round 32 attempt 2, W2 axis/§9 review

## Scoped verdicts

- **C1: HOLDS within this review.** Operability is the correct axis for repairing concurrent execution of the existing manifest append. Reproduced base **0/24**, landed **24/24**. No assigned §9 counterexample to C1 was reproduced.
- **C2: BROKEN as a §9 measurement/anti-shortcut claim, not as axis naming or landed-counter arithmetic.** Coverage correctly names a previously unread exempt-hop edge class. However, a new **no-source-reader control reaches 132/132 on two fresh seeds**. The landed gate also scored 132/132 in this seat; this finding is not a below-target candidate run or evidence that its actual audit implementation is wrong.

These are scoped falsification verdicts, not canonical admission judgments. Impacted axes: **coverage** (C2's counter cannot establish the claimed reading) and **calibration** (equating that counter with source-verification evidence would overclaim). No implementation regression or C1 harm is established here.

## Reproduced counterexample: source metadata substitutes for citation reading

Evidence directory **A** = `.ufo/waves/round-32/w2/CriticAxis32/`; scratch **S** = `/fast/scratch/hyaku/chousa-r32/w2/CriticAxis32/`.

The negative control at `S/metadata-control/tools/research-gate.sh`, retained verbatim as `A/metadata-control.sh`, reads the record but **never reads citation-source bytes or checks any anchor**. It sorts local source files by `(mtime_ns, inode)`, treats the first 36 as positive, flags their U hops, and emits the required CHAIN/finding/DRIFT syntax. It uses no seed, truth sidecar, receipt lookup, frozen-counter import, or network. Source: `A/metadata-control.sh:14-37,40-59`.

The leak is in the frozen fixture: `corpus/evidence/round32/c2-count-v2.py:79-95,188-215` writes R1, R2, R3's 12 files each before every negative class. `:259-265` shuffles table rows only, not source creation order. Random names and fresh seeds therefore do not remove the metadata correlation on this filesystem.

**Control SHA-256:** `79c4f44e1b16331dbbcae5b8839d526d158512de264a145d9414352cfe9ffcdc`.

| Frozen counter invocation | Exit | Actual key output | Receipt under A |
|---|---:|---|---|
| C2 metadata CONTROL, seed 32320021 | 0 | `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok` | `control-metadata-s32320021.json:3-15,17-34` |
| C2 metadata CONTROL, seed 32320022 | 0 | `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok` | `control-metadata-s32320022.json:3-15,17-34` |
| C2 pinned BASE control, seed 32320011 | 1 | `EXEMPT_AUDIT_MATCH=0/132`; `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0` | `control-base-c2-s32320011.json:3-18` |
| C2 LANDED gate, seed 32320011 | 0 | `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok` | `candidate-c2-s32320011.json:3-15` |
| C1 pinned BASE control, seed 32320001 | 1 | `APPEND_SERIALIZED=0/24`; every class zero | `control-base-c1-s32320001.json:3-20` |
| C1 LANDED gate, seed 32320001 | 0 | `APPEND_SERIALIZED=24/24`; every class full | `candidate-c1-s32320001.json:3-20` |

**Every counter run by this seat is in that table**, including the below-target controls. All six used committed counters unmodified, explicit `--receipt A/...`, scratch gates at `<lane>/tools/research-gate.sh`, and C1_TMP/C2_TMP/TMPDIR at `S/tmp`, outside every gate lane root. Exact expanded commands, exits, hashes and key output: `A/commands.json`. Example actually executed, cwd lane root:

```sh
timeout --kill-after=5s 120s prlimit --nproc=8000 --as=2147483648 --fsize=1048575 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticAxis32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticAxis32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticAxis32/tmp PYTHONDONTWRITEBYTECODE=1 python3 corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticAxis32/metadata-control/tools/research-gate.sh --seed 32320021 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s32320021.json
```

Additional direct probes, **not additional counter runs**:

- `strace -f -qq -e trace=openat,openat2` on the metadata control and the kept generated fixture found **zero citation-source opens**, while the control emitted 132 CHAIN lines, 36 resolvable lines and 36 findings. The only fixture file opened was the record. Inner command/exit 1 and counts: `A/evidence-summary.json:3-26`; raw trace: `A/metadata-open.trace`; raw stdout: `A/metadata-traced.stdout.txt`. Bounded capture command exited 0 (`A/commands.json`, additional_evidence_command).
- Negative-anchor witness: `S/witness/root/source.md` contains only `This file contains no matching citation.`; its unresolved row requests quote `completely absent phrase`. Metadata control falsely emits `observed=resolvable`, DRIFT, exit 1; landed gate correctly emits `observed=exempt`, CLEAN, exit 0. Commands and outputs: `A/evidence-summary.json:28-55`; raw stdout: `A/{metadata-control,landed-candidate}-witness.stdout.txt`. This establishes that the passing control is genuinely wrong, not a different legitimate citation reader.

## Axis names and §9 shape

**C1 axis naming holds.** `AXES.md:13` defines operability by runnable artifacts and stated outcomes. The changed surface is the existing `verify-all --json` critical section, not a new domain area. Landed `tools/research-gate.sh:3291-3310` opens an append descriptor, locks it before the last-byte probe and writes through it. The base/landed measurements above independently exercise that concrete execution behavior.

**C2 axis naming also holds.** `AXES.md:12` includes edge classes in coverage; the round prompt `.ufo/prompts/chousa-round-32.md:361-365` explicitly permits a previously ungoverned edge class. Pinned base gate `S/base/tools/research-gate.sh:1880-1883` simply exempts U/J without reading; landed `tools/research-gate.sh:1944-1963` probes U while leaving J unread. The prior frontier is explicit at `corpus/README.md:355-362`. Reusing resolved semantics for formerly unread statuses is a new governed edge class, not merely re-scoring resolved hops on fresh inputs.

**The §9 failure is discrimination, not nomenclature.** The prompt `:352-356` requires a target that a control skipping the claimed work cannot meet; `:362-363` bars coverage credit from sourceless counting. This metadata-only control meets the unchanged full P2 v2 target twice without that work. `claims.md:184-189` likewise says a control meeting P2 v2 stops data, never licenses re-scaling. The successful landed arithmetic does not distinguish its real audit from this shortcut.

## Are the before values honest?

- **C1 0/24: yes, for the frozen stress experiment.** Both gates faced the same 300 ms write-entry delay. Base receipt `A/control-base-c1-s32320001.json:23-60` records real held-lock/framing failures, not a record-wide score reset: L trials wrote under the cooperating lock, F trials had blank/invalid JSON lines. The counter explicitly defines this injected scheduling window (`c1-count-v2.py:4-14,234-284`). This is not an estimate of ordinary untraced failure frequency.
- **C2 0/132: numerically honest but composite, not 132 previously wrong hop decisions.** Record failure vetoes every hop (`c2-count-v2.py:312-347`). My base returned exit 0/no DRIFT; its raw per-hop decisions already match **96/132**, with only R1–R3's **36** genuinely wrong. Computed directly from receipt annotations: `A/evidence-summary.json:58-80`; concrete already-correct F1 rows: `A/control-base-c2-s32320011.json:254-282` (`verified+record-fail`). Frozen design already discloses this mechanism (`claims.md:177-182`), so I do not call the stated frozen-counter baseline fabricated. It must not be presented as a literal 132-hop coverage gain. Keep the frozen 0/132, with the 96/132 raw/0-of-36 new-edge explanation alongside it; do not replace the predicate post-data.

## Existing W1 controls and smallest safe correction

I opened all fourteen `w1/*/v2-rescore.md` supplements. They report no wrong-control target hit: C1 do-nothing/partial/all-false/wrong-lock/output mutants miss; C2 do-nothing/all-true/no-reader/status-blind/weak-reader/noisy/junk/output mutants miss. The strongest declared weak reader is 126/132 (`w1/CtlC2WeakReaderB/v2-rescore.md:9-15`); the prior generator shortcut is 120/132 (`w1/CtlC2JunkB/v2-rescore.md:24,40`; opened receipt `.../v2/generator-union-a.json:13-19`). Feasibility serializers are not no-work controls: `w1/OracleC1B/v2-rescore.md:18-20,38-60` records their actual probe+append locking and a separate-open-description measurement limit. These reports do not rule out the newly reproduced metadata shortcut.

**Smallest safe correction:** preserve the frozen v2 evidence and report the C2 §9 counterexample; do not rename the axis, narrow the target, or substitute a repaired counter as round-32 v2. The implementation need not be discarded merely because this measurement is unsound. **[INFERENCE]** A future pre-data fixture should create source files in label-independent shuffled order (rather than only shuffling table rows), with metadata decoupled from truth, and score this exact no-reader control before freezing. The present review does not exercise such a repair.

## Provenance and limits

Pinned gates were extracted with bounded read-only `git archive` from base `7a7259f0ad41a68068131bfa422a829db9fd1b55` and landed `5d8a170795dcf48c3746a4f03dee9cfe32812834`; observed hashes respectively `0bc318b3…1258` and `10f2fe12…4098`. Both frozen counter hashes match the assignment/design (`A/commands.json`, every receipt). No candidate count below target was observed by this seat; only one new candidate seed per claim was run, and I did not census every round-32 receipt, re-run no-harm/selftest, audit source rows, or establish province-wide saturation.

No installs, network, production/index/jj mutations, subagents, or background jobs. `timeout 20s df -h /fast` exited 0 before extraction (219G available). Every artifact write was bounded below 1 MiB; observed retained artifact maximum before this report was 17,366 bytes (`timeout 20s stat -c '%s %n' A/*`, exit 0). All started calls completed. Final targeted `timeout 20s pgrep -af '/fast/scratch/hyaku/chousa-r32/w2/[C]riticAxis32/(metadata-control/tools/research-gate.sh|candidate/tools/research-gate.sh|base/tools/research-gate.sh|capture-evidence.py)'` exited 1, empty output: no matching owned experiment process remained.
