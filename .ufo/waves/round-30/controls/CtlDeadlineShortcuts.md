# CtlDeadlineShortcuts — C2 control probe

Current results use design v4, freeze `abfdf93274d0c70e02465e22abcf029dea59efb9`, target 27/27. Paths below are relative to `.ufo/waves/round-30/controls/`. C1 was not run.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| `socket-timeout-05.py` | Total deadline; every socket operation gets 0.5 s instead | not run | 11/27, 11/27 | `CtlDeadlineShortcuts/receipt-socket-timeout-05-v4-run{1,2}.json` |
| `wall-cutoff-10.py` | DEADLINE; fixed 1.0 s alarm, unchanged DNS/connect path | not run | 17/27, 17/27 | `CtlDeadlineShortcuts/receipt-wall-cutoff-10-v4-run{1,2}.json` |
| `refuse-on-rebind.py` | Validated-address binding; refuse unequal pre-fetch DNS answers | not run | 13/27, 13/27 | `CtlDeadlineShortcuts/receipt-refuse-on-rebind-v4-run{1,2}.json` |
| `refuse-all-redirects.py` | All redirect fetching; round-29 path otherwise unchanged | not run | 13/27, 12/27 | `CtlDeadlineShortcuts/receipt-refuse-all-redirects-v4-run{1,2}.json` |
| `first-answer-global.py` | Checks after first global answer; original connection path unchanged | not run | 12/27, 13/27 | `CtlDeadlineShortcuts/receipt-first-answer-global-v4-run{1,2}.json` |
| `wall-cutoff-38.py` | DEADLINE; fixed 3.8 s alarm, unchanged DNS/connect path | not run | 18/27, 17/27 | `CtlDeadlineShortcuts/receipt-wall-cutoff-38-v4-run{1,2}.json` |

META-CHECK: none met

All 12 control runs printed `QUOTE_REOPEN_FETCH_BOUND_MATCH=<score above>` and exited 1; all 12 seeds differ. No measurement exited 2. Detector: `timeout 300 python3 corpus/evidence/round30/c2-count.py --tool <probe.py> --receipt <receipt.json>`, with `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` confined to this seat’s scratch.

## Per-kind failures from receipt `items`

Counts are failed/total within each kind. V = wrong/missing verdict; B = wall bound failed; D = unvalidated destination; K = harness killed the item process. Unlisted kinds matched.

| control | run1 failures | run2 failures |
|---|---|---|
| `socket-timeout-05` | drip-body 3/3 (VBK); drip-head 2/2 (VBK); drip-steady 2/2 (VBK); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D); slow-ok 1/2 (V) | same as run1 |
| `wall-cutoff-10` | rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D); slow-ok 2/2 (V) | same as run1 |
| `refuse-on-rebind` | drip-body 3/3 (VBK); drip-head 2/2 (VBK); drip-steady 1/2 (B); rebind-loop 4/4 (V); rebind-private 2/2 (V); rebind-redirect 2/2 (V) | same as run1 |
| `refuse-all-redirects` | drip-body 3/3 (VBK); drip-head 2/2 (VBK); drip-steady 1/2 (B); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (V) | drip-body 3/3 (VBK); drip-head 2/2 (VBK); drip-steady 2/2 (B); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (V) |
| `first-answer-global` | drip-body 3/3 (VBK); drip-head 2/2 (VBK); drip-steady 1/2 (B); mixed-address 1/1 (V); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D) | drip-body 3/3 (VBK); drip-head 2/2 (VBK); mixed-address 1/1 (V); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D) |
| `wall-cutoff-38` | rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D); slow-ok 1/2 (V) | drip-body 1/3 (B); rebind-loop 4/4 (D); rebind-private 2/2 (VD); rebind-redirect 2/2 (D); slow-ok 1/2 (V) |

## Restoration and identities

Pristine: `QUOTE_REOPEN_FETCH_BOUND_MATCH=12/27`, exit 1 (`CtlDeadlineShortcuts/receipt-pristine-c2-v4.json`). Restored: `QUOTE_REOPEN_FETCH_BOUND_MATCH=13/27`, exit 1 (`CtlDeadlineShortcuts/receipt-restored-c2-v4.json`). Because pristine already fails, formal mutant-kill attribution is **inconclusive**, not a killed-mutant claim. Every shortcut is below the target.

The scored working file was `/fast/scratch/hyaku/chousa-r30/CtlDeadlineShortcuts/probe.py`. Retained `<control>.py` files are byte-identical to their mutant receipts. Before the probe and after exact restoration, scratch, `round29-pristine.py`, and untouched lane `tools/quote-reopen.py` all had SHA-256:

`72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`

| retained control / mutation point | mutant SHA-256 |
|---|---|
| `CtlDeadlineShortcuts/socket-timeout-05.py:243,277,280,331` | `31955ef0d9b98d7e5fbdac4200c55620c0a34be400d6eedadb5f82e4d1021f75` |
| `CtlDeadlineShortcuts/wall-cutoff-10.py:332,352-365` | `15ab36c03b4d1bc9cfdc5db3d90b80dd75166022af375e7a34f023454089a5b1` |
| `CtlDeadlineShortcuts/refuse-on-rebind.py:189-192` | `8465e58274f32eb125bc086689c98f579b082ee79f1363efba9c8a7e9ca88ded` |
| `CtlDeadlineShortcuts/refuse-all-redirects.py:289-290` | `30f11a444ccd8ad8d3e8e6218e5e0ace2ba81bd6d9d156a185e6877196199924` |
| `CtlDeadlineShortcuts/first-answer-global.py:199-206` | `9385b0f17258bab0ff13cb4b7ac42bf9ef1d474b35308c95e4c981b86f91c09b` |
| `CtlDeadlineShortcuts/wall-cutoff-38.py:332,352-365` | `3cacbdadfd7c570d6d5e8b2881efec84783e1ead60be59bbac815334245899eb` |

Frozen SHA-256 checked before each v4 control pair and restored measurement:
- `c1-count.py`: `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6`
- `c2-count.py`: `0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f`
- `qr_harness.py`: `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4`

## Findings and history

- Baseline/restored scores differ only in `drip-steady` (0/2 versus 1/2 matches), on identical source bytes. Per-item deadlines are random (`corpus/evidence/round30/c2-count.py:119`), and scoring allows DEADLINE + 1.5 s (`:160,169`). The observed before score is therefore not constant across draws; this did not make a control meet 27/27.
- v4 retains a stale `"design": "v3"` receipt field (`corpus/evidence/round30/c2-count.py:218`); version identification here uses the authorized hashes, not that field.
- v2 history: tiny socket timeout scored 9/20 twice in `CtlDeadlineShortcuts/receipt-socket-timeout-05-v2-run{1,2}.json`; pristine 9/20 is `receipt-pristine-c2-v2.json` in the same directory.
- v3 history: tiny socket 12/27,11/27; 1 s cutoff 17/27,17/27; refuse-rebind 12/27,13/27; refuse-redirects 13/27,12/27. Receipts retain `-v3-` names. First-answer and 3.8 s were unrun on v3: the C1 hash changed at the pre-score gate, so scoring stopped until v4 authorization. Pristine v3 was 13/27 (`receipt-pristine-c2-v3.json`).
- One attempted asynchronous 3.8 s launch hit the global background-job limit before starting a detector; the two retained v4 measurements were then run synchronously. All started detector processes exited; capped item processes were reaped by the harness. No lane source, counters, git/jj state, or sibling files were edited. No tools were installed or updated.
