# Round-31 routed-defect text drafts (not applied)

Draft target paths below are relative to the chousa lane root except R6, which is a fleet-owned report target. No lane or fleet production file was edited.

## R1 — named append-only correction

**Target:** `corpus/lessons/round-31.md:97-98`; append after the current EOF at line 116.

**Before (retained; current lines 97-98):**

```
  CriticClaimsAfter31); fail-open hashing (MutC2Hash) and span-before-stale (MutSelftestNew31) are;
  killed by the counter but not by the selftest; end-line-only binding likewise (MutC1Binding);
```

**After (append this named correction at EOF):**

### R1 correction — fail-open and trim-space detector outcomes

Correction to the detector disposition in `## Falsify wave findings` above: fail-open hashing (`MutC2Hash`) survived both detectors, not just the selftest. Its two mutated counter receipts each report `REVISION_BINDING_MATCH=120/120` and `predicate_holds=true` (`.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.3277349906142620654.receipt.json` and `.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.9879869915017300514.receipt.json`); the mutated selftest passed `228 cases, 0 skipped` (`.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.selftest.run.json`). The omitted third counter-caught, selftest-missed mutant is `MutC2Parse/m2-trim-space`: its two counter receipts each score `118/120` with `predicate_holds=false`, while its selftest passed `228 cases, 0 skipped` (`.ufo/waves/round-31/falsify/MutC2Parse/m2-trim-space.seed1.receipt.json`, `m2-trim-space.seed2.receipt.json`, and `m2-trim-space.json`). Thus the old line 98 label incorrectly calls fail-open counter-killed; trim-space belongs among the counter-killed, selftest-survived cases.

**Evidence anchors:** routed finding `corpus/lessons/round-31-verifier-spotcheck.md:203-208`; original claim `corpus/lessons/round-31.md:95-100`; fail-open classification `.ufo/waves/round-31/falsify/MutC2Hash.md:5`; trim-space classification `.ufo/waves/round-31/falsify/MutC2Parse.md:4`; receipt fields `gate_sha256`, `matched`, `predicate_holds` at the paths above. All four counter receipts are HEAD objects, and the listed receipt/evidence files match HEAD (`git cat-file -e` and `git diff --exit-code HEAD -- ...`, both exit 0; exact commands are in the report).

## R4 — sibling-file corrections

### R4a — mark the old selftest count historical

**Target:** `SKILL.md:88-90`.

**Before:**

> **Round-25 final registry correction.** (Round 31: the rows above now read `PASS (228 cases)`.) The shared `154 cases` tally in the rows above records checkpoint `d8c8cff`; the final shared selftest is `PASS (161 cases, 0 skipped)` (metadata cases 137–161).

**After:**

> **Historical — Round-25 final registry correction.** The Round-25 shared `154 cases` tally belongs to checkpoint `d8c8cff`; the final Round-25 shared selftest was `PASS (161 cases, 0 skipped)` (metadata cases 137–161). Round 31 updated the rows above to `PASS (228 cases)`.

The existing following lines 91-92 (`round25-final-measure.log` / `round25-final-holds.log` supersede the tally without relabelling the historical checkpoint) remain unchanged.

### R4b — identify the final Round31 gate in the disposition

**Target:** `corpus/README.md:960-964`.

**Before:**

> Moved from frontier to held ground, measured on a synthetic fixture: a claim that names the line or line range its span sits on (`"line"`; C1, `LINE_BINDING_MATCH` 50/120 to 120/120) and a claim pinned to the SHA-256 of the exact source bytes it was made against (`"sha256"`; C2, `REVISION_BINDING_MATCH` 50/120 to 120/120), both in `verify-claims` at lane revision `6d0ae19f`; `knowledge/line-binding-r31.md`, `knowledge/revision-binding-r31.md`, sources S057 to S059.

**After:**

> Moved from frontier to held ground, measured on a synthetic fixture: a claim that names the line or line range its span sits on (`"line"`; C1, `LINE_BINDING_MATCH` 50/120 to 120/120) and a claim pinned to the SHA-256 of the exact source bytes it was made against (`"sha256"`; C2, `REVISION_BINDING_MATCH` 50/120 to 120/120), both in `verify-claims` on the final gate from lane revision `23536590` (gate SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`), unchanged in the final evidence/lesson revision `25c5bb70`; `knowledge/line-binding-r31.md`, `knowledge/revision-binding-r31.md`, sources S057 to S059.

### R4c — correct the selftest case range

**Target:** `tools/research-gate.sh:6802`.

**Before:**

> `# ---- r31 C2: revision binding via optional "sha256" (cases 216-224) ----`

**After:**

> `# ---- r31 C2: revision binding via optional "sha256" (cases 216-228) ----`

**Evidence anchors:** routed finding `corpus/lessons/round-31-verifier-spotcheck.md:219-226`; SKILL source `SKILL.md:88-92`; disposition `corpus/README.md:958-968`; gate comment `tools/research-gate.sh:6802`; actual selftest cases 216–228 appear in `.ufo/waves/round-31/falsify/MutC2Parse/m2-trim-space.selftest.stdout:217-229`. `git show --no-patch` and `git rev-parse <revision>:tools/research-gate.sh` confirmed revisions `23536590` and `25c5bb70` carry the same gate tree; `sha256sum tools/research-gate.sh` returned the full digest above.

## R6 — per-run gate identity rule for this round's report

**Target:** fleet-owned `/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/chousa.md`, in the measurements/gate-results section after the table (new paragraph; line number unassigned because this report was not present when checked). **[INFERENCE]** The target name follows the existing `.ufo/reports/round-31/chousa.md` convention; no fleet report was edited.

**Before:** no Round32 Chousa report file/line was present to replace.

**After (append this single paragraph):**

For every counter, selftest, or mutant measurement in this round's report, identify the exact gate used by each run: include the full SHA-256 of `tools/research-gate.sh` and, where established, its lane revision, citing the contemporaneous receipt or commit. Split aggregates whenever gate hashes differ and label any superseded-gate cohort; never report it as part of a final-gate total. For context, Round 31's `RerunSeedSweep31` 30-seed cohort used gate SHA-256 `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c`, superseded by final gate SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (landed at `23536590`, unchanged in evidence/lesson revision `25c5bb70`), so its `120/120` results are not final-gate measurements.

**Evidence anchors:** route `corpus/lessons/round-31-verifier-spotcheck.md:230-232`; original fleet results `/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/chousa.md:16,39-42`; full seed-sweep gate digest `.ufo/waves/round-31/falsify/RerunSeedSweep31.md:12-20`; final revisions and digest recorded in the report's read-only command outputs.
