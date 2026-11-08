# R95ConnectorSiblings — cross-lane pattern scan (round 95, read-only)

Seat `R95ConnectorSiblings`, lane `chousa`, round 95. Attacked tree: carrier `C`
`d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1` (shared clone, not repacked). Frozen claims read first:
`chousa-shokunin/.ufo/waves/round-95/claims.md` and `plans/round-95.md`.

Scope: `/home/vgpnk/Projects/shokunin/*-shokunin/` (all 20 sibling lanes, `chousa-shokunin` excluded from the
sibling side and included only as the subject). Three patterns, as assigned:

1. a tool that re-runs a recorded search/grep expression and compares counts;
2. a knowledge entry or SOURCES row holding PRISMA-S;
3. a search-record format with `hits`/`hit_set` columns.

Every command below ran read-only from `/home/vgpnk/Projects/shokunin`; nothing in a sibling lane was written.
Scratch `/fast/scratch/hyaku/chousa-r95/R95ConnectorSiblings` (deleted before yielding). No tool installed or
upgraded (nothing needed). `grep` is GNU grep 3.12 as `/usr/bin/grep` throughout.

## OVERLAPS=5

- **P1 — tool that re-runs a recorded expression and compares counts: 3 overlaps** (tameshi `count-recheck`;
  kagi `recheck-replay`; kagi `drift-pins COUNT`). The *core* mechanism of C1's revision leg is not new in this
  fleet: two sibling lanes already hold standing, selftested instruments that re-execute a recorded command at a
  named revision and compare the printed count, exiting non-zero on a mismatch. C1's *record form* (one Markdown
  `## Searches` table: glob scope, expression bytes, revision, date, hits and hit set, re-run over a second tree)
  is not held by any sibling.
- **P2 — PRISMA-S held in a sibling knowledge entry or SOURCES row: 0 overlaps.** PRISMA-S occurs fleet-wide only
  inside `chousa-shokunin` (306 files) and in three sibling wave receipts that are passthroughs of chousa's own
  files or captures (below). No sibling `corpus/SOURCES.md` carries a `PRISMA` row (0 rows across 20 lanes).
- **P3 — search-record format with `hits`/`hit_set` columns: 2 overlaps** (a literal `hit_sets_identical` field in
  a mori wave result; three narrative `| search | count |`-shaped report tables). No sibling holds a *committed,
  machine-verified* record format with those columns; the shape is common prose, the format is chousa-only.

### P1 items

| # | path | what it does | same mechanism as C1? |
|---|---|---|---|
| 1 | `tameshi-shokunin/tools/count-recheck.py` + `tools/count-recheck.json` (new r70, commit `3af968fa136e0fe212644cd3652731532cf1d5b0`, 2026-11-02; registered `SCORECARD.md:259,4090,4115`) | manifest row pins a record path at `record_rev`, the byte span carrying a printed integer, and the counting command `git grep -c [-E] <pattern> <rev> -- <path>`; re-runs it against git objects at the named rev and prints `COUNT_ROW <id> expect=<e> printed=<p> measured=<m> ok|MISMATCH`, exit 1 on unexpected; whole manifest resolved up front; selftest 6/6 | **Same core, narrower surface.** The revision-pinned re-execution + printed-count comparison + non-zero exit (C1's `COUNT_DRIFT`) is already enforced here. Differs: git-object blob, one path and one pattern per row, no glob scope, no hit set, no tree leg, no record table, and drift can be a *declared* red arm (`expect=drift`) rather than a refusal. |
| 2 | `kagi-shokunin/corpus/recheck-replay.py` (r56, last commit `9cbe9d5f803de2518d4c11c6bc6b9a585e5120ad`, 2026-11-07; in `SKILL.md:49`, booked as C1 capability acquisition at `SCORECARD.md:1861`) | replays every stated `recheck:` clock (`curl <flags> <url> \| grep -c '<BRE>'` → N, plus pdftotext/locate forms) offline with the fetch replaced by a committed capture and the filter stages run unchanged; `MATCH`/`MISMATCH`, `RECHECK_REPLAY: CLEAN|DRIFT`, exit 1 on any mismatch; selftest `PASS (20 cases)` | **Same class** (replay a recorded expression, compare the count it recorded), different object: a fetch clock over a capture, count only (`stated=%d replayed=%d`), no revision pin, no set comparison, no second tree. |
| 3 | `kagi-shokunin/corpus/drift-pins.sh` (`COUNT` verdict, `path:#<pin>->#<actual>`) | pins a grep count per symbol file in `corpus/drift-symbols.tsv` and reports `COUNT` drift | **Adjacent only.** Count pinning on one host file, no expression record, no revision, no set. |

Adjacent measurement, not a tool: `mori-shokunin/.ufo/waves/round-48/w1-results.json` (commit `e4dfff32…`,
2026-10-25), seat `ExecPortability`, recorded `count_at_entering_tip=395`,
`count_at_previous_round_entering_tip=395`, `hit_sets_identical=True`, with the commands
`git ls-tree -r --name-only <rev> -- tools/ .ufo/waves/round-*/ | grep -E '\.(py|sh)$'` and
`cat <files> | xargs git grep -l -F '/home/vgpnk' <rev> --`. That is C1's *set leg* (grep at a named revision →
file hit set → compare) executed ad hoc, once, inside a wave receipt. Also adjacent:
`kotodama-shokunin/reports/round-27/audit/x64-cold-rerun.py` separates a baseline revision from a clone's
revision for a `grep -rln` sweep — the same two-revision split C1 uses for `TREE_CHANGED`.

### P2 items

`/usr/bin/grep -rln --include='*.md' … "PRISMA-S\|jmla.2021.962" *-shokunin/` → 309 files: 306
`chousa-shokunin`, 1 each in `tsukuroi`, `kasegi`, `kake`. All three sibling files are wave receipts that quote
chousa's own bytes, not sibling holdings:

- `kasegi-shokunin/.ufo/waves/round-33/wave1/ConnSibling.md:57` — cites `chousa-shokunin/corpus/knowledge/cnki-citation-check-r40.md:6`.
- `kake-shokunin/.ufo/waves/round-92/w1/ConnectorScope/receipts/query-stale.txt:24` — a search receipt line naming
  `chousa-shokunin/corpus/knowledge/chinese-prisma-s-reception-r52.md:6`.
- `tsukuroi-shokunin/.ufo/waves/round-88/w1/ConnectorOverlap/pat-unified_kernel_uki_b___efi_b_EFI__.txt:18` — one
  grep-hit line from `corpus/captures/c9d1e74c3ac8d9eb332c9770.raw:420` of chousa's own corpus.

Sibling `SOURCES.md` rows containing `PRISMA`: 0 (20 lanes). C2 therefore duplicates no sibling knowledge; the
only prior PRISMA-S text in the fleet is chousa's own (S078 method article, S214 PRISMA 2020, S113/S117 Chinese
reception), which the entry itself distinguishes ("Neither holds PRISMA-S's own checklist text").

### P3 items

| # | path | what it is | same as C1/C2 format? |
|---|---|---|---|
| 1 | `mori-shokunin/.ufo/waves/round-48/w1-results.json` | the only literal `hit_set`-named field outside chousa (`"hit_sets_identical": true`, computed, JSON-in-JSON) | Ancestor of the **comparison**, not of the record: not a table, not committed as a format. |
| 2 | `mado-shokunin/.ufo/waves/round-17/w2/reports/ReopenS070.md:92` (`\| expression \| hits \|`), `tsukuroi-shokunin/.ufo/waves/round-96/w1/ScoutSources/report.md:104` (`\| search \| count \| consequence \|`), `kaidoku-shokunin/.ufo/waves/round-67/w1/ConnectorCross/overlap.md:71` (`\| search \| hits outside kaidoku \|`) | narrative report tables of searches with counts | The *shape* is established fleet prose; none is a machine-parsed record, none carries a revision, a glob scope or a hit set, and none is re-executed by a tool. |

No sibling file contains a `## Searches` heading (3 sibling hits are `## Searches run`, `## Searches that found
nothing specific`, `## Searches performed` in wave reports).

## Findings

### F1 — C1 fires on "the nearest prior instrument": unqualified superlative, contradicted fleet-wide

- Command: `/usr/bin/grep -n "nearest prior" chousa-shokunin/.ufo/waves/round-95/claims.md`
- Receipt: `.ufo/waves/round-95/w1/R95ConnectorSiblings-p4-novelty-scope.txt` (also `-p1-`, `-p5-`)
- Observed: `12:unless `--strict`). On the committed 8-search record every search matches at its revision; the nearest prior` (exit 0)
- Command: `python3 -B tools/count-recheck.py --repo . --manifest tools/count-recheck.json` (cwd `tameshi-shokunin`)
- Receipt: `…/R95ConnectorSiblings-p5-sibling-live.txt`
- Observed: `COUNT_ROW scorecard-r68corr-unanchored-r67tip expect=drift printed=4 measured=0 ok` … `COUNT_RECHECK: rows=7 met=7 unexpected=0` (exit 0); selftest `COUNT_RECHECK_SELFTEST: 6/6 pass` (exit 0)

The sentence asserts a *nearest* prior instrument without a scope word. Read as a claim about the lane, it is
true (`research-gate verify-sweeps` checks sweep locations, never executes the expression — that is what the
sentence compares). Read as written, it is false: a materially nearer prior instrument exists in the fleet,
`tameshi-shokunin/tools/count-recheck.py` (r70, 2026-11-02), which already re-executes a recorded counting command
at a recorded revision and exits 1 when the printed count differs — i.e. the `COUNT_DRIFT` half of C1 — and
`kagi-shokunin/corpus/recheck-replay.py` (r56, 2026-11-07), which replays recorded `curl|grep -c` clocks and
compares the stated count, booked in its own SCORECARD as C1 *capability acquisition*. One word ("the nearest
prior **lane** instrument") makes the sentence true and keeps the acquisition argument intact. As stated, the
comparative is unsupported by the instrument the sentence names and is contradicted by committed sibling bytes.

### F2 — the tool's own docstring makes the same unqualified claim, and it is false fleet-wide

- Command: `/usr/bin/grep -n "re-executes\|verify-sweeps" <carrier>/tools/search-rerun.py`
- Receipt: `…/R95ConnectorSiblings-p4-novelty-scope.txt`
- Observed: `6:The lane's `research-gate verify-sweeps` re-checks only that a NEGATIVE sweep's named glob set is empty; nothing` / `7:re-executes a recorded expression or compares the count it recorded. This tool does, for local searches over` (exit 0)

"nothing re-executes a recorded expression or compares the count it recorded" is true of the lane's gate and
false of the fleet (F1's instruments). This docstring is the probable source of the claim's "nearest" framing, so
it should be narrowed with it: "nothing **in the lane's gate** re-executes …". Not a predicate defect — a
documentation overreach inside the scored artifact.

### F3 — the round carries no sibling-overlap line, though the lane's own precedent does

- Command: `/usr/bin/grep -n "sibling\|Connector\|overlap" chousa-shokunin/corpus/lessons/round-95.md | wc -l`
- Receipt: `…/R95ConnectorSiblings-p4-novelty-scope.txt`
- Observed: `0` (exit 0); and `chousa-shokunin/corpus/lessons/round-62.md:49` reads
  `**Province**: … contested with tameshi (`tameshi-shokunin/PROVINCE.md` …) … Sibling overlap `ConnSiblingOverlap.md`: 11 overlaps`
  (exit 0)
- Command: `/usr/bin/grep -rn "tameshi-shokunin\|kagi-shokunin\|count-recheck\|recheck-replay" … chousa-shokunin/ | grep -v '/\.ufo/'`
- Observed: 2 lines, both `tameshi-shokunin/PROVINCE.md` references (`round-1.md:63`, `round-62.md:49`); no
  mention of either instrument (exit 0)

The lane's established practice (r62) is to record a sibling-overlap line with its count. This round's lesson,
plan and claims carry none, and that is why F1/F2 went unnoticed at freeze. Routing, not absorption: one
`Sibling overlap` line in the round-95 lesson naming the five items above.

### F4 — C2: no duplication, no contradiction found (held)

- Command: `/usr/bin/grep -rln … "PRISMA-S\|jmla.2021.962" *-shokunin/corpus/ | grep -v '^chousa-shokunin/'` →
  `(no stdout)`, i.e. 0 files (exit 0); `for d in *-shokunin/; do grep -Hn "PRISMA" "$d"corpus/SOURCES.md; done | wc -l` → `0` (exit 0)
- Receipt: `…/R95ConnectorSiblings-p2-prisma.txt`

No sibling lane holds PRISMA-S as a source or in a knowledge entry, so the entry's nine quotes cannot be a
duplicate of a sibling's reading, and no sibling instrument interprets item 15's two causes. I did not run C2's
predicates (that is the in-lane seats' work); I only checked the cross-lane axis C2 could be false on.

### F5 — convergence, not a defect: fail-closed ordering already matches the sibling precedent

- Command: `/usr/bin/grep -n "rows = parse_record\|for r in rows" <carrier>/tools/search-rerun.py`
- Receipt: `…/R95ConnectorSiblings-p6-carrier-predicate.txt`
- Observed: `282:    rows = parse_record(record)` then `287:    for r in rows:` (exit 0)

The whole record is parsed (and every row's engine/rev/date/hits/hit_set/glob validated) before any row is
measured — the same up-front resolution `tameshi` states at `count-recheck.py:52` ("resolved for ALL rows up
front, before any row effect", receipt `-p1-`). No action.

### F6 — route: a sibling pins the instrument's own bytes; this battery does not

- Command: `/usr/bin/grep -rn "GATE_SHA256_PIN" kagi-shokunin/corpus/` → `round-56-verifier-spotcheck.md:39:
  sha256sum corpus/recheck-replay.py ⇒ b6959d6c… = GATE_SHA256_PIN` (exit 0)
- Command: `/usr/bin/grep -n "sha256\|--tool\|TOOL =" <carrier>/corpus/evidence/round95/rerun-controls-r95.py`
- Receipt: `…/R95ConnectorSiblings-p6-carrier-predicate.txt`
- Observed: `37:TOOL = "tools/search-rerun.py"`, `189:    ap.add_argument("--tool")`, and the only `sha256` is
  line 106 — the *record's* set digest in the Q1 forgery case, not a digest of the tool under test (exit 0)

`rerun-controls-r95.py` accepts `--tool PATH` and never pins that file's sha256, so the battery's verdict is
about whatever tool it was handed. kagi binds its gate with `GATE_SHA256_PIN` so a stubbed helper cannot forge
CLEAN. Route only: at the carrier the tool bytes are already bound by the commit, so this is optional hardening,
not a defect of C1's predicate.

### F7 — route: a counting command that prints nothing and exits 1 is the count 0 (disclosed, measured)

- Command: `/usr/bin/grep -n "Counting command of record\|zero matches" tameshi-shokunin/tools/count-recheck.py`
- Receipt: `…/R95ConnectorSiblings-p1-rerun-tools.txt`
- Observed: `21:Counting command of record: `git grep -c [-E] <pattern> <rev> -- <path>`` and
  `114:        # zero matches: git grep -c prints nothing and exits 1 (measured,` (exit 0)

Directly relevant to C1's record recipe, which is GNU grep (`/usr/bin/grep -l … | LC_ALL=C sort`, then `wc -l`):
anyone regenerating a row with `grep -c`, or scripting the recipe with `set -e`, must read empty output + exit 1
as zero, or the record will file a count that looks like a failure. Route into the lane's search-record lesson,
do not absorb into this round's claim.

## What I did not measure

- C1 predicate 2 (the `rerun-controls-r95.py` battery groups) and C2's three predicates — in-lane seats.
- Whether any of the eight recorded expressions was the *right* search (C1 named limit d).
- Whether the sibling instruments would accept or refuse chousa's eight one-cell forgeries: they are
  manifest/clock-driven and cannot be handed a `## Searches` record without authoring their own manifests, so the
  comparison is not directly runnable. I therefore report mechanism overlap, not a battery result.
- Predicate 1 I did run once at the carrier for orientation: `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8
  tree_same=3/8 findings=0`, `SEARCH_RERUN: CLEAN`, `EXIT=0` (receipt `…-p6-`). Note `tree_same=3/8`: the carrier
  worktree already holds this round's new capture, so five searches read `TREE_CHANGED` — consistent with the
  claim's exit-0 rule, and the reason a "current tree" leg is a real leg on this tree.

## Evidence index (all under `.ufo/waves/round-95/w1/`)

- `R95ConnectorSiblings-p1-rerun-tools.txt` — P1 counts, provenance commits, docstring lines of both sibling
  instruments, standing registration in their SKILL/SCORECARD
- `R95ConnectorSiblings-p2-prisma.txt` — P2 fleet counts, per-lane split, the three passthrough files, sibling
  `SOURCES.md` PRISMA count = 0
- `R95ConnectorSiblings-p3-record-formats.txt` — P3 `hit_set` hits, `## Searches` headings, the mori field and its
  commands, the three narrative tables in full excerpt
- `R95ConnectorSiblings-p4-novelty-scope.txt` — claims.md:12, the tool docstring lines 6-7, chousa's sibling
  citations, round-95 lesson sibling-mention count = 0, kagi's `GATE_SHA256_PIN`, tameshi manifest shape
- `R95ConnectorSiblings-p5-sibling-live.txt` — both sibling selftests live (`6/6 pass`; `PASS (20 cases)`) and a
  live `COUNT_ROW … met=7 unexpected=0` sweep
- `R95ConnectorSiblings-p6-carrier-predicate.txt` — carrier HEAD, predicate-1 run, battery `--tool`/sha facts,
  fail-closed ordering lines

VERDICT: R95ConnectorSiblings C1 fired — the sentence's unqualified "the nearest prior instrument" is false fleet-wide (tameshi `count-recheck.py` r70 and kagi `recheck-replay.py` r56 already re-execute a recorded command at a named revision and compare the printed count), and the tool docstring repeats the same unqualified "nothing re-executes a recorded expression"; scope the word to the lane and the acquisition argument stands.
VERDICT: R95ConnectorSiblings C2 held — no sibling lane holds PRISMA-S in a knowledge entry or `SOURCES.md` row (0 rows across 20 lanes; the three sibling occurrences relay chousa's own files/captures), so nothing cross-lane contradicts C2.
