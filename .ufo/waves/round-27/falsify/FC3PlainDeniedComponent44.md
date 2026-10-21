# FC3PlainDeniedComponent44: falsification of C3 control `plain-denied-component`

Scope: round 27, attempt 1, falsify wave, C3 only. Pinned target `dd72641e574679c4f7882dd43de072b4c8892d6f`; gate `tools/research-gate.sh` sha256 `ca39d14d…` (matches pin). Control: `corpus/evidence/round27-regressions.py:166-175` (sha256 `5afea786…`). Base for comparison: `64eec5d41c7cf7f17f5ce1e968e28b3769952596` (gate sha256 `c2c813f1…`). Sandbox: `/tmp/chousa-r27-falsify-FC3PlainDeniedComponent44` (target) and `…-base` (archives). Synthetic fixtures only. The full selftest and the 58-case regression script were NOT run.

## Verdict

**FALSIFIED (scoped).** The control does not guard the C3 repair: it passes on base, passes when the repair is reverted, and is blind to over-broad denial. Its own expectation HOLDS: a colon-free `.config` component is refused, and no input found reads one.

Adjacent counterexample, same helper and same C3 sentence: the landed repair still denies a benign complete path on its citation-style prefix (C-A below).

## Q1. Is the expectation derived from the declared contract, independent of gate code?

Partly.

| Element of the expectation | Source | Status |
|---|---|---|
| `.config/` is a denylisted component | `corpus/knowledge/denylist-r22.md:9-21` (`*/.config/*`, bare-start `.config/`*) | Declared lane policy. The note cites gate lines, so it is lane-internal, not an external spec. |
| refused registry exits 2 | `corpus/evidence/round26-claims.md:90-93` ("unreadable/refused FILE … exits 2"); `:36-37` (denylist refusal unchanged) | Declared. |
| no verdict line on a refusal or usage error | `corpus/evidence/round27-claims.md` C1 (line 7) | Declared. |
| exact stderr `metadata registry refused: denylist` | No contract document. Grep of SKILL.md, MINT.md, README.md, PROVINCE.md, corpus/knowledge, corpus/README.md, corpus/evidence/README.md, round26-claims.md, round27-claims.md: no hits (exit 1). | Gate-derived pin only. Copied from `die_usage "metadata registry refused: $refuse"` (gate:2426; `die_usage` prints `research-gate: %s`, exits 2, gate:390). |

The harness hardcodes the path, the expected rc, and the substring. It never calls the gate's denylist function, so its inputs are independent of gate code. The stderr substring is the only gate-derived element.

Documentation gap: `SKILL.md:76` lists exit 2 as "no path, missing path, directory without .md" and omits refused registries.

## Q2. Revert or mutate the targeted fix: does the control fail for the intended reason?

Method: sandbox copies `mut/M*.sh`, each passing `bash -n` (exit 0). Probe `fx/probe.sh` runs 31 synthetic cases, each in a fresh root, with `env -i`, `LC_ALL=C`, `CHOUSA_STRICT=0`, invoked as `verify-metadata <entry> --root <root> --registry <path>`. A case mismatches when rc or the refusal reason differs from expectation.

| Variant | Edit (sandbox) | `plain-denied-component` | Probe mismatches of 31 | Failure shape |
|---|---|---|---|---|
| base `64eec5d` | none | PASS (rc2, denylist) | 5 | colon-prefixed cases rc0 (reads a denylisted file) |
| landed `dd72641e` | none | PASS | 1 | `ancestor-config-root` (C-C) |
| M1 | registry call sites gate:2394, 2401 back to `is_denylist_path` (revert of the repair) | PASS | 5 | colon cases rc0 |
| M2 | drop `*/.config/*` and `.config/*` (gate:604-605) | FAIL: rc0, normal verdict printed | 12 | denial absent |
| M3 | drop raw-path term at gate:2394 | PASS | 2 | only `.config/../registry.md` (see §4) |
| M4 | add deny-any-dot-directory rule after gate:605 | PASS | 6 | allowed siblings refused |
| M5 | delete gate:611 (full-path term of `is_denylist_fs_path`) | PASS | 5 | colon cases rc0 |
| M6 | disable registry denial (gate:2394, 2401) | FAIL: rc0, normal verdict printed | 19 | denial absent |
| M7 | `if true` at gate:2394 (blanket refusal) | PASS | 13 | allowed siblings refused |

Reading:
- The control fails only when the `.config` denial itself is removed (M2, M6). It then fails for the intended reason: exit 0 with a normal `RESEARCH_GATE` line. It is not a setup error, which would print the usage text and exit 2.
- It does not detect reverting the repair (M1), dropping the raw-path term (M3), an over-broad dot-directory rule (M4), a prefix-only rewrite (M5), or blanket refusal (M7). The colon controls catch M1 and M5; the sibling registry controls (`valid-table`, `ordinary-colon-is-allowed`, composed) catch M7.
- M4 passes the independent suite by inspection, not execution. `grep` for `/\.[a-z]` in `round27-regressions.py` returns only `.config` paths, and every registry, entry, and claim path in the file is either `.config`-denied or dot-free. This holds while TMPDIR is not under a dot-directory.
- Consistent with the lane's recorded L1 receipt `corpus/evidence/round27-regressions-after.json` (`plain-denied-component`: expected 2, actual 2, errors []). Not rerun.

## Q3. Nearby synthetic input where the landed gate is wrong or the control is vacuous

**C-A: benign complete path refused on its citation-style prefix (landed gate versus C3 text).** Reproduced on base and landed:

```
R=$(mktemp -d); mkdir -p "$R/corpus/knowledge" "$R/notes.env:v2" "$R/notes.env"
printf 'source: S001\nverified-at: 2026-01-02 checked synthetic fixture\nrecheck: 90d\n\n## Claim\nsynthetic\n' > "$R/corpus/knowledge/entry.md"
printf '| id | status | used-by |\n|---|---|---|\n| S001 | mined | corpus/knowledge/entry.md |\n' | tee "$R/notes.env:v2/registry.md" > "$R/notes.env/registry.md"
env -i PATH="$PATH" LC_ALL=C CHOUSA_STRICT=0 bash <gate> verify-metadata "$R/corpus/knowledge/entry.md" --root "$R" --registry "$R/notes.env:v2/registry.md"; echo rc=$?
#   -> rc=2, "research-gate: metadata registry refused: denylist", no verdict line (base and landed)
env -i PATH="$PATH" LC_ALL=C CHOUSA_STRICT=0 bash <gate> verify-metadata "$R/corpus/knowledge/entry.md" --root "$R" --registry "$R/notes.env/registry.md"; echo rc=$?
#   -> rc=0, one RESEARCH_GATE line (base and landed)
```

Cause: `is_denylist_fs_path` = full-path term OR `ptr_file_part` term (gate:609-613). `ptr_file_part` cuts at the first colon (gate:573-576), so the prefix `notes.env` matches `*.env`. The C3 text says filesystem-path denylist checks "must inspect complete filesystem paths, not citation-anchor prefixes." The repair adds the full-path term but keeps the prefix term. `legacy-env-anchor-refusal` (regressions.py:170, `synthetic.env:1`) and selftest case `metadata-colon-anchor-denylist-compat` pin the prefix behavior. The C3 text has no legacy exception, so that control's expectation is derived from pre-existing behavior, not from the claim. Round 26 named this class as the failure: `corpus/knowledge/registry-link-r26.md:56-58`, "a filesystem-path class inherited from the pointer-oriented helper." The landed repair closes the bypass direction only. The claims path uses the same helper (gate:1139, 1166); not probed.

**C-B: the control set is blind to over-broad denial (M4).** This is a gap in the control set, not a landed-gate defect; the landed gate refuses only the three declared directories. The plain control has no registry-level negative sibling under a non-`.config` dot-directory. Under M4, `.config-adjacent/`, `.config.d/`, `.hidden/`, `.local/share/`, and `.Config/` are all refused; on landed all are allowed.

**C-C: ancestor sensitivity (control ambiguity).** A fixture root under a `.config` ancestor, with no `.config` component of its own, is refused with the same message on base and landed (`ancestor-config-root`, rc2). The plain control's pass therefore cannot distinguish its fixture component from an ancestor. `tempfile` honors `TMPDIR`; if TMPDIR sits under `.config`, the plain control stays green for an ancestor reason while other registry controls fail.

## 4. Other probes (no counterexample)

Landed behavior, 31 cases (all match expectation except C-C):
- Refused, exit 2 with denylist: `.config/registry.md`; `./.config/…`; bare relative `.config/…`; `x/.config/…`; `.config/a:b.md`; `a:b/.config/registry.md`; `synthetic:fixture/.config/registry.md` (base rc0); `benign:x/credentials/…` (base rc0); `.omp/…`; `.local/state/…`; `credentials/…`; `registry.env`; `synthetic.env:1` (pinned, C-A); symlink to `.config` (file and directory); `x/../.config/…`; `.config/../registry.md` (canonical path benign; refused by the raw term only, an over-refusal).
- Allowed, exit 0: `x:.config/…` (component is `x:.config`); `.config-adjacent/`; `.config.d/`; `config/`; `.hidden/`; `.local/share/`; `.Config/` (case-sensitive filesystem); a regular file named `.config`; `synthetic:ordinary.md`; `a:b/…`; symlink to `a:b/…`; symlink to a plain file.
- `link/../registry.md` with `link -> .config/sub`: refused. `readlink -f` resolves `..` after the symlink.

Probe2 (prefix versus complete path): base 2 mismatches, landed 2 mismatches. `notes.env:v2/registry.md` refused (rc2); `a.env:b/c/d/registry.md` refused (rc2); complete-path sibling `notes.env/registry.md` allowed (rc0).

## Commands and exit codes

- `git -C <lane> archive dd72641e… | tar -x -C <sandbox>` and `… 64eec5d… | tar -x -C <base>`: rc 0. Read-only object access; no lane index or working-tree change.
- `sha256sum tools/research-gate.sh`: `ca39d14d…` (target), `c2c813f1…` (base). `cmp` of the lane's `round27-regressions.py` and `research-gate.sh` against the sandbox copies: identical.
- `bash fx/probe.sh <gate> <label>`: base `SUMMARY total=31 mismatches=5`; landed `SUMMARY total=31 mismatches=1`; mutants M1 through M7 as in the table. Probe wrapper exit 0; per-case gate rc appears in output.
- `bash fx/probe2.sh` base and landed: `mismatches=2` each.
- Minimal reproduction (C-A): base rc 2 then rc 0; landed rc 2 then rc 0.
- Contract-doc grep for the exact stderr string: exit 1 (no hits).

## 5. Limits

- Synthetic fixtures only, under `/tmp/chousa-r27-falsify-FC3PlainDeniedComponent44/fx`. No mounts, namespaces, live processes, network, or host secret files. Case-folding filesystems were not tested: `.Config` would alias `.config` there, while this host is case-sensitive.
- The full selftest and the 58-case regression script were not run (bounds). M4's "passes all 58" is inference from the paths in the script plus individual runs of the same registry shapes.
- Mutants are single-site edits to sandbox copies only. No lane production file, lane git, or index was touched.
- Two probe mistakes were corrected before any reported run: a relative gate path used after `cd`, and a fixture root name containing `credentials/` that confounded one case. Reported results come only from the corrected runs. One batch aborted on a leftover `set -e` in the persistent shell and was re-run with `set +e`; nothing from the aborted batch is used.

## 6. Author-lane advice (not an outside admission)

1. Settle the C3 legacy stance. Either name an exception in the claim ("filesystem paths keep anchor-prefix denial for `*.env:N` names") or make `is_denylist_fs_path` complete-path only and retarget `legacy-env-anchor-refusal` (regressions.py:170) and selftest case `metadata-colon-anchor-denylist-compat`.
2. Give the plain control a discriminating twin: a registry-level allowed sibling (`<root>/notes.env/registry.md` or `<root>/.config-adjacent/registry.md`, expect 0), and an explicit expectation for the `..`-escape spelling `.config/../registry.md`.
3. Assert, before running, that the fixture root contains no denylisted component (or create it under a neutral directory), so the plain control isolates its own fixture component.
4. Add refused registries to the exit-2 row in `SKILL.md:76`.

## Tooling

No installs. Existing tools only: bash, git (archive, read-only), tar, diff, cmp, sha256sum, grep, tee, mktemp, env.

## Axes

Judged on operability, freshness, calibration. This item bears on calibration (C3) only. No axis improvement is claimed. Operability and freshness are not affected by this item.

## Errata (appended after writing; the body above is unchanged)

- §2 table, M3 row: the two mismatches are `dotdot-out-of-config` (the M3-specific effect of dropping the raw term) and `ancestor-config-root` (the pre-existing ancestor case C-C, unaffected by M3). The cell should read "`.config/../registry.md` plus the pre-existing ancestor case", not "only `.config/../registry.md`".
- §2 M4 inspection bullet: the grep also matched one label string, `adjacent-real-ids` (regressions.py:159), which is not a path. The path-level conclusion is unchanged.
