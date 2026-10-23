# ScoutMistakeSweep33 — round-33 mistake candidates

Read-only. Base `2b9cc73aed30c2e2c95699db6617d9531ef49fb2`. `git diff --stat` of that commit against HEAD `3b528b9a` is empty for `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `corpus/lessons/round-32.md`, `corpus/lessons/round-32-verifier-spotcheck.md`, and `corpus/evidence/round32/c2-count-v2.py`. No counter was run. No install.

Sweep: `corpus/lessons/round-29.md` through `round-32.md` and their `*-verifier-spotcheck.md` Mistakes / routed-defect sections, plus `SCORECARD.md` capability and correction blocks. Five candidates. Each fix below is one that the current bytes already fail.

## 1. A frozen counter is met by a control after data

Class recurred. The prompt's triple is only two hits plus one neighbour.

| round | what met the frozen counter | when | counter then |
|---|---|---|---|
| 29 C1 | cache-only verifier, no network, `130/130` | after data | not redesigned (`corpus/lessons/round-29.md:94-97`) |
| 32 C2 | no-reader metadata control, `132/132`, `citation_source_open_count: 0` | after data (receipt utc 07:29Z, after candidate commit 07:25:26Z) | not changed (`corpus/lessons/round-32.md:54`; `corpus/lessons/round-32-verifier-spotcheck.md:32-35,72-75`) |
| 30 C2 | not this class | v4 controls' best is 18/27 (`SCORECARD.md:1704`). Post-data event is the landed tool at 26/27 on 3 of 44, counter not re-scaled (`corpus/lessons/round-30.md:33,108-109`; spot-check `:109`) | kept |

Cause that survived the fixes: each round's criterion names the channel that just leaked (page text; DNS/header shape, QUALITY 29) and not "any byte the fixture writes in class order". `c2-count-v2.py:200-256` calls `put_file` for R1/R2/R3 before every negative class; `:259-260` shuffles the record rows only. QUALITY 29's shown-to-fail example is the DNS-header control (`corpus/QUALITY.md:201-208`). That check stays green while `w2/CriticAxis32/control-metadata-s3232002{1,2}.json` score 132/132.

Captured-by: none before data (round-32 lesson `:54`). Round-29 pre-data wave and QUALITY 24/29 did not have this channel.

Fix that fails: "shuffle creation order, then the old control misses" (`round-32.md:54`; spot-check `:154-158` says the criterion is not yet shown able to fail). The shuffle is not in the committed generator, and the committed control still meets P2. A criterion that only re-scores that one script also fails the next channel (the record's `status` cell is still class-correlated; the lesson's own v1 row at `:52` was a different channel, duplicate findings, caught only because a seat tried it).

## 2. Current selftest sub-ranges disagree with the 241-case log

`SKILL.md:77-84` say `PASS (241 cases)`. That total matches the log. The sub-ranges do not.

Command: `git show 2b9cc73a:.ufo/waves/round-32/measure/post-falsify/selftest-f4731885.log` parsed for `^ok-case`. Result: 241 lines, numbers 1..241 monotonic, banner `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`.

- `SKILL.md:83` says metadata cases 137–154. The log has 78 `metadata-*` names, spanning 137–215, and 60 of them are outside 137–154 (155–208 and 210–215). Case 209 is `claims-registry-colon-deny`, also outside the verify-claims ranges in `:78`.
- `SKILL.md:79` lists chain cases 31–40, 43–44, and 229–232. Case 129 is `chain-fence-anchor`, which `SCORECARD.md:1323` cites as the round-23 capability. The registry row omits it.
- `SKILL.md:89-91` was updated so the paragraph is historical and the banner is 241, and it still says the round-25 final metadata range was 137–161. That sentence does not cover 162–215.

Captured-by: round-31 spot-check R4 (`corpus/lessons/round-31-verifier-spotcheck.md:220-222`) caught the bare `161 cases` sentence. It did not check sub-ranges. The landed historical note is that fix.

Fix that fails: marking the paragraph historical and setting the banner to 241. After that text, `:83` still says 137–154. Check: count `metadata-*` ok-case lines with number >154 in the log above. Observed 60, so the row fails.

## 3. SHONEN box 3 cites a superseded selftest tally

`SHONEN.md:9-10` points "instructions executable without oral context" at `bash tools/research-gate.sh --selftest` and `corpus/evidence/round25-measure-after.log`. The file exists (`git cat-file -e` at the base). Its holds line is:

`corpus/evidence/round25-measure-after.log:53` `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)`.

`SKILL.md:89-91` says that 154-case tally is checkpoint `d8c8cff`, the round-25 final was `PASS (161 cases, 0 skipped)`, and the current rows are 241. The round-32 spot-check (`:48`) passed box pointers because they resolve, and (`:174`) did not re-run `--selftest`.

Captured-by: none. The resolver check does not read the tally inside the file.

Fix that fails: "every pointer resolves". It passes for this path while the cited log's selftest line is 154, not 161 and not 241.

## 4. A passing fraction in the registry is not the frozen verdict

`SKILL.md:86` verdict map: `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` exit 0 for the round-30 C2 counter.

`SCORECARD.md:1697` verdict is **not met**: 26/27 on 3 of 44 fresh seeds. The correction at `SCORECARD.md:1725-1727` says the `27/27` capabilities pointer is not the frozen-predicate verdict (routed `corpus/lessons/round-30-verifier-spotcheck.md:165-168`). The same tree's Gates table still states 27/27 as the success line.

`SKILL.md:87` does the sibling thing for round 32: `EXEMPT_AUDIT_MATCH=132/132` exit 0, while `SCORECARD.md:1844` says that counter is met by a no-reader control, so no counter verifies the capability. The 132/132 map is the counter's exit contract, not a held claim; the 27/27 map is the one that contradicts a written miss.

Captured-by: QUALITY 26 (`corpus/QUALITY.md:181-188`) catches the adjective "live", not a bare fraction. The D1 correction fixed the capabilities row and left the Gates table.

Fix that fails: qualify adjectives and append a scorecard correction. `grep` of `SKILL.md:86` still shows `27/27` with no "not met".

## 5. `10f2fe12 ×18` — and the routed "20" — fail a header scan

`SCORECARD.md:1817` says committed C1 receipts on gate `10f2fe12` are ×18. Spot-check D2 (`corpus/lessons/round-32-verifier-spotcheck.md:159-162`) says a census finds 20 and the extra two are critic re-scores. Neither states a command that reproduces the count.

This seat's scan: `git grep -l -F APPEND_SERIALIZED 2b9cc73a -- .ufo/waves/round-32`, then keep JSON whose first 800 bytes contain both `"gate_sha256": "10f2fe12` and `"label": "APPEND_SERIALIZED=`. Result: **21** files, samples `APPEND_SERIALIZED=24/24`, `predicate_holds` true, counter `e6bf9531…`:

- `measure/after-c1-s3200{1,2}.json`
- `w2/CriticAxis32/candidate-c1-s32320001.json`
- `w2/CriticMistakes32/candidate-c1-v2-s323212.json`
- `w2/MutC1Gate/pristine-pristine-counter.json` and `restored-{a,b,c,d,e,f}-counter.json`
- `w2/NoHarmAfter32/c1-v2-s330{1,2}.json`
- `w2/RerunC1a/c1-s4400{1,2,3}.json`
- `w2/RerunC1b/rerunc1b-landed-fs.json`, `rerunc1b-landed-load{1,2}.json`, `rerunc1b-load{1,2}.json`

`rerunc1b-fs-tmpfs.json` is gate `f4731885`, not in the 21. `ReceiptCensus32/census-checks.json` mentions the sha and was not counted. Seeds were not de-duplicated. [INFERENCE] the spot-check's 20 drops one of the two load pairs; this seat did not find a rule in the spot-check that says so.

Captured-by: QUALITY 27 (`corpus/QUALITY.md:189-194`) already requires a stated re-run count to name committed receipts. It was applied to the round-29 "6 runs" sentence, not to this ×18.

Fix that fails: append "the count is 20" (D2's proposed correction). The header scan returns 21, so 20 fails the same way 18 does.

## Not candidates

- Round 31's pre-data wave did catch the shortcuts it ran (endpoint binder 120/120 on v1, 112/116/102 on v2). The post-data 120/120 fail-open case is a false "counter killed it" sentence, already QUALITY 33, not this class.
- Capability case pointers at `SCORECARD.md:600-602,674,731,1316-1323` match the 241-case log (86–92, 93–94, 95–98, 99–102, 103–106, 107–109 and 111, 112–116, 117–119, 120–122, 124, 125–128, 129, 130–133). The root-slash reconciliation that skips case 110 is right: 110 is `claims-root-dslash`.
- `LOG.md:455` Round 9 heading exists, so SHONEN box 2's pointer resolves. Box 4's `PROVINCE.md` path exists. Those were not disagreements.

## Limits

Did not re-run `--selftest` or any counter. The 21-file figure is a header scan, not `jq` over whole receipts, and not a distinct-seed count. The metadata 60-count is from the committed log, not a fresh gate run.
