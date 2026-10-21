# ScoutLegacyHolds — differential/legacy command inventory and sandbox map

Seat: ChousaR27.ScoutLegacyHolds (leaf, static read-only). Base observed:
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`. No gate, selftest, differential,
probe or interpreter against fixtures was executed. No edits to production, no
lane Git/jj/index writes. No tools installed or updated.

## Assigned item

Map the existing small differential and legacy-preservation commands and the
sandbox layout they depend on, without running them.

## 1. Differential / counting commands (existing)

| Command (verified from the file header/usage) | What it compares | Frozen dependency | Exit meaning | Sandbox |
|---|---|---|---|---|
| `bash corpus/evidence/round26-date-differential.sh [GATE]` (`round26-date-differential.sh:1-16`) | `verify-metadata --as-of` due/freshness pairs against a Python `datetime` oracle over sampled years 1900–2100, leap/century boundaries, explicit ISO rechecks, and invalid inputs (`:19-206`) | None; default gate is `tools/research-gate.sh` of this repo | 0 all agree (`DATE_DIFF_AGREE=N/N`); 1 any mismatch/duplicate/exit outside 0/1; 2 usage | `tempfile.TemporaryDirectory(prefix="round26-date-diff-")` (`:88`), resolved root, one fixture dir per batch, gate `cwd=root`, `CHOUSA_STRICT=0` (`:88-101`); honors `TMPDIR` |
| `bash corpus/evidence/round26-registry-differential.sh [GATE-TREE]` (`round26-registry-differential.sh:1-24`) | Gate vs `round26-registry-oracle.py` on frozen `r24plus` (5) + `pop29` (29) + generated adversarial (14) roots; `REGISTRY_DIFF_AGREE=N/M` | Inputs are `git show ba3333254dd337658a4f25e7a9471f9cf4e4567e:…` from the repo containing the script (`:51-70`); the oracle itself is read from the working tree, not from the base commit | 0 all suites agree; 1 disagree/suite-shape failure; 2 missing tree/gate/base commit | `mktemp -d /tmp/chousa-r26-registry-diff.XXXXXX` (`:26`, hardcoded `/tmp`), `$TMP/{label}.gate|.oracle.json|.stderr`, `$TMP/results.tsv`, trap removes; adversarial root plus an out-of-contract escaped-pipe root (`:117-176`) |
| `bash corpus/evidence/round25-meta-differential.sh` (no arguments, `:1-8`) | Three derivations per fixture: hand README table, gate, `round25-meta-oracle.py`; 27 fixtures × normal/strict; asserts 27 rows and exact file population | `corpus/fixtures/metadata-r25/` (27 `.md` + README) | 0 `AGREE=54/54`; 1 any disagreement; uncaught assert exits nonzero | None: cwd must be the lane root (relative `tools/research-gate.sh` and fixtures); only `CHOUSA_STRICT` is set per run; all other inherited `CHOUSA_*` remain |
| `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh [--output PATH]` (current file sha256 `3198bf21…aa751`, 183 lines) | Independent C1/C2/C3 synthetic contract controls; embeds the shipped C1 helper text and reads it from the gate source (`:69-91`) | The gate source text and the helper name/shape; no corpus files | 0 all declared expectations matched; 1 any mismatch; 2 setup/arg/helper-not-found | `tempfile.TemporaryDirectory(prefix='chousa-r27-synthetic-')` (`:47`); strips every inherited `CHOUSA_*` then sets `CHOUSA_STRICT=0`, `LC_ALL=C` (`:24-26`); per-run `LC_ALL` overrides; `timeout=30` per gate call (`:61-67`); synthetic `synthetic-cli.sh`, entry, registry, `.config`/colon paths |
| `python3 corpus/evidence/round27-mechanisms.py GATE` | Syntactic count of the six reported r26 mechanisms; prints JSON only | Gate text and function names/shape (`:15-24`) | Always 0 on successful counting; explicitly not an admission gate (`:2-5`) | None |
| `bash corpus/evidence/round25-measure.sh <tree-root>` / `bash corpus/evidence/round24-measure.sh <tree-root> [QUALITY.md]` | Historical r25/r24 counting probes (selftest count, stale indexes, registry rows) | Tree contents; r24 needs fleet root `SHOKUNIN_ROOT` | Measurement only; comparisons are manual | `mktemp -d` (`round25-measure.sh:18`), `mktemp -d` for the r24 manifest; r25 census also usable as `bash corpus/evidence/round25-sources-census.sh [TREE]` |

## 2. Legacy preservation commands and frozen anchors

| Command | Freeze / comparison | Anchor observed |
|---|---|---|
| `bash corpus/evidence/round25-holds/battery.sh TREE_ROOT [ANALYSIS_ROOT]` | Runs 12 holds against `corpus/evidence/round25-holds/holds/*.log`; masks `ts=` and `gate_sha256` (`:19-38`); for selftest compares only `ok-case` 1–136 plus `EXIT_CODE` (`:54-63`), deliberately not the final total | Selftest baseline `holds/selftest.log` ends `ok-case 136 json-unreadable-manifest`, `PASS (136 cases, 0 skipped)`, `EXIT_CODE=0`; twelve `MATCH` rows and `EXIT_CODE=0` in `corpus/evidence/round25-final-holds.log:1-14` |
| `bash corpus/evidence/round26-measure.sh TREE holds` (also `c1|c2|c3|all`) | `holds` runs the tree's selftest, hashes the **first 161 `^ok-case` lines**, runs `--drift` on the r12 baseline, and counts `VERDICT_BEARING_EXPORTS` (`round26-measure.sh:225-232`) | Base: `RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)`, `LEGACY_CASES_SHA=5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb`, `GATE_DRIFT: none`, `3/3` (`round26-measure-before.log:66-70`). Candidate: `FAIL (3/187 cases)`, same SHA, `none`, `3/3` (`round26-inherited-after.log:42-46`) |
| Direct byte-identity check available from committed evidence | `head -161 corpus/evidence/round25-retained-final-selftest.log` hashes to the same `5eac4a7e…e01cb` (checked here with `sha256sum` over the committed file only), so the first 161 **numbered names and exit codes** are preserved byte-for-byte, not just as a count | `round25-retained-final-selftest.log:1-161` + summary line 162 |
| `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` | Canonical verify-all capture byte-compare with volatile masking | `GATE_DRIFT: none`, exit 0 (`round26-measure-before.log:68-69`; battery `:73`). r8 baseline stays committed but the r12 baseline is the active check (`corpus/knowledge/gate-baseline-r12.md:5,35`) |
| `bash tools/research-gate.sh --pin PATH` | Writes a new baseline | **Must not be used during r27 verification**; it mutates evidence |

`round26-measure.sh` reads the frozen population from the gate's base commit via
`git -C ${R26_BASE_REPO:-/home/vgpnk/Projects/shokunin/chousa-shokunin} show ba333325:…`
(`:7-31`), so it works with an isolated `TREE` while keeping the population fixed.
`round25-holds/battery.sh` takes the tree as `TREE_ROOT` but uses
`ANALYSIS_ROOT` (default `/home/vgpnk/Projects/shokunin`) for the r1 archived
export (`:8-9,72-90`).

The isolation method documented by the earlier counting probes is
`git -C <lane> archive <commit> | tar -x -C <dir>` (`round25-measure.sh:4-7`,
`round24-measure.sh:3-6`). An archive has no `.git`, which is why the registry
differential must be launched from a repo that still has the base commit (gap 5).

## 3. Sandbox layout

### Gate selftest (`run_selftest`, `tools/research-gate.sh:3366-6247`)

| Object | Definition | Lifetime |
|---|---|---|
| `WORK` | `mktemp -d "${TMPDIR:-/tmp}/chousa-research-gate-selftest.XXXXXX"` (`:3368`) | trap `rm -rf` (`:3373`) |
| `OUTSIDE_FILE` | `mktemp "${TMPDIR:-/tmp}/chousa-gate-outside.XXXXXX"` (`:3371`), a file outside `WORK` used by out-of-corpus controls | trap removes |
| `GATE_CAP_DIR` | `mktemp -d "${TMPDIR:-/tmp}/chousa-gate-pin.XXXXXX"` (`:3133`) for `--pin/--drift` canonical capture; removed at end of capture and re-swept by the selftest trap (`:3377`) | trap removes |

Fixture skeleton: `$WORK/lib` (primary, chain, boundary), `$WORK/noise`,
`$WORK/claimsrc` (`:3381-3392`), then per-case dirs `meta-asof` (`:6044`),
`meta-registry*`/`meta-*` controls, `$WORK/corpus/knowledge` (`:6191`),
deliberate denied dirs `$WORK/.config`, `$WORK/.omp`, `$WORK/.local/state`
(`:5626-5640`), and symlink/namespace fixtures `aliasroot`, `crossdev`,
`nsprobe`, `sweepdir`, `sweepdir2`, `safe`, `target`. Cases are spawned as fresh
`bash "$SELF"` processes with `CHOUSA_ROOT=$WORK`, `CHOUSA_NOW_EPOCH`, unset
`CHOUSA_RECORD`, `CHOUSA_CLAIMS`, `CHOUSA_AGGREGATOR_ERE`, and `CHOUSA_STRICT=0`
(`:3454-3466`, repeated per runner).

Two sibling directories are created outside `WORK` as `$WORK/../chousa-outside-r19`
(`:5457-5459`) and `$WORK/../chousa-config-r21/.config` (`:5583-5585`) but are not
in the EXIT trap. They persist under `TMPDIR` after a selftest and are shared by
concurrent selftest runs. [Observed from source; not executed.]

### Differential sandboxes

| Script | Root | Notes |
|---|---|---|
| date differential | Python temp root; `case-00000.md` … per batch | Gate is run with `cwd=root`, `--root root`, `CHOUSA_STRICT=0`; fixtures are 4-line synthetic metadata entries |
| registry differential | `TMP/r24plus/root`, `TMP/pop29/root`, `TMP/adversarial/root` | Frozen files from the base commit; oracle output JSON per suite; adversarial `entries` are inline Python-written files |
| r26 measure | `W=/tmp/r26m.XXXXXX` with `W/frozen` (29 entries + base `SOURCES.md`), `W/c1`, `W/c2`, `W/c3`, `W/pop24`, `selftest.txt`, `drift.txt` | `peak()` runs each gate invocation in a fresh Python child with a 300 s cap (`:38-49`); C1 shapes are 8,388,000 bytes |
| r25 holds battery | `mktemp -d` (bare, honors `TMPDIR`) | One raw log + masked copy per hold; baseline logs live in the repo |
| r27 regressions | `tempfile.TemporaryDirectory(prefix='chousa-r27-synthetic-')` | `root/corpus/knowledge/entry.md`, `root/registry.md`, `root/synthetic-cli.sh`, plus the denied/allowed colon fixtures; no repo fixture reads |

Environment knobs that change sandbox resolution:

- `CHOUSA_ROOT` — default `$PWD` (`:286`) and **re-applied over the CLI `--root`**
  inside each mode (`ROOT=${CHOUSA_ROOT:-$ROOT}`, e.g. `:795`). An inherited value
  silently overrides a differential's `--root`.
- `CHOUSA_NOW_EPOCH` — pins verdict clock; selftest sets it, differentials do not.
- `CHOUSA_STRICT`, `CHOUSA_RECORD`, `CHOUSA_CLAIMS`, `CHOUSA_AGGREGATOR_ERE` —
  inherited test knobs; the selftest unsets all but `STRICT`, `round27-regressions`
  strips every `CHOUSA_*`, and the r25/r26 scripts do not.
- `TMPDIR` — honored by the gate (`:3133,3368,3371`) and the date/r27 Python
  sandboxes; **ignored** by `round26-registry-differential.sh` and
  `round26-measure.sh`, which hardcode `/tmp`.
- `SHOKUNIN_ROOT` / `R26_BASE_REPO` — fleet analysis root and base repo for
  r24/r25/r26 counting commands; `LANE_ROOT` is `$SCRIPT_DIR/..` (`:276`).

Gate-side read constraints that shape fixtures: 8 MiB source cap
(`SOURCE_READ_MAX_BYTES`, `:271`), registry reader opens `/proc/$$/fd/<n>` and
refuses multi-link files (`:2375-2405`), so synthetic fixtures must be regular,
single-link, below the cap. The source itself contains the two outside-`WORK`
sibling dirs noted above.

## 4. Calibration couplings observed in the new round-27 controls

- `round27-mechanisms.py` extracts `metadata_iso_date`, `metadata_add_days`,
  `metadata_registry_load`, `metadata_registry_check_source` with
  `^NAME\(\).*?^}` (`:15-24`). Keep those names at column 0 with a column-0
  closing brace. Expected post-repair counts are all zero, including a literal
  `local LC_ALL=C` **inside** `metadata_iso_date`
  (`C2_locale_unpinned_date_validator`) and no `digits=${digits##+(0)}`
  (`C2_recursive_zero_strip`).
- `round27-regressions.py` extracts the C1 helper by
  `^  metadata_asof_usage_case\(\).*?^  }\n` (or the alternate
  `metadata_asof_usage_accepts`, `:69-79`) but always invokes
  `metadata_asof_usage_case` (`:89`). A rename without a callable
  `metadata_asof_usage_case` would make the negative controls silently pass
  through `failures=0`; keep the old name callable or keep both.
- C1 scenarios pin: exit 2 with help text is accepted; a real anchored
  `RESEARCH_GATE: CLEAN`/`DRIFT` record must fail the helper; exit 1 must fail;
  a missing diagnostic must fail; a non-record line containing the substring
  (`note RESEARCH_GATE: not a record`) must not be treated as a verdict (`:80-91`).
- C2 controls pin exit 2 plus the exact diagnostic `--as-of must be a valid
  YYYY-MM-DD date` for Unicode-digit inputs under `C` and `en_US.UTF-8`, forbid
  `invalid integer`, `arithmetic syntax`, `cannot change locale`, and require
  zero anchored verdict records (`:96-124`).
- C3 controls pin exact messages `metadata registry has no table` and
  `metadata registry refused: denylist`, rc 2 with zero verdict records for the
  refused cases, fresh named headers after prose, header/delimiter width match,
  standalone-ASCII S-id occurrence counts, and full-path denylist semantics
  including a colon before a denied component and a colon before a `.env` suffix
  (`:126-170`).

## 5. Gaps and hazards for the integration run

1. **No committed full 187-identity listing.** Only the r26 failure names
   (`metadata-asof-invalid`, `metadata-asof-missing`, `metadata-asof-wrong-mode`)
   and the summary `FAIL (3/187 cases)` are committed. Cases 1–161 have a byte
   baseline (`round25-retained-final-selftest.log`, hash above); cases 162–187 do
   not. Identity preservation for the last 26 must come from a static source
   enumeration or from the final selftest output checked for ordinal+name against
   a frozen list created before integration, not from the total alone.
2. **Skip-case shifts the legacy SHA.** `round26-measure.sh:229` hashes the first
   161 `^ok-case` lines; a namespace skip prints `skip-case` and moves later lines
   into the window. Compare the SHA only with the same skipped count as r26
   (`0 skipped` in both receipts).
3. **No baseline-skip switch in `round27-regressions.py`.** The claims require the
   unsafe long-token case not to be rerun on the base archive and the skip to be
   marked explicitly, but the current runner has only `--gate`/`--output` and
   executes `leading-128k-zeros` unconditionally (30 s timeout, `:61-67,96-97`).
   The base-archive receipt therefore needs either a named skip mechanism added by
   L1 (and the runner re-run unchanged apart from that flag) or an explicit
   statement that the base C2 item is inherited from the r26 receipt.
4. **Registry oracle is not frozen.** The differential pins its *inputs* to
   `ba333325`, but `ORACLE=$SCRIPT_DIR/round26-registry-oracle.py` is the working
   tree copy; a candidate tree can differ only if that file is copied, so record
   its digest with the receipt.
5. **Registry differential needs a git repo.** It resolves `REPO` from the script
   location and requires the base commit there (`:19-23`), so an isolated
   `git archive` tree must be passed as `GATE-TREE` while the script is invoked
   from a clone that still has the base commit; a bare archive cannot host the
   script.
6. **Inherited `CHOUSA_ROOT` overrides `--root`.** Differential scripts other than
   the r27 runner do not clear it. Run each differential with `env -u CHOUSA_*`
   or in a clean environment, else fixture roots can be redirected.
7. **Hardcoded `/tmp`.** Registry differential and r26 measure ignore `TMPDIR`;
   on a constrained `/tmp` these are the first to fail with rc 2.
8. **Outside-`WORK` siblings.** `chousa-outside-r19` and `chousa-config-r21` are
   not removed by the selftest trap; concurrent selftests can collide on them.
   [Observed static.]
9. **`--pin` mutates evidence.** The frozen metadata check is `--drift` only.

## 6. Unrun checks (all intentionally not executed)

- `bash tools/research-gate.sh --selftest` and any numbered case capture.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`
  (base archive and integrated tree).
- `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh`.
- `bash corpus/evidence/round26-date-differential.sh` (any gate path).
- `bash corpus/evidence/round26-registry-differential.sh` (any tree).
- `bash corpus/evidence/round25-meta-differential.sh`.
- `bash corpus/evidence/round25-holds/battery.sh` and
  `bash corpus/evidence/round26-measure.sh TREE holds|all`.
- `bash tools/research-gate.sh --drift …-r12-….json`, `--pin`, and every
  `round25-sources-census.sh` / `round25-measure.sh` / `round24-measure.sh` probe.

Only static reads and the committed-file `sha256sum` of
`round25-retained-final-selftest.log` were performed. No claim of a passing
gate, differential, or selftest is made here.
