# FRegistryRegistryMultilink — C3 registry multilink refusal (round 26, attempt 1)

Seat: `ChousaR26R.FRegistryRegistryMultilink` (scout, leaf). Author-lane advice only;
not an outside judge and not a SHONEN claim.

## Target and revision

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`). Claim base `ba3333254dd3…` was not run.
- Sandbox: `/tmp/chousa-r26-falsify-FRegistryRegistryMultilink/tree`, made with
  `git archive 0e9784bd… | tar -x` (exit 0).
- Gate digest: `sha256sum tree/tools/research-gate.sh` and
  `git show 0e9784bd…:tools/research-gate.sh | sha256sum` both give
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This matches the
  pinned input (QUALITY 15). Lane `HEAD` at run time was also `0e9784bd…`.
- Script: `/tmp/chousa-r26-falsify-FRegistryRegistryMultilink/run.sh`. Run with
  `bash run.sh`; the script exited 0, and its raw log is `run.log` in the same sandbox.
- Contract under attack: `round26-claims.md:90-93`. FILE is read through the same
  denylist/multilink/NUL-refusing reader, and a refused FILE exits 2.
- Code read: `tools/research-gate.sh:2361-2407` (`metadata_registry_load`), `:2570-2574`
  (registry loaded before the entry loop), and `:6272-6274` (flag parse). `die_usage` is at `:390`.

## Observed results (rc = exit code of `research-gate.sh verify-metadata ENTRY --root W --registry REG`)

The fixture entry is `corpus/knowledge/e.md`, with `source: S001 …`, a dated `verified-at`
plus text, and `recheck: 90d`. The registry has one row, `| S001 | mined | corpus/knowledge/e.md, … |`.

| id | shape | rc | stdout bytes | stderr first line |
|---|---|---|---|---|
| T0 | single-link registry (positive control) | 0 | 382 | — (CLEAN) |
| T1 | registry nlink=2 | 2 | 0 | `research-gate: metadata registry refused: multilink` |
| T2 | same, named via the alias link | 2 | 0 | `… refused: multilink` |
| T3 | nlink=3 | 2 | 0 | `… refused: multilink` |
| T4 | symlink → nlink=2 file | 2 | 0 | `… refused: multilink` |
| T5 | symlink → single-link file (false-positive control) | 0 | 382 | — (CLEAN) |
| T6 | `--registry /dev/stdin` `<` nlink=2 file | 2 | 0 | `… refused: multilink` |
| T6b | `/dev/stdin` `<` single-link file | 0 | 382 | — |
| T7 | hardlinked, alias then removed (nlink back to 1) | 0 | 382 | — (CLEAN) |
| T8 | nlink=2 + NUL byte | 2 | 0 | `… refused: multilink` |
| T8b | NUL, nlink=1 (control) | 2 | 0 | `… refused: nul` |
| T9 | nlink=2 + sparse 8 MiB+1 | 2 | 0 | `… refused: multilink` |
| T9b | sparse 8 MiB+1, nlink=1 (control) | 2 | 0 | `… refused: size` |
| T10 | nlink=2 under `/.config/` | 2 | 0 | `… refused: denylist` |
| T11 | nlink=2 + no id/status/used-by header | 2 | 0 | `… refused: multilink` |
| T11b | no header, nlink=1 (control) | 2 | 0 | `… has no table with id, status, and used-by columns` |
| T12 | nlink=2, directory PATH (2 entries) | 2 | 0 | `… refused: multilink` |
| T12b | directory PATH, single-link (control) | 0 | 458 | — (CLEAN, 2/2) |
| T13 | nlink=2 + `--as-of 2026-10-21` | 2 | 0 | `… refused: multilink` |
| T13b | `--as-of`, single-link (control) | 0 | 415 | — (`due=2027-01-18 freshness=current`) |
| T14 | registry is a hardlink of the entry file | 2 | 0 | `… refused: multilink` |
| T15 | `--registry <nlink2> --registry <single>` | **0** | 382 | — (CLEAN) |
| T15b | `--registry <single> --registry <nlink2>` | 2 | 0 | `… refused: multilink` |
| T16 | entry nlink=2, registry clean (contrast) | 1 | 481 | — (`META_ENTRY_REFUSED … reason=multilink unparsed`, DRIFT) |
| T17 | `verify-claims … --registry <nlink2>` | 2 | 0 | `--registry is only valid with verify-metadata` |
| T18 | bind-mount alias (`unshare -rm`, nlink=1, dev 66305 = source dev 66305) | 0 | — | — (CLEAN) |

In every refusal case, stderr holds the refusal line followed by the full usage text
(T1 was captured in full). Stdout is empty, so no header or per-entry line appears.

## Findings

- **RRM-1 (holds): multilink refusal exits 2 with no output.** The registry is refused for
  nlink 2 and 3, under either link name, through a symlink, and through
  `/dev/stdin`. Because the check runs `stat -L` on the opened fd, it sees the object
  behind any alias. It also fires when the registry is a hardlink of the entry. With
  `--as-of` present and with a directory PATH it still exits 2. It never prints partial
  per-entry output, because the registry loads before the entry loop (`:2570`). On these
  shapes, C3's "refused FILE exits 2" holds for the multilink arm. Confidence: high (observed).
- **RRM-2 (holds): no false positive.** A symlink to a single-link file (T5), `/dev/stdin`
  from a single-link file (T6b), and a file whose extra link was removed (T7) are all
  accepted. The refusal depends on the file's current link count, not on its history or
  on the path's link type. Confidence: high (observed).
- **RRM-3 (holds): refusal order.** The order is denylist, then multilink, then size,
  then NUL, then the table-header check. Multilink beats size (T9), NUL (T8) and a missing
  header (T11). Denylist beats multilink (T10). This matches the entry reader's order
  (`:2584-2612`) and the source chokepoint's rule that identity comes before volume
  (`:1185`). Confidence: high (observed).
- **RRM-4 (calibration gap, not a behavior defect): nothing at the revision tests the
  registry multilink arm.** The only registry refusal case in the selftest is NUL
  (`research-gate.sh:6234-6237`). `round26-registry-differential.sh`,
  `round26-registry-oracle.py` and `corpus/knowledge/registry-link-r26.md` contain no
  `multilink`, `nlink` or `ln` fixture (grep over `corpus/evidence/round26-*` matched only
  `round26-claims.md:37,92`). So the claim's "multilink-refusing" wording for the registry
  rests on code reading plus this seat's T1–T14, not on a registered failing control. QUALITY 17
  asks for a negative fixture and a mutation kill. My assignment did not name a mutation, so
  I ran none: whether a selftest would kill a removed `links != 1` arm at `:2389` is
  unverified. T1 is a ready-made independent negative fixture for that.
- **RRM-5 (advisory, grammar): a repeated `--registry` is last-wins and silently drops the
  earlier one.** In T15 the first `--registry` is multilinked and would be refused, but it
  is discarded and the run exits 0 CLEAN against the second file. The reverse order (T15b)
  exits 2. `--as-of` (`--as-of 2026-13-01 --as-of 2026-10-21`, rc 0) and `--root`
  (`--root /nonexistent --root w`, rc 0) behave the same way, so this is the gate's general
  flag convention, not a hole specific to the registry. The refused file is never read, so
  the refusal itself is not bypassed. Two things make it worth noting:
  - The composition clause says "Neither flag is silently ignored" (`round26-claims.md:153-155`).
    It covers `--as-of` combined with `--registry`, not a repeated `--registry`.
  - The gate already refuses double baseline flags for the same "last-wins would silently
    … the wrong path" reason (`:6303-6316`).

  Severity: low. It does not falsify C1, C2 or C3 as written.
- **RRM-6 (scope observation): the registry reader checks no root containment and no
  device.** A bind alias, which keeps nlink 1, is accepted (T18, CLEAN). The registry reader
  also has no in-root constraint, so any readable non-denylisted path is accepted. That is
  consistent with the spec, which lists only denylist, multilink, size, NUL and read. The
  entry reader likewise has no device check. The claims do not say the registry is
  root-contained or device-bound, so this is no defect against C3. Do not read the multilink
  refusal as an alias-containment guarantee for the registry. In T18 the bind source and
  target shared dev 66305, so this run also did not exercise a cross-device bind.

## Verdict for this seat

The C3 multilink arm was not falsified across 26 fixture rows. All 13 multilinked-registry
shapes exit 2 with empty stdout: T1–T4, T6, T8–T14, plus T15b. Twelve of them
report `multilink`; T10 reports `denylist`, which outranks it. Every control behaves as expected. Two calibration notes remain. RRM-4: the
arm has no registered failing control or mutation kill at `0e9784bd`. RRM-5: a repeated
`--registry` is silently last-wins.

## Unknowns

- No mutation was run, so the selftest's ability to kill the `links != 1` arm is unknown.
- A time-of-check race (a link created after the fd `stat`) was not exercised. A pathname
  `stat` before the fd `stat` alone would not have closed that window.
- Cross-device aliasing was not exercised: T18's bind stayed on the same device.

## Tools

No installs or updates. Used tools already on the host: `bash`, `git`, `stat`, `ln`,
`truncate`, and `unshare -rm` (user and mount namespace, private to the process). No pacman
transactions, no network access, no production edits.
