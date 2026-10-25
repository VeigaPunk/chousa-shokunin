# RevC2Before — C2 before-state re-derived on three trees (round 46, wave 2)

Item: re-derive `corpus/evidence/round46/controls/c2-before.txt` on (A) base + only
`round46/*count.py`, (B) base + the whole `round46/` dir, (C) base alone; report which tree the
file labels "tree A"/"tree B"; report any mislabel with corrected lines.

Verdict: **C2 is not falsified** — the declared before-state reproduces exactly on tree A and the
after-state on the archived landing. **One record defect**: the "bare base tree … (no round-46
counters) — the pre-existing debt" paragraph carries tree B's numbers and prints the three round46
counters it says the tree lacks; the real bare-tree debt (13 of 68) is absent.

## Trees (exact construction)

```
git archive 6e2630a6343948b3fe5bf299901207a0619ad949 | tar -x -C /tmp/chousa-r46w2-RevC2Before/{A,B,C}
cp corpus/evidence/round46/{c1,c2,c3}-count.py /tmp/chousa-r46w2-RevC2Before/A/corpus/evidence/round46/
cp -r corpus/evidence/round46/.                /tmp/chousa-r46w2-RevC2Before/B/corpus/evidence/round46/
```

C untouched; A was also re-run with `corpus/fixtures/inference-ground-r46` copied in (no change).
Counter on every run: `corpus/evidence/round46/c2-count.py`, sha256
`60ad448e99b15cb6691e48ce4e01c86ba8f027618f3e2fbb3649485ea39ca7ff` (same at c2f0e9d, d09fc8e,
3807537), run as `python3 ./A/corpus/evidence/round46/c2-count.py --root ./<tree> --list`.

## Re-derived results (decisive lines)

| tree | ENTRY_POINTS | GATES_ROWS | REGISTERED | UNREGISTERED | exit |
|---|---|---|---|---|---|
| A (base + 3 counters) | `ENTRY_POINTS=71 (tools=7 counters=50 named=66)` | 30 | `55/71` | `16` | 1 |
| B (base + whole round46 dir) | `ENTRY_POINTS=71 (tools=7 counters=50 named=69)` | 30 | `55/71` | `16` | 1 |
| C (bare base alone) | `ENTRY_POINTS=68 (tools=7 counters=47 named=66)` | 30 | `55/68` | `13` | 1 |

The freeze commit c2f0e9d measures `ENTRY_POINTS=71 (tools=7 counters=50 named=69)` / 30 / `55/71` /
`UNREGISTERED=16` / exit 1 — identical to B (provenance only). `named` 66 vs 69 is the fingerprint: the
only difference is `round46/claims.md`, which names the three round46 counters; C's 47 counters = 50
minus those three files. Fixtures move no leg, so the file's "… and fixtures" clause is inert.

## What the file labels

`corpus/evidence/round46/controls/c2-before.txt`, 50 lines, sha256
`923c9499b48ad6b71d2598b406a19aada3f32ca50a6ed9b427e6cfff38c85469`, byte 1272 = line 27;
unchanged at c2f0e9d, d09fc8e, 3807537.

- **line 2** `### tree A: git archive 6e2630a6 + this round's counters and fixtures …` — lines
  20–23 (`71 … named=66`, `55/71`, `16`) are **tree A**. Correct.
- **line 27** `### tree B: the bare base tree git archive 6e2630a6 (no round-46 counters) — the
  pre-existing debt` — lines 45–48 (`71 … named=69`, `55/71`, `16`) are **tree B / the freeze
  tree**. **Mislabel.**

## Defect 1 (medium) — "tree B" is tree B's measurement under a bare-tree label

- line 45 `named=69` / `ENTRY_POINTS=71`: the bare tree has 68 points and 47 counters; 69 named is
  reachable only with `round46/claims.md` present.
- lines 42–44 print `UNREGISTERED_PATH corpus/evidence/round46/{c1,c2,c3}-count.py` — files the
  label says are absent. `REGISTERED=55/71` vs bare `55/68`: same numerator, three extra
  unregistered entries.
- The freeze tree c2f0e9d measures identically, so the block is the lane checkout at freeze, or base + round46 dir — not a `git archive 6e2630a6`.

Impact: the record's only "pre-existing debt" figure overstates numerator and denominator by 3
each; the honest baseline (13 of 68) is nowhere. C2's kill rule (`UNREGISTERED>0` or
`ENTRY_POINTS<71`) and its target (`≥71`) do not read this block, so the claim survives and the
control record does not.

Corrected lines — relabel 27, delete 42–44, fix 45–48, append the tree-C block:

```
### tree B: git archive 6e2630a6 + corpus/evidence/round46/ (counters, claims, spans, controls) — the freeze-tree shape; NOT the bare base
$ python3 corpus/evidence/round46/c2-count.py --root <tree B> --list
<the 13 paths at lines 29-41, unchanged>
UNREGISTERED_PATH corpus/evidence/round46/c1-count.py
UNREGISTERED_PATH corpus/evidence/round46/c2-count.py
UNREGISTERED_PATH corpus/evidence/round46/c3-count.py
ENTRY_POINTS=71 (tools=7 counters=50 named=69)
GATES_ROWS=30
REGISTERED=55/71
UNREGISTERED=16
C2=FAIL
exit=1

### tree C: the bare base tree git archive 6e2630a6 alone (no round-46 files) — the pre-existing debt
$ python3 <any copy of> corpus/evidence/round46/c2-count.py --root <tree C> --list
<lines 29-41 verbatim and in that order — round24-measure.sh, round25-ledger-recount.py,
round25-measure.sh, round25-meta-differential.sh, round26-date-differential.sh,
round26-measure.sh, round26-registry-differential.sh, round27-falsify-controls.py,
round27-mechanisms.py, round27-regressions.py, round33/d2-census.py,
round33/no-name-signals.sh, round34/self-audit.py>
ENTRY_POINTS=68 (tools=7 counters=47 named=66)
GATES_ROWS=30
REGISTERED=55/68
UNREGISTERED=13
C2=FAIL
exit=1
```

## Defect 2 (low) — the bare-tree block's command is not executable on its own tree

Line 28 `$ python3 corpus/evidence/round46/c2-count.py --root <tree B>`: on a tree with no
`corpus/evidence/round46/` that path does not exist (`ls <C>/corpus/evidence/round46` → `No such file
or directory`). Corroborates Defect 1; the corrected block names the invocation honestly.

## Defect 3 (low) — the "frozen-before tree" parenthetical on line 2

The stated construction (base + this round's counters + fixtures) does produce `named=66`, and I reproduce
it exactly, so the numbers are right for it; the parenthetical is not (the freeze commit c2f0e9d contains
`claims.md` and measures `named=69`). Suggested: `(base tree + this round's counters; the fixtures move no leg)`.

## After-state reproducibility (both PASS)

```
$ git archive d09fc8e | tar -x -C /tmp/.../L && cd /tmp/.../L && python3 corpus/evidence/round46/c2-count.py --list
ENTRY_POINTS=72 (tools=8 counters=50 named=70) / GATES_ROWS=35 / REGISTERED=72/72 / UNREGISTERED=0 / C2=PASS
$ git archive 3807537 | tar -x -C /tmp/.../W && cd /tmp/.../W && python3 corpus/evidence/round46/c2-count.py --list
ENTRY_POINTS=73 (tools=8 counters=50 named=71) / GATES_ROWS=35 / REGISTERED=73/73 / UNREGISTERED=0 / C2=PASS
```

The 72 → 73 delta is exactly one path, `corpus/evidence/round46/build-spans.py`, named in `SCORECARD.md`
at 3807537 and absent from the d09fc8e blob (`git show d09fc8e:SCORECARD.md | grep -c round46/build-spans`
→ `0`). The ticket's frozen `72` is the d09fc8e state; `measure-after.txt`'s `73` is the 3807537 state (the
lane advanced mid-run). Both satisfy `ENTRY_POINTS ≥ 71` and `UNREGISTERED=0`; no leg of C2 is harmed.

## Non-findings, residual risk

- `claims.md`'s quoted before line matches tree A exactly; the header's counter digest matches the
  committed bytes; c2f0e9d → d09fc8e changed only `gates_rows()` and `names()`, never
  `entry_points()`, so before/after differ by registry rows, not by measurement logic.
- Not tested here (other seats own them): `controls/c2-controls.txt`, `--skill` redirection, and
  row-verdict truth (C2's own named limit). The NAMED leg reads `SCORECARD.md`/`claims*.md` from the
  working tree, so the count drifts with uncommitted scribe edits.
- No installs, no tool changes, pacman untouched, no network. Scratch `/tmp/chousa-r46w2-RevC2Before/` removed.
