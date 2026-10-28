# ExecIndepBuilder3 — round 61 w1 — independent hardened builder (reachability)

## Findings
- The base builder plus a ~113-line diff reached `LEGS=20/20 C1=PASS` at all three seeds on the first counter run (61101, 61102, 61103; exit 0 each). `REAL_REBUILD=3/3`.
- Legs first failed: none. I did not run the counter on a draft that failed, so I have no failure-and-fix sequence to report. The base's known failures (P03, H07–H17, H20) were designed against from the docstring plus the base source, not measured by me. The code passed as written.
- Inputs: I read only the counter docstring (lines 1-49), the base `tools/build-spans.py` and `claims.md`. I did not open `controls/ref-build-spans.py`, and I did not read the counter body beyond the import lines the grep returned. The counter docstring was enough to build against.
- No labrat spawned. No installs. Scratch deleted (`/fast/scratch/hyaku/chousa-r61/ExecIndepBuilder3` gone).
- Sniff sweep (`grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]'` on the builder): exit 1, no match.
- Candidate: `.ufo/waves/round-61/w1/ExecIndepBuilder3/build-spans.py`, sha256 `51c40345977a6a2ee0dd70c6b5d84cc43f653a4a4300366edd70a2817e67ae88`.

## What the diff does (smallest change per hazard)
- `sys.dont_write_bytecode = True` before the `capture-text` import (P03).
- `MAX_BYTES` = 64 MiB. `Forms.slurp()` resolves the path and requires it inside the cache (H13). It opens with `O_NONBLOCK|O_NOFOLLOW`, then `fstat` must be a regular file (H18) and `st_size` ≤ cap before any read (H14, H15). The OLE/zip head is read as 8 bytes only. `OSError`/`ValueError`, including `capture-text` failures and a text form over 64 Mi chars, become a refused row, exit 1 (H17, H20).
- `--out` that exists and is not a directory: exit 2 before anything else (H16).
- `preflight()` runs before any write and returns exit 2 with nothing written when:
  - `spans/` is a symlink or non-dir (H10);
  - `spans.tsv` or a span-file target is a symlink or non-file (H11, H12);
  - without `--replace`, the existing `spans.tsv` bytes differ from the manifest this run would write (H07);
  - without `--replace`, DIR holds a span file this run does not write (H09).
- New `--replace` flag skips the last two checks only. Orphan span files are then deleted by the existing loop, and non-span files are kept (H08).
- Writes go through `put()`: `mkstemp` beside the target, `os.replace`, temp file removed on failure.

## Evidence (commands run, observed output)
All three seeds printed the same 20 pass lines. The `rss_kib` values are the child's peak RSS.

    python3 -B .../c1-count.py --builder <B> --work $S/w61101 --seed 61101   -> LEGS=20/20 C1=PASS (exit 0)
    ... --seed 61102 -> LEGS=20/20 C1=PASS (exit 0);  --seed 61103 -> LEGS=20/20 C1=PASS (exit 0)
    seed 61101 H14 rss_kib=19612 / H15 rss_kib=21876 (limit 98304); H20 rc=1 rss_kib=292004 (the counter sets no RSS limit there)
    seed 61102 H14 20108 / H15 22324;  seed 61103 H14 19872 / H15 22704
    python3 -B .../regress.py --builder <B> --work $S/rg
      round55 check_rc=0 build_rc=0 identical=True pass
      round56 check_rc=0 build_rc=0 identical=True pass
      round57/c3 check_rc=0 build_rc=0 identical=True pass
      REAL_REBUILD=3/3 (exit 0)

Per-leg rc at seed 61101, same at all seeds:
- P01 rc=0, P02 rc=0, P03 pass (tools = build-spans.py, capture-text.py only), P04 rc=0,0,1, P05 rc=1, P06 rc=0,0.
- H07 rc=2,2; H08 rc=0; H09 rc=2.
- H10, H11 and H12 each rc=2 with victim_unchanged=True.
- H13 rc=1, leaked=False.
- H16 rc=2, traceback=False; H17 rc=1, traceback=False; H18 rc=1; H19 rc=2.

## Counter docstring ambiguities (n=7)
1. **H07 "a different `spans.tsv`"**: different from what is unstated. I read it as bytes not equal to the manifest this run would write. A reading of "differs from the golden/previous build" would be the same for the leg's fixtures, but the rule for a real rebuild after a changed quote table is not specified.
2. **`--replace` is unspecified.** The docstring names the flag in H08 only. The base has no such flag, and nothing says what it overwrites or deletes. I chose: skip the foreign-manifest and orphan refusals, delete orphan span files, keep non-span files.
3. **H08 "the same input"**: the pre-state of DIR is not stated (foreign manifest, orphans, or both?). My design handles both, so I could not tell whether it was narrower.
4. **H10–H12 offer two acceptable behaviours** ("exit non-zero, or replaced by a regular file with the golden tree"). I took the refusal branch for all three. The docstring does not say which the lane prefers, and the leg cannot distinguish a deliberate refusal from an incidental error.
5. **H13 "outside the cache"**: it is not said whether a symlink that stays inside the cache is allowed. I allowed it (the resolved path must be under the resolved cache). The leg does not test that case.
6. **H14/H15/H20 "nothing written"**: it is unclear whether creating an empty `--out` directory counts. I create nothing before the checks pass. H20 gives no RSS bound (observed 220–292 MiB peak). "Over 64 MiB chars" does not say whether the cap applies to characters or bytes. I cap bytes for captures and characters for the form.
7. **P03 NOPYC**: it is not stated whether the counter launches the child with `-B`. I set `sys.dont_write_bytecode` inside the builder so the result does not depend on it. H17 (mode 000) only fails as intended for a non-root uid; I ran as uid 1000 and did not test root.

## Risks
- Named limits in claims.md hold for my builder as well: TOCTOU between the guards and the write, and no total bound over many rows (the cap is per capture).
- `--check` still follows a symlinked `spans.tsv` and reads it unbounded. No leg covers that; it is read-only.
- Reachability: a first-try 20/20 shows the legs are reachable from the docstring and the base source by someone who has not seen the reference. It says nothing about whether they discriminate between implementations. Other seats' mutants cover that.

VERDICT: INDEP3_LEGS=20/20 REAL_REBUILD=3/3 ambiguities=7
