# W3MutC2 — mutation test of the C2 counter (round 44, wave 3)

Leaf seat. Mutations on copies under `/tmp` only; production `disposition.tsv`
and `c2-count.py` untouched (read-only). No fetch, no jj/git.

## Axes named

- **Operability**: did the mutants actually execute, and did the counter behave
  as its docstring promises (0 pass / 1 count-failed)?
- **Calibration**: baseline must be a true PASS (exit 0) before any mutant run
  means anything; a mutant that still PASSes would mean the gate is deaf.
- **Depth**: use two mutation classes with distinct failure signatures, so the
  run shows the gate catches *different* ways of being wrong, not just one.

## Baseline (pristine table, no mutation)

```
$ python3 corpus/evidence/round44/c2-count.py
CONSISTENT=39/39
REVERIFIED=36/36
LEFT_NAMED=3/3
C2=PASS
EXIT=0
```

True PASS confirmed first; the mutants below are therefore meaningful.

## Mutant A — corrupt one reverified-commit sha256

Copy: `/tmp/w3-mut-sha.tsv`. Row 2 (`.ufo/waves/round-40/w1/CriticC1Control.md`)
digest replaced with 64 zeros, same length, so only the digest predicate breaks:

```
2c2
< .ufo/waves/round-40/w1/CriticC1Control.md	reverified-commit	771e948765baf3cd2864c1192a7ddf54c526cbfe00c0cbeb474af68a4ceaede3	...
---
> .ufo/waves/round-40/w1/CriticC1Control.md	reverified-commit	0000000000000000000000000000000000000000000000000000000000000000	...
```

```
$ python3 corpus/evidence/round44/c2-count.py --table /tmp/w3-mut-sha.tsv
CONSISTENT=38/39
REVERIFIED=35/36
LEFT_NAMED=3/3
C2=FAIL
EXIT=1
```

## Mutant B — delete one row entirely

Copy: `/tmp/w3-mut-delrow.tsv` (38 lines vs 39). Deleted row 39,
`corpus/evidence/round41/receipts/cells/cells.json` (a left-named row), chosen
deliberately so the failure signature differs from Mutant A:

```
39d38
< corpus/evidence/round41/receipts/cells/cells.json	left-named	-	left-named; not hunk-verified; ...
```

```
$ python3 corpus/evidence/round44/c2-count.py --table /tmp/w3-mut-delrow.tsv
CONSISTENT=38/39
REVERIFIED=36/36
LEFT_NAMED=2/3
C2=FAIL
EXIT=1
```

## Verdict

- Both mutants are **killed** by the gate: distinct signatures (A drops
  `REVERIFIED` 36→35; B drops `LEFT_NAMED` 3→2), both `C2=FAIL`, both exit 1,
  matching the documented exit-code contract. No false PASS under either class
  of corruption; baseline remains a true PASS. Predicate R44-C2's counting gate
  is mutation-sensitive in the right direction on the axes exercised.
- Both counters moved by exactly 1 — the gate localizes the damage rather than
  collapsing to a blanket fail, which is what makes it usable as a disposition
  gate rather than just a tripwire.

## Scope and honesty notes

- Single-point mutations, one row each; table-side only. The files on disk the
  script hashes were not touched, so the sha256/round-token/length half of the
  reverified-commit predicate ran against real content in every run; only the
  table half was perturbed.
- `--table` was the only flag varied; `--root` stayed at the lane default.
- One stray `--table ... --help` invocation occurred in the Mutant B shell
  line; argparse short-circuits before any counting, output discarded — not a
  result and none of the pasted runs above.
- Unrun, therefore not claimed: deleting a *reverified-commit* row (predicted
  `REVERIFIED=35/36` via the `rows.get` default, same shape as A), corrupting a
  left-named row's reason string, and the table-missing branch. Those are
  predictions from reading the script, not observations.
- Mutant copies left at `/tmp/w3-mut-sha.tsv` and `/tmp/w3-mut-delrow.tsv` for
  reproduction.
