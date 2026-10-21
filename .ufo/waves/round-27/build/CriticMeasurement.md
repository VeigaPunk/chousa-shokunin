# CriticMeasurement: attack on the r27 counting design (critic, author-lane advice only)

Seat `ChousaR27.CriticMeasurement`, leaf. Static read-only analysis. I ran no gate, selftest,
regression, mechanism or differential script. I installed nothing. Axes: operability, freshness,
calibration. This is not an admission or a judgment.

## Pinned inputs (observed 2026-10-21T11:42-03:00; the files were changing while I read them)

- Base `64eec5d` gate sha256 is `c2c813f1…abc6`. It equals the r26 measured revision `0e9784bd`
  (`git show … | sha256sum`), so the r26 falsify receipts describe the base byte-for-byte. It also
  equals `.ufo/waves/round-27/baseline-research-gate.sh`.
- `corpus/evidence/round27-regressions.py`: I read two versions. Version 1 was not hashed and
  extracted only `metadata_asof_usage_case`. Version 2, sha256 `3198bf21…a751`, extracts
  `metadata_asof_usage_accepts` and `metadata_asof_usage_case` (`:74-78`).
- `corpus/evidence/round27-mechanisms.py`: sha256 `00d71328…c6c4`.
- The lane `tools/research-gate.sh` is under L1 edit. I saw `8ee706b2…`, then `045c073e…`. The
  C1 diff I reviewed adds `metadata_asof_usage_accepts` and three `*-control` cases, and removes
  exactly one line: the faulty predicate.
- Committed baseline receipts:
  - C1: `corpus/evidence/round26-inherited-after.log:42`
    `RESEARCH_GATE_SELFTEST: FAIL (3/187 cases)`, and `:43` `LEGACY_CASES_SHA=5eac4a7e…`.
  - C2 and C3: the falsify reports `FDateAsOfUsage`, `FDateHugeCadence`, `FRegistryHeaderless`,
    `FRegistryIdBoundary` and `FRegistryRegistryDeny`, under `.ufo/waves/round-26/falsify/`.

## Counterexamples (fixable defects unless marked)

### M1 (crit, operability and measurement): "run unchanged on base" exits 2 before any case runs

- `round27-regressions.py:74-77` calls `parser.error` when `metadata_asof_usage_accepts` is
  missing.
- That function does not exist in the base gate. My `grep` of `baseline-research-gate.sh` found
  0 matches.
- So the claims' base run (`round27-claims.md:22`) exits 2 with zero observations. The script's
  C1 controls are keyed to the fix's internal helper name, so they cannot run on both trees.
- Version 1 had the mirror-image fault. On the fixed tree, the extracted helper calls an
  undefined function, so `if` is false and every scenario exits 1. The four `reject-*`
  scenarios would then match vacuously.

**Smallest correction:**

- Extract every `^  metadata_asof_usage_\w+\(\)` definition that is present. Require only
  `metadata_asof_usage_case`.
- Add `forbidden=('command not found',)` to the C1 observations, so that a missing helper is a
  mismatch and not a vacuous rejection.

### M2 (crit, freshness and safety): there is no baseline-skip mechanism, so the forbidden crash reproduction would run

- The claims require that the "unsafe old long-token crash reproduction is not rerun … mark its
  baseline skip explicitly" (`round27-claims.md:22`).
- The script has no skip option. `leading-128k-zeros` (`:96`) is 131,072 zeros. That is above the
  observed SIGSEGV threshold of 68,000 or more (`FDateHugeCadence.md:52`).
- `allzero-128k` (`:97`) hits the same `${digits##+(0)}` path. [INFERENCE] It crashes too. The
  r26 receipt only covers 40 all-zero digits (`z40_allzero`), so this case has no observed
  baseline at all.
- The docstring line "The reported r26 failures are … not reproduced by this script" is also
  false for a base run. On base, the script re-observes FDateAsOfUsage, all four registry
  classes, and the FNoTrade helper fault.
- Crash hygiene: `env` inherits all of `os.environ` except `CHOUSA_*` (`:27`). A segfaulting
  child can therefore persist host environment values into a core dump.

**Smallest correction:**

- Add a repeatable `--baseline-skip NAME`. Each NAME must be an existing case.
- Record each skip in the summary as `skipped:[{name, receipt}]`, pointing at
  `FDateHugeCadence.md:52`. For `allzero-128k`, mark the baseline as [INFERENCE] with no receipt.
- Refuse the skip unless `gate_sha256 == c2c813f1…`.
- Acceptance: the final summary has `skipped == []`.
- Build `env` from an allowlist (`PATH`, `HOME=<tmp root>`, `TMPDIR`, `CHOUSA_STRICT`, `LC_ALL`).
  Set `RLIMIT_CORE=0` in a `preexec_fn`. [INFERENCE] How pipe core handlers treat that limit
  is host-dependent, which is why the allowlist matters regardless.
- Rewrite the docstring: base observations are evidence that the controls are sensitive, not a
  re-confirmation of r26.

### M3 (high, measurement): "unchanged" cannot be verified, and the base-versus-final comparison is under-specified

- The script changed during this round, and I observed both versions. Its summary records only
  `gate_sha256`, with no script hash.
- Stdout lists only mismatches. Passing cases are named only in `--output`, which is optional.
- An exit of nonzero on base is satisfied by any failure, including a setup or helper error
  (M1).

**Smallest correction:**

- Add `script_sha256` (the hash of `__file__`) to the summary. Commit the script before the base
  run.
- Always persist `--output` for both runs, for example
  `corpus/evidence/round27-regressions-{base,final}.json`.
- Pre-register the exact base mismatch set and compare names, not counts.

Static derivation of that set from the r26 receipts, assuming M1 and M2 are fixed: 40 run
cases, 2 skipped, 17 expected mismatches and 23 holds. The 17 expected mismatches are:

| claim | expected base mismatches |
|---|---|
| C1 (2) | `correct-usage-with-help`, `nonrecord-mention-is-not-verdict` |
| C2 (3) | `ascii-cli-en_US.UTF-8-{２０２６-10-21, ٢٠٢٦-10-21, 2026-10-2１}` |
| C3 (12) | `header-break-{blank,prose}`, `reorder-{clean,queued}`, `delimiter-too-{short,long}`, `glued-before-terminal`, `glued-missing-before-terminal`, `nonstandalone-duplicate`, `glued-repeat-duplicate`, `colon-denied-{component,suffix}` |

If any other case mismatches on base, that control is environment-dependent or broken. If a
listed case does not mismatch, that control does not discriminate. Either way it must not count
toward the "after" number. The C2 cadence repair has **zero** runnable discriminating base
controls, so its "before" is receipt-only and must be labelled that way.

### M4 (high, freshness): a tail-truncation normalization passes all 12 date cases

A cheap non-recursive "fix" such as `digits=${digits: -7}` gets all twelve date cases right:

- 128k zeros followed by `90` gives `0000090`.
- All zeros gives `0`.
- 40 nines gives `9999999`, which is over the maximum, so unknown.
- `0003652058` gives `3652058`.

But `1` followed by 39 zeros would yield 0 days, where the correct answer is unknown. The r26
oracle had this exact discriminator (`n40_onetrail`, `FDateHugeCadence.md:141`). The 2^64+90
wrap control (`pow64p90`, `:142`) was also dropped.

**Smallest correction:** add these cases:

- `('one-then-39-zeros', '2026-01-02', '1'+'0'*39+'d', '2026-10-21', None)`
- `('long-zeros-then-8-digits', '0001-01-01', '0'*131072+'10000000d', '9999-12-31', None)`
- `('pow64-plus-90', '2026-01-02', '18446744073709551706d', '2026-10-21', None)`

These are safe on base: they are short tokens, or a long-zero token that M2 skips.

### M5 (high, calibration): the C3 controls cover only the raw registry arm and miss the claim-scope regressions

All of these pass the script with 0 mismatches.

- **A partial fix.** Repair only `"$path"` at `:2375`. The script still passes, but a symlink
  `plain.md -> synthetic:fixture/.config/registry.md` remains CLEAN through the canon arm. The
  entry reader at `:2584`/`:2591` also stays bypassed with `e/a:b/.config/e.md`
  (`FRegistryRegistryDeny.md:98-101`, FRRD-2). Paths are detailed in `CriticPathScope.md`
  CX2/CX4.
- **A global change of `is_denylist_path` to the full path** (r26 mutant M2). Citation pointers
  such as `x.env:12` stop matching `*.env`. Neither the script nor the selftest has a
  `.env:<n>` citation case. My `grep '\.env:'` of the gate found none; the only selftest pointer
  with a line number is `/home/vgpnk/.omp/agent/config.yml:1` at `:3989`, which still matches
  `*/.omp/*`.
- **A width check that requires outer pipes, or that counts raw pipes.** This rejects tables
  with no outer pipes, CRLF tables, or alignment-colon tables. The only positive control is
  `valid-table` (`:126`).

**Smallest correction:** add these synthetic cases:

- Registry symlinked-file and symlinked-directory aliases to a colon-plus-`.config` path,
  expecting `refused: denylist` and 0 verdicts.
- An entry path `synthetic:fixture/.config/e.md`, expecting `source=refused`.
- A `verify` or claims fixture whose citation is `synthetic.env:1`, expecting `SESSION_READ`
  or `CLAIM_SOURCE_SESSION` as a hold.
- Positive tables with no outer pipes, CRLF, and `:---:`, expecting rc0, 1 verdict and 0
  findings.

The fdcanon arm cannot be exercised separately without `/proc`. Report it as a source-order
limitation (see also `SentinelSynthetic.md`), not as a passed control.

### M6 (medium, freshness): the locale representation is incomplete, and an absent locale is misclassified

- Every case sets `LC_ALL` (`:28`, `:64`). The r26 default exposure was an inherited
  `LANG=en_US.UTF-8` with `LC_ALL` unset (`FDateAsOfUsage.md:99-100`). The claim says "under
  any inherited locale".
- The check for a missing `en_US.UTF-8` relies on the forbidden token `cannot change locale`.
  That makes it a C2 *mismatch* (exit 1) on both trees, which reads as a gate defect.
- Entry-side `verified-at:` with non-ASCII digits is untested. r26 marked it [INFERENCE]
  (`FDateAsOfUsage.md:105-109`).

**Correction:**

- Add one case with `LANG=en_US.UTF-8` and `LC_ALL` removed.
- Precheck the locale with `bash -c :` and exit 2 (setup) if it is unavailable.
- Add one entry with `verified-at: ２０２６-01-02` under `en_US.UTF-8`. It must not produce
  `invalid integer` and must not report `verified_at=dated`.
- Optionally add a C3 locale hold: source `S００２ and S001` under `en_US.UTF-8` gives 0
  `ROW_MISSING` and 0 `NOT_MINED`.

### M7 (medium, operability): the 187-identity claim has no baseline enumeration, and index-keyed comparison breaks

- No committed receipt lists the 187 names. `round26-inherited-after.log` has one `ok-case`
  line, only the FAIL summary, and the hash of the first 161 lines.
- L1's three `*-control` cases sit after `metadata-asof-wrong-mode`, so every later r26 case
  index shifts by 3. `LEGACY_CASES_SHA` covers only 1–161 and depends on skips
  (`CriticHarness.md:137-143`).
- Rerunning the base selftest to list names would re-observe the FAIL. Avoid it.

**Correction (no rerun):** prove identity statically from `git diff 64eec5d -- tools/research-gate.sh`.

- The selftest section must contain zero removed or modified case-invocation lines. The only
  allowed `-` line is the substring predicate at base `:6016`.
- In the final run, every base case name must appear as `ok-case`, compared by name and expected
  exit, never by index.
- Record `skip-case` count = 0, matching `round26-measure-before.log:66`.

### M8 (low, measurement): concatenated-stream anchoring, and the probe's limits

- `observe` counts `^RESEARCH_GATE: ` over `stdout + stderr` (`:32`). If stdout lacks a final
  newline, the first stderr record is glued to it and undercounted. That is the C1 bug class
  again. **Correction:** count each stream separately and sum the counts.
- In L1's helper, `${nverdict:-0}` treats a failed `grep` (empty output) as 0 verdicts, which
  fails open. **Correction:** require `[[ $nverdict == 0 ]]` with no default.
- `round27-mechanisms.py` counts names, not semantics, and says so (`:26-27`). Three limits:
  - The C3 arm regex (`:34`) scans only `metadata_registry_load`. It is blind to the entry
    reader and to `:636`.
  - Renaming the predicate could leave the count at 3 after a correct fix.
  - `C2_locale_unpinned` (`:30`) stays at 1 if the fix pins the locale at the caller.

  Report before→after values from it only as mechanism counts, never as axis deltas.
  `C2_recursive_zero_strip` is complete: `+(0)` occurs only at `:2348`.

## Tradeoffs to reject, not fix

- Counting an all-reject C1 helper as passing because the negatives match. The base reproduces
  exactly this, so the positive control must be required to pass.
- Treating base exit ≠ 0 as "before fails" without per-name equality to the pre-registered set
  in M3.
- Any run that uses a skip in the final summary, or any numeric operability score inference.
  Score 3 is frozen.

## Checks for L1 (not run by me)

1. Fix M1 and M2, commit the script, and record `script_sha256`.
2. Run the script on the base archive with `--baseline-skip leading-128k-zeros
   --baseline-skip allzero-128k`, then on the final tree with no skip. Diff the two `--output`
   JSON files against the M3 table.
3. Run the full selftest once. Check names and skips as in M7.
4. Run the existing round 26 date and registry differentials on isolated copies, and record
   their exit codes.
