# FC2AsciiCliC102122 — falsify `ascii-cli-C-٢٠٢٦-10-21` (C2) at dd72641e

Target: dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (verified in sandbox).
Sandbox: `/tmp/chousa-r27-falsify-FC2AsciiCliC102122` (`git archive` of the target; pre-fix base 64eec5d4 also extracted there). No lane files edited. bash 5.3.20, glibc 2.44, Python 3.14.8; installed locales: C, C.utf8, en_US.utf8, POSIX. No tools installed.

## Verdict

- **Named control `ascii-cli-C-٢٠٢٦-10-21`: FALSIFIED as a control for the C2 locale repair (vacuous).** It is green on the pre-fix base gate and green with the targeted `local LC_ALL=C` reverted. Under `LC_ALL=C` the pre-fix `[0-9]` regex cannot match multibyte digits either, so this row exercises nothing the base gate did not already do.
- **Landed gate behavior for the named input class: HOLDS.** `--as-of ٢٠٢٦-10-21` exits 2 with the usage diagnostic and no verdict under C and en_US.UTF-8; every other Unicode-decimal script and malformed ASCII-adjacent token I tried is also rejected.
- **Control-family defect (same loop, lines 123–128): one-sided coverage.** All six rows test only rejection. A wrong fix that rejects valid dates whenever the inherited locale is not C passes all six (mutant B below); the harness has no positive non-C-locale acceptance row. [INFERENCE from code inspection, whole script not run per bounds: that mutant would also pass the remaining 52 controls, because line 125 is the only `run(..., locale=...)` call and `date_cases` call `run('--as-of', asof)` with the default `locale='C'`.]

## (1) Is the expectation derived from the declared contract, independent of gate code?

Yes for the behavioral expectation, with one caveat.

- Exit 2, no `^RESEARCH_GATE: ` record, and the ASCII-only `YYYY-MM-DD` grammar are the declared usage contract: `corpus/evidence/round27-claims.md:11` ("Date grammar is ASCII YYYY-MM-DD under any inherited locale") plus the unchanged usage-error semantics. The diagnostic string `--as-of must be a valid YYYY-MM-DD date` is a shipped user-facing message that already existed in the base gate (base selftest case `metadata-asof-invalid`) and in the accepted r26 reports; it is a copied contract string, not a value computed from the implementation under test.
- The harness computes nothing from gate source in this block: `text = gate.read_text()` (line 26) is consumed only to extract the C1 helper bodies (lines 47–54). No gate predicate is called as the oracle.
- Caveat: the C-locale *case selection* is not derived from the contract's risk surface. "Under any inherited locale" is the claim; the failure only exists in a locale whose collation admits non-ASCII digits into `[0-9]`. C is precisely the locale where pre- and post-fix behavior are identical, so the row is a valid guard for `metadata_iso_date`-exists but not evidence for C2.

## (2) Mutation evidence

Targeted production fix = `local LC_ALL=C` at `tools/research-gate.sh:2311` in `metadata_iso_date` (the diff 64eec5d4→dd72641e adds exactly this line; the outer `--as-of` check at `:6573–6575` runs before `verify_metadata`'s own C pin at `:2564`, which is why the helper pin matters). Mutation drivers: single gate invocations with the harness's exact `run()` environment (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL` per row, cwd = synthetic root, absolute gate path). No full selftest or full regression script was run.

Sandbox gate hashes:

| variant | sha256 |
|---|---|
| landed | ca39d14d…2f84 |
| pre-fix base 64eec5d4 | c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6 |
| A: delete the `:2311` pin | 50276d4780b11fa24be38f4d4c9297ff3972096ff55b8605bc85f48c8af46cf3 |
| B: helper returns 1 unless inherited `LC_ALL` is `C` (wrong "fix") | d1536745f8b7bed74cfa097c7b763527ab7d1fa540cc79ffb912057fd13740c2 |
| C: remove the outer `--as-of` validation (`:6575`) | daa9b2ce7b5b207b1b16777308656e942c32e9d33853b752c015f9a426ad9bda |

Fixture: `probe/corpus/knowledge/entry.md` with `source: S001`, `verified-at: 2026-01-02 checked synthetic fixture`, `recheck: 90d`.

Matrix (PASS = the row's observe() would record no error):

| gate | C × ٢٠٢٦ | en_US.UTF-8 × ٢٠٢٦ |
|---|---|---|
| landed | **PASS** (rc2, diagnostic, 0 verdicts) | **PASS** (rc2, diagnostic, 0 verdicts) |
| base 64eec5d4 | **PASS** | FAIL: rc1, `10#: invalid integer constant` |
| A: pin deleted | **PASS** | FAIL: rc1, `10#: invalid integer constant` |
| B: reject non-C locale | **PASS** | **PASS** (but rejects valid ASCII dates too) |
| C: outer validation removed | FAIL: rc1, `line 2312: 10#: invalid integer constant`, 0 verdicts | FAIL: same |

Exact commands and exit codes (sandbox root):

```
$ LC_ALL=C bash tools/research-gate.base.sh verify-metadata probe/corpus/knowledge/entry.md \
    --root probe --as-of '٢٠٢٦-10-21'                                   # rc=2
research-gate: --as-of must be a valid YYYY-MM-DD date                  # 0 RESEARCH_GATE: lines
$ LC_ALL=C bash tools/research-gate.mutant.sh verify-metadata ...       # rc=2  <- named control still PASSES with fix reverted
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.mutant.sh verify-metadata ...  # rc=1
tools/research-gate.mutant.sh: line 2312: 10#: invalid integer constant (error token is "10#")
tools/research-gate.mutant.sh: line 2574: 10#: invalid integer constant (error token is "10#")
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.sh verify-metadata ...    # rc=2, usage diagnostic (landed)
```

Answer to "(does reverting the fix make the control fail for the intended reason?)": **No for the named row.** With the `:2311` pin deleted, `ascii-cli-C-٢٠٢٦-10-21` stays green (rc2 + diagnostic + zero verdicts); only its `en_US.UTF-8` sibling fails, with rc1 and the leaked `10#` arithmetic error. The named row is behaviourally identical on base and target, so it has zero discriminating power for the repair. A source-substring probe (`round27-mechanisms.py:30`, `'local LC_ALL=C' not in iso`) would catch the deletion; the behavioural named control adds nothing to that.

Why the sibling discriminates: glibc's `en_US.utf8` collation admits non-ASCII decimal scripts into `[0-9]`; `C`/`C.utf8` do not. Probe under en_US.UTF-8 (`[[ X =~ ^[0-9]{4}$ ]]`): ADMIT for U+0660 Arabic-Indic, U+06F0 extended Arabic-Indic, U+0966 Devanagari, U+09E6 Bengali, U+0E50 Thai, U+FF10 fullwidth, U+1D7DA math-bold; all rejected under C and C.utf8. Landed gate rejects every one of those as `--as-of` (rc2, diagnostic, 0 verdicts), and the base gate fails each under en_US.UTF-8 — the same asymmetry as the named token.

## (3) Nearby same-class inputs and counterexamples

1. **Named-input vacuity (counterexample to the control, not the gate).** The named C row passes on base 64eec5d4 and on mutant A. Any evidence line that counts it as C2 repair evidence is miscalibrated.
2. **One-sided coverage (counterexample to the control family).** Mutant B (`metadata_iso_date` starts with `[[ ${LC_ALL:-} == C ]] || return 1`) keeps all six ascii-cli rows green while breaking the contract in the opposite direction: landed gives `--as-of 2026-10-21` under en_US.UTF-8 → rc1 `META ... due=2026-04-02 freshness=overdue verdict=drift`; mutant B gives rc2 `research-gate: --as-of must be a valid YYYY-MM-DD date`. The suite's date cases cannot catch this because they run in C. A positive row in the discovered UTF-8 locale (`due=2026-04-02 freshness=overdue`) is missing.
3. **Host dependence.** The same six rows hard-code `en_US.UTF-8` with no discovery/skip. On a host lacking it (simulated with uninstalled `zz_ZZ.UTF-8`), bash emits `warning: setlocale: LC_ALL: cannot change locale (zz_ZZ.UTF-8)` and the gate emits it too; that string is in the row's forbidden list, so the rows fail rather than skip. The landed gate's own selftest discovers an admitting locale from `locale -a` and skips when none exists (`tools/research-gate.sh:6307–6327`); the independent harness does not.
4. **No landed-gate error found for this input class.** `٢٠٢٦-10-21`, `２０２６-10-21`, and `2026-10-2１`, plus Devanagari/Bengali/Thai/math-bold digit years and U+FF0D/U+2010/U+2212 hyphen forms, all exit 2 with the diagnostic under C, en_US.UTF-8 and C.utf8. ASCII-adjacent malformed tokens (`'2026-10-21\n'`, trailing `\r`, leading/trailing space, `x` suffix, fullwidth-first-digit mix) also exit 2; valid ASCII dates (`2024-02-29`, `2028-02-29`, `9999-12-31`, `0001-01-01`) are accepted with the expected freshness under en_US.UTF-8. The helper's function-local C pin does not leak (it is restored on return).
5. **Diagnostic reason, not just exit code.** With the pin reverted, the Arabic-Indic token's en_US failure is the intended one: rc1, `10#: invalid integer constant`, no usage diagnostic — i.e. a locale-admitted digit reached `$((10#...))`. Its output is strict-UTF-8 clean, so this pair is a sound discriminator. By contrast the mixed token `2026-10-2１` corrupts stderr at `:2574` with a split UTF-8 sequence (`10#2\xef: arithmetic syntax`), which makes `subprocess.run(..., text=True)` raise `UnicodeDecodeError` instead of recording a mismatch (cf. sibling report FC2AsciiCliC102121; reproduced here).

## Author-lane advice (controls only; no gate change required)

1. Relabel the three `C` rows as non-discriminating guards, or exclude them from the C2 discriminating count; keep the Arabic-Indic `C`/`en_US.UTF-8` pair, whose UTF-8 row fails cleanly for the intended reason.
2. Add a positive row in the discriminator locale: valid `--as-of 2026-10-21` must yield rc1 and `due=2026-04-02 freshness=overdue` (kills mutant B). Also assert a C-locale valid-date row for the same fixture, so the pair cannot be satisfied by a "reject non-C" fix.
3. Discover the discriminating locale the way the shipped selftest does (`locale -a` + regex probe) and record an explicit skip/setup outcome when none exists, instead of hard-coding `en_US.UTF-8` and tripping the `cannot change locale` forbidden string on minimal hosts.
4. Decode subprocess output with `errors='surrogateescape'`/`'replace'` so a gate that emits invalid UTF-8 is recorded as a mismatch rather than aborting the harness before later controls run.

## Limits

- One host/toolchain: bash 5.3.20, glibc 2.44; only C, C.utf8, en_US.utf8, POSIX installed. Which locales admit non-ASCII `[0-9]` is a glibc-collation property and may differ elsewhere (musl, other glibc versions).
- The full regression suite and full `--selftest` were not run (L1 owns them); the "mutant B passes 58/58" statement is inference from `run()`'s default `locale='C'` and the absence of any other non-C `run()` call (line 125 is the only one).
- The base-gate runs used the accepted pre-fix revision only for control discrimination, not to re-confirm the reported r26 failures.
- All fixtures are synthetic and inside the sandbox; no network, host secrets, live processes, debuggers, or mounts were used.
