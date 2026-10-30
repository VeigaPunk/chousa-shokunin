# Probe14 — round65 missing-blob receipt fixture (summary)

Scoped surface: missing-blob behavior of the round65 receipt-pin contract, exercised
against the frozen reference `corpus/evidence/round65/controls/ref-receipt-pin.py`
(production `tools/receipt-pin.py` absent, as C1's before-control expects). Freeze
`f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` verified as lane HEAD.

Isolated scratch fixture (own `git init` repo, no clone/fetch, TMPDIR pinned, scratch
deleted after receipt copy). Expectations derived independently from the frozen C1
format before running: a receipt whose named path has no blob at
`<revision>:<path>` cannot bind a digest → invalid → **exit 1**, token
**`RECEIPT_PIN=FAIL blob/digest`** per the reference contract.

Result: **4/4 cases match.**

- A positive control (existing blob, correct digest): exit 0 `RECEIPT_PIN=PASS`.
- B missing path @ valid revision: exit 1 `RECEIPT_PIN=FAIL blob/digest` (cat-file rc 128).
- C missing revision (absent object): exit 1 `RECEIPT_PIN=FAIL blob/digest` (rc 128).
- D lane repo @ freeze, missing path: exit 1 `RECEIPT_PIN=FAIL blob/digest` (rc 128).

Findings: missing-blob is classified invalid (1), never usage (2) nor consistent (0);
missing-path / missing-revision / lane-freeze variants are indistinguishable at the
exit+token level, so one battery case asserting `1 / RECEIPT_PIN=FAIL blob/digest` is
robust across constructions; the reference short-circuits on cat-file nonzero rc without
hashing working-tree bytes. No installs (python 3.14.8, git 2.56.0 preinstalled).
Full evidence and receipts: `.ufo/waves/round-65/w1/Probe14/` (`report.md`,
`probe14-missing-blob-results.json`, `*.receipt`). No production writes; no git/jj
mutations; leaf seat, no subagent dispatch.
