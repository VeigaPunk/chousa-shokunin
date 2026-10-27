# R56ConnPattern — cross-round C1 counter forgeability pattern (RW-1) and synthesis

Seat: R56ConnPattern · round 56 · wave W1 · 2026-10-27
Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin · BASE e5a3795191601797613eb986b36fa0b1a73fe6a1 · freeze 41c58925580af6be22049f13cfde234c5475b858
Report target: .ufo/waves/round-56/w1/R56ConnPattern.md · scratch /fast/scratch/hyaku/chousa-r56/R56ConnPattern (cleared at exit)

## 1. Cross-round RW-1 mechanism classes (rounds 49–55) vs round-55 W1 seats

Evidence in `corpus/evidence/round53/recurring.tsv:1`, spot-checks `corpus/lessons/round-{49..55}-verifier-spotcheck.md`, and round-55 W1 seats:
1. Replay / fixed-input forge (r48-r49, `CritForgeC1`): golden output replay on unchanging fixtures.
2. Literal token / DIFF echo (r50, `R50CritForgeC1`): counter searched for 6 literal regexes; 42-line forge passed 5/5.
3. Directory name & env scraping (r51, `R51CritForgeC1`): deterministic names (`s`, `d1`, `d2`) and `ASSIMILATE_CITES` leaked leg identity.
4. Representation variance (r52, `R52CritForgeC1`): generator syntactic monotony (rigid XML) permitted naive regex parsing.
5. Sibling file leakage & ctypes (r54, `R54CritForgeC1`, `R54W2CritC1Verdict`): HTML left beside `.doc`; ctypes bypassed hook.
6. Untested / redundant clauses (r55, `R55MutC1Counter.md:37-50`): all 9 mutants SURVIVED; slice vs char checks were mutually redundant; M3–M8 were unexercised by shipped controls; M9 (WIN_NL) broke candidate itself on `quotes.tsv` format.
7. Audit hook confinement loopholes (r55, `R55CritForgeHook.md:18-24`): `_posixsubprocess.fork_exec` spawned without `Popen`; `os.chdir` broke relative path realpath; `dir_fd`-relative `os.open` bypassed `allowed()`; symlink/kill/openpty unmonitored.
8. Non-reading surrogates (r55, `R55CritForgeEcho.md:58-75`): surrogate failed due to harness script bug; `GENOLE` protected by deleting generator tree (`shutil.rmtree(g)`), but `OLEPIN` remained bound to static captures.

## 2. Round-56 driver design: closed vs open mechanism classes

Driver: `corpus/evidence/round56/c1-count.py` (freeze `41c58925`, 290 lines); gate `c1-gate.py`; battery `battery/*.py` (`46e1758f`).
- **Clause-reason kills (lines 199-232, `MARKER` 86-96):** CLOSED the untested/redundant clause class. Single-tool controls cannot pass: each mutant M1–M8 requires a battery violator failing in G with that clause's exact failure regex, and passing in the mutant.
- **Triplicate random order at two seeds (lines 209-232):** CLOSED stateful/alternating forges. `secrets.token_hex(8)` hides G vs mutant in paths; 3 G and 3 mutant runs shuffled randomly at seeds 7 and 56 reduce call-counter/alternating forge odds to <= (1/20)^2 = 1/400.
- **Frozen mutant set M1–M9:** Closes the 9 specific round-55 weaknesses, but LEAVES OPEN two major structural classes:
  1. *Retrospective mutant horizon:* M1–M9 are frozen from round 55. New gate logic in `c1-gate.py` has zero mutants (dropping `_posixsubprocess.fork_exec` or `os.chdir` from `BAD`, or mutating `allowed()` / `PATHS` / `R55_ALLOW` leaves `KILLED=9/9` intact).
  2. *Incomplete audit hook & descriptor bypass:* `c1-gate.py:93-95` patched only two strings in `BAD`. Crucially:
     - `c1-gate.py:101`: `if isinstance(p, int): return True` allows raw file descriptor operations unmonitored.
     - `allowed(p)` resolves `os.path.realpath(p)` against `cwd`, ignoring `dir_fd`. In `p2-dirfd.py:17`, the probe was stopped by `os.chdir(sub)`, NOT by `dir_fd`. A relative path evaluated relative to an allowed dir_fd (e.g. `TOOLS`) without `os.chdir` bypasses `allowed()`.
     - In-process cooperative auditing (`sys.addaudithook`) lacks kernel isolation (no namespaces/seccomp).

## 3. Drafted RW-1 row update in `recurring.tsv`

Observed command on lane repo:
`$ python3 corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round53/recurring.tsv`
Observed output:
`FAIL RW-1 streak=0 claimed=5 first_in_run=- routed=corpus/evidence/round53/c1-supplement.py frozen counter forgeable`
`FAIL RW-3 streak=0 claimed=2 first_in_run=- routed=- stray write outside scratch`
`WEAKNESS_ROWS=2 FAILING=2`

Streak analysis: `txt[n]` matches `forg(e|ed|able|ery)` across rounds 49..55 (7 rounds: 49, 50, 51, 52, 53, 54, 55). At freeze, `round-56.md:5-7` has an empty Mistakes block, so scanning backwards from newest round 56 yields `s = 0`. Claimed streak in round 53 was 5.
Draft update to `corpus/evidence/round53/recurring.tsv` (shape: `id<TAB>label<TAB>regex<TAB>routed<TAB>streak`):

```tsv
RW-1	frozen counter forgeable	forg(e|ed|able|ery)	corpus/evidence/round56/c1-count.py	7
```

If the round-56 lesson records the gate's unclosed hook/mutant gaps, the streak advances to `8`; if the driver's triplicate random order is accepted as closing C1 counter forgeability, streak resets to `0` with routed path `corpus/evidence/round56/c1-count.py`.

## 4. Non-obvious move: unify confinement into the mutation matrix

- **Affected axes:** operability (C1 gate robustness), calibration (eliminating false confidence in incomplete blacklists).
- **Proposed move:**
  1. *Substrate (descriptor-aware hook):* Replace `isinstance(p, int): return True` and cwd-relative `realpath` in `c1-gate.py:allowed()` with `/proc/self/fd/`-aware inspection that resolves `dir_fd` targets and validates open descriptors.
  2. *Contract & driver (unify probes as mutants):* Retire ad-hoc probe scripts P1/P2. Promote hook events into the driver's `MUTANTS` (e.g. M10 dropping `_posixsubprocess.fork_exec` from `BAD`, M11 dropping `os.chdir`, M12 dropping `dir_fd` validation). Require battery violators to kill M10–M12 under the same triplicate random-order standard.
- **Risks & trade-offs:** Higher battery count (11+ tools) increases driver runtime from ~132s to ~175s; requires `/proc` mount.
- **Verification:** Mutating `BAD` in scratch reproduces `MUTANT M10 SURVIVED` until a violator exercises it; descriptor bypasses fail gate.

VERDICT: evaluated R56 C1 driver against RW-1 mechanism classes — clause-reason kills and triplicate random order close untested clauses and stateful forges, while retrospective mutant horizon and audit-hook descriptor blindspots survive open.
