# chousa round 99 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-09
round: chousa 99 · base `47ed34fa785288837f84cde9db15c41300854a78` · lane HEAD `ab280f6c9b9f381085583daedbad6ff0a6b85fe1`
report: `.ufo/reports/round-99/chousa.md` (fleet repo) · prompt: `.ufo/prompts/chousa-round-99.md`

Driver digest (`.ufo/watchdog.log`, copied):
`2026-11-09T00:57:59-03:00 launch chousa round=99 pgid=3746420 driver=hyaku-inline attempt=1` ·
`2026-11-09T02:07:38-03:00 complete chousa round=99; hyaku-inline attempt=1`

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report authored by lane | `git log --format='%an %H' -- .ufo/reports/round-99/chousa.md` | `chousa-shokunin 0cd1fc83c08074fefaf53ddc16c13363b4c65306` (2026-11-09 02:06:57 -0300, before the complete line) | ok |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]`, each with an evidence pointer | ok |
| cited commits on `master` | `git merge-base --is-ancestor <h> master` for 47ed34fa, d41f4cd8, f8f480ff, 96d761ee, c3bad643, 7fa312ac, ab280f6c | all ancestors; the six round commits authored `chousa-shokunin` | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state chousa-shokunin` · `git status --porcelain` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `ab280f6c…` | ok |
| prompt carries template contract | `grep -n '^#' .ufo/prompts/chousa-round-99.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit/push, §6 hyaku addendum, §7 scratch, §8 pre-file ledger | ok |

Not a marker report: two claims, six lane commits, committed receipts. Status `ok`.

## 2. Claims (step 2)

Neither claim is exploratory. Gates (`tools/gate-records.py`, `research-gate.sh`, `search-rerun.py`, the two round-99
batteries) are lane-owned and were not executed here (PROTOCOL §Gate standard, closure consequence): their committed
receipts were evidence-verified, and the claim cores were re-measured with plain reads over committed bytes at `ab280f6c`.

### C1 `C1-GATE-CHALLENGE-R99` — operability

Claim: `gate-records.py verify` gains CHALLENGE — a url/admit record, or a rev record on `corpus/captures/<24 hex>.txt`,
fails when its capture has ≤200 words and one of 11 frozen markers.

- Re-measured: `git diff 47ed34fa 96d761ee -- tools/gate-records.py` → 39 added lines; `git diff 96d761ee ab280f6c --
  tools/gate-records.py | wc -l` → 0 (tool bytes identical F2..HEAD, as reported). `CHALLENGE_MAX_WORDS = 200`;
  `CHALLENGE_MARKERS` has 11 entries; `is_challenge` is called on the url/admit path (line 280) and on the rev path
  guarded by `CAP_RE.fullmatch(kv["path"])` (line 307).
- Re-measured (independent re-implementation of the rule, lower-case + whitespace-collapse, over all 203
  `corpus/captures/*` blobs at HEAD): 5 captures hit — `0954149536aa…`, `58725f5e0ac4…`, `ff9013bd7d93…` (18 words,
  "cookies must be enabled"), `b5b8d050eea0…` (23 words, "checking your browser", "recaptcha"), `b90988847e70…` (37 words,
  "client challenge", "a required part of this site couldn't load") — i.e. the S229/S021/S022/S032 cookie pages, S230 and
  S234, matching the PROD legs and the comment block.
- Harm, re-measured: `git grep -l <capture key> ab280f6c -- corpus/knowledge corpus/lessons` for the 5 keys → only
  prose mentions in `corpus/lessons/round-98.md` and `round-99.md`; no knowledge entry cites a challenge capture, so no
  committed admit record newly fails (consistent with `HARM_SAME=25/25`).
- Evidence-verified receipts: `before/c1-base.txt` → `NEG_REFUSED=0/7 POS_ADMITTED=4/4 PROD_REFUSED=0/4 HARM_SAME=25/25
  BASE_NEG_ADMITTED=7/7`, `CHALLENGE_CONTROLS_R99=FAIL`, `exit=1`; `after-f2/c1-all.txt` → `NEG_REFUSED=7/7
  POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 ORACLES_REJECTED=5/5`, `CHALLENGE_CONTROLS_R99=PASS`, `exit=0`, with the
  base-blob do-nothing control re-run at F2 (FAIL, exit 1). `after-f2/c1-separability.txt` → PASS with C2's entry and
  captures deleted (`HARM_SAME=24/24`); the unmodified battery crashes there (`exit=1`), which is the probe's point.
- Matches the report. **Verifies.** Axis operability: **improved**.

### C2 `C2-ENTRY-R99` — coverage

Claim: new entry `corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 and S233 (opened this round), 23
located quotes, 8-row decision table.

- Re-measured: the entry exists at HEAD (143 lines added, absent at base); 25 `GATE-RECORD` lines = 23 url/admit + 2
  url/reject (S232 403, S235 500). Independent check over committed bytes: for all 23 admit records the capture blob's
  sha256 equals `capture_sha256` and the normalized quote is a substring of the capture text → **23/23**.
- Re-measured: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 230 at base, 235 at HEAD; removed lines in
  the SOURCES diff: 0 (append-only). Entry front matter `source: S236, S233`.
- Evidence-verified: `before/c2-base.txt` (`GATE_RECORDS_ERROR missing …` exit 2; controls exit 2); `after-f3/c2-all.txt`
  (`GATE_RECORDS files=1 records=25 ok=25 fail=0`; `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`; `rev_match=4/4`,
  `SEARCH_RERUN: CLEAN`; `QUOTES=23/23 … FORGERY_REFUSED=10/10 ACCEPTED=2/2`, `ENTRY_CONTROLS_R99=PASS`; all `exit=0`).
- Matches the report. **Verifies.** Axis coverage: **improved**.

### Axis table (must agree with the MANIFEST entry)

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured + receipts |
| coverage | improved | C2 re-measured + receipts |
| depth | unchanged | no claim; no knowledge entry edited (`git diff --stat` touches only the new entry) |
| freshness | unchanged | no claim; no SOURCES row changed |
| calibration | unchanged | QUALITY 230 added (line 1442); no claim |
| adjacency | unchanged | `PROVINCE.md` untouched; tameshi overlap routed |

SCORECARD diff `47ed34fa..ab280f6c` is append-only (round-99 verdict + round-100 plan); no axis harmed.

## 2b. Pre-file falsification ledger

`python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 99` →
`PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=8 findings=0`, exit 0. Ledger covers both claims and all 8
attack seats; no failing row to adjudicate.

## 3. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S233 (Mogull 2017, PLoS One) | admit, tier A | `curl -sL https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727` → http 200, 229,201 bytes; quote "I estimate that 14.5% …" present (grep count 1) | agree | publisher full text; quote located live and in capture; 24 words (`wc -w`) ≤ 25 |
| S236 (Europe PMC core record, PMID 26528420) | admit, tier B | `curl -s` the logged REST URL → contains "Indirect references accounted for less than one sixth of all quotation problems" | agree | authors' abstract via third-party index; B under the lane's carrier rule is defensible (tameshi grades A: routed fleet question) |
| S234 (Research Integrity and Peer Review, 2025) | reject (route) | `curl -sL` → http 200, 3,038 bytes, "client challenge" present | agree | 200 whose body is an interstitial, not the article; exactly the C1 case |
| S232 (PeerJ 1364) | reject (unreachable) | `curl -sL` → http 403, 5,431 bytes, quote absent | agree | still unreachable; reject is honest, flip condition stated |

New SOURCES row re-opened: S233 (`teaches` column paraphrases the 14.5% finding; the ≤25-word located quote sits in
`corpus/lessons/round-99.md` `## Gate` and its GATE-RECORD, 24 words, located in capture `4b70901ad80c513f0c2f750c` and
live). Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → `ok`, exit 0 (7
warnings: six W04 cross-scope duplicate URLs, one W01 S226 tier C mined — all pre-existing, same count as the lane's
census-start/end).

## Trend verdicts

- expansion: **improved** — registry 230 → 235 (re-counted), one new knowledge entry on ground with 0 base hits.
- quality: **improved** — the gate now refuses the 5 committed challenge captures (independently re-derived) with no
  committed admit record newly failing.
- discernment: **improved** — 4/4 spot-checked gate decisions agree on re-open, including the http-200 challenge reject.

## Defects routed to the lane (round 100; status-neutral)

1. `after-f2/c1-all.txt` tail: the do-nothing control's label "corrected by hand after the run" — rerun the control so the
   receipt's echo matches the blob it ran, rather than editing a receipt.
2. C1 limits the wave measured remain open: rev path not normalized before the capture guard (`R99SentinelC1` F-1);
   `R99MutantsC1` 13/28 survivors (no per-marker NEG fixtures, no 199/200/201 boundary); battery crash instead of SETUP on
   a missing fixture capture (seen in the separability probe).
3. S235's flip condition met by a seat re-open, and the 2025 update's Europe PMC record reachable: lane GETs owed.
4. Seat hygiene: `R99MutantsC2` receipts without seat prefix; L1 used `sed -i` for a README edit.
5. Fleet question (operator): one tier rule for index-record abstracts (chousa S236 B vs tameshi S327 A).

SHONEN note for the operator: boxes 2 (LOG `## Round 99`) and 3 (battery command + committed receipt) are checkable by a
non-author from committed bytes; promotion is operator-owned and was not done here.
