# MutC1V2Profile — round 62 w1 — mutation test of c1v2-count.py (neutral profile)

Scope: neutral-profile code of the frozen v2 counter (`Fx.__init__` names/cwd, `new_url`, `_env_and_limits`,
the pipe / closed-stdin branch of `run`). Frozen files were read, not edited. Scratch is deleted.

## Method

- 14 NEW single-edit mutants, N01–N14 (X01–X12 not repeated). Each edit is an exact-once string replacement in
  a copy of `c1v2-count.py`, laid out as `run-c1v2-controls.py` lays out its mutants: `<scratch>/mut/<name>/`
  holds `corpus/evidence/round62/c1v2-count.py` and `tools/capture-text.py` (copied from the lane). The driver
  asserts each pattern occurs exactly once before writing.
- Each mutant ran once through the frozen battery:
  `python3 -B corpus/evidence/round62/c1v2-battery.py --counter <mutant> --work <scratch>/b/<name>`
  (default `--landed` = frozen `tools/build-spans.py`, the full 23-subject battery, no `--only`).
- Intact control N00 through the same layout: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4
  BATTERY=PASS`, exit 0. Harness matches the frozen control file.
- Gap check (survivors only): for each survivor I wrote a candidate forger or honest builder with the battery's own
  `TEMPLATE`/`SNIFFS` machinery (or a plain landed-with-one-line builder) and ran the counter on it directly,
  once against the intact counter and once against the mutant. Output lines are the counter's last line.
- Two probes (F02b, PB, PS) use scratch copies with `TIMEOUT = 60` changed to `TIMEOUT = 5` (both the intact
  control and the mutant get the same change), so a hang costs 5 s instead of 60 s. Disclosed deviation; the hang
  mechanism is unchanged.

## Results

| ID | Edit (neutral profile) | Battery | Forgers accepted by battery | Named killer, intact -> mutant | Class |
|---|---|---|---|---|---|
| N01 | neutral cwd = fixture dir (drop the empty outside cwd and its mkdir) | exit 0, SURVIVED | - | G13 cwd holds the builder's dir: `exit 1 LEGS=11/20` -> `exit 0 LEGS=20/20` | gap (forger) |
| N02 | `range(secrets.choice(range(4, 10)))` -> `range(0)` (no random extra env keys) | exit 0, SURVIVED | - | F02b env keys within {PATH,HOME,LANG,LC_ALL,LC_CTYPE}: `exit 1 LEGS=10/20` -> `exit 0 LEGS=20/20` | gap (forger) |
| N03 | PATH shuffle removed (`shuffle(parts)` -> `pass`) | exit 0, SURVIVED | - | G14 PATH first entry == host first entry: `1 12/20` -> `0 20/20` | gap (forger) |
| N04 | LANG fixed to `C.UTF-8` | exit 0, SURVIVED | - | G15 LANG == C.UTF-8: `1 13/20` -> `0 20/20` | gap (forger) |
| N05 | AS jitter removed (`AS_LIMIT + (choice(range(0,25)) << 20)` -> `AS_LIMIT`) | exit 0, SURVIVED | - | G16 RLIMIT_AS == 200 MiB: `1 12/20` -> `0 20/20` | gap (forger) |
| N06 | fsize choice without 1 GiB (`[384,768,1024] MiB` -> `[384,768] MiB`) | exit 0, SURVIVED | - | G17 RLIMIT_FSIZE != 1 GiB: `1 17/20` -> `0 20/20` | gap (forger) |
| N07 | neutral host `.{rw}.test/` -> `.example.invalid/` | exit 1, KILLED | F05 | - | battery kill |
| N08 | neutral stdout = regular file, stderr still pipe | exit 1, KILLED | F11 | - | battery kill |
| N09 | neutral stderr = regular file, stdout still pipe | exit 0, SURVIVED | - | G18 `S_ISREG(fstat(2))`: `1 11/20` -> `0 20/20` | gap (forger) |
| N10 | neutral pipes not drained (drop the `t.start()` and `t.join()` loops) | exit 0, SURVIVED | - | honest PB (landed + 200 KB stdout), TIMEOUT 5: intact `0 20/20`, N10 `1 5/20` | gap (false positive) |
| N11 | neutral builder name fixed `build-spans.py` | exit 0, SURVIVED | - | G19 basename(__file__) == build-spans.py: `1 11/20` -> `0 20/20` | gap (forger) |
| N12 | neutral quotes name fixed `q.tsv` | exit 0, SURVIVED | - | G20 basename(--quotes) == q.tsv: `1 10/20` -> `0 20/20` | gap (forger) |
| N13 | neutral cache name fixed `cache` | exit 0, SURVIVED | - | G21 basename(--cache) == cache: `1 11/20` -> `0 20/20` | gap (forger) |
| N14 | neutral stdin write end left open (drop `os.close(wfd)`) | exit 0, SURVIVED | - | honest PS (landed + `sys.stdin.read()`), TIMEOUT 5: intact `0 20/20`, N14 `1 5/20` | gap (false positive) |

Battery verdict lines (exact): N07 and N08 print `FORGERS_REJECTED=11/12 BATTERY=FAIL`; all others print
`FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`. No stub or positive changed in any mutant.

## Findings

1. **The battery kills 2 of 14 mutants.** N07 (F05) and N08 (F11) are the only ones that let a battery forger
   through. Every other neutral-profile variation can be removed with BATTERY=PASS.

2. **All 12 survivors are real control gaps, none is equivalent in practice.** For each survivor I ran a named
   builder against the intact counter and against the mutant (table, last column). Ten are forgers the intact
   counter rejects and the mutant accepts (N01–N06, N09, N11–N13, plus N02 via F02b). Two are honest builders the
   mutant rejects (N10, N14): a false-positive direction the battery has no positive for. The battery's 12
   forgers sniff only nine of the neutral dimensions, so a variation no battery forger sniffs is invisible to
   BATTERY=PASS.

3. **N02's F02 kill is incidental (calibration).** Removing the random extra env keys leaves F02 rejected in the
   battery. Reason, from an instrumented F02 forger run under N02 with `--keep`: Python adds `LC_CTYPE` to the
   child's `os.environ` in some neutral draws (observed key lists: `['HOME','LANG','PATH']` and
   `['HOME','LANG','LC_CTYPE','PATH']` misses; at least one of the 19 neutral runs in that dump (only six
   were printed). [INFERENCE] the `LC_CTYPE` draws come from LANG=C/POSIX, under Python's C-locale coercion; the
   LANG value was not printed. So F02's battery kill under N02 depends on Python's locale behavior, not on the
   random keys that the mutant removed. F02b exposes that gap: the intact counter rejects it and N02 accepts it.
   The `LC_CTYPE` draw is observed; the LANG mapping is not.

4. **Routing.** These are counter limits for the next round's battery, not refutations of R62-C1. R62-C1's frozen
   count (BATTERY=PASS on the intact counter) is reproduced; nothing here changes C1's verdict. Candidate battery
   additions, each checked above: a forger for each of N01, N02 (F02b), N03, N04, N05, N06, N09, N11, N12, N13
   and two positives (PB: >64 KiB stdout; PS: reads stdin). Frozen files were not touched.

## Limits of this run

- One battery run per mutant. The counter draws seeds and salts at random, so a borderline result could differ on
  a rerun. The N07/N08 kills and the G-forger results are deterministic in their edits, except F02b and the
  N02 F02 miss, which depend on LANG draws.
- PB and PS ran with TIMEOUT 5 (scratch copies) to keep the run short. The frozen TIMEOUT 60 would make the same
  hang take 60 s per run. Not run at 60 s.
- Entailment of forgers is not claimed beyond the code path each one exercises. No external fetch, no installs,
  no pacman, no git or index mutation. Lane writes: this report only.

Commands run (from the lane root, scratch under /fast/scratch/hyaku/chousa-r62/MutC1V2Profile, now deleted):
`python3 -B mut.py` (15 battery runs at 4 jobs, 690 s wall, output: `N00 ... BATTERY=PASS`, `N07 ... exit 1`,
`N08 ... exit 1`, others `exit 0`); `python3 -B p2.py` (F02b, PB, PS; output above in the probes).

VERDICT: KILLED=2/14 survivors_that_are_gaps=12
