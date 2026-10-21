# FOverlap — cross-axis / sibling-overlap scan (round26 attempt1 falsify)

Seat `ChousaR26R.FOverlap`, leaf, advisory author-lane only (no outside judge,
no SHONEN claim). Judged on: calibration.

## Revisions observed

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); lane `HEAD` was the same
  commit when checked.
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `/tmp/chousa-r26-falsify-FOverlap/{tree,base}` via
  `git archive <rev> | tar -x` (rc0). `git show $R:tools/research-gate.sh | sha256sum`
  = `c2c813f1…abc6` = sandbox file digest = manifest digest (QUALITY15 holds for
  the gate).
- Tools installed/updated: none. `/usr/bin/time` absent (pacman paused); RSS
  measured with a `python3 resource.getrusage(RUSAGE_CHILDREN)` wrapper
  (`/tmp/chousa-r26-falsify-FOverlap/meas.py`).
- Not run (out of my item's scope): selftest, the 8 MiB probe, `round26-measure.sh`,
  lint/format/build.

## Axes

C1 operability (reader allocation), C2 freshness (`--as-of` schedule arithmetic),
C3 calibration (`--registry` relations), plus province scope (PROVINCE.md refusals).

## Province / scope overlap — no absorption found

- `git diff $B $R -- corpus SKILL.md tools | grep '^+' | grep -iE '<kengaku|kumitate|kagi|kasegi|live-target phrases>'`:
  no model-quality, vault/secret, bounty, or orchestration-method text in
  corpus/SKILL/gate. Hits are only `token=` shell variables and the
  `lessons/round-26.md` replacement paragraph.
- Source opening (`.ufo/waves/round-26/build/Src*.md`): plain `curl` GETs and
  reader opens of static public docs/PDFs (Cochrane, Python docs, W3C, RFC, CWE,
  COPE, CiTO). The Crossref Retraction Watch REST API is *quoted from its
  documentation*, not queried (no `api.crossref.org` hit). The only API touches
  are reader-tool side projections (W3C API, Crossref DOI metadata), both
  disclosed as not used for quotes. Inside the "static public documentation"
  allowance; no live-target research.
- Recheck scheduling and registry linking are source-verification metadata,
  which is chousa's own method. They do not implement orchestration.
- Advisory only: `lessons/round-26.md` R26-M4 and "Replacement continuation"
  restate a fleet agent-lifecycle rule ("continue the same claimed attempt and
  same unfinished identities, preserve every dead identity"). It is recorded as
  the lane's own process mistake, citing `PROTOCOL inherited-state rule`. I do
  not count that as absorption. Under QUALITY9, the fleet protocol should stay
  the single home, with the lesson pointing to it rather than restating it.

## Interaction findings (reader × schedule × registry)

### F1 — `--registry` reintroduces the R26-M1 amplification class (C1×C3), on a mode no probe exercises

`metadata_registry_check_source` emits one FINDING per S-id *occurrence*, so
FINDING_LINES grows with header tokens. It also rescans via
`source_scan=${source_scan#*"$source_match"}`, which copies the remaining
string on every token (quadratic). A header-only `source:` of repeated ` S001`
against a registry where S001 is `queued` (cwd sandbox, `--root perf --registry perf/regq.md`):

| source bytes | rc | findings | stdout bytes | peak RSS | elapsed |
|---|---|---|---|---|---|
| control (4-line, no registry) | 0 | 0 | — | 11,352 KiB | 0.01 s |
| 8 KiB | 1 | 1,638 | 193,563 | 11,640 KiB | 0.07 s |
| 16 KiB | 1 | 3,276 | 390,125 | 12,084 KiB | 0.16 s |
| 32 KiB | 1 | 6,553 | 780,088 | 12,068 KiB | 0.42 s |
| 64 KiB | 1 | 13,107 | 1,560,016 | 18,380 KiB | 1.36 s |
| 128 KiB | 1 | 26,214 | 3,145,965 | 30,656 KiB | 4.76 s |
| 32 KiB, same file, no `--registry` | 0 | — | — | 11,884 KiB | 0.02 s |

- At 128 KiB the extra RSS is about 19,300 KiB, roughly 150 bytes per input
  byte. That is above the C1 probe's own amplified threshold (`extra*1024 > 8*bytes`,
  `round26-measure.sh:75`).
- Time ratios ×3.2 and ×3.5 per doubling (near quadratic). Output is about 24×
  the input.
- Distinct ids give the same picture: 32 KiB of distinct `S000nn` produced
  4,681 findings in 0.30 s.
- Extrapolation to the 8 MiB cap, not run: [INFERENCE] about 1.7 M findings,
  about 190 MiB of stdout, and hours of time.

The C1 probe (`round26-measure.sh` c1) runs only plain `verify-metadata`
(lines 60–75), so `C1_AMPLIFIED=0/4` says nothing about `--registry`. That is
not a C1 refutation: C1's frozen shapes and mode are as claimed, and
`--registry` is new, so this is not a base harm. It is a calibration defect
against the round's own QUALITY18 ("A bound names its unit"):

- Usage text `tools/research-gate.sh:322` says "against a bounded SOURCES.md
  table" without naming a unit.
- SKILL.md:494–497 discloses only *time* risks for headerless/continuation
  inputs, not `--registry` per-token memory or output growth.

The registry *load* itself stays flat in memory but is linear in time. With
pipe rows before the header: 32/64/128 KiB took 0.16/0.31/0.60 s at
about 11.6–12.1 MiB RSS ([INFERENCE] about 38 s at 8 MiB).

### F2 — backlink identity depends on caller `--root`, not on the registry (C3 × QUALITY13)

- **T1**, the SKILL.md command (cwd lane root, `--root .`, both flags): rc1,
  57 findings, 0 USEDBY_MISSING; the three r26 entries are CLEAN.
- **T2**, the same command with the fleet-root-by-role layout QUALITY13
  recommends for rechecks (`--root ..`, the lane's parent): rc1 and
  **18 `META_SOURCE_USEDBY_MISSING`**. Every correct mined backlink is
  rejected; for example `recheck-due-r26.md` gets four: S035, S037, S038, S029.
- **T3**, the converse false approval: a different lane `laneB/corpus/knowledge/recheck-due-r26.md`
  citing S037 is CLEAN (rc0) against *lane A's* registry under `--root laneB`.
  The spec correction removed the same-basename false approval
  (`round26-claims.md:137–139`). The same-rooted-path / different-root false
  approval remains, because the registry's own location never anchors
  identity. `registry-link-r26.md` says "same basename elsewhere is not
  identity" but does not name this case.
- **T5** (symlinks): an entry reached through a symlink is identified by its
  canonical target (`readlink -f` of the fd). A `used-by` naming the symlink
  path drifts, and one naming the target is CLEAN. This is undocumented.

These are spec-conformant ("derived relative to `--root`"), so the problem is
not a wrong implementation. It is an unnamed limit, plus a latent conflict with
the QUALITY13 root-by-role convention and the r25 hold battery's fleet root. A
future `--registry` recheck written per QUALITY13 will be red for every
correct entry.

### F3 — composition holds (no defect)

- T4: one entry with overdue + used-by missing + bare verified-at, with both
  flags. Its line keeps `due=2020-01-31 freshness=overdue verdict=drift`, and
  all three warn findings are emitted (rc1, drift=3).
- Reversed flag order gives identical lines.
- `verify-all --as-of` and `verify --registry` both exit 2.
- Refused entries skip registry checks and carry `due=refused`.
- `recheck_first` is now reset per entry, which prevents cross-entry leakage.

This matches the composition clarification.

## Proposed move (one, bounded)

Tokenize the `source:` value in one linear pass and check each *distinct* S-id
once per entry:

```bash
local -A seen=()
local scan=${source_value//[^[:alnum:]_]/ } w
local -a words=()
read -r -a words <<<"$scan"
for w in "${words[@]}"; do
  [[ $w =~ ^S[0-9]{3,}$ && -z ${seen[$w]+x} ]] || continue
  seen[$w]=1
  # ... existing ROW_MISSING / NOT_MINED / USEDBY arms
done
```

The standalone-boundary semantics are unchanged: separators are
non-`[[:alnum:]_]` characters or string ends. Pair this with naming the unit
in usage line 322 ("byte-capped", not "bounded").

- **Improves:** C1/QUALITY18 resource honesty for the new mode, since findings
  are bounded by distinct ids and the scan is O(n). It also improves C3
  calibration, because one defect no longer inflates `findings=`/`drift=`
  thousands of times.
- **Harms:** none expected on the frozen controls (each control cites single
  ids) or on plain output (the code runs only under `--registry`).
- **Risk:** deduplication departs from the literal "yields every token". It
  needs an append-only spec clarification before landing (QUALITY4/11), so it
  is not a silent change.
- **F2:** I propose no code change. The disposition is to name the
  `--root`-relative identity, cross-root false approval, and symlink-target
  identity limits in `registry-link-r26.md` Limits and the SKILL row, and to
  state that `--registry` requires the *lane* root, which is an exception to
  the QUALITY13 fleet-root convention.

## Verification the integrator should run (I did not)

1. Rerun this seat's F1 table with the change (sandbox files under `perf/`):
   expect 1 finding per distinct id, and RSS within 8 bytes/byte of the control
   at 128 KiB.
2. `round26-measure.sh <tree> c3` with `C3_CONTROLS_CAUGHT=5/5` and
   `C3_POSITIVE_CLEAN=1/1` unchanged.
3. `round26-registry-differential.sh` agreement unchanged.
4. Selftest with cases 1–161 identical.

## Commands and exits (all in `/tmp/chousa-r26-falsify-FOverlap`)

- `git archive $R | tar -x -C tree` and the same for `$B`: rc0. The gate
  `sha256` matched `git show`.
- T1: `bash tools/research-gate.sh verify-metadata corpus/knowledge --root . --as-of 2026-10-21 --registry corpus/SOURCES.md` (cwd `tree`): rc1, `entries=32 complete=29 findings=57 drift=3`.
- T2: same with `--root ..`, without `--as-of`: rc1, `findings=75 drift=21` (18 USEDBY_MISSING).
- T2b: each r26 entry with `--root .` is CLEAN (rc0); with `--root ..` it drifts with 1, 4, and 2 USEDBY_MISSING.
- T3: `verify-metadata laneB/corpus/knowledge/recheck-due-r26.md --root laneB --registry tree/corpus/SOURCES.md`: rc0 CLEAN (false approval). With `--root .`: DRIFT (1 USEDBY_MISSING).
- T4/T4b composition: rc1, drift=3, and both flag orders give identical output. T4c: rc2 and rc2.
- T5 symlink: used-by on the symlink path gives DRIFT; on the target path, CLEAN.
- F1 table: `python3 meas.py OUT bash $G verify-metadata perf/k/sNN.md --root perf --registry perf/regq.md`: rc1 for each size. The no-registry runs and the control exit 0.
- `/usr/bin/time …`: rc127, `command not found`. This was a tool absence, not a gate failure; I replaced it with `meas.py`.
