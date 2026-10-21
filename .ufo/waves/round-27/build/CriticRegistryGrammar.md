# CriticRegistryGrammar — C3 attack beyond the named-header fix (round 27 attempt 1)

Seat `ChousaR27.CriticRegistryGrammar` (critic, leaf). This is author-lane advice only, not an admission. The work was read-only static analysis: no gate, selftest, differential or oracle run, and no installs.

## Identity

- Reviewed tree: `HEAD` = `64eec5d41c7cf7f17f5ce1e968e28b3769952596`.
- `sha256 tools/research-gate.sh` = `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This is byte-identical to the r26 measured target, so the r26 falsify line numbers still apply.
- `corpus/SOURCES.md` has an uncommitted working-tree change (row S042, L1's). I did not read the diff.
- No executor patch or `corpus/evidence/round27-regressions.py` existed when I reviewed. This report attacks the C3 plan in `round27-claims.md:15` against base code, not a candidate patch.

## Axes

Calibration is primary. Operability is secondary, through exit-2 versus exit-0 and finding counts. Freshness is not affected.

## Counterexamples the C3 plan does not fix

The plan's four repairs do not touch any of the classes below:

- fresh named headers after a break;
- header and delimiter widths must match;
- standalone ASCII S-ids;
- full-path denylist.

Each must either be reported as an explicit residual limit or be given an explicit contract decision. None may be claimed fixed.

| # | Shape (synthetic) | Base gate | Oracle `round26-registry-oracle.py` | After the C3 plan | Impacted |
|---|---|---|---|---|---|
| G1 fence | `` ``` ``, HDR, SEP, `\| S001 \| queued \| e.md \|`, `` ``` ``, then the real HDR, SEP and S001 `mined` row | first table wins, so `META_SOURCE_NOT_MINED` and rc 1 | the same false positive | **unchanged**: inside the fence the header is fresh and the widths match | calibration (false positive) |
| G2 indent | the same table indented 4 spaces | accepted, because the trim at `research-gate.sh:2418` strips any `[[:space:]]` | accepted (`str.strip()`) | **unchanged** | calibration; second authority (see below) |
| G3 duplicate column | `\| id \| status \| used-by \| status \|` + 4-cell SEP + `\| S001 \| queued \| e.md \| mined \|` | the `<0` guard at `:2457-2460` makes the first column win, so NOT_MINED | `header.index`, also first wins | **unchanged**, and a matching width now *blesses* the ambiguous header | calibration (silent binding choice) |
| G4 body-row header | `\| a \| b \| c \|`, SEP, HDR, SEP, ROW | accepted: line-pair scan, and rows 3–4 become the header | accepted | **unchanged**: no break occurs, and the header is fresh and width-matched | calibration; the oracle shares the flaw, so the differential cannot see it |
| G5 escaped pipe | `\| x \\\| id \| status \| used-by \|` + **4**-cell SEP | accepted, with id at cell 1 (the split at `:2422` ignores `\|`) | accepted | **still accepted** (4 = 4). In GFM this header has 3 cells, so it is not a table | calibration; contract-invalid input (`CORPUS.md:85` "No `\|` inside any cell") |
| G6 body separator | HDR, SEP, SEP, `\| S001 \| queued \| e.md \|` | the 2nd SEP is read as a body row (id `---` is ignored), then NOT_MINED | **breaks** at `oracle:51-52`, so ROW_MISSING | **gate and oracle disagree** on the code set | oracle as a duplicate authority; the regression script must not inherit this rule unexamined |
| G7 oracle whitespace | `\| id\x1f \| status \| used-by \|` (U+001F unit separator) | rc 2, because C `[:space:]` excludes `\x1f` | accepted, because `str.strip()` strips `\x1c`–`\x1f`, `\x85` and `\xa0` | disagreement persists (generalizes r26 H12 NBSP) | oracle laxity; a Python `strip()`-based r27 script repeats it |
| G8 fenced source id | entry `source: S001`, then without a blank line `` ```text ``, `S999`, `` ``` `` | S999 is counted; `:2634-2638` appends fence lines to `source_value`, so ROW_MISSING | the same (`oracle:76-78`) | **unchanged**: tokenizing the S-id does not exclude fence content | calibration (an id quoted in code becomes a citation) |
| G9 duplicate key | `source: S001` … `source: S999` before `##` | last key wins (`:2665`), so S001 is never checked | last key wins (`oracle:102-103`) | **unchanged** | calibration (an earlier citation is hidden) |

## Defects a naive C3 patch would introduce

1. **The new width state leaks like the old column state.**
   - Current state: the only missing reset is the non-pipe branch at `:2412-2415`, where `header_candidate=0` runs but `id_col`, `status_col` and `usedby_col` are kept.
   - The widths repair adds a header cell count. That count must be assigned on the same line that sets `header_candidate=1` (`:2463-2464`). It must be cleared on all three reset paths: `:2414`, `:2454` and `:2466`.
   - Strongest counterexample: HDR (3 cells), prose, then `\| a \| b \| c \| d \|` + 4-cell SEP. A leftover width of 3 combined with column reset must give rc 2.
   - Smallest safe correction: one helper, `registry_header_reset`, that clears all four variables, called at every reset site.

2. **"No duplicate occurrences" can break well-formed counts.**
   - Static grep (awk over the pre-heading `source:` block, not a gate run) finds standalone ids repeated within one `source:` value in live entries:
     - `citation-chain-fidelity-r24.md`: S003, S005
     - `claim-support-states-r24.md`: S006, S007
     - `contextual-source-admission-r24.md`: S002, S003, S004
     - `json-delimiter-r24.md`: S013
     - `metadata-screen-r25.md`: S029, S033
   - The base gate emits one finding per scan hit.
   - There are two readings of "duplicate" in the claim:
     - removing rescan duplicates only (r26 b3/b11/b12, where 1 standalone occurrence gave ×2 or ×3);
     - collapsing distinct standalone occurrences into one per id.
   - The second reading changes `findings=` counts for any repeated id that is flagged. It also diverges from r26 ExecC3Oracle's stated "retains token multiplicity" (`ExecC3Registry/ExecC3Oracle` reports). Note that the oracle at HEAD actually uses `set()` (`oracle:122`).
   - Smallest safe correction: fix the claim and the r27 expectations to **one finding per standalone occurrence and zero for non-standalone text**. Add a control `S002 and S002` that expects ×2, next to `S002x and S002`, which expects ×1.
   - [INFERENCE] The five frozen r24+ entries stay clean either way, because they had no findings in r26 (FRH-1b).

3. **The tokenizer's boundary set must stay ASCII.**
   - Replacing `[^[:alnum:]_]` with a space under `LC_ALL=C` turns UTF-8 bytes into boundaries. So `éS001` and `S001٣` yield S001. This matches the oracle's ASCII lookarounds (`oracle:12`) and the claim ("standalone ASCII").
   - The risk is the opposite: a patch that drops `local LC_ALL=C` from `metadata_registry_check_source`'s caller scope. It is inherited from `verify_metadata:2539`, so a direct caller or selftest path without it changes the class.
   - Add a control with a non-ASCII-adjacent id.

4. **Denylist: two pattern authorities.**
   - The claim requires complete filesystem paths while keeping the citation-pointer semantics, which strip `:line` via `ptr_file_part` (`:573-576`).
   - Filesystem-path callers are `:2375`, `:2382` (registry), `:2584` and `:2591` (entry reader; r26 FRRD-2 inherited), and `:636`. At `:636`, `canon` is a `readlink -f` result, so it is a filesystem path too, while the `$p` check at `:621` is a pointer.
   - Counterexample if `:636` and the entry reader are left on the pointer form: an entry at `w/a:b/.config/e.md`, or a pointer whose resolved target is `…/a:b/.config/x`, still passes.
   - Smallest safe correction: move the glob body of `:597-605` into `denylist_match STRING`. Then `is_denylist_path` becomes `denylist_match "$(ptr_file_part "$1")"`, and a new `is_denylist_fs_path` becomes `denylist_match "$1"`. Use the second at all five filesystem sites.
   - Do **not** copy the patterns, because a duplicated list drifts.
   - Do not apply `norm_ptr` backtick stripping to filesystem paths. It is harmless today but is pointer grammar.

## Duplicate authority on registry grammar (report as an inherited limit)

`SOURCES-CONTRACT-v1` (`../CORPUS.md:80-85`) and `../scripts/sources-census.sh:3,24-25,40-42` define the registry this way:

- one table under `## Registry`, with NF = 13;
- 0–3 leading spaces, while 4 or more is code and is ignored;
- a duplicate id is error E03;
- used-by is split on `[,;]`.

The gate's `--registry` reader differs on each point:

- it takes the first table anywhere with the three names;
- it accepts any indentation (G2);
- a duplicate id is a silent first-wins (`:2434`);
- it splits used-by on `,` only (`:2489`).

The live `SOURCES.md` has no indented, fenced, duplicate-column or `;` used-by row (static awk and grep, so [INFERENCE] for future rows). The claim keeps "exact used-by rules", so the `,`-only split must stay. The r27 report must state that the gate's C3 screen is not the contract's registry grammar, and that agreement with the Python oracle covers only shapes where both use the same line-pair scan (G1, G2, G4 and G8 are shared flaws, while G6 and G7 are disagreements).

## Tradeoffs versus fixable defects

- **Fixable inside C3 scope, with no behavior change for well-formed input:** defect 1 (width-state reset), defect 4 (one denylist pattern authority with filesystem callers), and making the claim say per-occurrence counting (defect 2).
- **Needs a contract decision, so it must be reported rather than silently changed:**
  - G1, G2 and G4: fence-aware, 0–3-space, GFM-body-aware registry scanning. Any of these would alter "existing well-formed registry behavior" for fenced or indented tables.
  - G3: reject duplicate required columns with exit 2, or document first-wins.
  - G5: contract-invalid input.
  - G8 and G9: fence content in the entry `source:`, and duplicate keys.
- **Must be rejected by the judge if claimed:** any "whole registry grammar" or "fence/indent safe" wording, or any differential agreement offered as proof for G1, G2, G4 or G8.

## Fixtures for persisted independent controls (synthetic, temporary dirs only)

- Gate expectations follow the plan. Oracle expectations must be derived independently, not copied from the gate.
- Width state: HDR, prose, 4-col `a b c d` + 4-cell SEP → rc 2. HDR, blank, HDR, SEP, ROW → rc 0 (a fresh header after a break must still work).
- Occurrence: `S002 and S002` → NOT_MINED ×2. `S002x and S002` → ×1. `see S001S002 and S001` → clean (r26 b1).
- Denylist full path: entry and registry under `a:b/.config/`, plus a symlink to such a path → refused before read. Compare the expected `ptr_file_part` output on `x.md:12` to confirm pointer anchors are unchanged.
- Limits (assert current behavior *and* label it as a limit, do not assert "fixed"): G1, G2, G3 and G4.

## Unrun checks (for L1, once, after integration)

`python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`; `bash tools/research-gate.sh --selftest`; `corpus/evidence/round26-registry-differential.sh` on an isolated copy. None of the counterexamples above were executed by this seat. Their outcomes are derived from code reading at the cited lines. They are [INFERENCE] except for the shapes r26 already observed: S01–S05, G01–G12 and B1–B6.
