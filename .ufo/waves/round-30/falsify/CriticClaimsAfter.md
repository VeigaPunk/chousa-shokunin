VERDICT: falsified — C1 holds on 14/14 fresh-seed runs; C2's frozen predicate prints 26/27 on fresh seeds of the landed tool (3 of 44 tip runs), so C2 is not a stable claim.

CriticClaimsAfter — attack on the landed C1/C2, round 30 wave 2.

Bounds observed: no network; counters run under the frozen hashes (c1 `5b312d84…9d6e6`, c2 `0a59e373…f88f`, harness `e2be0dd1…50d4`), tool `47a657e7…1201`. My receipts: this directory (`c1-run{1,2,3}.json`, `c2-run{1..9}.json`).

## 1. Was every predicate frozen before any candidate was scored? — yes

- Counters and harness were last changed in `abfdf932` (commit time `2026-10-23T00:07:40-03:00` = 03:07:40Z). `claims.md` was last changed in `60d51f79` (00:13:52-03:00 = 03:13:52Z); `git diff --numstat 60d51f79^ 60d51f79` shows only `claims.md` 5+/3- (wording: "every quote of the 100 document items"), no counter or harness file. The working tree at the tip hashes to the frozen values (`sha256sum corpus/evidence/round30/{c1-count,c2-count,qr_harness}.py`).
- The build spec and the v4 control receipts are `a0bc50b7` = 03:14:29Z.
- First round-30 candidate score: `build/ExecC1Head/c1-run1.json` 106/106 at 03:22:04Z (tool `69682cee…`). ExecC2Fetch 27/27 at 03:26:16Z; ExecC2FetchB at 03:25:09Z; ExecC1HeadB at 03:26:28Z. The earliest build receipt of any kind is `CriticD3Classes` 03:16:26Z (round-29 mutants, not the candidate). Every candidate receipt carries the frozen counter and harness hashes.
- Recorded-order nuance, not a violation: `before-c1-v4-run{1,2}` (03:07:08/09Z) and `before-c2-v4-run{1,2}` (03:06:30/51Z) predate the v4 freeze commit by 30-70 s and already carry the frozen hashes. The L1 wrote the counter, scored the do-nothing, then committed the freeze; no candidate existed at that point.
- v4 control ceilings (verified from the receipts): C1 max 86/106 (`skip-nothing`), C2 max 18/27 (`wall-cutoff-38`), tool absent 0/106 and 0/27, all `predicate_holds=false`. No control meets either target.

## 2. Is `bd43bd53` a rule change or a candidate fix? — a candidate fix

- `git diff --stat 33dd643f bd43bd53`: `tools/quote-reopen.py` +7 lines plus the revA receipts; no counter, harness or `claims.md` change. Tool SHA map: `33dd643f`→`0150361a…`, `bd43bd53`→`84b851aa…`, `49b2aa30`→`47a657e7…` (matches every receipt).
- The target stayed 27/27 and the counter bytes did not move, so it is not a re-scale. The added check is generic: end of stream at or after the tool's own deadline → `UNREACHABLE`; end of stream with `resp.length` still outstanding → `body truncated`. It is not keyed on a harness artifact.
- The 24/27 miss on `33dd643f` is disclosed (`measure/revA-c2-run1.json`; lessons row "Two passing runs…").

## 3. C2 — falsified as a stable predicate (main finding)

Three fresh-seed receipts on the landed tool (`47a657…`), the frozen counter (`0a59e373…`) and harness (`e2be0dd1…`) print 26/27, exit 1:

| receipt | seed | utc |
|---|---|---|
| `falsify/RerunC2B/run2.json` | 821943121835704974 | 03:35:12Z |
| `falsify/RerunC2B/run4.json` | 909001692554153263 | 03:35:24Z |
| `falsify/RerunC2B/extra16.json` | 3816068956073394450 | 03:39:43Z |

All three misses are `slow-ok` items: `got UNREACHABLE`, label `VERBATIM` (two) / `ABSENT` (one), `wall = deadline + 0.06-0.07 s` (2.126/2.06; 3.828/3.76; 2.662/2.6), `bound_ok true`, `unvalidated_dests []`, `killed false`. Snapshot 03:43:52Z: 41/44 tip runs pass (RerunC2A 5, RerunC2C 5, `measure/after-c2` 2, my 9 all 27/27; RerunC2B 17/20).

Cause [INFERENCE from code]: the harness delivers a `slow-ok` body over `DEADLINE - 1.0 s` from the head (`qr_harness.py` slow-ok branch; `param=(deadline - 1.0)` at `c2-count.py:139`) while the tool's deadline starts before connect. Under the wave's concurrent counter load the 1.0 s margin is consumed, and the tool refuses at its own deadline, which is what contract v2 item 2 requires. The miss is counter-side margin, not a tool-contract breach; but the frozen kill rule says any other value on the measured lane revision is a miss, and the claim's predicate is the command, not the two receipts.

Impacted axis: operability. Smallest safe correction: report the misses as a miss; do not re-scale or re-design the counter after data (§9); C2 is not reproducible at the tip. A future round may widen the slow-ok margin or floor the deadline as a new pre-data design.

## 4. C1 — holds

- 14/14 fresh-seed tip runs print 106/106, exit 0: my `c1-run{1,2,3}.json`, `falsify/RerunC1{A,B,C}` (9), `measure/after-c1-run{1,2}`.
- D3 mutants re-applied to the landed tool: `MutSkipScript` 66, `MutCasefold` 86, `MutOrder` 104, restored 106 — all below 106 (receipts under `falsify/MutR29*`).
- Provenance nit: the C1 predicate section of `claims.md` cites `before-c1-run{1,2}.json`, which carry the v1 counter `7206c355…` and v1 harness `d0c291bf…`; the frozen-counter receipts are `before-c1-v4-run{1,2}.json` (78/106 under `5b312d84…`/`e2be0dd1…`). Same value, stale pointer. Correction: cite the v4 receipts in the round report; do not edit the frozen rule.

## 5. Axis naming and D-list scope (§9)

- C1 conforms: it names the surface (one new edge class — pages that omit `</head>`) and gives the command that shows it unmoved (78/106).
- C2 partly conforms: "Axis by surface: operability, the lowest scored axis (SCORECARD.md line 7, score 3)" names the axis by the score and calls a code layer a surface. The round states 3→3, so there is no score inflation, but this is the §9 slip of naming by the number. Smallest correction: name the surface — the fetch layer's two stated bounds held against drip and rebinding senders — and drop the score clause.
- Scope: `claims.md:74` restricts the round to the round-29 routed list D1-D7; C1 is D7/D3, C2 is D7 T1/T4; there is no third claim; D1/D2/D4/D5/D6 are repairs. `SCORECARD.md:1677` carries "D-list only". The fleet anti-loop section (`.scratch/goal-20261022-hyaku-12h.md:180-200`) has no D-list clause, so the binding scope is `claims.md` plus `SCORECARD.md`, and the round stays inside it.

## 6. `corpus/lessons/round-30.md` — overclaims and defects

1. **C2 after-state is an overclaim.** "C2 12/27 → 27/27" (lessons:15-16; `LOG.md:1216-1218`; `SCORECARD.md` Round 30 "measured: met (author view)") is not reproducible: 3/44 fresh-seed tip runs print 26/27. The same file's Mistakes row names this exact class ("two passing runs of a randomized counter were read as coverage"). Correction: report the failing seeds and mark C2 not reproducible; the two after receipts are two runs, not a stable result.
2. **Gate sentence was prospective at commit time.** "The falsify wave re-opens each one, with the landed tool as well as by hand" was committed at 03:33:04Z, before any falsify source receipt existed (earliest `AttackRowS05*.md` 03:35:51Z). All seven now exist (S055 at 03:37:53Z), and S050/S051 used the landed tool, so it is now true; date it or move it to the wave-2 report.
3. **S050's "superseded" premise is not on the opened page.** The Gate row and `SOURCES.md` teaches cell say the dated Recommendation is "superseded by the WHATWG HTML Standard"; the page does not state it (`falsify/AttackRowS050.md` finding). Mark it `[INFERENCE]`.
4. **Wrong pointer for the redirect-follow disclosure.** "`ReviewContractV2.md` finding 7" is "Item 2's wording 'stops' has no tolerance"; the redirect disclosure is finding 13 and the network-disclosure block (`ReviewContractV2.md:185-192, 236-242`). Fix the pointer.

Verified true in the same file: the D2 checker (`python3 corpus/evidence/round30/rerun-check.py --stated 6 …` → `RERUN_RECEIPTS=5/6`, exit 1; byte-identical to the build copy); D3 scores 76/66/72 against 78; no-reader 79/84; `dns_header_keyed` 13/16 at v3 and 16 at v4; D1 SCORECARD correction (8 GETs, 8 responses 200); D4 `lessons/round-25.md` correction; D5 `lessons/round-29.md` correction; S050-S056 rows mined (`SOURCES.md` +19/-0 lines) and cited by `corpus/knowledge/quote-reopen-r30.md`; the Gate window 03:15-03:25Z matches receipt mtimes 03:15:56-03:21:51Z.

CLAIMS: C1 holds, C2 falsified
