# RevC1LegsH4 — review of C1 legs H16–H20 (reviewer)

Scope: `corpus/evidence/round61/c1-count.py` legs H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT,
H20 BIGFORM, read against predicate R61-C1 in `corpus/evidence/round61/claims.md` (sha256 9afec8d4…).
Counter and reference were not edited; nothing under `corpus/evidence/round61/`, `tools/`, `corpus/`,
`SKILL.md` was written. Scratch `/fast/scratch/hyaku/chousa-r61/RevC1LegsH4/` deleted (verified absent).
No installs. No git writes. No network.

## Findings

### D1 — FALSE POSITIVE: H16 reads only the first 64 KiB of stderr (counter lines 267-268, 501)
- `run()` reads stderr with `fh.read(65536)` (line 268); H16 tests `"Traceback" not in r["stderr"]` (line 501).
- Builder `i1` (reference + 3-line guard: if `--out` is a file, write 70 KiB of `x` then
  `\nTraceback (most recent call last):` to stderr, exit 2). Direct run on a file `--out`:
  `rc=2`, stderr 71729 bytes, `Traceback` at byte offset 71681 (`grep -b -o`).
- Counter: `LEG H16 OUTFILE pass rc=2 traceback=False` (seeds 61001 and 61002, `out/i1-*.txt`),
  `LEGS=20/20 C1=PASS`. The builder emits a traceback and the leg passes.
- Violates H16's own stated criterion ("no `Traceback` on stderr"). Counter defect.

### D2 — FALSE POSITIVE: "nothing written" checks only `--out`, not the fixture tree (lines 278-284, 533-540)
- `clean_out(fx)` (278-284) snapshots `fx.out` only. H17 (515), H18 (530), H19 (540), H20 (562) all
  use it. The predicate (lines 7-8) says the builder "leaves the file tree as each leg states".
- Builder `i3` (reference + on the `read_quotes` refusal path, rewrites every `cache/*.txt`).
- Direct H19-shaped run (`probe`, quote row entry `../abc`): `rc 2 out_exists False cache_changed True
  H19 clean_out True`.
- Counter: `LEG H19 ENTRYDOT pass rc=2` (seeds 61001 and 61002, `out/i3-*.txt`) → PASS.
- Counter defect: a refused run mutates the input capture and the leg still passes.

### D3 — FALSE NEGATIVE: H16 token search rejects a correct refusal (line 501; docstring lines 7-9)
- Builder `c4` (reference + `_refuse` message `... (Traceback-free refusal)`): rc 2, no traceback, `--out`
  untouched. Correct under H16's wording.
- Counter: `LEG H16 OUTFILE fail rc=2 traceback=True` (seeds 61001 and 61002, `out/c4-*.txt`);
  `LEGS=19/20 C1=FAIL`.
- Substring search contradicts the predicate sentence (lines 7-9: verdict "from the child's exit code, its
  file tree and its peak RSS only"). H16 and H17 (line 515) search stderr. Suggested repair for L1: a
  line-anchored test (`re.search(r"^Traceback \(most recent call last\)", stderr, re.M)` over the full stream)
  — it passes `c4` and still fails `i1` once D1 is fixed. INFERENCE: not run.

## Counter limits (not counted as leg defects; route per claims "counter limit, not a refutation")

- L1 H19 checks only a leading `../` (builder `i2`: line 176 `entry.startswith("../")`). `LEG H19 pass rc=2`
  (seeds 61001 and 61002). The leg's stated hazard is `../x`, so `i2` meets it; `corpus/../../x` escapes
  and no leg covers it. Entry-escape class sampled at one shape.
- L2 H18 accepts a read of the FIFO (builder `i4`: `_probe` treats FIFO as size 0; `_read` uses
  `os.read` with `O_NONBLOCK`, which returns EOF on a writerless FIFO). `LEG H18 pass rc=1`; the refusal is
  "quote occurs 0x" (direct run, stderr). The leg sees exit, timeout and tree only, so a read is invisible.
  INFERENCE (not run): with a writer supplying the quote, `i4` would emit a row.
- L3 H20 has no memory bound: line 562 is `rc != 0 and not timeout and clean_out`; RSS appears only in the
  detail string. Builder `i5` holds a 600 MiB bytes object before refusing: `rss_kib=764496`,
  `LEG H20 BIGFORM pass` (seeds 61001 and 61002). The reference's 221 MB is reported, not judged.
- L4 Exit code for an invalid input row is undefined by the builder's own table. Reference docstring line 28
  says "any refusal ... exits 1"; line 44 says "2 usage/env or an output refusal"; H19 pins 2 (line 540).
  Builder `c5` (bad-entry exit 1) fails only H19: `LEG H19 ENTRYDOT fail rc=1` (seeds 61001 and 61002).
  Not counted: an L1 decision on whether an entry error is "usage" (2) or a "refused row" (1). The docstring
  and the leg should say which.

## Calibration

- The always-exit-2 stub passes all five legs. `controls/c1-controls.txt` line 3: `always2 ... legs=14/20
  failing=P01,P02,P04,P05,P06,H08` — H16–H20 pass. H16–H20 discriminate only in combination with P-legs.
- In-set exit variants pass 20/20 at both seeds: `c1` (H17 and H18 → exit 2; H20 → exit 3), `LEGS=20/20
  C1=PASS` (`out/c1-61001.txt`, `out/c1-61002.txt`). `c2` (out-type guard moved before the quote table, plus an
  exception catch-all) `LEGS=20/20` (`out/c2-*.txt`). `c3` (open-time probe, `O_NONBLOCK|O_NOFOLLOW`, `fstat`)
  `LEGS=20/20` (`out/c3-*.txt`). So the H17/H18/H20 exit sets are not over-tight.
- `i1` and `i3` produce a passing C1 at both seeds (`LEGS=20/20 C1=PASS`), i.e. the counter as frozen would
  certify a builder that violates H16 and mutates the fixture tree.

## Method (commands run; all from the lane via absolute paths, `python3 -B`)

    python3 -B corpus/evidence/round61/c1-count.py --builder <variant> --work /fast/scratch/hyaku/chousa-r61/RevC1LegsH4/w/<name>-<seed> --seed {61001,61002}
    (ten variants × two seeds, run in parallel; each run exit recorded in out/<name>-<seed>.txt)
    python3 -B probe.py <variant>   (imports counter read-only; direct H16/H18/H19 fixture runs)
    python3 -B bld/i1.py --quotes /dev/null --out <file> --cache <dir>  (byte offset of Traceback)

Variant edits (from reference, lines of `controls/ref-build-spans.py`; all staged in scratch, now deleted):
- c1: line 213 `sys.exit(3 if any("over the" in r ...) else 2 if any("unreadable"/"not a regular" ...) else 1)`
- c2: insert after 321 out-type guard (`_refuse`); replace 339-340 with try/except → exit 2.
- c3: replace `_probe` 92-105 with `os.open(O_RDONLY|O_NONBLOCK|O_NOFOLLOW)` + `fstat`.
- c4: line 251 message appends `(Traceback-free refusal)`.
- c5: line 183 `sys.exit(2)` → `sys.exit(1)`.
- i1: insert after 321 `if os.path.isfile(out): stderr junk 70 KiB + "Traceback" line; return 2`.
- i2: line 176 → `entry.startswith("/") or entry.startswith("../")`.
- i3: wrap line 325 `read_quotes` in try/except SystemExit that rewrites `cache/*.txt`, re-raise.
- i4: `_probe` FIFO → ok 0 (line 103); `_read` reads with `O_NONBLOCK` (line 143).
- i5: insert after 150 `_ballast = b"x" * (600 << 20)`.
All ten parse (`ast.parse`). Reference: `controls/c1-reference.txt` 20/20 both seeds (unchanged).

## Result table (seeds 61001 / 61002, my legs only; full run = 20 legs each)

| builder | class | H16 | H17 | H18 | H19 | H20 | C1 |
|---|---|---|---|---|---|---|---|
| c1 exit-code variants | correct | pass | pass | pass | pass | pass | 20/20 both |
| c2 guard order + catch-all | correct | pass | pass | pass | pass | pass | 20/20 both |
| c3 open-time probe | correct | pass | pass | pass | pass | pass | 20/20 both |
| c4 "Traceback-free" msg | correct | **FAIL** | pass | pass | pass | pass | 19/20 both |
| c5 bad entry exit 1 | disputed (L4) | pass | pass | pass | **FAIL** | pass | 19/20 both |
| i1 traceback past 64 KiB | incorrect | **pass** | pass | pass | pass | pass | 20/20 both |
| i2 entry `../` only | limit (L1) | pass | pass | pass | pass | pass | 20/20 both |
| i3 mutate cache on refusal | incorrect | pass | pass | pass | **pass** | pass | 20/20 both |
| i4 read FIFO as empty | limit (L2) | pass | pass | **pass** | pass | pass | 20/20 both |
| i5 600 MiB then refuse | limit (L3) | pass | pass | pass | pass | pass | 20/20 both |

Counted: false_negative = 1 (c4), false_positive = 2 (i1, i3). c5 not counted (L4). i2, i4, i5 not counted (limits).

## Verdict basis

- Operability: the two counted false positives (D1, D2) are reproducible with one command each; the counter
  certifies a builder that prints a traceback or mutates its input.
- Depth: the stderr token rule conflicts with the predicate sentence (D3); the leg scope is narrower than the
  builder's contract (L1–L3).
- Calibration: H16–H20 are passed by the exit-2 stub; they add no weight alone.

VERDICT: LEG_DEFECTS=3 false_negative=1 false_positive=2 legs=H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT, H20 BIGFORM
