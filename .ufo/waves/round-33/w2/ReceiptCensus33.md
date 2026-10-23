# ReceiptCensus33 — round 33 wave 2 (FALSIFY), kill-rule receipt census

Seat: `ChousaR33.ReceiptCensus33` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Landed revision under claim: `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`, gate `tools/research-gate.sh`
SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`; counter v2
`corpus/evidence/round33/c1-count-v2.py` SHA-256
`cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`. No lane production file was
edited; everything below is read-only measurement plus my own receipts under
`.ufo/waves/round-33/w2/ReceiptCensus33/`.

**Snapshot warning.** The lane was live while I measured. HEAD moved from `0fb300b` to
`4c076a0f2974a5fc9af79e0b49efbe1d7bded7d2` at 09:09:25Z (`git log -2`), whose gate blob is still
`94a7be5a` (`git show 4c076a0:tools/research-gate.sh | sha256sum`), and the **working-tree gate was
being edited in place** after that: hashes observed in receipts within ~1 minute were
`fc08410e…` (09:10:09Z), `45d76b4f…` (09:10:27–31Z), `b808e9b5…` (09:10:50Z); the worktree read
`154f7d3d…` at 09:11Z (`sha256sum tools/research-gate.sh`). Counts below are timestamped snapshots,
not a closed set.

## What I attacked

The C1 v2 kill rule (claims.md "Design v2", *Kill rule v2*): every `c1-count-v2.py` run on a
candidate or landed gate is saved as a receipt and committed; **any such run on the landed revision
below 156 is a P1 miss**. I censused every committed receipt whose `label` starts
`TOPLEVEL_FIELD_MATCH`, grouped by `counter_sha256` × `gate_sha256`, listed every receipt on the
candidate gate `52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a` and the landed gate
`94a7be5a…`, then re-ran the counter myself on fresh seeds and checked receipt integrity
(per-class arithmetic, exit code, hash provenance, uct ordering, history).

## Counting command (paste)

Committed-set census (walk every committed JSON object under the two trees; a receipt is any object
with `label` starting `TOPLEVEL_FIELD_MATCH`):

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
git ls-files -z '.ufo/waves/round-33/**' 'corpus/**' | python3 -c '
import sys, json, os
LANE=os.getcwd(); V2="cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
CAND="52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a"
LAND="94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e"
def walk(o,p,acc):
    if isinstance(o,dict):
        acc.append((p,o))
        for k,v in o.items(): walk(v,p+"/"+str(k),acc)
    elif isinstance(o,list):
        [walk(v,p+"/"+str(i),acc) for i,v in enumerate(o)]
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

Executed equivalent (same filter, plus schema split): `python3 .ufo/waves/round-33/w2/ReceiptCensus33/census.py`
(rc=0) and `precise-census.py` (committed only, rc=0). Whole-tree snapshot (untracked included):
`tree-census.py` (rc=0). Every `c1-count-v2` receipt whose `gate` field is the lane-relative
`tools/research-gate.sh`, grouped by measured `gate_sha256`: `lane-gate-runs.py` (rc=0). Outputs and
scripts are in `.ufo/waves/round-33/w2/ReceiptCensus33/` with SHA-256 in `SHA256SUMS`.

## Results — committed receipts

Committed inventory (0fb300b snapshot, `census-out.txt`): **273** objects carry a
`TOPLEVEL_FIELD_MATCH…` label, of which **255 are receipts** (`schema` `chousa-r33-c1-receipt/v1`
= 180, `/v2` = 75) and **18 are manifest run copies** in
`.ufo/waves/round-33/w1/CtlC1LastWins/manifest.json` `runs[]` (no per-run `counter_sha256`; the
manifest top level carries `ab6b2ae2…`, so a naïve label grep over-counts by 18). No unparsable
committed JSON was found; no `label` disagrees with its own `matched/total` (0 disagreements).

Every committed receipt on the candidate/landed gates (`precise-census-out.txt`, rc=0):

| gate | file | seed | label | holds | added by |
|---|---|---|---|---|---|
| candidate `52f07c74…` | `.ufo/waves/round-33/measure/candidate/c1v2-s3351.json` | 3351 | `TOPLEVEL_FIELD_MATCH=156/156` | true | 7f6aeb7 |
| candidate `52f07c74…` | `…/measure/candidate/c1v2-s3352.json` | 3352 | `156/156` | true | 7f6aeb7 |
| landed `94a7be5a…` | `…/measure/integrated/c1v2-s3371.json` | 3371 | `156/156` | true | 0fb300b |
| landed `94a7be5a…` | `…/measure/integrated/c1v2-s3372.json` | 3372 | `156/156` | true | 0fb300b |

**No v2 receipt on the candidate or landed gate is below 156** → no P1 miss from committed receipts.
The other label-bearing groups are controls/other gates: base `f4731885` 60/156 ×7 (v2) and 60/144
×88 (v1), oracle `930a2075` 156/156, mutant gates 0–142/156, all with their own hashes — none of
those hashes is the candidate or landed gate. The 18 v1 manifest copies are 60/144 ×14, 0/144 ×2,
69/144 ×2.

History scan (`git rev-list 2b9cc73..HEAD`, 6 commits, every commit tree): receipt objects on the
two gates in commit trees = 6 entries (4 in `0fb300b`, 2 in `7f6aeb7`), **0 below 156**, no deleted
receipt files (`git log --diff-filter=D` empty). Gate blob provenance verified: `eb179ec:tools/research-gate.sh`
= `52f07c74…`, `0fb300b:…` = `94a7be5a…`; `git diff eb179ec..0fb300b -- tools/research-gate.sh` is
comments + usage text only (7 insertions, 1 deletion).

## Results — working-tree / in-flight receipts (live snapshot)

`tree-census-out.txt` (snapshot 09:09:56Z, HEAD `4c076a0`, rc=0): after the L1 committed wave-2
evidence, **58 distinct-seed C1-v2 receipts on the landed gate are in the index and every one is
`156/156`, `predicate_holds=true`** (seeds 3371…93330112; the integration pair plus 56 wave-2
artifacts); candidate gate still 2 (3351, 3352), both 156. **0 below 156.**

`lane-gate-runs-out.txt` (rc=0) groups every `c1-count-v2` receipt whose `gate` is the lane-relative
`tools/research-gate.sh` by the gate bytes the counter measured:

| gate_sha256 (observed) | runs | below 156 | utc range |
|---|---|---|---|
| `94a7be5a…` (landed) | 28 | 0 | 08:46:52Z – 09:09:11Z |
| `52f07c74…` (candidate) | 2 | 0 | 08:41:21 – 08:41:23Z |
| `fc08410e…` (in-flight worktree) | 1 | 0 | 09:10:09Z |
| `45d76b4f…` (in-flight worktree) | 3 | 0 | 09:10:27 – 09:10:31Z |
| `b808e9b5…` (in-flight worktree) | 1 | **1 (0/156)** | 09:10:50Z |

### The one below-156 run (must be adjudicated, not a landed P1 miss)

`.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json` (untracked at my snapshot) records seed 4117,
`gate_sha256 = b808e9b5e6d3b34473d96dc07a9ce5c6c30695722ece14c83217e7f1e88e55e4`,
`gate_rc=1`, `label=TOPLEVEL_FIELD_MATCH=0/156`, `predicate_holds=false`, every miss `observed=none`.
The bytes `b808e9b5…` no longer exist in the lane worktree (it was superseded within ~20 s:
`fc08410e` 09:10:09 → `45d76b4f` 09:10:27 → `b808e9b5` 09:10:50 → worktree `154f7d3d` at 09:11Z), and
no other receipt cites it. It is **not** the landed gate (`94a7be5a…`) and **not** the named
candidate (`52f07c74…`), so it does not trigger kill rule v2's "below 156 on the landed revision"
clause and P1 v2 is not falsified by it. It *is* a lane-gate run with a DRIFT rc=1 and no parseable
CLAIM lines, i.e. an intermediate worktree edit state; L1 must (a) keep/commit this receipt as the
kill rule requires for runs on candidate gates, (b) confirm `b808e9b5…` was never a published
candidate, and (c) re-run the counter after the worktree edit settles — a run taken while the gate
file is being rewritten is a race, not a measurement of any revision.

Also untracked at snapshot, both 156/156: `…/w2/NoHarmCorpus33/c1-landed-seed34101.json`
(gate `fc08410e…`) and `c1-landed-seed34102.json` (gate `45d76b4f…`); `…/w2/ProbeTypes33/c1-landed-s4202.json`
and `…/w2/ProbeLongLines33/c1-v2-seed5187.json` also cite `45d76b4f…`. The L1's integration must
commit these to satisfy kill rule v2's "saved as a receipt and committed" clause.

## My own kill-rule runs (fresh seeds, receipts + redirected stdout)

Both runs from the lane root with `C1_TMP`/`TMPDIR` in my scratch dir, gate then `94a7be5a…`:

```sh
C1_TMP=/fast/scratch/hyaku/chousa-r33/w2/ReceiptCensus33/tmp TMPDIR=$C1_TMP timeout 900 \
  python3 corpus/evidence/round33/c1-count-v2.py --seed 8101 \
    --receipt .ufo/waves/round-33/w2/ReceiptCensus33/c1v2-landed-s8101.json \
    > .ufo/waves/round-33/w2/ReceiptCensus33/c1v2-landed-s8101.out 2>&1   # same with --seed 8102
```

`seed=8101 rc=0`, `seed=8102 rc=0`; both stdout `TOPLEVEL_FIELD_MATCH=156/156` (15 class lines
follow, e.g. `D1_duplicate_top_level 24/24`); receipts: `gate_sha256=94a7be5a…`, `gate_rc=1`,
`total=156`, `matched=156`, `predicate_holds=true`, utc 09:05:55Z / 09:06:01Z
(SHA-256 in `SHA256SUMS`; stdout bytes identical, hash `1eeb8be8…`). Temp dir empty afterwards.

## Receipt-integrity checks (all pass)

- `label == TOPLEVEL_FIELD_MATCH=matched/total` for all 273 committed label objects; 0 disagreements.
- For all 255 receipts, per-class numerators sum to `matched` and denominators to `total`; 0
  inconsistent. `gate_rc` ∈ {0,1}; the only 4 `gate_rc=0` receipts are the `all-supported` control
  (v2 correctly scores 0/156 because `rc==1 and DRIFT` is required, `c1-count-v2.py` line "if not
  timed_out and rc == 1 and drift"), and those sit on the control gate, not candidate/landed.
- Ordering: all 71 committed v2 control/oracle/base receipts have utc 08:34:15–08:40:37Z, strictly
  before the first candidate receipt 08:41:21Z, matching commit order `96be792` (controls) <
  `eb179ec` (candidate). "Controls re-scored under v2 before the first candidate receipt" is
  corroborated (self-reported timestamps, but consistent with the commit chain).
- The 4 integration `.out` files on candidate/landed gates all print `156/156`, matching their
  receipts. No committed v2 receipt carries a counter hash other than `cb354dd1…`.

## Adjacent observations (not kill-rule misses)

- The L1's own post-data commit `4c076a0` reports a **fixture-keyed shortcut scoring 156/156**
  (receipt `.ufo/waves/round-33/w2/L1ShortcutMask/mask-s3391.json`, gate `ae7d4bfc…`; committed as
  "C1 §9 counterexample"). Its gate hash is not the landed gate, so it is not a P1 miss; it does
  mean `TOPLEVEL_FIELD_MATCH=156/156` alone cannot distinguish the landed reader from that
  shortcut. The L1 recorded it; I only report what the census sees.
- `.ufo/waves/round-33/w1/CtlC1LastWins/manifest.json` `runs[]` copies carry `label/matched/gate_sha256`
  but no per-run `counter_sha256`; they are attributable only via the manifest top level (`ab6b2ae2…`).
  Not receipts; excluded from the 255 count.

## Verdict

**HOLDS — no P1 v2 kill-rule miss on the landed revision.** Every `c1-count-v2` receipt on the
landed gate `94a7be5a…` (2 committed at `0fb300b`; 58 in the index at `4c076a0`; 28 lane-gate runs
in the whole snapshot) prints `156/156`, and the candidate gate `52f07c74…` is 156/156 on both
receipts. Two independent fresh-seed runs (8101, 8102) reproduce 156/156, rc=0. The single
below-156 run in the tree (`0/156`, seed 4117) is on a transient, superseded, uncommitted worktree
edit state `b808e9b5…`, not on the landed revision or the named candidate; it is a live-edit race
that L1 must adjudicate and commit, and it must not be treated as a scored candidate.

## Limits

- Snapshot of a live tree; the gate changed under me (`94a7be5a → fc08410e → 45d76b4f → b808e9b5 →
  154f7d3d` inside ~1 minute) and HEAD moved `0fb300b → 4c076a0`. Only hash-pinned statements above
  are stable.
- Receipts are self-reported. A run whose `--receipt` path was overwritten, or that died after
  printing but before writing (`c1-count-v2.py` prints the label before opening the receipt file),
  leaves no trace; the 4 integration `.out`/receipt pairs match, but absence of other lost receipts
  cannot be proven from the repository.
- Contract bounds: no scan of `/fast/scratch` (only my own dir), no other repos, no network.

## Files

Lane production: **none changed**. Report: this file. Artifacts (all < 1 MiB, SHA-256 in
`.ufo/waves/round-33/w2/ReceiptCensus33/SHA256SUMS`): `census.py`, `census-out.txt` (40 072 B),
`precise-census.py`, `precise-census-out.txt`, `tree-census.py`, `tree-census-out.txt`,
`lane-gate-runs.py`, `lane-gate-runs-out.txt`, `scan_untracked.py`, `untracked-scan.txt`,
`c1v2-landed-s8101.json/.out`, `c1v2-landed-s8102.json/.out`.
