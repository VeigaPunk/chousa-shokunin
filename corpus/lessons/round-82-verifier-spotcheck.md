# chousa round 82 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-06. Report `.ufo/reports/round-82/chousa.md` (fleet repo). Lane HEAD before `142b6f0c08e645ef9507f6d880be44e518c39043`,
after `03b586d1b8dc493623a2b758170307444bfc42be`. Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-06T16:37:37-03:00 launch chousa round=82 pgid=645538 driver=hyaku-inline attempt=1`;
`2026-11-06T17:46:30-03:00 complete chousa round=82; hyaku-inline attempt=1`.

Verdict: **status ok, not admitted (`rejected-honest-stop`)**. Both declared claims are falsified by their own frozen
kill rules; the closure agrees with both stops after re-reading the firing evidence.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-82/chousa.md` | `chousa-shokunin 811b5618… 2026-11-06T17:45:24-03:00` (before the 17:46:30 complete line) | pass |
| prompt committed | same over `.ufo/prompts/chousa-round-82.md` | `chousa-shokunin e46a247d… 16:37:35-03:00`; carries §1–§5 template contract + §6 hyaku addendum | pass |
| `## SHONEN` heading, one line per box | report lines 128–137; `git show 03b586d1:SHONEN.md \| grep -c '^- \['` → 4 | 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for 142b6f0c, 5d792e1e, 38f5af82, 57c0d167, b4a41d25, 46dd1dc3, 51a5dee8, 03b586d1 | 8/8 ok | pass |
| pushed, nothing uncommitted | `jj-lane.sh state …` ; `git status --porcelain` ; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = `03b586d1…` | pass |
| egress before fetch (r81 routed defect 3) | commit time of 5d792e1e vs `refetch.tsv:152-156` | 19:41:56Z < first fetch 19:42:03Z | closed |

Conformance defects (status-neutral): (1) the report's knowledge count "94 → 95" counts `corpus/knowledge/.gitkeep`;
`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` gives **93 → 94** (direction unchanged).
(2) `repair/rerun-repaired.txt` is headed "working tree gate" and `repair/selftest-repaired.txt` carries no revision
header; neither pins the tree it ran on to `51a5dee8`.

## Per-claim re-check

### C1 operability — evidence-verified (lane gate; not executed by closure)

`k2-gate-r82.py` drives `tools/research-gate.sh`, a lane-owned gate, so per PROTOCOL §Gate standard (Closure
consequence) closure verified committed evidence only.

- Instrument pins: `sha256sum` of `k2-gate-r82.py` = `4d6ba055…`, `depth-r82.py` = `726d3ed9…` at both 38f5af82 and
  03b586d1, equal to `instrument-pins.txt`; `tools/research-gate.sh` at 38f5af82 and 142b6f0c = `d5d48128…` = pin
  (gate unchanged before freeze).
- Before: `controls/c1-k0-donothing.txt` → `RUNLINES=2/2 K2_REFUSED=0/11 HOLD_REFUSED=9/9 CLASS_REFUSED=2/24
  POSITIVE=5/6`, `K2_GATE=FAIL`, `rc=1`. Matches report.
- After: `after/c1-after.txt` → `11/11 9/9 24/24 6/6`, `K2_GATE=PASS`, `rc=0`; `after/c1-selftest-after.txt` (rev
  b4a41d25) → `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`. Matches report.
- Controls: `controls/summary.tsv` 14/14 expected = observed (4 C1 FAIL; 8 C2 FAIL; P1 and B1 PASS).
- **K2 fired — closure agrees.** Static read of `tools/research-gate.sh` at b4a41d25, `load_sections()` line 870:
  `SEC_BODY[$sec]=""` on every `## ` heading, so a repeated heading discards the earlier body. A first
  `## Rejections` carrying an empty flip followed by a clean second one is therefore invisible to the item-4 check —
  exactly `R82ReviewerGate.md` F1 (receipts `r-dup-rejections.post.txt`, `r-dup-claims.post.txt`).
- **K3 fired — evidence-verified** (`R82ReviewerGate.md` F2 mixed `where=n/a,lib/x.md`; F3 Negatives carrier beside
  non-empty Sweeps). F3 the reviewer itself flags as a letter-of-rule reading; F1 alone kills the claim.
- Repairs (51a5dee8), evidence only: `repair/k2-gate-repaired.txt` still `K2_GATE=PASS`; `selftest-repaired.txt`
  `PASS (283 cases, 0 skipped)`; `rerun-landing.txt` → `rerun-repaired.txt`: in-class refused 182 → 185/185, but
  **out-of-class refused 8 → 9** and ambiguous refused 4 → 5 — one more out-of-class record is refused at the tip
  (not adjudicated by the lane; routed below).

### C2 depth — re-measured by closure

Command (frozen counter, pinned sha, run from the 38f5af82 archive copy against each archive tree):
`git archive <rev> | tar -x -C $S/<rev>; python3 -B $S/38f5af82/corpus/evidence/round82/depth-r82.py --root $S/<rev>`

| rev | observed |
|---|---|
| 38f5af82 | `DEPTH_R82 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0` / `DEPTH_R82=FAIL` |
| b4a41d25 | `ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11` / `entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4` / `PASS` |
| 03b586d1 | identical to b4a41d25, `PASS` |

Matches report. **K3 fired — closure agrees.** At b4a41d25 row 1 reads Never "force an intervention, comparator and
outcome onto a mapping question", warranted Q6/Q7 (S210). Closure re-opened the capture
`corpus/captures/bcb4a695b2aa019305121cff.txt` line 838 ("JBI suggests utilising the PCC …" — a suggestion) and line
840 ("there may be a compelling argument to use a different question format (such as PICO or … PECO) … as a precursor
to a systematic review"), and the live page (HTTP 200, both sentences FOUND). The source endorses PICO/PECO for a
subset of row 1's own situation; the Never is not supported. The landed row 2 already says so, so rows 1 and 2
conflicted. Repair after scoring does not rescue the claim (frozen K3 text).

### No-harm check

`git diff 142b6f0c 03b586d1 -- SCORECARD.md`: append-only (+33 lines, round-82 verdict + r83 plan); no prior row
edited. Non-evidence diff touches LOG, SCORECARD, SKILL (4 lines, item-2/item-4 notes), QUALITY (+1), README, SOURCES
(5+/2−), the r81 entry (Crossmark addendum), the new entry, lesson, gate. `PROVINCE.md` untouched. Census
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, only the five pre-existing W04
duplicate-url warnings (S051, S053, S073, S074, S075). Registry `grep -cE '^\| S[0-9]{3,} \|'`: 208 → 211. No axis
harmed.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | unprovable-but-better | claim falsified (K2 by static read, K3 evidence); tip gate refuses the r81 K2 forms with selftest 283 PASS (evidence-verified); one extra out-of-class refusal at the tip unadjudicated |
| depth | unprovable-but-better | claim falsified (K3, agreed); entry exists with 11/11 located quotes, 4 fresh sources, ground K4 held; row 1 repaired post-scoring |
| calibration | unchanged | QUALITY +1 row (163); no calibration measurement |
| coverage | unchanged | PROVINCE untouched |
| freshness | unchanged | S028 mined; no drift surface measured |
| adjacency | unchanged | `R82ConnectorSiblings.md`: no sibling holds question-frame content |

## Discernment spot-check (lesson `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S210 | admit | live `jbi-global…/pages/355862687` (HTTP 200) + capture bcb4a695 | agree | Gate quote FOUND live and in capture; page is the JBI scoping-review question section it claims |
| S008 | admit | live Cochrane Handbook chapter 2 (HTTP 200) | agree | quote "The review PICO (planned at the protocol stage) …" FOUND live; anchor drift self-reported and repaired |
| SPIDER / PRISMA-ScR | reject-for-now | live S008 page; `grep -c -i spider corpus/SOURCES.md` | agree | live S008 has 0 hits for "SPIDER" and "frame their questions"; no registry row, nothing taught; flip condition stated |
| S211 (new SOURCES row) | admit | live `…/pages/355862707` (HTTP 200) + capture 97223722 | agree | Gate quote (21 words, ≤25) FOUND live and in capture; capture sha `b8b542d9…` = `refetch.tsv` txt_sha256; registry `teaches` cell is a faithful paraphrase |

## Trend verdicts

- **expansion: improved** — knowledge `.md` entries 93 → 94 (new question-framing entry, K4 held), registry 208 → 211,
  S008 and S028 moved queued → mined.
- **quality: unprovable-but-better** — the gains (185/185 in-class refusal, 283 selftest, entry row repair) rest on
  post-scoring repairs that no frozen predicate scored; evidence-verified only, and the tip refuses one more
  out-of-class record than landing.
- **discernment: improved** — both claims filed as honest stops on the wave's own findings; the prefreeze r4-07
  byte-vs-description catch (QUALITY 163); all four sampled Gate decisions agreed on re-open.

## Routed defects (lane fixes next round)

1. Adjudicate the out-of-class record newly refused at the tip (`repair/rerun-landing.txt` out refused 8 →
   `rerun-repaired.txt` 9): name it and rule harm or in-class before freezing r83's control set.
2. Pin repair receipts to a revision (`# rev <hash>` header in `rerun-repaired.txt` and `selftest-repaired.txt`).
3. Count knowledge entries with `grep -c '\.md$'` (the `.gitkeep` inflated 94 → 95).
4. r83's gate claim must include duplicate-heading, fenced and commented table records in its frozen control set (the
   F1 class is a parser property, not a vocabulary one).

SHONEN: all four boxes `[~]`; operator note only — box 2 (`R82ExecTrial.md` end-to-end trial) and box 4
(`R82SentinelScope.md`) look checkable by a non-author; promotion is operator-owned.
