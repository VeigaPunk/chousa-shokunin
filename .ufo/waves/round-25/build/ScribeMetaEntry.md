# ScribeMetaEntry — chousa round 25 (recovery 2), claim 1 operability

Scope: draft of `corpus/knowledge/metadata-screen-r25.md` (NOT written to the lane), the SOURCES row it needs, and the observed/simulated facts behind it. Lane head b820e4e; live gate sha256 752e4e38 (no `verify-metadata` arm yet). Spec: `corpus/evidence/round25-claims.md` §Claim 1.

## Draft entry (for L1 to fill and commit)

````markdown
# Metadata screen — `verify-metadata` header check (round 25)

source: S0xx-TO-ASSIGN tools/research-gate.sh (own-work row; the `verify-metadata` arm at :<<L1:line>> and the `META_*` emitters at :<<L1:lines>>; gate sha256 <<L1:landed sha256>>); spec v1 corpus/evidence/round25-claims.md §"Claim 1"; rule screened corpus/QUALITY.md criterion 6 (lines 17–23)
verified-at: <<L1:landing ISO date>> (round 25; mode run on the frozen 28-entry copy and on the live corpus/knowledge directory at the landed gate; drifting entries re-read with `grep -n '^recheck:' corpus/knowledge/*.md`)
recheck: 90d (`bash tools/research-gate.sh verify-metadata corpus/knowledge` from the lane root: expect exit <<L1:rc>> and the warn entries <<L1:named list>>; `bash tools/research-gate.sh --selftest` cases <<L1:first–last new case>> pin the arms)

## Claim

`verify-metadata` checks the three header keys criterion 6 requires (`source:`, `verified-at:`, `recheck:`) on each `corpus/knowledge/` entry. On the frozen 28-entry population it exits <<L1:rc>> with `METADATA_COMPLETE=<<L1:N/28>>`, and its warn drifts are exactly `archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md` (`META_RECHECK_ABSENT` only). Falsified if another entry is warn-drifted, one of the three is missed, or the population exits 0.

## The move

- Header region: lines before the first `## ` outside a fence. A key starts at column 0; its value runs through continuation lines to a blank line, the next key, or the header end. The recheck's first token must be an ISO date, `<N>d`, or `on-release`.
- Severity: warn for absent `source:`, absent or undated `verified-at:`, absent `recheck:`. Info for an unscheduled recheck and for `--root ..` in a recheck value. Info drifts only under `CHOUSA_STRICT=1`.
- Run as `bash tools/research-gate.sh verify-metadata PATH [--root PATH]`. Not part of `verify-all`; the `--pin`/`--drift` baseline is unchanged.
- Rejected: reading `METADATA_COMPLETE` as criterion 6 conformance. It counts key presence (25/28); 21 of 28 recheck values do not begin with a cadence (Evidence row 4).

## Evidence

| # | O = observed, I = inference | command or anchor | output |
|---|---|---|---|
| 1 | O: no mode at base | `grep -n 'verify-all) MODE' tools/research-gate.sh`; `corpus/evidence/round25-measure-before.log` | :5215 is the only verify arm; `verify-metadata rc=2` |
| 2 | O: header census, 28 files | read-only header scan of `corpus/knowledge/*.md` | `source` 28/28, `verified-at` 28/28 (all dated), `recheck` 25/28 |
| 3 | O: absent recheck | same scan | `archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md` |
| 4 | I: first-token rule on the frozen population (scratch `/tmp/chousa-r25-ScribeMetaEntry/spec_sim.py`, not the gate) | spec-v1 reference simulation | 21 unscheduled; `METADATA_COMPLETE=25/28`; the three warns above |
| 5 | O+I: `--root ..` in recheck value | `grep -n '^recheck:.*--root \.\.'` (O: `archived-export-intake.md:4`, `citation-chain-fidelity-r24.md:5`); simulation for the rest | 9 entries |
| 6 | O: empty value on the key line, value on continuation | python check, same scan | `anchor-boundaries-r4.md:20`, `chain-resolution-r3.md:19`, `claim-verification-r2.md:10`, `hardening-r10.md:18`, `reference-integrity-r7.md:36`, `sweeps-rejections-r5.md:23`, `verify-all-r6.md:38` |
| 7 | I: strict view | same simulation | 3/28 clean under `CHOUSA_STRICT=1` (`claim-support-states-r24`, `contextual-source-admission-r24`, `json-delimiter-r24`); 22 carry an info finding |
| 8 | pending: live directory after landing | `bash tools/research-gate.sh verify-metadata corpus/knowledge` | `METADATA_COMPLETE=<<L1:N/29>>` |

## Limits

- Not checked, value truth: `verified-at:` is a leading-date test. It does not confirm the date, that the stated check ran, or that a `source:` anchor is quoted correctly (claim-support-states-r24: states 3–4 stay outside any gate).
- Not checked, `S###` row status: the screen never opens `corpus/SOURCES.md`; it does not confirm the id exists, is `mined`, or that `used-by` names the entry (criterion 6 first clause, criterion 7 tier).
- Not checked, recheck runnability: the command is never executed. The only content test is the `--root ..` substring. A mistyped command passes.
- Not checked, entries outside `knowledge/`: lessons, evidence, `LOG.md`, `SCORECARD.md`, READMEs and subdirectories are not screened. Criteria 9–12 are not machine-checked by this mode.
- Placement: a key after the first `## ` or inside a fence reads as absent.
- Severity: spec v1 keeps unscheduled rechecks at info, so the default verdict passes 21 entries whose recheck has no cadence first. Whether that is warn is a spec-v2 decision, not made here; it would move the named set from 3 to 24 (simulation).
- Not in `verify-all`; `GATE_DRIFT: none` does not cover it.
- The frozen count is 28; the live directory after landing is 29 with this entry.
- Unknown: whether the landed gate reads the seven empty-key-line values as the spec does; a selftest case must pin it.
````

## SOURCES row the L1 must add (opened this round; criterion 6 requires `mined`, used-by this entry)

`| S0xx-TO-ASSIGN | chousa verify-metadata mode — tools/research-gate.sh (own-work) | own-work | A | this gate's metadata-header screen at the landed sha, for knowledge/ entries only | verify-metadata arm and META_* emitters in tools/research-gate.sh (<<L1:lines>>); spec v1 in corpus/evidence/round25-claims.md §Claim 1 | Header keys source, verified-at, recheck are checked for presence, date shape and cadence — not truth | mined | <<L1:landing ISO date>> | on-release | corpus/knowledge/metadata-screen-r25.md |`

(Next free id after S018; the L1 assigns it. S001 is `used-by` json-delimiter-r24 only and must not be re-pointed.)

## Findings for the lead

1. **Operability gap, decision needed.** The pre-registered count `METADATA_COMPLETE=25/28` measures presence. 21 of 28 recheck values start with a command, not a cadence; QUALITY criterion 6 says a command-only recheck "leaves overdue uncomputable". Spec v1 reports these as info, so the default run passes them. Keeping v1 is consistent with the prediction; promoting to warn changes the drift set from 3 to 24. (Evidence rows 2, 4, 7.)
2. **Dispatch.** `verify-metadata` has no arm; the `*)` arm (`research-gate.sh:5237`) rejects a second positional argument with "multiple record paths". The new arm must go beside `verify-all)` (:5215) and set MODE, leaving PATH in RECORD_ARG.
3. **Prediction self-consistent.** The spec-v1 simulation reproduces the pre-registered `25/28` and the three names exactly (inference until the gate runs).
4. **Continuation parsing.** Seven entries put the recheck value on the next line (Evidence row 6). They pass only if the continuation rule is read as specified; add a selftest case.
5. **Live cwd dependence.** Nine recheck values carry `--root ..` (Evidence row 5), the cwd-dependent form the spec flags. The draft entry avoids it.
6. **Draft is in the strict-clean class.** Its recheck is cadence-first (`90d`), has no `--root ..`, and its header has no fence or `##` before the keys.

## Before the entry is committed (L1)

- `grep -nE '<<L1|S0xx-TO-ASSIGN' corpus/knowledge/metadata-screen-r25.md` must print nothing (QUALITY criterion 10).
- `grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH' corpus/knowledge/metadata-screen-r25.md` must print nothing.
- Add the coverage-map row in `corpus/README.md` under the round-25 heading (criterion 9; owned by the claim-2 seat).
- If `LOG.md` claims `Capabilities +1` for the mode, its `SCORECARD.md` row lands in the same landing (criterion 11).
- Re-run the measure: `bash corpus/evidence/round25-measure.sh <tree-root>` in a private clone, not the live lane.

## Tools and files

- Installs/updates: none. Used `python3` (already present) and `grep`.
- Files written: this report only, at the path above. Scratch, outside the lane: `/tmp/chousa-r25-ScribeMetaEntry/spec_sim.py` (sha256 `6a07472de92cece2…`, truncated).
- Lane files read only; no git or jj command run in the lane.

VERDICT: draft entry ready for L1 fill-in with no measured numbers asserted; spec v1 reproduces the pre-registered 25/28 and three names in simulation, but reports 21 command-first rechecks only as info.
