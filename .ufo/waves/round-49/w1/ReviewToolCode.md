# ReviewToolCode — line review of tools/assimilate-rows.py @ 65940928 (round 49 w1)

Scope: tool vs addendum §10 (/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-49.md:440-545)
and the frozen interface (corpus/evidence/round49/c1-count.py docstring). Tree == commit verified:
`git show 65940928:tools/assimilate-rows.py | diff - tools/assimilate-rows.py` → empty; sha256
3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6. Frozen-counter baseline:
`python3 corpus/evidence/round49/c1-count.py` → SETS_PASS=3/3, GUARD PASS, PIPE PASS, **C1=PASS**.
Census oracle: gawk row_pass/usedby_findings + url_of extracted verbatim (sources-census.sh:600-605).
All fixtures in /tmp/chousa-r49-ReviewToolCode (deleted after). No installs (none needed).

## F1 HIGH — lane: adopt/ scratch is stale vs the working registry (append-time hazard; not tool code)
Lane adopt/renumber.tsv maps all 9 cited staged ids `append` S096..S104 (registry max was S095 at
scratch time). The working tree now carries 8 UNCOMMITTED registry rows S096..S103 holding 8 of
those URLs: `git diff --stat -- corpus/SOURCES.md` → "1 file changed, 10 insertions(+)";
`git diff -- corpus/SOURCES.md | grep -cE '^\+\| S[0-9]'` → 8; last registry row S103; S104 absent.
Fresh tool run on the current registry (command per frozen interface, both set-A entries):
`→ CITED=9 APPEND=1 HELD=8`: S087→S096 held, S088→S097 held, S089→S098 held, **S091→S104 append**,
S092→S099 held, S100→S100 held, S101→S101 held, S102→S102 held, S103→S103 held.
If the scratch outputs are landed as-is: (a) scratch append.md re-creates ids S096..S103 → census
E03 duplicate id ×8 (+E04 same URLs); (b) adopt/corpus/knowledge/aggregator-vs-source-r36.md:7
cites `S099 — https://www.ncpssd.cn/` but S099 is now the ERIC lateral-reading row
(eric.ed.gov/?id=EJ1372738) — wrong document; (c) adopt/.../citation-count-semantics-r37.md:7
cites `S104 — library.um.edu.mo/…pdf` but that PDF is S103 now and S104 will be ncpssd.
Fix: regenerate at append time from a fresh tool run (deterministic); ncpssd is the only genuine
append (S104). This is §10's own drift warning ("the lane registry keeps moving") materialized.

## F2 MED — `##\tRegistry` / `#\tX` headers invisible to registry_rows (space-only literals)
registry_rows (tools/assimilate-rows.py:95,98) uses startswith("## ")/("# "); the census accepts a
tab after the hashes (gawk `/^ {0,3}##[ \t]/` sources-census.sh:609; bash heading_re `[[:space:]]`
sources-census.sh:540). Repro (tab header; registry row S007 holds the staged URL):
`tool → renumber.tsv: S050 S001 append held.example/a` (space-header control: `S050 S007 held`);
mirror census → `file E04 S001 duplicate url held.example/a within scope s` (control: rc 0, ok).
So a tab header hides held rows → duplicate append (E04) and resets `nxt` to S001 (non-contiguous
from the true max S007). Same root cause on the H1 reset: after `#\tOther` the tool still treats
rows as inside Registry (held S060→S008) where census flags that row `E12 row outside Registry
section`. Latent today: `grep -cP '^ {0,3}##\t' corpus/SOURCES.md` → 0.

## F3 MED — recheck reduction passes calendar-invalid ISO dates (census E09)
RECHECK_RE (tools/assimilate-rows.py:56) is shape-only; census epoch-validates ISO rechecks
(sources-census.sh:663-667). Staged rechecks `2026-13-45`, `2026-02-30`,
`2026-13-45 — re-verify upstream`, control `Recheck after next sync` → tool rc=0; appended rows
keep 2026-13-45 / 2026-02-30 verbatim with NO stripped record (RECHECK_RE "matched"); the reduction
path logs stripped prose but keeps the invalid leading date. Mirror census:
`E09 S002 recheck=2026-13-45 · E09 S003 recheck=2026-02-30 · E09 S004 recheck=2026-13-45`.
Control → no E09: the symbolic class is byte-identical to census `symbolic()`
(sources-census.sh:582), so only calendar-invalid ISO (also y==0) slips through. One such row fails
the round-end `validate --root` gate.

## F4 LOW — url_of not byte-exact when a Unicode space abuts the URL
Differential vs the census's own url_of (verbatim gawk extract), 24 vectors: 21 identical
(host-case, trailing-slash, fragment order, two-urls, port, empty-authority, scheme-only…). 3 diffs:
`nbsp-after tool='example.com/A' census='example.com/A\xa0page'`; `nbsp-inside …/A\xa0page/end`;
`nel tool='example.com/a' census='example.com/a\x85b'`. Python `\s` stops at U+00A0/U+0085; gawk
`[^[:space:]|]` continues through their UTF-8 bytes → held-detection on such a cell diverges from
the census's own identity → possible E04. Latent (real package cells are ASCII-space).

## F5 LOW — ESC_SPLIT lookbehind disagrees with the census cell split on `\\|`
ESC_SPLIT (tools/assimilate-rows.py:55) treats `\|` as escaped even when the backslash is itself
escaped. Fixture S056/S057 (`a \\| b` in teaches / source): tool ESC_SPLIT cells=11; `gawk -F'|'`
NF=14 → 12 cells. Appended rows are still census-clean (rewrite `\s*\\?\|\s*` removes every pipe;
mirror census rc 0), so latent — but the 11-cell gate is weaker than the census parse and
cell-indexed extraction (source/used-by) can mis-split on such rows.

## F6 LOW — --opened only shape-checked
`--opened 2026-13-45` → rc 0, appended row `… | mined | 2026-13-45 | 30d | …` → mirror census
`E08 S002 opened=2026-13-45`. DATE_RE (:58) mirrors census shape but not epoch validity/≤today.
Operator-input class; the counter passes a real date.

## F7 LOW — --out overlapping --knowledge mutates the tool's own input
Docstring claims "Read-only on its inputs". `--out $KNOW` → rc 0 and the entry file was rewritten
in place (sha256 changed; `source: S050` → `source: S002`). No guard against out∩input overlap.

## F8 LOW — non-UTF8 input crashes instead of refusing
Staged file with byte 0xE9 → `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 …`, rc 1 via
traceback (not a clean REFUSED line). The gawk census handles bytes.

## F9 INFO — duplicate staged id: first row wins silently
Staged S050 twice (different URLs) → tool uses the first row's URL, no refusal, second ignored
(renumber shows `first.example/p` only). Census never sees the second; no gate failure.

## F10 INFO — frozen-counter gap (not a tool defect): same-URL staged rows
Counter `want` (c1-count.py:214-222) allocates a NEW id per cited staged row without URL dedup; the
tool dedups (`by_url` → second row `held`, tools/assimilate-rows.py:168-179). Via the counter's own
check_set on a 2-row same-URL fixture: `SET_DUPURL TOOL_EXIT=0 CITED=2 APPEND=1/2 HELD=0/0
BY_DOC=1/2 … CENSUS=ok -> FAIL` — while the tool's block passes the census (rc 0). Appending BOTH
(the counter's expectation) would be E04. Frozen fixtures don't exercise this; a future leg edit
could fail a census-correct tool.

## Checks that held
- url_of: 21/24 differential vectors byte-identical (host-case, fragment/slash order, first-URL,
  scheme-strip, port, `https:///path`).
- grep_ids == §10 grep pipeline byte-for-byte on real registry AND staged package (REG_IDS_MATCH,
  STAGED_IDS_MATCH; COLLISIONS=22 = S082..S103).
- Escaped-pipe rewrite end-to-end: `\|` cells → ` / `, appended rows parse as 11 cells, mirror
  census rc 0 (PIPE-leg parity reproduced independently).
- used-by exactness: users computed from ORIGINAL entry texts; single simultaneous substitution
  (no S100→S101→S102 chaining); counter USED_BY n/n on all sets.
- Held-row behaviour: space-header control held S007; real set C 2/2 held; held used-by not widened
  (documented named limit).
- Write scope: happy + refusal paths create files only under --out (find-diff over a sandbox);
  `--entry ../x` and `/abs` refused rc 2; recheck refusal exits 1 before any entry/append write.
- recheck symbolic class identical to census symbolic(); NNd class identical (`[0-9]+d`).

## Residual risk / verification gaps
- Tool does not pre-check kind/tier/scope vocab (E05/E06) — §10's normalization list doesn't ask it
  to; the mirror census gate catches.
- Counter crashes (ValueError on max()) over a sectionless registry — counter-side, frozen,
  untriggered on the real base (tool guards with `default=0`).
- F1 must be re-checked at append time: the registry is moving; regenerate, never reuse adopt/
  outputs.
- I did not run or judge the lane's append itself (out of seat).

VERDICT: attacked the frozen C1 adopter line-by-line with census-oracled fixtures — counter green,
grep/url_of/pipe/used-by/held/write-scope hold; found 1 high lane-process defect (stale adopt/
scratch vs working registry: landing as-is → E03×8 + two mis-cited entries) and 2 census-divergence
defects (tab headers, calendar-invalid recheck) plus 5 low/info; no frozen predicate touched.
