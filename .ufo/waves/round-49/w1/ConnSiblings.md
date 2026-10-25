# ConnSiblings — round 49 w1 sibling-overlap scan (chousa derived-index theme)

Seat: ConnSiblings (leaf; no subagents). Skill godspeed read (`skill://godspeed`); tooling RULES.md read (`/home/vgpnk/.omp/agent/RULES.md`). No tool install needed/recorded (none performed). No scratch left (`mkdir -p /tmp/chousa-r49-ConnSiblings && rmdir …` → `scratch-ok`).

## 1. Method and commands

Term set (case-insensitive): `CiNii|J-STAGE|CNKI|被引|他引|自引|self-citation|lateral reading|NCPSSD|citation count|derived list`.

The fleet-wide glob `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/**/*` did NOT expand (tool returned "No matches found"; same for `*-shokunin/PROVINCE.md`), so all scans used explicit per-lane paths (20 sibling lanes, chousa excluded).

Scan 1 — corpora, group A (kaidoku, souji, kasegi, kengaku, mori):
`grep -iE '<term-set>' /home/vgpnk/Projects/shokunin/{kaidoku,souji,kasegi,kengaku,mori}-shokunin/corpus/**/*`
Observed: hits only in kasegi and kengaku; kaidoku/souji/mori → 0.

Scan 1 — group B (tameshi, tabi, kama, mado, kumitate):
Observed: hits only in tabi, kama, mado, kumitate; tameshi → 0.

Scan 1 — group C (kotodama, kake, revenger, tsukuroi, kotoba):
Observed: hits only in kotodama, kake, kotoba; revenger/tsukuroi → 0.

Scan 1 — group D (lore, game-dev-2d, audio, game-dev-3d, kagi), paged (skip=20,40; 56 matching files total):
Observed: hits only in audio (all copies of `measure_audio.py`); lore/game-dev-2d/game-dev-3d/kagi → 0.

Scan 2 — `grep -iE '<term-set>'` over all 20 sibling `PROVINCE.md` (explicit paths):
Observed: **No matches found** (0/20).

Reads for context (each opened): kotodama/tabi/kama/kumitate/audio PROVINCE.md (full); kake/kengaku/kotoba/mado PROVINCE.md:1-90; kengaku `corpus/knowledge/attrib-prior-art-r21.md:158-172`; kotodama `corpus/knowledge/verification/internal-consistency-audit.md:19-33`; mado `corpus/lessons/round-35.md:243-257`; tabi `corpus/evidence/round-18/routed/adjacency-selftest.json:1-31`.

## 2. Corpus hits by lane (path:line — term matched; sense)

- **kasegi** — `corpus/lessons/round-8-aggregator-box3-coldrun.md:76` (self-citation; lesson self-citations cannot create context-leak rows). Lane-internal vocabulary, not index ground.
- **kengaku** — `corpus/evidence/round10-fleet/r10-critic.md:42,:72` (citation counts; quoted from the r9 freshness claim under audit); `corpus/evidence/round13-coverage/r13-planner.md:66` (citation counts; proposal language); `corpus/lessons/round-13-coverage.md:40` (stale-citation count), `:54` (61-live-citation count); **`corpus/knowledge/attrib-prior-art-r21.md:165-167`**: "Citation counts seen in search snippets … are relayed through search results, not independently verified — used above only as crowding color, never as grounding." Closest thematic neighbor (epistemic caution about citation-count provenance), inside a knowledge entry, not a province claim.
- **tabi** — `corpus/evidence/round-18/harm-at-measured.json:517`; `corpus/evidence/round-18/routed/adjacency-selftest.json:8,:22` (self-citation; `case tabi-ref-self-citation verdict=pass` selftest case label — test fixture, not index semantics).
- **kama** — `corpus/lessons/round-20.md:151` (citation count; receipt-count sentence "Citation count17/17").
- **mado** — `corpus/QUALITY.md:107` (literal vs semantic citation counters); `corpus/lessons/round-12-verifier-spotcheck.md:17` ("a citation count, not judgment quality"); `corpus/lessons/round-30-verifier-spotcheck.md:129` (self-citation attack fails to falsify); `corpus/lessons/round-31-verifier-spotcheck.md:47-50` (resolved-citation counter v2); **`corpus/lessons/round-35.md:250`**: "The check passes only on a derived list; it fails on the copied one." (M35-1: staging ids read from `ID-REMAP.md` `was` column, a superseded base — derived-list term, but about ID remaps, not citation indexes).
- **kumitate** — `corpus/lessons/round-12.md:128` (citation counts; member-completeness probe description).
- **kotodama** — `corpus/SOURCES.md:360` (CiNii; source row S331: NDL Search record "supplied through CiNii Books", DOI → 国書データベース); `corpus/knowledge/synthesis/worldbible-integration-contract.md:209` ("Bilateral reading" — substring false positive for `lateral reading`; actual text is about bilateral reading receipts); **`corpus/knowledge/verification/internal-consistency-audit.md:25`**: "a source's existence and citation count therefore do not verify what is attributed to it" (Greenberg BMJ 339:b2680 basis) — second closest thematic neighbor, inside a verification-audit entry; `corpus/knowledge/verification/to-verify-triage-protocol.md:62` ("Do not demand an arbitrary citation count"); `corpus/lessons/round-17.md:164` (self-citation closes the loop); `corpus/lessons/supplement-opencode-1/sources/color.json:7,:61-67,:97` (J-STAGE on-site search retrieval notes).
- **kake** — `corpus/knowledge/publish-queue.md:233` (citation count; "kake's citation count for `bounties` is now 1" — lane-internal cite-count statement with line-pin caveat).
- **kotoba** — `corpus/knowledge/corpus-integrity-round11.md:155` (commit-citation count vs baseline); `corpus/lessons/round-66.md:18` (live citation counts).
- **audio** — `corpus/fixtures/measure_audio.py:11688` and copies under `corpus/live/r82…r97/**` (e.g. `r82-simplifier/folded/measure_audio.py:11684`, `r97-verifier/mut/min-nop/corpus/fixtures/measure_audio.py:11686`) — "Only a LIVE node's citation counts" = module reference-count comment; semantically unrelated to bibliographic citation indexes.
- **Zero hits**: kaidoku, souji, mori, tameshi, revenger, tsukuroi, lore, kagi, game-dev-2d, game-dev-3d.

## 3. Do any sibling PROVINCE.md claim this ground? — No

- Term scan over all 20 sibling `PROVINCE.md`: 0 matches.
- Read provinces confirm no claim of "a citation index's data is a derived artefact" (or any citation-index/metadata ground). Several instead hand research method to chousa: kotodama `PROVINCE.md:19` ("general source-research method (chousa)"); kake `PROVINCE.md:36-37` ("chousa owns research method and source hierarchy"); audio `PROVINCE.md:53` ("research method (chousa)"); kumitate `PROVINCE.md:27` ("Research method → chousa"); kotoba `PROVINCE.md:51` (adjacency row: chousa | adjacent | "deep-research method; kotoba cites it, never re-derives it"). kengaku's refusal list (PROVINCE.md:22-41) covers model-serving plane, kagi, kumitate, kasegi, kotoba, kake — not citation-index ground.

## 4. Verdict

**NO OVERLAP** — no sibling lane's corpus or PROVINCE.md claims the derived-index ground (a citation index's data is a derived artefact); the only thematic neighbors (kengaku `attrib-prior-art-r21.md:165-167`, kotodama `internal-consistency-audit.md:25`) are epistemic notes inside knowledge entries of lanes whose provinces are eval/worldbuilding, and several siblings explicitly defer research method to chousa, so adopting the theme in chousa neither duplicates a held claim nor harms a sibling axis.
