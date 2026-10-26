# R52ExecSeedRuns — C1 counter: flake and independence (round 52, wave 1)

seat: R52ExecSeedRuns (leaf) · 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
Object under test: `corpus/evidence/round52/c1-count.py` (read only, not edited) against the
candidate `tools/capture-text.py`. Lane HEAD `13bc28063b4bd7ea2e521167413ee9829202a420`;
candidate identity: `git show 804a45370dc992bfe714817281535055c2f9b032:tools/capture-text.py | sha256sum`
= `3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1` = `sha256sum tools/capture-text.py`;
`git status --porcelain tools/capture-text.py corpus/evidence/round52/c1-count.py` printed nothing.
No production file touched, nothing staged. No tool installed: `python3` and `/usr/bin/strace` were
already present (pacman paused host-wide, so no `-S`). Scratch = `/fast/scratch/hyaku/chousa-r52/R52ExecSeedRuns`,
`TMPDIR` set to it for every counter call, removed at the end.

## 1. Flake matrix — 45 invocations, 45 × `LEGS=9/9 C1=PASS` rc 0

Driver (43 lines, ran from the scratch dir with `TMPDIR=$PWD`; it prints one row per run and dumps
the full output of any run whose `LEGS` is not 9 or whose rc is not 0 — no such dump was produced):

```python
# drive.py — 20 unseeded + 20 seeded + 5 at --per-leg 10; logs TMPDIR entry count before/after each run
import os, re, subprocess, sys, time
S = "/fast/scratch/hyaku/chousa-r52/R52ExecSeedRuns"
CNT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/c1-count.py"
env = dict(os.environ, TMPDIR=S)
def entries():
    tot = sorted(os.listdir(S))
    return len(tot), [e for e in tot if e.startswith("c1r52-")]
def run(args, tag):
    before = entries(); t0 = time.monotonic()
    p = subprocess.run([sys.executable, CNT] + args, capture_output=True, text=True, env=env)
    dt = time.monotonic() - t0; after = entries(); out = p.stdout
    legs = re.search(r"^LEGS=(\d+)/(\d+)$", out, re.M); c1 = re.search(r"^C1=(\w+)$", out, re.M)
    fails = [l for l in out.splitlines() if "=FAIL" in l]
    print(f"{tag}\targs={' '.join(args) or '-'}\tLEGS={legs.group(1)}/{legs.group(2) if legs else '?'}"
          f"\tC1={c1.group(1) if c1 else '?'}\trc={p.returncode}\t{dt:.2f}s"
          f"\ttmp_before={before[0]}\ttmp_after={after[0]}\tleftover={before[1] or after[1] or '-'}")
    for l in fails: print(f"  FAIL-LINE {tag}: {l}")
    if p.stderr.strip(): print(f"  STDERR {tag}: {p.stderr.strip()}")
    if fails or p.returncode != 0 or not legs or legs.group(1) != "9":
        print(f"----- FULL OUTPUT {tag} -----\n{p.stdout}{p.stderr}----- END {tag} -----")
        return False
    return True
ok = True
for i in range(1, 21): ok &= run([], f"unseeded-{i:02d}")
for n in range(1, 21): ok &= run(["--seed", str(n)], f"seed-{n:02d}")
for i in range(1, 6): ok &= run(["--per-leg", "10"], f"perleg10-{i}")
print(f"ALL={'PASS' if ok else 'FAIL'} runs=45"); sys.exit(0 if ok else 1)
```

Per-run result (cell `NN 9/9 P r0` = run NN, `LEGS=9/9`, `C1=PASS`, rc 0; every run also reported
`tmp_before=2 tmp_after=2 leftover=-`; driver tail `ALL=PASS runs=45`, driver rc 0):

```
unseeded 01 9/9 P r0 | 02 9/9 P r0 | 03 9/9 P r0 | 04 9/9 P r0 | 05 9/9 P r0
unseeded 06 9/9 P r0 | 07 9/9 P r0 | 08 9/9 P r0 | 09 9/9 P r0 | 10 9/9 P r0
unseeded 11 9/9 P r0 | 12 9/9 P r0 | 13 9/9 P r0 | 14 9/9 P r0 | 15 9/9 P r0
unseeded 16 9/9 P r0 | 17 9/9 P r0 | 18 9/9 P r0 | 19 9/9 P r0 | 20 9/9 P r0
seed=1..20: 01 9/9 P r0 | 02 9/9 P r0 | 03 9/9 P r0 | 04 9/9 P r0 | 05 9/9 P r0
             06 9/9 P r0 | 07 9/9 P r0 | 08 9/9 P r0 | 09 9/9 P r0 | 10 9/9 P r0
             11 9/9 P r0 | 12 9/9 P r0 | 13 9/9 P r0 | 14 9/9 P r0 | 15 9/9 P r0
             16 9/9 P r0 | 17 9/9 P r0 | 18 9/9 P r0 | 19 9/9 P r0 | 20 9/9 P r0
--per-leg 10: 1 9/9 P r0 | 2 9/9 P r0 | 3 9/9 P r0 | 4 9/9 P r0 | 5 9/9 P r0
```

Wall time 1.34–1.48 s unseeded/seeded, 4.15–4.33 s at `--per-leg 10` (10 packages per generated
leg, i.e. 30 `--locate` and 40 refusal calls per run). No run diverged, so **no defect output to
paste**. Note `--per-leg 10` triples the LOCATE packages and quadruples REFUSE cases: `REFUSE` alone
was exercised 5 × 10 × 4 = 200 times, `MAIN_PART` 50 times over fresh random member names.

## 2. Scratch cleanup and write confinement

- Entry counts under `TMPDIR` never moved during any of the 45 runs (2 → 2: the driver's two files),
  and `ls -d c1r52-*` was empty after every run and after every probe below.
- `strace -f -e trace=openat,creat,mkdir,mkdirat,rename,renameat,unlink,unlinkat -o strace.log
  python3 c1-count.py` (7699 log lines): the counter `mkdir`ed `c1r52-qkfwdkfv` and removed every file
  it wrote (`unlinkat(3, "ecg1f1ol4k.docx", 0) = 0`, …); the only write-intent open outside that
  directory was one stdlib probe file in `TMPDIR` itself, created and unlinked immediately:
  `266: openat(AT_FDCWD, ".../R52ExecSeedRuns/81t4t_0b", O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600) = 3`
  `267: unlink(".../R52ExecSeedRuns/81t4t_0b") = 0` (still inside TMPDIR).
  `grep -E 'openat\(.*(O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND)' strace.log | grep -v '<scratch>'` → empty:
  **zero write-intent opens outside the scratch dir**.
- `--work` honoured: `c1-count.py --work $PWD/w` under `strace -e trace=mkdir,rmdir` gave
  `mkdir(".../w/c1r52-g3_var6y", 0700) = 0` then `rmdir(".../w/c1r52-g3_var6y") = 0`, `LEGS=9/9`,
  `w` empty afterwards (0 entries) — scratch is created and removed, never left behind.
- Failure paths still clean: `--tool /nonexistent/nope.py` → `LEGS=0/9 C1=FAIL` rc 1, entries 7 → 7;
  `--per-leg 0` → `per-leg must be >= 1` rc 2 with no scratch dir (arg check precedes `mkdtemp`).

## 3. Independence

- Non-stdlib read surface from the same strace log (paths opened, reads included), filtered to the
  two repositories: `.../corpus/evidence/round52/c1-count.py`, `.../chousa-shokunin/tools/capture-text.py`
  (the default `--tool`), and `.../shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw`
  — the pinned REAL capture, nothing else. No `corpus/knowledge` entry, no staged merge package, no
  second cache member is opened: the pass cannot be sourced from lane prose or from pre-read fixtures.
- Pinned capture digest still `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`
  (= `REAL_SHA` in the counter), so the REAL leg's `chars=19682` is measured on unchanged bytes
  (`REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`).
- Path independence: with the candidate copied to scratch, `--tool $PWD/copy-tool.py --seed 13` gave
  `LEGS=9/9 C1=PASS`; the counter measures behaviour, not the lane path.
- Not vacuous: with `--seed 7` the same counter scored the lane controls `naive-tool.py` 4/9
  (`REVISIONS=FAIL text differs at 8 (got 85 chars, want 36)`, `LAYOUT=FAIL text differs at 0`,
  `ALTCONTENT=FAIL text differs at 27`, `MAIN_PART=FAIL text differs at 0`, `REFUSE=FAIL norel not
  refused`), `cache-txt-tool.py` 0/9, `const-tool.py` 0/9 — identical to `claims.md`, so the 9/9 for
  the candidate separates it from a fixed-name/tag-strip reader and from the garbage `.txt` sidecar.

## 4. Residual flake vectors (both closed by reading, not by luck)

- REFUSE/`bytes`: `zipfile.is_zipfile` scans for an end-of-archive record, so random bytes could match
  with p ≲ 512·2⁻³² ≈ 1.2e-7; even then the bytes carry no `_rels/.rels`, so `main_part` raises
  `Refused` (c1-count.py:299-316 + capture-text.py:49-62) and the leg still passes. Not a flake source.
- LOCATE: `once` is 6+ characters drawn from ≥62-symbol alphabets, in text of a few hundred positions,
  so an accidental second occurrence is bounded by ~300·62⁻⁶ ≈ 5e-9 per package (arithmetic bound,
  [INFERENCE]; no collision in 45 runs plus 5 × 10 packages). A real collision would surface as
  `once=(1, 2, …) want (0,1,…)`, which no run printed.

Residual risk: all 45 runs share one host, one interpreter and one filesystem; there is no cross-host
replication, so "no flake observed" stays a statement about this host. Beyond the ask, 8 counters run
simultaneously on the shared `TMPDIR` all returned 9/9 (8 × `C1=PASS`, rc 0, no leftover dirs), so
`mkdtemp` name separation holds under contention.

VERDICT: attacked the frozen C1 counter for flake and independence — 45/45 runs at `LEGS=9/9 C1=PASS`
(20 unseeded, seeds 1–20, 5 × `--per-leg 10`), zero writes outside TMPDIR/`--work`, zero scratch
residue, read surface limited to the counter, the candidate tool and the pinned capture, controls
still 4/9/0/0 — no defect found and nothing edited.
