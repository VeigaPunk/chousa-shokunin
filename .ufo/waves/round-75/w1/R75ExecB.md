# R75ExecB — independent re-derivation of loader-matrix-v2 case expectations

Lane: chousa round 75, wave 1, seat R75ExecB (leaf executor). Scope: re-derive the twelve case
expectations of `corpus/evidence/round75/loader-matrix-v2.py` from the frozen r74 successor
counter's documented contract only, run the matrix against both counters, diff derived vs printed,
flag un-derivable or diff-only-decided expectations. Frozen revision confirmed in place.

## Environment / provenance

- Repo HEAD at start: `43a7a0db52c8aabdf32735f58e09610e05200e79` — exactly the frozen revision.
- sha256 `loader-matrix-v2.py` = `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7`
  (matches the sha declared in round75 claims C1). sha256 `round74/correction-count.py` =
  `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`; sha256
  `round73/c2-count.py` = `e6e22b1ec8d270171cf015d44cac3d544a61bd23a3fa67d14c91fa26585dc320`.
- python3 3.14.8, git 2.56.0 (pre-existing). Tooling authorization used: none — nothing
  installed or upgraded; pacman untouched (host guard respected).

## Method

Derivation made from `round74/correction-count.py`'s docstring (C2-1..C2-7), `check()`,
`anchored_count()` (exact-line, rstrip), `section()` (LAST exact heading → next `## `/EOF),
and `load()` (`git show rev:path`; numstat **column 2 = deletions** for C2-6; `--name-only`
over the two receipts for C2-7), plus the matrix's FILES dict read for fixture identity only —
the CASES table's expected columns were not consulted before the runs. Full per-case
derivation: `R75ExecB/derived-expectations.md`.

## Commands run (all from fleet-root cwd, absolute paths)

1. `mkdir -p /fast/scratch/hyaku/chousa-r75/R75ExecB/successor /fast/scratch/hyaku/chousa-r75/R75ExecB/r73 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-75/w1/R75ExecB` → `MKDIR_OK`, exit 0.
2. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD` (plus `sha256sum` of the three instruments, `python3 --version`, `git --version`) → exit 0, values above.
3. `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/correction-count.py --work /fast/scratch/hyaku/chousa-r75/R75ExecB/successor` → `LOADER_MATRIX=12/12 MATRIX=PASS`, **exit 0** (SEED=12171713789843709483).
4. `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round73/c2-count.py --work /fast/scratch/hyaku/chousa-r75/R75ExecB/r73` → `LOADER_MATRIX=3/12 MATRIX=FAIL`, **exit 1** (SEED=15724724988202262519) — matches the committed negative control `controls/negative-r73-counter-on-v2.txt` (3/12 exit 1).
5. `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-75/w1/R75ExecB/diff-derived-vs-printed.py <run-successor.log> <run-r73.log>` → **exit 0**, `DERIVED_VS_PRINTED=ALL MATCH (no expectation decided by the diff alone)` (two earlier invocations exit 1 were my own script's bugs — an f-string syntax error, then parsing the printed token `none` as a literal set member — both fixed in place before the recorded run; the matrix instruments were never touched).
6. `rm -rf -- /fast/scratch/hyaku/chousa-r75/R75ExecB && test ! -e …` → `SCRATCH_REMOVED`, exit 0.

Fixture-guard notes: the matrix itself asserts `git rev-parse --show-toplevel` equals its
TemporaryDirectory root before any commit (raises `fixture root mismatch` otherwise); all
commits use per-command `-c user.name=fixture -c user.email=fixture@invalid` inside the
fixture only. Both runs left the work dirs empty (TemporaryDirectory cleanup); scratch root
then removed and verified absent.

## Result — derived vs printed (24/24 MATCH)

| case | derived (rc, failed) | printed | successor actual | r73 actual |
|---|---|---|---|---|
| unchanged | 0, {} | 0, none | PASS | PASS |
| append-0/1/2 | 0, {} | 0, none | PASS | FAIL (spurious C2-6) |
| delete-0/1/2 | 1, {C2-6} | 1, C2-6 | PASS | FAIL (passes 7/7 — missed deletion) |
| replace-equal | 1, {C2-6} | 1, C2-6 | PASS | PASS |
| receipt-change | 1, {C2-7} | 1, C2-7 | PASS | PASS |
| dup-log-heading | 1, {C2-1,C2-2} | 1, C2-1,C2-2 | PASS | FAIL (extra C2-6) |
| dup-lesson-heading | 1, {C2-3,C2-5} | 1, C2-3,C2-5 | PASS | FAIL (extra C2-6) |
| dup-card-heading | 1, {C2-4} | 1, C2-4 | PASS | FAIL (extra C2-6) |

## Flags (the two assigned questions)

- **Cases whose expectation is NOT derivable from the frozen contract: none.** All twelve
  printed `expected_rc`/`expected_failed` pairs equal values derived before any run from the
  r74 counter's documented checks. The contract's fixed output shape (always exactly 7 CHECK
  lines, `C2=` token following the all-pass state) also pins the matrix's remaining ok-predicate
  terms; nothing in the expectations is matrix-internal choice.
- **Cases whose expectation is decided by the diff (observed run) alone: none.** Distinction
  kept explicit: five case verdicts (unchanged, append-*, delete-*, replace-equal,
  receipt-change) are also decidable by a diff-only *counter*, but their *expectations* are
  contract-derived; the three dup-* cases are counter-decidable only from protected-file
  content, and their expectations were still derived statically. Expectation provenance and
  counter decidability are independent axes; both are clean.

## Bonus characterization (grounded in sources read this session)

The r73 counter's 3/12 has a single mechanical cause: its `load()` reads numstat column
`parts[0]` (added lines) as the removal count, where the r74 successor reads `parts[1]`
(deletions, with non-digit→1 fallback). Hence appends/dup-* are falsely accused by C2-6
(added counted as removed) and true deletions slip through (added=0). replace-equal passes by
coincidence (1==1). One defect, nine case failures.

## Retained evidence (all under `.ufo/waves/round-75/w1/R75ExecB/`)

- `run-successor.log` — full matrix stdout, successor run (12/12 PASS, seed, COUNTER_SHA256).
- `run-r73.log` — full matrix stdout incl. per-case CHECK blocks, r73 run (3/12 FAIL).
- `derived-expectations.md` — per-case contract-based derivation and flag discussion.
- `diff-derived-vs-printed.py` + `diff-output.txt` — mechanical diff (final run exit 0, 24/24 MATCH).
- This report: `.ufo/waves/round-75/w1/R75ExecB.md`.

## Risks / limits

- Expectations are matrix constants, so the derived-vs-printed diff is seed-independent; the
  case-order seeds above are per-run (`secrets.randbits(64)`), single run per counter as assigned.
- My derivation is static analysis of frozen bytes at the frozen revision; no judgment is made
  about C1/C2 claims themselves (that belongs to L1/other seats).
- No blockers. No lane or fleet mutations; only my output dir and (now removed) scratch were written.
