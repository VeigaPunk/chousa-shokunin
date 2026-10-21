# FC3ReorderClean30 — `reorder-clean`

**Verdict: HOLDS, narrowly.** The declared expectation is independently justified, and the actual shipped control kills the targeted stale-column revert for the intended semantic reason. No new contract-valid landed counterexample was found in the nearby shapes exercised. A broader enforcement-bypass mutant survives this positive control alone; that is an isolation limit, not evidence that the landed repair or the companion negative controls fail.

Author-lane advice only; not an admission or outside judgment. Axes: **operability, freshness, calibration**. This item exercises calibration and command operability; it makes no new freshness or saturation claim.

## Findings, by severity

No actionable defect in the named repair/control was established. The single-positive-control blind spot and broader grammar probe are recorded below as residual limits, not promoted into a new contract.

## 1. Expectation is contract-derived, not gate-derived

- `corpus/evidence/round27-claims.md:15` requires fresh named headers after breaks and matching header/delimiter widths, while preserving existing registry behavior.
- `corpus/evidence/round26-claims.md:90–105,132–141` declares column lookup by header name, mined status, and the corrected exact rooted used-by path rule. `SKILL.md:482` states first qualifying table / first duplicate ID semantics.
- The first line in this fixture is **only an uncompleted header**, not an earlier completed table. After `prose`, the fresh header has four columns with a matching four-cell delimiter. By those names, S001 is mined and used-by names the entry. Clean exit0 therefore follows independently of parser implementation:

```text
| id | status | used-by |
prose
| id | note | status | used-by |
|---|---|---|---|
| S001 | ignored | mined | corpus/knowledge/entry.md |
```

Entry bytes: `source: S001\nverified-at: 2026-01-02 checked synthetic fixture\nrecheck: 90d\n\n## Claim\nsynthetic\n`.

The expectation is the literal `(0, None)` at `corpus/evidence/round27-regressions.py:136`; the table loop at :144–150 checks that exit and one anchored verdict. `observe` at :31–44 does not derive an oracle from gate output. Gate-source helper extraction elsewhere in the file belongs to C1, not this C3 expectation.

## 2. Exact shipped control and targeted mutation

Sandbox: `/tmp/chousa-r27-falsify-ReorderClean30-11` (`S` below). It was extracted with:

```sh
mkdir -p /tmp/chousa-r27-falsify-ReorderClean30-11
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-ReorderClean30-11
sha256sum /tmp/chousa-r27-falsify-ReorderClean30-11/tools/research-gate.sh
```

Setup exited0. Gate SHA-256 was exactly `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`.

`S/run-one-shipped-control.py` extracts only the pinned script's `reorder-clean` tuple, `entry_text`, `run`, `observe`, and original table-loop AST. It executes **one selected control**, not the whole regression script. Pinned regression script SHA-256: `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df`.

Exact command, cwd `S`, for each state:

```sh
timeout 45s python3 run-one-shipped-control.py tools/research-gate.sh
```

The extracted `run` invokes `bash GATE verify-metadata ENTRY --root FIXTURE --registry REGISTRY`, cwd the synthetic fixture, with inherited `CHOUSA_*` removed and `CHOUSA_STRICT=0 LC_ALL=C`. Its subprocess timeout is30s. No `--as-of` is supplied: this is intentionally plain metadata mode.

| Gate state | Gate SHA-256 | Gate exit | Runner exit / control result |
|---|---|---:|---|
| Landed | `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` | 0 | 0; errors `[]`; selected count1 |
| Targeted revert, M-reset | `d65fcdcd25919376063490b08b22829b690b102ba39c9c7a02b9404f62a9f05d` | 1 | 1; `exit 1 != 0`; selected count1 |
| Independent bypass, M-bypass | `8b6af72201cf63b827c64058918b233bbe7b021d49455a8525cc6a80b60a0197` | 0 | 0; errors `[]`; selected count1 |

**M-reset** deletes only the two newly added lines at landed `tools/research-gate.sh:2434–2435`:

```sh
      id_col=-1; status_col=-1; usedby_col=-1
      header_width=0
```

All other repairs, including width checking and the source checker call, remain enabled. This restores the old non-table-line state transition, without running the old gate. Old source was inspected statically only.

Landed key output:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=clean
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
```

M-reset key output:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=entry.md source_id=S001 registry row is not mined
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
```

Both have `METADATA_COMPLETE=1/1` and empty stderr. Thus the kill is **not** a parse, setup, timeout, or refused-path error. Stale indices `(id,status,used-by)=(0,1,2)` make the new row's status `ignored`, precisely the misbinding this control intends to catch. Definition evidence: reset :2431–2436, guarded column assignment :2481–2493, row binding :2452–2460, and status finding :2507–2512. The caller is `verify_metadata` at :2595–2598 and :2718–2720.

The sandbox gate was restored. The final selected-control run reported the original `ca39d14d…` hash and exit0; no production gate was edited.

## 3. Nearby synthetic inputs and isolation counterexample

Additional single-command probes used `S/probe-reorder.py`. Exact command schema, cwd `S`:

```sh
timeout 45s python3 probe-reorder.py --gate tools/research-gate.sh --case CASE
```

Every invocation uses one synthetic fixture beneath `S/synthetic/CASE`, the same scrubbed environment, and one gate subprocess with timeout30s. Rows below give the actual CASE arguments; all landed hashes were the pinned hash.

| CASE | Expected / actual gate exit | Runner exit; key observation |
|---|---|---|
| `reorder-clean` | 0 / 0 | 0; CLEAN, findings0 |
| `id-last-clean`, `usedby-first-clean`, `status-first-clean` | 0 / 0 each | 0 each; further column permutations stay clean |
| `note-queued-clean` | 0 / 0 | 0; queued in irrelevant note does not change mined status |
| `no-break-reordered-clean`, `two-breaks-clean` | 0 / 0 each | 0 each; candidate recovery / repeated reset |
| `named-queued` | 1 / 1 | 0; `META_SOURCE_NOT_MINED` |
| `wrong-usedby` | 1 / 1 | 0; `META_SOURCE_USEDBY_MISSING` |
| `missing-row` | 1 / 1 | 0; `META_SOURCE_ROW_MISSING` |
| `missing-fresh-header`, `short-second-delimiter`, `long-second-delimiter` | 2 / 2 each | 0 each; no-table diagnostic and zero verdict records |

M-reset also produced runner1 on `named-queued`: gate exit1, but **USEDBY_MISSING instead of NOT_MINED**. This reinforces the column-binding explanation rather than relying on exit status alone.

**Isolation counterexample:** M-bypass independently replaces only the source-checker call at landed :2720 with `:`. It leaves header parsing and all metadata checks intact. As the exact shipped-control run above proves, `reorder-clean` still passes when registry relationship enforcement is absent. On the same header/break class, changing only the row to:

```text
| S001 | mined | queued | corpus/knowledge/entry.md |
```

produces a false CLEAN under M-bypass: `named-queued` gate exit0, runner exit1 with `exit 0 != 1` and missing NOT_MINED. Likewise `wrong-usedby` gives gate0 / runner1 and a missing USEDBY finding. **These are mutant counterexamples, not landed failures**: landed correctly rejected both inputs. The named positive control is non-vacuous against M-reset, but cannot alone prove that all registry checking ran. The persisted suite has negative companions, including `reorder-queued` at :137; no suite-wide vacuity is claimed.

One exploratory `escaped-pipe-note` input replaces `ignored` with `ignored \\| note`. Landed returned1 / NOT_MINED and the broader-Markdown hypothesis in the probe returned runner1. This is **not counted as a C3 contract mismatch**: interpreting escaped cell pipes as a richer Markdown grammar goes beyond this named control, and :15 explicitly retains broader grammar limitations. The inherited headerless report also records unresolved grammar distinctions (`.ufo/waves/round-26/falsify/FRegistryHeaderless.md:85–113`). No grammar guarantee was imported from report text.

## Residual risk and verification gaps

- This establishes only the named control's contract provenance and sensitivity to its targeted fix, plus the listed nearby shapes. It does not establish whole C3, all Markdown grammar, general resource safety, or saturation.
- `xd://lsp` documentation/status requests both returned `No such tool`. References/definitions/diagnostics could not be obtained semantically; source citations are text inspection backed by the bounded runtime probes, not grep-as-semantic-proof.
- No full `--selftest`, whole regression script, old-gate behavioral reproduction, network/external target, direct `/proc` or live-process inspection, debugger, or background job was used. No resume path was in scope.
- Only sandbox fixtures/gate mutants and this requested report were written. No lane production source, index, branch, fleet, or sibling files were modified. No tools were installed or updated.

Report: .ufo/waves/round-27/falsify/FC3ReorderClean30.md

Append-only notation correction: the exploratory fixture contains **one literal backslash** before its embedded pipe: `ignored \| note`. The doubled backslash in the preceding prose is an escaped representation, not two fixture bytes.
