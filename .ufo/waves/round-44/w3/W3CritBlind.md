# W3 Crit — blind attack on C2's kill rule (c2-count.py)

Round 44 wave 3. Two mutations of `corpus/evidence/round44/disposition.tsv`, applied to copies
under `/tmp/w3-c2-mut/` only (production table untouched), each a single-line diff from the
unmutated baseline. Counter run frozen as instructed:
`python3 corpus/evidence/round44/c2-count.py --table <copy>`.

## Mutation (a): blank the reason of one reverified-commit row

Line 1, field 4 emptied (trailing tab kept, so still 4 fields):

```
> .ufo/waves/round-40/w1/ConnectorSiblingScan.md	reverified-commit	f0e58b2b…11b	
```

Stdout:

```
CONSISTENT=38/39
REVERIFIED=35/36
LEFT_NAMED=3/3
C2=FAIL
EXIT=1
```

**Caught.** `ok` requires `reason.strip()` non-empty (c2-count.py:101); the blank reason drops
exactly that one row: 35/36, FAIL, exit 1.

## Mutation (b): mark one modified path as reverified-commit

Line 37, field 2 `left-named` → `reverified-commit`, reason left as-is:

```
> .ufo/waves/round-40/w1/swarm-registry.json	reverified-commit	-	left-named; not hunk-verified; …
```

Stdout:

```
CONSISTENT=38/39
REVERIFIED=36/36
LEFT_NAMED=2/3
C2=FAIL
EXIT=1
```

**Caught.** The MODIFIED loop requires `cls == 'left-named'` (c2-count.py:110); the reclassified
row drops LEFT_NAMED to 2/3, FAIL, exit 1.

## Controls and bonus probes

- Baseline copy (unmutated): `CONSISTENT=39/39 / REVERIFIED=36/36 / LEFT_NAMED=3/3 / C2=PASS`,
  `EXIT=0` — the `--table` flag works and the landed table passes as copied.
- Bonus (c): zero the digest on line 1 — `CONSISTENT=38/39 / REVERIFIED=35/36 / LEFT_NAMED=3/3 /
  C2=FAIL`, `EXIT=1`. The sha256 arm kills digest-only tamper; mutations (a)/(b) do not exercise
  that arm, so this closes the third predicate clause.

## Verdict

The kill rule holds against both ordered mutations. Each single-field corruption moves exactly
one counter and fails the gate; no mutation produces a false PASS.

## Residual blind spots (what this test cannot falsify)

1. **Table↔filesystem, not table↔ground truth.** The counter proves the files match the recorded
   digests, not that the recorded digests are correct. A table written with wrong digests on day
   one still PASSes. Content drift is caught only on one side: editing a report breaks the digest,
   editing the table breaks the hash — but a *coordinated* two-file edit (report + its digest row)
   passes. Sha256 pins bytes, not provenance.
2. **Counts cover only the frozen UNTRACKED/MODIFIED lists.** Extra rows in the table are ignored
   (a 40th row moves no counter); `rows` is keyed by path, so duplicate rows silently last-win.
3. **FAIL is not diagnostic.** A deleted row and a drifted row produce the identical
   signature (count −1), so the counter cannot distinguish tamper modes, only detect them.
4. **Reason text is weakly validated.** For reverified rows only non-emptiness is enforced —
   a reason of `x` passes. Only the left-named arm checks a semantic substring
   (`not hunk-verified`). Mutation (b) was caught by class mismatch, not by reason semantics.
5. **Stem/round-token checks are mention-anywhere checks** — survivable in principle, but the
   digest clause backstops them: any content edit that removes the mention also breaks the hash.

Scope: all mutations lived under `/tmp/w3-c2-mut/`; no lane file, index, or repo state modified;
counter runs read lane report files read-only via the default `--root`.
