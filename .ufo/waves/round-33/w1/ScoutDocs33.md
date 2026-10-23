# ScoutDocs33 — C1 docs recon (read-only)

Seat: ScoutDocs33. Question: every text in the lane that states the claims JSONL record format or `json_str` / `json_has_key` semantics, and the sentence C1 would make stale or should extend.

C1 (frozen, `corpus/evidence/round33/claims.md:29-38`, design v1 `3b528b9a`) adds three reader rules the landed gate does not implement: read fields `id/source/span/expect/marker/line/sha256` are **top-level members only**; a read field **duplicated among top-level members** is `CLAIM_RECORD_INVALID`; characters **inside string values are not structure**. Flat records stay as at base (`claims.md:39-40`). Not claimed: `marker_default` rows, escaped key spellings, duplicated unread keys, non-JSON records (`claims.md:80-83`).

Axes used: completeness of stating texts; exact path:line; stale-if-landed vs extend vs leave. No gate or counter was edited. `c1-count.py` was not run.

Census (2026-10-23), lane root, files ≤2 MiB, skip `.git`/`.jj`/NUL. Command: a `python3` walk with needles `Claims file: one JSON object`, `json_str`, `json_has_key`, `one JSON object per`, `one JSON claim`, `Unknown JSON keys`, `marker_default`. Exit 0. `FILES 134`. Tops: `.ufo` 116, `corpus` 15, `SKILL.md` 1, `SCORECARD.md` 1, `tools/research-gate.sh` 1. A second walk (needles also `unknown keys are`, `flat record`, `flat-key`, `flat raw-line`, `nested "line"`) buckets the defect/usage echoes: `.ufo/waves/round-31` 44, `round-32` 31, `round-33` 6, `round-27` 4, `round-26` 2, plus the production files below. Lane-root `README.md`: `grep` for `Claims file:|one JSON object|json_str|verify-claims` → no matches.

Labels: **EXTEND** = still true of flat records, missing C1's three rules. **STALE** = present-tense claim that becomes false once C1 is the landed reader. **LEAVE** = dated snapshot, frozen prior contract, or fixture-local schema (C1 item 4: flat records unchanged). Do not rewrite frozen round-31 claims or counter docstrings.

## Live surfaces C1 should change

### Gate (the reader and the help text)

| path:line | sentence (opened) | after C1 |
|---|---|---|
| `tools/research-gate.sh:49` | `Every other line is one JSON claim {"id","source","span","expect"} with expect supported\|contradicted\|unsupported.` | **EXTEND.** Still the line shape. Add: those fields, plus optional `marker` / `line` / `sha256`, are top-level members only; a nested same-name member changes nothing; a duplicated top-level read field is invalid; bytes inside strings are not keys. |
| `tools/research-gate.sh:51-53` | `the optional JSON string field "line" holds "N" or "N-M" … A present "line" with any other value (empty, non-string, malformed) makes the record invalid.` | **EXTEND** with "top-level". A nested `"line"` must not count as present. |
| `tools/research-gate.sh:63-64` | Comment breaks mid-sentence: `…without it the claim is unproven. A marker on` / `A claim may carry optional "sha256": exactly 64 lowercase hex characters…` | **EXTEND** the sha256 sentence the same way (top-level; duplicate → invalid). The splice `A marker on` / `A claim may carry` is already broken; C1 does not cause it. |
| `tools/research-gate.sh:359-361` | Usage: `Claims file: one JSON object per claim line:` then `{"id":…,"source":…,"span":…,"expect":supported\|contradicted\|unsupported [,"marker":…][,"line":"N"\|"N-M"][,"sha256":…]}` | **EXTEND.** This is what `--help` prints, so every captured help dump copies it. Same three rules. Field grammar in `:362-369` (line pin, sha256 pin) stays. |
| `tools/research-gate.sh:1109` | `json_str() { # LINE KEY -> raw JSON string body on stdout (escapes intact); rc=1 absent` | **EXTEND.** Comment does not say first regex hit on the raw line. After C1, absent means absent as a top-level string member; a nested `"key":"…"` must not match; a second top-level hit is invalid, not first-wins. |
| `tools/research-gate.sh:1121-1125` | `json_has_key() { # LINE KEY -> rc0: KEY appears as a JSON object key (any value type)` / `Same shape as json_str (flat record objects), so a key appearing inside a string value is not seen as a field.` | **STALE** on `flat record objects` (that is the bug). **KEEP** the string-interior clause (C1 item 3). **EXTEND**: top-level only; a nested object/array member is not the field; two top-level occurrences of a read field → invalid. |
| `tools/research-gate.sh:1460-1462` | `json_str reads string values; json_has_key detects a present key of ANY value type, so a present empty or non-string value is distinguishable from an absent key (both are invalid).` | **EXTEND** "present" → "present as a top-level member". Presence-vs-type rule stays (round-31). Same for the sha256 arm `:1471-1472` (`a present non-string value is malformed, never "absent"`). |
| `tools/research-gate.sh:7358-7364` | `Nested-key contract, half the landed gate honours: a key spelling inside a STRING value is not a field … Note the object form {"meta":{"line": "9"}} is NOT honoured by the landed gate: it is read as the record's own key (observed line=9-9). … left unfixed here` | **STALE** once C1 lands (`NOT honoured` / `left unfixed` become false). **KEEP** the string half; case `claims-r2-nested-string` (`:7365-7369`) already pins it. The object form is the case the comment says must wait for the fix. |

Header `:46-48` (`Blank lines and #-comment lines are ignored; a {"marker_default":…} line … is not a claim`) matches C1's "not claimed" on `marker_default`. **LEAVE** that sentence.

### Skill and corpus status (named targets)

| path:line | sentence | after C1 |
|---|---|---|
| `SKILL.md:67` | `with a "sha256" pin (the SHA-256 of the exact source bytes read) on each claim; a changed source reads stale` | **EXTEND** only: the pin is a top-level string member; a nested `"sha256"` is not a pin. The stale outcome stays (C1 item 4). |
| `SKILL.md:73-78` | Gates table: commands, verdict map, `PASS (241 cases)`, line-binding cases 216–219 and revision-pin cases 220–228. | **LEAVE.** Names the command and case ids. Does not state the JSONL shape. (L78 is one long table row.) |
| `SKILL.md:129-131` | `verify-claims <claims-file> reads one JSON claim per line — {"id","source","span","expect"[, "marker"]}; blank lines, # comments and a {"marker_default":…} line are allowed` | **EXTEND.** Already behind round 31 (no `line` / `sha256`). Add those optional top-level fields and the three C1 rules. Blank / `#` / `marker_default` stay. |
| `corpus/README.md:986-988` | `Still open: … nested "line"/"sha256" keys read as the record's own (round-31 carry)` | **STALE** as current frontier once C1 is held. Move off "Still open". Round31 disposition `:962-966` (the `"line"` / `"sha256"` fields themselves) stays held ground. |
| `SCORECARD.md:1849-1850` | Planned round 33: `the nested "line"/"sha256" key defect (unanchored json_str/json_has_key)` | **STALE** as an open candidate once C1 lands. It is the right description of the defect today. |
| `README.md` (lane root) | no claims-JSONL schema and no `json_str` sentence | nothing to extend. |

### Knowledge notes that state the record

| path:line | sentence | after C1 |
|---|---|---|
| `corpus/knowledge/line-binding-r31.md:13` | `A claims JSONL record may carry "line" as a JSON string in either form` | **EXTEND**: top-level member only; a nested `"line"` is not this field; a second top-level `"line"` is invalid, not "any other value" of one field (`:18`). |
| `corpus/knowledge/line-binding-r31.md:38` | `Unknown JSON keys in a claim record are ignored, as before this round.` | **EXTEND, do not delete.** C1 keeps unread keys ignored (`claims.md:80-81` not claimed). It does not say a nested `"line"` under an unknown key is ignored, and it does not say a duplicated read field is invalid. |
| `corpus/knowledge/revision-binding-r31.md:9` | `adds an optional JSON string field, "sha256", to a claim record.` | **EXTEND** "top-level". |
| `corpus/knowledge/revision-binding-r31.md:11` | `A present non-string "sha256" is malformed. Unknown JSON keys are ignored, as before this round.` | Same **EXTEND** as line-binding `:38`. Non-string-is-malformed stays. |
| `corpus/fixtures/claims-r2.README.md:37-46` | `## Schema (one JSON object per line, UTF-8)` and the `id/claim/source/span/expect/marker` table | **LEAVE.** Fixture-local. Those rows are flat; C1 item 4 says flat records verify as at base. Not the gate schema (no `line`/`sha256`). |
| `corpus/fixtures/claims-r9.README.md:37-38` | `Identical to claims-r2.jsonl: one JSON object per line with id, claim, source, span, expect (+ marker only on contradicted entries).` | **LEAVE.** Same reason. |
| `corpus/knowledge/claim-verification-r2.md:40-44` | `Claims file: JSONL. … every other line is one JSON object {"id","source","span","expect"[,"marker"]}` citing gate `:728-768` | **LEAVE** as the frozen round-2 note. Already not the current gate (reader is `:1109-1128`, loop `:1436`). C1 does not uniquely falsify a dated r2 snapshot. Do not retarget those line numbers in place. |
| `corpus/knowledge/claim-verification-r2.md:122` | `A default marker can be set once per file via {"marker_default":…}` | **LEAVE.** `marker_default` is outside C1 (`claims.md:80`). |

`corpus/knowledge/json-delimiter-r24.md` is the verify-all manifest line terminator, not the claims record. Out of scope.

## Frozen or dated — do not amend to absorb C1

These state the format or the flat reader. They stay true as history. The round-33 contract already supersedes them going forward (`corpus/evidence/round33/claims.md:30-38` and `c1-count.py:10-14`).

| path:line | sentence | why leave |
|---|---|---|
| `corpus/evidence/round31/claims.md:74-76` and `:87` | `A claims JSONL record may carry the JSON string field "line" …` / `Unknown JSON keys are ignored, as at base.` | Frozen r31 C1. C1 cites that rule via `c1-count-v3.py:43` (`round33/claims.md:23-24`). |
| `corpus/evidence/round31/claims.md:141-143` and `:151` | same for `"sha256"`; `Unknown JSON keys are ignored, as at base.` | Frozen r31 C2. |
| `corpus/evidence/round31/c1-count-v3.py:16-22` and `:43` | `the gate's presence probe is a flat raw-line regex … so a nested "line" is read as the record's own` / `"line" absent -> unchanged behaviour; unknown JSON keys are ignored, as at base.` | Frozen counter. Control rule: never edit a counter. Describes gate `0bc318b3`, not a living spec. |
| `corpus/evidence/round31/c2-count-v3.py:37-40` | `the landed gate reads a nested "sha256" as the record's own pin (measured: observed=stale on 0bc318b3)` | Same. |
| `corpus/evidence/round32/r31-repairs.md:9` | `Nested-key class not added: the landed gate reads {"meta":{"line":"9"}} as the record's own key` | Repair log of round 32. |
| `corpus/lessons/round-32.md:27-28` | `Carried: nested "line"/"sha256" keys are still read as the record's own (unanchored json_str/json_has_key` | Round-32 lesson. Present tense is the round's close, not a post-C1 status. |
| `corpus/lessons/round-32-verifier-spotcheck.md:166-167` | `D4 (carried). Nested "line"/"sha256" keys are still read as the record's own (unanchored json_str/json_has_key). The lane already carries this into its round-33 plan.` | The route C1 is answering. Stays as the spot-check. |
| `SCORECARD.md:1800-1801` | `Open, not fixed: … nested "line"/"sha256" keys are read as the record's (flat-key parser` | End-of-round-31 status under "Round 31 — post-falsify". Historical. The living open line is `:1849-1850` and `corpus/README.md:987`. |

## Echoes (not authored contract)

116 `.ufo` files and 4 `corpus/evidence` logs/JSON receipts contain the usage sentence or `json_str`. They are wave notes and captured `--help` / selftest stdout (older logs stop at `,"marker":…}`: `corpus/evidence/sweeps-r5-20261016T011543Z-live.log:37`, `integrity-r7-20261016T030552Z-live.log:52`, `pin-r8-20261016T033757Z-pin.log:29`). Updating `usage()` (`:359-361`) does not rewrite them. Not listed line-by-line.

`tools/research-gate.sh:3498-3500` (`a duplicated key's values are concatenated`) is drift-scan tokenization, not the claims reader.

## What a docs pass should touch, and what it must not

Touch, if C1 lands: gate header `:49-68`, usage `:359-369`, `json_str`/`json_has_key` comments `:1109-1125`, caller comment `:1460-1462`, selftest comment `:7358-7364` (and then a case for the object form), `SKILL.md:67` and `:129-131`, `corpus/knowledge/line-binding-r31.md:13` and `:38`, `corpus/knowledge/revision-binding-r31.md:9` and `:11`, `corpus/README.md:986-988`, `SCORECARD.md:1849-1850`.

Do not touch: frozen `corpus/evidence/round31/claims.md`, `c1-count-v3.py`, `c2-count-v3.py`, round-33 `claims.md` / `c1-count.py` (already the contract), fixture READMEs `claims-r2` / `claims-r9`, `claim-verification-r2.md`, round-32 lesson and D4 spot-check, evidence logs.

## Limits

Read-only. No `c1-count.py` run, no install. Line numbers are from reads on 2026-10-23 at tip `3b528b9a` (gate comments match the frozen claim's `:1109-1128` and `:1448-1483`). `.ufo` echo count is the walk above, not a semantic index. LSP was not used; this recon is prose, and the sentences are the bytes opened.
