source: S059 — Python 3.15.1 `hashlib`, https://docs.python.org/3/library/hashlib.html#hash-algorithms; local application: `corpus/evidence/round39/verify-receipts.py:73-79,138-139`
verified-at: 2026-10-24 — re-opened S059 and re-derived the r39 stale-expectation refusal and regenerated active receipt set
recheck: 90d — from the lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`, run `python3 corpus/evidence/round40/c1-count.py`

# Receipt expectation digests — round 40

## Question

What does a receipt's `expect_sha256` establish, and why can a receipt fail after its scenario rows still match the current expectation table?

## Observation

S059 states that a hash object's digest is computed over the concatenation of the bytes supplied to it. The round-39 verifier streams the selected expectations file through `sha256_file` and compares that digest with the receipt's `expect_sha256` before re-deriving the scenario census and each row's expectation (`corpus/evidence/round39/verify-receipts.py:73-79,138-139`). Therefore a receipt's expectation digest binds the exact file bytes, not only the individual rows it happens to cite.

At round-39 closure, `expectations.jsonl` was `01cbdc3a…`, while four c1 receipts carried `3abd2dcb…`. Three receipts refused `expect-sha256-mismatch`; the superseded drafting receipt `c1-mutenv-s39003.json` refused first on `counter-sha256-mismatch` because its counter bytes were not committed. Reissued base, landed-gate, and mutant-control receipts use the committed expectation bytes. Their originals remain preserved and are not re-labelled as valid.

## Limit

A matching file digest establishes byte identity for the supplied input; it does not establish the truth of a claim, the authority of a source, or who authored a receipt. Those require separate source and provenance checks. The r39 verifier's scenario re-derivation is structural evidence about the counter's declared expectations, not an independent semantic oracle.

## Round-40 evidence

The red-before verifier outputs and the exact stale/current expectation hashes are in `.ufo/waves/round-40/controls/r1-stale-before.txt`. The committed active population and its recheck are `corpus/evidence/round40/active-r39-receipts.tsv` and `corpus/evidence/round40/c1-count.py`.
