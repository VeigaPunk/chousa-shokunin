# Cochrane LSR cadence source — round 26

## Opened source and outcome
- Requested Cochrane Community URL: `https://community.cochrane.org/review-development/resources/living-systematic-reviews`. `curl -sS -o /dev/null -w 'initial_http=%{http_code} redirect=%{redirect_url}\n' <URL>` returned `initial_http=301 redirect=https://resources.cochrane.org/`; following redirects returned HTTP 200 at `https://resources.cochrane.org/`, the Cochrane Resources homepage, not the guidance. The page-reader likewise returned the homepage as canonical.
- Official Cochrane alternative opened: *Guidance for the production and publication of Cochrane living systematic reviews: Cochrane Reviews in living mode*, Version December 2019, `https://resources.cochrane.org/sites/resources.cochrane.org/files/uploads/inline-files/Transform/201912_LSR_Revised_Guidance.pdf`. `curl -sS -o /dev/null -w 'pdf_http=%{http_code} final_url=%{url_effective}\n' <URL>` returned `pdf_http=200` at that exact URL; PDF text was accessible.
- The official Cochrane Interactive Learning module page also opened HTTP 200 and says it was last updated January 2026, but only its overview/outcomes were visible without launching the module; cadence findings below are grounded in the PDF, not inferred from that page.

## Findings
- **Observed:** Cochrane LSR guidance sets monthly searching at minimum for key databases and trial registries; it allows supplementary sources less frequently (e.g. every three or six months), and requires the frequency/range to be described in the protocol and reported in the review (§6.2, p.34).
- **Observed:** Search/screen cadence and publication/update cadence are distinct. Ideally publish an update when new evidence likely to affect conclusions is identified; when high evidence volume makes that less feasible, the protocol may set an editorial-team-approved fixed interval (example: every four months) (§4.3.4, p.19; fixed-interval scenarios §4.3.4.2, p.23).
- **Verbatim located quote (14 words):** “updated on a fixed-interval schedule approved by the editorial team (e.g. every four months).” — §4.3.4, *Once the review is in living mode*, p.19, Version December 2019.
- **[INFERENCE] C2 relevance:** this supports the semantics that a declared schedule can make an update due, but it distinguishes that schedule from search surveillance and does not establish a generic metadata field or date calculation.

## Proposed registry row (contract v1 column order)
`SOURCES.md` columns read at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:9-10`; v1 rules at `/home/vgpnk/Projects/shokunin/CORPUS.md:64-123`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| TBD | Guidance for the production and publication of Cochrane living systematic reviews: Cochrane Reviews in living mode — https://resources.cochrane.org/sites/resources.cochrane.org/files/uploads/inline-files/Transform/201912_LSR_Revised_Guidance.pdf | docs | A | Cochrane intervention LSR guidance on the cadence of evidence searches and review updates | §§4.3.4, 4.3.4.2 (pp.19, 23), §6.2 (p.34); Version December 2019 | Distinguishes monthly core database/registry searches from impact-triggered or protocol-fixed review publication updates; supplementary searches may be less frequent | queued | 2026-10-21 | 180d | — |

## Duplicate check and limits
- No duplicate of this LSR guidance row found in the opened registry. Existing S029 is Cochrane Handbook ch. IV on updating reviews, not this LSR production/publication guidance (`corpus/SOURCES.md:39`); S022/S030 are Elliott et al.'s paper, not this guidance (`:32`, `:40`). The highest existing ID observed is S033 (`:43`); use `TBD` here as requested until integration assigns the next ID.
- **Does not support (QUALITY 7/8 scope limits):** a universal cadence for systematic reviews outside Cochrane LSRs; a single mandatory interval for publishing updates; an assertion that monthly searches imply monthly published updates; a generic knowledge-entry `due`/freshness field, date-arithmetic rule, or verification-validity policy. The guidance is specifically for Cochrane LSRs, primarily intervention reviews (Introduction, pp.4, 12), and frames the interval choice as protocol-/context-dependent.
- Recheck `180d` is a curation judgment [INFERENCE], not a Cochrane requirement: the opened guidance is Version December 2019 and its introduction says the approach is expected to evolve.

Installs: none.

VERDICT: Official Cochrane guidance supports declared, protocol-specified LSR update cadence while separating it from monthly search cadence; its scope is Cochrane LSR methods, not general metadata freshness.
