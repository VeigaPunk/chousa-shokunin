# ScoutRegistryState — C3 header state, S-id token identity, full-path denylist

Seat: `ChousaR27.ScoutRegistryState` (scout, leaf). Assigned item: map every
`header_candidate` and column reset path plus the concrete stale-state minimal
fixtures. Static read-only; no test, selftest, differential, or runtime
execution was performed. Author-lane advice only.

## Identity and method

- Base: `64eec5d41c7cf7f17f5ce1e968e28b3769952596` (`git log -1` observed).
- The lane working tree is **not clean**: `git status` shows ` M tools/research-gate.sh`
  (+26/−1, all inside the C1 usage-helper block at ≥6007), ` M corpus/SOURCES.md`,
  ` M corpus/QUALITY.md`, plus untracked round-27 evidence. `git diff tools/research-gate.sh`
  was read: no hunk touches `metadata_registry_*`, `is_denylist_path`, or
  `ptr_resolves_meta`. Every line number below is live **and** base for the cited
  C3 regions; selftest insertion points shift by +25 lines from base.
- No LSP device is exposed in this seat's tool inventory (`xd://` has no lsp route;
  the mounted MCP surface is the REA reverse-engineering set). Locations below are
  from direct source reads, not semantic LSP results; no empty-cold-result claim is made.
- Sources read: `tools/research-gate.sh:567-606, 621-636, 1129-1157, 2361-2537,
  2571-2595, 6125-6250`; `corpus/evidence/round27-regressions.py:52-167`;
  `corpus/evidence/round26-registry-oracle.py:11-90`;
  `corpus/evidence/round26-registry-differential.sh:60-175`;
  `.ufo/waves/round-26/falsify/FRegistryHeaderless.md:30-118`,
  `FRegistryIdBoundary.md:23-113`, `FRegistryRegistryDeny.md:19-123`;
  `corpus/evidence/round27-mechanisms.py:20-40`,
  `corpus/evidence/round27-mechanisms-before.json`.
- Reported r26 failures are treated as ground truth and were not rerun.

## A. State machine — every candidate/column reset path (observed)

State: `header_candidate` (2414/2449/2450/2453/2464), `header_found` (2449/2469),
`id_col`/`status_col`/`usedby_col` (2364 and the resets below), per-line `cells`
(reassigned at 2422-2428), and the new `header_width` this report proposes.

| # | Location | Condition | Effect observed at base |
|---|---|---|---|
| 1 | `2363-2364` | function entry | `header_candidate=0`, `header_found=0`, cols `-1` |
| 2 | `2410` `declare -gA` | before parse | registry maps cleared |
| 3 | `2412-2416` | line has fewer than two `\|` | `((header_found)) && break`; else `header_candidate=0; continue` — **cols are NOT reset** (stale-state source) |
| 4 | `2443-2451` | candidate + every cell matches `^:?-{3,}:?$` | `header_found=1; header_candidate=0; continue` — cols deliberately retained for data rows; **no cell-count comparison** |
| 5 | `2453-2454` | candidate + non-separator table line | `header_candidate=0`; all three cols reset; falls through to the same-line name scan |
| 6 | `2456-2462` | table line after candidate handling | name scan only fills slots still `< 0`, so it **cannot overwrite stale indices**; first occurrence of each name wins |
| 7 | `2463-2467` | all three cols ≥ 0 | `header_candidate=1` **regardless of whether this line named anything**; else all three reset |
| 8 | `2469` | end of content | `((header_found)) \|\| die_usage "metadata registry has no table…"` (exit 2) |
| 9 | `2519-2537` (`metadata_registry_load` call at `2571`) | registry load precedes the entry loop | a registry refusal exits 2 before any entry is opened |

The only defect in this machine is path 3: it clears the candidate but leaves the
three indices bound to a line the parse has already left behind. Path 4 then
accepts a delimiter whose width was never compared; path 6 keeps stale indices
because of the `< 0` guards. Path 7's unconditional `header_candidate=1` is what
turns the stale indices into an accepted header.

## B. Concrete stale-state minimal fixtures (newly generated synthetic text)

`HDR` = `| id | status | used-by |`; `SEP3` = `|---|---|---|`;
`ROW` = `| S001 | mined | corpus/knowledge/entry.md |`. All traces are static
walks of lines 2409-2469 at base; no fixture was executed here.

| id | registry bytes (`\n`-joined) | base walk | base rc | target rc |
|---|---|---|---|---|
| F1 | `HDR`, blank, `\| a \| b \| c \|`, `SEP3`, `ROW` | HDR candidate 0/1/2 → blank clears candidate only → `a/b/c` passes the all-≥0 test → `SEP3` sets `header_found` → ROW parsed as S001/mined/entry | **0** | 2 |
| F2 | `HDR`, `prose`, `\| a \| b \| c \|`, `SEP3`, `ROW` | identical to F1; any line with <2 pipes triggers it | **0** | 2 |
| F3 | `HDR`, blank, `SEP3`, `SEP3`, `ROW` | blank → `SEP3` becomes candidate via stale cols → second `SEP3` sets `header_found` → ROW parsed | **0** | 2 |
| F4 | `HDR`, `prose`, `\| id \| note \| used-by \| status \|`, `\|---\|---\|---\|---\|`, `\| S001 \| mined \| corpus/knowledge/entry.md \| queued \|` | after prose, the scan cannot move `status_col`/`usedby_col` off 1/2; status is read from `mined` → false negative (real status `queued` invisible) | **0**, no finding | 1, exactly 1 `META_SOURCE_NOT_MINED` |
| F5 | `HDR`, `prose`, `\| id \| note \| status \| used-by \|`, `\|---\|---\|---\|---\|`, `\| S001 \| - \| mined \| corpus/knowledge/entry.md \|` | stale status_col=1 reads `-` → false positive; used-by is not reached because of the `elif` chain | **1**, `META_SOURCE_NOT_MINED` | 0, clean |
| F6 | `HDR`, `\|---\|`, `ROW` (also `\|---\|---\|---\|---\|`) | path 4 accepts a delimiter whose cell count differs from the 3-cell header; cols are still 0/1/2 so ROW parses cleanly | **0** | 2 |

F1-F3 isolate the stale-column leak (the accepted table has no named header);
F4/F5 isolate the un-resettable indices on a fresh named header; F6 isolates the
missing width check. They correspond one-to-one to
`round27-regressions.py` cases `header-break-blank`, `header-break-prose`
(blank and prose variants), `reorder-queued`, `reorder-clean`,
`delimiter-too-short`, `delimiter-too-long` at `:121-138`; the same shapes are the
r26 receipt's S01/S02, S04, S05 and G01/G02 (`FRegistryHeaderless.md:47-53,85-93`).
`valid-table`, `reorder-clean` (4/4 width) and `ordinary-colon-is-allowed` must
stay rc 0, and the r26 differential's 12-column generated table
(`round26-registry-differential.sh:126-139`) stays width-matched.

## C. Suggested header/width repair (minimal hunks)

```bash
# 2364
  local id_col=-1 status_col=-1 usedby_col=-1 is_separator header_width=-1

# 2412-2416 — break must invalidate candidate AND its column binding
    if [[ $line != *'|'*'|'* ]]; then
      ((header_found)) && break
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1; header_width=-1
      continue
    fi

# 2443-2451 — after computing is_separator, require the candidate's own width
      is_separator=1
      for cell in "${cells[@]}"; do
        [[ $cell =~ ^:?-{3,}:?$ ]] || { is_separator=0; break; }
      done
      (( ${#cells[@]} == header_width )) || is_separator=0

# 2453-2454
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1; header_width=-1

# 2463-2467
    if ((id_col >= 0 && status_col >= 0 && usedby_col >= 0)); then
      header_candidate=1
      header_width=${#cells[@]}
    else
      id_col=-1; status_col=-1; usedby_col=-1; header_width=-1
    fi
```

Effect: F1-F3 reach `2469` and exit 2; F4/F5 re-derive their own indices from a
fresh named header; F6 fails the width equality. No fence grammar, no new table
rule, and no change to the name→column mapping or `used-by` comparison is
introduced. Fenced-table and blockquote shapes stay inherited limitations
(`FRegistryHeaderless.md` R26-FRH-4), not fixed here.

## D. S-id occurrence scan — token identity (`metadata_registry_check_source:2472-2504`)

Observed root cause (matches `FRegistryIdBoundary.md:30-46`): the regex match
includes the boundary characters, and the loop advances with
`source_scan=${source_scan#*"$source_match"}` (`:2503`). The `#*` strip is a
**literal-prefix** strip, not a match-position advance. When the match ends at
`$`, `source_match` carries no trailing boundary, so the earliest literal
occurrence of e.g. ` S001` is found *inside a glued token* (`S001S003`), the
remainder starts mid-token, and `^` then treats the glued id as standalone.
That invents ids and re-emits one real token 2-3 times.

Target semantics are exactly the r27 persisted controls
(`round27-regressions.py:139-153`): glued tokens contribute nothing, real
repeated occurrences keep their multiplicity (`S002,S002` → 2 findings), and
`S001,S002` finds both. Note: **do not dedupe** — dedupe would make
`two-real-occurrences` fail its count of 2.

Suggested replacement (keeps the finding bodies and left-to-right order):

```bash
metadata_registry_check_source() {
  local source_value=$1 entry_path=$2 entry_base=$3
  local source_words source_id found_id=0 used_by token matched i
  local -a used_by_tokens=()
  local LC_ALL=C IFS=' '
  source_words=${source_value//[^[:alnum:]_]/ }
  for source_id in $source_words; do
    [[ $source_id =~ ^S[0-9]{3,}$ ]] || continue
    found_id=1
    # ... unchanged status/used-by body, source_id in place of BASH_REMATCH[2] ...
  done
  ((found_id)) || emit_finding META_SOURCE_NO_ROW_ID info metadata \
    "entry=$entry_base source has no S-id"
}
```

Notes for the executor:

- Delete the `source_scan`/`source_id_re`/`source_match` locals and the `:2503`
  strip. `source_words` contains only `[A-Za-z0-9_]` after the substitution, so
  unquoted splitting cannot glob; the explicit `IFS=' '` and `LC_ALL=C` make it
  locale- and environment-independent. Today `metadata_registry_load` and
  `metadata_registry_entry_path` pin `LC_ALL=C` (2366, 2539) but
  `metadata_registry_check_source` does not, so its `[[:alnum:]]` boundary is
  inherited-locale dependent (C3 requires standalone **ASCII** ids).
- Static mapping to the persisted controls: `glued-before-terminal` and
  `glued-missing-before-terminal` → 0 findings; `underscore-glued` → 0;
  `nonstandalone-duplicate` and `glued-repeat-duplicate` → exactly 1
  `META_SOURCE_NOT_MINED`; `two-real-occurrences` → 2; `adjacent-real-ids` → 1
  and 0 `META_SOURCE_ROW_MISSING`. Same walk reproduces the r26 20-fixture
  matrix in `FRegistryIdBoundary.md:60-100` (b1-b12), including the four
  false-positive entries and the ×2/×3 duplicate emissions.
- Resource note (qualitative only; numeric score3 stays frozen): the old strip
  re-walks the prefix for every match, i.e. worst case quadratic in match count;
  one linear substitution replaces it. No timing or memory figure is claimed.
- The registry **row** id rule `^S[0-9]{3,}$` (`:2433`) and first-row-wins
  duplicate handling (`-z ${...+x}`) are already correct and must stay; the
  duplicate-first-row and four-digit fixtures depend on them.

## E. Filesystem-path denylist — full path, not the citation prefix

Observed: `is_denylist_path` (`595-606`) matches its globs against
`ptr_file_part "$1"` (`573-576`), which returns `${p%%:*}`. Every call site that
passes a **filesystem** path therefore truncates at the first `:` and can be
bypassed by any path whose directory component contains a colon
(`FRegistryRegistryDeny.md` B1-B6; inherited entry-reader case FRRD-2). Citation
pointers legitimately need the `path:line` split; their semantics must not change.

Suggested split (patterns copied verbatim, one matcher):

```bash
is_denylist_component() {
  local f=$1
  case "$f" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $f == *chrome-profile* || $f == *Cookies* || $f == *"Login Data"* ]] && return 0
  [[ $f == *'/.omp/'* || $f == *'/.config/'* || $f == *'/.local/state/'* ]] && return 0
  [[ $f == '.omp/'* || $f == '.config/'* || $f == '.local/state/'* ]] && return 0
  return 1
}
is_denylist_path()    { is_denylist_component "$(ptr_file_part "$1")"; }   # citations: unchanged
is_denylist_fs_path() { is_denylist_component "$(norm_ptr "$1")"; }        # filesystem: full string
```

Call-site map (all nine `is_denylist_path` uses enumerated by grep):

| Line | Argument | Class | Action |
|---|---|---|---|
| `621` | `$p` in `ptr_resolves_meta` | citation pointer | keep `is_denylist_path` |
| `636` | `$canon` from `readlink -f` | filesystem | switch to `is_denylist_fs_path` |
| `650` | `$ptr` in `check_pointer` | citation pointer | keep |
| `1129` | `$src` in `claim_source_path` | citation pointer | keep (see gap) |
| `1598` | `$ref` in `chain_ref_file` | citation pointer | keep |
| `2375` | registry `$path`, `$canon` | filesystem | switch both |
| `2382` | registry `$fdcanon` | filesystem | switch |
| `2584` | entry `$file`, `$canon` | filesystem | switch both |
| `2591` | entry `$fdcanon` | filesystem | switch |

`is_denylist_fs_path` is checked **before** each `exec {fd}<` (2377, 2586), so a
denied synthetic path is never opened. Static mapping to `round27-regressions.py`:
`plain-denied-component` → `*'/.config/'*`; `colon-denied-component`
(`synthetic:fixture/.config/registry.md`) → `*'/.config/'*` on the full string;
`colon-denied-suffix` (`synthetic:fixture.env`) → `*.env`; all exit 2 with
`metadata registry refused: denylist` and zero anchored verdict lines, while
`ordinary-colon-is-allowed` (`synthetic:ordinary.md`) matches no pattern and stays
rc 0. Existing controls stay identical: `metadata-denylist-alias`
(`:5872-5879`) denies through `$canon`, `metadata-safe-symlink` allows,
`metadata-hardlink-refused` still refuses `multilink` at the fd probe.
`round27-mechanisms.py` counts `is_denylist_path "$path|$canon|$fdcanon"` inside
`metadata_registry_load`; replacing all three makes
`C3_pointer_predicate_on_registry_path` 0 (baseline 3, see
`round27-mechanisms-before.json`).

Residual, not one of the three named failures: `claim_source_path` (`1129-1157`)
checks only the citation string and has no denylist arm on its `$canon`, so the
same colon-before-`.config` alias class is still open for claims/chain sources
(FRRD-2's other half). Whether to add `is_denylist_fs_path "$canon"` there is an
L1 scope decision; the r27 controls do not cover it, and nothing in the three
reported failures requires it.

## F. Overlap, preservation, and unrun checks

- Overlap: `ScoutRegistryWidths`/`ReviewRegistryReorder` own the width rule; my
  `header_width` hunk is included only because it is reachable from the same
  candidate branch. `ReviewRegistryBoundary`/`ReviewRegistryOccurrence` cover the
  S-id boundary from the receipt; my tokenization is the concrete repair for the
  same defect. Reviewer `ReviewCasePreservation` owns the 187-identity check.
- Existing fixtures verified statically as width-compatible: live and base
  `corpus/SOURCES.md` header/delimiter pairs are 11/11 cells (`git show` pipe
  counts 12/12); `meta-registry.md` 3/3; `meta-registry-positive.md` 4/4;
  `meta-registry-duplicate.md` 3/3; the differential's generated table 12/12.
  Three-cell headers with two- or four-cell delimiters exist only in the new
  negative controls.
- Suggested optional selftest additions (append after `metadata-registry-refused-nul`
  at live 6254-6256 / base 6235-6237; do not alter existing expectations): F1 and F2
  as rc-2 cases requiring `metadata registry has no table with id, status, and
  used-by columns`; F4 as rc 1 requiring one `META_SOURCE_NOT_MINED`; F6
  (short and long) as rc 2. They need one clean entry (`source: S001`,
  `verified-at:` with trailing text, `recheck: 90d`) and a registry row whose
  `used-by` equals its root-relative path; reuse `meta-reg-positive.md`'s entry
  shape rather than `meta-reg-bare.md` (that entry is rc 1 on its own bare date).
- Unrun: no selftest, regression suite, differential, mechanism probe, shellcheck,
  or formatter was executed and no clone was created; all rc/finding expectations
  above are static walks. Final exit codes remain for L1's single post-integration
  verification run (`bash tools/research-gate.sh --selftest`, then
  `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`,
  then the r26 differential), including the explicit baseline skip for the unsafe
  long-token reproduction.
- No tools installed; nothing was updated.
