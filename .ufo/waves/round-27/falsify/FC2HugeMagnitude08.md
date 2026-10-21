# FC2HugeMagnitude08 — falsification of C2 control `huge-magnitude`

Scope: `corpus/evidence/round27-regressions.py:99` at landed `dd72641e574679c4f7882dd43de072b4c8892d6f`. Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches bounds). Base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`, byte-identical to the r26 measured gate (`.ufo/waves/round-26/falsify/FDateHugeCadence.md:20-21`). Leaf member; no subagents; sandbox `/tmp/chousa-r27-falsify-FC2HugeMagnitude08`. Author-lane advice, not an outside admission.

## Verdict

| Question | Verdict | Basis |
|---|---|---|
| Q1: expectation derived from the declared contract, independent of gate code | **HOLDS** | §1 |
| Q2: revert or mutate the targeted repair; control fails for the intended reason | **FALSIFIED (narrow)**. Detects the targeted length-guard revert (M1) for the intended wrap-around reason. Does not detect the r27 normalization revert (M2), the range-check revert (M4), or a 19-digit bound (M3). | §2 |
| Q3: nearby same-class input where landed is wrong or the control is vacuous | **FALSIFIED**. A refuse-all gate passes this control (12 of 16 rows). The 8–19-digit window is unguarded. Landed does not complete within 100 s on an admissible 8 MiB leading-zero cadence. No wrong verdict on any input that completed. | §3 |
| **Overall** | **FALSIFIED (narrow)** | The expectation is sound. The control is not the detector for the C2 repair it sits beside, and its positive power is one-sided. |

## Axes

- **Operability:** one gate process per row, about 0.05 s. No harness or parse errors. `bash -n` rc 0 on landed, M1–M4, M8 and M1b; M5–M7 ran without parse errors. Every mismatch is gate behaviour. The 8 MiB leading-zero entry did not finish in 100 s (rc 124, probe kill).
- **Freshness:** landed due and freshness values are correct on all 16 probe rows and on every long-zero row that completed. The control does not detect the normalization repair (§2, M2).
- **Calibration:** the hard-coded expectation matched my independent Python oracle on all 16 rows (`control_matches_oracle=True`). Coverage is overstated: this row is not the FDateHugeCadence detector (§1).

## 1. Q1: provenance of the expectation

- Row: `('huge-magnitude', '2026-01-02', '9'*40 + 'd', '2026-10-21', None)`, `regressions.py:99`. The harness sets expected exit `int(freshness == 'overdue')` = 0, requires `due=unknown freshness=unknown`, and requires one `RESEARCH_GATE:` line and one `META entry=` line (`regressions.py:112-117`).
- Contract: `round27-claims.md:11`, "out-of-range values remain unknown". Forty nines of days is out of range. From any start date the representable span is at most 3,652,058 days (0001-01-01 to 9999-12-31).
- Independent of gate code: the expected value is a literal `None`. My oracle (`date + timedelta(days=int(digits))`, overflow means unknown) agrees on all 16 rows.
- Inherited, not stated in the claims: "unknown means exit 0 and verdict clean". It is pinned by the base selftest `metadata-asof-large-cadence` (36 nines, unknown, rc 0; `base/tools/research-gate.sh:6108-6116`) and by r26 receipt F2 row `n40_huge` (`FDateHugeCadence.md:140`). The control also does not assert `verdict=clean`. Minor.
- The 40-nines row therefore duplicates behaviour that base already has; it is not new evidence. The L1 receipt agrees (`round27-regressions-after.json:94-98`, not rerun).
- It cannot reproduce the r26 failure it is filed under. Observed: r26 F2 ran the same gate bytes and recorded `n40_huge → unknown, rc0`. Static trace of base `metadata_add_days` (base 2343–2359): `${digits##+(0)}` is a no-op on forty nines, then `${#digits} <= 7` returns 1. I did not run base on this fixture (claims rule against reruns).
- The r26 failure is different. F1 is extglob leading-zero recursion, SIGSEGV at ≥68,000 zeros (`FDateHugeCadence.md:34-53`). This row has no zero prefix.

## 2. Q2: mutation evidence

Mutants are one-site edits of sandbox copies of landed (`tools/mut-*.sh`). `driver/huge_driver.py` replicates the control's fixture bytes, env (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL=C`), invocation and `observe()` for 16 synthetic rows: 6 from the control table (lines 99–104) and 10 neighbours. The driver exits 0 regardless; the `SUMMARY` line carries the result.

| Mutant (landed line) | `huge-magnitude` | Slice mismatches | Reading |
|---|---|---|---|
| landed | PASS | 0/16 | none |
| M1: length guard deleted (L2369) | FAIL: rc 1, no META or verdict line | 6/16 | Intended mechanism, see chain below. |
| M2: normalization reverted to base `${digits##+(0)}` (L2366–2367) | PASS | 0/16 | Not detected. The input has no leading zeros. |
| M3: length bound 7 → 19 (L2369) | PASS | 2/16 (`n19-nines`, `pow63-exact`) | Not detected. |
| M4: range check deleted (L2376) | PASS | 4/16 (7-digit boundary rows) | Not detected. |
| M8: refuse-all, `return 1` at L2362 | PASS | 4/16 (rows expecting a due) | Vacuous, §3.1. |

Chain for M1, confirmed with debug copy M1b (one `printf` inserted after the due assignment in the copy): forty nines makes `amount=$((10#…))` wrap to `-5047021154770878465` (bash 5.3.20). The range check `amount <= last_day - start` accepts the negative amount, so `due_date=-13818274584064392-08-01`. The re-parse in `metadata_days_from_iso` (line 2356) then dies with `10#: invalid integer constant` (rc 1, no output). The same chain holds for `pow63-exact` (`DBG_DUE=-25252734927764529-06-08`). For `pow64-plus-90` the wrap lands on 90, giving `due=2026-04-02 freshness=overdue` (exit 1, a semantic mismatch). `one-then-39-zeros` wraps positive, so the range check refuses it and it passes.

Did the control fail for the intended reason? For M1, yes: the wrap is accepted as in range. The gate's own crash is the downstream symptom, not a harness error. For M2, M3, M4 and M8 it does not fail.

## 3. Q3: counterexamples

### 3.1 Vacuity: refuse-all gate (M8)

M8 returns unknown for every cadence. It passes 12 of 16 rows, including `huge-magnitude`, `one-then-39-zeros`, `pow64-plus-90`, `overflow-span`, `n19-nines`, `pow63-exact`, `z40-huge`, `z40-pow64-plus90` and `end-plus1-7digit`. The four rows it fails are the ones that expect a due date. The suite as a whole still catches M8 through those rows, but this control has no positive power on its own.

### 3.2 Window gap: 8–19 significant digits (M3)

Significant-digit counts of every cadence row in the regression date table are {0, 1, 2, 7, 20, 40} (`regressions.py` lines 97–106, the leap rows at 111, and 118). Grep of the selftest's `recheck: <digits>d` fixtures found only 1–3-digit cadences and the 36-nines `large-cadence`. No row sits in 8–19. M3 therefore changes no regression or grep-visible selftest row, yet it is wrong for 2^63 ≤ x ≤ 10^19−1, which wrap negative.

Minimal counterexample: `recheck: 9223372036854775808d`, verified 2026-01-02, as-of 2026-10-21. Landed gives `due=unknown freshness=unknown`, rc 0. M3 gives the `10#` crash, rc 1. `9999999999999999999d` behaves the same way.

### 3.3 Time: admissible leading-zero cadence does not finish on landed

Each row is one `verify-metadata --as-of 2026-10-21` process with `LC_ALL=C` and `CHOUSA_*` stripped. The cadence is N zeros followed by digits (synthetic). Byte counts are the cadence token; the 8 MiB file is about 8.38 MB, under the 8 MiB cap (`SOURCE_READ_MAX_BYTES`, landed line 271).

| Row (landed) | Token bytes | rc | Wall time | Verdict vs oracle |
|---|---|---|---|---|
| 128 KiB zeros + `90d` | 131,075 | 1 | 0.07 s | correct (overdue) |
| 1 MiB zeros + `3652058d` (verified 0001-01-01, as-of 9999-12-31) | 1,048,584 | 0 | 2.51 s | correct (current) |
| 1 MiB zeros + `3652059d` (same) | 1,048,584 | 0 | 2.63 s | correct (unknown) |
| 2 MiB zeros + `90d` | 2,097,155 | 1 | 14.28 s | correct |
| 2 MiB zeros + `90d`, plain mode (no `--as-of`) | 2,097,155 | 0 | 14.62 s | correct (clean) |
| 4 MiB zeros + `90d` | 4,194,307 | 1 | 61.57 s | correct |
| 8 MiB − 4 KiB zeros + `90d` | 8,384,515 | 124 | >100 s (probe kill) | not completed |

Attribution, all sandbox:

- M5 (the r26 candidate regex in the normalization): 4 MiB 67.83 s. M6 (no normalization at all): 4 MiB 67.14 s. The normalization is not the time sink.
- Isolated bash micro-benchmark (`driver/regex_bench.py`, synthetic token, 1 MiB → 2 MiB): `line=${line%$'\r'}` at landed line 2657 costs 2.38 s → 13.29 s, about 5.6× per doubling. Every other gate-path operation stays at or below 0.085 s: key-split `(.*)$` 0.040 → 0.085 s; first-token capture 0.035 → 0.078 s; cadence capture 0.037 → 0.074 s; read loop 0.010 → 0.027 s.
- M7 (line 2657 replaced by `if [[ $line == *$'\r' ]]; then line=${line:0:${#line}-1}; fi`): 128 KiB 0.04 s, 1 MiB 0.23 s, 2 MiB 0.42 s, 4 MiB 0.88 s, 8 MiB − 4 KiB 2.04 s. Every verdict equals landed where landed completed, and equals the oracle throughout.
- Inherited, not introduced by C2: base `64eec5d` has the identical strip at base line 2632 (entry reader) and 2411 (registry reader; landed 2430). The C2 repair did not touch it.
- Extrapolation [INFERENCE]: landed scales 4.3× per doubling from 2 to 4 MiB, and the isolated strip scales 5.6× per doubling. The 8 MiB − 4 KiB case therefore projects to roughly 4.5–6 minutes.
- Base is not comparable at these sizes: it SIGSEGVs at ≥68,000 zeros (r26 F1), which masks the time cost [INFERENCE].

Counterexample: an admissible 8.38 MB entry with a leading-zero cadence does not finish within 100 s on landed. The 128 KiB control takes 0.07 s and cannot see the problem. Whether this violates "without termination" depends on whether C2 carries a time bound; `round27-claims.md:11` states none, so this is author-lane judgment. No wrong verdict was found on any input that completed.

## 4. Commands and exit codes (key)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C /tmp/chousa-r27-falsify-FC2HugeMagnitude08`: rc 0. `sha256sum tools/research-gate.sh`: `ca39d14d…2f84`.
- `git … archive 64eec5d… tools/research-gate.sh corpus/evidence | tar -x -C …/base`: rc 0. Base gate `c2c813f1…abc6`. `git rev-parse dd72641e…` returned the same sha (read-only).
- Bash arithmetic: `10#` of forty nines → `-5047021154770878465`; `1` plus 39 zeros → `6873995514006732800`; `10#18446744073709551706` → `90`. rc 0 each.
- Python: `date(2026,1,2) + timedelta(days=9999999)`, `…days=3652058` and `…days=3652059` each raise OverflowError. `date(9999,12,31) − date(1,1,1)` = 3,652,058 days.
- `python3 driver/huge_driver.py --gate <gate> --cases <16 names>`: landed `SUMMARY … mismatches=0`; M1 `=6`; M2 `=0`; M3 `=2`; M4 `=4`; M8 `=4`; M1b debug output as in §2.
- `bash -n` on landed, M1–M4, M8 and M1b: rc 0 each. `diff` against landed: each mutant is one edit (M2 replaces two lines with one; M3 changes one line; M1 and M4 delete one line; M8 replaces one line).
- `python3 driver/scale_probe.py` and `driver/scale_pick.py`: rows in §3.3. The probe kill is rc 124 inside the probe. No gate run ran longer than 100 s.
- `python3 driver/regex_bench.py 1048576 2097152`: rc 0, table in §3.3.

## 5. Process disclosures

- Installs or updates: none. Tools used: bash 5.3.20(1), Python 3.14.8, git (read-only `archive` and `rev-parse`), tar, sha256sum, diff, date, nproc.
- Lane writes: none apart from this report. Lane files were read only.
- Not run: the full `--selftest`; the whole regression script; the base gate on any control fixture; the unbounded long-zero crash reproduction (the r26 F1 receipt is cited instead). No network, host secret files, `/proc` or live-process inspection, strace or debugger.
- Fixtures are synthetic and confined to `/tmp/chousa-r27-falsify-FC2HugeMagnitude08`.

## 6. Limits

- The driver replicates the control's fixture and `observe()` for 16 rows; it is not the harness. The 58-control script was not run, as the bounds require.
- Timings are from a shared 32-core host, and some runs were batched in parallel; expect about ±10%. The scaling ratios are the robust part.
- M7 is an attribution probe, not a proposed patch. Equivalence for lines with one trailing CR rests on inspection of `${line%$'\r'}` semantics.
- Base equivalence for `huge-magnitude` rests on the committed r26 receipt (identical gate sha) and a static trace. Base was not run.
- The 8 MiB landed run did not complete. ">100 s" is a probe bound, not a completion time.
- Locale effects are not tested here. The sibling `FC2LongZeroPlainMode20` covers the plain-mode locale class.

## 7. Author-lane advice (not an outside admission)

1. Add a row with 8–19 significant digits, for example `9223372036854775808d` from 2026-01-02 expecting `unknown`. This kills M3.
2. Add an in-range long-zero row above 128 KiB with a wall-clock bound, for example 1 MiB of zeros plus `3652058d` from 0001-01-01 expecting `due=9999-12-31 freshness=current`. The 128 KiB row cannot see the quadratic step.
3. Re-examine `line=${line%$'\r'}` in the entry reader (landed 2657) and the registry reader (landed 2430). M7 is an attribution probe only; the owner must check semantics and re-measure.
4. Stop presenting `huge-magnitude` as the FDateHugeCadence detector. That receipt is leading-zero recursion. Keep `leading-128k-zeros` as the detector, as the sibling advises. Keep `huge-magnitude` as a boundary row, paired with in-range positive rows (`max-span` and the rest), which catch M8.
5. Adjacent, not measured [INFERENCE]: the claims-JSONL reader's trailing-whitespace loop (landed 1353–1354, `while [[ $line == *[[:space:]] ]]; do line=${line%?}; done`) has the same quadratic long-line shape.
