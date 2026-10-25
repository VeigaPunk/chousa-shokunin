# Round 40 — r39 receipt repair and calibration corrections

author: chousa L1 (host-mapped seat: no live L2 dispatch surface; wave prepared for the orchestrator)
date: 2026-10-24
round: 40 (attempt 1)

## Claims and measurements

- **C1 operability (lowest scored axis, 3/10):** the frozen active-r39 manifest's committed receipts verify against their gate, counter, verifier, and expectation bytes. `python3 corpus/evidence/round40/c1-count.py`: control `R39_ACTIVE_RECEIPTS=3/6`, exit 1 → work commit `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9` `R39_ACTIVE_RECEIPTS=6/6`, exit 0. Exact before output: `.ufo/waves/round-40/controls/control-before.txt`; committed after output: `corpus/evidence/round40/measure-after.txt`.
- **C2 calibration:** R2–R5 each have an evidence-backed disposition; R4 is explicitly not reproduced from the current committed r39 spec, plan, and report. `python3 corpus/evidence/round40/c2-count.py`: control `R39_CALIBRATION_DISPOSITIONS=0/4`, exit 1 → work commit `d164f88e` `R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0. Exact outputs are in the same control and after-measurement files.
- C1's three replacement receipts preserve their negative/positive roles: base control 7/8, landed gate 8/8, mutant control 4/8. The original r39 receipt files remain unchanged. The seven-file r39 receipt directory has one superseded draft and six active receipts after the correction.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| reference-drift — four r39 c1 receipts bind the old expectation digest `3abd2dcb…` rather than committed `01cbdc3a…`; three refuse `expect-sha256-mismatch`, and the superseded draft refuses first on its stale counter digest | `.ufo/waves/round-40/controls/r1-stale-before.txt`; the committed r39 verifier's exact refusal text | `corpus/QUALITY.md:455-468`, criterion 55 (expectation bytes are bound and each row is re-derived) | Reissue the three active measurements against the committed expectations file; preserve all originals and exclude the broken draft. The same committed verifier now yields six valid active receipts (`measure-after.txt`). |
| attribution — the r39 lesson says `c1-mutenv-s39003.json` was not committed, but the tracked file is present | `corpus/evidence/round39/receipts/c1-mutenv-s39003.json`; `corpus/lessons/round-39.md:27,54-61`; `corpus/evidence/round40/c2-count.py` | `corpus/QUALITY.md:46-51`, criterion 11 (claim/table/plan agreement), and `:286-291`, criterion 37 (re-derived tallies) | Append R2 erratum; keep the receipt as superseded, do not delete it, and correct the r39 receipt population from six to seven. |
| number-drift — the r39 report states 29 → 31 knowledge files; commit-pinned `.md` counts are 50 → 52 | `.ufo/reports/round-39/chousa.md:132-133`; `corpus/evidence/round39/claims.md:198`; `corpus/evidence/round40/c2-count.py` | `corpus/QUALITY.md:286-291`, criterion 37 | Append the corrected historical command and count; leave the filed r39 report bytes untouched. |
| attribution — the SCORECARD says “two independent runners” though the frozen claims disclose L1 construction runs and the wave was only prepared | `SCORECARD.md:2234`; `corpus/evidence/round39/claims.md:3-6`; `.ufo/waves/round-39/w1-spec.json` | `corpus/QUALITY.md:46-51`, criterion 11 | Append the correction: two seeds, both L1 construction runs; do not call them independent. |

## Spot-check intake

| Routed finding | Round-40 disposition | Evidence |
|---|---|---|
| R1 — stale `expect_sha256` | Three active receipts regenerated against committed bytes; originals preserved | `corpus/evidence/round40/receipts/`; `controls/r1-stale-before.txt`; C1 3/6 → 6/6 |
| R2 — superseded draft was committed | Corrected: the draft is tracked and explicitly excluded from the six active receipts | `corpus/evidence/round39/claims.md:197`; `routed-defect-dispositions.json` |
| R3 — wrong knowledge count | Corrected to 50 → 52 at the named r39 commits | `corpus/evidence/round39/claims.md:198`; `c2-count.py` |
| R4 — role-mix mismatch | Not reproduced: r39 report, spec, and validator plan agree on reviewer 6 / revenger 2 (32 total); the spot-check says reviewer 8 / revenger 0. No contradictory source was rewritten. | `corpus/evidence/round40/routed-defect-dispositions.json`; r39 spec/plan/report and spot-check |
| R5 — “two independent runners” | Corrected to two L1 construction seeds; wave prepared, not dispatched | `SCORECARD.md` “Round 40 — closure corrections to r39”; r39 frozen claims |

## Gate

### Candidate and admitted

The admitted knowledge entry is `corpus/knowledge/receipt-expectation-digests-r40.md`. It distinguishes whole-file digest identity from scenario-row equality and limits the result to byte identity, not authorship or truth. C1's evidence rests on the reopened S059 row; the note cites S059 and the committed verifier at lines 73–79 and 138–139.

### Sources opened and registry changes

- **S059 re-opened** — Python `hashlib` documentation, `https://docs.python.org/3/library/hashlib.html#hash-algorithms`, accessed 2026-10-24; anchor: “Hash algorithms,” paragraph beginning “There is one constructor method named for each type of hash.” Located quote (13 words): “the digest of the concatenation of the data fed to it so far.” It grounds the API's digest input, not the receipt policy or claim truth.
- **S074 opened and rejected as a duplicate row proposal** — same URL and anchor, accessed 2026-10-24; the same 13-word quote was located. S059 already covers the same source and digest-input scope. The rejected row remains with reason and flip condition: admit a new row only if a primary source grounds a distinct receipt-input property not stated in S059.
- S059 `used-by` old → new: `corpus/knowledge/revision-binding-r31.md` → `corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`. S059 status and recheck are unchanged. S074 is a new tier-A rejected row with `used-by=—`; no new source is admitted.
- Bounded search log: one official documentation page identified and screened; S059 re-opened; no source content excluded. The duplicate registration proposal is separately retained as rejected S074.

### Rejected claim

“SHA-256 proves receipt authorship or semantic truth” is rejected: neither S059 nor the verifier establishes those properties; the note labels them as limits. Flip: admit only with a distinct source and a separate authorship or truth-verification mechanism.

### Non-author spot-check

Pending an outside non-author review of at least one admit and one reject. No lane-dispatched seat was counted as independent review; this lesson does not claim that discernment was externally verified.

## Sources census

Round-start command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; exit 0. Exact output:
```text
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Round-end command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; exit 0. Exact output:
```text
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```
S074 is an intentionally retained rejected duplicate-row proposal; the validator passed.

Manual census: rows 73 → 74; tier A 67 → 68, B 1 → 1, C 5 → 5; status mined 50 → 50, queued 19 → 19, rejected 4 → 5. The only added row is the rejected tier-A S074 registration proposal. S059's only change is the logged `used-by` update. Knowledge files: 52 → 53. Counts and committed after outputs: `corpus/evidence/round40/measure-after.txt`; the round-start validation output is the tool result recorded in this lesson.
