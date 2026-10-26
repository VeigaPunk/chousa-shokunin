# R51W2MutSupplement — mutation test of `c1-supplement.py` (round 51, wave 2)

Target: `corpus/evidence/round51/c1-supplement.py` (lane tip 4436e279). Method: copies only — the lane files
were never opened for write. Scratch root `/dev/shm/chousa-r51-R51W2MutSupplement/` holds a mirror
`mirror/corpus/evidence/round51/{c1-supplement,c1-count}.py` plus `mirror/corpus/evidence/round50/c1-fixtures/`,
because `c1-count.py` resolves `R50_FIX = parents[3]/corpus/evidence/round50/c1-fixtures` and pins its digest:
generator check printed `mirror R50 digest match: True` (pin `c5c5648…cd43`). Subjects: real tool
`tools/assimilate-rows.py`, controls `controls/forge-dirname.py`, `controls/tool-candidate1.py` (copied to
scratch). Every run: `env -u ASSIMILATE_CITES python3 <supplement> --tool <subject> --seed 511` (the supplement
runs 3 rounds per invocation). No tools installed (none needed).

## Baseline (pristine) — all observed
- Lane receipt `python3 corpus/evidence/round51/c1-supplement.py --seed 511`: all six legs `PASS 3/3`,
  `SUPPLEMENT_LEGS=6/6`, `C1_SUPPLEMENT=PASS`, rc 0, 3.2 s. Mirror-vs-real run: identical, rc 0.
- vs `forge-dirname.py`: `SHAPE=PASS 3/3`, other five legs `FAIL 0/3`, `SUPPLEMENT_LEGS=1/6`, rc 1 — confirms
  wave 1: forge passes the frozen counter, and only the supplement's own legs hold it.
- vs `tool-candidate1.py`: `SHAPE/MUTATION/CLASH=PASS 3/3`, `CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC=FAIL 0/3`,
  `SUPPLEMENT_LEGS=3/6`, rc 1. (Candidate1 cites ALL tokens on `source:` lines, substitutes globally, and has no
  unknown-`source:`-id refusal — `diff -u controls/tool-candidate1.py tools/assimilate-rows.py` shows the real
  tool reads the header id after `source:` above the first `####`, refuses unknown source ids, substitutes
  per-entry, and computes bodyonly per entry.)
- Why forge dies under supplement packages (probe on a supplement-shaped package: 20 `mined` registry rows, no
  `Held`, entries `a.md`/`b.md`): `forge rc: 1`, `forge stderr tail: StopIteration`,
  `Held row in registry: False`. Forge's `held_n = next(… if "Held" in l)` aborts BEFORE its scene dispatch.

## Mutants — one per leg, single asserted-unique replacement each (`diff -u` showed exactly 2 changed lines)
- M1 SHAPE-true: `res["SHAPE"] = rc_c1.returncode == 0 and "LEGS=5/5" in …` → `res["SHAPE"] = True`
- M2 MUTATION-edits-nothing: `done = edit(m/"staged.md", "2026-12-01 …", "2027-01-01 …")` → `done = False`
- M3 CROSS_ENTRY-wrong-entry: `bo == [["corpus/knowledge/b.md", A]]` → `bo in ([…b.md…], [["corpus/knowledge/a.md", A]])`
- M4 SOURCE_LINE-drops-tail-id-case: fixture `source: {A} — {ua} — s (supersedes {B})` → `source: {A} — {ua} — s`
- M5 UNKNOWN_SRC-accepts-rc-0: `rc == 1 and "REFUSED" in err and …` → `rc in (0, 1) and "REFUSED" in err and …`
- M6 CLASH-expects-nothing: `rc == 0 and tsv(bodyclash) == [[…a.md…, lane_clash]] and "WARN" in err` → `rc == 0`
- M7 env-not-scrubbed: `ENV = {k: v … if k != "ASSIMILATE_CITES"}` → `ENV = dict(os.environ)`
- M8 dirnames-fixed: mkdtemp prefix `f"w{random.getrandbits(40):010x}-"` → `"w-fixed-"`

## Matrix — overall verdict (mutated-leg line where it differs from pristine); all runs seed 511
| mutant | real tool | forge-dirname | tool-candidate1 |
|---|---|---|---|
| pristine | PASS 6/6 | FAIL 1/6 | FAIL 3/6 |
| M1 | PASS 6/6 (≡) | FAIL 1/6 (≡) | FAIL 3/6 (≡) |
| M2 | **FAIL 5/6** (MUTATION=FAIL 0/3) | FAIL 1/6 (≡) | **FAIL 2/6** (MUTATION=FAIL 0/3) |
| M3 | PASS 6/6 (≡) | FAIL 1/6 (CROSS_ENTRY still FAIL) | FAIL 3/6 (CROSS_ENTRY still FAIL) |
| M4 | PASS 6/6 (≡) | FAIL 1/6 (≡) | FAIL 3/6 (SOURCE_LINE still FAIL) |
| M5 | PASS 6/6 (≡) | FAIL 1/6 (≡) | FAIL 3/6 (UNKNOWN_SRC still FAIL) |
| M6 | PASS 6/6 (≡) | FAIL 1/6 (CLASH still FAIL — forge rc≠0) | FAIL 3/6 (CLASH=PASS, as pristine) |
| M7 clean env | PASS 6/6 (≡ pristine) | FAIL 1/6 (≡) | FAIL 3/6 (≡) |
| M7 ambient `ASSIMILATE_CITES=all` | **FAIL 1/6** (SHAPE/CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC/CLASH=FAIL) | FAIL 1/6 (≡ its clean result) | **FAIL 1/6** (SHAPE flips to FAIL) |
| M8 | PASS 6/6 (≡) | FAIL 1/6 (≡) | FAIL 3/6 (≡) |

Control: PRISTINE supplement under ambient `ASSIMILATE_CITES=all` vs real tool = `C1_SUPPLEMENT=PASS` rc 0 —
the scrub does its job; only M7 loses that protection.

## Findings — survivors vs killed (mutant "survives" a subject iff no leg/verdict differs from pristine there)
1. **No weakening lets a control through the overall gate.** Forge is caught 5 legs deep (MUTATION + the four
   adopt legs), candidate1 3 legs deep (CROSS_ENTRY, SOURCE_LINE, UNKNOWN_SRC). Every one-leg mutant is still
   FAIL on both controls: no survivor in the coverage-hole sense. What holds: the supplement's verdict is
   over-determined; single-leg blind spots are masked.
2. **Verdict-equivalent survivors** (no available subject exercises the weakened aspect): M1, M3, M4, M5, M6, M8.
   Leg-level reading:
   - M1: the SHAPE leg passes BOTH controls even pristine (forge passes the frozen counter by design;
     candidate1 is a real implementation) — against these controls SHAPE contributes no discrimination; its
     value is re-running the frozen counter under the scrub + safe seed (docstring's stated purpose).
   - M3: candidate1's bodyonly is empty for the cross-entry package, so any entry-specific expectation fails;
     entry-identity of the `bodyonly.tsv` row is untested by the available controls.
   - M4: with the tail case dropped, SOURCE_LINE still kills candidate1 via the body-`source:` line case
     (candidate1 cites `{C}` from the body) — tail and body cases are redundant with each other vs candidate1.
   - M5: with rc accepted, UNKNOWN_SRC still kills candidate1 via `REFUSED`-in-stderr and no-outputs checks —
     the rc half of the check is redundant vs candidate1.
   - M6: CLASH passes candidate1 pristine (it implements clash) and fails forge only via rc≠0 — the
     bodyclash/WARN expectations are load-bearing against neither control.
   - M8: fixed directory names change nothing — forge is defeated by package shape (no `Held` registry row →
     StopIteration before scene dispatch), not by the w-prefix randomness; the docstring over-attributes the
     defense to random names.
3. **M2 is vacuous, not informative**: with no edit performed the R50 package legitimately selftests PASS, so
   the leg rejects the GOOD tool (FAIL 5/6) — a dead detector; it does show the leg's `edit` step is
   load-bearing setup, and it incidentally drops candidate1 to 2/6 (MUTATION now fails it too).
4. **M7 is the one true kill, and it fires in the harmful direction**: under ambient `ASSIMILATE_CITES=all` the
   un-scrubbed supplement flips the GOOD tool to FAIL 1/6 (and flips SHAPE against candidate1 too) — the scrub
   prevents false verdicts in a dirty environment; in a clean environment M7 is indistinguishable from pristine.
5. Candidate1's three real defects are each caught by a distinct leg: global-citation reading (SOURCE_LINE),
   global bodyonly attribution (CROSS_ENTRY), missing unknown-source refusal (UNKNOWN_SRC) — the supplement is
   strictly stronger than the frozen counter against it (c1-count alone: `LEGS=5/5`, i.e. SHAPE=PASS).

## Restoration and cleanup
- `sha256sum` of all five lane files before and after the whole session: byte-identical (`diff before.sha
  after.sha` → `LANE-UNCHANGED`). c1-supplement `163e9bdb…`, c1-count `94ddc7dc…`, assimilate-rows
  `6b975f91…`, forge-dirname `96c31f4c…`, tool-candidate1 `bdaf80f4…`.
- All 8 mutant dirs carry a `c1-count.py` byte-identical to the lane's (single hash `94ddc7dc…` across mirror
  and mutants), so every leg ran against the frozen counter's own logic.
- Scratch root deleted (`rm -rf /dev/shm/chousa-r51-R51W2MutSupplement`) after this report was written.

VERDICT: attacked the C1 supplement with 8 single-leg mutants × 3 subjects — no mutant lets forge-dirname or
tool-candidate1 through (forge caught 5 legs deep, candidate1 3 deep); six mutants are verdict-equivalent
(redundant checks: SHAPE and CLASH-vs-candidate1 discriminate nothing here, rc/entry-identity/tail halves are
backed by sibling checks, dirname randomness is not the forge defense), M2 is vacuous, and only M7 (env scrub)
bites — in the false-FAIL direction under ambient ASSIMILATE_CITES; the supplement holds.
