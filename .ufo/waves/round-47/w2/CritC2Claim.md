ATTACKS: C2 calibration verdict, post-freeze counter loosening, `\|`→`/` rewrite meaning
VERDICT: holds (with one recordkeeping defect)

## Verdict

The C2 claim holds and the "improved narrowly" SCORECARD wording is honest, **with one
defect: the SCORECARD C2 row's after-state numbers (93/93, freeze counter 92/92) do not
match the lane's own `measure-after.txt` (94/94 final, 93/93 freeze) at the same tip
commit.** The claim's predicate itself (final counter prints MISMATCHES=0, ENTRY_POINTS ≥
FLOOR) is met — I reproduced 94/94, MISMATCHES=0, exit 0. The instrument did NOT loosen:
every post-freeze counter change is stricter than the freeze counter (or neutral), and the
`\|`→`/` row rewrite is meaning-preserving as rendered (GFM shows a literal pipe) — it is
a parser accommodation, disclosed in the lesson, and its 10 "mismatches" are correctly
excluded from the calibration movement. The verdict "improved narrowly" is the honest
denominator: 8 real registry mismatches + 1 malformed row closed; the other 17 of the
freeze 25 never measured calibration.

## Evidence — counter × tree matrix (run at 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d and scratch)

| counter | tree | ENTRY_POINTS | REGISTERED | UNREG | DANGLING | MISM | C2 | exit |
|---|---|---:|---:|---:|---:|---:|---|---|
| final sha 60134f25 | freeze 22a44b8b | 93 (84/+2/+7) | 72/93 | 21 | 0 | 21 | FAIL | 1 |
| freeze sha 36b3934e | freeze 22a44b8b | 92 (84/+1/+7) | 67/92 | 25 | 0 | 25 | FAIL | 1 |
| final | base 9a9f94db | 90 (81/+2/+7) | 72/90 | 18 | 0 | 18 | FAIL | 1 |
| freeze | base 9a9f94db | 89 (81/+1/+7) | 67/89 | 22 | 0 | 22 | FAIL | 1 |
| final | tip 1fc5ed19 | 94 (85/+2/+7) | 94/94 | 0 | 0 | 0 | PASS | 0 |
| freeze | tip 1fc5ed19 | 93 (85/+1/+7) | 93/93 | 0 | 0 | 0 | PASS | 0 |

All six match the committed receipts (`controls/c2-before.txt`: 25/21/22/18; `measure-after.txt`: 94/94 final, 93/93 freeze at tip). Control leg reproduced: r46 counter on base = `C2=PASS 81/81` exit 0; r47 counter on base = `C2=FAIL 18`, exit 1; emptied-QUALITY freeze = `ENTRY_POINTS=86` < FLOOR, C2=FAIL.

## Post-freeze counter changes: strict or neutral, none loosening

Freeze→tip `c2-count.py` diff: CELL_SPLIT (unescaped pipes; fixes 10 phantom mismatches of
row 114), EXIT_CODE (word `exit`+digit OR backticked code; kills the "no exit code
documented" cheap gate and accepts `` `0` clean · `1` failed `` — the frozen sentence says
"names an exit code", so a backticked code is the literal reading), `~~~`-fence + repeated
inline-comment stripping (kills forges c2/c3/d3), `./` normalization (F3), BARE
directory-relative resolution (real dependence miss), DANGLING reads every row (e3), r46
exec-on-exact-hashed-bytes (SentScopeAudit), FLOOR enforced. The only "loosening" is the
backtick-exit acceptance, which was a false-rejection fix (F2), and it is bounded: a row
whose verdict cell has no exit code still never registers. MutC2Forge's surviving forges
(b2 c2 c3 d3 e3 e4 g2) are killed by the final counter except e4 (root-level no-slash
path, named limit) and g2 (floor substitution, named limit); a (one row listing every path)
is the named row-truth limit.

## Was the `\|`→`/` rewrite meaning-preserving?

Yes as rendered, not as raw bytes. SKILL.md:114 freeze: `` `round26-measure.sh TREE [c1\|c2\|c3\|holds\|all]` `` → tip: `` `TREE [c1/c2/c3/holds/all]` ``. GFM renders `\|` as a literal pipe, so the reader sees `c1|c2|c3|holds|all` vs `c1/c2/c3/holds/all` — the same alternatives in the same order. The rewrite exists only so the **freeze** counter's naive `split("|")` stops splitting the cell; the final counter's CELL_SPLIT handles escaped pipes (its own 15-not-25 GFM count). This is the wave-1 `CritC2Framing` "legitimate but cosmetic" rewrite, explicitly disclosed in lesson round-47.md mistake 3 ("meaning-preserving; disclosed here"), and correctly counted as parser artifacts, not calibration movement. Deeper issue: the round24–27 row's verdict cell ("counts, never verdicts, but…") does NOT name exit codes, so its 10 instruments stay unregistered under BOTH counters — the claim's "1 row whose unescaped pipes lost its exit map" is the mechanism-witness row (SKILL.md:100), which was rewritten to spell out `exit 0/1/2`; the "counts, never verdicts" row remains a known unregistered set under the named limit (they are not verdict gates).

## Defect: SCORECARD after-numbers are stale against measure-after.txt

- `measure-after.txt` (recorded at tip 1fc5ed19): final counter `ENTRY_POINTS=94 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS`; freeze counter `ENTRY_POINTS=93 REGISTERED=93/93 ... C2=PASS`.
- `SCORECARD.md:2506` claims after `ENTRY_POINTS=93 REGISTERED=93/93 ... C2=PASS` and "the freeze counter `92/92 MISMATCHES=0` too" — the 93/93 matches the **freeze** counter's output, the 92/92 appears in no archive (freeze counter at tip prints 93/93; at freeze itself it prints 67/92 FAIL under the new parser). The row omits the named counting command's (final counter) 94/94 measurement. Direction of the skew is not a pass-inflation (the instrument passes either way; freeze counter at tip also passes) — it is a recordkeeping error in the verdict row and should be corrected to 94/94 (final) and 93/93 (freeze at tip).

## Calibration honesty

"improved narrowly" is right: of the freeze 25, only 8 were real self-assessment mismatches (7 never-rowed paths + 1 malformed row) and they are closed at tip (mask-gate.sh, receipt-binding.py, slen-probe.sh, prose-check.py, rerun-check.py, q33-check.py, round25-meta-oracle.py, mechanism-witness.py), plus 3 base-gate controls re-categorized into the round35–41 controls row (a reclassification, not a closure — their row now carries explicit exit-code prose) and 10 parser artifacts excluded. The claim's predicate, kill rule and controls all hold as frozen. Name the SCORECARD row fix as the only correction.
