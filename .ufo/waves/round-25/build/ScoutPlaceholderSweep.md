# Round 25 — criterion-10 placeholder sweep

Scope: read-only Markdown sweep of `SKILL.md`, `LOG.md`, `SCORECARD.md`, and `corpus/` in the lane tree. Criterion: `corpus/QUALITY.md:38-43`.

## Primary grep and classification

Observed `grep -rnE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH|\[record ' ... --include='*.md'`: **10 matching lines in 6 files**; `grep -rnEo` count: **12 token occurrences**.

| Location | Hit(s) | Classification | Evidence |
|---|---|---|---|
| `SCORECARD.md:667` | `TBD` | **Shipped placeholder**; unquoted and names a still-undetermined round-14 claim. | Lines 665-668: “claim TBD … pre-registered at the round-14 opening.” |
| `corpus/knowledge/hardening-r10.md:488` | `${GSHA}` | **Shipped placeholder** (M-5); the gate revision value is missing, despite being inline-code formatted. | `Gate 91a01695… → ${GSHA}…`; `corpus/lessons/round-24.md:16` independently records this as M-5 and `grep -c → 1`. |
| `SCORECARD.md:1297`; `corpus/evidence/round25-claims.md:67`; `corpus/lessons/round-24.md:16` | `${GSHA}` | **Data in backticks — allowed.** Each line names the existing placeholder as a finding/claim/lesson datum, not as a value to substitute there. | SCORECARD round-25 plan; preregistration claim 3; M-5 row. |
| `corpus/QUALITY.md:39-41` | `TODO`, `TBD`, `[record `, `LANE_HASH` | **Data in backticks — allowed.** These are criterion examples and its literal grep expression. | The rule and command are quoted at lines 39-43. |
| `corpus/knowledge/sweeps-rejections-r5.md:132,249` | `TBD` | **Data in backticks — allowed.** Literal table/test values, not open fields in this note. | Line 132 reports the tested `TBD` flip value; line 249 enumerates values the mode accepts. |

**Primary totals:** 10 matched lines = **8 data lines / 2 shipped-placeholder lines**; 12 matched tokens = **10 data / 2 shipped placeholders**. The two actionable findings are `SCORECARD.md:667` and `corpus/knowledge/hardening-r10.md:488`.

## Angle-bracket and `XXX` supplement

`grep -rnEo '<[^<>]{1,80}>|XXX' ... --include='*.md'` returned **139 angle-bracket candidates in 49 files**; `XXX` was **0** (separate case-insensitive search also returned no matches).

| Classification | Count | Evidence / examples |
|---|---:|---|
| Definite unfilled template slots in records or recorded commands | **10** | `LOG.md:159` `<preserved spec>` is presented as the `--spec` argument to a completed plan command; `LOG.md:645` `<FILL>` leaves the round-16 gate hash blank; `corpus/knowledge/root-slash-boundary-r15.md:5` `<abs-source>.jsonl` is an unfilled `recheck:` input; `corpus/lessons/2026-10-15-claims-span-fidelity.md:57` `<probe>.jsonl` precedes reported run output; `corpus/lessons/2026-10-15-anchor-token-boundaries.md:51,92,110,195` `<scratch>` remains in before/after run paths; `corpus/knowledge/audit-r11.md:173` `<r8 baseline>` is in the “verbatim key lines” run; `corpus/lessons/2026-10-16-gate-behavioral-baseline.md:123` `<that baseline>` is in the measured probe row. |
| Intentional syntax, schema/metavariable examples, masked-value sentinel, operator text, or HTML-comment markup | **129** | Examples: CLI grammar in `SKILL.md:70-76` and `:103`; result grammar in `SKILL.md:325-338`; metadata output grammar in `round25-claims.md:29-38`; `<V>` masked-value examples in `corpus/evidence/README.md:595,622`; `<!-- -->` parser examples in `corpus/knowledge/html-comment-r20.md:10,20,28`; operator `<>` in `corpus/knowledge/anchor-boundaries-r4.md:65`. The `<tree-root>`/`<pre-round QUALITY.md>` args are explicitly documented parameters in `corpus/evidence/round24-measure.sh:2-6`, matching `SCORECARD.md:1256-1258`’s usage notation. |

Angle total is 139 (=10 definite slots +129 intentional syntax/markup); no `XXX` occurrences. All cited files were read in context; no source files were changed.

**Observed vs inference:** command outputs and cited source lines are observed. The 10-slot angle classification is a contextual judgment distinguishing run/evidence values from documented grammar; the two primary grep violations are unambiguous under QUALITY.md 10.

Installs: none.
VERDICT: Criterion-10 sweep found two primary violations plus ten unfilled angle-bracket slots; no `XXX` hits.