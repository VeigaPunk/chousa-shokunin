# SimplifyTool — YAGNI review of tools/assimilate-rows.py (round 49, wave 2)

Target: `tools/assimilate-rows.py` (252 lines) at lane tip 87e93353…, sha256
`4b995dbc…` (byte-identical to the C1-measured file at 4ce61fc…; measure-after.txt:12).
Frozen counter: `corpus/evidence/round49/c1-count.py`. Scratch: `/dev/shm/chousa-r49-SimplifyTool`.
No installs (none needed; pacman paused). Production bytes untouched — lane tool sha before/after identical:

```
$ sha256sum tools/assimilate-rows.py
4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32  tools/assimilate-rows.py
```

## Callers / tests / contract survey

- `grep -r assimilate-rows` over the lane: only the frozen counter (subprocess
  invocation), `SKILL.md:130` (Gate row), `LOG.md:1800-1802`, `corpus/lessons/round-49.md:50,137`,
  and wave specs/reports under `.ufo/waves/round-49/`. No `tests/` suite, no `scripts/`
  wrapper, no `import` of this module anywhere (grep of `tools/*.py`, `corpus/evidence/*/*.py`
  shows no cross-import into it). The only live caller is `c1-count.py` via `--tool`.
- Section-10 contract: `.ufo/prompts/chousa-round-49.md:440-545` (this file's own docstring is
  its restatement). Binding clauses used below: by-document renumbering (489-491), scratch
  transform/validate, 0-3-space collision pattern (470-483), recheck/cell/`used-by`/status
  normalization (494-506).

## Candidate 1 — `by_url` dedup path (main, lines 190/195-196/201): KEEP

It maps a cited staged row whose URL equals another *cited* staged row's URL to that row's new
lane id (`held`), so one URL yields one lane id. This implements the docstring's named limit
(assimilate-rows.py:44-45) and §10's "the URL/anchor is the evidence and the id follows it"
(489-491); deleting it emits two lane ids for one document (census E04 class). It is dead on
the frozen fixtures — the counter's own `want` (c1-count.py:214-222) never dedups URLs, and no
frozen set cites two same-URL staged rows (pinned package has 10 duplicate-URL groups total,
but per set: A/B none, C groups {S097,S120} and {S111,S133,S181} have only one cited member).
So the counter cannot see this path. Verified:

- Variant `v1-nobyurl.py` (by_url removed, diff below): **C1=PASS** — passing the counter does
  not prove the deletion safe; the counter is simply blind to it (W1 F10, ExecDupUrl agreed).
- End-to-end behavior difference on a same-URL fixture (registry S001; staged S100/S101 both
  `https://dup.example/doc`, both cited): pristine `S100→S002 append, S101→S002 held`
  (`CITED=2 APPEND=1 HELD=1`); v1 `S101→S003 append` (`APPEND=2 HELD=0`). The v1 output appends
  two rows for one URL — the census-flagged duplicate the by-document rule exists to prevent.

Conclusion: not dead weight; required by the documented contract; keep.

## Candidate 2 — helpers mirrored from c1-count.py: KEEP (documented as frozen-oracle mirror)

Exact duplicates (tool : counter): regexes `GREP_RE` 56:68, `ROW_RE` 57:67, `TOKEN_RE` 58:69,
`RECHECK_RE` 60:70, `ESC_SPLIT` 59:71; functions `url_of` 65-73:78-89, `grep_ids` 76-77:118-119,
`num` 80-81:122-123, `staged_rows` 84-90:92-99, `registry_rows` 93-108:102-115. ~55 lines of
mirrored code. True dedup would require editing the frozen counter (forbidden). The import
alternative was tested:

- Variant `v2c-importshared.py` (imports the five regexes + five functions from c1-count.py via
  importlib.util, keeping local `LEAD_RE`/`DATE_RE`/`valid_date`/`write_ids`): **C1=PASS**.
- Rejected because the frozen counter's `registry_rows` was never updated with the W1 F2 tab-
  heading fix: on a `##\tRegistry` file the tool's version returns `['S007']`, the imported
  counter version returns `[]` (probe below) — the dedup would silently regress the landed
  4ce61fc fix and re-open the F2 E04/E12 hazard. It would also couple a permanent adopter to a
  round-49 evidence artifact. Duplication is the price of a frozen oracle that must mirror the
  tool; no deletion without touching the counter.

## No dead branches / unused imports

Scan of all 252 lines: every regex (incl. `LEAD_RE` 61, `DATE_RE` 62) and every function
(`valid_date`, `write_ids`) is reached from `main()`; all five imports (`argparse`, `datetime`,
`pathlib`, `re`, `sys`) are used; both parse passes (`grep_ids` whole-file for collisions vs
`staged_rows`/`registry_rows` for cells) implement distinct contract outputs. Only cosmetic
repeat: `set(reg_ids) & set(st_ids)` computed twice (154-155) — not a deletion.

## Evidence (commands verbatim)

Baseline (pristine copy; identical to measure-after.txt:10-21):

```
$ TMPDIR=/dev/shm/chousa-r49-SimplifyTool python3 corpus/evidence/round49/c1-count.py --tool /dev/shm/chousa-r49-SimplifyTool/pristine.py
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32
BASE_CENSUS=ok
SET_A … -> PASS
SET_B … -> PASS
SET_C … -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS        # rc=0
```

V1 (by_url removed):

```
$ TMPDIR=/dev/shm/chousa-r49-SimplifyTool python3 corpus/evidence/round49/c1-count.py --tool /dev/shm/chousa-r49-SimplifyTool/v1-nobyurl.py
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=dc2bdb2955b679d9d95e249727040b39c1c665a540a0babbf044a5e5e3029c79
BASE_CENSUS=ok
SET_A … -> PASS   SET_B … -> PASS   SET_C … -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS        # rc=0
```

V2c (helpers imported from the frozen counter):

```
$ TMPDIR=/dev/shm/chousa-r49-SimplifyTool python3 corpus/evidence/round49/c1-count.py --tool /dev/shm/chousa-r49-SimplifyTool/v2c-importshared.py
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=da7b61525f97ce49ec257ab32882d98dc071182f825c336df77a65e4ba81af45
BASE_CENSUS=ok
SET_A … -> PASS   SET_B … -> PASS   SET_C … -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS        # rc=0
```

(All set legs in every run printed `TOOL_EXIT=0 … -> PASS` with the same tallies as
measure-after.txt:14-16; only the header lines and final verdicts are repeated here.)

V1 diff (the only tested deletion):

```
@@ -187,18 +187,14 @@
             held.setdefault(u, sid)
     nxt = max((num(s) for s in base), default=0) + 1
     mapping: dict[str, tuple[str, str]] = {}
-    by_url: dict[str, str] = {}
     for sid in cited:
         u = url_of(staged[sid][1])
         if u in held:
             mapping[sid] = (held[u], "held")
-        elif u in by_url:
-            mapping[sid] = (by_url[u], "held")
         else:
             lid = f"S{nxt:03d}"
             nxt += 1
             mapping[sid] = (lid, "append")
-            by_url[u] = lid
```

Same-URL fixture behavior (pristine vs v1):

```
$ python3 pristine.py --staged dup/staged.md --knowledge dup/know --registry dup/reg.md --opened 2026-10-25 --out dup/out --entry corpus/knowledge/e.md
COLLISIONS=0
CITED=2 APPEND=1 HELD=1
$ cat dup/out/renumber.tsv
staged_id	lane_id	action	url
S100	S002	append	dup.example/doc
S101	S002	held	dup.example/doc
$ python3 v1-nobyurl.py … --out dup/out1 …
CITED=2 APPEND=2 HELD=0
$ cat dup/out1/renumber.tsv
S100	S002	append	dup.example/doc
S101	S003	append	dup.example/doc
```

Tab-header divergence (counter vs tool `registry_rows` on `##\tRegistry`):

```
tool registry_rows tab-header -> ['S007']
counter registry_rows tab-header -> []
```

Pinned-package duplicate-URL reachability (10 groups overall; per frozen set, none has two
cited members of one group — so by_url is unexercised by every counter leg):

```
staged duplicate-URL groups: 10
set A cited=[S087,S088,S089,S091,S092,S100,S101,S102,S103] dup-URL-groups-with-cited-member=[]
set B cited=[S082,S083,S090] dup-URL-groups-with-cited-member=[]
set C cited=[S097,S114,S130,S131,S133] dup-URL-groups-with-cited-member=[['S097','S120'],['S111','S133','S181']]
```

## Tradeoff

Keeping the two flagged pieces preserves §10's by-document identity and the frozen-oracle
mirror. The cost is ~55 mirrored lines and a counter-blind edge (by_url); the counter's
blindness is a coverage finding (W1 F10), not a reason to delete behavior the contract documents.
Scratch `/dev/shm/chousa-r49-SimplifyTool` removed after this report; lane tree untouched.

VERDICT: assimilate-rows.py YAGNI items (by_url dedup path; mirrored c1-count helpers) — holds
— both are contract-documented and the frozen counter cannot detect their removal, so no
deletion is warranted.
