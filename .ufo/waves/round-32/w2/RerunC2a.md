# RerunC2a — P2 counter re-run on the landed gate (10 fresh seeds)

Scope: re-run `corpus/evidence/round32/c2-count-v2.py` on the landed `verify-chain`
exempt arm on ten fresh seeds; receipts kept; report minimum and any miss.

## Setup (verified before running)

- Lane HEAD = `5d8a170795dcf48c3746a4f03dee9cfe32812834`
  (`git -C <lane> rev-parse HEAD`, read-only).
- Gate `tools/research-gate.sh` sha256 = `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098` — matches the landed candidate.
- Counter `c2-count-v2.py` sha256 = `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a` — identical to the L1 v2 receipt's `counter_sha256` (`.ufo/waves/round-32/measure/after-c2-s32011.json`), i.e. the committed counter ran unmodified.
- Seeds 520101–520110 chosen fresh: not present in any receipt under `.ufo/waves/round-32/` (grep of `"seed": N` there shows 32011/32012/3221/3222/… only).
- `C2_TMP=TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/RerunC2a/tmp` (outside the lane root); `df -h /fast` = 219G free beforehand.

## Command (run once, sequential; per-run `timeout 300`, loop `timeout 870`)

```
for s in 520101 ... 520110; do
  C2_TMP=$SCRATCH/tmp TMPDIR=$SCRATCH/tmp timeout 300 \
    python3 corpus/evidence/round32/c2-count-v2.py --seed $s \
    --receipt .ufo/waves/round-32/w2/RerunC2a/rerun-c2-s$s.json
done
```

## Results — all ten runs printed `EXEMPT_AUDIT_MATCH=132/132`, exit 0

| seed | matched | predicate_holds | gate_rc | record_fails | misses | elapsed_s |
|---|---|---|---|---|---|---|
| 520101 | 132/132 | true | 1 | [] | [] | 14.858 |
| 520102 | 132/132 | true | 1 | [] | [] | 13.758 |
| 520103 | 132/132 | true | 1 | [] | [] | 14.181 |
| 520104 | 132/132 | true | 1 | [] | [] | 9.303 |
| 520105 | 132/132 | true | 1 | [] | [] | 8.918 |
| 520106 | 132/132 | true | 1 | [] | [] | 11.215 |
| 520107 | 132/132 | true | 1 | [] | [] | 9.335 |
| 520108 | 132/132 | true | 1 | [] | [] | 9.604 |
| 520109 | 132/132 | true | 1 | [] | [] | 9.781 |
| 520110 | 132/132 | true | 1 | [] | [] | 25.818 |

Minimum observed count: **132/132** (no run below target; `misses` empty in every receipt).
Every receipt carries `gate_sha256=10f2fe12…`, `counter_sha256=8ec1a1ed…`, `gate_rc=1`.
Receipts: `.ufo/waves/round-32/w2/RerunC2a/rerun-c2-s{520101..520110}.json` (~1 KiB each).

## Note on working-copy state

`git status --porcelain` on production paths shows unrelated `M` entries (`SKILL.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`) — other seats' wave-2
work in progress, not mine; I created only `w2/RerunC2a/` + scratch. The two artifacts
the measurement depends on (gate + counter) are byte-identical to the landed revision,
and the fixture root sits outside the lane, so these do not enter the gate run.

## Verdict

**HOLDS.** Under my attack the claim P2 v2 stands: 10/10 fresh-seed runs of the
committed counter on the landed gate print `EXEMPT_AUDIT_MATCH=132/132`
(`predicate_holds=true`), minimum 132, zero misses. No BROKEN signal from this seat.

## Limits

- I exercised only the frozen predicate surface (count + record checks + per-class
  buckets); a contract flaw invisible to the counter (e.g. a harm outside the exempt
  arm) is out of this seat's scope — covered by sibling seats.
- Timing observed 8.9–25.8 s/run on a loaded host; no run neared the counter's
  600 s gate timeout.
