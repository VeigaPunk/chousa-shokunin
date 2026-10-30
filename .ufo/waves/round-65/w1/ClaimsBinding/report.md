# ClaimsBinding report — round65

Full findings: `.ufo/waves/round-65/w1/ClaimsBinding.md`.

- Freeze `f99de3bd…` is HEAD; parent `d6ed8155…`. Claims file has exactly two claims (C1, C2).
- C1 and C2 counters match their docstrings and predicates. Control receipts reproduce: C1 before 0/20 exit 1, C1 reference 20/20 exit 0, always-pass 3/20, always-fail 17/20, C2 before 0/10 exit 1.
- Source checksums and quotes for S154–S157 verified.
- BASE SOURCES.md has 153 rows (matches census). Working tree has 157 (S154–S157 uncommitted).
- Working-tree drift and untracked `source-openings.json` flagged for L1.
- No tool installs. Scratch removed. No production writes.
