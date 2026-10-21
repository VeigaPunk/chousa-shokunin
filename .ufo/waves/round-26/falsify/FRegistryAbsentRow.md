# FRegistryAbsentRow — C3 standalone-S999 / META_SOURCE_ROW_MISSING attack

Seat `ChousaR26R.FRegistryAbsentRow`. This is author-lane advice only, not an outside judge or SHONEN claim. Axis judged: calibration.

## Verdict

**C3 falsified on one grammar point (R26-FRA-1).** Single-standalone `S999` detection works (control 1/1). However, the S-id scanner reports a non-standalone token as a source id when the entry's last true id ends the `source:` value. The result is a false `META_SOURCE_ROW_MISSING`, with exit code 1 (drift), on an entry that is clean under the registered spec and under the lane's own oracle. The lane differential compares only sets of finding codes per entry, so it cannot see the extra spurious id in other shapes either. The frozen 29-entry population is not exposed (0 glued tokens), so registered counts are unaffected; this is a defect in the checker's grammar, not a change to the population figure.

## Identity

- Target revision `0e9784bd52eca456b24d0bc40921480a47f91a2b`, tree `3fccf03d58d5af72eb28ef255a1212c6e76ba4b7`. The lane HEAD observed at 12:59Z is the same commit. Claim base is `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (not run).
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryAbsentRow/tree`, exit 0.
- Hashes of the archived files match `round26-measured-revision.json`:
  - `tools/research-gate.sh` c2c813f1…abc6
  - `round26-registry-oracle.py` 6b2d135c…1d78
  - `round26-registry-differential.sh` 852a7648…76e9
  - `SOURCES.md` 8308e629…aa9
  - `QUALITY.md` 2428baaf…6dce6
  - `round26-claims.md` dcbe2b5f…7c5e
- Runtime: GNU bash 5.3.20(1), Python 3.14.8. No tools were installed or updated.

## Command

The fixtures are under `/tmp/chousa-r26-falsify-FRegistryAbsentRow/fx`. Each entry was run with:

```
env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=$F \
  bash tree/tools/research-gate.sh verify-metadata $F/corpus/knowledge/<e>.md --root $F --registry $F/reg.md
```

The oracle was run as `python3 tree/corpus/evidence/round26-registry-oracle.py $F/corpus/knowledge --root $F --registry $F/reg.md`, exit 0.

The fixture registry `reg.md` (sha256 a32155de…99d3) has three rows:

| id | status | used-by |
|---|---|---|
| `S001` | `mined` | every fixture |
| `S123` | `mined` | `corpus/knowledge/nobody.md` |
| `S0999` | `mined` | every fixture |

`S999` is absent from the registry.

## Results (gate output vs oracle code set)

Every fixture has `verified-at: 2026-10-20 checked` and `recheck: 90d`.

| fixture | `source:` value | gate rc / findings | oracle | status |
|---|---|---|---|---|
| a01 | `S999` | 1 / ROW_MISSING S999 | ROW_MISSING | control caught |
| a02 | `S001` | 0 / none | none | positive clean |
| **a03** | `ref S001S999 S001` | **1 / ROW_MISSING S999** | **none** | **false positive** |
| **a12** | `ref S001S999` + continuation `  S001` | **1 / ROW_MISSING S999** | **none** | **false positive** |
| a04 | `x S999S123 S999` | 1 / ROW_MISSING S999, **USEDBY_MISSING S123**, ROW_MISSING S999 | ROW_MISSING | spurious id S123 (extra code) |
| a11 | `ref S001S999 S001 ` (trailing space) | 0 / none | none | negative control: trigger needs end-of-value anchor |
| a06 | `S999 S999` | 1 / ROW_MISSING S999 ×2 (findings=2) | ROW_MISSING | duplicate count, see notes |
| a05 | `S999` then a second `source: S001` | 0 / none | none | last key wins (matches spec and oracle), see notes |
| a07 | `see below` + continuation `  S999` | 1 / ROW_MISSING | ROW_MISSING | agree |
| a08 | `S999é` (UTF-8 suffix) | 1 / ROW_MISSING | ROW_MISSING | agree: ASCII boundary |
| a09 | `source:S999` (no space after colon) | 1 / ROW_MISSING | ROW_MISSING | agree |
| a10 | tab + `S999` + tab, CRLF lines | 1 / ROW_MISSING | ROW_MISSING | agree |
| a13 | `S0999` (`S0999` row mined) | 0 / none | none | agree: `S0999` and `S999` are distinct ids |
| a14 | `none`; `S999` only in the body after `## ` | 0 / NO_ROW_ID info | NO_ROW_ID | agree |
| a15 | `s999` | 0 / NO_ROW_ID info | NO_ROW_ID | agree |
| a16 | `x` + fenced `S999` continuation | 1 / ROW_MISSING | ROW_MISSING | agree |

Two-table registry (`reg-2tables.md`, 02e35b94…d923), with `S999` only in the second table: the gate gives a01 rc 1 ROW_MISSING S999, and the oracle gives ROW_MISSING. Both use the first qualifying table. This is consistent with the oracle, but the spec in `round26-claims.md:90-96` does not say so. The real `SOURCES.md` has one table (lines 9–49), so there is no exposure.

The frozen corpus with the base `SOURCES.md` was run as `verify-metadata corpus/knowledge --root . --registry corpus/SOURCES.md`. It gave rc 1 from other findings (not adjudicated here) and 0 `META_SOURCE_ROW_MISSING`. Running `grep -E 'S[0-9]{3,}S[0-9]{3,}'` over `corpus/knowledge/*.md` gave 0 matches.

## R26-FRA-1 — consumed-prefix rescan invents ids (calibration defect)

`tools/research-gate.sh:2476-2504`, function `metadata_registry_check_source`:

```
while [[ $source_scan =~ (^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$) ]]; do
  ...
  source_scan=${source_scan#*"$source_match"}
```

The parameter expansion removes the shortest prefix ending at the *first textual occurrence* of the matched string, not at the match's position. Take the shape where the leftmost true match is end-anchored (` S001` + `$`) and an earlier glued `S001S999` contains the same substring ` S001`. The scanner then cuts inside the glued token. The leftover `S999 …` begins at `^`, so `S999` matches as if it were standalone.

This breaks the spec-v1 correction (`round26-claims.md:133-135`), which requires "standalone ASCII alphanumeric/underscore boundaries". The oracle's lookbehind `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` gets this right.

Effects:
- A clean entry becomes drift, exit 1 (a03, a12).
- A non-id becomes a checked id, which can emit a different code (a04: `USEDBY_MISSING S123`).
- The real id is reported twice (a04).

**Detection gap:** `round26-registry-differential.sh:213-255` builds `actual[name]` as a set of finding codes. Spurious ids that share a code with a true finding (a04's second ROW_MISSING) are invisible, and `source_id` is never compared. Its adversarial no-id fixture (`adv-noid.md`, line 143) contains no glued-then-end shape.

Correctness condition (not a patch): advance the scan from the match offset, for example by stripping `${source_scan:0:pos+len}`, or by consuming only through the id and keeping the trailing boundary.

## Notes (not falsifications)

- **Repeated ids are reported per occurrence (a06).** `S999 S999` gives findings=2 and drift=2, while the oracle uses a set. The spec says "yields every … token" and does not say whether to deduplicate. This only changes drift counts, not the verdict, but finding totals are not one per id.
- **A duplicate `source:` key hides an earlier missing id (a05).** This is last-key-wins, the same as the other keys and the oracle, so it conforms to the spec. It is still a calibration blind spot: an entry can carry an unchecked `S999` with exit 0.
- **Expected negative controls held:** a11, a13, a14, a15. They are not regressions.

## Not run

No selftest, build, lint, `round26-measure.sh`, differential script, or 8 MiB probe was run. No source fetch was made. No production file was edited apart from this report.
