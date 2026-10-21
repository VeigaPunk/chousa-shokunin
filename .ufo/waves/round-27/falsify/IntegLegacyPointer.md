# IntegLegacyPointer — round27 attempt1

Target: `dd72641e574679c4f7882dd43de072b4c8892d6f`, archived into the isolated `/tmp/chousa-r27-falsify-IntegLegacyPointer/target` sandbox. `sha256sum tools/research-gate.sh` there: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the assigned gate hash).

**Item attacked:** citation-pointer versus filesystem-path denylist boundary. **Verdict: HOLDS. Severity: none found in the landed target.**

## LegacyPointer attack

Static source at target `tools/research-gate.sh:573–616` retains `ptr_file_part()` and the citation wrapper `is_denylist_path()`; filesystem checks use `is_denylist_fs_path()`, which tests the full input with the single shared `is_denylist_path_value()` predicate, then tests the previous `ptr_file_part()` projection. No denylist pattern list is copied. The filesystem wrapper is used at the canonical pointer target (646), claim source input/canonical path (1139, 1166), registry input/canonical/open-fd path (2394, 2401), and metadata input/canonical/open-fd path (2609, 2616).

Synthetic fixture exploit shape: `claim:synthetic/credentials/source.md` exists under the fixture root and contains the claimed span. `ptr_file_part()` truncates this string to `claim`, so the old projection alone misses `credentials/`.

Commands and gate exits (each a single `verify-claims`/`verify` invocation; fixtures and mutant are sandbox-only):

- Target: `env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=/tmp/chousa-r27-falsify-IntegLegacyPointer/fixtures/legacy/root bash /tmp/chousa-r27-falsify-IntegLegacyPointer/target/tools/research-gate.sh verify-claims /tmp/chousa-r27-falsify-IntegLegacyPointer/fixtures/legacy/claims.jsonl` → **gate exit 1**, `CLAIM_SOURCE_SESSION`, `observed=refused`, `VERDICT_BEARING_CLAIMS=0/1`, `RESEARCH_GATE: DRIFT`; diagnostic says `path=claim denied (not opened)`.
- Reverted only the raw-full-path arm in a sandbox copy of the target helper (keeping the prior `ptr_file_part()` check): same command against `mutant/tools/research-gate.sh` → **gate exit 0**, claim `observed=supported`, `VERDICT_BEARING_CLAIMS=1/1`, `RESEARCH_GATE: CLEAN`. **Mutation evidence: yes—the deny control fails when the targeted fix is reverted.** The regression mutant admits/reads the colon-bearing credentials path.
- Positive filesystem control: `ordinary:synthetic.md` with `source=ordinary:synthetic.md` → **gate exit 0**, CLEAN; ordinary colon paths are not over-denied.
- Citation wrapper control: target `verify` on the sandbox record whose source/claim pointers are `lib/primary.md:1` and `:2` → **gate exit 0**, CLEAN. Anchor suffixes still resolve through `ptr_file_part()`.

**Exploit path / impact:** the attempted raw-path bypass is stopped before the source is opened in the target. If the raw-path check is removed, the exact fixture becomes a supported claim instead of a refusal, so a colon-bearing path under a denylisted directory could be admitted as evidence. **Smallest remediation:** none for the landed revision; retain the raw-full-path check and the existing citation wrapper.

## Requested cross-checks

- **S040–S042 source gate:** all three lesson quotes match their cited round-26 reports exactly after collapsing Markdown line-wrap whitespace. S040 `FNoTrade.md:126–128` describes a harness defect, not incorrect gate behavior; the archived base has the rejecting `$out != *'RESEARCH_GATE: '*` test at line 6016 and `die_usage` prints the usage line `Verdict: RESEARCH_GATE: CLEAN|DRIFT` at 385. S041 `FDateHugeCadence.md:42–44` precisely scopes the recursive `digits=${digits##+(0)}` before the seven-digit bound; the archived base confirms extglob at 256 and strip/bound at 2348–2350. S042 `FRegistryHeaderless.md:45` precisely describes the stale-column path; the archived base’s non-pipe branch at 2412–2415 resets only `header_candidate`, while the column resets are later at 2454/2466. These are correctly scoped historical diagnoses, not claims that the repaired target still has those defects.
- **IntegCaseIdentity:** static comparison of the target and archived base `64eec5d41c7cf7f17f5ce1e968e28b3769952596` found the first 187 selftest case-call helper/name pairs identical in source order: first `pass-control`, #187 `metadata-registry-refused-nul`; 0 mismatches. SHA-256 of the normalized 187-pair sequence is `f387754c30c984551eebe9071f073ae3823e227700fec470078313a2131e671f` for both. No selftest was run.
- **IntegTokenCost:** synthetic source size exactly 1,048,576 bytes; same claim/root fixture, one `verify-claims` command per archive. Base `64eec5d4…`: gate exit 0, CLEAN, real `0.060 s`; target: gate exit 0, CLEAN, real `0.059 s`. No new time regression observed in this single paired sample (timings are noisy, not a benchmark).
- **Simplifier:** only new function definitions versus the base are `is_denylist_path_value` and `is_denylist_fs_path`; both have call sites. The former centralizes the existing patterns, the latter is the required raw-plus-legacy union, and the citation wrapper remains distinct. No dead or duplicate helper/pattern list found; no edit made.

**Limits:** static source inspection plus synthetic sandbox-only single gate commands and one 1 MiB timing pair. No full selftest or regression script, host-secret access, network, `/proc`/live-process inspection, namespace/mount, debugger, or production-lane edit.