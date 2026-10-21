# SrcAhrqSignals — AHRQ/Shekelle signal-detection source opening (round 26, C2)

Seat ChousaR26.SrcAhrqSignals-3 · 2026-10-21 · leaf member, no subagents. No installs (stock `curl` + `read` tool only).

## HTTP outcomes (observed)
- ANSWERED: https://link.springer.com/article/10.1186/2046-4053-3-13 — `curl -s -o /dev/null -w '%{http_code}' …` → `200`; full text served. Shekelle PG, Motala A, Johnsen B, Newberry SJ, "Assessment of a method to detect signals for updating systematic reviews", Syst Rev 2014;3:13, DOI 10.1186/2046-4053-3-13, published 2014-02-14, open access (SpringerOpen). This is the Shekelle 2014 open record assessing the AHRQ methods report (11-EHC042-EF). Page also displays: "An Erratum to this article was published on 26 March 2014" (10.1186/2046-4053-3-22).
- Blocked: https://www.ncbi.nlm.nih.gov/books/NBK56774/ (curl `200`, but read tool returned reCAPTCHA interstitial "Checking your browser before accessing www.ncbi.nlm.nih.gov"); no text obtained, not used.
- Blocked: https://effectivehealthcare.ahrq.gov/sites/default/files/pdf/updating-reviews-signal-detection_white-paper.pdf → curl `202`; body "JavaScript is disabled In order to continue, we need to verify that you're not a robot." Not used.
- Not opened: https://pmc.ncbi.nlm.nih.gov/articles/PMC4298255/ → curl `200` (official mirror candidate only; no quote drawn from it).

## (1) Verbatim located quotes (each ≤25 words)
- Q1 (grounds signal-triggered update policy): "supports a policy of delaying an update of a systematic review until new evidence is sufficient to warrant assigning it at least a medium priority" — 25 words; Discussion, paragraph beginning "With the limitation of small sample size in mind".
- Q2 (grounds the periodic half of the hybrid): "designed to assess each AHRQ systematic review every 6 months and to take 3 months to complete" — 17 words; Discussion, final paragraph.
- Also observed (Abstract, Results): "The agreement on overall priority for updating between prediction and actual changes to conclusions was Kappa = 0.74."

## (2) Proposed registry row (contract v1 column order; id TBD → S034, next unused after S033, L1 confirms)
| S034 | Shekelle et al. 2014, Assessment of a method to detect signals for updating systematic reviews — https://link.springer.com/article/10.1186/2046-4053-3-13 | paper | A | this study's own assessment of its 2009 AHRQ surveillance-signal method on 11 comparative effectiveness reviews (9 updated) and that program's 6-month assessment cadence; not a cadence or trigger rule for this lane's knowledge metadata | Discussion: paragraph "With the limitation of small sample size in mind" (delay-until-signal policy sentence); final Discussion paragraph (6-month cadence sentence); Syst Rev 2014;3:13, DOI 10.1186/2046-4053-3-13, open access, as served 2026-10-21 | Update priority can be triaged by evidence signals at periodic assessments instead of fired purely by a calendar due date; low-priority records safely waited for a signal (κ = 0.74) | queued | 2026-10-21 | 365d | — |

## (3) Scope limits — what this source does NOT support (QUALITY 7/8)
- Not authority for this lane's `recheck:` values or `--as-of` due-date semantics: clinical CER surveillance ≠ lane metadata policy; any transfer is a labelled lane inference (QUALITY 7).
- Does not support calendar-overdue updating as the mechanism: it argues updates can wait for signals ("delaying an update … until new evidence is sufficient") — counter-evidence to "due date fires ⇒ must update".
- κ = 0.74 is this study's result only: 9 CERs / 149 conclusions, one program, unblinded 2013 re-assessment (the paper's own three limitations). Not predictive validity of surveillance generally.
- Signal search is not complete: its one poor-concordance conclusion stemmed from evidence published after the signal-search window — does not support "no signal ⇒ current" (QUALITY 8: absence-of-signal ≠ truth observation).
- Nothing about deep-research agent outputs, web sources, or metadata header design; no `verified-at:` analog.
- Treating Q2's 6-month cadence as a recommended lane cadence would be use outside scope.

## Duplicate check
No AHRQ/Shekelle/signal-surveillance row in corpus/SOURCES.md S001–S033; nearest are S029 (Cochrane periodic), S032 (Shojania survival timing), S028 (Crossmark triggers) — different sources. No duplicate.

## Fit to C2 (overdue vs event-triggered rechecks)
Complements S029 (periodic assessment) and S032 (signal timing): grounds the hybrid — periodic assessment with signal-triggered priority — so a computed `due=` can coexist with event-triggered recheck. Left `queued`; mining is L1's call.

VERDICT: Opened Shekelle 2014 via SpringerOpen (HTTP 200) after NCBI/AHRQ bot-blocks; propose queued tier-A row S034 grounding signal-triggered triage over calendar-only rechecks.
