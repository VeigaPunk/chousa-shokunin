# ConnectIntegration — C1/C2/C3 patch ownership, conflicts, integration order

Scope: read-only mapping of `tools/research-gate.sh` at base `64eec5d4` and the current lane tree
(C1 already applied by L1). No gate, selftest, build, lint or formatter was run; every statement
below is from source text and working-tree diffs.

## 1. Owned surfaces (base line numbers; current tree where shifted)

| Surface | Base range | Owner | Required edit | Must not change |
|---|---|---|---|---|
| `is_denylist_path` | 595-607 | C3 | add full-string `is_denylist_fs_path`; keep this as citation wrapper over `ptr_file_part` | `ptr_resolves_meta` 609, `check_pointer` 643, `chain_ref_file` 1596, `chain_citation` 1598 |
| `claim_source_path` (deny at 1129) | 1125-1225 | C3 | raw-path predicate; callers at 1379 (claims), 1694 (chain, ref already file-part via `chain_ref_file`), 2921 (verify-all) | refusal ids/observations, nlink/size/device probe order |
| `metadata_iso_date` | 2295-2309 | C2 | helper-local `LC_ALL=C`; same boolean contract | callers 2345, 2720, 2739, 2747, 6297 |
| `metadata_days_from_iso` | 2338-2341 | C2 | no edit required (input already validated) | 2755 |
| `metadata_add_days` | 2343-2360 | C2 | replace `${digits##+(0)}` at 2348 with stack-safe, O(n) normalization; keep post-strip `<=7`, range equality, `META_DATE_RESULT` | `10#$` value semantics, return 1 on overflow |
| `metadata_registry_load` | 2361-2470 | C3 | reset `id_col/status_col/usedby_col/header_candidate` on non-table lines while `header_found=0` (2412-2416); compare separator width to candidate width (2437-2447) | refuse order 2375-2407 (denylist, open, fdcanon, stat, multilink, size, NUL/read), `((header_found)) && break`, duplicate-first-row at 2426-2434 |
| `metadata_registry_check_source` | 2472-2508 | C3 | replace consumed-text rescan at 2499 with exact standalone ASCII token iteration; one finding per occurrence; keep `META_SOURCE_NO_ROW_ID` when zero tokens | used-by `./` normalization and exact entry-path match 2494-2498 |
| `metadata_registry_entry_path`, `metadata_verified_at_bare` | 2509-2529 | C3 | no edit | — |
| `verify_metadata` | 2530-2786 | C2+C3 | C2: 2549-2551, 2720, 2739, 2747-2748, 2755 call sites only if needed; C3: 2571-2572, 2584, 2591, 2694-2695 | function already has `local LC_ALL=C` at 2539; do not reformat |
| `metadata_asof_case` | 5983-6009 | C1 (no edit) | leave assertion helper alone | already anchored `^RESEARCH_GATE: ` |
| `metadata_asof_usage_accepts` | absent / current 6010-6014 | C1 | candidate for inline-only use (see §2.1) | — |
| `metadata_asof_usage_case` | 6010-6024 / current 6015-6028 | C1 | anchored verdict count; keep exit2, diagnostic, case identity | must stay self-contained for the extracted harness (§2.1) |
| `metadata_asof_usage_control_case` | absent / current 6029-6042 | C1 | controls only | — |
| selftest tail | cases end base 6237 / current 6256 | C1+C2+C3 | append-only, after 6256 and after current C1 controls 6257-6267 | original cases 1..187 keep names and ordinals |
| `run_selftest` locals | 3367 | C2 | place `zero_prefix`/`unicode_locale` here, not mid-function | counter lines |
| harness `corpus/evidence/round27-regressions.py` | L1-owned | — | see §2.1 | executors must not edit it |

## 2. Conflicts

### 2.1 HARD — C1 extraction coupling (current tree is broken for the persisted suite)

`corpus/evidence/round27-regressions.py:72-90` extracts the shipped helper source and runs it in a
stub that defines only `cases`, `failures`, `SELF`. The harness now extracts
`('metadata_asof_usage_accepts', 'metadata_asof_usage_case')` (line 74) and the current tree's
`metadata_asof_usage_case` (6015-6028) delegates to `metadata_asof_usage_accepts` (6010-6014).
Consequences:

- On the **base archive** (no `metadata_asof_usage_accepts`) the harness calls
  `parser.error('usage selftest helper not found…')` and exits 2 setup: the mandatory base run
  produces no C1/C2/C3 baseline results at all.
- If the harness is reverted to a single extraction without changing the gate, the final tree's
  extracted helper loses the accepts definition and every C1 scenario fails with `command not found`
  (`correct-usage-with-help` expected 0 failures is the load-bearing one).

Choose exactly one resolution and apply it before verification:

- **A (recommended):** inline the anchored count in `metadata_asof_usage_case`
  (`local … nverdict; nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true); if [[ $rc -eq 2 &&
  $out == *"$expected"* && ${nverdict:-0} -eq 0 ]]`), keep `metadata_asof_usage_accepts` only for
  `metadata_asof_usage_control_case`, and revert the harness to extracting `metadata_asof_usage_case`
  only. Base then runs and reports the two expected C1 mismatches; final reports zero.
- **B (fallback, keeps current tree):** make the accepts extraction optional
  (`if match is not None: helpers.append(...)`), so base runs usage_case alone while final extracts
  both. Do not leave the strict dual extraction as-is.

### 2.2 HARD — C2 repeats the C1 predicate (ExecDates working diff, notified)

`metadata_asof_locale_usage_case` checks `$out != *'RESEARCH_GATE: '*`; real `usage()` ends with
`Verdict: RESEARCH_GATE: CLEAN|DRIFT` (`tools/research-gate.sh:385`), so the Unicode case fails
whenever it executes (a UTF-8 locale is installed: `en_US.utf8`). It must count
`^RESEARCH_GATE: ` records. Its `skip-case` branch also neither increments `cases` nor `SKIPPED`,
making the new control host-dependent and invisible in the summary; run the case unconditionally
under the discovered UTF-8 locale, else `LC_ALL=C`.

### 2.3 Anchor collisions

- Base 6025 (before `mkdir -p "$WORK/meta-asof"`) and base 6088 (after the three usage cases) are
  target lines for both C1 and C2 patches. L1 already relocated C1's five controls to current
  6257-6267. Apply C2's helper at current 6042/6044 boundary and C2's execution cases at the tail;
  do not re-insert at base 6088.
- C2 and C3 both append before the summary at current 6271. Serialize: C1 controls (188-192),
  then C2 date controls, then C3 registry controls; never interleave.
- Adjacent-but-safe: C2's last change in `metadata_add_days` (2360) touches C3's leading hunk context
  for `metadata_registry_load` (2361+). Keep C2 from inserting lines after 2360; ordinary 3-line
  context survives.
- `verify_metadata` is shared but the line sets are disjoint (C2 2549-2551/2720/2739/2747-2748/2755;
  C3 2571-2572/2584/2591/2694-2695). Neither may reflow the function.

### 2.4 C3 semantics that the patch must not lose (base defects are ground truth)

- Consumed-text rescan: for `see S001S002 and S001`, the shortest-prefix strip removes through the
  glued ` S001`, the remainder starts at `S002`, and `^` re-anchors it — invented S002 and duplicate
  emissions (r26 FRegistryIdBoundary b1/b2/b5/b6/b3/b11/b12). Position-exact iteration is required;
  a literal `${scan#*"$match"}` rewrite is not a fix. A boring O(n) shape that preserves cardinality:
  `local LC_ALL=C; spaced=${source_value//[^A-Za-z0-9_]/ }; read -r -a tokens <<<"$spaced"` then keep
  tokens matching `^S[0-9]{3,}$`. This also makes non-ASCII a boundary, as the spec correction says.
- Filesystem predicate: full string, applied before `exec {fd}<"$canon"` and to `fdcanon`. The
  citation wrapper must keep `ptr_file_part` extraction, otherwise `secret.env:12` stops being denied
  while `synthetic:fixture.env` becomes denied. Do not "fix" `ptr_file_part` to strip only numeric
  suffixes; non-numeric anchors exist in chain pointers.
- Header state: reset only while `header_found=0`; the first complete table wins and a non-table line
  ends parsing. Width mismatch in either direction must leave `header_found=0` and reach
  `die_usage "metadata registry has no table with id, status, and used-by columns"` (2469).
- Preserve `META_REGISTRY_*` global maps, first-row duplicate policy, and NUL/size/multilink refusal
  ids (`metadata registry refused: …`).

## 3. No-duplicate-fix rules

1. Exactly one anchored-verdict implementation in the shipped extraction path; the harness must not
   depend on a second helper name (see 2.1).
2. `LC_ALL=C` in date helpers is C2-only; C2 must not touch the registry parser, which already has
   its own `local LC_ALL=C` at 2366.
3. Full-path denylisting is C3-only; C2 must not touch `is_denylist_path` or any of its call sites.
4. Registry parser/scanner is C3-only; C2 must not edit `metadata_registry_load`/`_check_source`,
   including line 2366.
5. Neither C1 nor C2 may add cases before line 6256; all new cases append and increment as they run.
6. Executors must not edit `corpus/evidence/round27-regressions.py`; it is the unchanged counting
   command and L1-owned.

## 4. Integration order

1. Resolve §2.1 in the lane tree (inline predicate + harness single extraction, or optional accepts
   extraction). This is prerequisite to both the base baseline run and the final run.
2. Apply C2 patch: hunk at 2295, hunk at 2343-2351, helper insert at current 6043, cases append after
   current 6267. Fix §2.2 before applying.
3. Apply C3 patch: predicate at 595-608, callers 1129 / 2375 / 2382 / 2584 / 2591, parser 2361-2508,
   cases append after C2's new cases (before 6271). No C2 line overlap.
4. Keep C1's already-relocated controls at 6257-6267 unchanged; do not reapply the original
   `ExecUsage.patch` (its case hunk targets base 6088 and would duplicate).
5. Run verification once (below).

## 5. Acceptance checks for L1 (I ran none)

- `bash -n tools/research-gate.sh`; then `bash tools/research-gate.sh --selftest` → PASS; original
  case names/ordinals 1..187 unchanged; controls 188+ pass; no `skip-case` output.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` → exit 0,
  `mismatches: 0`; C1/C2/C3 totals include the new controls.
- Same harness, unchanged, on an isolated `64eec5d4` archive → must exit 1 with recorded mismatches
  (not exit 2 setup); record the actual per-claim counts, do not assume a number.
- Existing differentials on isolated copies: `corpus/evidence/round26-date-differential.sh`,
  `corpus/evidence/round26-registry-differential.sh`; frozen metadata checks; record exit codes.
- Confirm usage exits still print zero `^RESEARCH_GATE: ` lines while normal runs print exactly one.

## 6. Risks / open items

- Current lane tree fails the persisted C1 scenarios as written (§2.1) — highest-priority fix.
- C2's new helper fails whenever executed (§2.2) and its skip path is nondeterministic.
- `ExecRegistry` has produced no patch yet; its surface is unmodified in the lane tree. The mapping
  above is pre-emptive; if its patch changes `is_denylist_path` globally or rewrites `ptr_file_part`,
  reject that hunk and keep the wrapper/predicate split.
- Tail append order is the only remaining patch-geometry conflict between C2 and C3.
- Claim separability is preserved: C1 touches only the usage helper/controls; C2 only date helpers;
  C3 only the predicate, registry parser and their call sites.

---

## 7. Update — executor patches reviewed after §1-6 (still read-only, nothing run)

### 7.1 C1 (ExecUsage `patches/ExecUsage.patch`, clone 45+/3-)

The revised patch inlines the anchored count in `metadata_asof_usage_case` (`local … nverdict;
nverdict=$(grep -c '^RESEARCH_GATE: ' … || true)`), so the extracted helper is self-contained.
`metadata_asof_usage_accepts` is now **dead code**: the new `metadata_asof_usage_control_case`
overrides `SELF` with `$WORK/meta-asof/usage-stub.sh`, calls the real helper in a command
substitution, and judges `ok-case` presence. Five controls: help-accept, CLEAN-reject, DRIFT-reject,
wrong-exit, missing-diagnostic. Consequences for integration:

- The lane tree (6010-6042) still contains the superseded delegation and the old five controls at
  6257-6267. Applying the revised patch on top would duplicate `metadata-asof-usage-help-control`
  and leave the broken delegation. Replace the C1 block wholesale: delete current 6010-6042 and
  current 6257-6267, then apply the revised patch.
- Delete `metadata_asof_usage_accepts` (unused) **and** revert the harness to extracting
  `metadata_asof_usage_case` only, or keep it dead and make the harness extraction optional. Do not
  keep the strict dual extraction: base archive still exits 2 before any scenario runs.
- Command substitution isolates the inner helper's `cases`/`failures`; each control counts once.
  Stub is invoked via `bash "$SELF"`, so no exec bit is needed; directory exists by call time.
- The helper's shape stays `^  metadata_asof_usage_case\(\)` … `^  }`; inlining preserves the
  extraction regex.

### 7.2 C2 (ExecDates clone, 66+/3-)

- The Unicode control now calls the real `metadata_asof_usage_case` under `LC_ALL=<locale>` and
  therefore **functionally depends on C1's inline fix**; if C1 is not applied, this case fails.
  Keep that ordering. Fallback/`SKIPPED` branch removed; a `-C` case always runs.
- Residual calibration risk: the discovered-locale case name is
  `metadata-asof-unicode-date-${unicode_locale}`, so the case identity varies by host; the `-C`
  case is stable. Acceptable if the report records the observed name, but a fixed name is better.
- Drop the whitespace-only hunks at base 6026 and 6092. The 6026 hunk cannot apply to the current
  tree (C1's control helper now sits between `}` and `mkdir`); the 6092 hunk is harmless noise.
- New date cases append at base 6242; in the current tree that anchor is before C1's controls. Append
  after current 6267 to keep the tail one block.
- `local … zero_prefix unicode_locale candidate_locale` correctly moved to the `run_selftest` local
  line (3368). Plain-mode control (`metadata-asof-128k-zero-prefix-plain`) is additive and anchored
  (`^RESEARCH_GATE: ` exactly 1, no date fields); it does not weaken the as-of case.
- Normalization `[[ $digits =~ ^0*([0-9]*)$ ]]` + capture is O(n) and preserves value-before-length
  bounding; no change needed.

### 7.3 C3 (ExecRegistry clone, 40+/19-)

- Predicate split is exactly the safe shape: `is_denylist_path_value` holds the patterns,
  `is_denylist_fs_path` checks full string then file part, and `is_denylist_path` remains the
  citation wrapper (`ptr_file_part`). `check_pointer`, `chain_citation` and the first
  `ptr_resolves_meta` check were left on the wrapper. Migrated: `ptr_resolves_meta` canon (643),
  `claim_source_path` raw + new canon check (1136/1166), registry load (2387/2390/2402),
  metadata entry reads (2605/2612). No C2-owned line touched.
- Parser: `header_width` recorded at candidate, compared before separator cells, reset on non-table
  break and on candidate rejection; matches the harness's short/long/reorder expectations.
- Scanner: replaced consumption with
  `done < <(printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+' || true)` and
  `[[ $source_id =~ ^S[0-9]{3,}$ ]]`. Tokenization is maximal ASCII word runs, so glued/underscore
  forms cannot be re-anchored and each real occurrence yields one finding. The loop runs in the
  current shell (process substitution, not a pipe), preserving `found_id` and
  `META_SOURCE_NO_ROW_ID`. `local LC_ALL=C` is required for both the grep and the test; it is present.
- Remaining acceptance risk: confirm `grep -oE` with no match does not trip `set -e` via the
  process substitution; the `|| true` covers the pipeline, and the loop simply does not execute.
- No patch file is written yet; when it lands, its only shared anchor with C2 is the tail append
  block (current 6268-6270) and its only shared anchor with C1 is none.

### 7.4 Revised tail order and merge

1. Replace C1 block + controls (7.1), resolve extraction (7.1).
2. Apply C2 substantive hunks; append its cases after C1's controls.
3. Apply C3 hunks; append its cases after C2's.
4. Drop C2's two whitespace-only hunks and any ExecUsage hunk that re-adds the old controls.
5. One verification pass per §5; the base-archive harness run must produce results, not exit 2.

### 7.5 C3 selftests (ExecRegistry clone now 193+/19-)

`metadata_registry_finding_count_case` is defined at the head of C3's new block (base 6256 boundary),
then 150+ lines of fixtures. They stay inside C3's surface and reuse existing `metadata_case` and
`tclaims` without editing them. Integration notes:

- The helper and fixtures insert at the same tail anchor as C1/C2; move the whole block after C2's
  appended cases (current 6267+) so the helper precedes its uses and original cases 1..187 keep
  ordinals. Its `grep -Fxc` exact-line counts are stricter than the persisted harness's regex counts;
  the expected finding strings must match emitted `FINDING … obs=…` lines verbatim.
- Two fixtures pin the predicate split: `metadata-colon-anchor-denylist-compat`
  (`metadata.env:1.md` refused) requires `is_denylist_fs_path` to keep the file-part fallback — do not
  simplify it to full-string-only. `claim:synthetic/alias.md` refreshed through a symlink requires the
  canon denylist check added at `claim_source_path` (1166) to stay.
- New registry header/width/reorder fixtures and the S-id cardinality fixtures match the harness
  expectations analyzed in §7.3; no overlap with C2's date cases.
- No C3 hunk touches `metadata_asof_*`, `metadata_iso_date`, or `metadata_add_days`; no C2 hunk
  touches `is_denylist*` or `metadata_registry_*`.
