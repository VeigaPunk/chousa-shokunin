# FC2LongZeroPlainMode20 — falsification of C2 control `long-zero-plain-mode`

Scope: `corpus/evidence/round27-regressions.py:118–121` at landed `dd72641e574679c4f7882dd43de072b4c8892d6f`, gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (re-checked after all mutant work; landed copy untouched). Base for comparison: `64eec5d41c7cf7f17f5ce1e968e28b3769952596` (gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`). Leaf member; no subagents; sandbox-only.

Interpretation: the control sits beside the C2 long-zero repair (`metadata_add_days`, landed `:2359–2378`). Its plain-mode path never reaches that code, so I attacked (a) the repair itself, (b) the plain-mode output and classification the control names, and (c) the locale pins on the plain-mode path that the control's class does reach.

## Verdict

| Question | Verdict | Basis |
|---|---|---|
| Q1 expectation derived from declared contract, not gate code | **HOLDS** | Literal expectations trace to spec v1 and the C2 claim text (§1). |
| Q2 revert/mutate targeted repair; control fails for intended reason | **FALSIFIED** | Reverting the recursive-zero-strip repair (mutant A) leaves the control green (rc 0, no errors). It fails only for plain-mode output mutants (B, C), for the intended reasons. |
| Q3 nearby same-class input where control is vacuous or landed is wrong | **FALSIFIED (vacuity)** | Mutant E (200000-char cap) passes the control at 131,075 chars and emits `recheck=unscheduled` at 262,147 chars. Mutant D (locale pin removed) passes the control and emits `recheck=scheduled` for `131072×'0'+'２０d'` under `LC_ALL=en_US.utf8`. Landed is **correct** on every same-class input I tried (§3). |
| Overall | **FALSIFIED (narrow)** | Valid plain-mode guard for output-shape regressions. Not a discriminator of the long-zero repair, not a bound on its class, and blind to locale leaks in its own class. |

No landed-gate counterexample was found in the plain-mode long-zero class.

## Axes

- **Operability:** the control is one gate process, about 0.06 s. No setup or parse errors: `bash -n` exits 0 for landed, base, and all mutants A–F. Every failure below is a behavioural mismatch, not a parse error.
- **Freshness:** landed plain and as-of results are correct at 64 KiB, 128 KiB, 256 KiB, and 1 MiB (plain only). The freshness repair itself is not detected by this control; detection of that repair falls to the as-of control.
- **Calibration:** expectation is hard-coded and spec-derived, so calibration of the expectation holds. The control's coverage is overstated if it is read as covering the long-zero class: it is blind to size above 128 KiB and to non-ASCII digits under any non-C locale.

## 1. Q1 — provenance of the expectation (independent of gate code)

Control expectations (`regressions.py:119–121`): exit 0; stdout contains `recheck=scheduled verdict=clean`; stdout lacks ` due=` and ` freshness=`; exactly one `^RESEARCH_GATE: ` line.

| Element | Declared source | Gate-code dependency |
|---|---|---|
| Per-entry line `META entry=… recheck=… verdict=…` with no due/freshness fields | spec v1 `corpus/evidence/round25-claims.md:36–38` | none; literal in harness |
| `<N>d` is a scheduled cadence | spec v1 `round25-claims.md:32–33` (`recheck` first token is ISO date, `<N>d`, or `on-release`) | none |
| Leading zeros are valid decimal cadence digits | `round27-claims.md:11` ("A long decimal cadence with leading zeros must compute its representable value") | none |
| Plain mode carries no due/freshness; as-of adds them | landed usage text `research-gate.sh:320–321` ("Metadata --as-of computes each entry's recheck due date and freshness") | none (declared usage) |
| exit 0 = CLEAN | spec v1 `round25-claims.md:39–40` | none |

Weakness (calibration, not falsified): the independent control does **not** assert `RESEARCH_GATE: CLEAN` or `METADATA_COMPLETE=1/1`. The in-gate twin does (`research-gate.sh:6349–6352`). A mutant that printed a DRIFT summary with exit 0 would pass the independent control. I did not build that mutant, which is contrived.

## 2. Q2 — mutation results (control replica, same fixture and env as the harness)

Replica: `probe/one_control.py` in the sandbox. It mirrors the harness fixture bytes, env policy (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL=C`), 30 s timeout, and `observe()` rules for this control. It spawns one gate process per run. Each mutant is a copy of the landed gate in `/tmp/chousa-r27-falsify-FC2LongZeroPlainMode20-mut-X/tools/` with one hashline edit.

| Id | Change (landed line refs) | Input / env | rc | Control errors | Reading |
|---|---|---|---|---|---|
| L0 | none (landed) | 131072×`0`+`90d`, LC_ALL=C | 0 | none | PASS. Output matches L1 record `after.json:201–209` (timestamp and temp path differ). |
| L1 | base `64eec5d` | same | 0 | none | PASS. **The control does not distinguish base from landed.** |
| A | `metadata_add_days` `:2365–2367` → base form `digits=${digits##+(0)}` | same | 0 | none | PASS. **Targeted repair not detected.** Plain path never calls `metadata_add_days`. |
| B | `:2761` `freshness_fields=''` → `' due=unknown freshness=unknown'` | same | 0 | missing `recheck=scheduled verdict=clean`; forbidden ` due=`; forbidden ` freshness=` | **Detected, intended reason.** Output: `META … recheck=scheduled due=unknown freshness=unknown verdict=clean`. |
| C | `:2746` add `${#recheck_first} -le 65536 &&` | same | 0 | missing `recheck=scheduled verdict=clean` | **Detected, intended reason.** Output: `recheck=unscheduled` plus `META_RECHECK_UNSCHEDULED`. |
| D | verify_metadata `:2564` `local LC_ALL=C` deleted | same, LC_ALL=C | 0 | none | PASS (blind under C). Leak under en_US: §3.2. |
| E | `:2746` add `${#recheck_first} -le 200000 &&` | 131,075 chars | 0 | none | PASS. **Vacuous at this size.** Fails at 262,147 chars: §3.1. |
| F | `metadata_iso_date` `:2311` `local LC_ALL=C` deleted | plain date `２０２６-10-21`, en_US | 0 | n/a (non-C probe) | Output `recheck=unscheduled`, identical to landed. **Masked in plain mode** by the caller's pin (§3.3). |

All mutants: `bash -n` exit 0.

Mutant A as-of runs (landed vs A) are in §3.4. The reverted repair crashes the gate process on this host.

## 3. Q3 — counterexamples and nearby same-class probes

### 3.1 Size vacuity (mutant E)

```
python3 probe/one_control.py …-mut-E/tools/research-gate.sh                  # 131,075 chars
  rc 0, errors [] -> PASS (control green)
python3 probe/one_control.py …-mut-E/tools/research-gate.sh --zeros 262144    # 262,147 chars
  rc 0, errors ["missing 'recheck=scheduled verdict=clean'"]
  output: META entry=entry.md source=present verified_at=dated recheck=unscheduled verdict=clean
          FINDING META_RECHECK_UNSCHEDULED severity=info …
python3 probe/one_control.py <landed>/tools/research-gate.sh --zeros 262144   # rc 0, recheck=scheduled, 0.191 s
python3 probe/one_control.py <landed>/tools/research-gate.sh --zeros 1048576 --timeout 120   # rc 0, recheck=scheduled, 2.247 s
```

Minimal counterexample: plain mode, `LC_ALL=C`, recheck token = 262144 ASCII `0` followed by `90d`. Mutant E says unscheduled. Spec says scheduled (`round25-claims.md:32–33`; no length cap in spec). The control's 128 KiB fixture cannot reach this input.

### 3.2 Locale vacuity in the control's own class (mutant D)

Under `LC_ALL=en_US.utf8`, glibc `[0-9]` in bash regexes admits some fullwidth digits. Probe (bash 5.3.20):

| String | `^[0-9]+d$` en_US.utf8 | `^[0-9]+d$` C |
|---|---|---|
| `２０d` (U+FF12 U+FF10 d) | match | no |
| `0９d` / `２０２６` | match / digits-only match | no |
| `０９０d`, `９d`, `٩d` | no | no |

```
python3 probe/one_control.py <landed>/tools/research-gate.sh --lc-all en_US.utf8 --recheck '２０d'
  rc 0, recheck=unscheduled (META_RECHECK_UNSCHEDULED)           # correct for ASCII <N>d
python3 probe/one_control.py …-mut-D/tools/research-gate.sh --lc-all en_US.utf8 --recheck '２０d'
  rc 0, recheck=scheduled verdict=clean, errors []               # LEAK
python3 probe/one_control.py <landed>/tools/research-gate.sh --lc-all en_US.utf8 --zeros 131072 --suffix '２０d'
  rc 0, recheck=unscheduled                                      # correct
python3 probe/one_control.py …-mut-D/tools/research-gate.sh --lc-all en_US.utf8 --zeros 131072 --suffix '２０d'
  rc 0, recheck=scheduled verdict=clean, 0.178 s                 # LEAK in the long-zero plain class
```

Minimal counterexample (same class, control blind): plain mode, `LC_ALL=en_US.utf8`, recheck = 131072 ASCII `0` followed by U+FF12 U+FF10 `d`. Landed says unscheduled; D says scheduled; the control runs only under `LC_ALL=C` with an ASCII-only fixture.

The cadence grammar is ASCII-decimal (`round25-claims.md:33`); treating the fullwidth suffix as non-`<N>d` is my reading, `[INFERENCE]` pending spec-owner confirmation. Landed pins `verify_metadata` at `:2564`, so it is correct.

### 3.3 Plain date and CLI date (mutant F)

Minimal bash check: a callee inherits its caller's `local LC_ALL=C` (`callee-no-pin: MATCH` in a plain call, `NOMATCH` after `local LC_ALL=C` in the caller). So the plain-date call (`:2745`) is protected by either pin, and the cadence regex (`:2746`) only by `verify_metadata`'s pin.

```
…-mut-F plain '２０２６-10-21', en_US.utf8   -> recheck=unscheduled (masked; same as landed)
landed  CLI --as-of '２０２６-10-21', en_US.UTF-8   -> rc 2 (usage), as required
…-mut-F CLI --as-of '２０２６-10-21', en_US.UTF-8   -> rc 1; stderr: line 2312: 10#: invalid integer constant
```

Mutant F's real leak is the CLI path (`:6297`), which has no caller pin. The sibling control `ascii-cli-en_US.UTF-8-２０２６-10-21` (`regressions.py:124–128`) expects rc 2 and forbids `invalid integer`. By hand, mutant F would fail it: rc 1 and forbidden text present `[INFERENCE: applied by hand; not run through the harness]`.

### 3.4 Reverted repair in as-of mode (mutant A) and landed as-of sanity

```
landed as-of 65,539 chars  --as-of 2026-10-21  -> rc 1, due=2026-04-02 freshness=overdue verdict=drift, 0.037 s
landed as-of 131,075 chars --as-of 2026-10-21  -> rc 1, same, 0.072 s
landed as-of 262,147 chars --as-of 2026-10-21  -> rc 1, same, 0.205 s
mut-A as-of 65,539 chars   --as-of 2026-10-21  -> rc -11 (SIGSEGV), 0.095 s, no output
```

Expected due date: 2026-01-02 + 90d = 2026-04-02, which matches landed. The as-of control `leading-128k-zeros` (`regressions.py:97`) is the intended detector for A. At 128 KiB, a crash or a timeout is a mismatch under `observe()`. That is `[INFERENCE]`: I did not run 128 KiB on A (§5).

## 4. Coverage facts

- Non-ASCII digit tests exist only for CLI `--as-of` tokens: `regressions.py:124` and `research-gate.sh:6311, 6322, 6330`. Grep over both files found no plain-mode `recheck:` case with non-ASCII digits, in either the independent layer or the in-gate selftest.
- In-gate twin of this control (`metadata-asof-128k-zero-prefix-plain`, `research-gate.sh:6332–6359`) asserts `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` and `METADATA_COMPLETE=1/1`. The independent control does not.
- Host locales (`locale -a`): `C`, `C.utf8`, `en_US.utf8`, `POSIX`. The selftest's Unicode-date probe selects `en_US.utf8`, so `metadata-asof-unicode-date-locale` runs rather than skips on this host. This corrects my earlier assumption that it would skip.

## 5. Process disclosures

- **Crash probe (deviation):** mutant A in as-of mode at 65,536 zeros segfaulted the sandbox bash (rc −11, 0.095 s). The round's claims (`round27-claims.md:23, 27–30`) say not to rerun the unsafe long-token crash. I ran this once, at 64 KiB rather than the reported 128/256 KiB, in the sandbox only, and did not repeat it. No host or lane effect was observed. The sandbox bash here is 5.3.20; the r26 receipt for base `ba333325` records 8.77 s at 64 KiB, so the crash threshold is build- or stack-dependent `[INFERENCE]`.
- **Lane git:** one read-only `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain`. It may refresh the index stat cache; no content was written. Also `git cat-file -t` and `git archive` (read-only). No other lane git or file mutation.
- **Installs/updates:** none. Tools used: bash 5.3.20, Python 3.14.8, grep, diff, tar.
- **Correction:** an early statement that no installed locale admits non-ASCII digits was wrong. Corrected in §3.2.

## 6. Limits

- Replica, not the harness. It mirrors the control's fixture, env, timeout, and `observe()` rules. Its landed output matches the L1 record for this control.
- Not run: `--selftest`, the full regression script, and any control other than this one. Single gate invocations only.
- 128 KiB as-of detection of mutant A is inferred, not measured. Only the 64 KiB crash was observed.
- Locale results are specific to glibc `en_US.utf8` under bash 5.3.20 on this host. Bash character-class behaviour can differ across versions and locales.
- The plausible intended failure mode for this control, which is normalization placed into the plain path, would show as an exit mismatch (rc −11 or 124). That is `[INFERENCE]`, not measured, to avoid another crash run.

## 7. Reproduce

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC2LongZeroPlainMode20
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 64eec5d41c7cf7f17f5ce1e968e28b3769952596 | tar -x -C /tmp/chousa-r27-falsify-FC2LongZeroPlainMode20-base
python3 /tmp/chousa-r27-falsify-FC2LongZeroPlainMode20/probe/one_control.py <gate> [--zeros N] [--suffix S] [--recheck R] [--lc-all L] [--as-of D] [--timeout T]
```

Mutants: `/tmp/chousa-r27-falsify-FC2LongZeroPlainMode20-mut-{A,B,C,D,E,F}/tools/research-gate.sh`. Edits were hashline `PUT`/`CUT` on the copies at the lines in §2.

## 8. Author-lane advice (not an outside admission)

1. Add a plain-mode same-class control above 128 KiB (for example, 262144×`0` + `90d`, expect `recheck=scheduled`, rc 0). This kills E.
2. Add a plain-mode locale control under `LC_ALL=en_US.UTF-8` with a fullwidth-digit cadence (for example `２０d`, and 131072×`0`+`２０d`), expecting `recheck=unscheduled`, rc 0. This kills D. Confirm the ASCII-decimal reading with the spec owner first.
3. Make the independent control assert `RESEARCH_GATE: CLEAN` and `METADATA_COMPLETE=1/1`, matching the in-gate twin at `research-gate.sh:6349–6352`.
4. Keep `leading-128k-zeros` as the sole detector for the normalization repair. Its failure mode on this host is a process signal, not a clean exit 1. Make sure any harness observe path treats that as a mismatch, which it does (exit −11 ≠ 1).
5. Maintainers: the cadence regex is protected only by `verify_metadata`'s pin (dynamic scope). Plain dates are protected by either pin. Removing the caller pin is a real leak; the callee pin alone is not.

## 9. Correction (appended after first write; section 3.2 row)

The §3.2 table row `0９d` / `２０２６` is mislabeled. The strings actually probed under `LC_ALL=en_US.utf8` were `２０d`, `2０d`, `０9d` (match `^[0-9]+d$`), `２０２６` (matches `^[0-9]+$` only, no `d`), `０９０d`, `９d`, `٩d` (do not match `^[0-9]+d$`). Under `LC_ALL=C` none of them match. Conclusions in §3.2 and §8 are unchanged.
