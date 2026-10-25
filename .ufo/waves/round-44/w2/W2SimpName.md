# W2SimpName — `citation-version-binding-r36.md` vs lane round 36

Seat: W2SimpName (simplifier, leaf). No production file written, renamed, or deleted. No fetch. No descendant. Claims not retuned.

## Verdict

YES. `citation-version-binding-r36.md` is a campaign path label, not a lane round number.

YES. Using that filename repeats the round-43 filename pattern (`search-log-method-r39.md` kept under a package suffix that is not the admitting lane round).

The words "campaign label" are this seat's question, not a sentence in the campaign files. Those files say "Campaign staging root" and "Merge package". Round 43's own words are "the package's label". Same path, two names. The suffix `-r36` is also not the campaign's round index. That column is `round1`.

## Axes

- Operability: R44-C3 and `c3-count.py` freeze the string `citation-version-binding-r36.md`. A rename fails that contract. Not done.
- Calibration: "campaign label" means the path the corpus-expansion campaign staged. It does not mean the campaign called the file a campaign label, and it does not mean the suffix equals campaign round 1 or lane round 36.
- Depth: the pattern is suffix ≠ admitting lane round, and a glob of `*-rNN.md` then mixes the staged name with notes the lane actually admitted in round NN. Stop before a second name.

## What the name is

The corpus-expansion campaign staged the path. It did not land it in the lane.

Campaign brief, `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/briefs/ScoutChousa.md`:

```
6:- Campaign staging root: /home/vgpnk/Projects/shokuknow
9:- Nobody writes into a lane repo. The campaign stages material for the lane owners.
```

Merge package head, `/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md`:

```
1:# Merge package — chousa
3:Staged by `corpus-expansion-1`. **Nothing was written into the lane repo.**
```

Measured row, same table: `citation-version-binding-r36.md` is `new-file`, round column `round1`, suffix `-r36`. The round-43 analog `search-log-method-r39.md` is `amendment`, round column `round4`, suffix `-r39`. All four campaign-round1 new files share `-r36`:

- `search-log-fields-r36.md`
- `citation-version-binding-r36.md`
- `aggregator-vs-source-r36.md`
- `source-type-taxonomy-r36.md`

The heading in `/home/vgpnk/Projects/shokuknow/lanes/chousa/KNOWLEDGE-PROPOSED.md` line 77 is `## corpus/knowledge/citation-version-binding-r36.md`. Its `ground:` line does not mention the filename. It uses `r2` and `r31` as lane-round shorthand for other notes:

```
ground: frontier item 2 — location binding and revision remain unverified; the lane's r2 `verify-claims` mode measures byte-span identity, and the r31 revision-binding note used W3C SRI, which authenticates bytes rather than dating a state
```

Phrase search of that proposed file, the merge report, and the staged knowledge copy: `campaign label` 0, `package's label` 0, `not a lane round number` 0. The campaign does not negate the suffix. The batch table does.

## What it is not

It is not a note lane round 36 admitted.

Command, lane root, exit 0 except the counter (exit 1, expected):

```
ls -1 corpus/knowledge/*-r36.md; echo '---LANE-FILE---'; if [ -f corpus/knowledge/citation-version-binding-r36.md ]; then echo PRESENT; else echo ABSENT; fi; echo '---README---'; rg -n 'citation-version-binding-r36|engine-swap-canary-r36|per-record-argv-attribution-r36' corpus/README.md || echo 'README_DONE'; echo '---LESSON36---'; rg -n 'citation-version-binding' corpus/lessons/round-36.md || echo 'LESSON36_NO_HIT'; echo '---GIT-NAME---'; git log --all --diff-filter=A --format='%H %ci %s' -- corpus/knowledge/citation-version-binding-r36.md; echo 'GIT_LOG_EXIT:'$?
```

Stdout:

```
corpus/knowledge/engine-swap-canary-r36.md
corpus/knowledge/per-record-argv-attribution-r36.md
---LANE-FILE---
ABSENT
---README---
1051:| `knowledge/engine-swap-canary-r36.md` | Round-36 note: fourteen swap/contract scenarios, four new separations (manifest hash shim, C-locale decode, pin echo isolation, drift token); the narrowed S7-S9 reading and the per-record attribution that keeps a no-call gate from scoring | `S070`; `evidence/round36/claims.md`; `.ufo/waves/round-36/measure/` |
1052:| `knowledge/per-record-argv-attribution-r36.md` | Round-36 note: the NUL-delimited argv witness separates the five output-equivalent engines per record, writes the channel outside the gate environment, and does not false-kill a renamed matcher; the recorded limits (global threshold, prefix-64 bypass) | `S069`; `evidence/round36/claims.md`; `.ufo/waves/round-36/measure/c2-*.json` |
---LESSON36---
LESSON36_NO_HIT
---GIT-NAME---
GIT_LOG_EXIT:0
```

`git log --all` printed no commit. Exit 0 with an empty log is "never added on a ref this command sees", not a missing check.

The two Round-36 notes were added in lane round 36. That tree does not contain this filename.

```
git log --diff-filter=A --format='%H %ci %s' -- corpus/knowledge/engine-swap-canary-r36.md corpus/knowledge/per-record-argv-attribution-r36.md
```

```
76597487c8c3f963465cdbcfcabe91acd1ea2500 2026-10-23 18:38:20 -0300 round-36: engine-swap canary 14/14 (4 new separations) + per-record argv witness 5/5 (renamed passes), frontier S069-S070, QUALITY 50-52, lesson, wave-1 evidence, errata 1-13
```

```
git ls-tree -r --name-only 76597487c8c3f963465cdbcfcabe91acd1ea2500 -- corpus/knowledge | rg 'r36|citation-version'
```

```
corpus/knowledge/engine-swap-canary-r36.md
corpus/knowledge/per-record-argv-attribution-r36.md
```

`corpus/README.md` labels those two "Round-36 note" and has no row for `citation-version-binding-r36.md`. Lane index convention is suffix = admitting round. This suffix would be read under that convention. The admitting round for this path has not happened. Lane round 36 already spent `-r36` on two other files.

Default C3, because the entry is not in the lane:

```
python3 corpus/evidence/round44/c3-count.py; echo EXIT:$?
```

```
ENTRY_CITES=0/1
QUOTE_LOCATED=0/1
URL_MATCH=0/1
C3=FAIL entry-missing
EXIT:1
```

That is the frozen do-nothing control (`claims.md`: a missing entry prints `C3=FAIL entry-missing` and exits 1). It is not a claim failure to retune.

## Round-43 pattern, and the repeat

Round 43 kept a package filename whose suffix is not the lane round that admitted it.

`corpus/lessons/round-43.md` line 33:

```
`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label.
```

That lesson does not say "not a lane round number" (count 0). The admitted entry does, `corpus/knowledge/search-log-method-r39.md` line 6:

```
The filename is the package's label, not a lane round number.
```

The file was added in lane round 43 (`737f40b6aa8f37ffe2269db370fd6d65a720d9a8`, 2026-10-24), while `corpus/README.md` lines 1057–1058 still call `capture-bash-pin-r39.md` and `receipt-verifier-subject-r39.md` "Round-39 note". A glob of `corpus/knowledge/*-r39.md` lists the package path between those two notes. Round-43 C3 froze that path string. The seat that measured this (`.ufo/waves/round-43/w1/SimpFilename.md`) did not rename it.

`citation-version-binding-r36.md` is the same shape:

| | round 43, landed | this filename, not landed |
|---|---|---|
| Path | `corpus/knowledge/search-log-method-r39.md` | `corpus/knowledge/citation-version-binding-r36.md` |
| Who minted the suffix | merge package, campaign round4, kind `amendment` | merge package, campaign round1, kind `new-file` |
| Suffix vs campaign round index | `-r39` ≠ round4 | `-r36` ≠ round1 |
| Suffix vs lane round that admits it | `-r39` ≠ lane round 43 | `-r36` ≠ lane round 44 (and ≠ lane round 36) |
| Collision if placed in `corpus/knowledge/` | two README "Round-39 note" files | two README "Round-36 note" files |
| What freezes the string | round-43 C3 and the S078 used-by cell | `corpus/evidence/round44/claims.md` line 77; `c3-count.py` lines 24 and 58 |

Using the filename repeats the pattern. The repeat is the name, not an already-admitted file.

The assimilation draft already copies the round-43 entry sentence and still keeps the campaign name. Draft only, `.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md` line 6:

```
The filename is the package's label, not a lane round number.
```

Phrase counts in that draft: `package's label` 1, `not a lane round number` 1, `campaign label` 0. The draft does not contain its own filename. The path does. That draft is not `corpus/knowledge/`, and C3 does not read it.

## What does not repeat yet

- The file is absent. Round 43 had already committed the analog. This round has not.
- Merge kind differs: `new-file` here, `amendment` there. The merge note on the r39 row says the target already existed. This row says `new file`. The filename pattern does not depend on that column.
- No production lesson for round 44 states either sentence. `corpus/lessons/round-43.md` does not mention this path (count 0). A lesson that later says only "the package's label" would repeat the round-43 disclosure gap. A lesson that also says "not a lane round number" would match the entry, not the lesson.
- Campaign round3 and round5 suffixes are mixed (`-r3`, `-r37`, `-r38`, `-r39`, `-r40`). Do not treat `-r36` as a formula `campaign_round + 35`. The measured fact used here is the round1 batch: four new files, one suffix, round column `round1`.

## Tradeoff

Keeping the campaign path preserves the frozen C3 string and the package's path identity. Cost: the suffix still sorts with lane round 36, and neither the campaign copy nor `claims.md` says so. Renaming would improve the name axis and fail `c3-count.py` line 58 (`"citation-version-binding-r36.md" in row`) and the entry-path constant on line 24. Not done. No second filename proposed.
