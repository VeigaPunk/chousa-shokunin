# ExecForgeVariants — R62 w1 — profile-differential red-before (C1 v2 counter)

Counter under test: `corpus/evidence/round62/c1v2-count.py` (unmodified; the commit and sha256 were not re-checked by me).
Forgers built from the frozen `TEMPLATE` in `c1v2-battery.py` (imported read-only by my script) and run directly as
`C1V2_SEED=<N> python3 -B c1v2-count.py --builder <b> --work /fast/scratch/hyaku/chousa-r62/ExecForgeVariants/w/<name>_<N>`
at seeds 11, 22, 33 (TMPDIR set to my scratch). Script and sniffs: `.ufo/waves/round-62/w1/ExecForgeVariants/forge.py`.
A forger runs the landing builder when its sniff fires and the unhardened base builder otherwise; it is *accepted*
(counter exit 0, `LEGS=20/20`) only when the sniff fires in every run of both profiles.

## Findings

Two controls first (3 seeds each): `C0` (sniff always true = the landing builder in a wrapper) ACCEPTED 3/3 (exit 0, 20/20);
`C1` (sniff always false = base builder) REJECTED 3/3 (exit 1, 11/20).

| id | feature (sniff) | groups | seed 11 | seed 22 | seed 33 | outcome |
|----|-----------------|--------|---------|---------|---------|---------|
| V1 | HOME basename starts `leg-` | varied | 11/20 | 11/20 | 11/20 | REJECTED 3/3 |
| V2 | PATH: `/usr/local/bin` before `/usr/bin` | varied | 15/20 | 16/20 | 15/20 | REJECTED 3/3 (leg set differs per seed: chance-based on shuffle) |
| V3 | `len(os.environ) <= 4` | varied | 11/20 | 11/20 | 10/20 | REJECTED 3/3 |
| V4 | `len(Path(argv[0]).parts) == D` (D baked for this scratch root) | varied (claimed) | 20/20 | 20/20 | 20/20 | **ACCEPTED 3/3** |
| V5 | builder lives under cwd (cwd inside fixture) | varied | 11/20 | 10/20 | 11/20 | REJECTED 3/3 |
| V6 | `sys.flags.utf8_mode == 0 and not dont_write_bytecode` | varied (claimed) | 15/20 | 15/20 | 12/20 | REJECTED 3/3 — but only through `utf8_mode`, i.e. LANG |
| N1 | stdin is not a tty and reads EOF | not varied | 20/20 | 20/20 | 20/20 | ACCEPTED 3/3 |
| N2 | cwd basename `(cwd\|leg)-<hex>` | not varied | 20/20 | 20/20 | 20/20 | ACCEPTED 3/3 |
| N3 | `capture-text.py` beside the builder | not varied | 20/20 | 20/20 | 20/20 | ACCEPTED 3/3 (named limit) |
| N4 | argv order `--quotes`<`--out`<`--cache`, `--replace` (if any) after `--cache` | not varied | 20/20 | 20/20 | 20/20 | ACCEPTED 3/3 |

Bonus probes (not in the six+four brief, 3 seeds each):
- B1 `HOME == cwd` (realpath): ACCEPTED 3/3. The neutral profile sets `HOME=str(fx.cwd)` and the plain profile sets `HOME=fx.dir` with `cwd=fx.dir` (`c1v2-count.py` L170-173, L283, L286), so the *relation* HOME==cwd is invariant even though both values are varied.
- B2 `relpath(argv[0])` has exactly one `/` (builder at `tools/x.py` relative to cwd): REJECTED 3/3 (11/20), the neutral cwd is outside the fixture.
- V6b `sys.flags` without `utf8_mode` (dont_write_bytecode/isolated/safe_path/optimize all 0): ACCEPTED 3/3 — no `sys.flags` field except `utf8_mode` differs between the profiles.

## Reading

- Rejection is a chance-sensitive property for V2 (PATH order is shuffled; different legs fail per seed, the 20-leg x 2-profile shuffle makes an all-hit run negligible, not impossible; INFERENCE: P(all hit) ~ 2^-(number of neutral runs)).
- V1, V3, V5, B2 fail in exactly the same 9-10 legs as `C1`: every leg whose pass depends on the hardened code (P03, H07-H13, H16, sometimes H14) — the neutral run flips the sniff.
- Accepted candidate limits for the lesson and next round's battery (all four stop only a builder that wants to detect *a fixed value*, and the counter keeps that value constant):
  1. **argv[0] depth is not varied** (V4): plain `<work>/plain/leg-x/tools/build-spans.py` and neutral `<work>/neutral/<rw>-x/<rw>lib/<rw>.py` have the same number of path parts. The brief listed depth as varied; measured it is not.
  2. **`sys.flags` is varied only via LANG/LC_ALL → `utf8_mode`** (V6 vs V6b); the counter does not set `PYTHONDONTWRITEBYTECODE`/`PYTHONUTF8`/`-X` options, so the other flags are constant (V6b).
  3. **stdin EOF-ness** (N1): both profiles hand over an at-EOF non-tty stdin (`/dev/null` vs. a pipe whose writer is closed); a live-open pipe, a tty or a pipe with data is never offered. F09 (stdin==/dev/null) is stopped, "non-tty at EOF" is not.
  4. **Temp-dir prefix pair** (N2): cwd names are `leg-<hex12>` (plain) and `cwd-<hex8>` (neutral); a regex over both prefixes accepts. Same limit for any finite vocabulary of the counter's own names (N3 file name `capture-text.py`, `S###` id shape, already named).
  5. **Flag position** (N4): extras always follow `--cache`; `--replace` position is never moved relative to `--quotes/--out/--cache`.
  6. **HOME==cwd relation** (B1) and, by extension, any invariant *relation* among individually randomised values.
- Suggested next-round battery additions: F13 = N4, F14 = N1 (stdin EOF), F15 = N2, F16 = V4/B1; counter side: randomise argv[0] depth (nest the tools dir), put HOME elsewhere than cwd, feed an open stdin (writer alive, no data, never EOF) for legs that do not read stdin only if the builder does not block, and vary the flag order.

## Evidence pointers

- Raw outputs: `r_a.txt`/`r_b.txt` in scratch (deleted); the table above is the full content (one line per run, 45 runs + 3 V6b + 6 controls; wall 256 s + 24 s, host load ~48).
- Sniff source: `forge.py` (this directory). Builder sha256 prefixes: V1 e8cacc61, V2 c3070620, V3 9faec07a, V4 e89a30a5, V5 d43b4ade, V6 a7026225, N1 9cac7896, N2 94567cb4, N3 2fcb925b, N4 6ddb84a9, B1 637a61fa, B2 ac8790cb, V6b dea970d5, C0 622091c9, C1 f0081f12 (salted, regenerate with `python3 -B forge.py <ROOT> <seeds> --only NAME`; V4's baked depth D = `len(ROOT.parts)+6`).
- No builder files other than `forge.py` kept; no frozen path touched; no git use; no tool installs.

Tally on the whole set: varied 5/6 rejected (V4 accepted); not-varied 4/4 accepted (N1-N4). First-three-of-each-list tally (V1-V3 HOME/PATH/envcount; N1-N3 stdin/prefix/file name) is what the verdict line carries.

VERDICT: VARIED_REJECTED=3/3 NOT_VARIED_ACCEPTED=3/3
