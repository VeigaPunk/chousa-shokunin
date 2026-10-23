# ReceiptCensus33 — round 33 wave 2 (FALSIFY), kill-rule receipt census

Seat: `ChousaR33.ReceiptCensus33` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Claim pins as dispatched: landed revision `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`, gate
`tools/research-gate.sh` SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`,
counter v2 `corpus/evidence/round33/c1-count-v2.py` SHA-256
`cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`, candidate gate
`52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a`. No lane production file was
edited; all output below is read-only measurement plus my own receipts under
`.ufo/waves/round-33/w2/ReceiptCensus33/`.

**Snapshot warning (the tree moved under the census).** During this seat HEAD advanced
`0fb300b` (HEAD at dispatch) → `4c076a0` (09:09:25Z, falsify evidence) → `0cad05e` (09:14:07Z,
post-falsify repairs). The gate moved with it: `94a7be5a` at `0fb300b`; `4c076a0` still carried
`94a7be5a` (`git show 4c076a0:tools/research-gate.sh | sha256sum`); `0cad05e` carries the new landed
gate `165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563`, equal to the worktree at
09:17Z. In between, the worktree gate was edited in place and receipts observed
`fc08410e…` (09:10:09Z), `45d76b4f…` (09:10:27–31Z), `b808e9b5…` (09:10:50Z) and `154f7d3d…` (09:11Z).
All numbers below are timestamped snapshots.

## What I attacked

Kill rule v2 (claims.md "Design v2"): every `c1-count-v2.py` run on a candidate or landed gate is
saved as a receipt and committed; **any such run on the landed revision below 156 is a P1 miss**.
I censused every committed receipt whose `label` starts `TOPLEVEL_FIELD_MATCH`, grouped by
`counter_sha256` × `gate_sha256`, listed every receipt on the candidate and landed gates, re-ran the
counter on fresh seeds, and checked receipt integrity, provenance, ordering and history.

## Counting command (paste)

Committed-set census — walk every committed object under the two trees and report label-bearing
receipts on the candidate/landed gates:

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
git ls-files -z '.ufo/waves/round-33/**' 'corpus/**' | python3 -c '
import sys, json, os
LANE=os.getcwd()
CAND="52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a"
LAND="94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e"
def walk(o,p,acc):
    st=[(o,p)]
    while st:
        o,p=st.pop()
        if isinstance(o,dict):
            acc.append((p,o))
            for k,v in o.items(): st.append((v,p+"/"+str(k)))
        elif isinstance(o,list):
            for i,v in enumerate(o): st.append((v,p+"/"+str(i)))
n=0
for f in sys.stdin.buffer.read().split(b"\0"):
    if not f.endswith(b".json"): continue
    try: d=json.load(open(os.path.join(LANE,f.decode())))
    except Exception: continue
    acc=[]; walk(d,"",acc)
    for p,o in acc:
        lab=o.get("label")
        if isinstance(lab,str) and lab.startswith("TOPLEVEL_FIELD_MATCH"):
            n+=1
            if o.get("gate_sha256") in (CAND,LAND):
                print("%s%s counter=%s gate=%s seed=%s %s" % (f.decode(), "" if p=="/" else " "+p,
                      str(o.get("counter_sha256"))[:12], str(o.get("gate_sha256"))[:12], o.get("seed"), lab))
print("receipt objects:",n)'
```

As run at 09:13Z it printed `receipt objects: 362` and only 156/156 rows; a live-tree rerun prints
more (the index grew to 405 label objects by 09:15Z, see below). Because the trees now include a
committed 10-000-deep hostile fixture (`.ufo/waves/round-33/w2/SentinelC1After/deep-10000.jsonl`,
20 096 B), the command filters `.json` and the walk is iterative — a recursive walk over every
committed file crashes with `RecursionError`.

Scripts and outputs (SHA-256 in `SHA256SUMS`): `precise-census.py` (strict committed filter, rc=0),
`census.py` (full inventory/groups, rc=0), `head-tree-census.py` (strict HEAD-tree walk, rc=0),
`tree-census.py` (working-copy snapshot, rc=0), `lane-gate-runs.py` (runs keyed to the lane-relative
gate path, rc=0), `scan_untracked.py`.

## Results — committed receipts on the gate hashes

Strict HEAD-tree census (`head-tree-census-out.txt`, rc=0, HEAD `0cad05e`): every C1-v2 receipt
object in HEAD's tree, **zero below 156**:

| gate | objects | below 156 | named pair |
|---|---|---|---|
| candidate `52f07c74…` | 2 | 0 | `measure/candidate/c1v2-s3351.json`, `s3352.json` |
| landed `94a7be5a…` | 84 | 0 | `measure/integrated/c1v2-s3371.json`, `s3372.json` |
| post-falsify landed `165acd5f…` | 2 | 0 | `measure/post-falsify/c1v2-s3501.json`, `s3502.json` |

All 88 label `TOPLEVEL_FIELD_MATCH=156/156`, `predicate_holds=true`. At the dispatch-time snapshot
(0fb300b, `census-out.txt`) the committed inventory was **273** label objects = **255 receipts**
(`chousa-r33-c1-receipt/v1` 180, `/v2` 75) + **18 manifest run copies** in
`w1/CtlC1LastWins/manifest.json` `runs[]` (no per-run `counter_sha256`; the manifest top level
carries `ab6b2ae2…`, so a naïve label grep over-counts by 18). At the 09:15Z index snapshot
(`census-index-0915-out.txt`) it was **405** label objects = 387 receipts (v1 182, v2 205) + 18
copies; the candidate group was 2 and the landed group 84, all 156/156. No unparsable committed
JSON was found and **no label disagrees with its own `matched/total`** (0 disagreements).

History and provenance:
- `git rev-list 2b9cc73..0fb300b`, every commit tree: receipts on the two gates = 6 entries (4 in
  `0fb300b`, 2 in `7f6aeb7`), **0 below 156**; no deleted receipt files (`--diff-filter=D` empty).
- `eb179ec:tools/research-gate.sh` = `52f07c74…`; `0fb300b:…` = `94a7be5a…`; `git diff
  eb179ec..0fb300b -- tools/research-gate.sh` is comments + usage text only (7 insertions, 1 deletion).
  `0cad05e:tools/research-gate.sh` = `165acd5f…` = worktree.
- `precise-census-out.txt` (committed-only, rc=0): candidate 2 objects, landed 2 objects at 0fb300b,
  both groups all 156.

## Results — working-tree / in-flight receipts

`tree-census-out.txt` (snapshot 09:09:56Z, rc=0): 58 distinct-seed landed-gate receipts in the
index, all 156/156; candidate 2. `lane-gate-runs-out.txt` (rc=0) groups every C1-v2 receipt whose
`gate` is the lane-relative `tools/research-gate.sh` by the gate bytes measured at run time:

| gate_sha256 (observed) | runs | below 156 | utc range |
|---|---|---|---|
| `94a7be5a…` (landed 0fb300b) | 28 | 0 | 08:46:52 – 09:09:11Z |
| `52f07c74…` (candidate) | 2 | 0 | 08:41:21 – 08:41:23Z |
| `fc08410e…` (transient worktree) | 1 | 0 | 09:10:09Z |
| `45d76b4f…` (transient worktree) | 3 | 0 | 09:10:27 – 09:10:31Z |
| `b808e9b5…` (transient worktree) | 1 | **1 (0/156)** | 09:10:50Z |

### The one below-156 run — committed, but not on a candidate/landed gate

`.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json` (now in HEAD `0cad05e`; verified with
`git cat-file -e HEAD:<path>`): seed 4117, gate
`b808e9b5e6d3b34473d96dc07a9ce5c6c30695722ece14c83217e7f1e88e55e4`, `gate_rc=1`,
`label=TOPLEVEL_FIELD_MATCH=0/156`, `predicate_holds=false`, every miss `observed=none` (DRIFT
fired but no parseable CLAIM lines). The bytes `b808e9b5…` were superseded within ~20 s
(`fc08410e` 09:10:09 → `45d76b4f` 09:10:27 → `b808e9b5` 09:10:50 → worktree `154f7d3d` 09:11 →
final `165acd5f`), and no other receipt cites them. `b808e9b5…` is **neither the candidate
`52f07c74…` nor a landed gate** (`94a7be5a…` or `165acd5f…`), so kill rule v2's "below 156 on the
landed revision" clause is not triggered and P1 v2 is not falsified. It is, however, a committed
lane-gate run with 0/156 against an intermediate repair state: the L1 should record that
adjudication and note that it is a run against a worktree being rewritten, not a revision.

## My own kill-rule runs (fresh seeds, receipt + redirected stdout)

Both from the lane root, `C1_TMP`/`TMPDIR` in my scratch dir, gate then `94a7be5a…`:

```sh
C1_TMP=/fast/scratch/hyaku/chousa-r33/w2/ReceiptCensus33/tmp TMPDIR=$C1_TMP timeout 900 \
  python3 corpus/evidence/round33/c1-count-v2.py --seed 8101 \
    --receipt .ufo/waves/round-33/w2/ReceiptCensus33/c1v2-landed-s8101.json \
    > .ufo/waves/round-33/w2/ReceiptCensus33/c1v2-landed-s8101.out 2>&1   # same with --seed 8102
```

`seed=8101 rc=0`, `seed=8102 rc=0`; both stdout `TOPLEVEL_FIELD_MATCH=156/156` (15 class lines,
`D1_duplicate_top_level 24/24`); receipts record `gate_sha256=94a7be5a…`, `gate_rc=1`, `total=156`,
`matched=156`, `predicate_holds=true`, utc 09:05:55Z / 09:06:01Z. Stdout hashes identical
(`1eeb8be8…`); receipt hashes in `SHA256SUMS`. Temp dir empty afterwards.

## Receipt-integrity checks (all pass)

- `label == TOPLEVEL_FIELD_MATCH=matched/total` for every committed label object; 0 disagreements.
- Per-class numerators sum to `matched`, denominators to `total`, for all 255 receipts at the
  0fb300b snapshot; 0 inconsistent. Among C1 receipts `gate_rc` ∈ {0,1}: the only `gate_rc=0`
  entries are the four `all-supported` control receipts (v1 ×2, v2 ×2); v2 correctly scores them
  0/156 because scoring requires `rc==1 and DRIFT` (`c1-count-v2.py`, `if not timed_out and rc == 1
  and drift`). Two further `gate_rc=0` objects are round-32 D1 counter-v3 receipts, outside C1.
- Ordering: all 71 committed v2 control/oracle/base receipts carry utc 08:34:15–08:40:37Z, strictly
  before the first candidate receipt 08:41:21Z, matching the commit chain `96be792` (controls) <
  `eb179ec` (candidate). "Every v1 control re-scored under v2 before the first candidate receipt"
  is corroborated (self-reported timestamps, consistent with commits).
- The four integration `.out` files on the candidate/landed gates print 156/156, matching receipts.
- All-label loophole scan on the three gate hashes at HEAD (`gate-hash-all-labels.py/.out`, rc=0):
  the only `cb354dd1` (v2) objects on those hashes are the 88 `TOPLEVEL_FIELD_MATCH=156/156`
  receipts plus one `label=null, matched=null` detector-extraction metadata object
  (`w2/MutSelftest33/detector-extraction.json`). No C1-v2 run evades the label filter; the other
  counters on those hashes carry their own labels (`EXEMPT_AUDIT_MATCH=132/132`,
  `LINE_BINDING_MATCH=132/132`, `APPEND_SERIALIZED=24/24`).

## Adjacent observations (not kill-rule misses)

- HEAD `4c076a0` records a **fixture-keyed shortcut scoring 156/156** (receipt
  `w2/L1ShortcutMask/mask-s3391.json`, gate `ae7d4bfc…`, in HEAD) as a "C1 §9 counterexample,
  post-data". It is not a landed-gate run, but it means `TOPLEVEL_FIELD_MATCH=156/156` alone does
  not distinguish the landed reader from that shortcut. Recorded by L1; not adjudicated here.
- The wave committed hostile-input fixtures (`w2/SentinelC1After/*.jsonl`, incl. the 10-000-deep
  document). Peer report `w2/SentinelC1After.md` claims malformed-JSON fail-open on the old gate; I
  did not re-run it (outside this census).
- `w1/CtlC1LastWins/manifest.json` `runs[]` copies lack a per-run `counter_sha256` (top level has
  `ab6b2ae2…`); they are copies, not receipts.

## Verdict

**HOLDS — no P1 v2 kill-rule miss.** On the claim's landed revision (`0fb300b`, gate `94a7be5a…`)
every C1-v2 receipt is 156/156: 2 committed at `0fb300b`, 84 in HEAD `0cad05e`'s tree, 28 lane-gate
runs across the whole snapshot; candidate `52f07c74…` is 2/2 at 156. The new post-falsify landing
`0cad05e` (gate `165acd5f…`) also carries exactly 2 receipts (seeds 3501/3502), both 156/156. Two
independent fresh-seed runs (8101, 8102) reproduce 156/156, rc=0 on `94a7be5a…`. The one below-156
run (0/156, seed 4117) is against a superseded intermediate worktree state `b808e9b5…`, committed
but neither a candidate gate nor a landed gate; it does not trigger the kill rule, and it must not
be mistaken for a scored revision.

## Limits

- Snapshot of a live tree: HEAD moved twice and the gate bytes changed five times during the seat;
  only hash-pinned statements above are stable.
- `git ls-files` in this jj-colocated lane tracks the working-copy snapshot, not only HEAD; the
  strict committed statement is `head-tree-census.py` (HEAD tree), the index statement is
  `census-index-0915-out.txt`.
- Receipts are self-reported; a run whose `--receipt` was overwritten, or that died after printing
  but before writing (`c1-count-v2.py` prints the label before opening the receipt), leaves no
  trace. The four integration `.out`/receipt pairs match; absence of other lost receipts cannot be
  proven from the repository.
- Contract bounds: no `/fast/scratch` scan (only my own dir), no other repos, no network.

## Files

Lane production: **none changed**. Report: this file. Artifacts (all < 1 MiB, SHA-256 in
`.ufo/waves/round-33/w2/ReceiptCensus33/SHA256SUMS`): `census.py`, `census-out.txt` (40 072 B,
0fb300b snapshot), `census-index-0915-out.txt` (405 label objects), `precise-census.py/.out`,
`head-tree-census.py/.out` (HEAD `0cad05e`, 88 gate receipts, 0 below 156), `tree-census.py/.out`
(09:09:56Z), `lane-gate-runs.py/.out`, `gate-hash-all-labels.py/.out`, `scan_untracked.py`,
`untracked-scan.txt`, `c1v2-landed-s8101.json/.out`, `c1v2-landed-s8102.json/.out`.
