# Round 50 W1 — DraftMistakes: `## Mistakes` rows for `corpus/lessons/round-50.md`

seat: DraftMistakes · round 50 · wave 1 · 2026-10-25
scope: draft the round-50 lesson's `## Mistakes` rows from the three mined defects, verify each one myself,
and propose one check per row shown failing on committed bytes. No fetch (L0 `8d77e6c1` open). Only this report
is written; scratch `/dev/shm/chousa-r50-DraftMistakes/` is deleted before finishing; nothing else was modified.

## M1 — the restated quote count is stale (28 vs 31)

The owning artefact is the 31-data-row manifest, and the counter QUALITY 72 names prints 31:

```
$ python3 corpus/evidence/round49/quote-substance-check.py
IDS=8 QUOTES=31 FAILURES=0                      # RC=0
$ awk 'NR>1 && NF' corpus/evidence/round49/spans.tsv | wc -l
31
$ wc -l corpus/evidence/round49/spans.tsv
32 corpus/evidence/round49/spans.tsv            # header + 31 data rows
$ grep -c 'S[0-9][0-9][0-9]' corpus/evidence/round49/spans.tsv
31
```

Three files restate 28 (`-o` where the phrase sits late in a long row):

```
$ grep -n 'QUOTES=28' corpus/QUALITY.md
746:    prints `IDS=8 QUOTES=28 FAILURES=0`, exit 0. — `corpus/lessons/round-49.md`
$ grep -n -o '28-row manifest' corpus/README.md
1074:28-row manifest
$ grep -n -o '28 located quotes' LOG.md
1803:28 located quotes
```

The committed after-measurement says 31 (`sed -n '38p;45p;78p' corpus/evidence/round49/measure-after.txt`):

```
QUOTE_ROWS=31 ON_BOUND=31/31
CAPTURE_BOUND=31/31
IDS=8 QUOTES=31 FAILURES=0
```

Round-49 verifier spot-check defect 2 (`corpus/lessons/round-49-verifier-spotcheck.md:96`) records the same
three stale lines. Criterion that should have caught it: **QUALITY 37** ("every numeric tally carries its
counting command. Check: run the named command and compare") — the command was named and never re-run;
**QUALITY 9** (one home per number; restating files closed in the same landing) would have propagated the fix.

## M2 — a closure report filed before the waves settled, with the seat reports it names left uncommitted

Report text (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/chousa.md:94-96`):

```
94:**Conformance defect:** this report was filed before WAVE-DONE arrived for either wave, because the run reached its budget stop.
95:- At filing, W1 had 39/40 reports (`ScoutInherited` outstanding) and W2 had 27/35 (MutA05, MutSubstance, ReviewQuality, ExecReplayC1, ScribeScorecard, ScribeTrends, ScribeShonen and ScoutPlanned outstanding).
96:- These seats were live, not dead; their late reports remain uncommitted wave evidence.
```

Commit order and tree state:

```
$ git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ci' -- .ufo/reports/round-49/chousa.md
3cbe92a467d4313f1d1494614afe4275571712c8 2026-10-25 17:37:45 -0300
$ git -C chousa-shokunin log -1 --format='%H %ci %s' 4d13657
4d13657e220354ee19a6bb171c7f367b35a841dd 2026-10-25 17:54:31 -0300 round-50: inherited round-49 late seat reports (MutA05, MutSubstance, ReviewQuality)
$ git -C chousa-shokunin ls-tree -r 5275c892 --name-only | grep -c 'round-49/w2/\(MutA05\|MutSubstance\|ReviewQuality\)'
0
$ git -C chousa-shokunin ls-tree -r 4d13657 --name-only | grep -c 'round-49/w2/\(MutA05\|MutSubstance\|ReviewQuality\)'
3
```

Spot-check defects 1 and 4 (`corpus/lessons/round-49-verifier-spotcheck.md:95,98`). Criterion that should
have caught it: **QUALITY 61** ("a dispatch is complete only when the dispatcher stayed alive until each seat
settled, and the record names the seats that returned a report and the seats that died") — the report named
the outstanding seats but filed the closure anyway; **QUALITY 9**'s same-landing clause covers the three
reports the report itself called "uncommitted wave evidence".

## M3 — the adopter's `cited` set takes body cross-references, so another document's rows are adopted

Exact dispatch command (scratch out dir):

```
$ python3 tools/assimilate-rows.py --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
    --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
    --registry corpus/SOURCES.md --opened 2026-10-25 \
    --out /dev/shm/chousa-r50-DraftMistakes/o --entry corpus/knowledge/cnki-citation-check-r40.md
COLLISIONS=22
CITED=3 APPEND=3 HELD=0                          # RC=0
$ cat /dev/shm/chousa-r50-DraftMistakes/o/renumber.tsv
staged_id	lane_id	action	url
S109	S104	append	www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
S111	S105	append	www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3
S124	S106	append	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf
```

The staged entry cites its own document at `…/corpus/knowledge/cnki-citation-check-r40.md:4` (`source: S124 —
https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf`) and mentions two other documents
in body prose: `:41` "`S109`–`S111`" (round-4's search-record theme) and `:64` "`S076` raised about J-STAGE".
`S109` is `japanese-search-record-r38.md`, `S111` is `chinese-search-log-r37-amendment-2026-10-23.md`, `S124`
is the CNKI 管理员 manual. The tool's entry copy shows the overreach (`diff -u`):

```
-source: S124 — https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf — 第6章 辅助功能, 6.1 引文核对 — PDF text extracted 2026-10-23
+source: S106 — https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf — 第6章 辅助功能, 6.1 引文核对 — PDF text extracted 2026-10-23
-  (round 4's `S109`–`S111`). The amber state is the lane's missing middle
+  (round 4's `S104`–`S105`). The amber state is the lane's missing middle
```

Consequence against this round's plan: lane ids S104–S107 are free at the registry maximum S103
(`grep -cE '^\|[[:space:]]*S10[4-7][[:space:]]*\|' corpus/SOURCES.md` → 0: none present), so the run
would bind S104 to a J-STAGE paper, S105 to a medsci PRISMA-S article, and push the 管理员 manual
(S124/S135/S180/S187) to S106 — the planned 子账号 id. The tool delegates the check to the reader
(`tools/assimilate-rows.py:25-26` "staged ids pass through unchanged — checking that they name the right lane
document is the reader's job"), and this run applied none. Criterion that should have caught it: **none** —
QUALITY 1-72 contains no criterion making "the id names this entry's document" a checkable finding; the
by-document rule lives in campaign addendum section 10.

## Drafted rows — intended lane path `corpus/lessons/round-50.md`

```markdown
## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| A restated count drifts from the manifest it restates: one number, three stale copies | `corpus/QUALITY.md:746` prints `QUOTES=28`; `corpus/README.md:1074` says "28-row manifest"; `LOG.md:1803` says "28 located quotes … `CAPTURE_BOUND=28/28`"; the counter prints `IDS=8 QUOTES=31 FAILURES=0` and `corpus/evidence/round49/measure-after.txt:38,45` carry 31 over a 31-data-row `corpus/evidence/round49/spans.tsv` (`wc -l` 32 incl. header); round-49 verifier spot-check defect 2 (`corpus/lessons/round-49-verifier-spotcheck.md:96`) | QUALITY 37 named the counting command and nobody re-ran it; QUALITY 9's one-home rule was not applied to the three restating files | `corpus/evidence/round50/restated-count-check.py` (below): runs the named counter and requires the newest restatement in each of the three files to equal its `QUOTES=` figure. Shown able to fail now: `MISMATCH corpus/QUALITY.md have 28 want 31`, `MISMATCH corpus/README.md have 28 want 31`, `MISMATCH LOG.md have 28 want 31`, `RESTATED_COUNT=FAIL want=31`, exit 1; corrected copies → `RESTATED_COUNT=PASS want=31`, exit 0. |
| A closure report is filed before either wave settles, and the seat reports it names as outstanding are left uncommitted | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/chousa.md:94` "filed before WAVE-DONE arrived for either wave", `:95` "W1 had 39/40 … W2 had 27/35", `:96` "their late reports remain uncommitted wave evidence"; lane tree `5275c892` holds 0 of the three named reports and `4d13657` (17:54:31) holds 3, after the report commit `3cbe92a4` (17:37:45); spot-check defects 1 and 4 (`round-49-verifier-spotcheck.md:95,98`) | QUALITY 61 — a dispatch is complete only when every seat settled, and a shortfall is not a completed wave; the report named the outstanding seats but filed closure anyway. QUALITY 9's same-landing clause for the uncommitted reports | `corpus/evidence/round50/landing-check.py` (below): requires each wave's `W<n> had <a>/<b>` line with `a==b` and the report commit not earlier than the newest `.ufo/waves/round-N/` commit. Shown able to fail on round 49: `WAVE_INCOMPLETE W1 39/40`, `WAVE_INCOMPLETE W2 27/35`, `REPORT_BEFORE_SEATS report=1792960665 newest-wave-commit=1792961683`, `LANDING=FAIL`, exit 1; `/dev/shm` git fixture with the wave committed first → `LANDING=PASS` exit 0; reversed → `REPORT_BEFORE_SEATS` exit 1; `W1 had 3/4` → `WAVE_INCOMPLETE W1 3/4` exit 1. |
| An adoption tool's `cited` set is every staged id token in an entry, so body cross-references to other documents are adopted and renumbered | `tools/assimilate-rows.py:17-18` ("every staged id the entries cite") and `:25-26` ("Tokens that are not staged ids pass through unchanged — checking that they name the right lane document is the reader's job"); staged entry `…/corpus/knowledge/cnki-citation-check-r40.md:4` (`source: S124`), `:41` (`S109`–`S111`), `:64` (`S076`); run on that entry → `CITED=3 APPEND=3`, `renumber.tsv` `S109→S104`, `S111→S105`, `S124→S106` | none in QUALITY 1-72 — the by-document rule is addendum section 10; no criterion makes id-to-document binding a finding | `corpus/evidence/round50/cited-id-check.py` (below): every staged id in `renumber.tsv` must have a `^source: <id>` line in the entry. Shown able to fail now: `BODY_CROSSREF S109->S104`, `BODY_CROSSREF S111->S105`, `CITED_IDS=FAIL rows=3`, exit 1 (and `S124->S106` mis-binds the 管理员 manual away from the planned S105); source-only renumber tsv → `CITED_IDS=PASS rows=1`, exit 0. |
```

## Proposed checks — intended lane paths, for the L1 to integrate

```python
# corpus/evidence/round50/restated-count-check.py
#!/usr/bin/env python3
"""restated-count-check — the round-49 located-quote count restated in QUALITY.md, README.md and
LOG.md must equal what the named counter prints. Newest restatement per file wins (LOG is append-only).
Usage: python3 restated-count-check.py [LANE_ROOT] · exit 0 equal · 1 mismatch/missing · 2 no figure."""
import pathlib, re, subprocess, sys
LANE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out = subprocess.run([sys.executable, str(LANE / "corpus/evidence/round49/quote-substance-check.py")],
                     capture_output=True, text=True).stdout
m = re.search(r"QUOTES=(\d+)", out)
if not m:
    print("NO_COUNTER_FIGURE"); sys.exit(2)
want = m.group(1)
PATS = [("corpus/QUALITY.md", r"QUOTES=(\d+)"), ("corpus/README.md", r"(\d+)-row manifest"),
        ("LOG.md", r"(\d+) located quotes")]
bad = 0
for rel, pat in PATS:
    hits = re.findall(pat, (LANE / rel).read_text(encoding="utf-8"))
    if not hits:
        print(f"MISSING {rel}"); bad += 1
    elif hits[-1] != want:
        print(f"MISMATCH {rel} have {hits[-1]} want {want}"); bad += 1
print(f"RESTATED_COUNT={'PASS' if not bad else 'FAIL'} want={want}")
sys.exit(0 if not bad else 1)
```
```python
# corpus/evidence/round50/landing-check.py
#!/usr/bin/env python3
"""landing-check — each wave settled to its seat count, and the report commit not earlier than the
newest wave-directory commit.
Usage: python3 landing-check.py <REPORT> <LANE_ROOT> <FLEET_ROOT> <ROUND> · exit 0 landed · 1 short
wave / missing commit / report first · 2 no settled-count line."""
import pathlib, re, subprocess, sys
report, lane, fleet, rnd = (pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]),
                            pathlib.Path(sys.argv[3]), sys.argv[4])
rows = re.findall(r"W([12]) had (\d+)/(\d+)", report.read_text(encoding="utf-8"))
if not rows:
    print("NO_SETTLED_COUNT"); sys.exit(2)
bad = 0
for wave, got, total in rows:
    if got != total:
        print(f"WAVE_INCOMPLETE W{wave} {got}/{total}"); bad += 1
def ct(repo, path):
    return int(subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct", "--", path],
                              capture_output=True, text=True).stdout.strip() or 0)
rct, sct = ct(fleet, f".ufo/reports/round-{rnd}/chousa.md"), ct(lane, f".ufo/waves/round-{rnd}/")
if not rct or not sct:
    print(f"NO_COMMIT report={rct} wave={sct}"); bad += 1
elif rct < sct:
    print(f"REPORT_BEFORE_SEATS report={rct} newest-wave-commit={sct}"); bad += 1
print(f"LANDING={'PASS' if not bad else 'FAIL'}")
sys.exit(0 if not bad else 1)
```

```python
# corpus/evidence/round50/cited-id-check.py
#!/usr/bin/env python3
"""cited-id-check — every staged id renumbered for an entry must be a `source:` line of that entry,
not a body cross-reference to another document.
Usage: python3 cited-id-check.py <ENTRY> <RENUMBER_TSV> · exit 0 bindings only · 1 a body ref · 2 no rows."""
import pathlib, re, sys
entry = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
lines = [l for l in pathlib.Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
if not lines:
    print("NO_ROWS"); sys.exit(2)
bad = 0
for l in lines:
    staged, lane_id = l.split("\t")[:2]
    if not re.search(rf"^source: {staged}\b", entry, re.M):
        print(f"BODY_CROSSREF {staged}->{lane_id}"); bad += 1
print(f"CITED_IDS={'PASS' if not bad else 'FAIL'} rows={len(lines)}")
sys.exit(0 if not bad else 1)
```

## Divergences from the dispatch brief (verbatim, for the canonical judge)

- M3's expectation "appends rows for S076/S109/S111": observed `CITED=3` = **S109, S111, S124**. S076 is not
  a staged row (`grep -n 'S076' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` over 114
  staged rows → no output), so the tool passes it through unchanged; it still names another lane document
  (`corpus/SOURCES.md:86` = the GNU `sed(1)` row) and must be dropped or described by file path.
- M1's "`wc -l`, `grep -c`" parenthetical: `wc -l` is **32** (header + 31); the 31 count is the data rows
  (`awk 'NR>1 && NF' | wc -l` = 31, `grep -c 'S[0-9][0-9][0-9]'` = 31). `spans.tsv` has 31 rows, not 32.
- M2's report lives in the fleet repo, the seat reports and wave dirs in the lane repo; the comparison spans both.

## Touched surfaces

Read-only: lane repo, fleet repo, `shokuknow` staged package and cache. Written: this report only. Scratch
`/dev/shm/chousa-r50-DraftMistakes/` (three checks, corrected copies, two git fixtures) deleted. No installs, no gate run, no commit.

VERDICT: attacked the three routed round-49 defects — confirmed the 28-vs-31 number drift, the pre-WAVE-DONE filing with three seat reports uncommitted, and the adopter adopting body cross-references (S109/S111 plus S124, not S076); drafted three Mistakes rows whose proposed checks each fail on committed bytes and pass on corrected input.
