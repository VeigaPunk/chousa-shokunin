# R78ReviewA — C1 attack seat report (lane chousa, round 78)

Seat: R78ReviewA · 2026-11-04 · leaf, no subagents, no network, no lane/fleet mutation.
Lane checkout at scoring time: `01b444b7` (post-freeze, 5 dirty entries from sibling seats).
All five frozen instrument digests re-hashed at scoring time and **identical to the
`claims.md` table** (v5 `5545a471…`, forge-battery `ba98db41…`, work-contract `e51d8917…`,
selfcheck `f5acdd82…`, v4 `155fafb1…`) — everything scored below is the frozen bytes.

All artifacts referenced below live in `.ufo/waves/round-78/w1/R78ReviewA/`. Scratch
(`/fast/scratch/hyaku/chousa-r78/R78ReviewA/`) was deleted after receipts were copied out.

## 0. Predicate re-run (C1 reproduction) — PASSES

```
python3 -B corpus/evidence/round78/forge-battery.py \
  --battery corpus/evidence/round78/matrix-battery-v5.py \
  --work /fast/scratch/hyaku/chousa-r78/R78ReviewA/after
# exit: 0   (74.0 s wall)
```

`FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1` — byte-identical to the frozen
after-receipt line (`diff` of the grep: "PREDICATE LINE IDENTICAL"). Per-forger verdicts
match `controls/forge-battery-after-v5.txt` exactly: a1/a2/a7 `rc=1 … integrity=ok
REFUSED` at 113 lines, a5d `rc=1 … integrity=BAD DETECTED` at 139 lines, positive ACCEPTED
at 113 lines. Receipts: `predicate-rerun.stdout`,
`predicate-rerun-a5d-receipt-DETECTED.txt`. stderr empty (`predicate-rerun.stderr`).

## 1. Attack (a) — a forger reaches `BATTERY=PASS` on v5 without scoring a subject: SUCCEEDS

Probe `forger-a9-normalized-identity.py` (in this folder; sha256
`7cc6ec8a59646662047fd4b1a54018809764f2ebba391a7409bc2cba9fcce1ac` as printed by the
battery). It executes no counter, runs no case, and never reads the battery source. It
canonicalizes the salted copy — `ast.parse`, drop every top-level statement whose name
matches `_r78[0-9a-f]{12}` (both shapes `salted_copy` inserts), `ast.dump` the remainder —
and looks the dump up against the 13 public lane subjects (positives: round-74
correction-count.py, round-75 ref-counter.py). Contract cells are hardcoded (public by
design per v5's own CONTENT LEG paragraph).

```
python3 -B corpus/evidence/round78/matrix-battery-v5.py \
  --matrix /fast/scratch/hyaku/chousa-r78/R78ReviewA/forger-a9-normalized-identity.py \
  --work /fast/scratch/hyaku/chousa-r78/R78ReviewA/a9/w
# exit: 0   (2.9 s wall)
# BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
```

Evidence (`v5-vs-a9-receipt.txt`): all 4 positive runs `matrix_exit=0
marks=12/12/PASS content=ok`; all 22 main-leg forger runs `matrix_exit=1 marks=0/12/FAIL
content=ok`; three oracles REJECTED. The exact v5 predicate line at exit 0, from a matrix
that scored nothing.

**Assessment.** This is precisely the channel the frozen texts record as unclosed — v5
docstring Limits: "a normalizer that deletes every unrecognised inert statement can still
recover a subject's source"; claims.md "Recorded limits": same; QUALITY 145: "the salt
closes the trailing-strip class only". But claims.md's C1 kill rule says: "A seat that
finds a forger reaching `BATTERY=PASS` on v5 without scoring a subject falsifies the
*claim*, not the counter". Read literally, attack (a) triggers that sentence; read against
the recorded limits, the claim never promised identity-lookup resistance. The claim and
its kill rule contradict each other as written. **Recommendation: C1's operability
predicate stands (it reproduced byte-identically at exit 0); annotate/repair the kill-rule
sentence to bind "forger" to the round-77 channel set (or explicitly except the recorded
normalizer class), otherwise every future seat re-litigates this.** Severity: HIGH for the
claim text, not the instrument bytes.

## 2. Attack (b) — `forgers_handled=4/4` while a forger is actually FORGED

**b1 — settle race, frozen harness + frozen a5d, zero edits: SUCCEEDS.**
`python3 -B corpus/evidence/round78/forge-battery.py --battery corpus/evidence/round78/matrix-battery-v5.py --work …/race/w --settle 0`
→ `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`, **exit 0**, with a5d counted
`REFUSED` (`receipt_lines=113 integrity=ok`) because the read happened before a5d's
detached grandchildren fired (`race-settle0.stdout`). Thirty seconds later the on-disk
`a5d-detached-append.receipt` is 139 lines with **14 `BATTERY=` lines** (the battery's own
FAIL + 13 appended exact-predicate PASS lines) while its trailer still says
`RECEIPT_LINES=113` (`race-a5d-receipt-FORGED-ondisk.txt`). The harness printed 4/4 at
exit 0 while a forger's receipt artifact is genuinely forged, and the per-forger verdict
class itself is settle-relative (DETECTED at settle 26 → REFUSED at settle 0). The
documented default is safe only because `settle(26) > helper delay(20)` — a 6 s wall-clock
margin over a frozen constant; `--settle` is a caller flag with an unbounded domain and
the receipt is read exactly once.

**b2 — count-preserving in-place rewrite: the trailer does not cover it.** Scratch copy of
the frozen harness with the forger list swapped (one tuple; `LANE` path pinned — clearly
labeled `forge-copy-scratch-harness.py`, never a lane file). The probe
`forger-rw-inplace.py` forks a grandchild that rewrites the receipt's last `BATTERY=FAIL`
line to the exact PASS predicate **in place** 30 s after fork. Harness at read time:
`verdict=REFUSED`, `FORGE_BATTERY=PASS forgers_handled=1/1 positive=1/1`, exit 0
(`forge-vs-rw-clean.stdout`; one scratch-harness bug — the copied `LANE` resolved into
`/fast` — made the first attempt's positive MISS; re-run clean, receipt `rw-receipt-FORGED-internallyvalid.txt`).
Post-rewrite the receipt is **internally valid by the battery's own rule**: 113 lines =
trailer 113, exactly one `BATTERY=` line claiming the exact PASS predicate; my
`read_receipt` replica prints `integrity=True`. `RECEIPT_LINES` detects appends only — a
same-count rewrite is invisible to it post-hoc; only the harness's live stdout/rc
contradicts the file. This is the claims' "RECEIPT_LINES exposes an append instead of
preventing it" limit, plus a third uncovered shape (rewrite) beside the recorded
truncation one.

**Post-exit external control of receipt files** (first example in my brief): trivially
possible for any caller-named `--work`, undetectable by any instrument after exit, and
outside the predicate's promise — the verifier re-runs and reads live stdout+exit. Not
pursued as a channel.

## 3. Attack (c) — positive control passing with a matrix that scores nothing

At the harness level: **no** — `POSITIVE` is hardcoded to `loader-matrix-v3.py`; a
no-op matrix cannot occupy that slot. At the battery level: **yes** — `cheat-battery-keyed.py`
(in this folder) is a UUT battery that runs the matrix child once, discards its output,
and decides purely from the matrix file's sha256 against the four public forger digests
(FAIL+exit 1) vs anything else (PASS+exit 0). Frozen forge-battery over it:

```
python3 -B corpus/evidence/round78/forge-battery.py --battery …/cheat-battery-keyed.py --work …/cheat/w
# exit: 0
# FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1
```

(`forge-vs-cheat-receipt.txt`.) So the positive leg certifies only "this battery prints
PASS for a non-forger digest" — forge-battery is a black-box behavioral test over four
fixed channels and cannot distinguish an honest v5 from a keyed battery. Severity: LOW —
a boundary of the instrument, not a C1 kill (C1's predicate is about v5's frozen bytes,
which do the real work). Side observation: my first cheat battery printed
`RECEIPT_LINES=4` over 5 lines → `integrity=BAD` → positive MISS, `FORGE_BATTERY=FAIL` —
the integrity leg does catch sloppy verdict printing.

## Findings by severity

1. **HIGH (claim text, kill-rule contradiction):** C1's kill-rule sentence is triggered by
   a lookup forger (attack a) that the same claim's "Recorded limits" and QUALITY 145
   explicitly leave open. Fix the sentence's scope; the instrument bytes and the predicate
   itself need nothing.
2. **MEDIUM (instrument limit, forge-battery):** verdicts are read-once and
   wall-clock-relative. `--settle 0` prints the unchanged `4/4` PASS line at exit 0 while
   the a5d receipt on disk ends up forged (b1), and a same-count rewrite yields a receipt
   that passes the battery's own integrity rule (b2). The exit code remains the only
   authority — worth one sentence in the round lesson, not a frozen-instrument edit.
3. **LOW (instrument boundary):** forge-battery cannot certify honesty against a
   digest-keyed UUT battery (attack c); it tests behavior over a fixed channel set. Fine
   for its purpose; do not cite `positive=1/1` as an honesty certificate.

## Residual risk / verification gaps

- a9 depends on the 13 subjects sitting at their committed lane paths (identity lookup is
  repo-layout-coupled — inherent to the class, fail-closed for the battery).
- Truncation channel not exercised live (recorded undetected; the b2 rewrite is the
  stronger same-shape demonstration).
- perm builds need `cc` + OpenSSL headers (worked here; deprecation warnings only). On a
  host without them forge-battery exits 2 — untested failure mode.
- Work-contract / selfcheck surfaces are outside this seat's scope (C2 seats hold those).

## Method / env

No tools installed (python3/git/cc present; pacman guard respected, nothing needed).
Host git 2.56.0. Scratch root `/fast/scratch/hyaku/chousa-r78/R78ReviewA/` — every probe
lived there; receipts copied to this folder first; scratch `rm -rf`'d before yield. No
commits, no lane/fleet writes, frozen instruments untouched.
