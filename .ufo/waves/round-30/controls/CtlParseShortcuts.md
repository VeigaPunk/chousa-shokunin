# CtlParseShortcuts — C1 controls

Receipt/code directory `D = .ufo/waves/round-30/controls/CtlParseShortcuts/` (lane-relative). All three frozen hashes matched the assignment before scoring and after restoration. Fetch, verdict order and the original deadline implementation were copied unchanged from the round-29 tool; no contract-v2 fix was built.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| raw-grep | HTML parsing; searches raw markup after the tool's normal decoding/normalization | 27/106, 29/106 | not run, not run | `D/receipt-raw-grep-run1.json`, `D/receipt-raw-grep-run2.json` |
| skip-nothing | head suppression only; removes `head` from SKIP and keeps title text | 86/106, 86/106 | not run, not run | `D/receipt-skip-nothing-run1.json`, `D/receipt-skip-nothing-run2.json` |
| tag-strip | HTML parsing and hidden-content suppression; substitutes `<[^>]+>` with empty text | 66/106, 66/106 | not run, not run | `D/receipt-tag-strip-run1.json`, `D/receipt-tag-strip-run2.json` |
| casefold | case-sensitive matching; otherwise original parser | 72/106, 72/106 | not run, not run | `D/receipt-casefold-run1.json`, `D/receipt-casefold-run2.json` |
| keep-script | script suppression only; removes `script` from SKIP, retaining original head behavior | 74/106, 72/106 | not run, not run | `D/receipt-keep-script-run1.json`, `D/receipt-keep-script-run2.json` |

META-CHECK: none met

Expected detector: frozen C1 target `QUOTE_REOPEN_HEADLESS_MATCH=106/106`, exit 0. Actual stdout used that label with the table's scores; every scored counter exited 1, with no killed harness child. Each run1 scored an isolated scratch mutant; run2 scored its byte-identical retained `D/<control>.py` artifact. All 20 pristine/mutated/restored runs had distinct fresh seeds. C2 was not exercised.

## Per-class misses

Computed as `total - matched` from each receipt's complete `by_class`, not its capped `misses_first40`. Cells are **misses run1/run2**, not fractions. Unlisted classes, including every verdict-order class, have zero misses for all five controls.

| by_class key | raw-grep | skip-nothing | tag-strip | casefold | keep-script |
|---|---|---|---|---|---|
| closed-head/body-window | 12/11 | 0/0 | 0/0 | 0/0 | 0/0 |
| closed-head/case-flip | 0/0 | 0/0 | 0/0 | 6/6 | 0/0 |
| closed-head/script-window | 6/6 | 0/0 | 6/6 | 0/0 | 4/6 |
| closed-head/title-window | 6/6 | 6/6 | 6/6 | 0/0 | 0/0 |
| headless-body/body-window | 9/10 | 0/0 | 0/0 | 10/10 | 10/10 |
| headless-body/script-window | 5/5 | 0/0 | 5/5 | 0/0 | 0/0 |
| headless-body/title-window | 5/5 | 5/5 | 5/5 | 0/0 | 0/0 |
| headless-nobody/body-window | 10/9 | 0/0 | 0/0 | 10/10 | 10/10 |
| headless-nobody/script-window | 5/5 | 0/0 | 5/5 | 0/0 | 0/0 |
| headless-nobody/title-window | 5/5 | 5/5 | 5/5 | 0/0 | 0/0 |
| headless-text/body-window | 8/7 | 0/0 | 0/0 | 8/8 | 8/8 |
| headless-text/script-window | 4/4 | 0/0 | 4/4 | 0/0 | 0/0 |
| headless-text/title-window | 4/4 | 4/4 | 4/4 | 0/0 | 0/0 |

## Findings and mutation verdict

No design invalidation observed. Dropping head suppression alone exposes all 20 title windows (`D/skip-nothing.py:58`; construction labels `corpus/evidence/round30/c1-count.py:223-229`). Regex stripping exposes those titles and all 20 script windows (`D/tag-strip.py:104-106`). Casefold and script-retention misses on this base are confined to closed-head regressions in addition to its existing body misses; the original head skip still masks headless content (`tools/quote-reopen.py:58,83-101`). These probes do not establish mutation kills on a repaired tool.

**Mutation-kill verdict: inconclusive for all five**, not killed/survived: every pristine baseline already fails C1 at 78/106. As pre-data controls, all five remain below the frozen 106/106 target.

## Exact-byte restoration

Each `/fast/scratch/hyaku/chousa-r30/CtlParseShortcuts/<control>.py` was scored pristine, mutated, then restored from `D/pristine.py` and scored again with the same bounded C1 invocation (`timeout 300`; harness cap 180 seconds). All five pristine and all five restored outputs were `QUOTE_REOPEN_HEADLESS_MATCH=78/106`, exit 1. Before/after receipts: `D/receipt-pristine-<control>.json`, `D/receipt-restored-<control>.json` for each control above.

Common pristine/restored SHA-256: `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`. Direct final `sha256sum` matched this for all five scratch files, `D/pristine.py`, and the untouched lane tool. Retained mutants and both mutated receipts agree on these hashes:

| control | mutated SHA-256 |
|---|---|
| raw-grep | `9c6b1b61d0dc6d249b4ead10ca725e8cb0fc67ba034e05f22fc4f982955caa77` |
| skip-nothing | `b1faf3d86b3af509cbb9e911b592a3803f3f945aaaef1136211284ad3e9142e2` |
| tag-strip | `8cbde5d6868f9d1da907790b715581ca142c6a92c59b13cbeaa7f2a2150c8fae` |
| casefold | `c19f927aeee2dd1ec68b074049886dc810cfc6597869b9881716f8d4fc1527e1` |
| keep-script | `7bf0d7ee05bfd783fc2828933f1de35d47ca6b2ce7af4e0bb5b776556c6ba5e3` |

All counter processes returned and their harness children exited (`tool_killed=false`); no long-lived process was started. Temporary harness writes stayed under the seat's scratch directory (`TMPDIR`); bytecode writes were disabled. No network fetch, source/counter edit, git/jj operation, tool installation or update occurred.

**Harness-v3 re-score** (freeze `7908ce2a6413522fc6fab63f284327693f70eec6`): verified all three newly frozen hashes before scoring; C1 remains unchanged and every new receipt records harness SHA-256 `16f17d60708952f9ba3d015eae306a075b37691deebf1e5c2c126137c6797ab7`. One fresh run per unchanged control: raw-grep **26/106**, skip-nothing **86/106**, tag-strip **66/106**, casefold **72/106**, keep-script **75/106**. Receipts: `D/receipt-raw-grep-h3.json`, `D/receipt-skip-nothing-h3.json`, `D/receipt-tag-strip-h3.json`, `D/receipt-casefold-h3.json`, `D/receipt-keep-script-h3.json`. All exited 1, `predicate_holds=false`, `tool_killed=false`; retained tool hashes match the table above. No new mutation or C2 measurement. **META-CHECK: none met.**

H3 `by_class` misses (unlisted keys zero): raw-grep misses every body-window (closed-head 12, headless-body 10, headless-nobody 10, headless-text 8), every title-window and every script-window (6, 5, 5, 4 by those same document classes); skip-nothing misses every title-window (6, 5, 5, 4); tag-strip misses every title-window and script-window (6, 5, 5, 4 each); casefold misses headless body-window classes (10, 10, 8) and closed-head/case-flip (6); keep-script misses headless body-window classes (10, 10, 8) and closed-head/script-window (3).

**Design-v4 re-score** (freeze `abfdf93274d0c70e02465e22abcf029dea59efb9`): verified all three newly frozen hashes before scoring. New receipts record C1 SHA-256 `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6` and harness SHA-256 `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4`. One fresh run per unchanged control: raw-grep **30/106**, skip-nothing **86/106**, tag-strip **66/106**, casefold **72/106**, keep-script **75/106**. Receipts: `D/receipt-raw-grep-v4.json`, `D/receipt-skip-nothing-v4.json`, `D/receipt-tag-strip-v4.json`, `D/receipt-casefold-v4.json`, `D/receipt-keep-script-v4.json`. All exited 1, `predicate_holds=false`, `tool_killed=false`; retained tool hashes match the table above. No new mutation or C2 measurement. **META-CHECK: none met.**

V4 `by_class` misses (unlisted keys zero): raw-grep misses body-window classes (closed-head 10, headless-body 10, headless-nobody 8, headless-text 8), every title-window and every script-window (6, 5, 5, 4 by those same document classes); skip-nothing misses every title-window (6, 5, 5, 4); tag-strip misses every title-window and script-window (6, 5, 5, 4 each); casefold misses headless body-window classes (10, 10, 8) and closed-head/case-flip (6); keep-script misses headless body-window classes (10, 10, 8) and closed-head/script-window (3).
