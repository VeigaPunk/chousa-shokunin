# ScribeRowsNormalize — Round 45 wave 1 seat report

- Seat: `L1Chousa45.ScribeRowsNormalize` (leaf; no subagents spawned)
- Lane: chousa-shokunin, round 45, wave 1 (build + first falsifiers)
- Date: 2026-10-25
- Item: draft the three lane Registry rows S082/S083/S084 in the CORPUS.md census schema (11 cells) from staged rows S139/S140/S132, renumbered BY DOCUMENT, with self-located anchor quotes from the on-disk captures.

## Assignment and frozen constraints (from the ticket + claims.md)

- Rebind by document: S139 (AVeriTeC README) → S082; S140 (AVeriTeC v3 HTML paper) → S083; S132 (AVeriTeC train.json) → S084.
- status `mined`; opened `2026-10-25`; recheck stripped of prose (valid cadence only).
- NO literal or escaped `|` in any cell; anchor = own located quote ≤25 words from the capture; used-by exactly `corpus/knowledge/evidence-archive-field-policy-r41.md` for S082/S083 and `corpus/knowledge/evidence-snapshot-coverage-r40.md` for S084; 12 `|` per line; teaches grounded, no pipe.

## Drafted rows (verbatim)

```
| S082 | AVeriTeC dataset README (Schlichtkrull et al., MichSchli/AVeriTeC) — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md | dataset | A | the AVeriTeC corpus's own field dictionary — the project's documented meaning of the two archive fields, read from the dataset's own documentation rather than inferred from its values | record-schema block JSON field dictionary, lines 18 and 36: "Where possible, an archive.org link to the original claim url" and "An archive.org link for the source url" (main branch, 4,771 bytes, read 2026-10-25) | the two archive fields are not symmetric: cached_original_claim_url is documented as "Where possible, an archive.org link to the original claim url" — a best-effort field — while the evidence-level cached_source_url is documented as "An archive.org link for the source url" — stated without a qualifier; so an empty claim-level field records that no archive was taken for that claim's original URL, and does not mean that no archived copy of it exists | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-archive-field-policy-r41.md |
| S083 | The AVeriTeC corpus paper (Schlichtkrull et al., arXiv:2305.13117v3) — https://arxiv.org/html/2305.13117v3 | paper | A | the corpus's stated archiving practice — whether archiving was systematic or opportunistic, as the corpus's own paper describes it | the data-collection paragraph on web archiving, line 665: "we cache all pages used as evidence in the internet archive" (arXiv v3 HTML, 144,049 characters, read 2026-10-25) | the corpus states that it caches all pages used as evidence in the internet archive, so archiving at the evidence level is systematic; read together with S082, which restricts the claim-level archive to where possible, this makes an empty claim-level field a record of an archive not taken rather than of an archive that does not exist | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-archive-field-policy-r41.md |
| S084 | AVeriTeC training data (Schlichtkrull et al.; released with the FEVER workshop's AVeriTeC dataset) — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json | dataset | A | how completely the corpus binds each verdict to an archived snapshot of its evidence — the measure wave 5 asked for and could not state | record 1 evidence entry, line 29: "cached_source_url": "https://web.archive.org/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden"; and line 47: "cached_original_claim_url": null (3,068 records, 10,184,813 bytes, read 2026-10-25) | of the evidence entries in the file that carry cached_source_url, 6,510 hold a non-empty archive.org URL and 1 is empty — so the per-citation archive binding is effectively universal; but of the 2,531 records that carry cached_original_claim_url, only 1,145 are non-empty and 1,386 are empty — the claim's own original URL is archived for well under half of the records that have the field | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-snapshot-coverage-r40.md |
```

## Stripped prose (removed from recheck cells; cadence retained as `365d`)

- S082: "re-fetch the README and confirm the two field descriptions still read 'Where possible, an archive.org link to the original claim url' and 'An archive.org link for the source url'" (prior-run stamp "(ran 2026-10-24)" also stripped).
- S083: "re-fetch the v3 HTML and confirm the sentence still reads 'we cache all pages used as evidence in the internet archive'" (prior-run stamp also stripped).
- S084: "re-download the file and re-count the empty cached_source_url and cached_original_claim_url entries" (prior-run stamp also stripped).

## Commands run (verbatim decisive output)

1. Shape source: read `chousa-shokunin/corpus/SOURCES.md` rows S079–S081 (lines 89–91) — 11-cell shape `| S079 | <source> | spec | A | <scope> | <anchor> | <teaches> | mined | <open> | 365d | <used-by> |`; copied that shape.
2. Staged source: read `merge/chousa/SOURCES.append.md` lines 57 (S132), 64 (S139), 65 (S140) — full rows incl. teaches and prose-carrying recheck cells.
3. Row validation (`awk` on the draft file at `/tmp/chousa-r45-ScribeRowsNormalize/rows.md`):

```
line 1: pipes=12 fields=13
line 2: pipes=12 fields=13
line 3: pipes=12 fields=13
S082 | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-archive-field-policy-r41.md
S083 | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-archive-field-policy-r41.md
S084 | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-snapshot-coverage-r40.md
```

4. Anchor quote location (`grep -boF` over captures; byte offsets):

```
== README ==
1027:Where possible, an archive.org link to the original claim url
1969:An archive.org link for the source url
== paper ==
14755:we cache all pages used as evidence in the internet archive
121660:Archive.org returns a 404 page for these
== train.json ==
1415:"cached_source_url": "https://web.archive.org/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden"
2366:"cached_original_claim_url": null
```

5. Capture sha256 (grounding the train.json byte count 10,184,813):

```
ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c  .../974299ae4b5f3bdb808b36a9.txt
8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5  .../ce16d57277fedfd4f0e7750e.txt
a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f  .../412b146a2720ce6557268d05.txt
```

## Verdict

- All three rows satisfy the schema: 12 `|` per line, 11 cells (NF=13), no `|` inside any cell (verified by count; cells carry only prose, URLs, dates, and quotes).
- Rebound by document: S082=README URL, S083=arXiv v3 HTML URL, S084=train.json URL; S083's teaches cross-reference updated from staged `S139` to `S082`.
- Anchors are quotes I located myself in the captures (byte offsets above), each ≤25 words: README 11/8 words, paper 11 words, train.json data excerpts 2 tokens each.
- status `mined`, opened `2026-10-25`, recheck `365d` (prose stripped and listed above).
- used-by exactly as instructed: S082/S083 → `corpus/knowledge/evidence-archive-field-policy-r41.md`; S084 → `corpus/knowledge/evidence-snapshot-coverage-r40.md`.

## Resolvable pointers

- Staged rows: `merge/chousa/SOURCES.append.md:57` (S132), `:64` (S139), `:65` (S140).
- Shape exemplars: `chousa-shokunin/corpus/SOURCES.md:89-91` (S079–S081).
- Captures: `.../.qcache/ce16d57277fedfd4f0e7750e.txt` (README; quote @1027, @1969), `.../.qcache/412b146a2720ce6557268d05.txt` (paper; quote @14755, @121660), `.../.qcache/974299ae4b5f3bdb808b36a9.txt` (train.json; quote @1415, @2366; sha256 `ae5eda7c…`).
- Claims source: `chousa-shokunin/corpus/evidence/round45/claims.md` (construction-check char positions for the two README quotes match my located offsets 1027/1969; paper byte offset 14755 vs claim char 14575 — offset basis differs, bytes vs chars, no conflict).

## Out of scope / notes

- The two citing knowledge entries (`evidence-archive-field-policy-r41.md`, `evidence-snapshot-coverage-r40.md`) do not yet exist in the lane tree (checked via glob; other seats write them this wave). The used-by cells are per instruction regardless.
- No tool installed/upgraded; no network access or fetch performed (all reads were on-disk captures / committed files). Scratch at `/tmp/chousa-r45-ScribeRowsNormalize/` will be deleted on finish.
- No lane production files, git/jj state, fleet repo, or `merge/chousa` files were modified.
