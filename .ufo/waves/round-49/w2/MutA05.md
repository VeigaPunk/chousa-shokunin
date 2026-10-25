# MutA05 — mutation probe of `corpus/evidence/round49/a05-check.py` (R49 W2 FALSIFY)

Target sha256 `cad12e5f2ccaf0b2e32481367849c6b6aff7b558d4b17d02eb6659abc61e5a28` (before == after all runs).
Contract under test: every `corpus/lessons/*.md` line (except `round-49.md` itself) carrying `3/12` with `a05`
and not the true figure `2/12 (p03, p04)` (`a05-check.py:23-24,42-46`) must be named `<file>:<line>` on a
`2/12` line inside `round-49.md`'s `## Mistakes` / `## Spot-check intake` sections (`a05-check.py:35-40`).

## Baseline (real lane, run in place)

```
$ sha256sum corpus/evidence/round49/a05-check.py && TMPDIR=/dev/shm/chousa-r49-MutA05 \
  python3 corpus/evidence/round49/a05-check.py; echo "exit=$?"
cad12e5f…a528  corpus/evidence/round49/a05-check.py
CORRECTED round-47-verifier-spotcheck.md:29
CORRECTED round-48.md:34
A05_PROPAGATIONS=2 CORRECTED=2
exit=0
```

Re-run at certification time on the committed tip bytes: identical stdout, exit=0.

## Method

- Scratch `/dev/shm/chousa-r49-MutA05/` (deleted before finish). Six states, each a byte-copy of
  `corpus/lessons/` (60 `.md`, 904K; sha256 manifest equal to lane at staging) plus
  `corpus/evidence/round49/{a05-check,m1..m5}.py`. Mutants execute only from scratch copies — the script
  reads lessons relative to its own location (`parents[3]`), and the lane tree was never written.
  "Against the lane" = `S_base`, the manifest-equal byte copy; pristine `S_base` output is identical to the
  real-lane run above.
- Mutants, single-point, verified by `difflib` before runs:
  - m1 drops the TRUE-figure exemption: `a05-check.py:46` `if PROP.search(line) and not TRUE.search(line):` → `if PROP.search(line):`
  - m2 scans round-49.md too: deletes the `if p.name == "round-49.md": continue` skip (`a05-check.py:43-44`)
  - m3 accepts a correction without the figure: `a05-check.py:39` `if keep and "2/12" in line:` → `if keep:`
  - m4 accepts a correction outside the intake sections: `a05-check.py:37` allowlist → `keep = line.strip().startswith("## ")`
  - m5 drops case-insensitivity: `a05-check.py:23` regex loses `(?i)`
- Probes: `zz-mutprop.md:3` = new uncorrected propagation `3/12 … a05` without the true figure, added in
  S_prop/S_corrno212/S_corrsec; `zz-mutprop-upper.md:3` (`…A05…`) in S_upper; S_gate inserts the same stale
  figure inside round-49.md's `## Gate` section; S_corrno212 adds a `## Mistakes` row naming `zz-mutprop.md:3`
  WITHOUT `2/12`; S_corrsec appends a `## Corrections` section (non-intake) with `zz-mutprop.md:3 true figure 2/12 (p03, p04).`

## Kill matrix (exit codes; certification run on committed tip bytes)

| script \ input | S_base (lane) | S_prop | S_gate | S_corrno212 | S_corrsec | S_upper |
|---|---|---|---|---|---|---|
| pristine | 0 | 1 | 0 | 1 | 1 | 1 |
| m1 drop TRUE exemption | **1 KILL** | 1 | 1 | 1 | 1 | 1 |
| m2 scan round-49.md | 0 | 1 | **1 KILL** | 1 | 1 | 1 |
| m3 corr without 2/12 | 0 | 1 | 0 | **0 KILL** | 1 | 1 |
| m4 corr outside intake | 0 | 1 | 0 | 1 | **0 KILL** | 1 |
| m5 case-sensitive regex | 0 | 1 | 0 | 1 | 1 | **0 KILL** |

All 36 cells exit+stdout-identical across two lesson variants (see Restoration note), checked programmatically: `True`.

## Observed kill cells (verbatim)

```
m1 @ S_base   exit=1 : CORRECTED round-47-verifier-spotcheck.md:29 ; UNCORRECTED round-48-verifier-spotcheck.md:46 ;
                       UNCORRECTED round-48-verifier-spotcheck.md:78 ; CORRECTED round-48.md:34 ;
                       A05_PROPAGATIONS=4 CORRECTED=2      (pristine: exit=0, PROPAGATIONS=2)
m2 @ S_gate   exit=1 : … ; UNCORRECTED round-49.md:37 ; A05_PROPAGATIONS=3 CORRECTED=2   (pristine: exit=0)
m3 @ S_corrno212 exit=0 : … ; CORRECTED zz-mutprop.md:3 ; A05_PROPAGATIONS=3 CORRECTED=3  (pristine: exit=1 UNCORRECTED)
m4 @ S_corrsec   exit=0 : … ; CORRECTED zz-mutprop.md:3 ; A05_PROPAGATIONS=3 CORRECTED=3  (pristine: exit=1 UNCORRECTED)
m5 @ S_upper     exit=0 : A05_PROPAGATIONS=2 CORRECTED=2   (pristine: exit=1 UNCORRECTED zz-mutprop-upper.md:3)
```

m1 mechanism: `round-48-verifier-spotcheck.md:46` and `:78` each carry PROP∧TRUE — the stale
`exit-level 3/12 incl. a05` beside `2/12 (p03, p04)` — so pristine exempts them; the corr lines
(`corpus/lessons/round-49.md:19,28`) name only `…:29`, `round-48.md:34`, `…:35`, and `…:43,46`, and the
`:43,46` form cannot match ref `:46` (`re.escape(ref)+r"(?!\d)"` needs literal `md:46`). m1 flags both → exit 1.

## Detector-direction controls (pristine; includes the assigned scratch probe)

- S_prop (new uncorrected propagation): `UNCORRECTED zz-mutprop.md:3`, exit 1 — caught.
- S_upper: `UNCORRECTED zz-mutprop-upper.md:3`, exit 1 — uppercase `A05` still matched (case-insensitive).
- S_corrno212 / S_corrsec: exit 1 — a correction lacking `2/12`, or living outside `## Mistakes` /
  `## Spot-check intake`, is refused.

## Survivors

None — 5/5 killed. Coverage note: m2/m3/m4/m5 are behaviour-invisible on the lane's current bytes (their
S_base column matches pristine exactly); the kills needed out-of-frozen-input probes. The lane pass of this
checker is therefore necessary but not sufficient evidence of its correctness — consistent with its role as a
closed-form correction checker over append-only lessons.

## Restoration / no-harm evidence

- `sha256sum corpus/evidence/round49/a05-check.py` before and after all runs: `cad12e5f…a528` both times.
- `git rev-parse master` before and after the matrix runs: `87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0` both
  times. After cleanup, the tip advanced to `5275c892…` ("round-49: final after-measurement", lane-owner
  commit, not mine); `git show master:corpus/evidence/round49/a05-check.py | sha256sum` is still
  `cad12e5f…a528` — the tested bytes are the tip bytes — and a pristine re-run at the new tip prints the
  same `A05_PROPAGATIONS=2 CORRECTED=2`, exit=0.
- `git status --porcelain -- corpus/` → 0 lines at both checks; all lane-wide porcelain entries were
  siblings' untracked `.ufo/waves/**` files (11 → 23 during the window), none authored here.
- Transient observation (not my edit): during the window the lane working tree's `round-49.md` moved from a
  stale variant (sha `46931e04…`, lacking the committed `### Wave-2 narrowing` block and the full-quote S100/
  S101/S102 span rows) back to the committed tip bytes (sha `28a85f25…`; `git show master:…` == working file).
  The variance touches only the `## Gate` spans table and the Wave-2 section — not the intake sections the
  checker reads — and the full 36-cell matrix was re-certified byte-identical on the committed bytes.
- Lessons manifest lane == scratch copy: equal at staging; at final check differed only by the `round-49.md`
  variant above; both variants were exercised with identical results.
- Scratch tree `rm -rf /dev/shm/chousa-r49-MutA05` (exact root, only mine) executed before finish; `TMPDIR`
  pointed into the scratch root for every Python run.

VERDICT: a05-check.py — holds — all five assigned mutants killed (m1 on lane-equal bytes, m2/m3/m4/m5 on
targeted probes beyond the frozen inputs), pristine passes the lane and catches a new uncorrected
propagation, no survivors, and the lane tree is byte-unchanged by this probe.
