# R57W2ReviewReport — pre-file contract check on the L1 report draft

Seat: leaf reviewer (no subagent dispatch). Scope: `.ufo/waves/round-57/w2/chousa-report-draft.md`
(no fleet `.ufo/reports/round-57/chousa.md` exists yet — `ls` → No such file), audited against
`.ufo/prompts/chousa-round-57.md` §4 (lines 99–129) + `w1/R57W1ReviewReportShape.md` gates 1–10.
Target file read at `3010e75`; lane HEAD `3010e7537d163d9a76264a166d491214ecdaf45e`. No lane writes
other than this file; no scratch needed (all checks read-only against the live tree).

## Passes

- **Section order** — `grep -n '^## '` draft → Work performed / Landed changes / Before→after
  measurements / Sources & frontier / Trend verdicts / SHONEN, exactly the §4 order. **PASS**.
- **SHONEN grep gate** — `grep -c '^## SHONEN'` → `1`; `grep -c '^- \[[x~ ]\]'` on draft → `4`;
  `grep -c '^- \[[ x~]\]'` on lane `SHONEN.md` → `4`. All `[~]` (correct — no external promotion
  verifier) each with a resolvable pointer (verified `tools/capture-fetch.py`,
  `tools/store-record-audit.py`, `corpus/knowledge/grey-literature-field-china-r42.md` exist). **PASS**.
- **W1 settled** — `python3` on `w1-results.json` → `seats=65 results=65`; `ls w1/R57W1*.md | wc -l` →
  `65`; results names ≡ on-disk reports (set difference empty); committed (git ls-files shows all).
  Role mix vs `w1-spec.json`: 12 scout/21 executor/13 reviewer/6 critic/6 scribe/2 mutation-tester/
  2 connector/1 sentinel/1 revenger/1 simplifier — matches draft verbatim; attack share
  (13+6+2)/65 = 32% ≥25%. **PASS**.
- **Counters at tip** — I ran both: `c2-count.py` → `SET=47 … C2=PASS` exit 0; `c3-count.py` →
  `BOUND=4/7 (R1:S131 R2:S132 R3:S133 R7:S118) SWEPT=3/3 QUOTE_ROWS=10 … C3=PASS` exit 0, identical
  to the draft's quoted strings. **PASS**.
- **Receipt headers** — `controls/c2-before.txt` first line names `6656f077…`; `c3-before.txt`
  names `c2f914c…`; `census-start.txt` carries `exit=0` + 5 W04 + `ok`; SOURCES rows `grep -c '^| S'`
  → 133; S131/S132/S133 present at lines 141–143, tier B. **PASS**.
- **Trend verdicts** — one verdict each expansion/quality/discernment, each `improved` with evidence
  pointers. **PASS**. **Stale-lane line** (line 52) and **tool installs: none** (line 54) present.
  **PASS**.
- **LOG tie** — `LOG.md:1883` `## Round 57` names `e0e73e0f`, `a8d4e7da`, `c2f914c`, `fd95724`,
  `6656f07`, `b022b13`; a `**Waves.**` bullet covers the W1 seat accounting (dispatch commits
  `a03824d`/`3010e75` not literal-hashed but their content is the waves bullet's subject). **PASS**.
- **Fleet misroot** — `git -C /home/vgpnk/Projects/shokunin status --porcelain` → only
  `?? .ufo/reports/round-61/kake.md` (kake lane; not ours to touch). **PASS**.

## Defects

- **D1 (major) — "wave-settled" claim false at draft-write time; filing now repeats round-55 D1.**
  Draft:13 says "W2 residual call (8 seats) returned 8/8 reports, zero dead; both `*-results.json`
  committed." Observed: `ls .ufo/waves/round-57/` shows **no `w2-results.json`**;
  `ls w2/R57W2*.md | wc -l` → 5 seat reports of 8 (CritDoNothingRound, MutC2Counter, MutC3Counter,
  ReviewC2After, SentFinal); `git status` shows every w2 file untracked, plus mid-flight edits
  `M SCORECARD.md`, `M corpus/lessons/round-57.md`, `?? corpus/evidence/round57/attempt3-sidecar-audits.md`.
  Draft (mtime 06:23) predates most seat reports (SentFinal 06:27). W2 seat count/dead-seat claims
  are unverifiable until `w2-results.json` exists and the seat .md set is committed. Gate 1 requires
  WAVE-DONE + results handoff + commit before filing.
- **D2 (moderate, QUALITY 108) — measurement citations missing receipt-named revisions.**
  (a) C3 after: "re-run at the integration tip" names no revision — must be a hash (the recorded
  re-verify commit is `1c9626e`'s "C2/C3 re-verified PASS at this state").
  (b) C3 before: "re-derived at freeze `fd95724`" — no committed receipt's first line carries that
  revision (`c3-before.txt` names `c2f914c`); the actual receipt is `w1/R57W1ReviewBefore.md`
  (re-derived at `fd95724ad150…`, diffs stripped-header-identical) — cite it explicitly.
  (c) C2 before "re-derived … at freeze `c2f914c`" — technically the string appears in
  `c3-before.txt`'s first line, but the honest citation is `R57W1ReviewBefore.md`; name it.
  C2 after `e0e73e0f`/`a8d4e7da` are named by committed `SCORECARD.md:2863` — those PASS.
- **D3 (minor) — Sources & frontier census claims exceed their receipts.** Draft:34 says start
  receipt "→ rows 130, exit 0" but `census-start.txt` has no row count (7 lines: 5×W04, ok, exit=0);
  `census-end.txt` has **no `exit=` line at all** (6 lines) though its `ok` line is present.
  Fix: paste the row-counting command (e.g. `grep -c '^| S' corpus/SOURCES.md` before/after) and
  record `exit=N` in the end receipt or re-run with `; echo exit=$?`.
- **D4 (minor) — universal clauses without counting commands.** "refetch.tsv … all attempts and
  committed bytes"; "all seat scratch roots were `/fast/scratch/hyaku/chousa-r57/<seat>/`" — and
  SentFinal:54 observed leftovers `R57W1ReviewAxes/ dryrun/ fetch/` still present; the draft is
  silent on cleanup. Either paste the count or scope the clause.
- **D5 (minor, disclosure) — committed `SCORECARD.md:2863` C3 freeze hash does not resolve.**
  `git cat-file -t fd95724d56a33a150cd2638fadd2ce1f3425e6c` → "Not a valid object name"
  (`…a150…` transposed; real object `fd95724d56a33ad150cd263f8add2ce1f3425e6c`). Worktree `git diff`
  already carries the `a150→ad150` fix (uncommitted, in flight — SentFinal F1). Draft's short
  `fd95724` citations resolve fine; the filed report should name the correction commit once landed.
- **D6 (trivial) — forward self-reference.** SHONEN box 4 cites `R57W2ReviewReport.md` (this file)
  before it exists; resolves at commit. Acceptable, noting for completeness.
- **D7 (trivial) — Landed-changes tail unwritten.** Line 25 leaves "the final lane tip … cited in
  the fleet report" as a forward reference; the last commit must also cover `w2/*.md`,
  `w2.ready.dispatched`, the SCORECARD/lesson fix and `attempt3-sidecar-audits.md` (untracked now).

## Residual risk

W2 is mid-flight: 3 seat reports still owed (ReviewC3After, CritC3Forge, this one), so every
W2-derived number in the draft (8/8, zero dead, results committed) must be re-derived from
`w2-results.json` at filing, not carried from the draft. Nothing else in scope was left unrun.

VERDICT: attacked the pre-file report draft — sections/SHONEN/counters/mix survive; falsified the
wave-settled claim (D1), two revision citations (D2), the census-receipt claims (D3).
