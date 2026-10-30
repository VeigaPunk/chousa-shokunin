# Probe07 — no-exit reference probe

Detailed report: `.ufo/waves/round-65/w1/Probe07/report.md`.

Frozen format independently requires EXIT; omitting its header makes the receipt invalid: expected exit 1 with `RECEIPT_PIN=FAIL ` prefix. Exactly one isolated reference-validator invocation observed exit **1**, stdout exactly `RECEIPT_PIN=FAIL header/body\n`, empty stderr. Classification matches expectation; diagnostic suffix is observed, not a frozen exact requirement.

Retained exact receipt, argv/output/status JSON, and executed fixture driver in `.ufo/waves/round-65/w1/Probe07/` as `probe07-noexit-receipt.txt`, `probe07-noexit-run.json`, and `probe07-noexit-driver.py`. Evidence records lane freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` and receipt revision `d6ed8155e9b4735639a2cf0a3e479c62f2056195`.

No production changes or full battery; production tool was absent when inspected. Scratch removed after retaining evidence. No installations. No blocker; production and post-integration gate remain L1's responsibility. This probe makes no execution-authenticity or broader-parser claim.
