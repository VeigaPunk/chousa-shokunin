# chousa round 98 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-09. Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6`, lane HEAD `80b754e425361f7fdc4675aa85ac36366dacf2b1`.
Report `.ufo/reports/round-98/chousa.md` (fleet repo). Driver digest (`.ufo/watchdog.log`):
`2026-11-08T23:43:41-03:00 launch chousa round=98 pgid=1117672 driver=hyaku-inline attempt=1`;
`2026-11-09T00:54:52-03:00 complete chousa round=98; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report author | `git log --format='%an %H' -- .ufo/reports/round-98/chousa.md` | `chousa-shokunin 36fb35d85f661d6ad6bd8bb2aeedebecbd770455` (2026-11-09 00:53:46 -0300) | ok |
| SHONEN heading | read report | `## SHONEN`, four `[~]` lines, one per box | ok |
| cited commits on branch | `git merge-base --is-ancestor <h> master` for base, `aac82684`, `bc3ebc7c`, `1689f4ad`, `1c6e01c5`, `f0050074`, `80b754e4` | all 7 ok | ok |
| pushed, clean | `jj-lane.sh state …` ; `git status --porcelain` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; `ls-remote` master = `80b754e4…` | ok |
| prompt contract | `grep -n '^#' .ufo/prompts/chousa-round-98.md` | §1-§5 template sections, §6 hyaku addendum, §7 scratch, §8 pre-file ledger | ok |
| evidence timing | `git log -1 --format=%ci` | F3 commit 00:40:46, C2 receipt `ts=2026-11-09T03:40:57Z` (00:40:57 -03), landing 00:43:01 | ok, not future-dated |

Defect (status-neutral): `.ufo/waves/round-98/claims.json` `freeze.F3` is the placeholder string
`"<the lane commit that first carries the F3 amendments>"`, not `1c6e01c52149c7b4d6dfc4a8cfc419243dc8c101`.

## 2. Pre-file falsification ledger (step 2b)

`python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 98` →
`PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=8 findings=0`, exit 0. Every `falsifies-wording`
row (C1: R98MutantsC1, R98SentinelC1, R98RevenPrior; C2: R98ExecC2Repro, R98MutantsC2, R98ReviewerC2,
R98CriticClaims, R98ScoutSources) names a narrowing (A1-A7, B1-B8); I read the F2 sentences in `claims.md`
and found them consistent with those amendments (e.g. M1 now stated as the record's title, limit (d)
names G01-G03/D05/F1, limit (e) rewritten at F3).

## 3. Claims (step 2)

**C1 `C1-SELFTEST-R97MUTANTS-R98` (operability)** — rests on a lane-owned self-test and battery:
evidence-verified, not executed (§Gate standard, closure consequence), plus plain measurements.

- Plain: `git show <rev>:tools/search-rerun.py | grep -oE '"(g00|r[0-9]{2}|[pmj][0-9]{2})-[a-z0-9-]+"' | sort -u | wc -l`
  → base 48, HEAD 67; ids `g00-guard-canary`, `r01`…`r34` present. Matches "67 named case lines (round 97's 48, g00, r17-r34)".
- Evidence: `corpus/evidence/round98/after-f2/c1-all.txt` header `computed_against F2=1689f4ad…`; line 70
  `SEARCH_RERUN_SELFTEST: PASS cases=67/67`; tally line equals the frozen predicate verbatim; `SELFTEST_CONTROLS_R98=PASS`, `exit=0`.
  Before `before-f2/c1-base.txt`: `KILL_REQUIRED=12/35 … EQUIVALENT_SURVIVED=0/3 … BASE_KILLED=12/37`, FAIL, exit 1.
- Revision measured: F2; `git diff --stat 1689f4ad 80b754e4 -- tools/search-rerun.py corpus/evidence/round98/selftest-controls-r98.py` empty, so the receipt grades the landed bytes.
- Out-of-sentence residue (not a falsification): `after-f2/c1-rescore-r98mutants.txt` shows R98MutantsC1 survivors
  G01-G03, D01-D05, R32. G01-G03/D05 are named limit (d); D01-D04 are killed by the battery's DIRECT_PATH leg;
  R32 (verify-line double space) is caught by the round-95 battery per the seat report §3 but is not in SCORECARD's round-99 plan.
- Verdict: **verified** (operability improved).

**C2 `C2-ENTRY-R98` (depth)** — re-measured independently.

- Quotes vs sources: a script I wrote extracted every `| M/K | S | "quote" |` row of the entry and checked it
  (whitespace-normalised) against the live Europe PMC record (S231 abstractText + title, fetched 2026-11-09) and the
  committed S225 capture `corpus/captures/347c55ba9be9d63afe17986e.txt`: 37/37 located and ≤25 words (M1 first
  appeared to mismatch: the title carries a U+00A0 before "Statement."; equal after normalisation).
- Coverage: question-mark lines in S225 capture lines 33-80 (checklist heading to "Derived from:") = 36; held by the
  round-97 entry's S225 quotes 16, by the round-98 entry's 20, by both 36. Matches `BASE_HELD=16/36` → `36/36`.
- Counts: M rows 15 (title + 14 abstract quotes) as stated.
- Gate tallies evidence-verified: `after-f3/c2-all.txt` (computed_against F3) `GATE_RECORDS files=1 records=38 ok=38 fail=0`,
  `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, `rev_match=5/5`, `SEARCH_RERUN: CLEAN`, controls tally = predicate,
  `ENTRY_CONTROLS_R98=PASS`; entry and instruments unchanged F3..HEAD (`git diff --stat` empty).
- Verdict: **verified** (depth improved).

**Harm.** `git diff 98b8177c 80b754e4 -- SCORECARD.md` appends only the round-98 verdict and plan. `git diff --stat`
over `tools/ PROVINCE.md`: only `tools/search-rerun.py` changed; PROVINCE untouched. `after-f2/c1-verify-harm.txt`:
8 `SAME`, 0 diff lines. SOURCES diff: four appended rows (S228-S231), one S225 `used-by` cell, one search-log line.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0 (W04 ×6 pre-existing, W01 S226).

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1, evidence-verified + case count re-measured |
| depth | improved | C2, re-measured (quotes, 36/36) |
| coverage | unchanged | 226 → 230 rows (one admit), no coverage claim |
| freshness | unchanged | no re-verification claim |
| calibration | unchanged | no calibration claim |
| adjacency | unchanged | PROVINCE untouched |

## 4. Discernment spot-check (step 3)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S231 Europe PMC core record, PMID 27005575 | admit, tier B | `curl` the REST URL → http 200; title, doi 10.1016/j.jclinepi.2016.01.021, pmid, vol 75, pages 40-46 present; quote "The seventh (skilled translation … was removed," found in abstractText, 13 words | agree | authors' own abstract via a third-party index: B under the carrier rule is right; quote located verbatim |
| S228 CADTH report 477 appendices | reject (unreachable) | `curl` → http 403 | agree | no bytes; flip condition stated |
| S230 NCBI Bookshelf NBK98350 | reject (route) | `curl` → http 200, body contains "recaptcha" | agree | 200 status but challenge body; refusing is correct and the gate-tool gap is routed (QUALITY 229) |

SOURCES row re-opened: S231 (new) — its ≤25-word quote is the 13-word Results sentence above, located in the live record. Agree.

## 5. Trends

- expansion: **improved** — new knowledge entry closing README round-97's "17 of S225's question lines" gap (36/36 re-measured); registry 226 → 230.
- quality: **improved** — self-test 48 → 67 cases; base tool kills 12/37 R97 mutants, landed tool 35/37 (committed receipts).
- discernment: **improved** — three route refusals and a tier downgrade each agreed by this non-author re-open.

## 6. Routed defects (lane fixes next round)

1. `claims.json` `freeze.F3` placeholder — record the F3 hash (or state the convention) in future claims.json.
2. R98MutantsC1 survivor R32 (verify-line whitespace invisible to the self-test) is absent from SCORECARD's round-99 plan; route it with the G01-G03/D05 items or record why the round-95 leg suffices.
3. Carried from the lane's own plan: `tools/gate-records.py` admits a quote from an http-200 challenge page (`gate-records-challenge-200.txt`); NO_WRITE leg blind to writes outside its dirs (A6).
