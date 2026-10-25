# ExecGateReproduce — round-49 w2: reproduce the Gate's scratch facts

Seat: ExecGateReproduce (leaf). Item attacked: the four scratch facts the round-49 Gate rests on —
section-10 collision sets, the guard proof, the `adopt-final/` tool run, and the lesson's renumber
and stripped tables. No frozen predicate, target or counter is proposed for change; sole write is
this report. Lane checkout `87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0` (tracked code at
`4ce61fc5`); base registry read from `414a2ec6`; staged package
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` (read-only, sha256
`a6dec4a0086d3cf7…`). Scratch `/dev/shm/chousa-r49-ExecGateReproduce` (`TMPDIR` exported for the
tool's `tempfile` use), deleted before finish. `RULES.md` read; no install, no pacman transaction,
no network.

## 1. Section-10 collision commands

```
$ git show 414a2ec6:corpus/SOURCES.md | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]{3,}' | sort -u > $S/reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/merge/chousa/SOURCES.append.md | grep -oE 'S[0-9]{3,}' | sort -u > $S/staged-ids
$ comm -12 $S/reg-ids $S/staged-ids > $S/collisions
  95 reg-ids · 114 staged-ids · 14 collisions
$ diff $S/reg-ids .ufo/…/assimilation/reg-ids      → IDENTICAL
$ diff $S/staged-ids .ufo/…/assimilation/staged-ids → IDENTICAL
$ diff $S/collisions .ufo/…/assimilation/collisions → IDENTICAL
S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095
```
reg-ids contiguous S001–S095 (`nums==range(1,96)` → `True`); staged ids S082–S195, monotone.
Lesson `corpus/lessons/round-49.md:44-48` reproduced exactly.

## 2. Guard proof

Fixture rebuilt from the lesson's description (not copied): `## Registry` + `| S001 | a |` +
`  | S002 | b |`; staged `| S002 | c |`, `| S003 | d |`.
```
0–3-space pattern:  collisions=[S002]   reg-ids=[S001 S002]
column-zero pattern: collisions=[]      col0-bytes=0   reg-ids-col0=[S001]
$ python3 tools/assimilate-rows.py --staged $S/guard2/staged.md --knowledge $S/guard2/empty \
    --registry $S/guard2/registry.md --opened 2026-10-25 --out $S/guard2/tool
COLLISIONS=1  exit=0  tool reg-ids=[S001 S002] collisions=[S002]
```
So the lesson's guard claim (`round-49.md:48-51`) holds, and the tool's own `GREP_RE`
(`tools/assimilate-rows.py:13`) is the same 0–3-space pattern — the proof tests the mechanism the
append run actually uses, not a shell look-alike. My rebuilt `reg-ids/staged-ids/collisions/`
`reg-ids-col0/collisions-col0` are byte-identical to `.ufo/…/assimilation/guard-proof/` (5/5 files).
Completeness probe: `any-indent` count == 0–3-space count on both real files (95 and 114), zero
tab-led and zero 4+-space row-shaped lines — the pattern loses nothing on these two files.

## 3. `adopt-final/` reproduced

Recipe as the lesson states it (`round-49.md:51-52`): staged aggregator entry **minus its S091
`source:` line** + staged citation-count entry, base registry.
```
$ grep -v '^source: S091 — ' …/knowledge/corpus/knowledge/aggregator-vs-source-r36.md > $S/kin/corpus/knowledge/…
$ cp …/citation-count-semantics-r37.md $S/kin/corpus/knowledge/
$ python3 tools/assimilate-rows.py --staged …/SOURCES.append.md --knowledge $S/kin \
    --registry $S/base-SOURCES.md --opened 2026-10-25 --out $S/out \
    --entry corpus/knowledge/aggregator-vs-source-r36.md --entry corpus/knowledge/citation-count-semantics-r37.md
COLLISIONS=14
CITED=8 APPEND=8 HELD=0        exit=0
```
All seven outputs byte-identical to `.ufo/waves/round-49/assimilation/adopt-final/`:
```
592b8fdf… append.md      6b2ade16… renumber.tsv   32da1a76… stripped.tsv
b0febed8… aggregator-vs-source-r36.md   68a8db1a… citation-count-semantics-r37.md
reg-ids, staged-ids, collisions: IDENTICAL
```
(`68a8db1a…` is the entry hash `ReviewProvince.md:5` records.) Map reproduced: S087→S096,
S088→S097, S089→S098, S092→S099, S100–S103 unchanged by document, all `append`, `HELD=0`.

## 4. Lesson tables vs the files

Parsed `round-49.md` tables programmatically and compared cell-by-cell:
```
renumber lesson/file rows: 8 8  MATCH      (staged id, lane id, https:// + renumber.tsv url)
stripped lesson/file rows: 19 19 MATCH     (lane_id, column, stripped — verbatim incl. "(ran 2026-10-23)")
```
Strip completeness re-derived from the staged rows: the 8 cited rows are `status=mined` already
(no status strip), `opened=2026-10-23` (8 strips), recheck leads `180d/90d/90d/365d/180d×4`
(8 strips), and S101/S102/S103 carry a two-entry staged `used-by` (3 strips) → 19 = 8+8+3. No
cited row contains a literal or escaped pipe inside a cell (`pipe_inside=False` ×8), so no
`cellN-pipe` strip is missing. The 19-row table is complete.

Disclosure exactness (adopt-final rows vs landed `corpus/SOURCES.md` S096–S103, header at
`corpus/SOURCES.md:9`): differences are `anchor` on all 8 rows and `teaches` on S101 only; the
other nine cells of every row are equal. That is precisely the lesson's sentence at
`round-49.md:134-137` — not a wider rewrite.

## 5. Probes beyond the recorded facts

- **Refusal is human, not tool-enforced (measured).** Deleting only the staged S091 *row* and
  leaving the entry's source line: `COLLISIONS=13 CITED=8 APPEND=8 exit=0`, the *same*
  renumber/append block, but the emitted aggregator keeps
  `source: S091 — https://www.ncpssd.cn/ …` — and lane S091 is CFEVER
  (`$S/base-SOURCES.md:101`). The tool passes a token through when its staged row is gone, so
  `round-49.md:51` "NCPSSD refused before the run" is true only of the entry-line deletion the
  operator performed; the tool cannot distinguish the two preparations.
- **`adopt-final/corpus/knowledge/*` is renumbering evidence, not an adoptable entry.** The
  mechanical rewrite keeps staged text: `adopt-final/corpus/knowledge/citation-count-semantics-r37.md:10`
  still reads `… (S076)`, and lane S076 is the GNU `sed(1)` manual (`base-SOURCES.md:86`); the
  aggregator's `recheck:` still says "re-open the five URLs … and the NCPSSD item 7" after the
  fifth source line was deleted. Landed entries have 0 `S076` and re-point by document to S096
  (`corpus/knowledge/citation-count-semantics-r37.md:11,45,52,75`) — the erratum/lesson disclosure
  is accurate. Risk only if a closure seat copies that directory.
- **Row-head ids ≠ referenced ids.** The staged file carries 118 distinct `S###` tokens against
  114 row-head ids; the four non-staged tokens are `S003 S009 S075 S077`, all passed through
  unchanged (the by-document error class `w1/ExecToolMoreSets.md:41-45` measured). None is in the
  two adopted entries except the held `S003` (SIFT), which the entries use correctly.
- Landed registry row count 103 (`grep -cE`), matching the lesson's `## Census` 95 → 103.

## Risks / calibration

1. The four scratch facts are reproducible byte-for-byte from the stated inputs; nothing in them
   is stale, arithmetically fudged or unreproducible. The Gate's *scratch* layer is sound.
2. The one soft spot is provenance, not arithmetic: `adopt-final/` mixes renumbering evidence with
   un-adoptable staged entry text, and the refusal that shaped the map is an operator edit. Both
   are disclosed in the lesson, but only in prose a reader must join across sections.
3. Not in this seat and not checked: counter replays (C1/C2), span/quote grounding, registry
   re-opens, the post-freeze `build-spans` change.

VERDICT: round-49 Gate scratch facts (collisions 95/114/14, guard proof, adopt-final byte-for-byte reproduction, lesson renumber/stripped tables) — holds — every recorded fact reproduced exactly from the stated inputs, with the refusal step shown to be an operator edit the tool cannot enforce and `adopt-final/`'s entry text shown to be staged residue rather than adopted text.
