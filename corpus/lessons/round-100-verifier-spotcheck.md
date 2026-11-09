# Round 100 — non-author verifier spot-check (hyaku closure, 2026-11-09)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `chousa`, round 100. Lane HEAD at close: `f0aea4f14d3c733f1f2dfe5a9eb429300783fd3a` (master, `ls-remote` verified).
Base: `929c784c63a1fd17961d21742101b2b109b7b8ff`. Report: `.ufo/reports/round-100/chousa.md`.
Re-measurements were run by the verifier against committed bytes (not by reading receipts alone); where a claim rests on a lane-owned gate, the committed evidence was verified and the gate was not re-executed against sibling state beyond the claim's own frozen counter commands.

## Step-1 conformance

- Report committed in fleet repo by lane identity: `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-100/chousa.md` → `chousa-shokunin f4bab3b975d03439d65985b12684e7d1bda7ce3f`. PASS.
- `SHONEN` heading present with one line per box (4 lines, all `[~]` with evidence pointers). PASS — not a marker report: content carries work, evidence pointers, landed changes tied to LOG, and a checkable final hash.
- Cited commits all ancestors of master: `git -C chousa-shokunin merge-base --is-ancestor <hash> master` for P `9683523467a1be9a9c46972f9b92bed26f44750d` and final `f0aea4f14d3c733f1f2dfe5a9eb429300783fd3a` both ok. PASS.
- Lane clean and pushed: `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `f0aea4f1...`. PASS.
- Prompt carries the template contract (§1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 push scope, §6 hyaku addendum). PASS.
- Dispatch/completion digest (from `.ufo/watchdog.log`, copied): `2026-11-09T02:10:45-03:00 launch chousa round=100 pgid=616576 driver=hyaku-inline attempt=1`; `2026-11-09T03:59:42-03:00 complete chousa round=100; hyaku-inline attempt=1`. Single attempt; no earlier round-100 attempt existed.

Defects (status-neutral): none found in step-1 items.

## Claims — re-measured by the verifier

### C1 `C1-GATE-REVCAP-R100` (operability) — RE-MEASURED, verified on the A1-A6 sentence

Command (run twice, 2026-11-09, tip `f0aea4f1...`):
`python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work <scratch>` → exit 0.

Observed: `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=28/28 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`. 59 `CASE ... PASS` lines.

- Predicate line matches `claims.json` regex exactly (`HARM_SAME=(\d+)/\1`, `harm_min 26`); 28/28 ≥ 26. The after-F2 receipt (`after-f2/c1-all.txt`) reads `HARM_SAME=27/27` — the count grew by one because the lesson file (carrying GATE-RECORD lines) landed at the final commit after the F2 receipt was taken; the predicate is satisfiable by construction and the delta is explained, not a mismatch.
- Before receipt independently consistent: `before/c1-base.txt` shows the base tool at `REV=3/11 PROD=4/6`, `CHALLENGE_CONTROLS_R100=FAIL` exit 1, `BASE_REV_ADMITTED=8/11` — the same 8/11 the after run reports, and the 8 refused set is exactly the round-99 F-1 class (`./`-relative spellings, `.raw`, byte copies).
- Frozen bytes: `git diff 6d4e8487 4ba51a26 -- tools/gate-records.py corpus/evidence/round100/challenge-controls-r100.py corpus/evidence/round100/entry-controls-r100.py` → empty. Tool, battery and controls are byte-identical F..F3, so the F2 receipt measures the landed bytes.
- Harm: `HARM_SAME=28/28` over every committed file with GATE-RECORD lines — base and round-100 tools produce identical stdout and exit codes; no owned axis harmed.

**Kill-rule adjudication (C1).** The frozen kill rule's literal text — "any wave artifact shows a rev record whose blob has a capture's object id at that rev, whose capture text is a challenge page by the round-99 rule, and which this tool prints OK" — *is* met by `R100SentinelC1` F-1 (byte-identical copy under a new key rebinds the oid) and F-2 (`--repo` at a subdirectory empties the capture set). The row is real, was disclosed in the report, and is the reason for amendments A5/A6 (named limits (i)/(j), routed to round 101). C1 therefore does **not** verify on the F1 sentence; it verifies on the narrowed A1-A6 sentence, which is the sentence the predicate and limits actually state. This is the disclosed outcome, recorded here so the closure is not read as claiming the un-narrowed sentence passed.

### C2 `C2-ENTRY-UPDATE-R100` (freshness) — RE-MEASURED, verified on the B1-B9 entry and sentence

Commands re-run independently at tip (all exit 0):

- `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md` → `GATE_RECORDS files=1 records=17 ok=17 fail=0`.
- `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .` → `QUOTES=16/16 FIELD=16/16 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=24/24 NEVER=8/8 FRESH=1/1 TOPIC=1/1 NUMBERS_SOURCED=24/24 BASE_TOPIC_HITS=0 BASE_ENTRY=absent BASE_UPDATE_LINK=0 FORGERY_REFUSED=13/13 ACCEPTED=2/2`, `ENTRY_CONTROLS_R100=PASS`.
- Harm: `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md` → `records=25 ok=25 fail=0`; `entry-controls-r99.py` → `ENTRY_CONTROLS_R99=PASS`.

- Entry provenance trio present (`source: S238, S236`, `verified-at`, `recheck: on-release`); round-99 entry carries the `## Update` flag naming the entry and S238. Before receipts show the do-nothing controls failing (entry absent → exit 2; pre-link → `FRESH=0/1 FAIL`). C2 is sourced on S238, opened this round. C2 kill rule: no wave artifact after the B1-B9 repairs shows a Do/Never overreach, an unlocated quote, or a sign/form mismatch — the counter-evidence (B4/B5 limit (e)) is named in the narrowed sentence.
- Registry delta verified: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 238 at tip, 235 at base (`git show 929c784c:...`); S236 `used-by` = `corpus/knowledge/quotation-error-rates-r99.md, corpus/knowledge/quotation-error-update-r100.md` (NF=13, used-by column correct).

## Pre-file falsification ledger (§8/addendum)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 100` → `PREFILE-FALSIFICATION: pass claims=2 rows=20 attack_seats=8 findings=0`, exit 0 (re-run by verifier).

Adjudication: 20 rows cover both claims; every `falsifies-wording` row (11) names its narrowing in the note column (A1-A6 for C1 incl. A4 no-narrowing answer, B1-B9 for C2). All are real and reconciled by the F2/F3 amendments; A4 was answered without narrowing via `after-f2/q3-note-is-challenge.txt`. No unreconciled real row against the narrowed sentences. The ledger script independently reached `pass`.

## Discernment spot-check

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| S238 · admit (tier B, `mined`) | `corpus/captures/b5eec205612ee5f138cf065d.txt` (sha256 `175f805d...` = refetch.tsv row S238, http 200) + live re-open of the Europe PMC core record URL (pmid 40696441, doi 10.1186/s41073-025-00173-z, 2025) | agree | 19-word Results quote is located verbatim in the capture's abstract; carrier-rule tier B is the lane's standing treatment of index-carried abstracts (S236, S231); live fetch returns the same record with `16.9%` in the abstract |
| S239 · reject (http 500 ×3) | `corpus/evidence/round57/refetch.tsv` rows S239 (05:12:32Z/05:18:35Z/05:28:39Z, curl rc 22, http 500, no bytes) + lesson GATE-RECORD `capture=none words=0` | agree | rejection is evidence of taste, not fabrication: flip condition (a 200 carrying the XML) is stated; seat re-open answering 200 is correctly treated as a different request, not a contradiction of the lane's GETs |
| S237 · reject (http 500 ×3) | refetch.tsv rows S237 (05:12:31Z/05:18:33Z/05:28:38Z, rc 22, 500) | agree | same as S239; W04 duplicate-URL warning vs S235 (round-99 attempt, also rejected) disclosed in lesson and census |
| S238 quote ≤25 words | lesson GATE-RECORD line | agree | quote is 19 words, counted; anchor names the field (`abstractText`, Results) and the location is the capture |
| S110 row quote ≤25 words (`teaches` cell) | `corpus/SOURCES.md` S110 row | agree | `teaches` text is 18 words (counted); anchor names section 3, the 检索策略 paragraph, and char offsets |

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `chousa ok`. Before/after census receipts (`census-start.txt`, `census-end.txt`) match; the one new W04 (S237/S235 same URL across scopes, both rejected) is disclosed. W01 S226 (tierC mined) is pre-existing.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | gate judges rev records by object identity: `REV 3/11→11/11`, `PROD 4/6→6/6`, 12/12 oracles refused, harm 28/28 |
| depth | unchanged | no depth claim; QUALITY 231 + SKILL correction line added, no depth move claimed |
| coverage | unchanged | registry 235→238; new entry sits on ground round 99 opened (S238), no uncovered coverage-map ground |
| freshness | improved | first `on-release` recheck answered in the lane (1/26); 2015 reading flagged in place; `FRESH=1/1` |
| calibration | unchanged | both sentences narrowed to their instruments before filing (A1-A6, B1-B9); kill-rule literal disclosed rather than buried |
| adjacency | unchanged | kagi `on-release` watchers routed by `R100ConnectorSiblings`, not absorbed; PROVINCE untouched |

No axis harmed.

## Trend verdicts

- **expansion: unchanged** — registry +3 rows but the admitted entry is on ground round 99's coverage map already held; no new frontier ground entered.
- **quality: improved** — gate now follows the object git resolves (8 fixture + 2 production records the round-99 tool admitted are refused, byte-identical output elsewhere); a held rate re-verified against its newer source and flagged where held.
- **discernment: improved** — S238 admitted at B under the carrier rule, S237/S239 refused with flip conditions; 20 ledger rows adjudicated with every `falsifies-wording` narrowed, and the kill-rule literal disclosed. (Author-assessed; the verifier's spot-check above concurs on the sampled decisions.)

Author trend verdicts in the report agree with the verifier's: expansion unchanged, quality improved, discernment improved.

## Routed defects (lane must fix next round)

1. C1 limits (i)/(j) (R100SentinelC1 F-1/F-2 as amended at F3): byte-copy oid rebinding and subdir `--repo` still print OK — bind `oid -> [paths]`, read the sibling of the named capture path, anchor `ls-tree` to the repo root, fail loudly on an empty capture set. Already in SCORECARD `## Planned — round 101` item 1.
2. C1 limit (f) / battery loosenings (h): two-commit fixture with cross-rev legs; battery PASS must check the REV verdict code, both HARM channels, and missing oracle sites. Planned item 1.
3. C2 limit (e): FRESH must require one checkable warrant numeral in the `## Update`; an `on-release` must name its watcher. Planned item 2.
4. Seat hygiene: `R100MutantsC1` left three unprefixed files in the wave dir; `R100ScoutSources` made a third attempt on one URL beyond its item's two. Process notes only; already disclosed in the report.

## Attestation

I did not author round 100. I re-ran the frozen C1/C2 counter commands, re-opened the sampled sources, re-ran the census and the pre-file ledger, and read the wave artifacts and the amendments myself. C1 verifies on the narrowed A1-A6 sentence (the literal kill rule is met by R100SentinelC1 F-1/F-2 and was disclosed — see adjudication); C2 verifies on the B1-B9 entry and sentence. No axis is harmed. Spot-check hash cited by the closure entry is the `landed` hash of the commit carrying this file.
