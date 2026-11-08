# Search transparency — what a search record must report and how to record its sources (round 84)

source: S214, S018, S023
verified-at: 2026-11-08 (round 84; captures `a640b15abf781e5c583d7088`, `248b43277f376e437a356909`, `f5545a194c06ab421875b047`)
recheck: on-release

## What this entry governs

The lane's method searches sources, captures them, and registers what was found (`PROTOCOL.md` §4–§6). Held entries
say how a query is built (`search-query-exposure-r51.md`, `search-query-templates-r54.md`) and how a search log records
each attempt (`search-log-method-r39.md`, `search-tracking-record-r40.md`); none says what a *report of the search itself*
must contain so that a reader can audit it. PRISMA 2020's checklist states the reporting items for systematic-review
searches; a 2026 survey of evidence-based text generation states why linking output to supporting evidence matters; and
DCMI's metadata terms define the properties a record can use to name its source and its dates. The rows below keep only
what each quote states about reporting a search and recording its provenance; the checklist items for other review
sections are not taken.

## Located quotes

| qid | source | quote |
|---|---|---|
| Q1 | S214 | "Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies." |
| Q2 | S214 | "date when each source was last searched or consulted." |
| Q3 | S214 | "Present the full search strategies for all databases, registers and websites, including any filters and limits used." |
| Q4 | S214 | "Specify the methods used to decide whether a study met the inclusion criteria of the review" |
| Q5 | S214 | "Describe the results of the search and selection process, from the number of records identified" |
| Q6 | S018 | "aiming to link model outputs to supporting evidence to ensure traceability and verifiability" |
| Q7 | S018 | "Thereby, we focus on approaches that use citations, attribution, or quotations for evidence-based text generation." |
| Q8 | S018 | "However, the field is fragmented due to inconsistent terminology, isolated evaluation practices, and a lack of unified benchmarks." |
| Q9 | S023 | "A related resource from which the described resource is derived." |
| Q10 | S023 | "Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty." |
| Q11 | S023 | "range" |
| Q12 | S023 | "Date that the resource became or will become available." |
| Q13 | S023 | "Date on which the resource was changed." |

## Decision table

| Situation | Do | Never | Warrant |
|---|---|---|---|
| Reporting which sources were searched | name every database, register, website, organisation, reference list, and other source consulted | report only the sources that returned results and omit those that returned none | Q1 (S214) |
| Reporting when a source was searched | state the date each source was last searched or consulted | report the search without dating it, so the reader cannot tell how current it is | Q2 (S214) |
| Reporting the search method | present the full search strategy for each source, including filters and limits | summarize the strategy in prose when the full strategy can be stated | Q3 (S214) |
| Reporting how studies were selected | state the methods used to decide whether a study met the inclusion criteria | report the selected studies without the selection method | Q4 (S214) |
| Reporting the search outcome | describe the results from records identified to studies included, ideally with a flow diagram | report only the final count without the identification-to-inclusion path | Q5 (S214) |
| Linking a claim to its source | cite, attribute, or quote the supporting evidence so the link is traceable | assert a claim without linking it to the evidence that supports it | Q6, Q7 (S018) |
| Comparing evidence-based generation approaches | use a shared taxonomy and unified benchmarks rather than isolated evaluation practices | compare approaches that use different terminologies and metrics without noting the fragmentation | Q8 (S018) |
| Recording what a resource derives from | name the related resource from which the described resource is derived | record a resource without naming its source | Q9 (S023) |
| Recording when a resource changed | state the date on which the resource was changed | record that the resource changed without the date on which it changed | Q13 (S023) |
| Recording when a resource is valid | state the date or range of validity of the resource | record a validity period without its dates | Q11 (S023) |
| Recording when a resource became available | state the date the resource became or will become available | record availability without its date | Q12 (S023) |

## Inference (lane's, not stated by the sources)

For this lane a "search record" is a committed search log or report (`corpus/logs/`), a "source" is a registry row
(`SOURCES.md`), and a "claim" is a lane claim or entry row. Read that way, the rows describe practice the lane already
runs in part — searches are logged with query and result (`search-log-method-r39.md`), sources are registered with
status and dates (`SOURCES.md`), and claims cite `S-ids` and `Q-ids` (`claims.md`, entry decision tables). The sources
state none of this mapping; it is the lane's reading, to be tested by future rounds.

## Limits

- PRISMA 2020 is written for systematic reviews of intervention studies; the checklist items govern review reporting,
  not general web search. The rows keep only the search-transparency items (6, 7, 8, 16a); eligibility criteria,
  risk-of-bias, synthesis, and reporting-bias items are not taken.
- The S018 survey is about evidence-based text generation with LLMs, not systematic reviews; its taxonomy and metrics
  are for model evaluation, not for search reporting. The rows keep only the attribution/traceability motivation.
- DCMI's terms are general metadata properties; they define what `source`, `modified`, `valid`, and `available` mean,
  not when or how often to set them. The rows keep only the definitions; no freshness or verification policy is implied.
- Row 8's Never assumes the related resource can be named; when the source is unknown or unavailable, the row does not
  apply.
