# Seat R76ExecA — C1 both directions reproduced from committed bytes (round 76, wave 1)

Date: 2026-11-04 · Lane: chousa · Seat: R76ExecA (leaf executor) · Godspeed: yes
Scope: reproduce C1's two directions for `corpus/evidence/round76/claims.md` and report. No instrument edited, no lane mutation, no installs.

## 0. Frozen-byte fidelity (fail-closed precheck)

- Lane repo clean reads only; `git rev-parse HEAD` = `5eeca32ba9ad80081d19906c7cb52dff35891e8c`; `da9ac7ec684fe9fe9ad5554cab6180057255b76b` (controls commit named in claims.md) `merge-base --is-ancestor HEAD` → yes.
- Worktree vs `git cat-file blob da9ac7ec:…` sha256, all equal:
  - `loader-matrix-v3.py` = `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` (matches claims.md)
  - `matrix-battery-v3.py` = `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360` (matches claims.md)
  - round75 `loader-matrix-v2.py` = `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7` (matches claims.md)
- Subject digests printed by my runs (`9334721a5e7a4080`, `909987ce9f762398`, … all 13) are identical to the digests in the frozen receipts `controls/after-battery-v3-matrix.txt` / `before-battery-v2-matrix.txt`, so the positives and forgers are byte-identical to what the controls measured.
- Environment: Python 3.14.8, git 2.56.0. No tool installed or upgraded (none needed); pacman guard respected (no pacman transactions).

## 1. Direction A (after): r76 battery over r76 matrix

Command (exit 0, 2 runs, default matrix timeout 300 s; child bound 3 s via `LOADER_MATRIX_CHILD_TIMEOUT`):

```
python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work /fast/scratch/hyaku/chousa-r76/R76ExecA/a-v3
```

Exact tail: `forgers_rejected=11/11 positive=2/2` then

```
BATTERY=PASS forgers_rejected=11/11 positive=2/2
```

This is byte-for-byte the C1 predicate sentence in claims.md. Exit code 0. stderr empty.

Positive controls accepted: `successor-counter` (r74 `correction-count.py`) 12/12/PASS on both runs; `ref-counter` (r75 independent implementation) 12/12/PASS on both runs.

Forgers accepted by this matrix: **none** — all 11 REJECTED on both runs, exit 1, marks < 12: `constant-pass` 4/12, `constant-fail` 4/12, `order-twelve` 2/12 then 1/12, `diff-only` 9/12, `naive-grep` 4/12, `subject-map` 4/12 (the r75 answer key rejected), `tree-identity` 5/12, `size-map` 5/12, `harness-source` 3/12 then 2/12, `seed-leak` 4/12, `hang` 0/12 (matrix kills the hung child at the 3 s bound and completes with FAIL — no invocation reached the battery's 300 s bound).

## 2. Direction B (before): r76 battery over r75 matrix — seat-assigned bounded variant

Command (exit 1; `--runs 1 --matrix-timeout 120` as assigned; the committed before receipt used battery defaults RUNS=2 MATRIX_TIMEOUT=300):

```
python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work /fast/scratch/hyaku/chousa-r76/R76ExecA/a-v2 --runs 1 --matrix-timeout 120
```

Exact tail: `forgers_rejected=9/11 positive=2/2` then

```
BATTERY=FAIL forgers_rejected=9/11 positive=2/2
```

Same 9/11 tally as the frozen before receipt `controls/before-battery-v2-matrix.txt`; only the hang leg's kill point differs (120 s matrix bound here vs the 300 s battery bound there). stderr empty.

Positive controls accepted by the r75 matrix: both `successor-counter` and `ref-counter` 12/12/PASS.

Forgers accepted by the r75 matrix (the answer-key channels claims.md names): **`subject-map` — 12/12/PASS, matrix_exit=0** (reads only `git log -1 --format=%s`; reproduced exactly as claimed). **`hang` — no verdict (matrix_exit=timeout at the 120 s bound)**, i.e. the r75 matrix cannot bound a stalled candidate. The other nine forgers REJECTED: `constant-pass` 4/12, `constant-fail` 4/12, `order-twelve` 1/12, `diff-only` 9/12, `naive-grep` 4/12, `tree-identity` 5/12, `size-map` 5/12, `harness-source` 3/12, `seed-leak` 4/12.

## 3. Stall question

No subject stalled the harness. Direction A: zero invocations hit any bound (the matrix itself kills the hang child at 3 s). Direction B: exactly one stall — the `hang` forger's matrix invocation, killed at the supplied 120 s bound; total wall time for both directions run concurrently was 125.9 s, consistent with that single 120 s stall. A correct positive was never killed at a bound (both positives exit 0 well inside it), so the recorded limit "a correct-but-slow counter can be killed at the bound" was not exercised against.

## 4. Kill-rule conformance

- Direction A: predicate line exact, exit 0, 11/11 forgers rejected in both runs, both positives accepted in both runs → the C1 "after" direction is reproduced as claimed.
- Direction B: `subject-map` accepted and `hang` unbounded on the r75 matrix → the two open channels claimed for round 75 are reproduced; 9/11 + 2/2 matches the frozen before receipt's tally.
- No instrument, forger, case or check was found deviating from its frozen bytes; no defect to report against the instruments. Per-run mark variance on `order-twelve`/`harness-source` (e.g. 2/12+1/12 vs the receipt's 4/12+2/12) is the recorded per-run salt doing its job; verdicts are unchanged.

## 5. Exact retained evidence (wave folder)

- `.ufo/waves/round-76/w1/R76ExecA/v3-battery.txt` — header + full verbatim stdout + stderr size + `EXIT=0`; stdout block diff-verified byte-identical to the captured run.
- `.ufo/waves/round-76/w1/R76ExecA/v2-battery.txt` — same shape, `EXIT=1`, diff-verified, plus the bounded-variant note.

Scratch `/fast/scratch/hyaku/chousa-r76/R76ExecA/` (battery work dirs `a-v3`, `a-v2` and raw stdout/stderr captures) is removed after this report; receipts were copied out first. Nothing under `/tmp` was used; no file over 50 MB was created anywhere. No git/jj mutation anywhere; lane writes limited to this seat's folder and this report.
