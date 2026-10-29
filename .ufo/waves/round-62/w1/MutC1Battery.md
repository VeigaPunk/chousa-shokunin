# MutC1Battery — mutation test of the frozen R62-C1 battery (w1)

Scope: `corpus/evidence/round62/c1v2-battery.py` (sha256 prefix `9afe00b917fb95e2`). Mutants were applied only to scratch copies under `/fast/scratch/hyaku/chousa-r62/MutC1Battery/` (deleted before yield). No lane file, control, counter or git state was touched.

## Result

- 18 single-anchor mutants (each `str.replace` asserts exactly one match). 11 are killed by the frozen controls with a stable notice; 7 are control gaps.
- Mutants that flip a BATTERY verdict wrongly (false PASS or false FAIL, against the known answer): 13 of 18. Of those, 9 are caught by the frozen controls; 4 are not (M09, M13, M17, M18).
- Two further mutants (M02, M03) flip no frozen counter but admit a wrong PASS against a counter I built (section 4). M15 has no observable effect.
- Frozen-control noise: control X02 (`no PID namespace`) is not reproducible on this loaded host (section 3). Its notices are excluded from the kill count.

## 1. Method and baseline

Lane copy: `cp --parents` of `tools/build-spans.py`, `tools/capture-text.py`, `corpus/evidence/round61/c1-count.py`, the round-62 battery and counter, and the whole `controls/` directory; byte equality with the lane asserted before every run. The lane's `controls/` directory gained an untracked file `path-keyed-counter.py` (mtime 21:14:17) during the wave; it is not in the frozen claims, is not used by the battery, and was excluded from my copy check.

Counters per mutant (`python3 -B BATTERY --counter K --work DIR --landed tools/build-spans.py`):
- v2 `c1v2-count.py` (expected PASS); r61 `corpus/evidence/round61/c1-count.py` (expected FAIL);
- `null-pass`, `null-fail`, `null-hashlist` from `controls/` (expected FAIL);
- three probes I wrote, not frozen (expected FAIL): `probe-exit2` (exit 0 for known hashes, 2 otherwise), `probe-token` (runs v2; accepts a builder whose source contains `C1V2=PASS`), `probe-fingerprint` (exit 0 when a unique landed line is present);
- r61 and null-pass again with `--only LANDED POSITIVE` (expected FAIL: a partial run must not pass);
- the frozen control suite `controls/run-c1v2-controls.py` (X00–X12) run with the mutant battery in place.

Baseline (unmutated battery) reproduces the committed records. BASE line of the driver:
`BASE verdicts {'v2': 'PASS', 'r61': 'FAIL', 'null-pass': 'FAIL', 'null-fail': 'FAIL', 'null-hashlist': 'FAIL', 'probe-exit2': 'FAIL', 'probe-token': 'FAIL', 'probe-fingerprint': 'FAIL'} only {'r61': 'FAIL', 'null-pass': 'FAIL'} wrong [] notices []`
- r61 per-subject tuples and summary equal `controls/c1v2-before.txt` (`FORGERS_REJECTED=0/12`);
- the three null summaries equal `controls/null-counters.txt`;
- X00 `BATTERY=PASS`; the other X lines equal `controls/c1v2-controls.txt`; `CONTROLS_UNEXPECTED=0`.
- v2 standalone, `C1V2_SEED=7 python3 -B c1v2-count.py --work .../w`: `LEGS=20/20 C1V2=PASS`, exit 0, `real 0m2.452s` (unloaded).

"Killed by frozen control" = a regenerated control record (r61 subject tuples, a null summary, or an X line / `CONTROLS_UNEXPECTED`) differs from the committed record, excluding X02 (section 3).

## 2. Mutant table

| ID | What changed in the battery | Verdict effect (wrong flips) | Stable frozen-control notice | Class |
|---|---|---|---|---|
| M01 drop salt | `salted()` returns `src` | null-hashlist → PASS | null-counters(null-hashlist) | killed |
| M02 constant salt | `salt = "0"*16` | none on frozen; denylist probe → PASS (§4) | none | gap |
| M03 exit 2 counts as reject | `ok` also true when want 1 and rc 2 | none on frozen; recognise-or-abort probe → PASS (§4) | none | gap |
| M04 forgers expect exit 0 | `want=0` for FORGER | v2 → FAIL; r61 → PASS | c1v2-before; 3 nulls; X00, X01, X03–X08, X10, X12 | killed |
| M05 sniffs always fire | forgers always run LANDED | v2 → FAIL | c1v2-before; X00, X01, X03–X08, X10, X12 | killed |
| M06 sniffs never fire | forgers always run BASE | r61 → PASS | c1v2-before; X01, X03–X08, X12 | killed |
| M07 drop F10 sniff | F10 `hit = False` | none (r61 FORGERS 1/12, BATTERY still FAIL) | c1v2-before (r61 subject changed) | killed |
| M08 drop stub group | no STUB subjects | v2 → FAIL (`S == [4,4]` unsatisfiable) | c1v2-before; 3 nulls; X00, X01, X03–X08, X10, X12 | killed |
| M09 verdict ignores stubs | `and S == [4,4]` removed | probe-token → PASS | none | gap |
| M10 forger threshold 11/12 | `F[0] >= F[1]-1` | none on subjects | X03, X04, X06, X08 (CONTROLS_UNEXPECTED=4) | killed |
| M11 forger denominator uncounted | `tally[1]` not incremented for FORGER | v2 → FAIL | c1v2-before; 3 nulls; X00, X01, X03–X08, X10, X12 | killed |
| M12 LANDED 2 of 3 | `for i in (1, 2)` | v2 → FAIL | c1v2-before; 3 nulls; X00, X01, X03–X08, X10, X12 | killed |
| M13 `--only` passes verdict | verdict over non-empty groups only | `--only LANDED POSITIVE`: r61 → PASS, null-pass → PASS | none (controls never use `--only`) | gap |
| M14 miss tallied correct | `tally[0] += 1` | every counter → PASS (incl. all three nulls) | c1v2-before; 3 nulls; X01, X03–X08, X12 | killed |
| M15 sniff exception fires | `except` → `hit = True` | none | none | gap (survivor) |
| M16 F12 without bytecode switch | F12 becomes honest | v2 → FAIL | X00, X01, X03–X08, X10, X12 | killed |
| M17 positives not required | `P == [4,4]` removed | probe-fingerprint → PASS | none | gap |
| M18 token stub defanged | stub-base-token prints `LEGS=0/20` | probe-token → PASS | none | gap |

Notes:
- The driver's own summary printed `KILLED_BY_FROZEN=13/18`, counting M02 and M09 through X02 notices alone. Those are flake (section 3), so I count them as gaps.
- M10 and M14 are the only mutants that a null counter notices in a way the controls record would show, besides M01, M04, M08, M11, M12.

## 3. Frozen-control instability (X02)

The `no PID namespace` control (X02) is not stable on this host. F12 (the detached cleaner) is dropped from X02's accepted set in 5 of 19 matrix runs whose mutation does not touch F12 (M01, M02, M07, M08, M09). Repeat on the unmutated battery, `python3 -B controls/run-c1v2-controls.py --work runs/X02rep$i --only X02 --jobs 1`, four runs:
- three: `CONTROL X02-no-sandbox battery_exit=1 KILLED forgers_accepted=F06,F10,F12 expected=ok ...`, `CONTROLS_UNEXPECTED=0`, rc 0;
- one: `CONTROL X02-no-sandbox battery_exit=1 KILLED forgers_accepted=F06,F10 expected=UNEXPECTED ...`, `CONTROLS_UNEXPECTED=1`, rc 1.

So the committed suite can exit 1 on the intact battery on a busy host. The battery's own verdict is unaffected (X00 passed in every run where the battery was unchanged), but any kill count that depends on X02 is noise. Cause: INFERENCE, not run to ground. Likely: F12's cleaner is a detached `setsid` helper that races the counter's `__pycache__` check, and the no-sandbox counter sees host processes.

## 4. Gaps the frozen controls do not notice

Battery verdict flips with no frozen-control notice. Probes were run by `exp2.py` (scratch); outputs verbatim:
- M09 + probe-token: `BATTERY=PASS` for a counter that accepts any builder printing the pass token. The stub group is the only subject that tests this, and M09 removes its verdict check. No frozen counter trusts tokens.
- M18 + probe-token: stub-base-token printing `LEGS=0/20` → probe-token PASS. Same gap: the token subject is the only check.
- M17 + probe-fingerprint: a counter that accepts builders containing a landed-unique line passes when `POSITIVES` is not required. `P == [4,4]` is the only check that stops it.
- M13 + `--only`: `--only LANDED POSITIVE` → `BATTERY=PASS` for r61 and null-pass. The guard `full = not a.only` is never exercised by the controls. The unmutated battery's `--only` run is FAIL for both, so the guard works; it is untested.
- M02 + denylist: a counter that rejects builders whose sha256[:16] is on a list recorded from a previous run. The recorded list equalled an earlier M02 run's FORGER/STUB hashes (`M02 denylist equals earlier M02 run's FORGER/STUB hashes: True`). Output: `M02+deny: rc=0 ... FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`. Against the real salted battery the same counter gives `BASE+deny: rc=1 ... FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL`. No control enforces the predicate's "random salt on each".
- M03 + recognise-or-abort probe (exit 0 if a landed/positive fingerprint is present, else 2): `M03+recog2: rc=0 ... BATTERY=PASS`; `BASE+recog2: rc=1 ... BATTERY=FAIL`. The battery scores exit 2 as a MISS only when want is 1 (`ok = r.returncode == want`). M03 makes exit 2 an accept for forgers and stubs. No frozen control returns exit 2.
- M15 (sniff exception path): no subject raises inside any sniff, so the `except` branch never runs. Survivor; low value.

## 5. Operability notes

- Battery cost: v2 is 2.45 s wall per subject unloaded, so one battery is about 60 s. Under the host load (average 40–56 during the wave) one control suite took 670 s. The control suite (12 batteries) is the slow part.
- Host sharing: the no-sandbox forgers F06/F10 scan every `/proc` cmdline for `c1` and `count`; other seats' processes match those strings (INFERENCE, consistent with X02 noise).

## 6. Recommendations (for L1; no frozen file changed)

Per the claims' rule these are limits or next-round battery additions, not rewrites of this round's battery:
1. Add a token-trusting counter and a stub-accepting counter to the controls (kills M09, M18).
2. Add an `--only` run with a passing subset to the controls (kills M13).
3. Add an exit-2 recogniser counter (kills M03) and a denylist-by-hash counter (kills M02).
4. Add a positives-free counter (kills M17).
5. Make X02 stable, or drop its F12 expectation, before using `CONTROLS_UNEXPECTED` as a gate.

## Evidence index

- Scratch driver (deleted): `drive.py full` (matrix, JSON per run), `exp2.py` (probes); outputs quoted in sections 1–4.
- Commands run: `python3 -B drive.py full`, `python3 -B exp2.py`, `python3 -B c1v2-count.py --work ...` (C1V2_SEED=7), `run-c1v2-controls.py --only X02` ×4.

No tool was installed or upgraded. Python used: system `python3` (3.14).

VERDICT: BATTERY_MUTANTS_KILLED=11/18 control_gaps=7
