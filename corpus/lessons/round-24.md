# Round-24 lesson — learning from the lane's own mistakes (2026-10-19)

Lane `chousa-shokunin`, worktree HEAD `ab19cff` (2026-10-19); M-1..M-12 are the
STATE dossier's §4 ids (`.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/chousa-state.md`),
M-13/M-14 its D-6/D-2. Every pointer below was re-run in this worktree on
2026-10-19; `corpus/QUALITY.md` and `tools/research-gate.sh` carry uncommitted r24 edits.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M-1 | pre-registered wave not dispatched | `SCORECARD.md:1175` (16-seat AgentSwarm on `devin swe-2`); `LOG.md:804` (`direct integration (no wave — claim's before→after already measured by the r20 wave's live reproduction)`); commit `77bcfd1` subject `round-23: report (no wave — direct integration per honest-stop)` | 11 | criterion 11 appended; planned-vs-ran disposition now required; the r23 record stands as admitted |
| M-2 | claim registered before its before-state | `LOG.md:818` retracts the `--drift` truncated-baseline item as `measured as NOT a defect: every truncation form produces GATE_DRIFT ... exit 1`; commit `098f5e6` | 1, 3 | none — criteria 1 and 3 held; the correction landed with the claim |
| M-3 | stale open finding in the skill | `SKILL.md:432-434` (`the one live finding ... remains open pending fix-or-absorb`); `corpus/fixtures/archives-r9/A-r9.md:50` cites `A-shokunin-tradition.md:86`; `corpus/knowledge/audit-r11.md:320` (`finding closed; 18/19 is the pre-fix measurement`) | 9 | criterion 9 appended; the SKILL.md:432-434 close-in-every-file repair is queued r25 |
| M-4 | restated ledger numbers diverge | `SKILL.md:376-378` says `71 rows ... carried 23 · closed 7 ... queue 26` then `the 27-item round-11 audit queue`; `SKILL.md:430-434` repeats `carried 22 · closed 3 · finding 1 · operator 4`. Ledger: `hardening-r10.md:453-455` (r12: 38·23·7·0·3), `:484-486` (r13: 38·22·8·0·3), `:506-508` (r14: 38·21·9·0·3) | 9 | criterion 9 appended; the three divergent restatements are queued r25 |
| M-5 | unfilled template placeholder shipped | `corpus/knowledge/hardening-r10.md:488` — `Gate 91a01695… → ${GSHA}…` (`grep -c` → 1) | 10 | criterion 10 appended; the substitution is queued r25 |
| M-6 | limit ledger stale by 8 rounds | `hardening-r10.md` addenda end at `:520` (`### Round-15 addendum`); 0 addenda match r16–r23 though those rounds closed boundary classes; `SKILL.md:430` names this file as the one disposition home | 9 | criterion 9 appended; the r16–r23 addenda are queued r25 |
| M-7 | stale daily reflection committed | `considerthese/2026-10-19.md:3` (`4 commits, all between Oct 16 22:40 and Oct 17 12:56 BRT; nothing since`) vs 8 commits measured in that window and 12 between 09:06 and 12:00 -0300 on 2026-10-19; `:16` cites `68 rows` and the `27-item` queue; commit `efd9ba0` (09:06:17 -0300) | 10 | criterion 10 appended; the dated reflection stays as history (any correction is an appended erratum) |
| M-8 | uncommitted prior-session work absorbed mid-wave | `SCORECARD.md:1041-1043` — the uncommitted `tok_span_at` rewrite and `claims-cap-eof` case 123 `absorbed and recorded` | none — disclosure was recorded in the round-20 verdict; no criterion was appended because the work was disclosed, not hidden | none — recorded in the r20 verdict |
| M-9 | receipt cut withdrawn after a comparator artifact | `corpus/evidence/README.md:928-932` — first cut `20261016T054941Z` withdrawn; its live receipt compared case-line stability against a receipt that embeds no case lines | 3, 4 | none — criteria 3 and 4 already captured it; the withdrawn cut is kept as a note |
| M-10 | seat deficit / not-dispatched wave, recorded not backfilled | `SCORECARD.md:683` (`63/64 seat reports — seat 54 (OverflowScout) failed on a provider content-filter 400`); `SCORECARD.md:1138-1140` (`antigravity gemini-3.8-flash failed 24 seats ... + 8 aborted`); fleet `MANIFEST.json` round-1 closure (2026-10-15) has `lanes.chousa` = `in-flight` and `lane_rounds.chousa` = 1 | 5 | none — criterion 5 already captured it; the deficit is recorded, not backfilled |
| M-11 | calibration: score frozen while 19 verdicts say improved | `SCORECARD.md:7` — operability `3`, last-change `1`; 19 verdict rows record operability `improved` | 12 | criterion 12 appended and applied at this landing: the operability counting command (`SCORECARD.md` §Planned, round 1) re-run → `VERDICT_BEARING_EXPORTS=3/3` → score 3, re-derived (SCORECARD round-24 verdict); the narrow 3/10 construct itself is queued r25 |
| M-12 | path/index misfiling | `corpus/evidence/README.md:580` (`## Round-8 gate-baseline receipts`); 43 round-stamped r12–r23 receipt rows sit inside lines 580–733 (ten stamp prefixes; 45 stamp rows minus the 2 r12 baseline-file rows = 43); the last heading is `:830` (`## Round-10 ...`), so r12+ has no section | 9 | criterion 9 appended; the r12–r23 index sections are queued r25 |
| M-13 | metadata registry not machine-checkable | `corpus/knowledge/archives-verified-r9.md`, `audit-r11.md:22` (`recheck (from the lane cwd ...` — no colon), `gate-baseline-r8.md` lack the `^recheck:` key; at dossier time 0 of 21 values were dates, while the four r24 notes now carry ISO/cadence values (e.g. `json-delimiter-r24.md:5`, `recheck: 90d`), so the 3 legacy headers remain the defect (STATE D-6) | 6 | criterion 6 appended; the 3 legacy headers are queued r25 |
| M-14 | capability table vs LOG divergence | `SCORECARD.md:600-602`, `:674`, `:731` = 5 capability rows (r12×3, r13, r14); `LOG.md` records `Capabilities +1` at r13, r14, r15, r17, r18, r19, r20, r21, r22, r23 (10 lines) plus r12's 3 rows = 13 claimed; r16 says `+0`; 8 acquisitions (r15, r17–r23) have no row (STATE D-2) | 11 | criterion 11 appended (the capability-row duty already existed at `AXES.md` §Capabilities — the class is a duty not followed, so the bar now names it at landing); the 8 missing rows are queued r25 |

Pointer corrections after re-running from the worktree (dossier line numbers otherwise reproduce):

- M-4: the dossier's `:486`, `:493`, `:512` do not all reproduce as revision pointers. `:486` is the r13 counts line, `:493` is blank (the r14 heading is `:492`), and `:512` is the r14 supersede line. Corrected above: r12 counts `:453-455` (trail `:456-458`), r13 `:484-486` (trail `:487-488`), r14 `:506-508` (trail `:512-513`).
- M-8: the content begins at `:1041`; the dossier's `:1040` is the preceding line.
- M-10: the fleet entry is the 2026-10-15 round-1 closure; the 2026-09-29 round-1 closure has no `chousa` key. The cited `in-flight` value and `lane_rounds.chousa = 1` reproduce.
- M-13: the dossier's "0 recheck values are dates" no longer reproduces: the r24 notes now carry ISO/cadence values (`90d`, `on-release`). The three missing-key notes reproduce unchanged.
- Revision: every `SKILL.md:N` pointer above is at the pre-round commit `ab19cff` (`git show ab19cff:SKILL.md`). The round-24 fold inserted lines, so at the landing commit an original line N maps to N+2 for N 22–31, N+4 for N 32–40, and N+5 for N ≥ 41 (e.g. `:432-434` → `:437-439`).

## Unlearned before this round

Ten classes had no pre-round criterion: M-1, M-14 → 11; M-3, M-4, M-6, M-12 → 9; M-5, M-7 → 10; M-11 → 12; M-13 → 6. (M-2, M-9 and M-10 were already carried — criteria 1+3, 3+4 and 5; M-8 stays `none`: disclosed in the r20 verdict, not a bar failure.)

## Gate — sources opened this round (contract v1 rule 1)

Every row of `corpus/SOURCES.md` was opened in this round by its author
(L2 `R24ExecSources`, 2026-10-19); the knowledge executors re-opened the
rows they cite and quote them in their entries' `## Evidence`. Quotes are
verbatim, ≤25 words.

| id | URL / path | accessed | quote | location |
|---|---|---|---|---|
| S001 | `tools/research-gate.sh` | 2026-10-19 | "A manifest whose last byte is not '\n' (hand-edited, truncated, or written by another tool) would glue this object onto its last line" | append block comment; sha in `knowledge/json-delimiter-r24.md` |
| S002 | https://ifcncodeofprinciples.poynter.org/the-commitments | 2026-10-19 | "uses the best available primary, not secondary, sources of evidence wherever suitable primary sources are available" | Principle #2, criterion 2 |
| S003 | https://hapgood.us/2019/06/19/sift-the-four-moves/ | 2026-10-19 | "trace the claim, quote, or media back to the source, so you can see it in it's original context" | "Trace claims…" section |
| S004 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24 | 2026-10-19 | "We advise caution in assessing NRSI according to existing 'evidence hierarchies'" | §24.2.1.3 |
| S005 | https://aclanthology.org/2025.acl-long.1534/ | 2026-10-19 | "when citing papers have low fidelity to the original claim, future papers that cite the citing paper and the original have lower fidelity" | Abstract |
| S006 | https://arxiv.org/html/2605.06635v1 | 2026-10-19 | "Link Works verifies URL accessibility, Relevant Content measures topical alignment, and Fact Check validates factual accuracy against source content" | §3.3 |
| S007 | https://arxiv.org/html/2601.08536v3 | 2026-10-19 | "this only measures the accuracy of the citations and does not necessarily confirm that the information is correct" | §2.1 |
| S008 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 | 2026-10-19 | "the first and most important decision in preparing a systematic review is to determine its focus" | §2.1 |
| S009 | https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/assessing-risk-bias-included-studies-c52-c60 | 2026-10-19 | "Use (at least) two people working independently to apply the risk-of-bias tool" | Standard C53 |
| S010 | https://aclanthology.org/2025.acl-long.1574/ | 2026-10-19 | "mainly rely on Natural Language Inference (NLI) to assess binary or ternary supportiveness from cited sources, which we argue is a suboptimal proxy" | Abstract |
| S011 | https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf | 2026-10-19 | "Each sentence in a generated answer is checked against its cited document to verify factual grounding" | §1, evaluation workflow item 3 |
| S012 | https://aclanthology.org/2026.acl-long.1586/ | 2026-10-19 | "labels and rationales remain revisable: when a verifier disagrees with the current benchmark, it submits evidence" | Abstract |
| S013 | https://jsonlines.org/ | 2026-10-19 | "If a line terminator follows the last JSON value in a file, it must be the last byte in the file" | Requirement 3 |
| S014 | https://www.cebm.ox.ac.uk/resources/levels-of-evidence/levels-of-evidence-introductory-document | 2026-10-19 | "no evidence ranking system or decision tool can be used without a healthy dose of judgement and thought" | opening, 2011 document |
| S015 | https://openai.com/index/introducing-deep-research/ | 2026-10-19 | "It can sometimes hallucinate facts in responses or make incorrect inferences, though at a notably lower rate" | "Limitations" |
| S016 | https://en.wikipedia.org/wiki/Hierarchy_of_evidence | 2026-10-19 | "hierarchies are a poor basis for the application of evidence in clinical practice" | Criticism section |
| S017 | https://www.prisma-statement.org/prisma-2020 | 2026-10-19 | "an expanded checklist that details reporting recommendations for each item/sub-item" | PRISMA 2020 page |
| S018 | https://aclanthology.org/2026.acl-long.1430/ | 2026-10-19 | "we systematically analyze 134 papers, introduce a unified taxonomy" | Abstract |

Rows touched old→new: none (the registry is new this round). Before commit
the L1 narrowed, without re-opening, three cells the row author wrote: S006
and S007 `scope`/`teaches` (to the paper's own framework and statement, not
its results about evaluated systems — the round critic's province finding),
S002/S009 `recheck` `on-revision` → `365d` (contract cadences), and S001's
anchor (the landed revision instead of a draft sha).

## What the round learned

- A first fix is a hypothesis: the delimiter fix landed three times inside
  the round (bare `$(tail -c1)` → hex probe after a NUL test → unreadable
  refusal after the L2 reviewer's write-only repro). Each version passed the
  selftest it shipped with; only adversarial controls found the next hole.
- A test oracle can lie in the same way as the code: GNU grep reads a NUL as
  a line break in a binary file, so the case-135 blank-line check failed on
  correct output until `grep -a`.
- Before this round 11 of 14 mined mistake classes had no criterion; the
  repeated shape is "a record restates a fact owned elsewhere and drifts"
  (M-3, M-4, M-6, M-7, M-12, M-14) — one home per fact is the lane's most
  violated rule, now criterion 9.
