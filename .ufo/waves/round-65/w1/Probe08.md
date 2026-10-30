# Probe08 — round65 negative-exit probe (seat report)

Scoped result: the reference receipt-pin control's negative-exit surface matches
the frozen format expectation derived independently from round65 claims.md.

- Expectation: `EXIT` grammar is unsigned decimal 0..255 ⇒ `EXIT=-1` is invalid ⇒
  exit code 1 with a `RECEIPT_PIN=FAIL` token (exit 2 reserved for usage/environment).
- Fixture: 8 receipts, digest bound to real blob `d6ed8155…:SKILL.md` via read-only
  `git -C <lane> cat-file`; argv preserved (`--receipt/--root/--revision`).
- Outcome: 8/8 CONSISTENT. Frozen battery case `negative-exit` → rc=1,
  `RECEIPT_PIN=FAIL header/body`; minus-sign family (-1, -0, -255, -256, `- 1`,
  `--1`) all rejected at rc=1; in-grammar controls EXIT=0 and EXIT=255 pass,
  proving sign-driven (not magnitude-driven) rejection.
- Verdict: reference semantics for negative-exit are frozen-format-exact; a
  production `tools/receipt-pin.py` must reproduce rc=1 + FAIL token on this case
  to satisfy c1-count.py's `negative-exit` row.
- No tools installed (python3 stdlib + system git only). No production writes;
  no git/jj mutations; lane repo used read-only at freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
- Full detail + verbatim log: `.ufo/waves/round-65/w1/Probe08/report.md`
  (evidence: `probe08-run.log`, `negative-exit-frozen.receipt.txt`, `probe08-negative-exit.py`).
