# FRegistryExactPath — C3 used-by exact-path grammar attack (round 26, attempt 1)

Seat `ChousaR26R.FRegistryExactPath` (falsify, leaf). Advice from the author lane only; this is not an outside judge or SHONEN verdict.

## Verdict

**Not falsified.** At revision `0e9784bd52eca456b24d0bc40921480a47f91a2b`, the C3 `used-by` matcher behaves as the spec-v1 correction says (`round26-claims.md`, "Spec-v1 correction"). A `used-by` token names an entry only when it equals the entry's path relative to `--root`. Only leading `./` is normalized, after comma-splitting and whitespace trimming. Paths that use `../`, have trailing junk, or have any other non-exact form get `META_SOURCE_USEDBY_MISSING`. In the isolated matrix, all 48 cases agreed with the spec and none mismatched. Every one of the five targeted mutants was killed by its targeted cases, and each kill came from a changed verdict, not from a parse error.

## Revisions and identity (observed)

- Lane `HEAD` at observation: `0e9784bd52eca456b24d0bc40921480a47f91a2b`. This is the same as the target in `corpus/evidence/round26-measured-revision.json`.
- The claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` is an ancestor of the target: `git merge-base --is-ancestor` exited 0.
- `git show 0e9784bd…:tools/research-gate.sh | sha256sum` gave `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This equals the manifest entry, and it equals the `git archive` copy I measured (QUALITY 15).
- Sandbox: `/tmp/chousa-r26-falsify-FRegistryExactPath`, created with `git archive 0e9784bd… | tar -x -C …/tree`. The lane working tree was not graded.

## Code under test (observed)

- `tools/research-gate.sh:2488-2501` (`metadata_registry_check_source`) works in this order:
  1. Split `used-by` on `,`.
  2. Trim `[:space:]` from both ends, under `LC_ALL=C`.
  3. Strip leading `./` repeatedly (`while [[ $token == ./* ]]`).
  4. Accept only when `[[ -n $entry_path && $token == "$entry_path" ]]`. The right-hand side is quoted, so the comparison is literal, not a glob.
- `tools/research-gate.sh:2509-2521` (`metadata_registry_entry_path`) derives the entry path from the fd-canonical entry path (`readlink -f` of `/proc/$$/fd/N`) and the root's `pwd -P`. It returns an empty string when the entry is outside the root. There is a special case for `--root /`.
- `tools/research-gate.sh:2424-2428` trims each table cell when the registry is loaded.

## Commands and exits

| Command (cwd `/tmp/chousa-r26-falsify-FRegistryExactPath`) | Exit | Result |
|---|---|---|
| `bash matrix.sh $PWD/tree/tools/research-gate.sh /tmp/chousa-r26-falsify-FRegistryExactPath/cases` | 0 | `MATRIX cases=48 agree=48 mismatch=0` |
| same matrix against `gate-m1.sh` (deletes the `./` strip loop) | 1 | 9 mismatches, all accept cases flipped to `missing` (a02–a06, a08–a11) |
| same matrix against `gate-m2.sh` (prefix match `"$entry_path"*`) | 1 | 12 mismatches, all trailing-junk cases flipped to `clean` (r05–r16) |
| same matrix against `gate-m3.sh` (basename compare) | 1 | 16 mismatches: `../`, basename, absolute, case, other-dir, inner `//` and `/./`, and others flipped to `clean` |
| same matrix against `gate-m4.sh` (also strips leading `../`) | 1 | 3 mismatches: r01, r02, r33 (`../` forms) flipped to `clean` |
| same matrix against `gate-m5.sh` (unquoted glob, `$entry_path == $token`) | 1 | 3 mismatches: r24, r31 (glob tokens) flipped to `clean`; a12 (literal `[x].md` name) flipped to `missing` |

Every mutant log had `got=other` count 0. So each kill is a `clean`↔`missing` verdict flip, not a parse error or usage exit (QUALITY 17). Across all mutants, the flips were 10 `want=clean got=missing` and 33 `want=missing got=clean`.

Every case invocation was `env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_ROOT CHOUSA_STRICT=0 bash GATE verify-metadata ENTRY --root ROOT --registry REG`. Each entry has `source: S101`, `verified-at: 2026-10-20 checked the claim` and `recheck: 90d`. Each registry is a single `| S101 | mined | <cell> |` row under an `id | status | used-by` header.

The finding text shown for every reject case was exactly:
`FINDING META_SOURCE_USEDBY_MISSING severity=warn surface=metadata obs=entry=x.md source_id=S101 used-by does not name entry`. It came with `RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)` and rc=1. Every accept case gave `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` and rc=0.

## Matrix (target revision; all agree)

Entry `corpus/knowledge/x.md` under the root unless a different entry is stated.

**Accept (rc=0, CLEAN):**
- a01 `corpus/knowledge/x.md`
- a02 `./corpus/knowledge/x.md`
- a03 `././corpus/knowledge/x.md`
- a04 and a05: whitespace-padded and tab-padded `./…`
- a06 `corpus/knowledge/y.md, ./corpus/knowledge/x.md`
- a07: the same list with no space after the comma
- a08 `./corpus/knowledge/a b.md`, for entry `a b.md`
- a09, a10, a11: `./…` with `--root` given as `root/`, as a symlink to the root, and as `root/sub/..`
- a12 `corpus/knowledge/[x].md`, for entry `[x].md`
- a13 `--root /` with the full path minus its leading `/`

**Reject (rc=1, `META_SOURCE_USEDBY_MISSING`), grouped by attack:**
- Parent traversal:
  - r01 `../corpus/knowledge/x.md`
  - r02 `./../…`
  - r03 `corpus/../corpus/knowledge/x.md`
  - r04 `../root/corpus/knowledge/x.md` (a `../` path that resolves back to the real file)
  - r33 `../` under `--root /`
- Trailing junk:
  - r05 ` junk`
  - r06 `)`
  - r07 `;`
  - r08 `/`
  - r09 `.bak`
  - r10 `#L1`
  - r11 `:12`
  - r12 `/.`
  - r13: a second path after a space
  - r14: trailing U+00A0 (not trimmed under the C locale)
  - r15: trailing `\`
  - r16: trailing `"`
- Other non-exact forms:
  - r17 basename `x.md`
  - r18 backtick-wrapped
  - r19 `.//…`
  - r20 `corpus//knowledge/x.md`
  - r21 `corpus/./knowledge/x.md`
  - r22 `/corpus/knowledge/x.md`
  - r23 `Corpus/…` (case differs)
  - r24 `corpus/knowledge/*.md`
  - r25: `;`-separated list
  - r26: the same relative path given for entry `other/knowledge/x.md`
  - r27: empty cell
  - r28 `./`
  - r29 `xcorpus/…`
  - r30 `.corpus/…`
  - r31 `corpus/knowledge/?.md`
  - r32: the absolute filesystem path

## Observations (not defects under the written spec; adjudication for L1)

- **O1. Vertical tab and form feed count as whitespace.** A trailing `\v` (o01) or `\f` (o02) is accepted (rc=0, CLEAN), because `[:space:]` trimming covers VT and FF. The spec only says "trimmed". `[INFERENCE]` This is harmless, because a Markdown table cell would not normally carry VT or FF.
- **O2. A symlinked entry matches its target's path, not its link path.** Entry `corpus/knowledge/x.md` is a symlink to `real.md`:
  - `used-by` = `corpus/knowledge/x.md` gives rc=1 `USEDBY_MISSING obs=entry=x.md`.
  - `used-by` = `corpus/knowledge/real.md` gives rc=0 CLEAN.

  This happens because the path is derived from the fd-canonical object. The finding prints the link basename (`entry=x.md`), while the match uses the target path. That is consistent with the snapshot-bound reader, but the spec's "exact repo-relative entry path" does not say whether the link path or the target path is meant. It falls outside the frozen controls.
- **O3. The path is relative to `--root`, not to the repository.**
  - With `--root <repo>/corpus`, `knowledge/n.md` gives rc=0, and `corpus/knowledge/n.md` gives rc=1.
  - With an entry outside `--root` (`--root <sibling dir>`), both `corpus/knowledge/n.md` and `../root/corpus/knowledge/n.md` give rc=1 `USEDBY_MISSING`.

  The entry path is empty, and an empty path never matches. This follows the stated "derived relative to `--root`" rule. A caller who passes the wrong root sees `USEDBY_MISSING` rather than a usage error.
- **Unrelated negative control (my fixture error, kept).** `--root …/knowledge/sub0` pointed at a directory that does not exist. It exited 2 with `research-gate: root is not a directory: …`. This is the expected usage refusal, not a regression.

## Finding IDs

No new defect. The only finding ID I exercised was `META_SOURCE_USEDBY_MISSING` (warn). It appeared for all 33 reject cases plus the O2/O3 rejects, and for no accept case. I did not observe a `META_SOURCE_ROW_MISSING`, `META_SOURCE_NOT_MINED`, `META_SOURCE_NO_ROW_ID` or `META_VERIFIED_AT_BARE` line in any matrix case.

## Scope and limits

- I did not run the full selftest, build, lint, formatter, the 8 MiB probe or `round26-measure.sh`. I did no source fetch and no population grading. The base `SOURCES.md` `used-by` cells are bare comma-separated paths; I observed rows S001–S003 only. Population false-positive rates belong to the `FRegistryPopulation` seat.
- The mutants live only in the sandbox as `gate-m1.sh` … `gate-m5.sh`. Their sha256 values are `8abc6175…`, `241f3659…`, `2aaf0781…`, `851df275…` and `8cfa3705…`. They are not final-code changes.
- Matrix script: `/tmp/chousa-r26-falsify-FRegistryExactPath/matrix.sh`, sha256 `6269c9001b22d598755fc03224e2f277216c4cdcb14535ac705c281fa117da0b`. Logs are `matrix.log` and `matrix-m{1..5}.log` in the same directory.
- Tools installed or updated: none.
