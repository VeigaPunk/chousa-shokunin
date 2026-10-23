Draft only; `corpus/SOURCES.md` was read and not modified.

| S048 | Unicode Standard Annex #15, Unicode Normalization Forms — https://unicode.org/reports/tr15/ | spec | A | UAX #15 on NFKC compatibility normalization and formatting or semantic distinctions it can erase; not a quote-verification policy | §1.1, Figure 2 (`#Compatibility_Equivalence_Figure`); §1.2, Normalization Forms (`#Norm_Forms`) | NFKC folds compatibility differences and can erase formatting distinctions or distinctions significant to text semantics | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r29.md |

Evidence: opened `https://unicode.org/reports/tr15/` (Unicode 18.0.0, revision 58); §1.2 quote: “Normalization Form KC additionally folds the differences between compatibility-equivalent characters that are inappropriately distinguished in many circumstances.” (17 words; access date 2026-10-23).

Risk: For a verbatim-quote check, this can make visibly different strings such as ① and 1 compare equal after NFKC, so normalized equality alone does not prove character-for-character identity.

Work and gates: read `corpus/evidence/round29/claims.md`, `corpus/lessons/round-28-verifier-spotcheck.md`, and `corpus/SOURCES.md`; opened the specified UAX #15 URL. No shell commands or installs; no command exit codes apply. Draft row only, no registry or product files changed; no NFKC test or C1 measurement run.

Verdict: source row drafted for the requested narrow scope. Report artifact: `.ufo/waves/round-29/build/ScribeSrcUax15.md`.
