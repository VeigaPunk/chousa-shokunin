# chousa — round 57

## Work performed

Declared claims: **R57-C2 (freshness)** — re-fetch the 47 captures pinned by the base spans manifests into lane-owned, digest-checked bytes; **R57-C3 (depth, sourced)** — chain the workflow standard's normative references to their own documents. Both predicates/counters/controls were frozen in attempt 1 before data (`corpus/evidence/round57/claims.md`, commits `c2f914c` and `fd95724`); attempt 2 built on them, not widened them.

- **C2 capture pass:** added `tools/capture-fetch.py` (campaign GET recipe, max 3 attempts, lane-root guard) and `corpus/evidence/round57/refetch.tsv`; re-fetched the 47-pinned set, with all attempts and committed bytes; attempt-1/attempt-2 details and the 4 failed URLs in `corpus/evidence/round57/refetch.tsv` (101+ rows at last census of the record; final row count is re-derived below).
- **C2 measurement:** `python3 corpus/evidence/round57/c2-count.py` → `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (exit 0), independently re-derived by `R57W1ExecC2Recompute.md` (0 disagreements).
- **C3 entry and manifest:** added `corpus/knowledge/normative-reference-chain-china-r57.md`, 10-row `corpus/evidence/round57/c3/spans.tsv` and its span files (`tools/build-spans.py`); `python3 corpus/evidence/round57/c3-count.py` → `BOUND=4/7 (R1:S131 R2:S132 R3:S133 R7:S118) SWEPT=3/3 QUOTE_ROWS=10 ... C3=PASS` (exit 0).
- **Frontier / quarantine:** curated SOURCES rows S131-S133 (opened this round, tier B for the repost/mirror carriers), logged the S118/S127 used-by changes old→new; hand-checked 24 register rows in wave reports `R57W1QuarA-D.md`, zero fabrication verdicts; the lane census remains exit 0.
- **Routed D1:** appended `#### Corrections (round 57)` to `corpus/knowledge/grey-literature-field-china-r42.md`, correcting the stale 表 10 recheck instruction to 表7; the scribe's sweep found exactly one stale instruction and nine legitimate mentions (`R57W1ScribeD1.md`).
- **Mistakes / gates:** `corpus/lessons/round-57.md` records four mistakes (misroot, record-less bytes, seat scope write restored, inference-ground token miss); `corpus/QUALITY.md` criteria 111-113 and `tools/store-record-audit.py` are landed, with a live failing audit receipt for the known record-denied/orphan classes.
- **Wave evidence:** W1 (65 seats) returned 65/65 reports, zero dead; W2 residual call (8 seats) returned 8/8 reports, zero dead; both `*-results.json` committed under `.ufo/waves/round-57/`.
- **Round shape / role mix:** one v2 build+attack wave W1 (65: 12 scout, 21 executor, 13 reviewer, 6 critic, 6 scribe, 2 mutation-tester, 2 connector, 1 sentinel, 1 revenger, 1 simplifier; attack share = 21/65 = 32%); planner seat held by L1; plus the prompt's residual ordinary falsify call W2 (8: 3 reviewer, 2 mutation-tester, 2 critic, 1 sentinel). Total = 73 seats. The residual dispatch was under the prompt's explicit ≤8-seat residual clause after the v2 validator refused 8 lanes as below its 64-seat wave band; no wave was split or shrunk.
- **Scope / scratch:** all seat scratch roots were `/fast/scratch/hyaku/chousa-r57/<seat>/`; no installs/upgrades (no tool/version/channel entry owed), no pacman transaction attempted; the campaign cache was not recreated or modified.

## Landed changes

- **C2 fetch tool, record, captures:** lane commit `f9736a39a0344a0aed63a65dfaddf7db624303d9` (LOG Round 57, C2 bullet). The tool's first run misrooted 86 capture files + `refetch.tsv` into the fleet root; they were copied byte-exact to the lane, `cmp`-verified, and the fleet copy deleted under the mandated misroot sweep; fleet `git status --porcelain` was clean after.
- **C2 after-receipt and retry captures:** lane commit `e0e73e0f76163b014033e80c6ba53ed92c14113d` (LOG Round 57, C2 bullet). The record-less S105 wrap-up `.raw` was removed because the frozen UNREACHABLE predicate requires no capture; its historic bytes and pin-matching conflict are disclosed below.
- **W1 spec/dispatch:** lane commit `a03824d1a0c70278b33cca4ae4e2b8d6d9691e70` (65-seat v2 wave, policy v2).
- **C3 entry/manifest/registry/lesson:** lane commit `a8d4e7da15a70a06d731739cace43cc3287801a1` (C3=PASS; added entry, 10 span rows, S131-S133, S118/S127 used-by changes, lesson).
- **Quality, D1, curriculum, census:** lane commit `1c9626efba2455d513b6b18df9b3df291e66556f` (LOG/SCORECARD, QUALITY 111-113, store-record audit, fetch-tool root guard, S077 used-by fix, D1 append, census-end).
- **W2 residual dispatch:** lane commit `3010e7537d163d9a76264a166d491214ecdaf45e` (8-seat residual attack call, explicit prompt residual clause).
- Every landed change above is tied to `LOG.md` Round 57; the final lane tip is printed by `jj-lane.sh state` after W2 integration and cited in the fleet report.

## Before → after measurements

- **R57-C2 freshness:** before `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL` (committed `controls/c2-before.txt`, re-derived in a scratch clone at freeze `c2f914c`); after `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (lane master `e0e73e0f`; re-run at `a8d4e7da`). Command: `python3 corpus/evidence/round57/c2-count.py`. Before/after are on the frozen 47-triple set at `SET_REV=6656f077`; no target, count or recipe changed.
- **R57-C3 depth:** before `ENTRY=no BOUND=0/7 QUOTE_ROWS=0 C3=FAIL` (`controls/c3-before.txt`, re-derived at freeze `fd95724`); do-nothing HELD and CITER controls both `BOUND=1/7 C3=FAIL`; after `ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes BOUND=4/7 SWEPT=3/3 QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- C3=PASS` (lane master `a8d4e7da`, re-run at the integration tip). Command: `python3 corpus/evidence/round57/c3-count.py`. The target 4/7 and all heading/token/title rules remain frozen.

## Sources & frontier

- `corpus/SOURCES.md` census rows: **130 → 133** (S131-S133, all tier B; no tier A/B/C row altered); end command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → `ok`, exit 0, five pre-existing W04 duplicate-URL warnings (receipt `corpus/evidence/round57/census-end.txt`). Start receipt `corpus/evidence/round57/census-start.txt` → rows 130, exit 0, same five W04s.
- Row additions: 3 tier-B source rows (S131 2019 notice repost, S132 2021 notice repost, S133 2021 management-guideline attachment mirror). No status/recheck changes. Used-by changes old→new: S118 adds `normative-reference-chain-china-r57.md`; S127 adds the same entry; S077 drops non-entry tool path `tools/quarantine-check.py` (old `tools/quarantine-check.py, corpus/lessons/round-42.md` → new `corpus/lessons/round-42.md`).
- Frontier advanced: workflow-standard normative-reference chaining; entry lives at `corpus/knowledge/normative-reference-chain-china-r57.md` and cites S127/S118/S131-S133. C2's 47-record re-fetch is a quality/freshness move, not expansion. Assimilation: none adopted from the package; the 24-row quarantine slice was adjudicated and adoption stays closed. Considerthese: mined one stable-proposal-id proposal from `considerthese/2026-10-26.md`; no implementation was counted (see lesson/report), so no SOURCES row added.
- Cache blocker: `.qcache` remains absent and untouched; the operator L0 line from round 56 is still open. The three remaining normative technical guidelines R4-R6 are explicitly UNBOUND with query/host sweeps in the entry; no L0 decision was needed.

## Trend verdicts

- **expansion — improved.** One admitted entry on new coverage-map ground (normative-reference chaining of the 2025 workflow standard), citing three new `mined` rows plus held S118; 4/7 references bound by document.
- **quality — improved.** 47 pinned captures re-fetched and measured; D1 corrected append-only; S077 used-by contract fix; QUALITY 111-113 carry runnable checks shown able to fail; quarantine verdicts replace the register's false-fabrication class. Caveat: S105's unreachable verdict is record-level (its historic capture bytes match the pin), and the C2 counter's known 5-genuine quote-splicing forge is disclosed.
- **discernment — improved.** W1/W2 independent seats reviewed the C3 citations, C2 counters and quarantine decisions; the quarantine review found zero fabrications among 24 rows, a row-by-row correction of the register class; the C3 gate records three UNBOUND decisions with reason and the 2019 gcpunion repost was refused when its title quote repeated 3×, then S131 was pointed by document to nmgyyxh where the title occurs once.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md`; C3 entry + SOURCE rows (lane assertions; no external promotion verifier).
- [~] At least one end-to-end domain task executed and logged in LOG.md — LOG Round 57, C2/C3 after-receipts and counters.
- [~] Instructions executable by an agent without oral context — `python3 tools/capture-fetch.py --status`, `python3 tools/store-record-audit.py`, `python3 corpus/evidence/round57/{c2-count.py,c3-count.py}`.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md`; `R57W1ConnSiblings.md` / `R57W2ReviewReport.md`.

Stale-lane: respawn-per-round; no other mission of this lane is open.

Tool installs/updates: none. No pacman transaction attempted.
