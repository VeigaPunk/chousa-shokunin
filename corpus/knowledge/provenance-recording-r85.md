# Provenance recording — what a record must write to name its derivation, its generation and its provenance (round 85)

source: S215, S026, S031
verified-at: 2026-11-08 (round 85; captures `6e48bcc4a04d13b7b3ebb68e` via the W3C alternate URL,
`67983a3dbbd1d690aa648744` GO FAIR R1.2 opened this round, `11d6cc56bb24adfc61eea2b4` Schema.org lastReviewed
opened this round)
recheck: 365d

## What this entry governs

The lane's method records where a claim came from and when it was read (`SOURCES.md` rows carry a `source:`,
a `verified-at:` date and a `recheck:`). Held entries say how a search is reported (`search-transparency-reporting-r84.md`)
and how metadata headers look (`metadata-screen-r25.md`); none says what PROV-O, the FAIR R1.2 interpretation and
Schema.org stake out as the declarable facts of provenance itself: a derivation link, the times an entity stood,
the facets a provenance record must carry, and the date a reviewed content was last checked. The rows below keep
only what each quote states about naming a source and its dates.

## Located quotes

| qid | source | quote |
|---|---|---|
| Q1 | S215 | "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property." |
| Q2 | S215 | "A derivation is a transformation of one entity into another." |
| Q3 | S215 | "then we can say that the bar chart prov:wasDerivedFrom the dataset." |
| Q4 | S215 | "The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence." |
| Q5 | S026 | "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions" |
| Q6 | S026 | "using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit" |
| Q7 | S031 | "Date on which the content on this web page was last reviewed for accuracy and/or completeness." |

## Decision table

| Situation | Do | Never | Warrant |
|---|---|---|---|
| Naming what a resource derives from | form the provenance chain with the derivation property where the chain's entities are set | record a resource with no derivation link when the chain's entities are known | Q1, Q3 (S215) |
| Recording a derivation's direction | state the transformation from one entity into another | call two unrelated entities a derivation | Q2 (S215) |
| Recording the bounds of an entity's existence | state the generation moment and the invalidation moment that bound it | describe an entity as atemporal, with no generation or invalidation moment | Q4 (S215) |
| Recording a resource's provenance | state how the resource was generated, why it was generated, by whom, and under what conditions | ship data with no record of how it came to be | Q5 (S026) |
| Recording the source behind a resource | state the starting data or source resource, and who owns the data and should be given credit | omit the starting data, the owner or the credit from the provenance record | Q6 (S026) |
| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |

## Inference (lane's, not stated by the sources)

For this lane a "resource" is a `corpus/SOURCES.md` row or a `corpus/knowledge/` entry; `generatedAtTime` /
`invalidatedAtTime` motivate the `verified-at:` + `recheck:` pair, and R1.2's facets are the lane's Gate record
itself. The sources state none of this mapping.

## Limits

- PROV-O is a description of provenance relations, not a rule for when to re-verify a source. The rows take only
  the derivation and generation/invalidation terms.
- FAIR R1.2 is a foundation interpretation, not a W3C recommendation. The rows take only its provenance facets.
- Schema.org's `lastReviewed` is a publication-date-adjacent property, not a verification-policy date. The row
  takes only its definition.
