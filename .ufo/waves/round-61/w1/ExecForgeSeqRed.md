# ExecForgeSeqRed — red-before for amendment A1 (round 61, wave w1)

## Findings
1. A call-counting forge (no output guards) scores **20/20 C1=PASS** on the FIRST-freeze counter
   (`1661b85b:corpus/evidence/round61/c1-count.py`) at 5 of 5 seeds (61001, 61002, 61003, 81001, 81002).
2. The SAME forge scores **9, 11, 8, 10, 12 /20 C1=FAIL** on the AMENDED counter
   (`corpus/evidence/round61/c1-count.py`, git blob 137b6a70…, sha256 f1d8b6fd…cfff9ef) at 5 seeds
   (71001–71005). Min 8, max 12.
3. Red-before MET: first-freeze forged to 20/20, amended not. The forge is able to fail on the amended counter
   only because of the leg shuffle (route 1); the setsid/killpg and stderr-cap changes (routes 2, 3) were not
   exercised by this forge (it spawns no helper and prints little) — INFERENCE: not shown by this item.

## Forge (scratch /fast/scratch/hyaku/chousa-r61/ExecForgeSeqRed/forge.py, sha256 845b9f46…a9a97; deleted)
Counts its invocations in a file keyed by `os.getppid()` (the counter's pid, so each counter run restarts at 1).
Uses the first-freeze fixed leg order to map call index → leg:
calls 1–8 (P01, P02, P04×3, P05, P06×2) delegate to the unchanged BASE builder `tools/build-spans.py`
(blob 072415ad…, `sys.dont_write_bytecode=True` so P03 passes); call 11 (H08 `--replace`) deletes the old
`spans/`+`spans.tsv` then delegates to base (base alone fails H08: it refuses any non-empty `--out`);
every other call (9,10,12–23: H07, H09–H20) just prints `build-spans: refused` and exits 2 (1 for the H17/H18
calls 20,21). No symlink, size, memory, entry or file-type check exists anywhere in it. (forge.py was 25 lines and was deleted with the scratch; first version without the call-11 branch scored 19/20 on seeds 61001/61002,
H08 failing rc=2 — shown before the fix.)

## Evidence (commands run, `TMPDIR=/fast/scratch/hyaku/chousa-r61/ExecForgeSeqRed`, `python3 -B`)
First-freeze: counter extracted with `git show 1661b85b…:corpus/evidence/round61/c1-count.py`, placed at
`<scratch>/tree/corpus/evidence/round61/c1-first.py` with `tree/tools/capture-text.py` copied from the lane
(HERE/LANE resolve into `tree/`):
    python3 -B tree/.../c1-first.py --builder forge.py --work $TMPDIR/w-first-<seed> --seed <seed>
    → `LEGS=20/20 C1=PASS` ×5 (seeds 61001 61002 61003 81001 81002; the 19/20 runs above were the pre-fix forge)
Amended:
    python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round61/c1-count.py --builder <scratch>/forge.py --work … --seed <seed>
    seed 71001 → LEGS=9/20  (fail: P02 P04 P05 H07 H08 H10 H11 H15 H17 H19 H20)
    seed 71002 → LEGS=11/20 (fail: P01 P02 P04 P06 H07 H08 H12 H14 H15)
    seed 71003 → LEGS=8/20  (fail: P01 P02 P04 P05 P06 H07 H08 H09 H10 H11 H12 H16)
    seed 71004 → LEGS=10/20 (fail: P01 P04 P05 P06 H07 H08 H09 H12 H16 H17)
    seed 71005 → LEGS=12/20 (fail: P01 P02 P04 H07 H08 H15 H16 H17)
    each exit 1 `C1=FAIL`; outputs were kept in scratch only during the run.
Observation: P04 failed with `counter exception FileNotFoundError …/out/spans` at 4 of 5 seeds: when the shifted
call lands the hazard refusal on P04's first build, `out/spans` is never created. Not a counter defect — the
exception is caught as a leg failure by the counter's own `except Exception` path.

## Limits
- The forge defeats only the fixed-order route (1). A forge that identifies the leg from the fixture state
  (e.g. whether `--out` exists, a symlink under it, cache file sizes) would be a guard in all but name and was not
  built or tried: INFERENCE that the shuffle does not stop a state-sniffing builder; the admission sniff-sweep
  (`grep getppid|/proc/|c1-count|…`, A1) covers `getppid` — this forge uses `os.getppid()` and would be matched.
- Five amended seeds is a sample, not a distribution; the expected-pass-by-luck rate was not computed.
- No install, no network, no write outside scratch and this report; no git mutation. Scratch removed on exit.

VERDICT: FIRST_FREEZE_FORGED=20/20 AMENDED=8-12/20 over 5 seeds
