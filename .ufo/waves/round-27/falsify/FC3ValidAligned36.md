# FC3ValidAligned36 — falsification of C3 control `valid-aligned`

- Target: chousa-shokunin @ dd72641e574679c4f7882dd43de072b4c8892d6f (master). Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches brief).
- Control: `corpus/evidence/round27-regressions.py:142` (assertion logic `:31–41`, table loop `:144–150`).
- Comparison base: 64eec5d41c7cf7f17f5ce1e968e28b3769952596, gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
- Sandbox: `/tmp/chousa-r27-falsify-FC3ValidAligned36` (lane files untouched; no installs; no network).

## Verdict

**FALSIFIED (narrow).** The control's expectation is correct and matches base behavior, and the landed gate's aligned-table behavior holds (no fail-open found in the aligned class). As a *guard*, `valid-aligned` is:

1. **vacuous for registry consultation**: a gate that ignores `--registry` passes it (CE1);
2. **reason-blind** on its rc-0 path: a setup/parse error fails it with the same signature as an over-rejection (CE2);
3. **silent on the 1–2-dash delimiter boundary**, and it is the only colon-grammar fixture in the suite (CE3).

## 1. Is the expectation derived from the declared contract, independent of gate code?

- **Independent of gate code: yes.** Fixture and expectation (rc 0; one `^RESEARCH_GATE: ` line; no `required`, no `forbidden`) are literals. `regressions.py` imports no gate regex. Its gate-text read (`:25`) feeds only usage-helper extraction, not this control.
- **Derived from a declared contract: no.** No declared clause names alignment markers. The revision's docs (`corpus/README.md`, `knowledge/metadata-screen-r25.md`, `knowledge/registry-link-r26.md`) show only plain `|---|` delimiter rows. `corpus/README.md` cites `kaika/SOURCES-CONTRACT-v1.md`, which is absent from the archived revision. The gate usage text says only "a bounded SOURCES.md table" (`research-gate.sh:322`).
- **Actual anchor: pre-existing behavior.** Base accepts the fixture (probe: base rc 0). Base uses the same cell rule `^:?-{3,}:?$` (base `:2446`), unchanged at landed `:2469`. Markdown/GFM delimiter syntax is the implicit contract [INFERENCE: no GFM-capable parser runs offline; `/usr/bin/cmark` renders the table as a paragraph].
- **Net:** a non-regression pin for colon grammar. It is not a test of the landed width repair.

## 2. Revert / mutate the targeted fix

Targeted region in landed `metadata_registry_load`: width check `:2466`, cell rule `:2469`, header width `:2490`. Each mutant is a one-line edit of a sandbox copy (`diff` confirmed one changed line each).

Probe `fc3-probe.py` runs single `verify-metadata … --registry` invocations with the control's fixture text, env (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL=C`), argv order, and rc/count semantics. Cells are `rc` plus ✓/✗ against the fixture's expected rc.

| fixture (expected rc) | base | landed | M1 drop colons `:2469` | M3 left colon only `:2469` | M4 no width check `:2466` | M6 width+1 `:2490` | M7 1–2 dashes `:2469` | REG `--registry` ignored `:6552` | SYN missing `}` `:2469` |
|---|---|---|---|---|---|---|---|---|---|
| ctl-valid-aligned (0) | 0✓ | 0✓ | 2✗ | 2✗ | 0✓ | 2✗ | 0✓ | 0✓ | 2✗ |
| ctl-valid-table (0) | 0✓ | 0✓ | 0✓ | 0✓ | 0✓ | 2✗ | 0✓ | 0✓ | 2✗ |
| right-only (0) | 0✓ | 0✓ | 2✗ | 2✗ | 0✓ | 2✗ | 0✓ | 0✓ | 2✗ |
| one-dash-aligned (0, GFM) | 2✗ | 2✗ | 2✗ | 2✗ | 2✗ | 2✗ | 0✓ | 0✓ | 2✗ |
| too-few-aligned (2) | 0✗ | 2✓ | 2✓ | 2✓ | 0✗ | 2✓ | 2✓ | 0✗ | 2✓\* |
| too-many-aligned (2) | 0✗ | 2✓ | 2✓ | 2✓ | 0✗ | 0✗ | 2✓ | 0✗ | 2✓\* |
| queued-aligned (1) | 1✓ | 1✓ | 2✗ | 2✗ | 1✓ | 2✗ | 1✓ | 0✗ | 2✗ |
| ctl-delimiter-too-short (2) | 0✗ | 2✓ | 2✓ | 2✓ | 0✗ | 2✓ | 2✓ | 0✗ | 2✓\* |
| ctl-reorder-queued, non-aligned (1) | 0✗ | 1✓ | 1✓ | 1✓ | 1✓ | 2✗ | 1✓ | 0✗ | 2✗ |

\* Probe checks rc and verdict count only. The real suite also requires `metadata registry has no table` on rc-2 fixtures (`regressions.py:146–148`), which SYN does not print, so these would fail there too.

Reading the matrix against the control:
- **M1 / M3 / M6** fail `valid-aligned` with rc 2 and zero verdict lines. Stderr is `research-gate: metadata registry has no table with id, status, and used-by columns`, so the intended reason holds. The control's own MISMATCH text (`exit 2 != 0; count '^RESEARCH_GATE: ': 0 != 1`) does not name it, because `required=()` on rc-0 controls.
- **M1 / M3** are caught only by `valid-aligned`. `ctl-valid-table` passes both. No other regression fixture contains a colon delimiter.
- **M4** (remove width check) does not trip `valid-aligned`. That is correct: it is not a width detector. The width repair is guarded by `ctl-delimiter-too-short/long`, which fail under M4.
- **M7** (accept 1–2 dashes) passes `valid-aligned` and every fixture in the suite (see CE3).
- **REG** passes `valid-aligned` vacuously (CE1).
- **SYN** fails `valid-aligned` with the same observable signature as M1 (CE2).

## 3. Counterexamples (minimal)

**CE1 — vacuity (registry ignored).** Mutant REG: `research-gate.sh:6552` `REGISTRY_ARG_SET=1` → `=0`. On the control fixture: rc 0, one verdict line, `META entry=entry.md source=present … verdict=clean` → PASS. Every rc-0 table control I replicated passes under REG (`ctl-valid-table`, `ctl-valid-aligned`); by fixture inspection so do the rc-0 `valid-*`, `ordinary-colon-is-allowed` and zero-occurrence `glued-*` controls [not run]. Requiring `source=present` does not fix this: `source_state` comes from the `source:` key alone (`:2712–2713`); registry consultation (`:2718–2721`) emits findings only. Aligned negatives fail under REG (`queued-aligned` → rc 0, expected 1), but the suite has no aligned negative. The non-aligned `reorder-queued` fixture (`regressions.py:137`) is the only control that catches REG here (replica: rc 0, expected 1) [suite not run].

**CE2 — reason-blindness on the rc-0 path.** Mutant SYN: line 2469 missing its closing `}`. `valid-aligned` → rc 2, zero verdict lines, stderr `…line 2470: syntax error near unexpected token`. Its MISMATCH text is identical to M1/M3/M6, because rc-0 controls have `required=()` (only rc-2 fixtures get the `no table` requirement, `:146–148`).

**CE3 — 1–2-dash boundary unpinned.** Mutant M7: `^:?-{1,}:?$`. `valid-aligned` passes. Escape-aware search `[|n]:?-{1,2}:?(\||\\)` matches nothing in `round27-regressions.py` or `research-gate.sh`, so M7 survives the 58-control suite by construction [fixture inspection; suite not run]. The gate's own selftest has no alignment-colon rows either (`grep -c -F ':---' tools/research-gate.sh` → 0). The only colon-grammar pin in the suite is line 142.

**CE4 — GFM-divergent rejection, fail-closed, inherited.** `| id | status | used-by |` / `|:-|-:|:-:|` / `| S001 | mined | corpus/knowledge/entry.md |` → rc 2 "no table" on base and landed. Same for `|-|-|-|` and `|:--|--:|:--:|`. GFM admits one or more hyphens [INFERENCE]. Fail-closed and not a landed regression, but the 3-dash minimum is pinned by nothing (CE3).

**CE5 — adjacent fail-open (inherited, outside the landed C3 change).** Aligned table, then `| S001 | mined | corpus/knowledge/entry.md |` followed by `| S001 | queued | corpus/knowledge/entry.md |` → rc 0 CLEAN on base, landed, and REG. First-row-wins (`research-gate.sh:2455`) silently ignores the conflicting later row. The selftest pins only queued-first (`metadata-registry-duplicate-first-row`).

## 4. Held (no counterexample found)

- **Well-formed aligned variants:** 13 of 13 accepted by landed (rc 0, one verdict). Covered: left/right/center/no-colon, no outer pipes, inner spaces, CRLF, trailing spaces, tab padding, mixed outer pipes, extra data cell, reordered columns.
- **Malformed delimiters:** 12 of 12 rejected by landed (rc 2). Covered: double colon, inner-space cell, fullwidth colon, U+2010 hyphens, too-few and too-many cells, empty delimiter cell, trailing-empty header cell, blank or prose between header and delimiter.
- **Data-row faults:** 7 of 7 fail closed on landed (rc 1). Covered: short used-by, one-pipe row, queued status, wrong used-by, second-table-only, first-row-queued duplicate, non-aligned reorder-queued.
- **Width repair effective vs base:** base accepts too-few/too-many aligned and ctl-delimiter-too-short/long (rc 0), and base fails non-aligned reorder-queued (rc 0). Landed rejects or corrects all five.
- **Real lane registry:** `corpus/SOURCES.md` (11-cell header and 11-cell delimiter) with `corpus/knowledge/json-delimiter-r24.md` → rc 0 `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`. Base output identical.
- **NBSP trailing cell:** rc 2 on both; GFM status unknown, not claimed.

## 5. Axes

- **Calibration:** the control is correct but weak. Vacuous for registry consultation (CE1), reason-blind on rc 0 (CE2), no 1–2-dash pin (CE3), single point of failure for colon grammar. Landed aligned behavior produced no false CLEAN across 37 fixtures.
- **Operability:** the rc-0 MISMATCH text cannot name a cause. Exit 2 is "setup/usage" per the gate header (`research-gate.sh:9`), so over-rejection and setup error look the same unless stderr is read.
- **Freshness:** not applicable. No `--as-of`; plain-mode META has no due/freshness fields; rc is independent of wall clock.

## 6. Commands and exit codes (sandbox)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C $S` → exit 0; `sha256sum tools/research-gate.sh` → `ca39d14db907ec3f…` (match).
- `git -C … archive 64eec5d… | tar -x -C $S/base-64eec5d` → exit 0; base sha `c2c813f1…`.
- `diff -u base-64eec5d/tools/research-gate.sh tools/research-gate.sh > gate.diff` → exit 1; 494-line diff, inspected for registry/denylist hunks.
- `python3 fc3-probe.py --gate <gate> --label <label>` → exit 0 for base, landed, M1, M3, M4, M6, M7, REG, SYN; 37 fixtures each; ~0.1 s per gate. Output in `probe3-*.tsv`.
- `diff tools/research-gate.sh mut/<M>/tools/research-gate.sh` → exit 1; one changed line per mutant (M1 `:2469`, M3 `:2469`, M4 `:2466`, M6 `:2490`, M7 `:2469`, REG `:6552`). SYN changed `:2469` only. Hashes: M1 `6520509e…`, M3 `d2d51123…`, M4 `f48d439e…`, M6 `6532fca1…`, M7 `345a68e9…`, REG `48e415b5…`, SYN `e757d8b9…`.
- Escape-aware search `[|n]:?-{1,2}:?(\||\\)` over `round27-regressions.py` and `research-gate.sh` → no match.
- Search `[|n]:-{3,}|-{3,}:(\||\\)` → only `round27-regressions.py:142`.
- `env -i PATH=$PATH HOME=$HOME LC_ALL=C CHOUSA_STRICT=0 bash tools/research-gate.sh verify-metadata corpus/knowledge/json-delimiter-r24.md --root . --registry corpus/SOURCES.md` → exit 0, `RESEARCH_GATE: CLEAN`; base output identical.

## 7. Limits

- **Not run:** the full `--selftest` and the 58-control regression script (bounded). `fc3-probe.py` replicates `valid-aligned`'s invocation and `observe()` semantics for rc and verdict count. Suite-level claims (M7 survives; REG caught by `reorder-queued`) rest on fixture inspection plus single-fixture replicas.
- **No offline GFM oracle:** `cmark` is CommonMark-only (table rendered as paragraph); Node v24.21.0 has no markdown package; no network; pacman paused. Every GFM statement is marked [INFERENCE].
- **Mutants:** single-line, not exhaustive. Fixture set is hand-picked (37 rows).
- **Real-registry check:** ran on the sandbox copy of the lane's own corpus files (lane revision content, not host files).
- **Incidental:** one `ls ../` in the sandbox listed `/tmp` names only. No file contents outside the sandbox were read. No `/proc`, live processes, strace, debugger, mount, or network.

## 8. Author-lane advice (not outside admission)

1. Keep `valid-aligned`: it is the only pin on colon grammar.
2. Add aligned negative twins using `|:---|---:|:---:|`: `queued` (rc 1 + `META_SOURCE_NOT_MINED`) and absent S-id (rc 1 + `META_SOURCE_ROW_MISSING`). These fail under REG inside the class.
3. Give colon over-rejection twins (too-few/too-many/double-colon aligned) `required=('metadata registry has no table',)`. Add a setup-error canary (`forbidden=('syntax error',)`) on the aligned positive.
4. Do not adopt `required=('source=present',)` as the registry-consultation proof (CE1).
5. Decide the dash minimum (gate `{3,}` vs GFM `-+`) and pin both sides; M7 currently survives the suite by construction.
6. Decide the duplicate-row policy (CE5) and pin it if it is contract.

## 9. Tooling record

- No installs or updates performed.
- Versions used: GNU bash 5.3.20; `/usr/bin/python3` 3.14.8; Node v24.21.0 (present, not used as a Markdown oracle); `/usr/bin/cmark` (CommonMark-only, not used as a GFM oracle).
- No pacman; no network.

## 10. Sandbox artifacts

`/tmp/chousa-r27-falsify-FC3ValidAligned36/`: `tools/` (dd72641e), `base-64eec5d/` (64eec5d), `mut/{M1,M3,M4,M6,M7,REG,SYN}/tools/research-gate.sh`, `fc3-probe.py`, `probe*.tsv`, `real-*.out`, `gate.diff`.

## Erratum (appended after write; corrects two statements above)

- Timing (§6): each `fc3-probe.py` run (37 gate invocations) took about 0.5 s, so about 13 ms per invocation. The "~0.1 s per gate" figure is wrong.
- Axes (§5): "no false CLEAN across 37 fixtures" is wrong. Within the colon/width class no false CLEAN was found. The adjacent aligned duplicate fixture `dup-first-mined-then-queued` returns rc 0 CLEAN on base, landed, and REG (CE5). Read the §5 bullet as "no false CLEAN within the colon/width class".
