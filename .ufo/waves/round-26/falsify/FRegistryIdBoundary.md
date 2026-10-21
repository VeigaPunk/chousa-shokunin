# FRegistryIdBoundary — C3 S-id boundary attack (round 26 attempt 1)

Seat `ChousaR26R.FRegistryIdBoundary`, author-lane advice only (no outside judge).

**Verdict: C3 FALSIFIED on the boundary grammar.** The four assigned forms
`xS001 S001x _S001 S001_`, tested on their own, are correctly rejected as ids.
But `metadata_registry_check_source` re-scans the source after a match using a
literal prefix strip. When the last standalone id is at the end of the
`source:` value, a non-standalone token that appears earlier is processed
again. The result is spurious ids such as `S002` taken from `S001S002`, false
drift findings and exit 1, plus duplicate finding lines. The independent oracle
disagrees on 3 of the 20 fixtures by finding-ID set, and the frozen differential
does not cover this shape.

## Revisions and inputs

- Target revision is `0e9784bd52eca456b24d0bc40921480a47f91a2b`, taken from
  `corpus/evidence/round26-measured-revision.json`. Lane HEAD was observed equal
  to it. The claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` is an
  ancestor (`git merge-base --is-ancestor`, rc 0).
- The sandbox was created with `git archive 0e9784bd… | tar -x -C
  /tmp/chousa-r26-falsify-FRegistryIdBoundary/tree`.
- `tools/research-gate.sh` has sha256 `c2c813f1…6abc6` and the oracle
  `round26-registry-oracle.py` has sha256 `6b2d135c…1f78`. Both match the
  revision JSON.
- Tools: GNU bash 5.3.20(1), Python 3.14.8. Nothing was installed or updated.

## Root cause (observed in source)

`tools/research-gate.sh:2474-2504`:

- The regex is `(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)`, and each match
  is consumed with `source_scan=${source_scan#*"$source_match"}`. That removes
  the *shortest* prefix ending in the matched text, not the prefix ending at
  the match's own position.
- When the match ends at `$`, `source_match` is `<boundary>S001` with no
  trailing character. An earlier `<boundary>S001` that is followed by an
  alphanumeric or `_` character is not a regex match, but it is the first
  literal occurrence of that text. The strip stops there.
- The remainder then begins inside the glued token, for example `S002 …` taken
  from `S001S002`. On the next pass `^` treats that position as a boundary, so
  the glued id is extracted.
- If the match ends in a real boundary character, an earlier literal occurrence
  of the matched text would itself have been a leftmost match. So the defect
  needs the last standalone id at end of value. It does not fire when trailing
  text or a continuation line follows (fixtures b7 and b8).

## Fixtures and results

All fixtures are under `/tmp/chousa-r26-falsify-FRegistryIdBoundary/fx`.

The registry `reg.md` has three rows:

- `S001` is `mined`, and its `used-by` lists every fixture path.
- `S002` is `queued`.
- `S1234` is `mined`, used by `b6-long.md`.

There is no `S003` or `S0003` row. Every entry has `verified-at: 2026-10-21
opened the source`, `recheck: 90d`, and `## Claim`.

The gate command was `bash tree/tools/research-gate.sh verify-metadata ENTRY
--root fx --registry fx/reg.md`. The oracle was `python3 round26-registry-oracle.py
ENTRY --root fx --registry fx/reg.md`, which exited 0 on all 20 fixtures. The raw
log is `run1.log` in the sandbox.

| fixture | `source:` value | gate rc | gate findings (id:source_id) | oracle | result |
|---|---|---|---|---|---|
| a1-x | `xS001` | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a2-sx | `S001x` | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a3-us | `_S001` | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a4-su | `S001_` | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a5-all | `xS001 S001x _S001 S001_` | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a6-allq | same four forms with queued S002 | 0 | NO_ROW_ID | NO_ROW_ID | agree |
| a7-allplus | `xS002 S002x _S002 S002_ S001` | 0 | none (clean) | none | agree |
| a8-digit | `S0010 9S001 S001S` | 1 | ROW_MISSING:S0010 | ROW_MISSING | agree (S0010 is valid) |
| **b1-glue-q** | `see S001S002 and S001` | **1** | **NOT_MINED:S002** | none | **DISAGREE: false positive** |
| **b2-glue-miss** | `see S001S003 and S001` | **1** | **ROW_MISSING:S003** | none | **DISAGREE: false positive** |
| **b5-cont** | `x S001S003` + continuation line `  S001` | **1** | **ROW_MISSING:S003** | none | **DISAGREE: false positive** |
| **b6-long** | `x S1234S0003 y S1234` | **1** | **ROW_MISSING:S0003** | none | **DISAGREE: false positive** |
| b3-dup-sx | `ref S002x and S002` | 1 | NOT_MINED:S002 ×**2** | NOT_MINED | set agrees; duplicate emission |
| b11-dup-us | `ref S002_ and S002` | 1 | NOT_MINED:S002 ×**2** | NOT_MINED | set agrees; duplicate emission |
| b12-dup-xid | `ref S002S002 and S002` | 1 | NOT_MINED:S002 ×**3** | NOT_MINED | set agrees; triple emission |
| b4-single-q | `S002` (control) | 1 | NOT_MINED:S002 ×1 | NOT_MINED | agree |
| b7-trailsp | `see S001S003 and S001 ` (trailing space) | 0 | none | none | agree; trigger needs end-of-value |
| b8-nextline | `see S001S003 and S001` + continuation line `  more` | 0 | none | none | agree |
| b9-paren | `(S001S003) S001` | 0 | none | none | agree; earlier text is `(S001`, not ` S001` |
| b10-under | `see S001_S003 and S001` | 0 | none | none | agree; remainder `_S003` is not re-anchored |

The b1 case gives **4 false-positive entries out of 4 trigger fixtures** (b1,
b2, b5, b6). Each wrongly marks a clean, correctly cited entry as drift and
exits 1. The differential compares sets, so it would count these as 4
disagreements.

The duplicate cases show the non-standalone `S002x`, `S002_` and `S002S002` being
re-read as an `S002` occurrence. Exactly one standalone token gives 2 or 3
identical finding lines, against 1 for the control. Exit code and finding set
are unchanged, so the oracle and differential cannot see this; only `findings=`
counts inflate.

## Root-cause confirmation (isolated sandbox mutation; not a production patch)

`mut/research-gate.sh` (sha256 `440011bf…228d`) replaces the regex/strip loop
with tokenisation:

- every byte outside `[[:alnum:]_]` (C locale) is turned into a space;
- each word is kept only if it matches `^S[0-9]{3,}$`;
- the `source_scan=${source_scan#*…}` line is deleted.

The diff is 4 added lines and 4 removed lines, at 2477-2480 and 2503.

On the same 20 fixtures the mutation agrees with the oracle finding sets on
**20/20**. It emits exactly one line per token in b3, b11 and b12, and it does
not change the a* outcomes. The raw log is `run-mut.log`. This shows the
strip line is the cause. It is not offered as the landing fix, and I did not
run the selftest or differential against the mutation.

## Coverage and population exposure

- The frozen differential fixture `adv-noid.md`
  (`round26-registry-differential.sh:143`) is the four forms with **no**
  trailing valid id, which is fixture a5 and agrees. The selftest case
  `meta-reg-noid` (`research-gate.sh:6198`, `xS001 S001a`) is the same kind of
  shape. Neither reaches the trigger, so `C3_CONTROLS_CAUGHT=5/5` and the
  differential's agreement do not exclude this defect.
- I searched the target tree with `grep -nE
  '[A-Za-z0-9_]S[0-9]{3,}|S[0-9]{3,}[A-Za-z0-9_]' corpus/knowledge/*.md
  corpus/SOURCES.md` and found no matches. The frozen 29-entry population and
  the base registry contain no glued S-id, so `C3_POP_R24PLUS_CLEAN` and the
  frozen hashes are not affected by this defect. **[INFERENCE]** This is from
  the static grep, not from re-running `c3`.

## Calibration consequence

C3's spec v1 correction requires ids to have "standalone ASCII
alphanumeric/underscore boundaries". The landed scanner breaks that whenever a
glued token comes before an end-of-value occurrence of its prefix id. The C3
screen is not calibrated on this input class: it produces false
`META_SOURCE_ROW_MISSING` and `META_SOURCE_NOT_MINED` drift findings and
inflated finding counts. Adding fixtures b1 and b2 (and b3 for counts) to the
differential's adversarial suite would turn this into a failing independent
control, as QUALITY 17 requires.

## Commands not run

I did not run the full selftest, build, lint, formatter, the 8 MiB probe,
`round26-measure.sh`, or `round26-registry-differential.sh`. I did not fetch
any source. No production files were edited; this report is the only write to
the lane.
