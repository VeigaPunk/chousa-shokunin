# AttackRowS048 — registry and live quote audit

**Assigned axis:** operability. Checks: source identity, scoped authority, quote fidelity, provenance, and no-harm.

**Scoped verdict: HOLDS** for S048's substantive source/knowledge use and the landed tool's result on its quoted warning. This probe does **not** falsify C1 or re-measure its frozen 130-item predicate. One metadata cell is **WRONG relative to the supplied review date**, as distinguished below; that is not a matching defect.

## Evidence opened

- `corpus/SOURCES.md`, especially line 58; `corpus/knowledge/quote-reopen-r29.md`, lines 1–104.
- The live [Unicode Normalization Forms page](https://unicode.org/reports/tr15/) through `read`, both rendered text and raw HTML. It identifies itself as Unicode Standard Annex 15, Unicode 18.0.0, revision 58, dated 2026-08-12. Its Status says it is approved for publication and stable, and may be cited as a normative reference.
- `corpus/knowledge/contextual-source-admission-r24.md`, lines 54–60, defines A as primary or authoritative for the stated scope.
- `corpus/evidence/round29/claims.md`, lines 38–119, for the frozen C1/matcher boundary; no frozen file was changed.
- `.ufo/waves/round-29/build/ScribeSrcUax15.md`, lines 1–11, and `build/ScribeKnowledge/quote-reopen-r29.md`, lines 1–65, for reported opening provenance. These are reports, not independently authenticated historical access receipts.
- The landed `tools/quote-reopen.py` declarations and item-loading/verification code, lines 351–416.

## Every S048 cell

| Cell | Verdict | Evidence / qualification |
|---|---|---|
| id | OK | S048 identifies the Unicode row and is the ID cited by the knowledge entry. |
| source | OK | The named annex/title agrees with the page opened at the exact registered URL. |
| kind | OK | `spec` is justified by the Unicode Standard Annex and approved/stable normative-reference status; this is not a secondary article. |
| tier | OK | A is justified **only for what UAX 15 itself says** about compatibility normalization. It is not authority for this lane's quotation policy. |
| scope | OK | Explicitly limited to NFKC and distinctions it can erase; explicitly excludes quote-verification policy. |
| anchor | OK | Both named sections exist. Raw HTML contains `name="Canon_Compat_Equivalence"` for section 1.1 and `name="Norm_Forms"` for section 1.2. The knowledge entry's `#Norm_Forms` locator is real. |
| teaches | OK | Section 1.2 says KC folds compatibility-equivalent differences and KC/KD must not be blindly applied; it explicitly warns about formatting and semantic distinctions. Section 1.1/Figure 2 includes circled ① versus 1. |
| status | OK | `mined` accurately describes the source's actual quotation/use in the cited knowledge entry. |
| opened | WRONG | The recorded `2026-10-23` is later than the supplied review date, so it cannot serve as an already-completed-as-of-this-review access record. The UAX scribe report repeats that date, while the knowledge scribe draft records an earlier opening date. The page cannot establish which historical opening date is correct; this finding is not an assertion that no opening happened. |
| recheck | OK | `365d` is a declared lane cadence, not a requirement attributed to Unicode. The knowledge entry separately declares 180d and release-triggered reopening; no claim of identical schedules is made. |
| used-by | OK | The named file exists and cites S048 at line 3 and uses its warning at lines 55–59. |

The landed entry's `verified-at` also carries the later date. **Smallest safe provenance correction:** reconcile `opened` and `verified-at` against actual access/verification evidence; do not guess or backdate from this review's clock alone. No frozen claim, counter, fixture, or denominator change is warranted.

## Quote and scope challenge

Copied from the page text I opened:

> Normalization Forms KC and KD must not be blindly applied to arbitrary text.

That sentence is the entry's S048 quote verbatim as readable text, including its final period. In raw HTML, `not` is inside `<i>not</i>`; markup and layout line breaks do not change the sentence.

The strongest local challenge is that NFKC can erase a meaningful distinction rather than preserve a character-for-character quotation. The page itself supports that challenge. The knowledge entry does **not** conceal it: lines 53–59 state the normalization steps, cite the warning, give the circled-digit example, and explicitly distinguish equality after folds from byte identity. Elsewhere in the entry, S048 is not used to authorize punctuation folding, zero-width deletion, boundary rules, claim truth, or quotation policy. **Beyond-scope use: OK — none found.** The frozen normalized meaning of `VERBATIM` is a disclosed design tradeoff, not an S048 implementation counterexample.

## Requested landed-tool probe

Created only this header plus one data row in `.ufo/waves/round-29/falsify/AttackRowS048/items.tsv`:

```tsv
id	source_id	quote
s048-warning	S048	Normalization Forms KC and KD must not be blindly applied to arbitrary text.
```

From the lane root, ran:

```sh
timeout 120 python3 tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS048/items.tsv
```

It printed the following result. Repeated with `&& timeout 5 printf 'EXIT_CODE=0\n'` solely to make the exit status explicit; the repeat produced the same verdict and printed `EXIT_CODE=0`:

```text
QUOTE_REOPEN	s048-warning	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
EXIT_CODE=0
```

**Tool verdict: VERBATIM. Correct: OK. Exit: 0.** The sentence is present on the live source, and S048's raw HTML has an explicit `</head>` before `<body>`, unlike the S047 limitation described in the entry. The inline emphasis around `not` was correctly tolerated.

## Limits and no-harm

Only S048 and its use in this entry were challenged; no full C1 measurement, other-source verdict, archive-based historical-date authentication, or canonical judgment was performed. Live content can change. No tool installs or updates. No production, frozen evidence, Git index, jj state, sibling lane, or fleet file was modified. Both commands were bounded and completed; no server or background job was started. The first tool call requested a terminal but reported that it was unavailable; the explicit-status repeat did not request one.
