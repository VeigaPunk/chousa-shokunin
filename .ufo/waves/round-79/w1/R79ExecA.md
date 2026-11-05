# Seat R79ExecA — C1 operability reproduced from committed bytes

Lane chousa, round 79, wave 1. Scope: both directions of frozen claim C1 (forge battery
before/after) plus its supporting measurement (derivative check) and the battery's own
predicate (legitimate matrix accepted). Frozen revision: controls commit
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane HEAD at run time `b58a02db`
("round-79: freeze the two claims…"), a child of the controls commit.
`git status --porcelain` showed 4 dirty entries, none under `corpus/evidence/` — every
instrument ran from committed bytes.

## Pre-flight verification

All instrument digests on disk match the frozen table in `claims.md` exactly
(receipt: `R79ExecA/instrument-digests.txt`):

- `matrix-battery-v6.py` `bb91406e…5542a61e1d` — match
- `forge-battery.py` `5761edc5…be84ebbcad4fc936` — match
- `derivative-check.py` `af6fbe72…0a2bca0df3a0e35397bc1` — match
- `forgers/a9-v6-wrapper-normalizer.py` `851222ed…760be6b306c5` — match
- `forgers/a8-v5-salt-normalizer.py` `65f590af…5d965d6373c953` — match
- `round78/matrix-battery-v5.py` `5545a471…44c032b5af0` — match
- `round76/loader-matrix-v3.py` `b79d6441…2805c81913f` (printed by run (c) itself) — match

Toolchain: python3 3.14.8 (/usr/bin/python3), cc = GCC 16.2.1 20260810 (forge-battery built
the permutation enumerator from `round78/forgers/perm.c` with it). No tools were installed
or upgraded for this seat; pacman untouched per the 2026-10-20 host guard.

## Results — zero deviations from the frozen sentences

| run | command | expected | observed (verbatim predicate) | exit | wall | receipt |
|---|---|---|---|---|---|---|
| a | forge-battery --battery round78/matrix-battery-v5.py --work …/w-v5 | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1`, exit 1 | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` | 1 | 80 s | `R79ExecA/a-forge-v5.txt` |
| b | forge-battery --battery round79/matrix-battery-v6.py --work …/w-v6 | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, exit 0 | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | 81 s | `R79ExecA/b-forge-v6.txt` |
| c | matrix-battery-v6 --matrix round76/loader-matrix-v3.py --work …/w-v6 | exit 0, `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` | 0 | 88 s | `R79ExecA/c-battery-v6.txt` |
| d-v5 | derivative-check --battery round78/matrix-battery-v5.py | `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096`, exit 1 | `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096` | 1 | 0 s | `R79ExecA/d-deriv-v5.txt` |
| d-v6 | derivative-check --battery round79/matrix-battery-v6.py | `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23`, exit 0 | `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` | 0 | 0 s | `R79ExecA/d-deriv-v6.txt` |

All receipts are the full stdout+stderr of the run plus ISO start/end timestamps and an
`EXIT=`/`WALL=` footer.

### (a) per-forger verdicts (before direction — identical to committed `controls/forge-battery-before-v5.txt`)

```
FORGER a1-trailing-salt-strip rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a2-parent-cmdline-source rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a7-printed-order-digest rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a5d-detached-append rc=1 receipt_lines=139 trailer=yes integrity=BAD verdict=DETECTED
FORGER a8-v5-salt-normalizer rc=0 receipt_lines=113 trailer=yes integrity=ok verdict=FORGED
FORGER a9-v6-wrapper-normalizer rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
POSITIVE legit-matrix rc=0 receipt_lines=113 integrity=ok verdict=ACCEPTED
```

The kill vector is exactly the one the claim names: the four-line `_r78<hex>` normalizer
makes the v5 battery print `BATTERY=PASS forgers_rejected=11/11 positive=0/2` at exit 0
(per-forger receipt: `R79ExecA/work-v5/a8-v5-salt-normalizer.receipt`, line 113).

### (b) per-forger verdicts (after direction — identical to committed `controls/forge-battery-after-v6.txt`)

```
FORGER a1-trailing-salt-strip rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a2-parent-cmdline-source rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a7-printed-order-digest rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a5d-detached-append rc=1 receipt_lines=139 trailer=yes integrity=BAD verdict=DETECTED
FORGER a8-v5-salt-normalizer rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a9-v6-wrapper-normalizer rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
POSITIVE legit-matrix rc=0 receipt_lines=113 integrity=ok verdict=ACCEPTED
```

Both one-normalizer-per-salt-family forgers are refused by v6 (a8 receipt now ends
`BATTERY=FAIL forgers_rejected=11/11 positive=0/2`), the four round-77/78 channels are
unchanged, and the legitimate matrix is still ACCEPTED — no blanket refusal.

### (c) subject outcomes (receipt `R79ExecA/c-battery-v6.txt`, lines 27–39)

Both positives ACCEPTED (`successor-counter`, `ref-counter`, each 12/12 on both runs); all
11 forgers REJECTED (constant-pass, constant-fail, order-twelve, diff-only, naive-grep,
subject-map, tree-identity, size-map, harness-source, seed-leak, hang); oracle
`ORACLE:summary-only` REJECTED (marks-only forgeries that PASS 12/12 on marks fail the
content check).

### (d) derivative windows

v5: all 13 subjects DERIVATIVE (positives `successor-counter` 4096 / `ref-counter` 2885;
forgers 389–1564) → `13/13 MAX_WINDOW=4096`. v6: every subject `window=23
not-a-derivative` → `0/13 MAX_WINDOW=23`. No copy shares a 40-byte window with its
committed source under v6 — the C1 kill rule's textual-derivative arm holds.

## Kill-rule assessment

- After predicate line differs? No — byte-identical sentence, exit 0.
- Positive control MISS? No — ACCEPTED in (b) and (c).
- Any forger FORGED in the after direction? No — 6/6 handled.
- Any v6 copy sharing a 40-byte window with its committed source? No — max window 23.

**C1 reproduces in both directions with zero deviations.** No post-freeze finding to
report from this seat.

## Notes and limits (observations, not defects)

1. `SETTLE=26` in my runs matches the committed controls; it is the instrument default
   (longest forger delay 20 s + 6), not a flag I passed.
2. The `a5d` DETECTED verdict depends on the 26 s settle window absorbing the 20 s detached
   append delay; it reproduced identically in both of my runs and in the committed
   controls.
3. Assignment paths reuse `w-v6` for both (b) and (c); the two instruments write disjoint
   files there, and I serialized (b) before (c). Top-level listings kept:
   `R79ExecA/work-v5/work-dir-listing.txt`, `R79ExecA/work-v6/work-dir-listing.txt`.
4. derivative-check's default `--work` (I ran the predicate command verbatim, with no
   `--work`) is `/fast/scratch/hyaku/chousa-r79/derivative-<battery>.{py,}` — inside the
   wave scratch root but outside my seat dir; left in place, regenerable.
5. Per-forger receipts and forger call logs from both work dirs are preserved under
   `R79ExecA/work-v5/` and `R79ExecA/work-v6/`.

## Environment

- Runs at 2026-11-04T21:22:33 to 21:25:49 -03:00; cwd was my scratch
  `/fast/scratch/hyaku/chousa-r79/R79ExecA`.
- `df -h /fast` before: 804G total, 486G used, 318G avail (61%) — `R79ExecA/df-before.txt`.
- `df -h /fast` after: 804G total, 490G used, 314G avail (61%) — `R79ExecA/df-after.txt`.
- Receipt sha256: a-forge-v5.txt `efc95d163efb566c74946a8683b2e97f0c3cc29d2dfea57a31b800327831ee7f`,
  b-forge-v6.txt `ebe3dfdd040ca184a159a4c275c369f374b9eb538a70cfbfbc107721eda12b94`,
  c-battery-v6.txt `475afbbe4b9a1a3ac6a5bd3bc10e2923110f2941d5665e0b59989d48d01e3e11`,
  d-deriv-v5.txt `dfe2dad613a82b6dfc6c597c526a86e1b55f455285e144054571ab64d0cd9956`,
  d-deriv-v6.txt `3ba7cfe2e808aaa3e4c249598cf6a5d500d72382ea206c676999f9f5b32061b3`,
  df-before.txt `0c5477286ca78d8e11012152993d13ac0b9a4c9a7fc55c97b219d47c800e044a`,
  df-after.txt `a3e5673298c2b0ad6bfca9444108e74bdce48d18f91bbab7e93143c9cc967b99`.

Scratch `/fast/scratch/hyaku/chousa-r79/R79ExecA` deleted after receipt preservation; no
fleet, lane, or sibling files were modified (the only writes are this report and the
`R79ExecA/` receipt folder).
