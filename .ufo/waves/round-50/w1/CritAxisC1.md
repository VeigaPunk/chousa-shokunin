# CritAxisC1 — attacking R50-C1 as an operability axis move

seat `CritAxisC1` · round 50, wave 1 · candidate `ec52e632edbad7fe51a6573d29acad5a028a7158`
(`tools/assimilate-rows.py` sha256 `bff32c11d02bc1bdc28ed484d4895d86c7f3537d8a9496ad474c73d4531f5b81` = `git show
ec52e63:… | sha256sum`); counters/fixtures/controls frozen at `6a068f2`; no tool installed; scratch
`/dev/shm/chousa-r50-CritAxisC1/` deleted.

## 1. Reproduction and freeze integrity

```
$ python3 corpus/evidence/round50/c1-count.py
SELFTEST_DEFAULT=PASS / BASELINE=PASS rc=0 findings=26 / PERTURB P1..P6 applied=1 rc=1 -> PASS
PERTURB_PASS=6/6 / EXPECTED_BAD=PASS rc=2 / R49_REGRESSION=PASS rc=0 / LEGS=5/5 / C1=PASS  (rc=0)
```

Controls reproduce `controls/c1-before.txt` exactly: `tool-before` `BASELINE=FAIL rc=2 LEGS=2/5`, `echo-tool`
`BASELINE=PASS PERTURB_PASS=0/6 LEGS=4/5`, `const-tool` `BASELINE=FAIL rc=0 LEGS=2/5`, all `C1=FAIL`. `git diff --stat
6a068f2 ec52e63` touches only `tools/assimilate-rows.py`, `corpus/fixtures/assimilate-selftest/*` and two round-49
reports — `corpus/evidence/round50/` untouched — and `controls/tool-before.py` is byte-identical to `git show
6a068f2:tools/assimilate-rows.py` (`4b995dbc…`). Hand re-derivation of 8 of the 26 `expected.json` lines from the
addendum rules (collision set {S011,S012}; contiguous S013/S014/S015 with S012 held→S001; three `ROWUSEDBY`, three
`ROWRECHECK`, six `STRIPPED`) found no discrepancy.

## 2. Q1 — self-test: operability move or inert plumbing?

An operability move **by the axis definition and by precedent, and it moves no score.**

- Fleet `AXES.md:13`: operability = "Runnable artifacts … | A checklist item can be run and produces the stated
   outcome". Met: 26 findings, exit 0; six perturbations exit 1 with the named `DIFF`; unparseable expected exits 2 with
   `SELFTEST=ERROR`.
- Precedent already scores selftest growth as operability: `SCORECARD.md:46`, `:108`, `:152` ("operability | improved |
   selftest 20 → 30 / 30 → 40 … exit contract 0/1/2 held").
- But the score (3/10, `SCORECARD.md:7`) is pinned to another observable — `:11-13` "the number of the three named
   archived inputs that exit 1 and emit exactly one `RESEARCH_GATE: DRIFT` summary" — and that command never invokes
   `assimilate-rows.py`. Rerun now: `VERDICT_BEARING_EXPORTS=3/3`.

Lane-facing effect it does have: it closes the routed round-49 defect "no self-test for a reusable gate" and is the
only way to re-verify the adopter without the read-only package (§5) — plumbing (QUALITY 64 tag correct) **with** a
maintainability effect, not inert, not a score move. **Defect (calibration, textual):** the header `operability
(lowest scored axis, 3/10; capability extension)` invites a closure to read C1 as raising 3/10; the Gate must say the
score stays 3/10 and carry the delta on the `SCORECARD.md:2584` capability row.

## 3. Q2 — are C1 and C2 causally separable as `claims.md` says?

**Separable in outcome — yes. The frozen sentence's stated inputs — false.** C1 is immune to round-50 entry work:
`c1-count.py:85-93` runs the tool on the lane default tree, legs 2-4 use `c1-fixtures`, leg 5 (`:136-138`) shells the
round-49 counter; a scratch root holding only `tools/assimilate-rows.py` + `corpus/fixtures/assimilate-selftest/` (no
`corpus/knowledge`, no `corpus/SOURCES.md`) prints `LEGS=5/5 C1=PASS`. C2's counter never mentions the adopter (`grep
-c assimilate corpus/evidence/round50/c2-count.py` → `0`; it runs `inference-ground.py` / `quote-substance-check.py`).
Neither can flip the other.

But `claims.md` ("C1's counter … never reads the lane's entries or registry rows") is contradicted by leg 5:
`round49/c1-count.py:366` runs `git -C LANE archive BASE_REV corpus`, `:384` copies `corpus/SOURCES.md` out as the
base registry, `:392` runs the tool on the real package (`:49-51` `/home/vgpnk/Projects/shokuknow/merge/chousa`).
Observed every run: `BASE_REV=414a2ec6…`, `SET_A … CITED=9`, `SET_C … HELD=2/2`. A frozen claim whose text misstates
its own reads is a calibration defect even when the conclusion holds.

## 4. Q3 — can C1 pass with the adopter broken on a real package?

Yes for date insensitivity; no for scale/mapping/grep defects — leg 5 is a real real-package leg (three entry sets,
9/3/5 cited ids, census mirror), so "fixtures are small" is only partly true.

| mutant | R50 counter | R49 counter | real-package break |
|---|---|---|---|
| M1 column-zero-only collision grep (`^ {0,3}\|` → `^\|`) | `BASELINE=FAIL R49_REGRESSION=FAIL LEGS=3/5 C1=FAIL` | `GUARD … COLLISIONS=[] -> FAIL`, `C1=FAIL` | — caught |
| M3 cited-id cap `[:6]` (fixtures cite 4, SET_A cites 9) | `LEGS=4/5 C1=FAIL` | `SETS_PASS=2/3 C1=FAIL` | — caught |
| M4 `url_of` without the trailing-slash strip | `LEGS=5/5` **`C1=PASS`** | `SETS_PASS=3/3` **`C1=PASS`** | unpinned `renumber.tsv` `url` column only |
| M2 `--opened` hardcoded `"2026-10-25"` | `LEGS=5/5` **`C1=PASS`** | **`C1=PASS`** | wrong `opened` in every appended row |

M2 is decisive. Both counters pass `--opened 2026-10-25` — the selftest at `tools/assimilate-rows.py:157`, the
round-49 counter at `:53` and `:257` (`cells[8] == OPENED`) — so no leg varies the one value parameter. On the real
package (real entry, `--opened 2026-10-26`):

```
pristine      id= S104 opened= 2026-10-26 | S105 opened= 2026-10-26 | S106 opened= 2026-10-26
m2-hardopened id= S104 opened= 2026-10-25 | S105 opened= 2026-10-25 | S106 opened= 2026-10-25
```

A tool that stamps the fixture date into lane rows prints `C1=PASS` from both counters. M4 is the same class one
severity lower: `renumber.tsv`'s `url` column is never compared (`round49/c1-count.py:226` reads `r[0],r[1],r[2]`), so
its normalisation is unpinned and the mutant's `www.ncpssd.cn/` and `check.cnki.net/tmlc/` rows pass both counters.
Second bound, structural: `SELFTEST_DEFAULT` is not independent evidence — the lane default tree is byte-identical to
`c1-fixtures` (both digest `c5c56480…` = `PIN`) and is **not** pin-covered (`c1-count.py:79` digests `FIX` only);
dropping one finding from the scratch default tree gives `SELFTEST_DEFAULT=FAIL … LEGS=4/5 C1=FAIL` with no
`PIN_CHANGED`: leg 1 duplicates leg 2 and is the only leg a lane edit can flip without the guard firing — a
duplicate-authority seam, not a false pass.

## 5. Lane-facing fact found on the real package

One full-package run refuses: `--staged …/merge/chousa/SOURCES.append.md --knowledge …/merge/chousa/knowledge
--registry corpus/SOURCES.md --opened 2026-10-25 --out … --entry <all 55>` → `rc=1 REFUSED S194: staged row names no
http(s) URL`. 11 of 114 staged rows carry no http(s) URL and 8 of the 55 real entries cite one, so the adopter must be
driven per entry subset. Documented behaviour (docstring "Refusals"), but `SCORECARD.md:2584`'s capability row ("turns
staged campaign entries into census-valid lane rows") reads wider than the artifact does.

## 6. Impacted axes

- **calibration** (primary): frozen text misstates C1's reads (§3); the claim header implies a 3/10 move it cannot
   deliver (§2); two measured counter bounds (M2, M4) are undeclared, unlike C2's declared "known counter limit".
- **operability**: improved in the lane's verdict convention (AXES.md:13; precedent SCORECARD.md:46/108/152), score
   unchanged 3/10 (rerun 3/3); no harm — leg 5 still passes on the real package, so the +121-line selftest does not
   regress the CLI path.
- **depth, freshness, coverage, adjacency**: untouched by C1; nothing to reject.

## 7. Smallest safe corrections (none touches a frozen predicate, target, counter or control)

1. Round-50 Gate/lesson: operability score **unchanged 3/10**, credit C1 on the capability row, record the full-package
   refusal/subset requirement (§5).
2. Fix the two non-predicate sentences of `claims.md`: the separability clause → "C1's four fixture legs read no lane
   bytes; its fifth leg runs the round-49 counter, which reads the lane corpus at `BASE_REV` and the pinned package, so
   C1 is immune to round-50 lane edits but not lane-free"; the header parenthetical → "plumbing; score unchanged".
3. Declare beside C2's known limit: "no leg varies `--opened`, so a hardcoded date passes (M2)"; "`renumber.tsv`'s `url`
   column is unpinned (M4)"; round-51 candidate (not this round): a new counter with a second-`--opened` leg and a
   `url`-column leg — the frozen counter may not grow one.

VERDICT — attacked C1 as an axis move and falsified its own scope claims: the self-test is a real operability move by
`AXES.md:13`/precedent but moves no score (3/3 unchanged); C1 and C2 are separable in outcome while `claims.md`'s
"never reads lane bytes" is false (leg 5 archives the lane); the frozen counter passes a date-hardcoding adopter (M2)
and an unnormalised `url` column (M4) on the real package while catching the column-zero-only grep (M1) and a scale
cap (M3), so C1 is admissible as plumbing with those bounds declared, not as a 3/10 move.
