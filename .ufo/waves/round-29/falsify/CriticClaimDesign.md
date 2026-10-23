# CriticClaimDesign — C1 design and measurement provenance

**Verdict: FALSIFIED / CLAIM-FALSIFIED (design discrimination).** A new offline, URL-keyed snapshot control scored **130/130 twice** with the unchanged v3 counter, while its candidate process recorded **0 socket events**. It read neither fixture labels nor measurement receipts and did not key verdicts on item ids. The landed tool's own recorded 130/130 results remain genuine observations; this finding does not demonstrate that its implementation fails the literal equality predicate. It demonstrates that the predicate accepts a command lacking the claimed live-reopening behavior. No canonical judge was invoked or admission decision made.

**Axes:** operability is the declared runnable-command surface. Freshness and calibration are impacted when label equality is offered as evidence of live reopening. They are not newly assigned numeric scores. Other lane axes and general no-harm were outside this review.

## (a) Freeze chronology: clean for the two tool executors, not literally every wave-1 seat

All times below are **2026-10-23 UTC**. The git log prints the preceding calendar date with `-03:00`; these are the same instants, not a chronology discrepancy.

| Event | Commit / source | UTC |
|---|---|---|
| v1 freeze | `f9fd6d6c0982325c40c1b4a86b698859fdb1def8` | 01:13:12 |
| v2 redesign and freeze | `12244431d636bfa615d7e8d3a0a48b85b3cba06f` | 01:19:53 |
| Build-wave registry created / updated | `build/swarm-registry.json` | 01:20:28.680 / 01:23:34.408 |
| v2 receipts committed | `8026fe6010804720ad10dbd4e4c8b1d7ae9ec490` | 01:22:45 |
| Mutation-seat pristine counter executions | `build/MutateCounter/*-pristine.receipt.json` | 01:25:59 |
| ExecToolB says zero counter invocations | original stop-order reply | 01:27:55.681 |
| ExecTool says no counter invocation of any kind | original stop-order reply | 01:28:00.033 |
| v3 redesign and freeze | `aa5e1a3187955fa923de14e11c150bf1c526efc6` | 01:28:23 |
| Mutation-seat stop reply discloses earlier runs | original reply | 01:28:35.625 |
| v3 control receipts committed | `66bf1b9300733b24b76efe393646b3037402088e` | 01:32:11 |
| ExecTool first scratch / delivered counter receipt | `receipt-v3-run1.json` | 01:34:02 |
| ExecToolB first scratch counter receipt | `receipt-v3-run1.json` | 01:44:50 |

I opened the complete claims.md git history, the requested round commit log, the build registry, ExecTool's report, both executor transcripts, the original timestamped stop replies, and scratch / delivered receipts. The receipt audit covers **9 ExecTool scratch receipts, 3 delivered copies, and 4 ExecToolB scratch receipts**. Every inspected candidate receipt uses the v3 counter hash. The two primary implementations were not measured before either redesign according to these receipts and their explicit acknowledgments.

**Qualification that must not be erased:** the broader statement “before any data seat had run the counter” is false if it includes all wave-1 seats executing the scoring machinery. `build/MutateCounter.md:5,11,43` and `1-pristine.result.json:79-80` explicitly describe an imported `counter.main()` with replayed page cases and fixed entropy. Its pristine receipts begin at 01:25:59, and its last restored receipt is 01:27:45, both before the v3 freeze. The stop reply discloses this rather than denying it. These were scratch mutation/replay experiments, **not** live, unmodified predicate measurements of the candidate; mutated 130/130 outputs are not v3 control passes. There is no demonstrated pre-v3 result-driven tuning of the primary candidate here.

The original replies and timestamps are preserved in `CriticClaimDesign/chronology-extracts.json`; complete receipt headers and commit history are in `CriticClaimDesign/receipt-audit.json`.

Historical wording caveat: v2's claims text said a full-score control would make C1 exploratory, and the warmed v2 control did score 130/130. v3 instead removes the seed option. Its numeric target remains 130, so this is another redesign rather than a numeric rescaling. I report that tension; artifact wording does not authorize changing the current frozen assignment, axes, or judgment.

## (b) Existing committed v3 controls: none reaches the target

A read-only audit of JSON committed under `controls/` at `66bf1b9` selected receipts by the **actual v3 counter SHA-256**, not merely filenames:

```text
COMMITTED_V3_CONTROLS=28
MAX_CONTROL=126/130
FULL_SCORE_CONTROL_COUNT=0
CONTROL_TIME_RANGE=2026-10-23T01:28:23Z..2026-10-23T01:31:11Z
```

All 28 carry counter hash `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`. The no-fetch contrast control's historical best is 115/130; the casefold/no-boundary control supplies the 126/130 maximum. The v2 warmed 130/130 receipts use a different counter hash and must not be passed off as v3 results. My new full-score controls below are falsify artifacts, not pre-data control receipts.

## (c) Axis by changed surface: supported, with the score boundary intact

`claims.md:38-47` names **operability** because the new surface is the runnable command `tools/quote-reopen.py verify`. That matches `SCORECARD.md:7`: operability = **3**. Lines 9-13 explicitly say it is the **one measured axis**; the other axes have no numeric scores. It is therefore the lowest scored axis, not evidence that every unmeasured axis is higher. Nothing in this review supports replacing the round-1 scale or increasing its 3/10 score.

## (d) New counterexample: offline snapshots meet frozen v3

Scratch directory: `/fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/`.

I built `offline_snapshot_control.py`, a small cache-only verifier. Preparation copied the already-existing wave-1 `CriticRuntimeVariants/cache/*.independent.txt` normalized page snapshots into a **URL-keyed** `snapshots.json`. Their original mtimes are 01:25:38.132568 to 01:25:38.133174 UTC, about **27 minutes before** the new measurements. Preparation used the source manifest solely to associate snapshot text with registry URLs; it did not obtain any labels or receipts.

The candidate reads the registry and incoming items, resolves each source id to its URL, and searches the old normalized text with the contract's normalization, length precedence and boundary check. Item ids are only echoed. It does not fetch, import the counter, inspect another process, learn expected answers, or use fixture / receipt files. It deliberately reports `offline snapshot only; no page reopened`. Source-id registry lookup is the ordinary input interface, not an answer key.

`network_guard.py` refuses and counts every Python `socket.*` audit event in the candidate process. Both receipts record `stderr_tail: "CANDIDATE_SOCKET_EVENTS=0\n"`.

Commands, from the lane root:

```sh
timeout 30s python3 /fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/prepare_snapshots.py
# Completed: SNAPSHOTS_COPIED=8; CANDIDATE_PREPARATION_GETS=0.
```

The following command was run twice concurrently, substituting `N=1` and `N=2` in the receipt path, with no seed argument:

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py \
  --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/CriticClaimDesign/offline-snapshot-runN.json \
  -- python3 /fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/network_guard.py \
  /fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/offline_snapshot_control.py
```

| Run | Fresh seed | Counter exit | Candidate exit | Match | Candidate socket events | Whole-command wall time |
|---|---:|---:|---:|---|---:|---:|
| 1 | 18048917927880715405 | 0 | 1 | **130/130** | **0** | 4.485 s |
| 2 | 6764259072167322905 | 0 | 1 | **130/130** | **0** | 4.502 s |

Both receipts are stamped **01:52:40Z**, both have `predicate_holds: true`, both report candidate wall time 0.03 s, and every class is perfect, including page windows **24/24** and page transpositions **24/24**. Candidate exit 1 is correct for a batch containing non-VERBATIM verdicts; counter exit 0 is the acceptance result.

Example newly sampled run-1 positive: S013, `a file, it must be the last byte in the`, labeled VERBATIM and answered VERBATIM from the old snapshot. Fresh random windows and fresh ids do not establish that the answering process reopened the source.

**Network accounting:** the counter itself performs its normal 16 page fetch slots per run. The earlier wave-1 author originally obtained the snapshots by fetching pages. The demonstrated omission is **all candidate-side live reopening at evaluation time**, not an assertion that these page bytes were never fetched by anyone.

Artifacts in `CriticClaimDesign/`:
- `offline-snapshot-run1.json`, `offline-snapshot-run2.json`: full frozen-counter receipts.
- `offline-snapshot-run1-command.json`, `offline-snapshot-run2-command.json`: exact commands, exit codes, stdout, stderr and total wall time.
- `snapshot-provenance-summary.json`: snapshot origin, paths, timestamps and dataset hash.

Reproduction hashes:
- `snapshots.json`: `b22b0f3482ff4f2eb0c13ac47279592413948169ed3c7d3bfc2a95ccb01dc3ab`.
- `offline_snapshot_control.py`: `8ec6ac7b6697901954b29110d7f42c43a66d40d1ada7cef861dbd9e57e0ea2cd`.
- `network_guard.py`: `10e93e64d45271d4a2d8a911a4a9a9a4a72084decb96032e50b6d4cf6b2b4f73`.

This is a measurement-discrimination defect, not evidence that the actual landed implementation secretly uses a cache. [INFERENCE] A future changed page can make this old-snapshot control fail; that does not undo the two observed full-score counterexamples.

## (e) Landed-revision after values: supported by the original command transcript

The landed commit is `30c9d24da1815e01e161ed2f52d5f951005cc2b8`, committed at **01:47:42Z**. The original L1 command record at 01:47:48.522Z first executes `git rev-parse master` and inspects relevant working-tree status, then performs both measurements. Its result at 01:48:01.813Z prints the exact landed hash, no intervening status rows, and twice prints:

```text
QUOTE_REOPEN_MATCH=130/130
counter_exit=0
```

`measure/after-run1.json` is stamped **01:47:55Z**, seed 1858171162794361068; `after-run2.json` is stamped **01:48:01Z**, seed 11266274748383853032. Both use `cmd: ["python3", "tools/quote-reopen.py", "verify"]`, the v3 counter hash above, and match 130/130. Their receipt commit `b18b3ec9d8a01f966dd81991615bac27df6d66a1` follows at 01:48:08Z. A bounded read-only hash of `30c9d24:tools/quote-reopen.py` yields `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`, matching the delivered-tool report.

The receipts alone contain no lane revision or tool hash; the original command transcript supplies the revision binding. I preserved its relevant facts in `chronology-extracts.json` rather than inventing fields in the frozen receipt.

One fixable documentation typo: `build/ExecTool.md:5` prints nonexistent revision `66bf1b9300733b24e76efe393646b3037402080e`; the actual control commit is `66bf1b9300733b24b76efe393646b3037402088e`. My first receipt-audit command failed with exit 1 because git rejected that printed hash (git child exit 128). Resolving the observed abbreviated commit and correcting only my scratch audit allowed the audit to complete. This typo does not invalidate the landed after measurements.

## Smallest safe correction, limits and scope

**Keep the frozen claim, counter, fixture and all numeric results unchanged. Surface the cache-control falsifier and do not treat 130/130 as discriminatory proof of live source reopening.** The defensible measured fact is label equality on these samples, with live fetching established separately by implementation / provenance evidence, not by this predicate alone. Do not hide the control, change its score, re-scale the target, or infer saturation. Native judgment remains with the assigned canonical judge.

For chronology, distinguish “neither tool executor had measured its candidate” from “no wave-1 seat had executed counter machinery”; preserve the disclosed mutation history. The report's revision typo can receive an explicit erratum rather than a rewritten history.

This review opened local source, history and receipts and ran only the assigned local audit / negative-control experiments. It did not run the landed tool again, open any additional external page, invoke a judge or another agent runtime, edit production / frozen files, or write git / jj state. No tools were installed or updated. No background jobs or servers were started; the two scoring commands and all bounded audit commands completed. The cached control covers the 8 fixture source URLs, not every registry page or future page revision. General parser conformance, security and no-harm are not claimed verified here.

Report: .ufo/waves/round-29/falsify/CriticClaimDesign.md
