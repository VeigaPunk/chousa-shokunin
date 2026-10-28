# MutC1ExtraWrite — mutation test of the C1 reference builder's output path (round 61, w1)

Scope: 15 new mutants of `corpus/evidence/round61/controls/ref-build-spans.py` aimed at `guard_out`,
`_atomic_write`, `write_out`. Frozen 14 (M01–M14) not re-run. Counter `c1-count.py` run unchanged, seed 61001.
Reference sha256 prefix `86d64c31` (matches the claim). Lane files read only.

## Findings

- Counter kills 3/15. 12 survive. Of the 12: 2 equivalent (N01, N02), 10 coverage gaps.
- Every gap sits in one of two blind spots of the 20 legs:
  (a) no leg forces an `OSError` inside `write_out` after the guard has passed. H16 is refused by
  `guard_out` before any write, so the write-failure path is never run; (b) the counter never reads
  output file modes, and no leg tests a foreign file that collides with a builder-chosen name or a
  manifest that differs from the golden one only by whitespace.
- Two of the gaps are safety-relevant, not cosmetic: N10 (a symlink orphan is unlinked under
  `--replace`, which the reference refuses) and N15 (a foreign `spans.tsv` is overwritten without
  `--replace`). N07, N08 and N09 leave an inconsistent or lost state after a failed build.
- Reference passes the frozen counter at seed 61001 (`LEGS=20/20 C1=PASS`, rc 0). The probe fixtures
  below were run on the reference only as the expected-behaviour baseline (rc and tree), not through the counter.

## Table (counter: `python3 -B c1-count.py --builder <mut>.py --work <absent dir> --seed 61001`)

Mutants are string-anchored edits (each anchor asserted to occur exactly once) of the frozen reference,
written to a scratch copy. Output lines from the counter's `LEG` rows; `failing` = legs with `fail`.

| id | edit | legs failed | counter | class |
|---|---|---|---|---|
| REF | none (frozen reference) | none | LEGS=20/20 C1=PASS, rc 0 | baseline |
| N01 | `_atomic_write`: drop `O_NOFOLLOW` | - | SURVIVED | equivalent (see E1) |
| N02 | `_atomic_write`: drop `O_EXCL` | - | SURVIVED | equivalent in practice (see E2) |
| N03 | `_atomic_write`: mode `0o644` -> `0o666` | - | SURVIVED | gap G1 |
| N04 | `_atomic_write`: mode `0o644` -> `0o600` | - | SURVIVED | gap G1 |
| N05 | tmp name `.{name}.{hex}.tmp` -> `{name}.tmp` | - | SURVIVED | gap G2 |
| N06 | `_atomic_write`: no `os.unlink(tmp)` on failure | - | SURVIVED | gap G3 |
| N07 | `_atomic_write`: `raise` -> `return` (error swallowed) | - | SURVIVED | gap G3 |
| N08 | `write_out`: `spans.tsv` written before span files | - | SURVIVED | gap G3 |
| N09 | `write_out`: orphans unlinked before writes | - | SURVIVED | gap G3 |
| N10 | `guard_out`: orphan symlink not refused (`if p.is_symlink() and f"spans/{p.name}" in files`) | - | SURVIVED | gap G4 |
| N11 | `write_out`: `except OSError` -> `except ZeroDivisionError` | - | SURVIVED | gap G3 |
| N12 | `guard_out`: `if (differs or orphans) and not replace` -> `if differs and not replace` | H09 ORPHAN | KILLED | — |
| N13 | `write_out`: `mkdir(parents=True, ...)` -> `mkdir(...)` | P01, P02, P04, P06 | KILLED | — |
| N14 | `guard_out`: `differs = m.is_file()` (no content compare) | P06 REBUILD | KILLED | — |
| N15 | `guard_out`: compare `read_bytes().rstrip() != manifest.rstrip()` | - | SURVIVED | gap G4 |

Counter totals: `KILLED=3/15`, `SURVIVED=12`. Raw counter output: `LEGS=19/20` for N12, `LEGS=16/20` for N13,
`LEGS=19/20` for N14; `LEGS=20/20` for the 12 survivors (exit 0 each).

## Survivors: equivalent or gap, with the smallest killing fixture

Fixture base for all probes: one `.txt` capture holding one quote, one row (id `S101`), `tools/` holding the
builder and the lane's `capture-text.py`, `--cache` pointing at the capture directory. Each probe ran the
reference and the mutant on the same fixture. Probes were my own runs (not counter legs); "kill" means
the reference and the mutant disagree on that fixture.

- **E1 (N01) equivalent by construction.** `os.open(symlink, O_WRONLY|O_CREAT|O_EXCL)` raises
  `FileExistsError` (errno 17); the reference with `O_NOFOLLOW` raises the same. `O_EXCL` alone refuses
  a symlink at the final component. Observed in a scratch check.
- **E2 (N02) equivalent in practice, not by construction.** Without `O_EXCL` the open only differs if the
  48-bit random tmp name already exists as a regular file. Observed: the reference raises `FileExistsError`
  on that file; N02 writes `NEW` over `EXISTING` at offset 0 (no `O_TRUNC`) and leaves `NEWISTING`. That
  case needs the token to be predicted, so no black-box fixture reaches it. Equivalent for the counter.
- **G1 (N03, N04) mode unobserved.** Fixture: one clean build, then `stat` of `out/spans.tsv` and
  `out/spans/S101-1.txt`. umask 022: REF `0o644`, N03 `0o644` (no difference, equivalent at this umask),
  N04 `0o600` (difference). umask 000: REF `0o644`, N03 `0o666` (difference), N04 `0o600`.
  The counter's `snap()` compares content digests and symlink targets, never `st_mode`.
- **G2 (N05) fixed tmp name collides with a foreign file.** Fixture D: `out/spans.tsv.tmp` created as a
  foreign regular file ("FOREIGN"), then the build. REF: rc 0, golden tree built, foreign file kept.
  N05: rc 2, nothing built (`O_EXCL` on the fixed name fails). No counter leg puts a foreign file
  at a builder-chosen tmp name.
- **G3 (N06, N07, N08, N09, N11) write-failure path never run.** Fixture A (smallest): as the base, plus a
  directory at `out/spans/S101-1.txt` so the first span write fails with `IsADirectoryError`.
  REF: rc 2, no `Traceback`, no `.tmp` residue, no `spans.tsv`. Mutant results:
  - N06: rc 2, residue `spans/.S101-1.txt.eb2d74b55448.tmp` left behind.
  - N07: rc 0, `spans.tsv` written, span file missing (silent partial success).
  - N08: rc 2, `spans.tsv` present after the failed build (manifest without span files).
  - N11: rc 1, `Traceback ... IsADirectoryError` on stderr (rc 2 expected).
  Fixture B (orphan plus blocker, `--replace`): REF rc 2 with orphan `spans/S404-9.txt` kept; N09 rc 2 with
  the orphan already deleted (data lost by a failed build).
  Counter reach: `leg_h16` is refused in `guard_out` before `write_out`'s `try` (`out` is a regular file,
  guard returns 2), and no other leg makes a write fail. Hence the write path has no leg.
- **G4 (N10, N15) guard refusal bypassed, not exercised by any leg.**
  - N10, fixture C2: `out/spans/S999-1.txt` is a symlink to a victim file, `--replace`. REF: rc 2, link kept,
    victim intact (the reference refuses a symlink orphan even under `--replace`). N10: rc 0, link removed,
    victim intact. Without `--replace` (fixture C1) both refuse with rc 2, which is why `H09` (a regular-file
    orphan) and the counter miss it.
  - N15, fixture E: a successful build, then one `\n` appended to `spans.tsv`, no `--replace`. REF: rc 2, file
    unchanged. N15: rc 0, file rewritten to the golden manifest.

## Limits of this run

- One seed only (61001), as the seat asked. No frozen-14 re-run; no edits to any frozen file; no
  mutant or probe file is kept (scratch deleted before yield).
- The probes are my own fixtures. They show a reference-versus-mutant divergence on a single fixture each; they
  do not add a counter leg, and the frozen predicate forbids that change here. A candidate counter leg would be
  a counter limit under the claim's kill rule (routed, not a refutation of C1).
- The C1 claim (`LEGS=20/20` on the landed builder) is not put in question by any survivor, because every
  survivor is a behaviour the 20 legs do not measure. INFERENCE: the landed builder, if it matches the reference
  on these probes, would also pass the frozen counter.

## Install / environment record

No installs or updates (Python 3.14.8 in use, `python3 -B` for every script). No git, jj or index
mutation; no lane writes except this report. Scratch: `/fast/scratch/hyaku/chousa-r61/MutC1ExtraWrite/`
(mutants under `mut/`, probes under `probe/`), removed before yield.

VERDICT: KILLED=3/15 survivors_that_are_gaps=10
