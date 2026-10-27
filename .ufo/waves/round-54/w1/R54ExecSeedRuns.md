# R54ExecSeedRuns — C1 counter flake and independence check (round 54, wave 1)

Seat scope: run the frozen C1 counter `corpus/evidence/round54/c1-count.py` many times and
falsify it on flake, independence and containment grounds. I edited neither the counter nor the
tool, the lane registry, the git index or jj state, and wrote no lane file except this report.
Scratch: `/fast/scratch/hyaku/chousa-r54/R54ExecSeedRuns` (created with `mkdir -p`, removed on exit).

## Headline

**81 counter runs, 0 flakes.** Every run of the frozen C1 counter that I executed printed
`LEGS=6/6` / `C1=PASS` / exit 0. No run was short of 6/6, so there is no defect to paste and
reproduce with a seed. The counter is deterministic in its verdict under reseeding and
per-leg resizing, cleans its scratch, leaves no `soffice.bin` behind, and reads nothing from
the lane registry/entries/spans (so it is causally separable from C2, as the freeze claims).

Three findings, none of which changes a frozen predicate, target, counter or control — they are
reported to the L1 for a decision:

1. **The lane's working-tree `tools/capture-text.py` moved mid-wave** (22:49:44), so the
   counter's default `--tool` is not stable across a wave; both measured shas pass 6/6.
2. **The counter writes a `.pyc` into the lane tree** (not `TMPDIR`/`--work`) when
   `corpus/evidence/round52/__pycache__/c1-count.cpython-314.pyc` is absent (mirrored-tree run);
   gitignored, so no tracked file changes.
3. **`--work DIR` is not re-entrant**: a second run into an existing `--work` dir dies with
   `FileExistsError` (traceback, exit 1) — outside the frozen predicate, a robustness note.

## 1. Flake matrix (primary run: pinned candidate blob)

The frozen candidate is commit `8a7d0f137a352000d78704ba5695ded8857104fe`, tool sha256
`fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`. Because of finding 1 the
authoritative matrix pins that blob to scratch and passes it with `--tool`, so a sibling's
lane-tree edit cannot perturb the measurement.

Driver (≤60 lines; `/fast/scratch/hyaku/chousa-r54/R54ExecSeedRuns/driver3.sh`):

```bash
#!/bin/bash
# R54ExecSeedRuns — driver v3: pins the FROZEN candidate 8a7d0f1 blob
# (sha256 fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89), because a
# sibling seat edited the lane's working-tree tools/capture-text.py mid-matrix (22:49:44).
set -u
S=/fast/scratch/hyaku/chousa-r54/R54ExecSeedRuns
CNT=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/c1-count.py
TOOL="$S/cand-capture-text.py"
mkdir -p "$S/out3"
cd "$S" || exit 1
LOG="$S/driver3.tsv"
: > "$LOG"
run_one() {
  local label="$1"; shift
  local out="$S/out3/$label.txt" tmp="$S/tmp3-$label"
  local before after t0 t1 rc legs c1 mine sha
  rm -rf "$tmp"; mkdir -p "$tmp"
  export TMPDIR="$tmp"
  before=$(find "$tmp" -mindepth 1 | wc -l)
  pgrep -af soffice > "$S/out3/soffice-before-$label.txt" 2>&1
  t0=$(date +%s%N)
  python3 "$CNT" --tool "$TOOL" "$@" > "$out" 2>&1
  rc=$?
  t1=$(date +%s%N)
  after=$(find "$tmp" -mindepth 1 | wc -l)
  pgrep -af soffice > "$S/out3/soffice-after-$label.txt" 2>&1
  mine=$(grep -c "chousa-r54/R54ExecSeedRuns" "$S/out3/soffice-after-$label.txt")
  legs=$(grep -E '^LEGS=' "$out" | tail -1)
  c1=$(grep -E '^C1=' "$out" | tail -1)
  sha=$(grep -o 'sha256=[0-9a-f]*' "$out" | head -1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$label" "$legs" "$c1" "$rc" \
    "$(( (t1 - t0) / 1000000 ))" "$before->$after" "mine=$mine" "$sha" >> "$LOG"
  echo "== $label $legs $c1 rc=$rc ms=$(( (t1 - t0) / 1000000 )) tmp=$before->$after mine=$mine $sha"
  rm -rf "$tmp"
}
for i in $(seq 1 12); do run_one "unseeded-$i"; done
for n in $(seq 1 12);  do run_one "seed-$n" --seed "$n"; done
for i in 1 2 3;          do run_one "perleg8-$i" --per-leg 8; done
echo "DONE"
```

Observed table (`driver3.tsv`: label / LEGS / C1 / exit / wall-ms / TMPDIR before->after /
soffice survivors under my scratch / tool sha):

```text
unseeded-1  LEGS=6/6 C1=PASS 0 7919  0->0 mine=0 sha256=fd0ed3f5...
unseeded-2  LEGS=6/6 C1=PASS 0 8295  0->0 mine=0 sha256=fd0ed3f5...
unseeded-3  LEGS=6/6 C1=PASS 0 8247  0->0 mine=0 sha256=fd0ed3f5...
unseeded-4  LEGS=6/6 C1=PASS 0 8272  0->0 mine=0 sha256=fd0ed3f5...
unseeded-5  LEGS=6/6 C1=PASS 0 11078 0->0 mine=0 sha256=fd0ed3f5...
unseeded-6  LEGS=6/6 C1=PASS 0 10316 0->0 mine=0 sha256=fd0ed3f5...
unseeded-7  LEGS=6/6 C1=PASS 0 9123  0->0 mine=0 sha256=fd0ed3f5...
unseeded-8  LEGS=6/6 C1=PASS 0 8775  0->0 mine=0 sha256=fd0ed3f5...
unseeded-9  LEGS=6/6 C1=PASS 0 8647  0->0 mine=0 sha256=fd0ed3f5...
unseeded-10 LEGS=6/6 C1=PASS 0 8274  0->0 mine=0 sha256=fd0ed3f5...
unseeded-11 LEGS=6/6 C1=PASS 0 8619  0->0 mine=0 sha256=fd0ed3f5...
unseeded-12 LEGS=6/6 C1=PASS 0 8883  0->0 mine=0 sha256=fd0ed3f5...
seed-1      LEGS=6/6 C1=PASS 0 8852  0->0 mine=0 sha256=fd0ed3f5...
seed-2      LEGS=6/6 C1=PASS 0 9030  0->0 mine=0 sha256=fd0ed3f5...
seed-3      LEGS=6/6 C1=PASS 0 8819  0->0 mine=0 sha256=fd0ed3f5...
seed-4      LEGS=6/6 C1=PASS 0 9506  0->0 mine=0 sha256=fd0ed3f5...
seed-5      LEGS=6/6 C1=PASS 0 8852  0->0 mine=0 sha256=fd0ed3f5...
seed-6      LEGS=6/6 C1=PASS 0 8337  0->0 mine=0 sha256=fd0ed3f5...
seed-7      LEGS=6/6 C1=PASS 0 8172  0->0 mine=0 sha256=fd0ed3f5...
seed-8      LEGS=6/6 C1=PASS 0 8735  0->0 mine=0 sha256=fd0ed3f5...
seed-9      LEGS=6/6 C1=PASS 0 8538  0->0 mine=0 sha256=fd0ed3f5...
seed-10     LEGS=6/6 C1=PASS 0 8476  0->0 mine=0 sha256=fd0ed3f5...
seed-11     LEGS=6/6 C1=PASS 0 8443  0->0 mine=0 sha256=fd0ed3f5...
seed-12     LEGS=6/6 C1=PASS 0 8635  0->0 mine=0 sha256=fd0ed3f5...
perleg8-1   LEGS=6/6 C1=PASS 0 11037 0->0 mine=0 sha256=fd0ed3f5...
perleg8-2   LEGS=6/6 C1=PASS 0 10757 0->0 mine=0 sha256=fd0ed3f5...
perleg8-3   LEGS=6/6 C1=PASS 0 10689 0->0 mine=0 sha256=fd0ed3f5...
```

Wall time: min 7919 ms, max 11078 ms, mean 9012 ms, median 8735 ms (n=27). `--per-leg 8`
printed `GEN=PASS 8 docs`, `NONWORD=PASS 8 sheets`, still `LEGS=6/6`.

Two earlier matrices, same shape, run before and across the sibling edit:

- `driver.tsv` (27 runs, default `--tool`, tool sha `fd0ed3f5…` throughout): all `LEGS=6/6`
  / `C1=PASS` / rc 0; ms min 10406, max 12881, mean 11619. **Caveat, disclosed:** this
  driver's LEGS scrape was `grep … | head -1`, which matched the REGRESS leg's inner
  `['LEGS=9/9']` string; the TSV shows `LEGS=9/9` for all 27 rows while the underlying stdout
  says `LEGS=6/6`. `driver2.sh`/`driver3.sh` take the last top-level `LEGS=` line instead;
  re-extraction of all 27 `driver.tsv` stdout files confirms `LEGS=6/6`, `C1=PASS`, zero
  `=FAIL` lines.
- `driver2.tsv` (27 runs, default `--tool`): 16 rows at tool sha `fd0ed3f5…` and 11 at
  `e7e381b6…` (after the sibling edit); all 27 `LEGS=6/6` / `C1=PASS` / rc 0 — the sibling's
  working-tree variant of the tool also passes the frozen counter 6/6.

Total: **81 counter runs, 81 × `LEGS=6/6`, 0 flakes.**

## 2. Independence

- **Seed → verdict**: 12 unseeded runs produced 12 distinct seeds (e.g. `seed=914596453`,
  `seed=418250772`, `seed=956492897`, …) and all 12 passed; 12 fixed seeds 1..12 all passed.
- **Seed → bytes**: the same seed twice is byte-identical in the generated documents
  (`--seed 11` into two work dirs: `ggen0.doc` `cdd2155d…`, `ggen1.doc` `8fbac6ce…`,
  `ggen2.doc` `0af6bd79…` both times; the two stdout files `diff` **IDENTICAL**). A different
  seed gives different documents (`--seed 12`: `49424c33…`, `0f703ca8…`, `dcda3f22…`), so the
  seed genuinely varies the corpus and the verdict is invariant to that variation.
- **Counter does not read lane state**: the `strace` read surface is exactly
  `corpus/evidence/round52/c1-count.py`, `corpus/evidence/round52/c1-supplement.py`,
  `corpus/evidence/round54/c1-count.py`, `tools/capture-text.py`, and the six pinned
  `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/*.raw` captures. It
  never opens the registry, the knowledge entries or the span manifest — C1 and C2 are
  causally separable as the freeze asserts. Write intent under the campaign cache: 0.
- **Base-tool negative control** (tool at `BASE_REV` `c49ffc6c…`, sha `6902db6a…`, extracted
  with `git show`): `LEGS=1/6`, `C1=FAIL`, exit 1 on `--seed 1` and `--seed 7`, every leg
  failing with `REFUSED not a zip (an OOXML capture is a zip package)` — reproduces the frozen
  before-receipt `controls/c1-before.txt` independently.
- **`--per-leg 1` guard**: `usage: --per-leg must be at least 2 (sample-size guard)`, exit 2.
- **`ENV_CHANGED` is reachable**: a counter copy whose `REAL` prefix for `54fe0734…` is
  perturbed to `00000000000000000000` printed
  `ENV_CHANGED pinned capture 54fe0734c01f699e735b4b0a differs` and exited 2 (not 1) — the
  kill rule's exit-2 branch is distinguishable from a leg failure.

## 3. Scratch, process and filesystem containment

- **Scratch cleanup**: with a fresh per-run `TMPDIR`, entries under `TMPDIR` went `0 -> 0` in
  all 54 runs of `driver2`/`driver3`; the default work dir is a `TMPDIR` mkdtemp removed on
  exit (`c1-count.py` `finally: shutil.rmtree(work)`); an isolated empty-`TMPDIR` run left 0/0.
- **`--work DIR` is not cleaned** (by design: `own = a.work is None`) and **not re-entrant**:
  a second run into an existing `--work` dir raised `FileExistsError: … /reuse/src-gen`
  (traceback, exit 1). Reported, not patched — the frozen predicate does not cover `--work`.
- **`soffice.bin` survivors**: `pgrep -af soffice` after the matrix shows only other seats'
  processes (`R54ExecOleFuzz/c1work/…`); `pgrep -af "UserInstallation=file://$S"` returns
  nothing (rc 1) at every per-run checkpoint (`mine=0` in all 27 rows of `driver3.tsv`) and
  at the end of the session. **No survivor of mine.**
- **Writes outside `TMPDIR`/`--work`** (`strace -f -y -e trace=openat,creat,mkdir,rename`,
  two runs, one with `-y`):
  - `/tmp/hsperfdata_vgpnk/<pid>` — created by the JVM LibreOffice's Java helper starts
    (`mkdir("/tmp/hsperfdata_vgpnk") = -1 EEXIST`, then
    `openat(…"/tmp/hsperfdata_vgpnk","1430986",O_RDWR|O_CREAT|…) = 6`); the per-pid file is
    removed on JVM exit (`find /tmp/hsperfdata_vgpnk -type f | wc -l` → 0). LibreOffice's own
    behaviour, not the counter's.
  - `/usr/lib/libreoffice/program/../share/uno_packages/cache/stamp.sys` — attempted with
    `O_CREAT|O_EXCL`, refused with `EACCES`, so no write occurred.
  - `~/.config/libreoffice` — **0 references** in either trace (the private
    `-env:UserInstallation` profile keeps it untouched; dir mtime `2026-10-22`, unchanged).
  - The lane tree: **0** write-intent opens under `/home/vgpnk/Projects/shokunin/chousa-shokunin`
    in the direct-lane trace, and a full-tree before/after snapshot (26248 files,
    path+mtime+size) around one counter run printed `LANE UNCHANGED`.
  - **Exception (finding 2):** when the lane's `corpus/evidence/round52/__pycache__/` is
    absent, the REGRESS leg causes a `.pyc` to be written **into the lane tree**, outside
    `TMPDIR`/`--work`. Proven on a mirrored copy of the two counters (no `__pycache__`
    beforehand):
    `openat(AT_FDCWD<…>, "…/mirror2/corpus/evidence/round52/__pycache__/c1-count.cpython-314.pyc.139762071429136", O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC, 0644) = 3`
    (route: `c1-supplement.py` `_load()` → `importlib.util.spec_from_file_location` +
    `exec_module` of `round52/c1-count.py`). In the live lane the file already existed (mtime
    `22:21:35`, from the L1's pre-freeze feasibility run), so my runs only *read* it
    (`openat(…, "…/round52/__pycache__/c1-count.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3`).
    `corpus/**/__pycache__/` is gitignored (`.gitignore:3`), so no tracked file or index
    entry changes.
- **Working-tree tool edit (finding 1)**: at `2026-10-26 22:49:44.975810605 -0300` a sibling
  seat changed the lane's `tools/capture-text.py` from candidate sha `fd0ed3f5…` to
  `e7e381b6…` (`git status`: ` M tools/capture-text.py`; the diff adds a `cb_grpprl` bounds
  check in `doc_text_form`'s Clx `Prc` walk, raising
  `Refused("ole-malformed: Prc GrpPrl outside the Clx")`). The default `--tool` resolves to
  that mutable path, so a wave-long measurement silently switches tools mid-matrix. Both shas
  measure `LEGS=6/6` / `C1=PASS` (16 + 11 runs in `driver2`, 27 pinned runs in `driver3` on
  `fd0ed3f5…`), so the verdict is unaffected — but the reproducibility of "the candidate" is
  not, and the L1 should decide whether admitted evidence must cite the tool sha (the counter
  already prints it in its header line).

## 4. What I did not do

I did not edit the counter, the tool, the frozen claims, the controls or any registry/entry,
did not run any `/home/vgpnk/Projects/shokuknow` campaign tool, and did not write to the fleet
repo, a sibling lane or `~/.local/bin`. No tool was installed or upgraded this round (the runs
used only the host's `/usr/bin/strace`, LibreOffice 26.8.1.1, Python 3.14.8), so the operator
tooling directive has nothing to record.

## 5. Verdict on the frozen claim

The frozen C1 predicate's kill rule ("any leg failing in any of those runs, or an `ENV_CHANGED`
exit 2") was not triggered by anything I could produce: 81 runs, 81 × 6/6, exit 0, no flake
under 12 unseeded seeds, 12 fixed seeds, 3 × `--per-leg 8`, and 2 additional matrices. The
counter is seed-invariant, sample-size-robust, self-cleaning, spawn-free on the tool path,
and independent of lane state. The three findings above are robustness/hygiene issues for the
L1 to weigh (tool-sha pinning of the default `--tool`; the lane-tree `.pyc` write; `--work`
re-entrancy); none is a leg failure and none is patched here.

VERDICT: C1 counter flake/independence attack — 81 runs (12 unseeded + 12 seeded + 3 per-leg-8, three matrices) all `LEGS=6/6` `C1=PASS`, no defect to reproduce; scratch cleans, no `soffice.bin` survivor, no `~/.config/libreoffice` write, but the counter's default `--tool` moved mid-wave and the REGRESS leg writes a `.pyc` into the lane tree.
