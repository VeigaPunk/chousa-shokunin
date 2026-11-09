# R100ReviewerC2 — C2 fidelity review (kill rule) at F 6d4e8487

Scope: `corpus/knowledge/quotation-error-update-r100.md` + `## Update` in
`corpus/knowledge/quotation-error-rates-r99.md` against S238 capture
`b5eec205612ee5f138cf065d` (U0=title, U1–U13 in `abstractText`) and S236
`405a0054e1f6dbd1854a3618` (J1/J2), SOURCES rows S236–S239, refetch.tsv.
Tree: shared clone at F. Counting commands reproduced:
- `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md`
  → `records=17 ok=17 fail=0`, exit 0
  (`R100ReviewerC2-gate-r100.txt`).
- `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .`
  → `QUOTES=16/16 FIELD=16/16 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=24/24 NEVER=8/8
  FRESH=1/1 TOPIC=1/1 NUMBERS_SOURCED=24/24 BASE_TOPIC_HITS=0 BASE_ENTRY=absent
  BASE_UPDATE_LINK=0 FORGERY_REFUSED=13/13 ACCEPTED=2/2`,
  `ENTRY_CONTROLS_R100=PASS`, exit 0 (`R100ReviewerC2-entry-controls.txt`).
- Captures' full abstracts: `R100ReviewerC2-abstracts.txt`; refetch S237–S239:
  `R100ReviewerC2-refetch.txt`.

## Decision rows (Do/Never vs warrants)

All eight Never cells are identically `(none stated by the sources)` — no
Never overreach. All Do numerals are token-equal to warrants (controls
NUMBERS/NEVER legs pass).

| Row | Verdict | Evidence |
|---|---|---|
| 1 Stating how often | faithful | 16.9%, CI 14.1%–20.0%, major 8.0% [6.4%–10.0%], "46 studies analyzing 32,000" all verbatim from U4/U7. No invented precision. |
| 2 Reading 2015 next to 2025 | OVERREACH | Final clause of Do — "the gap between them is not a measured trend" — is stated by no warrant. U9's flat slope (-0.002, p=0.85) is the meta-regression trend *within* the 2025 study set; nothing in J1/J2/U4/U7 states anything about the cross-synthesis gap. The clause is a lane inference presented in the Do (source) column, not the Lane column. Same sentence repeated in the r99 `## Update` ("their gap is not a trend"). |
| 3 Asking whether improved | faithful | "no significant improvement over recent years (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85)" verbatim from U9; supported by U12. |
| 4 Journal standing as proxy | OVERREACH (minor) | Do: "record the association only as printed: ... risk of bias and the number of references were not". The qualifier is dropped: U10 says "were *statistically significantly* associated". "Were not" converts a non-significance result into a null-association statement, widening the source. The completion "was associated with total error rate" (U10 ends "but journal impact factor was:") is a faithful syntactic completion; only the dropped significance qualifier overreaches. |
| 5 Defining what is counted | faithful | "count a reference that does not support the authors' claim" = U1; "about half ... classed major" = U7 "approximately half classified as major" (spelled-out quantity, unchecked per named limit (b), but faithful). |
| 6 Weighing the pooled estimate | faithful | "heterogeneity was high; Egger's ... remained negative throughout" verbatim U8. Lane cell correctly notes the statistic is not stated. |
| 7 Judging how synthesis was made | faithful | Method list (no date/language restriction, two raters, random-effects meta-analyses + meta-regression, OSF) each from U3/U5/U6. Do omits PubMed/WoS/reference lists by omission only — not overreach. |
| 8 Deciding what to do | faithful | "standing problem" = U12 "remain a problem"; "concerted efforts" = U13 "requires concerted efforts". "Needs" = "requires" faithful. |

## `## What this entry governs`, `## Named limits`, `## Update`

- **FIRED (governs + limits)**: "the full-text route, PMC12285159, answered
  http 500 to **both** of this round's GETs, S239" (line 20) and "answered
  http 500 to this round's **two** GETs" (line 89) are false as stated.
  `R100ReviewerC2-refetch.txt` shows **three** attempts each for S237
  (05:12:31Z, 05:18:33Z, 05:28:38Z) and S239 (05:12:32Z, 05:18:35Z, 05:28:39Z),
  all already present at pre-freeze P (6f837487) and at F. SOURCES.md's own
  round-100 log line says "seven GETs" (3+1+3), contradicting the entry's
  "both/two" inside the same tree at F.
- "Thirteen quotes from the abstract (U1-U13) and the record's title (U0)" —
  count held (13 + U0 = 14; + J1/J2 = 16 total, matching QUOTES=16/16).
- Verified-at identity (Baethge C, Jergas H; Res Integr Peer Rev 2025;10(1);
  doi 10.1186/s41073-025-00173-z; PMCID PMC12285159) matches all capture
  fields — held.
- Client Challenge history: "Round 99 could not read it — the publisher
  answered with a Client Challenge page (S234)" is borne by the S234 capture
  (`<title>Client Challenge</title>`) — held.
- "metadata verified" claims are within the abstract: the entry does not
  state an overlap count and its named limit correctly hedges "the abstracts
  do not say how many studies they share" — held. (The r99 `## Update`'s
  "the two rates pool different study sets" is true at different
  cardinality (28 vs 46); it does not assert disjointness.)
- r99 `## Update`: "no significant improvement over time by meta-regression"
  merges U9 ("over recent years", meta-regression) with U12 ("with no
  improvement over time", Conclusions). "Over time" slightly widens U9's
  "over recent years"; U12 supports "over time" for the conclusion but not
  specifically as meta-regression output. Minor conflation, subsumed by the
  row-2 overreach finding's second instance ("their gap is not a trend").

## Tier, SOURCES, Lane cells

- Tier B for S238 held: Europe PMC core record is a third-party carrier
  (authorString "Baethge C, Jergas H.", index platform) — same rule as
  S236 (B); consistent with the lane's carrier rule.
- SOURCES audit vs refetch/captures: S237 rejected with attempts 1–3 text
  matching refetch timestamps; S239 likewise; S238 admitted with correct
  capture key, sha, and summary ("a pooled 16.9% ... about half of them
  major (8.0%), with no significant improvement over recent years") faithful
  to U7/U9. S236 used-by change (added r100 entry) held: J1/J2 are genuinely
  re-quoted by the new entry. S239 used-by names the r100 entry (it names
  S239 as a rejected route); S237 used-by "—" is consistent because the
  entry never names S237 (checked).
- Lane cells held throughout: r99 first-row pointer, tier-rule note,
  G4/G5 definition note, "did not open the OSF protocol" (consistent with
  egress-approval's closed table), 2015-specific-measures note (J6/J7 vs
  U13's generic wording). No Lane cell contradicts a capture.

## Summary

Two fired sentences, one headlining: the entry understates its own S239
(and S237) GET count as "both/two" where refetch proves three each, and
row 2's Do states an unwarranted trend verdict in the source column. Rows
1, 3, 5, 6, 7, 8, the tier choice, SOURCES rows and Lane cells are faithful.

VERDICT: R100ReviewerC2 C2 fired — entry says "both/two GETs" where refetch shows three S239 attempts, and row 2's Do states a trend verdict no warrant says.
VERDICT: R100ReviewerC2 C1 n/a — this seat audited C2 fidelity only, no C1 artifact examined.
