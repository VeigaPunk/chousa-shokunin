# Round 27 falsify — IntegReaderOrder (+ CaseIdentity, SourceGate, TokenCost, Simplifier)

Target: landed `dd72641e574679c4f7882dd43de072b4c8892d6f`, gate `tools/research-gate.sh` sha256 `ca39d14d…92f84` (verified).
Comparison base: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate sha256 `c2c813f1…3abc6` (verified).
Sandbox (only writes outside the lane): `/tmp/chousa-r27-falsify-IntegReaderOrder/` (`base/`, `target/`, `mutA/`, `mutB/`, `mutC/`, `ro/`, `timing/`, JSON/logs).
Not run: full `--selftest`, `round27-regressions.py`, date/registry differentials (L1-owned). No network, no external target, no host secret file, no strace/debugger/mount, no lane git write. Gate-internal `readlink -f /proc/$$/fd/N` runs as part of normal gate execution; I inspected no other /proc entry. The fd-canonical divergence was injected by a sandbox `readlink` shim that answers `/proc/*/fd/*` queries from an env var and never reads /proc.

## Verdicts

| item | verdict | basis |
|---|---|---|
| ReaderOrder: entry/registry raw, canonical, fd-canonical deny precede byte reads; NUL/size/stat/multilink unchanged | **HOLDS** (not falsified) | static source order; 13-case base/target differential; 3 single-site reversion mutants; diff shows only predicate swaps |
| CaseIdentity: original 1–187 retain order, text, exits, diagnostics | **HOLDS** | 185/185 base top-level invocation lines identical in order; counts reconcile to 187 (base) and 210 (target); 23 new cases appended after the last original |
| SourceGate: S040–S042 located quotes, scope, rows | **HOLDS** for quotes, scope, rows, base binding; **GAP**: no final-bytes census receipt | exact quotes at cited r26 lines; `corpus/SOURCES.md` +11/−0 |
| TokenCost: no new time regression | S-id-dense path **HOLDS** (large gain). **FALSIFIED (narrow)** for dense non-S-id sources in `--registry` mode, and a ≈+1 ms per-entry cost (noisy) | measured below |
| Simplifier: dead/duplicate code introduced | **One introduced dead helper** plus a duplicated predicate | `metadata_asof_usage_accepts` has no caller in the gate |

## 1. ReaderOrder

### 1.1 Static source order (target, line numbers in `tools/research-gate.sh`)

| chokepoint | order in target |
|---|---|
| entry `verify_metadata` (2602–2651) | raw/canon deny `2609` → `exec {meta_fd}<"$canon"` `2611` → fd-canon deny `2616` → `[[ -f $fdpath ]]` + `stat -Lc '%s %h'` `2618` → multilink `2623` → size `2625` → bounded read `read -r -d '' -n cap+1 … <&"$meta_fd"` `2631` → `exec {meta_fd}<&-` `2641` |
| registry `metadata_registry_load` (2380–2497) | raw/canon deny `2394` → `exec {registry_fd}<"$canon"` `2396` → fd-canon deny `2401` → stat `2403` → multilink `2408` → size `2410` → bounded read `2413` → close `2424` |
| claim source `claim_source_path` (1135–1239) | raw deny `1139` → canon deny `1166` (new) → in_root `1181–1191` → `-f/-r` `1192` → `stat -c '%s %h %d'` `1203` (nlink `1204`, size `1209`, device `1222`) → `CLAIM_SRC_PATH` `1237`; caller reads `cat -- "$path"` at `1403` (claims) and `1719` (chain) |

Diff evidence (`diff -u base target`, 19 hunks, 303+/25−): the only changes in these paths are the `is_denylist_path` → `is_denylist_fs_path` swaps (entry 2609/2616, registry 2394/2401, claim 1139 and the new 1166 check). The `-n` bounds, `stat` probes, nlink/size/NUL branches and read calls are byte-identical to base. Predicate monotonicity: `is_denylist_fs_path(x)` = `value(x) || value(ptr_file_part(x))`, a superset of base's `value(ptr_file_part(x))`. Citation paths keep `is_denylist_path` (631, 660, 1613). No byte read precedes a deny check in the entry or registry path; the only pre-check operations are `-e/-r/-f` tests, `readlink -f`, and directory globbing.

### 1.2 Observable differential (`python3 ro.py`, exit 0; sandbox fixtures only)

Outcome per case. Base = landed predecessor; mutants per 1.3. "entry:x" = `META_ENTRY_REFUSED reason=x`; "registry:x" = `metadata registry refused: x`.

| case | base | target | mutA | mutB | mutC |
|---|---|---|---|---|---|
| ok entry (control) | parsed | parsed | parsed | parsed | parsed |
| NUL in entry | entry:nul | entry:nul | entry:nul | entry:nul | entry:nul |
| 8 MiB+1 with NUL at byte ~100 | entry:size | entry:size | entry:size | entry:size | entry:size |
| hardlinked alias with NUL | entry:multilink | entry:multilink | … | … | … |
| `credentials/` plain denylist with NUL | entry:denylist | entry:denylist | entry:denylist | entry:denylist | entry:denylist |
| **colon path `entry:synthetic/credentials/…` with NUL** | **entry:nul (read)** | **entry:denylist** | entry:denylist | entry:denylist | entry:denylist |
| **colon registry `registry:synthetic/credentials/…`** | **registry:nul (read)** | **registry:denylist** | registry:denylist | registry:denylist | registry:denylist |
| plain registry with NUL (control) | registry:nul | registry:nul | … | … | … |
| **claim symlink → colon-credentials target** | **supported (read)** | **CLAIM_SOURCE_SESSION, rc 1** | CLAIM_SOURCE_SESSION | CLAIM_SOURCE_SESSION | **supported** |
| plain claim (control) | supported | supported | … | … | … |
| **fd-canon `fd:synthetic/credentials/x.md` (shim)** | **entry:nul (read)** | **entry:denylist** | **entry:nul** | entry:denylist | entry:denylist |
| fd-canon benign (shim, control) | entry:nul | entry:nul | entry:nul | entry:nul | entry:nul |
| fd-canon `credentials/x.md` (shim) | entry:denylist | entry:denylist | **entry:nul** | entry:denylist | entry:denylist |

Reading: non-denylisted outcomes are identical base/target (NUL, size, multilink logic unchanged, observable). Size and multilink refusals fire before the NUL read even when a NUL is present (`size`, `multilink` rather than `nul`), so stat probes precede byte reads. Base's bold `nul` outcomes show base reads the bytes of denylisted colon-named paths; target refuses first.

### 1.3 Mutation evidence (sandbox copies; `bash -n` exit 0 for each)

- mutA: fd-canonical deny removed in entry (2616) and registry (2401) → `fd-shim-colon` and `fd-shim-plain-denylist` now read (`nul`); the fd check is the only guard for fd-canonical divergence. Control fails as expected.
- mutB: raw/canon deny removed in entry (2609) → no observable change (the fd check backstops; the pre-open check only avoids `open(2)` of denylisted names).
- mutC: claim canonical deny removed (1166) → `claims-colon-symlink` returns `supported`; control fails. The new canonical claim check is necessary.
- C1 cross-check (single gate commands, rc only): `verify-metadata … --as-of 2026-02-30` → base and target both rc 2 with one `RESEARCH_GATE: ` substring in usage text; base's `*'RESEARCH_GATE: '*` predicate fails it; target's anchored count (0) accepts it.

### 1.4 Limits (ReaderOrder)

- Race closure is not claimed. Entry/registry fd checks bind the name at check time; the inode is fixed after `open`, but a rename between the fd-canon check and `read` is not excluded.
- Claim and chain readers are path-based after the canonical check (`cat -- "$path"` at 1403/1719). No fd binding there; base has the same design. The invariant does not require it.
- Pre-existing, not introduced: `file_size_bytes` falls back to `wc -c <"$1"` (730) which reads the whole file before the cap check (claim path only, line 1229); entry/registry have no in-root containment (operator-supplied paths, denylist-only guard); `[[ -z $fdcanon ]]` maps to `refuse=denylist` (2401/2616), a mislabel; sweep glob expansion (`sweep_glob_matches`, 1909–1927) has no denylist predicate (names only, no bytes read; static reading, not run).
- The shim is synthetic. A real canonical/fd divergence needs a race or bind mount, which the bounds exclude.

## 2. CaseIdentity (static; selftest not run)

- Counting method: top-level helper-invocation lines of `run_selftest`, parsed with one-line helper scoping (`write_rec`, `add_scope_row` ranges fixed; earlier intermediate counts 168/188/194/214 were parser defects and are superseded), plus inline `cases=$((cases + 1))` sites.
- Base: 185 top-level invocations + 5 inline sites (`5917`, `5945` unconditional; `5256`, `5276`, `5700` else-branches). Reconciliation: 185 + 2 = **187**, matching r26's measured `3/187` if all if-branches run.
- Target: 207 top-level invocations (22 appended; includes 2 env-prefixed `LC_ALL=… metadata_asof_usage_case` at 6319/6328) + inline (`5943`, `5971`, `6348` unconditional; `5282`, `5302`, `5726` and `6324` else-branches). Reconciliation: 207 + 3 = **210**, matching L1's measured PASS 210. Both reconciliations assume branch selection (a static model), not a runtime count.
- Identity: all 185 base invocation lines are text-identical and in the same order at the same positions in target (0 mismatches over the base prefix, including arguments, expected exits and diagnostics). Inline increments are preserved (contexts identical, +26 line shift). The 22 appended invocations plus 1 unconditional inline (plain-mode, 6348) follow base's last original case `metadata-registry-refused-nul` (base 6235 = target 6283), so new cases are 188–210 under this order.
- Diff proof: no `run_selftest` invocation line is deleted or changed. The only deleted lines inside the selftest are in the `metadata_asof_usage_case` body (predicate and FAIL printf). The predicate change from "no substring `RESEARCH_GATE: `" to "no line beginning `RESEARCH_GATE: `" is the authorized C1 change. Residual: the anchored count depends on every verdict `printf` starting at column 0. I confirmed all such sites do.

## 3. SourceGate (S040–S042 in `corpus/lessons/round-27.md`)

| row | located quote (lesson) | re-opened r26 text | words | scope check |
|---|---|---|---|---|
| S040 | `FNoTrade.md:126–128` "the predicate is unsatisfiable for any usage exit, and the failure is deterministic rather than flaky." | exact at lines 127–128 (inside the cited range); 126 is the `usage` sentence | 16 | matches reported usage-harness cause; cited `research-gate.sh:6016` is the base predicate line |
| S041 | `FDateHugeCadence.md:42–44` "Bash's extglob `+(0)` longest-prefix match recurses in proportion to the run length." | exact across the 42–43 wrap | 12 | matches F1 (`${digits##+(0)}`; 64,000 zeros 8.77 s; ≥68,000 SIGSEGV) |
| S042 | `FRegistryHeaderless.md:45` "a non-pipe line sets `header_candidate=0; continue` but does not reset `id_col`/`status_col`/`usedby_col`." | exact at line 45 | 11 | base 2412–2415 verified as the non-pipe branch |

Other cited ranges, also re-opened: FDateAsOfUsage 70–86 (non-ASCII `[0-9]` under locale, arithmetic abort) matches S041; FRegistryIdBoundary 28–46 (shortest-prefix rescan of `S001S002`) matches S042; FRegistryRegistryDeny 23–30 (`ptr_file_part` applied to raw/canon/fd paths) matches S042.

Rows and binding: `corpus/SOURCES.md` S040–S042 present (own-work, tier A, mined). `git diff --numstat` base→landed: `corpus/SOURCES.md 11 insertions / 0 deletions`, so no existing row changed. `corpus/evidence/round27-census-before.json`: `measured_revision` 64eec5d4; `source_sha256` `8308e629…` equals base `corpus/SOURCES.md` sha256 (verified); 39 rows at base; states it was materialized after the rows were drafted and infers no timestamp.

GAP: no final-bytes census receipt. Target `corpus/SOURCES.md` is `3e8eac97…` (42 rows, verified sha256) and is not recorded in any evidence file; the claims asked for an initial and a final census. Retroactive-admission rejection and "green ≠ source truth" language are present in the lesson.

## 4. TokenCost (time; sandbox, bounded 120 s per run)

Harness: `timing.py`, `timing2.py` (Python 3.14.8; bash 5.3.20). Each run killed by process group at 120 s. Host load was high (background job cap of 100 reached by other agents), so ≥1 MiB numbers are single runs and should be read as order-of-magnitude.

S-id-dense source (10 S-ids cycling, every id in registry, used-by = entry):

| entry bytes | base | target | output |
|---|---|---|---|
| 65,578 (64 KiB) | 1.387 s (median of 3) | 0.272 s | identical |
| 262,188 (256 KiB) | 17.925 s (2 runs) | 1.179 s | identical |
| 1,048,618 (1 MiB) | >120 s (killed) | 6.997 s | — |
| 2,097,193 (2 MiB) | >120 s (killed) | 21.776 s | — |
| 4,194,348 (4 MiB) | >120 s (killed) | 84.690 s | — |

Dense non-S-id source (Q-ids, no S-ids, registry mode; `timing2.py`):

| entry | base | target | delta |
|---|---|---|---|
| 256 KiB | 0.181 s | 0.367 s | +0.186 s (2.0×) |
| 1 MiB | 2.174 s | 2.972 s | +0.798 s (+37%) |
| 4 MiB | 63.796 s | 65.851 s | +2.055 s (+3%) |

Outputs identical (sha `aed0ea3b…`). The per-token cost (≈3–5 µs per alnum token) comes from the new loop over every token. Base skipped that loop because its regex pass found no S-id; the loop only runs with `--registry` (source capture at line 2654). Base's 64 s at 4 MiB is pre-existing entry parsing (carried as "entry-reader time" in r26), not introduced.

Small typical entry (1 S-id, 30 runs each): base median 20.0 ms (mean 19.6), target median 21.0 ms (mean 21.1). About +1 ms, within noise; mechanism inferred as one extra `grep` fork per registry-mode entry.

Claims path, 4 MiB source (`verify-claims`): base 0.168 s, target 0.182 s; no measurable change.

Parity (tricky tokens `S777 xS777 S777x _S777 S777_ S777,S777 S777;S777 S0001 S01 s777 S777S777 S777é S001 S001x`, registry has S001 only): both rc 1, both 7 `META_SOURCE_ROW_MISSING` (six standalone `S777`, one `S0001`), identical stdout sha `354383df…`. Occurrence identity and standalone rule are preserved.

Streaming check: no recursive prefix match and no negated-class substitution in the new code; `grep -oE '[[:alnum:]_]+'` plus `^S[0-9]{3,}$`. First-row policy and used-by logic unchanged.

## 5. Simplifier (no edits made)

1. **Introduced dead helper.** `metadata_asof_usage_accepts` (`tools/research-gate.sh:6036–6040`) has zero callers in the gate. `metadata_asof_usage_case` (6041) inlines the same predicate. The independent control `corpus/evidence/round27-regressions.py:74–77` requires the name (`parser.error` if absent), but its harness (88–89) executes only `metadata_asof_usage_case`. So the helper is presence-checked, not executed, and the predicate exists twice. CriticHarness already flagged this (`build/CriticHarness.md:188`).
2. Duplicate: the claim canonical refusal block (1166–1170) repeats the raw refusal block (1139–1143).
3. Duplicate: registry reset `id_col=-1; status_col=-1; usedby_col=-1; header_width=0` appears at 2434–2435, 2478–2479, 2492–2493.
4. Redundant: `local LC_ALL=C` in `metadata_registry_check_source` (2502) alongside the explicit `LC_ALL=C grep` (2529).
5. Pre-existing copy-paste: entry (2607–2642) and registry (2393–2425) open/deny/fd/stat/read blocks. The landing swapped the predicate in both, so they are in sync; a shared helper would prevent future drift.
6. Not dead: `is_denylist_path` still serves citation pointers (631, 660, 1613). `metadata_iso_date` and `metadata_add_days` need their `local LC_ALL=C` for the CLI `--as-of` path. The `metadata_add_days` ASCII check is required for the empty-string case.

## 6. Commands and exit codes (exact)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C target` → 0; `archive 64eec5d4… | tar -x -C base` → 0.
- `sha256sum target/tools/research-gate.sh base/tools/research-gate.sh` → `ca39d14d…`, `c2c813f1…` (0).
- `git --no-pager diff --stat 64eec5d4 dd72641e` → 84 files +12662/−25; `diff --numstat … -- corpus tools` → `tools/research-gate.sh 303/25`, `corpus/SOURCES.md 11/0` (0).
- `git --no-pager show 64eec5d4:corpus/SOURCES.md | sha256sum` → `8308e629…`; `show dd72641e:corpus/SOURCES.md | sha256sum` → `3e8eac97…` (0). Read-only git only.
- `python3 timing.py` → 0 (518.8 s); `python3 timing2.py` → 0 (135.5 s).
- `python3 ro.py` → 0; `python3 ro.py mutA=… mutB=… mutC=…` → 0. Mutants: `bash -n` → 0 each.
- Static analysis (python, read-only over sandbox copies) and `_grep`/`_read` of lane evidence; no exit-code-bearing gate runs beyond the above and the C1 single-command pair (both rc 2).
- No installs or updates. Existing tools only: python3 3.14.8, bash 5.3.20, GNU readlink/stat/timeout, git. (Operator tooling rule: nothing needed.)

## 7. Advice to the author lane (not an outside admission)

- Make `metadata_asof_usage_case` call `metadata_asof_usage_accepts`, so there is one live predicate. The name check in `round27-regressions.py` is still satisfied. This matches CriticHarness's suggestion.
- The non-S-id registry-mode cost is a real, small, bounded regression. Option: a pre-filter (`[[ $source_value =~ S[0-9]{3,} ]]`) before the grep pipeline skips the loop when no S-id-shaped substring exists. This is semantically neutral because only `S[0-9]{3,}` standalone tokens count. [INFERENCE — not executed.]
- Record a final-bytes census receipt for the landed `corpus/SOURCES.md` (sha `3e8eac97…`, 42 rows) to close the SourceGate gap.
- Keep the 13-case base/target/mutant differential as a standing control for colon-named denylist paths. Those paths are the only cases where base and target diverge, which is the intended C3 effect.

## Corrections and axis mapping (appended after the initial write)

- Section 1.2, row "8 MiB+1 with NUL": the NUL sits right after the 67-byte header, not at byte ~100 as written above. The size-before-read reasoning is unchanged.
- Section 1.2 header: "Base" means `64eec5d4` (the comparison base), not the landed predecessor.
- Section 2, residual: the anchored verdict count relies on every verdict `printf` whose format string begins with `RESEARCH_GATE: ` (output column 0). The wording "starting at column 0" referred to output, not source indentation. I confirmed all such format strings begin with the literal.
- Section 4, environment: the 100-job cap was reached in the shared shell (I did not measure host load). I started the timing run in the foreground for that reason, and host load was uncontrolled. Treat the ≥1 MiB numbers as order-of-magnitude.
- Section 2, "new cases are 188–210": runtime case ordinals, not counts of new invocations (23 new cases total = 210 − 187).
- Axis mapping: ReaderOrder → calibration (C3 path representation, plus no operability regression); CaseIdentity → operability (C1); TokenCost → operability (time); SourceGate → calibration (provenance); Simplifier → maintainability. Freshness (C2) is outside this item's scope and was not attacked here.
