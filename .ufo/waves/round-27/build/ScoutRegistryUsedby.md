# ScoutRegistryUsedby — C3 used-by semantics and path-normalization limits to preserve

Seat: `ChousaR27.ScoutRegistryUsedby` (scout, leaf). Read-only static analysis; no gate,
selftest, regression, or differential execution. Base master `64eec5d4`; the lane worktree
carried only in-flight C1 usage-helper edits (`research-gate.sh:6007+`) and the S040–S042
rows in `corpus/SOURCES.md` while this was read — the C3 registry region was unchanged.
Independent expectations are the already-persisted `corpus/evidence/round27-regressions.py`
(C3 block `:118–170`); the r26 falsifier reports are accepted ground truth.

## 1. Used-by: the exact shipped rule (observed, tools/research-gate.sh:2472–2506)

Precedence per discovered S-id (`:2478–2501`) is fixed and must not be reordered:

1. No registry row for the id → `META_SOURCE_ROW_MISSING` (warn).
2. Row exists but status is not exactly the byte string `mined` → `META_SOURCE_NOT_MINED` (warn);
   used-by is never consulted.
3. Otherwise the used-by cell is split on a literal comma (`IFS=',' read -r -a`), each token is
   trimmed with `[[:space:]]` at both ends, every leading `./` is stripped, and the token must
   equal the entry path by quoted string equality: `[[ -n $entry_path && $token == "$entry_path" ]] && matched=1` (`:2500`).
   No token matches → `META_SOURCE_USEDBY_MISSING` (warn).
4. No valid id at all → `META_SOURCE_NO_ROW_ID` (info) (`:2505–2506`).

Equality is literal (RHS quoted, so no glob), case-sensitive, and byte-exact. There is **no**
normalization of `..`, `//`, trailing `/`, backslashes, backticks, URL/percent escapes, or
basename matching. An empty used-by cell, an empty token (trailing comma), or an empty
`entry_path` never matches. Genuine duplicate tokens change nothing; the id is checked once
per source occurrence.

Entry path derivation (`metadata_registry_entry_path`, `:2509–2523`) must stay as is:
`fdcanon` (the `readlink -f` of `/proc/$$/fd/N`) is relativized against `registry_root`
(`pwd -P` of `--root`), with the root `/` special case stripping the leading slash. Therefore:

- Used-by names the **canonical repo-relative path of the entry that cites the id**, not the
  registry's location or the process CWD.
- A symlink spelling, an absolute path, a basename (`knowledge/x.md`), or `a/../x.md` does not
  match; the differential fixtures at `round26-registry-differential.sh:109–111` already pin
  trailing-space success, `./` success and basename failure.
- If the entry resolves outside `--root`, `entry_path` is empty and every id reports used-by
  missing; that guard must remain.

Locale caveat to close without changing ASCII results: `metadata_registry_check_source` has no
`local LC_ALL=C` (unlike the loader at `:2366`), so `[[:alnum:]]`, `[[:space:]]` trimming, and
`[0-9]` follow the inherited locale. Add `local LC_ALL=C` in that function so the ASCII trim and
ASCII id boundaries are unconditional; ASCII fixtures are byte-identical under either locale.
Note the gate strips **repeated** `./` (`while [[ $token == ./* ]]`), while the r26 Python oracle
(`round26-registry-oracle.py:110–117`) strips one; `././x` is a divergence input. Preserve the
gate rule ("existing ... exact used-by rules remain") and do not add `././` to oracle-differential
fixtures.

## 2. S-id occurrence identity (tools/research-gate.sh:2472–2506)

The defect is the literal-prefix rescan `source_scan=${source_scan#*"$source_match"}` with the
unanchored regex, which can re-enter a glued token when the last genuine id ends the value
(r26 FRegistryIdBoundary b1/b2/b5/b6). Replacement must preserve these observed identities:

- Genuine occurrences are counted per occurrence: `S002,S002` → exactly **2**
  `META_SOURCE_NOT_MINED`; `S001,S002` (S001 mined+used-by-correct, S002 queued) → 1
  (`round27-regressions.py:149–150`).
- `ref S002x and S002` and `ref S002S002 and S002` → exactly **1** each; `see S001S002 and S001`
  and `xS002 S002x _S002 S002_ S001` → **0** (`:144–148`). "No duplicate occurrences" means no
  rescan of consumed text, not collapsing genuinely repeated ids.
- Id grammar: `S` + at least three ASCII digits, case-sensitive; boundary bytes are anything
  outside `[A-Za-z0-9_]`, and `_` is word-internal (so `S001_x` is not an id). Non-ASCII bytes
  are boundaries (C-locale byte rule), matching the oracle lookarounds
  (`round26-registry-oracle.py:12`).
- Safe implementation shape (as the r26 mutation demonstrated): scan the **whole multi-line
  `source_value`** (continuation lines at `:2694` are part of it), treating bytes outside
  `[A-Za-z0-9_]` as separators, keep words matching `^S[0-9]{3,}$`, and emit findings in
  first-occurrence order. Set `local LC_ALL=C`; `[[:alnum:]]` alone is not ASCII-stable.

## 3. Filesystem paths vs citation pointers: split the denylist, keep the wrapper

`is_denylist_path` (`:595–606`) matches its globs against `ptr_file_part` (`:573–576`), which
truncates at the **first colon** (`${p%%:*}`) — a citation-anchor convention. Every filesystem
path containing an earlier colon therefore bypasses all deny patterns (r26 FRegistryRegistryDeny
B1–B6). Preserve the pattern set (`:597–605`, including path-start `.omp/`, `.config/`,
`.local/state/` forms) and split by caller representation:

| line | argument | representation | disposition |
|---|---|---|---|
| 636 | `$canon` in `ptr_resolves_meta` | canonical filesystem path | migrate to raw fs predicate |
| 2375 | `$path`, `$canon` in `metadata_registry_load` | CLI filesystem path + canonical | migrate |
| 2382 | `$fdcanon` registry fd | filesystem path | migrate; empty fdcanon stays `denylist` |
| 2584 | `$file`, `$canon` metadata entry | filesystem path | migrate |
| 2591 | `$fdcanon` entry fd | filesystem path | migrate; empty fdcanon stays `denylist` |
| 621 | `$p` in `ptr_resolves_meta` | citation pointer (may carry anchor) | keep wrapper |
| 650 | `check_pointer` pointer | citation pointer | keep wrapper |
| 1129 | `claim_source_path` `$src` | citation pointer | keep wrapper |
| 1598 | `chain_ref_file` ref | citation pointer | keep wrapper |

Suggested minimal design: keep `is_denylist_path` as `raw $(ptr_file_part "$1")` (byte-identical
for all pointer callers, including the `SESSION_READ` display at `:651` and the source display at
`:1131`), and add a sibling `is_denylist_fs_path` whose body applies the same case arms to
`$(norm_ptr "$1")` **whole**. Do not route the new predicate through `ptr_file_part`, and do not
change `norm_ptr` (it strips only surrounding backticks) or `is_session_url`/`is_url_ptr`.
Migration must not alter ordering: in `metadata_registry_load` the `-e/-r/-f` tests stay before
deny (`:2369–2374`, so a missing denylisted path still reports `not found`); deny stays before
`exec {fd}<`; fdcanon deny stays before stat and the bounded read. In the entry loop the same
order holds (`:2566–2591`). Regression expectations (`round27-regressions.py:155–170`):
`.../synthetic:fixture/.config/registry.md` and `.../synthetic:fixture.env` exit 2 with
`metadata registry refused: denylist` and zero `^RESEARCH_GATE: ` lines; `.../synthetic:ordinary.md`
exits 0 with one verdict line. A colon alone is not deny evidence.

## 4. Header binding that used-by lookup depends on (tools/research-gate.sh:2361–2470)

Used-by values are read through `usedby_col`, so column binding must be repaired without
changing value semantics:

- On every non-pipe line before a header is found, reset `id_col`, `status_col`, `usedby_col`
  **and** `header_candidate` (`:2412–2416` currently resets only the candidate). This is the
  FRegistryHeaderless root cause and the `header-break-blank`/`header-break-prose` controls
  (`round27-regressions.py:128–129`): the later `| a | b | c |` table must not become a
  candidate and the run must exit 2. A header interrupted by any line, including prose, must be
  supplied fresh; `reorder-clean` (`:130`) requires scanning to continue after that break.
- The delimiter row must have the **same cell count** as the named header and every cell must
  match `^:?-{3,}:?$`; `delimiter-too-short`/`delimiter-too-long` must exit 2 with
  `metadata registry has no table` (`:132–133`). Do not add data-row width enforcement: shorter
  rows yield empty cells (`${cells[$col]-}`) and extra cells are ignored today.
- Preserve: first qualifying table wins; names are exact lowercase after ASCII trim (first
  occurrence per name wins); row id must match `^S[0-9]{3,}$`; the **first row per id wins**
  (duplicate rows ignored, used-by included); status comparison is exact `mined`; absence of any
  qualifying table still `die_usage` exit 2 with the current diagnostic.

## 5. Round27 population note (calibration risk, not a code change)

The new `S040–S042` rows declare `used-by` = `corpus/lessons/round-27.md`. Used-by is only
enforced for an id that appears in some metadata entry's `source:` value. `corpus/lessons/round-27.md`
has no `source:`/`verified-at:`/`recheck:` lines and no `corpus/knowledge/*` entry currently cites
S040–S042 (static grep), so no check fires today. If a knowledge entry is later created citing
them, each cited row's used-by must name **that knowledge entry's** root-relative canonical path,
not the lesson file.

## 6. Suggested follow-up fixtures (synthetic, temporary; no host paths)

- Used-by: trailing spaces; `./` prefix success; `././` (gate-only, not oracle); basename, `..`,
  absolute, trailing-slash and backticked tokens as negatives; empty cell; trailing comma;
  queued status suppressing used-by; duplicate id rows first-wins with mismatching used-by;
  symlinked entry where used-by names the symlink instead of the canonical path.
- Occurrence: single continuation-line id; `S01` and `s001` negatives; `S0001` positive;
  `S003,S003` row-missing count 2 (per-occurrence consistency).
- Deny: colon-in-ancestor directory with a valid table (proves refusal happened before parse);
  colon before `.env`; ordinary-colon positive; if entry readers are migrated, the analogous
  `a:b/.config/e.md` entry case must yield `META_ENTRY_REFUSED ... reason=denylist unparsed`.
- Header: named header separated from a valid reordered table by prose (already present);
  separator width mismatch with extra/missing outer pipes; header-only table still
  `META_SOURCE_ROW_MISSING`.

## 7. Unrun checks and remaining unknowns

- Not run: `--selftest`, `round27-regressions.py`, `round26-registry-differential.sh`, the r26
  date differential, builds, linters, formatters, strace, and any host-file inspection.
- Line numbers were read while the C1 diff was uncommitted; the C3 block itself was unchanged
  (function starts 2361/2472/2509, denylist calls 2375/2382/2584/2591, pointer calls
  621/650/1129/1598).
- [INFERENCE] The raw-fs-predicate split is sufficient for the three colon controls because the
  full absolute path still matches the unchanged `*/.config/*` and `*.env` arms; no new pattern
  is required.
- [INFERENCE] Per-occurrence emission for genuinely repeated ids follows the persisted controls;
  if L1 instead adopts set semantics, `two-real-occurrences` would need an explicit decision,
  which the current regression file does not permit.
- No tools were installed or updated; no network, live process, `/proc` (other than none), or
  debugger probes were used.
