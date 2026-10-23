# ExecRerunCount — D2 re-run-count checker

Delivered `.ufo/waves/round-30/build/ExecRerunCount/rerun-check.py` (stdlib
only, ~140 lines): takes a list of receipt files plus a stated count, prints
one `seed=` line per receipt, then `RERUN_RECEIPTS=<distinct seeds>/<stated>`
and exits 0 on agreement, 1 on mismatch, 2 when an input carries no seed or
no match line (a failed measurement, not a run). A receipt file may be JSON
(`seed` + `match`/`total`, or `seed` + `label` + `n`/`t`, or `seed` +
`match_line`) or a captured counter-output file with `seed=<int>` and
`NAME=n/t` lines — the shape a receipt-less run leaves behind.

## The defect, located

The round-29 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/chousa.md`
"Before → after" section, 4th bullet) says "Wave 2 re-ran it independently
6 more times"; `SCORECARD.md:1603` says "130/130 in 6 further runs
(RerunCounterA, RerunCounterB x2, ScoutFreshnessH x3)". `ScoutFreshnessH.md:18`
lists run 2 seed `12970099299958901445` but cites `rederive3.out`, which
records run 3's seed `3497534629407128034`. A repo-wide grep finds seed
`12970099299958901445` only in that report table — no committed artifact
holds it. The committed evidence therefore holds 5 runs.

## Evidence runs (all from the lane root, no network)

Command 1 — stated count 6, expect failure:

```
timeout 60 python3 .ufo/waves/round-30/build/ExecRerunCount/rerun-check.py --stated 6 \
  .ufo/waves/round-29/falsify/RerunCounterA/receipt.json \
  .ufo/waves/round-29/falsify/RerunCounterB/receipt-1.json \
  .ufo/waves/round-29/falsify/RerunCounterB/receipt-2.json \
  .ufo/waves/round-29/falsify/ScoutFreshnessH/rederive-receipt.json \
  .ufo/waves/round-29/falsify/ScoutFreshnessH/rederive3.out
```

Output (`EXIT=1`):

```
seed=16442982337510174646  MATCH=130/130            RerunCounterA/receipt.json
seed=5392061795029416258   MATCH=130/130            RerunCounterB/receipt-1.json
seed=1932010155184684229   MATCH=130/130            RerunCounterB/receipt-2.json
seed=13173258806708832500  MATCH=130/130            ScoutFreshnessH/rederive-receipt.json
seed=3497534629407128034   QUOTE_REOPEN_MATCH=130/130  ScoutFreshnessH/rederive3.out
RERUN_RECEIPTS=5/6
EXIT=1
```

Command 2 — same files, true count 5, expect pass: same seed lines then
`RERUN_RECEIPTS=5/5`, `EXIT=0`.

Edge checks: passing `RerunCounterA/receipt.json` twice yields
`RERUN_RECEIPTS=4/4` with a stderr note (seeds deduplicate); a non-receipt
input (`SCORECARD.md`) exits 2 with `no seed field and no seed= line`.

## Per-receipt seeds (committed evidence)

| file | seed | source of seed |
|---|---|---|
| `RerunCounterA/receipt.json` | 16442982337510174646 | JSON `seed` field |
| `RerunCounterB/receipt-1.json` | 5392061795029416258 | JSON `seed` field |
| `RerunCounterB/receipt-2.json` | 1932010155184684229 | JSON `seed` field |
| `ScoutFreshnessH/rederive-receipt.json` | 13173258806708832500 | JSON `seed` field (run 1) |
| `ScoutFreshnessH/rederive3.out` | 3497534629407128034 | `seed=` line in captured stdout (run 3) |
| (none) | 12970099299958901445 | report table only — no committed artifact |

## Verdict

Checker shown able to fail and to pass: `RERUN_RECEIPTS=5/6` exit 1 on the
stated count, `RERUN_RECEIPTS=5/5` exit 0 on the true count. The stated count
of 6 is wrong by exactly one run — ScoutFreshnessH run 2 has no committed
receipt or output file.

## Limits

- Receipts are trusted as recorded; the checker does not re-execute the
  counter or verify receipt signatures/hashes.
- A `.out` capture is accepted as run evidence because it carries both the
  seed and the match line the counter printed; a JSON receipt is preferred
  when both exist (`rederive.out` and `rederive-receipt.json` hold the same
  seed and count once).
- No installs; python3 stdlib only. Writes: this report and the checker,
  both under `.ufo/waves/round-30/build/ExecRerunCount/`.

Report: .ufo/waves/round-30/build/ExecRerunCount.md
