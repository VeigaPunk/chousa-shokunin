# R51W2MutSupplement-2 — mutation-test of `c1-supplement.py` (round 51 wave 2, falsify)

Attacked claim: each of the supplement's six legs (SHAPE, MUTATION, CROSS_ENTRY, SOURCE_LINE,
UNKNOWN_SRC, CLASH) plus its env scrub and random work-dir names is load-bearing. One minimal mutant
per leg, each run against the real tool `tools/assimilate-rows.py` (sha256 `6b975f91…`), and the
controls `controls/forge-dirname.py` and `controls/tool-candidate1.py`. Fixed seed 51101, 3 rounds/run.

Path note: my charter trailer names `R51W2MutSupplement.md`; sibling seat R51W2MutSupplement had
already delivered that file (peer message, confirmed). Honoring "never write another seat's report",
this replication lands at `R51W2MutSupplement-2.md`. Its mutants are defined independently below.
No tools installed (tooling authorization read; pacman transactions untouched).

## Setup

Scratch `/dev/shm/chousa-r51-R51W2MutSupplement-2/` (deleted at end). Lane files copied, never
symlinked; the supplement imports `c1-count.py` from its own directory, so depth was preserved:

    S=/dev/shm/chousa-r51-R51W2MutSupplement-2; mkdir -p $S/corpus/evidence/round51 $S/corpus/evidence/round50
    cp <lane>/corpus/evidence/round51/c1-count.py $S/corpus/evidence/round51/
    cp -a <lane>/corpus/evidence/round50/c1-fixtures $S/corpus/evidence/round50/
    cp <lane>/corpus/evidence/round51/c1-supplement.py $S/corpus/evidence/round51/supp-pristine.py

Copies byte-identical (sha256): c1-count `94ddc7dc273c…`, supplement `163e9bdbdf22…`. The frozen
pin check (c1-count.py:79-81 exits 2 on pin mismatch) passing inside SHAPE proves the fixture copy
kept digest `c5c56480…`. Mutants generated from the pristine copy by exact `str.replace` with a
`count(old)==1` assertion per site; all 9 files `py_compile`-clean. Run template (31 runs total,
`env -u ASSIMILATE_CITES` throughout except the two deliberate polluted runs):

    env -u ASSIMILATE_CITES python3 $S/corpus/evidence/round51/<prog>.py --tool <tool> --seed 51101

## Mutants (one per leg; sites are lane-file lines opened for this report)

| id | edit (c1-supplement.py:line, old → new) |
|----|------------------------------------------|
| M1 | :117 `res["SHAPE"] = rc_c1.returncode == 0 and "LEGS=5/5" in rc_c1.stdout` → `res["SHAPE"] = True` |
| M2 | :122 `done = edit(m / "staged.md", "2026-12-01 — re-verify…", …)` → `done = False` (harness edits nothing) |
| M3 | :135 `bo == [["corpus/knowledge/b.md", A]]` → `bo == [["corpus/knowledge/a.md", A]]` |
| M4 | :140 `— s (supersedes {B})\n` → `— s\n` in the tail fixture (tail-id case dropped) |
| M5 | :152 `res["UNKNOWN_SRC"] = rc == 1 and` → `rc in (0, 1) and` (accepts rc 0) |
| M6 | :159 `res["CLASH"] = rc == 0 and tsv(…bodyclash.tsv) == [[…]] and "WARN" in err` → `res["CLASH"] = rc == 0` |
| M7 | :46 `ENV = {k: v … if k != "ASSIMILATE_CITES"}` → `ENV = dict(os.environ)` |
| M8 | :58,:120 `prefix=f"w{random.getrandbits(40):010x}-"`/`f"m{…}"` → `prefix="w-"`/`"m-"` (mkdtemp still appends its 8-char uniqueness suffix) |

## Baselines (pristine, observed)

    === supp-pristine|real rc=0    SHAPE=PASS 3/3 …all six PASS… SUPPLEMENT_LEGS=6/6 C1_SUPPLEMENT=PASS
    === supp-pristine|forge rc=1   SHAPE=PASS 3/3, other five FAIL 0/3, SUPPLEMENT_LEGS=1/6 FAIL
    === supp-pristine|cand1 rc=1   SHAPE/MUTATION/CLASH=PASS 3/3, CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC=FAIL 0/3, 3/6 FAIL
    === supp-pristine|real|ASSIMILATE_CITES=all rc=0   6/6 PASS   (scrub absorbs ambient var)

Matches the recorded `controls/c1-supplement-controls.txt` (read at start). Grounding for M7: the
tool reads the ambient var when no `--cites` flag — tools/assimilate-rows.py:331,336
`cites = a.cites or os.environ.get("ASSIMILATE_CITES") or "source"`.

## Kill matrix (observed; cells = SUPPLEMENT_LEGS and every leg-line that differs from the pristine row for that tool)

| mutant | vs real tool | vs forge-dirname | vs tool-candidate1 | verdict |
|--------|--------------|------------------|--------------------|---------|
| M1 | PASS 6/6 (SHAPE not even run) | 1/6, same legs | 3/6, same legs | SURVIVED |
| M2 | **FAIL 5/6, MUTATION=FAIL 0/3** | 1/6, same | 2/6, MUTATION PASS→**FAIL** | **KILLED** |
| M3 | **FAIL 5/6, CROSS_ENTRY=FAIL 0/3** | 1/6, same | 3/6, same | **KILLED** |
| M4 | PASS 6/6 | 1/6, same | 3/6, SOURCE_LINE still FAIL | SURVIVED |
| M5 | PASS 6/6 | 1/6, same | 3/6, same | SURVIVED |
| M6 | PASS 6/6 | 1/6, CLASH=FAIL 0/3 still | 3/6, same | SURVIVED |
| M7 | PASS 6/6 clean; with `ASSIMILATE_CITES=all`: **FAIL 1/6** (SHAPE=FAIL 0/3, CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC/CLASH=FAIL) | 1/6 | 3/6 | **KILLED** (polluted env only) |
| M8 | PASS 6/6 | 1/6, same | 3/6, same | SURVIVED |

Key raw rows:

    === M2-mutation-edits-nothing|real rc=1    … MUTATION=FAIL 0/3 … SUPPLEMENT_LEGS=5/6 C1_SUPPLEMENT=FAIL
    === M3-cross-entry-wrong-entry|real rc=1   … CROSS_ENTRY=FAIL 0/3 … SUPPLEMENT_LEGS=5/6 C1_SUPPLEMENT=FAIL
    === M7-env-not-scrubbed|real|ASSIMILATE_CITES=all rc=1   SHAPE=FAIL 0/3 … 4 more FAIL … 1/6 FAIL

## Mechanism probe (why M6/M8 cannot flip forge-dirname)

Direct probe, supplement-`adopt()` layout (registry+staged in `out.parent`, one entry, random-named
work dir `w0123456789`), running the lane control file: `forge rc: 1`, `forge stderr tail:
StopIteration`, `Held row in registry: False`, `wrote append.md: False`. forge-dirname.py dies at
`held_n = next(… if "Held" in l)` before scene dispatch because supplement registries carry only
status `mined` rows — it never reaches its exit-0 fallthrough on any supplement package, whatever
the work-dir name. (My pre-run prediction of an M6 leg-flip on forge was wrong; the run falsified it.)

## Findings

- Killed: M2, M3 (fail the good tool — MUTATION and CROSS_ENTRY assertions are not tautologies) and
  M7 under ambient `ASSIMILATE_CITES` (the :46 scrub is the only defense; pristine+polluted passes).
- Survivors (coverage findings, NOT contract changes; none flips an overall control verdict):
  M1 — no current control depends on SHAPE (both pass the frozen counter; forge-dirname passes 5/5
  via canned scene names keyed to the frozen counter's fixed dirs); under M1 the leg prints PASS
  without running it. M4 — the tail-id sub-case is unprobed: removing it leaves every outcome
  unchanged (cand1 fails SOURCE_LINE for non-tail reasons). M5 — `rc==1` vs `rc in (0,1)`
  indistinguishable on all three tools; an exit-0-with-REFUSED tool would slip UNKNOWN_SRC and no
  control models one. M6 — bodyclash/WARN assertions never discriminate (forge writes nothing;
  cand1 passes CLASH genuinely). M8 — fixed `w-`/`m-` prefixes indistinguishable from random names;
  the anti-recognition defense is not what rejects either control.
- Holds: pristine passes the real tool 6/6, refuses both controls (1/6, 3/6), absorbs ambient
  pollution; cand1 is caught exactly by CROSS_ENTRY+SOURCE_LINE+UNKNOWN_SRC (M2 shows MUTATION is
  the leg that accepts its honest selftest behavior).

## Restoration evidence

    sha256sum <lane>/corpus/evidence/round51/c1-supplement.py <lane>/corpus/evidence/round51/c1-count.py <lane>/tools/assimilate-rows.py
    163e9bdbdf225330cc2af2661790b698fc28fc0b7f6ac416bfbe5e7b77cbe498 …
    94ddc7dc273c831407f49cdf175301fbf8b272ece2c9998de58dddc3b2a25284 …
    6b975f91c809485c8d03e6134e2a17bdb7f9079c22218d74e9321a14632572f6 …

Identical to the pre-run hashes taken before any mutant ran. Scratch
`/dev/shm/chousa-r51-R51W2MutSupplement-2/` deleted (`ls: cannot access … No such file or directory`).

VERDICT: attacked the c1-supplement legs with 8 mutants — MUTATION, CROSS_ENTRY and the env scrub
are load-bearing (killed); SHAPE, the tail-id case, UNKNOWN_SRC's rc clause, CLASH's output clause
and the random dirnames survive as coverage gaps; the supplement itself holds (real tool 6/6, both
controls refused, pollution absorbed).
