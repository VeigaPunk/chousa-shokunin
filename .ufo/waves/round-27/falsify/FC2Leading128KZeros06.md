# FC2Leading128KZeros06 — C2 `leading-128k-zeros`

## Scope and verdict

- Revision: `dd72641e574679c4f7882dd43de072b4c8892d6f`; isolated archive `/tmp/chousa-r27-falsify-FC2Leading128KZeros06` only.
- Axes: **freshness** (decimal cadence/due date), **operability** (bounded real CLI execution), **calibration** (distinguish a surviving control mutant from a landed defect).
- **HOLDS for the named landed witness and nine nearby inputs. No landed-gate counterexample found in this bounded probe.**
- **Mutation verdict: SURVIVED the assigned persisted control.** A one-character defect in the new normalization expression rejects one-significant-digit cadences while preserving the control's `90d` witness. This is a scoped coverage finding, not falsification of C2 or the complete regression suite.

## 1. Is the expectation contract-derived and independent?

**Yes.** `corpus/evidence/round27-claims.md:9-11` requires a leading-zero decimal cadence to compute its representable value without termination. The underlying definition is `round26-claims.md:65-73`: first token `<N>d`, valid leading verified date, proleptic Gregorian addition, and overdue iff as-of is strictly later than due.

`round27-regressions.py:97` supplies:

```python
('leading-128k-zeros', '2026-01-02', '0' * 131072 + '90d',
 '2026-10-21', '2026-04-02')
```

The numeric value is 90, so `2026-01-02 + 90 days = 2026-04-02`; October 21 is later. This was independently checked with Python `datetime.date + timedelta(days=90)`, not gate helpers. The persisted observer requires exit 1, `due=2026-04-02 freshness=overdue`, one anchored verdict record, and one anchored META entry. The due literal is not obtained from gate code; freshness comparison uses Python dates.

The scratch detector AST-selects only that tuple, the unchanged `observe` (`31-44`), `entry_text` (`57-58`), `run` (`60-67`), and date-case loop (`112-117`). It does **not** execute the regression script wholesale or any usage/registry tests. The same selected detector and neighboring inputs run in all three phases.

## 2. One production-fix mutation and actual results

Smallest mutation, `tools/research-gate.sh:2366`, inside the new nonrecursive normalization fix:

```diff
-  [[ $digits =~ ^0*([123456789][0123456789]*)?$ ]] || return 1
+  [[ $digits =~ ^0*([123456789][0123456789]+)?$ ]] || return 1
```

Only `*` became `+` in the significant suffix. This plausible ERE cardinality defect wrongly requires at least two significant digits. It leaves `90` valid but rejects `9`, `8`, and `1` after zero stripping. No expectations or detector bytes were changed. This is a mutation of the fix, **not a rerun of the historical recursive-extglob crash**.

Exact commands, all from the sandbox unless the command names the lane:

```sh
mkdir /tmp/chousa-r27-falsify-FC2Leading128KZeros06 && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC2Leading128KZeros06
# exit 0
sha256sum tools/research-gate.sh corpus/evidence/round27-regressions.py
# exit 0; hashes below
python3 leading128k-probe.py pristine
# exit 0
# Apply the one-character patch above with edit.
python3 leading128k-probe.py mutated
# exit 1: five neighboring semantic mismatches; assigned detector still PASS
# Restore the original character with edit.
python3 leading128k-probe.py restored
# exit 0
sha256sum tools/research-gate.sh corpus/evidence/round27-regressions.py leading128k-probe.py
# exit 0; hashes below
```

Each gate invocation is exactly the persisted wrapper's command shape:

```sh
bash /tmp/chousa-r27-falsify-FC2Leading128KZeros06/tools/research-gate.sh verify-metadata /tmp/chousa-r27-falsify-FC2Leading128KZeros06/leading128k-fixture/corpus/knowledge/entry.md --root /tmp/chousa-r27-falsify-FC2Leading128KZeros06/leading128k-fixture --as-of DATE
```

Inherited `CHOUSA_*` variables are removed, `CHOUSA_STRICT=0`, `LC_ALL=C`; subprocess timeout 30 seconds, enclosing command timeout 120 seconds. No timeout occurred.

| Phase | Assigned gate exit | Assigned observer | Nearby mismatches | Whole scoped detector exit |
|---|---:|---|---:|---:|
| Pristine | 1 | PASS | 0/9 | 0 |
| Mutated | 1 | PASS — mutant survives | 5/9 | 1 |
| Restored | 1 | PASS | 0/9 | 0 |

For the assigned witness, all three phases actually emitted:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled due=2026-04-02 freshness=overdue verdict=drift
FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=entry.md due=2026-04-02 as_of=2026-10-21
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
```

All captured stderr was empty. The mutation was behavior-bearing, not a parse/setup error: the following same-class inputs changed from correct dated results to successful `unknown` results.

## 3. Precise nearby sensitivity counterexample

Synthetic file (the expression means exactly 131,072 ASCII zero bytes):

```python
'source: S001\nverified-at: 2026-01-02 checked synthetic fixture\nrecheck: ' + '0' * 131072 + '9d\n\n## Claim\nsynthetic\n'
```

With `--as-of 2026-10-21`, the independent contract expectation is due **2026-01-11**, overdue, exit **1**.

- **Landed/restored:** that exact due/freshness, `META_RECHECK_OVERDUE`, DRIFT, exit **1**.
- **Mutant:** exit **0**, no overdue finding, and:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
```

The unchanged assigned `90d` control therefore cannot distinguish this real normalization defect. The nearby `9d` detector does: `exit 0 != 1` and `missing 'due=2026-01-11 freshness=overdue'`.

Other neighboring inputs, each prefixed with 131,072 zeros except the stated adjacent lengths:

| Suffix / verified / as-of | Expected due, freshness | Mutant |
|---|---|---|
| `9d` / 2026-01-02 / 2026-01-11 | 2026-01-11, current | unknown; detected despite unchanged exit 0 |
| `8d` / 2026-01-02 / 2026-10-21 | 2026-01-10, overdue | unknown; detected |
| `1d` / 2028-02-28 / 2028-03-01 | 2028-02-29, overdue | unknown; detected |
| `09d` / 2026-01-02 / 2026-10-21 | 2026-01-11, overdue | unknown; detected |
| `90d` / 2026-01-02 / 2026-04-02 | 2026-04-02, current | correct |
| `90d`, 131,071-zero prefix / 2026-01-02 / 2026-10-21 | 2026-04-02, overdue | correct |
| `90d`, 131,073-zero prefix / 2026-01-02 / 2026-10-21 | 2026-04-02, overdue | correct |
| `900d` / 2026-01-02 / 2026-10-21 | 2028-06-20, current | correct |

The overdue `9d` row above plus these eight rows comprise the nine neighbors. All nine were correct on pristine and restored bytes. The assigned test is **not vacuous for its exact witness**; its demonstrated blind spot is the normalization suffix-cardinality dimension.

## Restoration and evidence

SHA-256:

| Object / phase | Digest |
|---|---|
| Gate before | `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` |
| Gate mutant | `bf5354f4c2b4eadf51cc228afc29d81b5e41ca0de1c4694b8f8ba449bb44ab77` |
| Gate restored | `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` |
| Persisted regression, every phase | `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df` |
| Scratch detector | `c6b2f43f1dfd205375b8eefff425fd6de39715c81f417ace8c0a0f6606c9fa93` |

Scratch files retained: `leading128k-probe.py`, `leading128k-pristine.json`, `leading128k-mutated.json`, `leading128k-restored.json`. The JSON captures contain actual stdout/stderr, expected/actual gate exits, observer errors, and gate/control hashes. The inverse edit restored the original gate hash before the restored behavioral run.

## Limits and author-lane advice

- Exactly one mutation; no second runtime/agent, full selftest, full regressions, historical crash replay, external targets, secret files, direct process inspection, debugger, or production-source edits. Only this requested report is written to the lane.
- Gate commands necessarily use their existing fd-bound reader internally; no separate `/proc` or live-process probe was introduced.
- No claim that the **whole suite** misses this mutant. [INFERENCE] Existing `decimal08`, `decimal09-overdue`, and leap-date cases appear capable of detecting it; those controls were not run here.
- If this named long-prefix control is cited as evidence across significant suffix widths, pair it with a long-prefix single-digit case such as the `9d` input above. Do not weaken the existing `90d` expectation or construe this survivor as a landed bug.
- No tools installed or updated. Observed existing runtimes: Bash 5.3.20(1)-release, Python 3.14.8. The informational command `bash --version && python3 --version && timeout --version` exited 125 because the installed `timeout` rejected a version-only invocation; it was not used by the detector, which uses Python's subprocess timeout.

Author-lane advice only; not an outside-admission verdict.
