# Round 49 W2 — ScribeFrontier: `## Sources & frontier` section body

Seat: ScribeFrontier (leaf, no subagents). All paths relative to the lane checkout
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. No tool installed (none expected; RULES.md read).
Base `414a2ec6…`; tip `4ce61fc…`.

## Census before/after

Command (run from the lane checkout):
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`

Observed output (exit code shown):

```text
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

Before-state (base `414a2ec6…`, from `git show 414a2ec6…:corpus/SOURCES.md`, pipe-row parse):
`BASE_ROWS 95`; `BASE_tier {'A': 89, 'B': 1, 'C': 5}`; `BASE_status {'mined': 71, 'queued': 19, 'rejected': 5}`. This equals the lesson's round-start census (`corpus/lessons/round-49.md:187-197`).

After-state (working-tree parse, same method): `ROWS 103`; `tier {'A': 92, 'C': 5, 'B': 6}`;
`status {'mined': 79, 'queued': 19, 'rejected': 5}`; also `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `103`.

## Rows added by tier

- A (3): S096, S097, S098 — `corpus/SOURCES.md:106-108` (CiNii manual, J-STAGE publisher page, J-STAGE FAQ).
- B (5): S099, S100, S101, S102, S103 — `corpus/SOURCES.md:109-113` (ERIC record, CNKI 他引频次 copy, journal data-spec copy, CNKI KNS8.0 guide, CNKI AI guide).
- All eight: `status=mined`, `opened=2026-10-25`, tiers/statuses parsed from the file directly.

## Rows touched old→new

None. `git diff 414a2ec6…..master -- corpus/SOURCES.md` → `10 insertions(+), 0 deletions(-)`; the ten added lines are the eight rows S096–S103, the Round-49 search-log bullet (`SOURCES.md:282`), and one blank. No pre-existing row's `status`/`recheck`/`used-by` changed between base and tip.

## Frontier rows advanced

No registry row changed, so the frontier advance is at the knowledge-entry level:
- Coverage map (`corpus/README.md`) gained two Round-49 entries: `knowledge/aggregator-vs-source-r36.md` (`README.md:1071`, binds `S096`–`S099`) and `knowledge/citation-count-semantics-r37.md` (`README.md:1072`, binds `S100`–`S103`); `README.md:1075` adds the `tools/assimilate-rows.py` row.
- `SOURCES.md:282` adds the Round-49 Search-log row: "Identified 2 candidate entries on the derived-index theme (9 staged documents), screened 9 documents, included 8 … excluded 1 (staged NCPSSD homepage row…)".
- `README.md` `## Frontier` (`:348`) carries no Round-49 paragraph; the last round disposition heading is `## Round32 frontier disposition` (`:972`).

## Assimilation

- Theme: **a citation index's data is a derived artefact** (source hierarchy: aggregator versus source) — `lessons/round-49.md:37`.
- considerthese proposal: `considerthese/2026-10-25.md:55-56` proposes "Report a capture-age line"; landed as QUALITY 71 with `corpus/evidence/round49/capture-age-check.py` (`lessons/round-49.md:173-181`).
- Section-10 collisions: `comm -12` over `reg-ids` (95) ∩ `staged-ids` (114) → 14 ids S082–S095 (artifact `.ufo/waves/round-49/assimilation/collisions`; counts 95/114 from the same dir). Guard proof (`.ufo/waves/round-49/assimilation/guard-proof/`): indented `  | S002 |` → `collisions` = S002 under the 0–3-space pattern; `collisions-col0` empty under the column-zero pattern.
- Renumber map: `.ufo/waves/round-49/assimilation/adopt-final/renumber.tsv` — S087→S096, S088→S097, S089→S098, S092→S099, S100→S100, S101→S101, S102→S102, S103→S103 (S100–S103 land on the same numbers by document, not by arithmetic; staged S091 NCPSSD refused before the run — `lessons/round-49.md:42-66`).
- Refused row: staged S091 NCPSSD homepage (`refused-doc: https://www.ncpssd.cn/`, `lessons/round-49.md:131`); no `ncpssd` registry row exists. Its capture is `76914d78c20094f677dea77d.raw`; the register verdict records both quotes verbatim only in the companion help-page capture `c4e1446a42d0a709c34097be` (offsets 24872/25269, `lessons/round-49.md:115-118`).

## Capture-age freshness

- Newest capture in `.qcache`: `50f8d9adb0d75b3c6ddefd3b.txt` — 2026-10-24 23:26:57 -03:00.
- This round's nine theme captures (URL→`sha256(url)[:24]` mapping, mtimes): 09fc63de 20:33:31, 167e9db7 20:33:32, fea98dc5 20:33:46, 76914d78 (NCPSSD homepage) 20:34:30, b539a802 20:36:56, 6dc68fd6 20:37:06, 7809d511 20:37:23, 02aefcf5 20:37:37, 32d1d24b 20:53:44 — all 2026-10-23, matching `lessons/round-49.md:178-180`. Help-page capture c4e1446a (S086 verdict) 2026-10-23 21:21:19.

VERDICT: Sources & frontier claims (census before/after, rows added by tier, no rows touched, frontier advance, assimilation line, capture-age freshness) — holds — every component re-derived from the lane's current files and commands matches the frozen round-49 record exactly.
