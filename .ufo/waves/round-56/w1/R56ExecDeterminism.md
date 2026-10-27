# R56ExecDeterminism — the C1 gate is deterministic per (tool, seed): triple-run kill rule survives

seat: R56ExecDeterminism · round 56 · wave W1 (build + attack) · 2026-10-27
axis: operability (C1), calibration of the frozen counter's triplicate kill rule
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`; BASE `e5a3795191601797613eb986b36fa0b1a73fe6a1`; tested bytes equal
lane HEAD `99eff0e` (`git diff --stat 0c2f4ce..HEAD -- corpus/evidence/round56/ tools/` only adds C2 spans/quotes, so the
C1 gate and battery are unchanged from `46e1758`).
bytes under test (sha256, as echoed by every run header): `c1-gate.py`
`e3cb3ec5764592553b8601a1718bb5d07fd8c9991de9f4128482d41ffd4e4971`, `tools/build-spans.py`
`1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, `battery/m2-span-beside-quote.py`
`136adc60868150682646e7d32d3561cd0b8bd53f7bdd71d96219b5e3ab535776`, `battery/m6-manifest-on-refusal.py`
`255d95fc8c4aac332f284bce610636b05c792cbb956e4a944834b43cfbbeee78`.
Scratch `/fast/scratch/hyaku/chousa-r56/R56ExecDeterminism` (TMPDIR there, `PYTHONDONTWRITEBYTECODE=1`), removed at the end.

Claim under attack: R56-C1's KILLED rule — "fails a leg ... in its first G run and in three more G runs, and passes that
leg ... in three mutant runs, the six runs in a random order" / M9's "three G vectors ... three mutant vectors" —
presupposes each gate run is a function of `(tool, seed)` alone. If two runs at one seed differed (quote pick, soffice
output, timing), a kill could be counted from chance rather than from the mutated clause.

## Method — the seat's matrix, then two sharpenings

```
S=/fast/scratch/hyaku/chousa-r56/R56ExecDeterminism; L=/home/vgpnk/Projects/shokunin/chousa-shokunin
python3 $L/corpus/evidence/round56/c1-gate.py --tool <T> --seed <7|56> --per-leg 2 --work $S/runs/w-<T>-<seed>-<i>
#   T = tools/build-spans.py, battery/m2-span-beside-quote.py, battery/m6-manifest-on-refusal.py
#   i = 1..5, fresh empty --work each time (the gate keeps the work tree when --work is given)
```
30 runs, then every file the gate leaves behind was sha256'd per run (`find . -path ./soffice-profile -prune -o -type f
-print0 | sort -z | xargs -0 sha256sum`), so the comparison covers `.doc`/`.xls` cache bytes, `quotes.tsv` (the quote
picks), `out/spans.tsv`, every span file and `hook.py` — not only the printed lines.

## Result 1 — the seat's matrix: 30/30 identical within every (tool, seed) group

```
builder seed=7   out_distinct=1  core_distinct=1   GENOLE=PASS 2 docs, 4 quotes · OLEPIN=PASS 4 captures, 8 quotes
                                                   REFUSE=PASS 4 cases · REGRESS=PASS r54 33 rows identical
                                                   LEGS=4/4 C1=PASS rc=0
builder seed=56  out_distinct=1  core_distinct=1   same five lines
m2 seed=7        out_distinct=1  core_distinct=1   GENOLE=FAIL S901 char · OLEPIN=FAIL S921 char
                                                   REFUSE=PASS 4 cases · REGRESS=FAIL spans.tsv differs from round 54's
                                                   LEGS=1/4 C1=FAIL rc=1
m2 seed=56       out_distinct=1  core_distinct=1   same five lines
m6 seed=7        out_distinct=1  core_distinct=1   GENOLE=PASS · OLEPIN=PASS · REFUSE=FAIL NOFORM: spans.tsv written
                                                   REGRESS=PASS r54 33 rows identical · LEGS=3/4 C1=FAIL rc=1
m6 seed=56       out_distinct=1  core_distinct=1   same five lines
```
`out_distinct` = distinct sha256 of the 5 stdout+rc captures; `core_distinct` = distinct sha256 of the 5 work-tree
manifests (86 files for builder/m2, 73 for m6). One digest each ⇒ the printed leg lines, the verdict, and every judged
artifact reproduced exactly five times per seed on all three tools.

## Result 2 — sharpenings

1. **Quote picks are identical, not merely equal in count.** `quotes.tsv` is inside the core manifests and its digest is
   stable across the five runs; the comparison is not vacuous, because it does separate the seeds:
   `w-builder-7-1/run1-*/quotes.tsv` = `18c482fc2761728e6801…`, `w-builder-56-1/run1-*/quotes.tsv` =
   `4a742f15a5decafbe2b0…` (different quote picks at different seeds, identical at the same seed).
2. **`--per-leg` is visible to the checker, so the leg lines carry real information.** Builder, seed 7:
   `per-leg=2 GENOLE=PASS 2 docs, 4 quotes / OLEPIN=PASS 4 captures, 8 quotes`;
   `per-leg=3 GENOLE=PASS 3 docs, 6 quotes / OLEPIN=PASS 4 captures, 12 quotes`.
3. **Time-shifted repeat (≈4 min later, committed gate, seed 7):** `late rc=0`, and its core manifest is byte-identical
   to the first run's (`late_vs_first_core_distinct=1`). So the generated `.doc` bytes soffice writes carry no
   wall-clock component that reaches the gate.
4. **Three concurrent gate instances (shared host, separate soffice profiles), each seed:** `conc seed=7 distinct=1`,
   `conc seed=56 distinct=1`, both `LEGS=4/4 C1=PASS`. Contention does not perturb the run.
5. **The counter's own G is not the committed file** — `c1-count.py` HARNESS rewrites `LANE` (H1) and
   `CAPTURE_TEXT = R56_ORACLE or …` (H2) before running. I rebuilt that copy in scratch (anchors matched once each;
   `wrote gates/G.py sha256=c415fce62ab46c647d2e499ddd57b91704a1898dc4b6c6af4a9af57caddde17a`) and ran **every battery
   builder** on it, 3 repeats at both seeds: `m1..m7` each `out_distinct=1 core_distinct=1` at 7 and 56, verdicts
   `m1 1/4`, `m2 1/4`, `m3 1/4`, `m4 2/4`, `m5 2/4`, `m6 3/4`, `m7 0/4`, builder `4/4 C1=PASS` (48 runs). For the builder
   the harness copy's core manifest is byte-identical to the committed gate's (`d1343e12…` at seed 7, `97d72d8c…` at 56),
   i.e. H1/H2 change the oracle path, not the behaviour. Representative lines (seed 7, harness G):
   `m1 GENOLE=FAIL S901 span is not a slice of the defined form` · `m2 …FAIL S901 char` · `m3 …FAIL S901 capture_sha256`
   · `m4 …FAIL S901 QUOTE line` · `m5 …FAIL extra or missing span files` · `m6 REFUSE=FAIL NOFORM: spans.tsv written`
   · `m7 GENOLE=FAIL rc=97 b"AUDIT_FORBIDDEN open '…/chousa-shokunin/SKILL.md'\n"`, `REFUSE=FAIL NOFORM: rc=97`.

## Realised variation — confined to the LibreOffice profile, outside every judged artifact

The full work-tree manifests do differ between repeats, in exactly five files, all under `soffice-profile/`:
```
diff man-builder-7-1.txt man-builder-7-2.txt
< … PackageRegistryBackend/backenddb.xml            (digest differs)
< … PackageRegistryBackend/configmgr.ini            (digest differs)
< … PackageRegistryBackend/lu2705479tiveo.tmp/OptionsDialog.xcu   > … lu2707509tiwog.tmp/…
< … lu2705479tivep.tmp/Filter.xcu                                  > … lu2707509tiwoh.tmp/…
< … lu2705479tiver.tmp/Paths.xcu                                   > … lu2707509tiwoj.tmp/…
```
soffice stamps its own per-run profile (temp names + registry state); `find … -path ./soffice-profile -prune` removed
exactly those five lines and made the manifests identical (`core_distinct=1`). No gate clause reads the profile, and the
`.doc`/`.xls` bytes it produced (`cache/*.raw`) are identical — so the variation is real but cannot reach a verdict.

## Why a timing jitter could not forge a kill

The only wall-clock-dependent path is a subprocess deadline (`soffice` 600 s; each leg 300 s builder / 600 s regress under
the counter's 1800 s outer timeout). A leg that times out is printed as `FAIL timeout [...]`, which matches none of the
`MARKER` reasons (`span is not a slice…`, `char`, `capture_sha256`, `QUOTE line`, `extra or missing span files`,
`spans.tsv written`, `AUDIT_FORBIDDEN`/`rc=97`, `ENV_CHANGED`) and would make a G vector differ from its baseline — both
directions lose a kill, none fabricates one. The rule is fail-safe under load; measured absent at 3-way concurrency.

## Risks / blockers

- None to this hypothesis. What the measurement cannot cover: (a) host-level `soffice` failure (missing binary, profile
  it cannot write) turns any run into `ENV_CHANGED` exit 2, a miss not a kill — the counter reports that as a shortfall,
  which is the correct direction; (b) M9's "vector equality" leg is the only rule where an anomalous-but-consistent run
  could matter, and both G and mutant sides of it reproduced identically at both seeds here; (c) `oracle-m8-unpinned.py`
  is not a `--tool` entry (`c1-count.py` runs it as G's oracle via `R56_ORACLE`), so it was not in the matrix; it is a
  static file whose digest is printed by the counter.

VERDICT: attacked R56-C1's triplicate kill rule (per-seed determinism of `c1-gate.py`) — SURVIVED: 5/5 identical runs per seed on the landed builder, m2 and m6 (stdout, rc and all 86/73 judged artifacts), plus 3/3 on all seven battery builders under the counter's harness-edited G, a time-shifted repeat and 3-way concurrency; the only realised variation is soffice's own profile directory, which no clause reads.
