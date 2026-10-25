# ScribeEntryFieldPolicy — Round 45 wave 1

## Item given
Draft the lane-re-grounded version of the staged `evidence-archive-field-policy-r41.md`, using the lane style and captures only; report it here. No production entry was written.

## Commands / reads and outcomes
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/claims.md`: C3 frozen predicate requires adopted entry, source lines binding S082/S083/S084 to corresponding URLs and quote spans; construction checks place the four quotes in README/paper captures. (Read only.)
- `read /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md`: staged content used as a subject, not copied as lane wording; its S139/S140 and Q17 references were excluded.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-version-binding-r36.md`: lane header and Observation / Inference / Unknown style observed.
- `read /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt`: README capture defines `cached_original_claim_url` at line 18 and `cached_source_url` at lines 35–37.
- `read /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt`: paper capture opened read-only.
- `grep 'we cache all pages used as evidence in the internet archive' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt`: `665:To avoid sources disappearing from the web, we cache all pages used as evidence in the internet archive 3 3`.
- `grep 'Archive\.org returns a 404 page for these' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt`: `3966: https://web.archive.org/web/20201229212702/https://archive.md/28fMd . Archive.org returns a 404 page for these. To view such a link, please just copy-paste the archive.is part (e.g.`
- `grep 'Where possible' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt`: one match at line 3981, describing extractive answers, not archive fields.
- `glob /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md`: lane knowledge style files listed; reference above inspected.

No external fetch, install, counter run, or production write. Scratch directory not created.

## Verdict / limits
Draft uses lane IDs S082/S083 only, source URL anchors, required four exact strings, the requested three body headings, and adds the bounded inference that a populated archive link does not establish that the capture resolves. The cited 404 is specifically about double-archived fact-checking article links in the paper's guideline, not a test of the AVeriTeC dataset's `cached_source_url` values. This draft does not claim those field values were live-checked. No report path for another seat is claimed.

## Draft

```markdown
source: S082 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md — JSON format example, claim and answer fields
source: S083 — https://arxiv.org/html/2305.13117v3 — Section 4, paragraph on evidence caching; Appendix J, archive-link guidance
verified-at: 2026-10-25
recheck: 365d
ground: The two archive fields describe links for different URLs and the paper describes evidence-page caching. These statements do not establish that every populated archive link resolves.

# What AVeriTeC archive fields describe—and what they do not establish

#### Observation

- The README describes `cached_source_url` as “An archive.org link for the source url” (S082). The paper says “we cache all pages used as evidence in the internet archive” (S083).
- The README describes `cached_original_claim_url` as “Where possible, an archive.org link to the original claim url” (S082). The wording marks the original-claim link as conditional; it does not state why a link may be absent.
- The paper's archive guidance says “Archive.org returns a 404 page for these” (S083), referring to the cited double-archived fact-checking-article links that also contain archive.is links.

#### Inference

- The two fields concern distinct URLs: an answer's evidence source and a claim's original location. Their descriptions are not interchangeable. The documentation supports treating the original-claim archive as best-effort; the paper describes caching pages used as evidence.
- A filled archive field records a link, not successful resolution of the linked capture. The paper's 404 example is a concrete warning that an archive.org link can return a 404; it does not establish that any particular AVeriTeC field value fails. A populated field is therefore not proof that the archived capture resolves.
- An empty `cached_original_claim_url` alone does not identify the cause of absence. The README's “Where possible” wording does not specify a per-record reason.

#### Unknown

- These captures do not establish whether each populated `cached_source_url` or `cached_original_claim_url` resolves, nor do they give the cause for an individual missing original-claim archive link.
- No linked archive page was opened here; this entry makes no claim about present-day resolution or availability.
```
