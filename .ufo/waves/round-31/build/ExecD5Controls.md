# ExecD5Controls — D5 tally: v4 control receipt maxima (round 30)

Assignee: ChousaR31.ExecD5Controls (leaf, wave 1 build). Date: 2026-10-23.

## Task
Routed defect D5 (round-30-verifier-spotcheck.md:182-183): verify the v4 C1 control
maximum (86/106, not 84) by tallying every receipt under
`.ufo/waves/round-30/controls/` carrying the v4 counter hashes (C1 `5b312d84…`,
C2 `0a59e373…`).

## Method
Wrote and ran a read-only Python tally (no lane files modified; no tools installed;
no network):

- script: `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.py`
- output: `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out`
- command: `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && timeout 600 python3 .ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.py | tee .ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out`
- exit code: 0 (EXIT=0); 61 receipts matched a v4 counter hash, all parsed, zero SKIPs.

Match rule: `counter_sha256` prefix `5b312d84` → C1 v4, `0a59e373` → C2 v4
(full hashes `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6` /
`0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f`, as recorded in
receipts). No-reader = receipt under `CtlNoReader/` or `net_connect_events == 0`.

## Results (table)

| Axis | Max | Score | predicate_holds | Receipt path (rel. to lane root) | Tool |
|---|---|---|---|---|---|
| C1 v4 overall | **86/106** | n=86, t=106 | false | `CtlParseShortcuts/receipt-skip-nothing-v4.json` | `CtlParseShortcuts/skip-nothing.py` |
| C1 v4 no-reader | **84/106** | n=84, t=106 | false | `CtlNoReader/receipt-relational-v4-c1-v4-run2.json` | `CtlNoReader/relational-v4.py` |
| C2 v4 overall | **18/27** | n=18, t=27 | false | `CtlDeadlineShortcuts/receipt-wall-cutoff-38-v4-run1.json` | `/fast/scratch/hyaku/chousa-r30/CtlDeadlineShortcuts/probe.py` |
| C2 v4 no-reader | **14/27** | n=14, t=27 | false | `CtlNoReader/receipt-eight-absent-c2-v4-run1.json` | `CtlNoReader/eight-absent.py` |

All 61 v4 receipts have `predicate_holds=false`; none passes its predicate (expected:
controls must stay below 120/120). C1 next-highest: 84 (the no-reader max), 79
(relational-v4 run1), 78 (do-nothing / baseline / dns_header_keyed / before). C2
next-highest: 17/27 (wall-cutoff-38 run2, wall-cutoff-10 runs 1-2).

Per-control run table (C1/C2, all v4) is in `tally_v4_receipts.out`.

## D5 verdict
Confirmed. The committed v4 C1 control maximum is **86/106** at
`CtlParseShortcuts/receipt-skip-nothing-v4.json`; 84/106 is the best v4 C1 no-reader
control (`CtlNoReader/receipt-relational-v4-c1-v4-run2.json`). The spot-check defect
statement at lines 182-183 already states these facts; the round-31 repair draft
should append the dated verification below.

Exact corrected sentence (append-only, dated 2026-10-23):

> [2026-10-23] D5 verified by receipt tally: the committed v4 C1 control maximum is
> 86/106 (`CtlParseShortcuts/receipt-skip-nothing-v4.json`, `skip-nothing.py`,
> predicate_holds=false), and the best v4 C1 no-reader control is 84/106
> (`CtlNoReader/receipt-relational-v4-c1-v4-run2.json`, `relational-v4.py`); the v4
> C2 control maximum is 18/27 (`CtlDeadlineShortcuts/receipt-wall-cutoff-38-v4-run1.json`),
> and the best v4 C2 no-reader control is 14/27
> (`CtlNoReader/receipt-eight-absent-c2-v4-run1.json`).

## Limits / risks
- Only receipts under `.ufo/waves/round-30/controls/` were tallied (per assignment);
  L1 smoke runs and other rounds' receipts are out of scope. All `.json` files there
  were walked recursively (no glob truncation).
- C2 receipts carry a `design` field value "v3" in some files but the v4 counter hash;
  version was keyed on `counter_sha256` as instructed, not on that field.
- No tools installed or updated; no network; no lane files modified (tally script and
  output live only in `.ufo/waves/round-31/build/ExecD5Controls/`).
