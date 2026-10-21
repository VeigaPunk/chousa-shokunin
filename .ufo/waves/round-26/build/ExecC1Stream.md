# Round 26 — ExecC1Stream

## Implementation
- Private clone `/tmp/chousa-r26-ExecC1Stream-3`; observed HEAD/base: `f361d12e44687841e30ec35710ddb366c6f795e0`. The counting probe reads its frozen population from `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (probe output).
- `tools/research-gate.sh:2310,2383-2429`: removed the snapshot-to-`lines` array pass and run the original CR-strip, fence, heading, key, and continuation logic directly in a `while read` loop; stop remains at first unfenced `## `. Snapshot/refusal path unchanged.
- `tools/research-gate.sh:5663-5693`: appended cases 162–164 after the prior final case 161: final header line without newline, fenced `## ` before header keys, and pre-/post-heading duplicate recheck (pins last-key-wins and ignores keys after heading).
- Clone files written: `tools/research-gate.sh` SHA-256 `99771ea29565accbfd4d4f2090de0f6b0223933743f5f8d39988178ef85202fa`; patch `/tmp/chousa-r26-ExecC1Stream-3/r26-ExecC1Stream-3.patch` SHA-256 `0c82e9acdad78d7f2c818d7e4df6bc72b1336d5a89c2f36c57d3aecf6ad8aba9`.

## C1 evidence
Command: `bash /tmp/chousa-r26-ExecC1Stream-3/corpus/evidence/round26-measure.sh /tmp/chousa-r26-ExecC1Stream-3 c1`
```
ctl rc=0 maxrss_kb=11880 elapsed_s=0.0
s1-newlines bytes=8388000 rc=1 maxrss_kb=54888 extra_kb=43008 elapsed_s=88.2 bounded
s2-header-body bytes=8388000 rc=0 maxrss_kb=54880 extra_kb=43000 elapsed_s=0.1 bounded
s3-crlf bytes=8388000 rc=1 maxrss_kb=54676 extra_kb=42796 elapsed_s=44.4 bounded
s4-header-noheading bytes=8388000 rc=0 maxrss_kb=54888 extra_kb=43008 elapsed_s=61.1 bounded
C1_AMPLIFIED=0/4
C1_FROZEN_RC=1 C1_FROZEN_SHA=3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37
METADATA_COMPLETE=26/29
RESEARCH_GATE: DRIFT (entries=29 complete=26 findings=33 drift=3)
```
- Before comparison: `corpus/evidence/round26-measure-before.log:3-10` records control RSS 11,644 KiB, `C1_AMPLIFIED=4/4` (s1 2,238,736 KiB / 90.6 s; s2 1,125,328 / 11.7 s; s3 1,125,008 / 45.7 s; s4 1,126,028 / 63.6 s), and frozen RC 1 / SHA `3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37`. The frozen output SHA is unchanged.

## Holds evidence
Command: `bash /tmp/chousa-r26-ExecC1Stream-3/corpus/evidence/round26-measure.sh /tmp/chousa-r26-ExecC1Stream-3 holds`
```
RESEARCH_GATE_SELFTEST: PASS (164 cases, 0 skipped)
LEGACY_CASES_SHA=5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb (first 161 ok-case lines)
GATE_DRIFT: none
drift rc=0
VERDICT_BEARING_EXPORTS=3/3
```
Baseline `round26-measure-before.log:65-70` has PASS (161 cases), the identical legacy SHA, no drift, and 3/3 exports.

## Risks / blockers
- The already byte-capped `content` snapshot remains; the parser no longer creates a per-line array. No other blocker observed. LSP was unavailable in the mounted tool interface.
- Installs/updates: none.

VERDICT: C1 operability result matches the registered prediction (0/4 amplified); frozen output, cases 1–161, drift, and verdict-bearing exports hold.