# Round 61 · w1 · MutC1ExtraMain — mutation probe of the C1 reference builder

Scope: 23 new mutants (N01–N23) of `corpus/evidence/round61/controls/ref-build-spans.py`, beyond the frozen M01–M14. Aimed at `read_quotes`, `build`, `check`, `main`, exit codes 1 vs 2, `--check` read errors, partial writes after refusal, the `span == quote` refusal, and memo reuse. Each mutant was scored with the frozen counter at seed 61001:
`python3 -B corpus/evidence/round61/c1-count.py --builder <mutant> --work <scratch>/w/<name> --seed 61001` (TMPDIR = scratch). Frozen predicates, counter, controls and lane were not edited; the only lane write is this report.

Baseline (reference, unmodified, sha256 `86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd`): `LEGS=20/20 C1=PASS`, rc 0.

## Findings

1. **Counter kills 9/23.** All nine are caught by legs that the frozen predicate names (H19, P05, H09, P01, P02, P04, P06, H07, H08, H16 and the large-file legs).
2. **14 survive.** Of these, 10 are coverage gaps (the 20 legs never exercise the mutated behaviour), 2 are equivalent (N10, N23), 1 is accepted by design by the H11 disjunction (N20), and 1 is outside the counter's stated scope (N22: stdout is never read, QUALITY 117).
3. **Two safety-relevant gaps.** N02: an id such as `../../v` writes `v-1.txt` outside the output directory; no leg sends a non-`S###` id. N21: when a span path is blocked, the manifest is written without its span files, which contradicts the builder docstring's "a failed run never leaves a manifest without its spans"; no leg injects a mid-write failure.
4. **Exit-code and read-error gaps.** N12 (`--check` on a non-UTF-8 manifest: reference rc 2, mutant rc 1 with a traceback), N16 (missing cache: rc 2 vs 1), N17 (missing input: rc 2 vs 1). No leg covers these.
5. **Consequence for C1.** The frozen 20/20 shows the 20 named hazards reach the builder. It does not measure header validation, id validation, url-conflict, quote-count, `--check` orphan detection, manifest-read errors, or write-order under failure. INFERENCE: the landed `tools/build-spans.py` carries the same `ID_RE` guard (lines 46, 112) and the same write order as the reference, so N02 and N21 apply to it by identical code. I did not mutate the landed file.
6. Routing: per the frozen kill rule, these are counter limits to route, not refutations of C1 as frozen. I did not edit the counter.
7. Self-correction: my first N07 build dropped the function's final `return`, so it failed all 20 legs for the wrong reason. I rebuilt it with the anchor fixed and reran; the table below reports the corrected run only. No other mutant was rerun.

## Table (counter seed 61001; reference 20/20)

| # | edit on the reference | legs failed | verdict | class of survivor |
|---|---|---|---|---|
| N01 | `read_quotes`: header check removed | – | SURVIVED | gap (input validation) |
| N02 | `read_quotes`: `ID_RE` check disabled | – | SURVIVED | gap, safety (path escape) |
| N03 | `read_quotes`: same-id/different-url check disabled | – | SURVIVED | gap (correctness) |
| N04 | `read_quotes`: bad rows printed, no exit 2 | H19 | KILLED | – |
| N05 | `build`: `n != 1` → `n == 0` (ambiguous quote accepted) | – | SURVIVED | gap (correctness) |
| N06 | `build`: `span == quote` refusal removed | – | SURVIVED | gap (correctness) |
| N07 | `build`: refusal returns, `main` exits 0 (corrected) | P05, H13, H14, H15, H17, H18, H20 | KILLED | – |
| N08 | `build`/`main`: refused rows still written, exit 1 (partial write after refusal) | P05, H14, H15, H17, H18, H20 | KILLED | – |
| N09 | `Forms.get`: memo returns the first url's result for any url | P01, P02, P04, P06, H07, H08, H09, H16 | KILLED | – |
| N10 | `Forms.get`: memo lookup disabled | – | SURVIVED | equivalent (same output, see F10) |
| N11 | `build`: span end `+CONTEXT` → `+CONTEXT-1` | P01, P02, P06, H08 | KILLED | – |
| N12 | `check`: manifest read error no longer caught (traceback, rc 1) | – | SURVIVED | gap (`--check` read error, exit code) |
| N13 | `check`: span-file byte comparison removed | P04 | KILLED | – |
| N14 | `check`: orphan span detection disabled | – | SURVIVED | gap (`--check`) |
| N15 | `check`: always returns 0 | P04 | KILLED | – |
| N16 | `main`: missing cache exits 1, not 2 | – | SURVIVED | gap (exit code) |
| N17 | `read_quotes`: missing input exits 1, not 2 | – | SURVIVED | gap (exit code) |
| N18 | `main`: `write_out` return code ignored | H07, H09, H10, H11, H12, H16 | KILLED | – |
| N19 | `guard_out`: orphan files allowed without `--replace` | H09 | KILLED | – |
| N20 | `guard_out`: span-file symlink guard removed | – | SURVIVED | predicate-accepted (H11 allows "healed") |
| N21 | `write_out`: manifest written before span files | – | SURVIVED | gap, safety-adjacent (manifest without spans) |
| N22 | `main`: QUOTE line prints span start, not char N | – | SURVIVED | outside predicate (stdout unread, QUALITY 117) |
| N23 | `_atomic_write`: `O_EXCL \| O_NOFOLLOW` removed | – | SURVIVED | equivalent under the counter threat model (INFERENCE, not run) |

Non-duplicates: N19 differs from frozen M09 (which disables the whole guard); N13 differs from frozen M05 (which also swaps the write).

## Smallest fixtures for the survivors (run directly, reference vs mutant)

Each fixture is one row unless noted. Commands were `python3 -B <builder> --quotes q.tsv --out out --cache cache` with a `.txt` capture as the source.

- **N01** header `id url quote bogus`: REF `rc=2` ("header must be id url quote entry"); MUT `rc=0`, writes `spans.tsv` and `S101-1.txt`.
- **N02** id `../../v`: REF `rc=2` ("id '../../v' is not S###"); MUT `rc=0`, writes `fx/N02/v-1.txt`, outside `out/`.
- **N03** `S101` on two urls: REF `rc=2` ("names ... earlier rows name ..."); MUT `rc=0`, writes `S101-1.txt` and `S101-2.txt`.
- **N05** quote occurring twice in the capture: REF `rc=1` ("occurs 2x"); MUT `rc=0`.
- **N06** capture text exactly `alpha beta gamma`, quote the same: REF `rc=1` ("holds no context"); MUT `rc=0`, writes a span equal to the quote.
- **N12** `out/spans.tsv` = bytes `ff fe 20 6a 75 6e 6b 0a`, then `--check`: REF `rc=2` ("cannot read"); MUT `rc=1` with `UnicodeDecodeError` traceback.
- **N14** golden tree from a clean build plus `out/spans/S404-9.txt`, then `--check`: REF `rc=1`, `SPANS_FILE_ORPHAN spans/S404-9.txt STALE=1`; MUT `rc=0`, `STALE=0`.
- **N16** `--cache` pointing at a missing directory: REF `rc=2`; MUT `rc=1`.
- **N17** `--quotes` pointing at a missing file: REF `rc=2`; MUT `rc=1`.
- **N21** `out/spans/S101-1.txt` is a directory: REF `rc=2`, no `spans.tsv` written; MUT `rc=2` with `out/spans.tsv` written and `S101-1.txt` absent (manifest without its span).
- **N22** quote at offset 142: REF prints `QUOTE S101 char 142`; MUT prints `char 62`.
- **N20** `out/spans/S101-1.txt` is a symlink to `victim.txt`: REF `rc=2` (refused, "is a symlink"); MUT `rc=0`, replaces the link with a regular file, victim bytes unchanged. Counter H11 passes this (its rule accepts a refusal or a healed tree).

## Equivalence checks

- **N10 (memo disabled):** on a two-row, one-url fixture, reference and mutant gave byte-identical stdout, stderr and rc 0. Equivalent in output.
- **N23 (`O_EXCL | O_NOFOLLOW` removed):** not run. INFERENCE: the temp name carries 48 random bits from `secrets.token_hex(6)`, so no leg can pre-create it; the flags are defence in depth, not reachable by the counter's inputs.

## Suggested counter legs (not applied; the counter is frozen)

- H21 ID-ESCAPE: id `../../v` → exit 2, nothing written outside DIR (N02).
- H22 SPAN-BLOCKED: a directory at a span path → exit ≠ 0 and no manifest (N21).
- H23 CHECK-BADMANIFEST and H24 ORPHAN-CHECK: `--check` on a non-UTF-8 manifest, and on an extra span file (N12, N14).
- H25 UNIQUE/CONTEXT: quote occurring twice, and a form equal to the quote (N05, N06).
- H26 EXIT-CODES: missing cache and missing input → exit 2 (N16, N17).

## Installs / updates

None. The probe used the host's Python 3 and the lane's frozen counter.

## Evidence pointers

- Reference: `LEGS=20/20 C1=PASS`; `BUILDER sha256=86d64c31...eccfd`, seed 61001, rc 0.
- Counter runs for N01–N23: the table above. Logs were in my scratch and are deleted; the rows are reproducible from the command above.
- Fixture comparisons: direct runs of the reference and each mutant CLI, output quoted in the list above.

VERDICT: KILLED=9/23 survivors_that_are_gaps=10
