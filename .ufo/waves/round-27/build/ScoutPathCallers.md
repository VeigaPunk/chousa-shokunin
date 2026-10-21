# ScoutPathCallers — C3 `is_denylist_path` call classification (round27 attempt1)

Seat: `ChousaR27.ScoutPathCallers` (leaf, static read-only). Base observed:
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`; `sha256 tools/research-gate.sh = c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
(6351 lines). No edits, no lane Git/jj writes, no test/gate/selftest execution, no network,
no host/live-process/`/proc` inspection, no installs.

## Assigned item

Categorize every `is_denylist_path` call in the gate as a **citation pointer** (first `:` is an
anchor, so `path:line` truncation is intended) or a **raw filesystem path** (colons are name
bytes, so truncation is a bypass). Static source review only.

## Method and LSP availability

No `lsp` device is mounted in this seat (`read xd://lsp` → “No such tool: xd://lsp”; the mounted
devices are the `ast_edit`/`debug`/`mcp__rea_*` set). Locations below therefore come from
literal text search plus reading the cited ranges; they are not semantic proof. A repo-wide
search finds calls only in `tools/research-gate.sh` (other hits are prose in `LOG.md`,
`SCORECARD.md`, `corpus/knowledge/*.md`, `.ufo/**`, and seeded executor clones, not code).

Grounding quote (C3 contract): “Filesystem-path denylist checks must inspect complete filesystem
paths, not citation-anchor prefixes” — `corpus/evidence/round27-claims.md:13` (14 words).

## Call inventory (11 calls on 9 lines; definition excluded)

| # | Location | Enclosing function | Argument and provenance | Category | Required action |
|---|---|---|---|---|---|
| 1 | `tools/research-gate.sh:621` | `ptr_resolves_meta` | `$p = norm_ptr($1)`: pointer cell from a record table (`check_pointer` `:910`, `:956`; chain hop `to=` `:998`) | citation pointer | keep pointer predicate |
| 2 | `:636` | `ptr_resolves_meta` | `$canon = readlink -f -- $cand` — resolved target of the citation’s **file part** (already truncated at `:622`) | raw filesystem path | convert to complete-path predicate |
| 3 | `:650` | `check_pointer` | `$ptr` = pointer cell (`Sources.pointer`, `Claims.pointer`) | citation pointer | keep |
| 4 | `:1129` | `claim_source_path` | `$src = norm_ptr($1)`: claims `source`, chain ref after `chain_ref_file`, `verify-all` declared claims path | citation pointer | keep |
| 5 | `:1598` | `chain_ref_file` | `$ref` = chain-row `ref`/`to` cell | citation pointer | keep |
| 6 | `:2375` | `metadata_registry_load` | `$path` = `REGISTRY_ARG`, the literal `--registry PATH` CLI value (`:6274`) | raw filesystem path | convert |
| 7 | `:2375` | `metadata_registry_load` | `$canon = readlink -f -- $path` | raw filesystem path | convert |
| 8 | `:2382` | `metadata_registry_load` | `$fdcanon = readlink -f /proc/$$/fd/$registry_fd` | raw filesystem path | convert |
| 9 | `:2584` | `verify_metadata` entry loop | `$file` = `--path` argument or a `$path/*.md` directory child (`:2560-2570`) | raw filesystem path | convert |
| 10 | `:2584` | `verify_metadata` entry loop | `$canon = readlink -f -- $file` | raw filesystem path | convert |
| 11 | `:2591` | `verify_metadata` entry loop | `$fdcanon` = readlink of `/proc/$$/fd/$meta_fd` | raw filesystem path | convert |

Tally: **4 citation-pointer calls** (`621`, `650`, `1129`, `1598`) and **7 raw-filesystem calls**
(`636`, `2375`×2, `2382`, `2584`×2, `2591`). The definition at `:595-606` is pointer semantics by
construction (`f=$(ptr_file_part "$1")`); it is not itself a call.

Why `:636` is raw: `canon` is the output of `readlink -f`, so any `:` in it belongs to a
directory or file name, not to a citation anchor. The pointer grammar was already applied to the
input at `:622`; the r21 comment at `:615-616` says the denylist must apply to the canonical
target, but the current predicate truncates that target at its first colon. [INFERENCE] A
colon-free citation `lib/benign.md` symlinked to `<root>/x:y/.config/secret.md` therefore passes
`:636` today; this shape was not executed in this seat (r26 tested the registry and entry arms,
not this pointer arm).

## Confirmed defect locations (inherited, retained evidence)

- `is_denylist_path` matches on `ptr_file_part` output: `tools/research-gate.sh:595-606`;
  `ptr_file_part` returns `${p%%:*}` at `:573-576`.
- Registry arm: `.ufo/waves/round-26/falsify/FRegistryRegistryDeny.md:25-30` (code under attack),
  `:59` (`B1 a:b/.config/reg.md` → rc 0, bytes read), `:91-97` (FRRD-1 crit).
- Entry arm: same file `:98-101` (FRRD-2: `e/a:b/.config/e.md` → rc 0, `verdict=clean`).
- The r26 M2 diagnostic (`:83-87`) changed `:596` globally and was rejected because it also
  changes citation-pointer denylisting; that is why the fix must split predicates, not patch
  `ptr_file_part`.

## Suggested change (minimal, preserves pointer semantics)

Factor the pattern body into one matcher and add a raw-path wrapper; leave `is_denylist_path`
byte-equivalent in behavior.

```bash
denylist_match() { # TEXT -> rc0 when TEXT carries a denied component
  local f=$1
  case "$f" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $f == *chrome-profile* || $f == *Cookies* || $f == *"Login Data"* ]] && return 0
  [[ $f == *'/.omp/'* || $f == *'/.config/'* || $f == *'/.local/state/'* ]] && return 0
  [[ $f == '.omp/'* || $f == '.config/'* || $f == '.local/state/'* ]] && return 0
  return 1
}

is_denylist_path() { # citation pointer: the first ':' is the anchor
  local f; f=$(ptr_file_part "$1")
  denylist_match "$f"
}

is_denylist_fs_path() { # complete filesystem path: ':' is a name byte
  denylist_match "$1" || denylist_match "$(norm_ptr "$1")"
}
```

The second `norm_ptr` probe keeps the current edge-backtick leniency (a literal path whose first
byte is a backtick followed by `.config/` is denied today) without restoring colon truncation.
`norm_ptr` strips only one leading and one trailing backtick, so it cannot hide an interior
denied component.

Rewrites: `:636`, `:2375` (both calls), `:2382`, `:2584` (both calls), `:2591` → 
`is_denylist_fs_path`. Leave `:621`, `:650`, `:1129`, `:1598` on `is_denylist_path`. No diagnostic,
exit-code, refusal order, or `die_usage` text changes.

## Expected outcome / controls

- `corpus/evidence/round27-regressions.py:154-167`: `colon-denied-component`
  (`synthetic:fixture/.config/registry.md`), `colon-denied-suffix`
  (`synthetic:fixture.env`) → exit 2, `metadata registry refused: denylist`, zero anchored
  `^RESEARCH_GATE: ` records; `ordinary-colon-is-allowed` (`synthetic:ordinary.md`) → exit 0, one
  verdict record. Today the first two bypass (colon truncation); the third must stay accepted.
- Preserved pinned behavior: selftest case 128 `ptr-deny-symlink`
  (`tools/research-gate.sh:5581-5598`), cases 129-132 `claims-{config,omp,localstate}-start` /
  `claims-config-adjacent` (`:5619-5650`), and case 152 `metadata-denylist-alias`
  (`:5876-5879`) must keep their exact exits/findings.
- Pointer-suffix semantics stay intact: `secret.env:12` is still refused because `:621`/`:650`/
  `:1129`/`:1598` truncate at the anchor before matching `*.env`.
- Expected deltas only at the seven raw-path calls; no new refusal for paths with a colon but no
  denied component.

## Additional synthetic fixtures worth adding (executor/verifier; all under `mktemp -d`)

1. Registry symlink to a colon-denied target: `benign.md` → `synthetic:fixture/.config/reg.md`.
   Raw name is clean; canonical is denied. Expected exit 2 `refused: denylist` with no
   `RESEARCH_GATE:` record. This exercises the `:2375` canon arm distinctly from the raw arm,
   mirroring selftest case 152 for metadata entries.
2. Entry reader colon shape (FRRD-2): `--path <tmp>/synthetic:fixture/.config/entry.md` with valid
   `source/verified-at/recheck` frontmatter → exit 1,
   `FINDING META_ENTRY_REFUSED ... reason=denylist unparsed`, `METADATA_COMPLETE=0/1`; and
   `<tmp>/synthetic:ordinary.md` → exit 0. Covers `:2584`/`:2591`.
3. Pointer canonical target: record `Sources` pointer `lib/benign.md` symlinked to
   `<tmp>/lib/synthetic:fixture/.config/private.md` → `RESEARCH_GATE: DRIFT`,
   `FINDING POINTER_UNRESOLVED severity=warn surface=sources` (the exact shape of case 128 at
   `:5581-5598`). Covers `:636`. [INFERENCE] This fails today; not executed here.
4. Per-fixture negative control: same shapes with `synthetic:ordinary` and no denied component
   must remain accepted, so the fix cannot pass by refusing every colon path.

## Out-of-scope observations (not required by C3’s three named failures)

- `claim_source_path` checks the denylist only on the raw citation (`:1129`) and never rechecks
  the canonical target before the stat/device probes (`:1140-1218`). A colon-free citation
  symlinked to an in-root `x:y/.config/...` target would still be read. Inherited gap; changing it
  would expand claim semantics beyond C3 and alter original-187 behavior, so flag only.
- `sweep_path_guarded` (`:1859-1891`) performs containment checks with no denylist call; sweep
  locations are not currently denylisted by design.
- Citation-pointer grammar itself still treats the first `:` as an anchor (`:573-576`); a
  literal-colon path cited as a pointer is truncated before resolution. C3 requires preserving
  that semantics, so the new fs predicate does not change it — only the resolved/canonical and
  CLI/directory inputs get complete-path matching.
- `--registry` existence/readability tests precede the denylist (`:2367-2373`), so absent denied
  paths report “not found” (FRRD-5). Exits stay 2; untouched.

## Unrun checks / limits

- Not run (lane bounds): `bash tools/research-gate.sh --selftest`,
  `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`, any gate
  invocation, the r26 harness, the date/registry differentials, shellcheck/bash -n. No expected
  pass is claimed from this seat.
- No LSP server answered; the call inventory is a literal-search plus line-range reading, and
  selector/refactor advice is based on that reading.
- No tools installed or updated; no pacman/uv/npm/official-binary action taken.
- Integration owner must run the single post-integration verification and confirm the original
  187 selftest identities plus the C3 controls.

## Trailer

Seat `ChousaR27.ScoutPathCallers`; report `.ufo/waves/round-27/build/ScoutPathCallers.md`; base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`; observed gate
`tools/research-gate.sh` sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Read-only: no product code, tests, fixtures, indexes, or sibling reports were modified.
