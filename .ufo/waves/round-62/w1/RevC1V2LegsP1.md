# RevC1V2LegsP1 — review of legs P01 TXT, P02 DOCX, P03 NOPYC of `c1v2-count.py` (both profiles)

Axes: operability, coverage, calibration. Seat: reviewer (leaf; no subagents; no lane writes outside this report).
Integrity checked before runs: `corpus/evidence/round62/c1v2-count.py` sha256 prefix `b7016fba91b03460`, `tools/build-spans.py` prefix `c366492005ce304a` (both as the claims state); `git status` on `corpus/evidence/round62` and `tools` clean.
Runs: `C1V2_SEED=<n> python3 -B corpus/evidence/round62/c1v2-count.py --builder <b> --work <scratch>/w`, `unshare` present at `/usr/bin/unshare`. Per-leg lines quoted from the counter output. Scratch `/fast/scratch/hyaku/chousa-r62/RevC1V2LegsP1/` deleted before yield. No installs, no network.

## Findings

**F1 — tautology (P03 NOPYC passes a builder that does nothing).** `P03` checks only `tools_unchanged` (name listing) on the P02 fixture; a builder that does nothing leaves the listing equal.
- Repro: builder `import sys; sys.exit(0)` (and `sys.exit(2)`), seed 1 and seed 3:
  `LEG P01 TXT fail neutral: FAIL rc=0 | plain: FAIL rc=0` / `LEG P02 DOCX fail ...` / `LEG P03 NOPYC pass neutral: ok tools=['capture-text.py', 'yluhmu.py'] | plain: ok tools=['build-spans.py', 'capture-text.py']`.
- exit-2 stub: `LEG P03 NOPYC pass ...`, `LEGS=14/20 C1V2=FAIL`. The overall verdict still fails (P01/P02), so the battery is not fooled by this alone; the defect is that P03 is vacuous in isolation.

**F2 — false negative (P03 compares names, not bytes).** An in-place rewrite of the fixture's `tools/capture-text.py` passes every leg.
- Repro: builder appends `\n# rewritten in place by the builder\n` to `TOOLS/capture-text.py` (same name), then runs the landed builder via `runpy`: `mut/mut-tools-rewrite.py`, seed 1: all 20 legs `pass` in both profiles, `LEGS=20/20 C1V2=PASS`.
- The leg is named NOPYC; its stated check ("listing is unchanged") does not see modification of a tool file.

**F3 — false negative (P03 runs only on the DOCX fixture).** Bytecode written only on the TXT path (P01 fixture) is invisible: P03 never inspects `tools/` after a TXT build.
- Repro: builder writes `tools/__pycache__/capture-text.cpython-314.pyc` only when the cache holds no `.raw` (i.e. the P01 fixture), then runs the landed builder: `mut/mut-pyc-txt.py`, seed 1, `LEGS=20/20 C1V2=PASS`.
- Positive controls show the leg does catch DOCX-path bytecode: `mut/mut-pyc-always.py` → `LEG P03 NOPYC fail ... tools=['__pycache__', 'build-spans.py', 'capture-text.py']`; the round-61 base builder (`controls/base-build-spans.py`) → `LEG P03 NOPYC fail ... tools=['__pycache__', ...]`.

**F4 — false positive (P01, P02, P06): manifest newline.** A candidate identical to `cand-a` except the manifest uses CRLF (`"\r\n".join(...)`) fails three legs.
- Repro: `mut/cand-a-crlf.py`, seed 1: `LEG P01 TXT fail neutral: FAIL rc=0 | plain: FAIL rc=0`; `LEG P02 DOCX fail ...`; `LEG P06 REBUILD fail neutral: FAIL rc=0,0 | plain: FAIL rc=0,0`; `LEGS=16/20 C1V2=FAIL`.
- Why it is a false positive: the builder docstring specifies the manifest's header and columns and says the TSV *input* may end lines with LF, CRLF or CR; it does not fix the output line terminator. The golden (`golden()` in the counter) is LF-only and P01 compares bytes (`snap` hashes file contents). The byte-exact LF requirement is therefore unstated in the contract. [INFERENCE: a reader that splits on LF/CRLF/CR accepts both.]

**F5 — false positive (calibration, P01, P02): thread budget under the 200 MiB address-space limit.** A builder with output identical to the landed one, that first starts 32 idle threads, fails both profiles.
- Repro: `mut/threads-32.py`, seed 1: `LEG P01 TXT fail neutral: FAIL rc=1 | plain: FAIL rc=1`; `LEG P02 DOCX fail neutral: FAIL rc=1 | plain: FAIL rc=1`; `LEGS=11/20 C1V2=FAIL`.
- Direct probe (no counter): `bash -c 'ulimit -v 204800; python3 -B -c "<start 32 threads>"'` → `started 6 then RuntimeError can't start new thread`; without the limit → `started 32`. So the 200 MiB budget admits about six threads on this host (Python 3.14, 32 cores, glibc default 8 MiB stacks).
- The docstring discloses the 200 MiB limit as part of the contract, so this is a budget failure, not a wrong byte. I count it as a false positive by the item's definition and route it as a calibration limit: the verdict depends on thread count, which the leg statement does not mention.

**F6 — profile-dependent verdict (observation, not a leg defect).** The plain profile can pass a name-keyed hazard that the neutral profile catches.
- Repro: `mut/mut-hardcode-out.py` (ignores `--out`, writes to the sibling `out` of `tools/`), seed 1: `LEG P01 TXT fail neutral: FAIL rc=0 | plain: ok rc=0`; `LEG P02 DOCX fail neutral: FAIL rc=0 | plain: ok rc=0`; `LEG P06 REBUILD fail neutral: FAIL rc=0,0 | plain: ok rc=0,0`; `LEG P04 CHECK fail neutral: FAIL counter exception FileNotFoundError ... neutral/.../spans | plain: ok rc=0,0,1`.
- Because a leg passes only when both profiles pass (`results[n] = (all(oks), det)`), the plain-only pass never becomes a verdict. The neutral profile is what catches the hazard; I found no hazard among the P-legs that the neutral profile masks. [INFERENCE: random 4–8 letter names collide with fixed names with negligible probability.]

## (a) Three correct builders, run

Built from scratch in `/fast/scratch/hyaku/chousa-r62/RevC1V2LegsP1/cand/`, following the policy text of `pos-indep1..3.py` and the landed builder docstring (I did not copy and edit the 12–17 KB pos files; the policies are the docstring's). All three implement default build, `--check`, `--replace`, and the exit sets 0/1/2.

| file (sha256 prefix) | policy differences |
|---|---|
| `cand-a.py` (`1bef75aa…`) | refuses every link (capture, DIR, spans, span path, manifest); capture-text via `runpy`; temp file + `os.replace`; output guard after the rows are built |
| `cand-b.py` (`357d6278…`) | output guard first (before any capture is read); replaces links at DIR/spans, DIR/spans.tsv and span paths by rename (the target is never opened); captures read by descriptor, inside-cache links followed; capture-text via importlib with `dont_write_bytecode`; tree staged beside DIR and renamed in, manifest last |
| `cand-c.py` (`3e883596…`) | every open with `O_NOFOLLOW` / `dir_fd`; capture-text compiled from source and `exec`'d (no import); spans dir created only after the guard passes |

Results (all with `C1V2_SEED` set, full counter):
- `cand-a`, `cand-b`, `cand-c` at seeds 1, 2, 3: `LEGS=20/20 C1V2=PASS` nine times out of nine; every P01–P06 `pass` in both profiles.
- Reference pos builders: `pos-indep1` (seeds 1, 2), `pos-indep2` (seeds 1, 3), `pos-indep3` (seed 1): `LEGS=20/20 C1V2=PASS` each.
- Hence: no false positive from the three independent correct builders at the seeds run.

Other observations from the same runs (not scored):
- The landed builder: `LEGS=20/20 C1V2=PASS` at seed 1, with the P03 names `['capture-text.py', 'pxkqo.py']` (neutral) and `['build-spans.py', 'capture-text.py']` (plain).
- `pos-indep2` (seed 1) shows `H11`/`H12` as `rc=0` with the victim unchanged (healed tree); `pos-indep1` (seed 1) shows them `rc=2`. H-legs are not in this item and are not judged here.

## (b) Tautology checks

- Can a P-leg pass with the builder doing nothing? P01 and P02: no (both fail with `exit 0` and `exit 2`). P03: **yes** (F1). P04/P06 do not pass with the stubs (P04 raises a counter exception on a missing `spans`, scored FAIL).
- Can the neutral profile mask a hazard? See F6: no masking that reaches a verdict; the neutral profile is the one that catches name-keyed hazards.
- Can P03 be satisfied while bytecode or edits land in `tools/`? Yes, for F2 (in-place edit) and F3 (TXT-path bytecode).

## (c) Profile-dependent verdicts

- P01, P02, P04, P05, P06 (the out-tree legs): depend on the `out` name, the cwd and HOME. Measured flip: F6 (plain pass, neutral fail → overall FAIL).
- P03: depends on the tools directory name (`tools` in plain, random in neutral) and only on the DOCX run (F3). No flip measured.
- Address-space limit: plain fixed 200 MiB; neutral 200–224 MiB drawn at random. The neutral limit is never stricter, so a builder that fits plain fits neutral: no flip from the draw. Thread budget (F5) is the same in both profiles; it is a host/thread-count dependence, not a profile dependence.
- RLIMIT_FSIZE: neutral 384 MiB minimum against plain 512 MiB. Stricter in neutral, but P-leg outputs are a few KiB; no flip measured. [INFERENCE: a builder writing more than 384 MiB would flip.]
- stdout/stderr pipes (neutral) vs files (plain), closed-pipe stdin (neutral) vs `/dev/null` (plain), random environment keys, LANG in {C, POSIX, C.UTF-8}: no flip observed; all three candidates and the reference builders pass both profiles with these settings.

## Verification gaps

- Python builders only; one host (32 cores, Python 3.14.8); x86_64; thread budget measured only here.
- I did not run the battery, the controls or the H-legs as part of this item.
- The three candidate builders and the mutants are in scratch, deleted before yield; their hashes are above. Their source is reproducible from the descriptions in this report, not stored in the lane (the item does not ask for candidate files).

Recommended routing (not edits; the counter is frozen): F1–F3 as P03 limits with a named P03 supplement (byte-compare `tools/` against a snapshot; run the NOPYC check on the TXT run too); F4 as a spec gap (state the output line terminator in the builder docstring, or compare manifests after newline normalisation in the next round's counter); F5 as a named calibration limit (thread count under the 200 MiB cap).

VERDICT: LEG_DEFECTS=5 false_positive=2 tautology=3 legs=P01 TXT, P02 DOCX, P03 NOPYC
