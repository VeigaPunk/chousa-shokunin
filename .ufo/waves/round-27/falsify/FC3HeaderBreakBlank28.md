# FC3HeaderBreakBlank28 — blank-break control sensitivity

**Verdict: FALSIFIED (control coverage), not a landed-gate behavioral counterexample.** The named `header-break-blank` control survives a one-line defect that bypasses precisely the blank-line header reset. A nearby, smaller fixture detects the defect for the intended semantic reason. The landed gate rejects both invalid fixtures.

Axes: operability, freshness, calibration. This probe attacks calibration only; no new C1/C2 conclusion.

Target: `dd72641e574679c4f7882dd43de072b4c8892d6f`.
Sandbox: `/tmp/chousa-r27-falsify-FC3HeaderBreakBlank28`.

## 1. Is the expectation contract-derived and independent?

**Yes.** `corpus/evidence/round27-claims.md:15` requires “fresh named headers after breaks.” The inherited registry contract in `corpus/evidence/round26-claims.md:90–93` requires exit 2 when no table has the named `id`, `status`, and `used-by` columns. In the control (`round27-regressions.py:134`), the named header is separated by a blank from a new table headed `a`, `b`, `c`; that table has none of the required names. Exit 2 follows without consulting gate implementation. The regression's literal expected exit and anchored verdict-count expectation (`:147–150`) are not computed from gate code.

The limitation is **sensitivity**, not an incorrect expected result: the unnamed row supplies a second reason to forget the old header even when blank-break handling is broken.

## 2. Mutant and bounded detector

Inserted exactly one line into the sandbox gate, after original line 2432 and before the state-reset assignments:

```bash
    if [[ $line != *'|'*'|'* ]]; then
      ((header_found)) && break
      [[ -z $line ]] && continue  # inserted mutant; actual insertion has no comment
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1
      header_width=0
      continue
    fi
```

This plausible “ignore empty lines” defect preserves a pending named header across a blank, while leaving prose handling and already-started-table termination unchanged. It directly bypasses the blank-break portion of the production fix.

Detector: sandbox `probe-header-break-blank.py`, SHA-256 `f7a5f6ec876dd832f048ac0975c06a44599424c82c0307164138a8971b48cb5f`. It AST-selects the exact shipped `header-break-blank` tuple and the shipped `observe`, `entry_text`, and `run` helpers, without executing the regression module. It runs only that control plus three nearby cases. Each gate subprocess has the original 30-second timeout; each detector invocation is bounded by 120 seconds.

All runs use the same synthetic entry:

```text
source: S001
verified-at: 2026-01-02 checked synthetic fixture
recheck: 90d

## Claim
synthetic
```

### Exact commands and exits

Sandbox creation (exit 0):

```bash
mkdir /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28 && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28
```

From that sandbox, before insertion / after insertion / after exact removal:

```text
timeout 120s python3 probe-header-break-blank.py pristine   => exit 0
timeout 120s python3 probe-header-break-blank.py mutated    => exit 1
timeout 120s python3 probe-header-break-blank.py restored   => exit 0
```

Every case invokes this exact subprocess with cwd equal to `probe-fixture`, inherited `CHOUSA_*` variables removed, and `CHOUSA_STRICT=0 LC_ALL=C`:

```bash
bash /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28/tools/research-gate.sh verify-metadata /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28/probe-fixture/corpus/knowledge/entry.md --root /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28/probe-fixture --registry /tmp/chousa-r27-falsify-FC3HeaderBreakBlank28/probe-fixture/registry.md
```

### Actual results

| Case | Expected exit | Pristine | Mutated | Restored |
|---|---:|---:|---:|---:|
| valid-table | 0 | 0 | 0 | 0 |
| shipped header-break-blank | 2 | 2 | 2 | 2 |
| blank-direct-delimiter | 2 | 2 | **0** | 2 |
| blank-fresh-header | 0 | 0 | 0 | 0 |

Every exit-2 result has empty stdout, no anchored verdict record, and starts stderr with:

```text
research-gate: metadata registry has no table with id, status, and used-by columns
```

The shipped control's `errors=[]` in **all three** phases. Therefore the named control **SURVIVES** the mutant; reverting/bypassing this targeted repair does **not** make that control fail.

The new adjacent-delimiter fixture **KILLS** the same mutant. Its actual mutated output includes:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
```

Stderr is empty. The shipped observer records exactly:

```text
['exit 0 != 2', "missing 'metadata registry has no table'", "count '^RESEARCH_GATE: ': 1 != 0"]
```

This is successful execution with incorrect registry acceptance, not a syntax, timeout, or fixture/setup error. Both positive cases remain clean under the mutant.

## 3. Minimal nearby sensitivity counterexample

The shipped fixture is:

```text
| id | status | used-by |

| a | b | c |
|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
```

Delete only `| a | b | c |\n` to obtain the smaller `blank-direct-delimiter` fixture:

```text
| id | status | used-by |

|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
```

The contract still requires exit 2: no fresh named header follows the break. The landed/restored gate does reject it; the mutant emits CLEAN. Its registry SHA-256 is `9cc72d709f2668cfca24bfd7c1974da9fbe308695b760a887789eb3f665cde8a`.

Why the shipped control misses it: even when the blank fails to clear state, `| a | b | c |` is not a delimiter, so the later candidate-rejection block (original gate lines 2464–2479) clears that state independently. The following delimiter cannot recover named columns. Thus this control does not isolate the blank-reset repair.

Author-lane advice: retain the existing case, and add the direct-delimiter case (plus the already exercised positive “blank then fresh named header” case). Do not weaken the exit-2/no-verdict contract. No production or regression fix was made in this probe.

## Restoration and retained evidence

Gate SHA-256, recorded by the same detector in each phase:

- Pristine: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`.
- Mutated: `246e91639a7470fbf06e11645553e8b1de369a6b35dc3a24073933294db399c6`.
- Restored: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` — exact original identity restored before the restored detector run.

The unchanged regression source has SHA-256 `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df` in all phase records. Full stdout/stderr, commands, fixture bytes/hashes, and observer errors remain in the sandbox:

| Evidence | SHA-256 |
|---|---|
| `probe-pristine.json` | `5d8bc31a545306d830b1b259ee0c1b1c5248a52f0c108f656ae831ed5e4f9ccb` |
| `probe-mutated.json` | `5534c3d6432bea01af5d1a4a78aba45a9c5c6105f751b4de6f1c20c64338d366` |
| `probe-restored.json` | `b9cdb94ae6b0ef76d193af9c205c34e46e56551298819e2d39560e05621e9762` |

Limits: one mutant, four cases per phase, no full selftest or whole regression run; no claim of a landed-gate failure or whole-parser safety. No subagents, network, external targets, host secret files, direct `/proc` inspection, debugger, or production source/index edits. This report is the only lane write. No tools installed/updated. Existing runtimes: Python 3.14.8 and GNU Bash 5.3.20(1)-release.
