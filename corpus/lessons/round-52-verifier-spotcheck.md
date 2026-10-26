# chousa round 52: verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
lane tip measured: `f80a9a255908389992faa6daa495fc6b9276af15` (before: `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`)
inputs: fleet report `.ufo/reports/round-52/chousa.md`; prompt `.ufo/prompts/chousa-round-52.md`
driver lines (`.ufo/watchdog.log`): `2026-10-26T19:51:22-03:00 launch chousa round=52 pgid=1151232 driver=hyaku-inline attempt=1` · `2026-10-26T20:39:08-03:00 complete chousa round=52; hyaku-inline attempt=1`

The closure ran every measurement below over committed bytes: `git archive` exports of the tip (`/tmp/r52chk`) and the base (`/tmp/r52base`), packages I wrote myself, and the lane's read-only on-disk captures under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = first 24 hex of sha256 of the URL; I confirmed this for the NIPH `.docx`, the PRISMA-S DOI and the S130 `.doc`). I executed no lane counter (`c1-count.py`, `c1-supplement.py`, `c2-count.py`, `build-spans.py`, `verdict-gap.py`) and read their committed receipts instead. I ran the lane's tool `tools/capture-text.py` as a capability on my own inputs and on the NIPH capture. I ran the lane's two C1 control tools (`controls/naive-tool.py`, `controls/forge-shape.py`) on my own probe for comparison only. The two probe scripts are reproduced in section 7 so that a later reader can re-run them.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-52/chousa.md` (fleet repo) | `chousa-shokunin c8f8e4367de96f1ec0d40d9a56a818bd39c3ab96`. Committer time 2026-10-26T20:38:22-03:00: after the lane tip's committer time (20:38:07) and before the 20:39:08 complete line, so it landed last. ok |
| SHONEN heading, one line per box | `grep -c '^## SHONEN'` on the report; `grep -c '^- \[' SHONEN.md` | heading once; 4 boxes and 4 lines, all `[~]` with pointers. ok |
| every cited lane commit exists and is an ancestor of the branch | `git merge-base --is-ancestor <h> master` for `37468ead 804a4537 13bc2806 01c17ce3 e769c037 d1d972cf 643ac77b 1a170f55 f80a9a25` plus base `00f8c7f5` | all ten resolve and are ancestors. The nine round commits are authored `chousa-shokunin`. ok |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=f80a9a25… remote=f80a9a25… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote prints `f80a9a255908389992faa6daa495fc6b9276af15`. ok |
| prompt carries template contract | grep of `.ufo/prompts/chousa-round-52.md` (624 lines) | §1 MISSION/AXES binding; §2 claims 1–3 with the lowest-axis rule; §2b frontier step; §3 L2 floor; §4 report path, the SHONEN requirement and the marker rule; §5 commit-then-push, push scope and L0; write scope at line 365; hash citation at lines 389 and 433; §6 hyaku addendum (run 9 band 64–128). ok |
| round size | `jq` over `.ufo/waves/round-52/w1-results.json` / `w2-results.json` | W1 `seats=45 results=45`, W2 `seats=38 results=38`, no error field. Two v1 waves of 32–64 summing to 83 sit inside the 64–128 band. ok |
| append-only files | `git diff --numstat 00f8c7f5 f80a9a25` | 173 files, 16,891 insertions, **0 deletions** (SCORECARD +30, LOG +10, SKILL +2, QUALITY +8, README +27, SOURCES +5). ok |
| marker rule | real committed work: two claims with counters and nine lane commits | not a marker; status `ok` |

Defects (status-neutral) are listed in section 6. None changes the status.

## 2. Per-claim re-check

### R52-C1 operability (capability): `tools/capture-text.py`. Re-measured by independent probe; counter tallies evidence-verified.

| leg | command | observed |
|---|---|---|
| base | `ls /tmp/r52base/tools/capture-text.py` | `No such file or directory`: the tool is absent at base |
| tip, my own probe (9 cases) | `python3 /tmp/r52close/c1probe.py /tmp/r52chk/tools/capture-text.py <wd>` (section 7) | `PROBE=9/9`. Cases: (1) a hand-spelled package that does not follow the lane generators' spelling — namespace prefix `q:` rather than `w:`, single-quoted attributes, a `CDATA` run, an XML comment, non-self-closing `<q:tab></q:tab>`/`<q:br></q:br>`, `&#x3042;`, a `pPr/tabs` stop, `delText`, `instrText`, an `mc:Fallback`, a paragraph nested in a table cell, the main part at a random member named by a `/`-prefixed `_rels/.rels` target under prefix `r:`, and a decoy `word/document.xml`. Output equals my hand-written expectation `'A… & <b>\tC\nD\nE\n\nF\nGあ\n'`. (2) `--locate` once gives `count=1 offset=23` rc 0. (3) `--locate` six times gives `count=6` rc 1. (4) `--locate` of the decoy text gives `count=0 offset=-1` rc 1. (5)–(9) not-a-zip, no `_rels/.rels`, missing target, `xl/workbook.xml` root and `../x.xml` target each give rc 2 with stdout empty and stderr `REFUSED …` |
| controls on the same probe | same probe with `controls/naive-tool.py` / `controls/forge-shape.py` | `PROBE=2/9` / `PROBE=5/9`. The representation forge that passes the frozen counter 9/9 fails my re-spelled package, which confirms the lane's own finding that the frozen counter certifies the generators' spelling and not conformance |
| real capture | `python3 tools/capture-text.py .qcache/3a8b45977cd111e45e3980a5.raw` (key = sha256 of the NIPH URL; raw sha256 `16fc8c55ee85…`) | 19,682 characters. `--locate` gives `offset=8996` (3.1 sentence), `9020`, `9428`, `9419` (`使用した検索式`), `19496` and `19521`, each `count=1` |
| independent reader | my own `xml.dom.minidom` walker implementing the frozen predicate (section 7) on the same `.raw` | main part `word/document.xml`, 19,682 characters, `SRにおける文献検索期間について明記する。` once at 8996, `その名前と所属…` once at 19496. Character-for-character agreement with the tool on length and offsets, so the REAL leg is grounded in more than the tool agreeing with itself |
| tool digest vs receipt | `sha256sum tools/capture-text.py`; `git diff --stat 643ac77b f80a9a25 -- tools corpus/knowledge corpus/SOURCES.md` | `6902db6acf3ae5a0ac579ff88ae4fe4a36877b7b960c438bf36a67007b26be17` equals the `measure-after.txt` header `tool-rev: 643ac77b… digest: sha256:6902db6a…`. tools, knowledge and SOURCES are unchanged after `643ac77b` |
| committed gate evidence | `controls/c1-before.txt`, `measure-after.txt`, SKILL.md Gates rows `capture-text` and `chousa round-52 counters and checks` | base `LEGS=0/9 C1=FAIL exit=1`; naive 4/9, cache-txt 0/9, const 0/9; after `LEGS=9/9 C1=PASS exit=0` on three unseeded runs and `--seed 7`; supplement `SUPPLEMENT_LEGS=4/4`; the forge fails the supplement 0/4 and passes the frozen counter 9/9 (receipt lines 61–90). Registry rows are present at the lane's registry home (`SKILL.md`) |

Re-measured: base absence, nine behaviours on packages I wrote, the real capture, and an independent reader. Evidence-verified only: the frozen counter's tallies, its controls and the supplement. The frozen counter is forgeable by XML spelling and the supplement by a memoised NIPH text (lane's own findings, disclosed). My re-spelled probe shows the landed tool does not depend on that spelling. Grade **improved**.

### R52-C2 depth (sourced): three entries on four documents. Re-measured.

| leg | command | observed |
|---|---|---|
| SOURCES rows before → after | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` on the base and tip exports | 112 → 116 (S113–S116). Each new row has `NF=13` under the CORPUS.md awk |
| theme absent at base | `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5… -- corpus/knowledge` | exit 1 (nothing). At the tip each entry holds its own term: niph-form `文献検索期間` 6, prisma-item-wording `完全な検索戦略` 6, prisma-s-reception `检索报告清单` 4 |
| all 39 manifest quotes | python over `corpus/evidence/round52/spans.tsv`: capture located by URL key (`.txt` UTF-8, or the `.raw` through `tools/capture-text.py` for the `.docx`), quote counted in it, present in the citing entry and in `corpus/lessons/round-52.md`, ≤25 whitespace words and ≤160 characters | `ROWS 39 BAD 0` (S113 6, S114 9, S115 15, S116 9) |
| lesson offsets | each `## All located quotes` row's `char offset` compared with `find()` in the same form | `LESSON_ROWS 39 OFFSET_MISMATCH 0` |
| row anchors | every `char N` in the anchor cells of S113–S116 is one of that id's located offsets | S113 `[2034 2328 2433 3139 4850]`, S114 `[1650 1707 1785 5530]`, S115 `[8996 9020 9408 9419 9428]`, S116 `[475 592 641 753]`: all true |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit 0, `ok`, five pre-existing W04 only (S051 S053 S073 S074 S075). Matches the report |
| committed gate evidence | `controls/c2-before.txt`, `controls/c2-controls.txt`, `measure-after.txt` | `BOUND=0/4 C2=FAIL exit=1`; staged-copy control `REF_ID_UNBOUND=31 C2=FAIL`; after `BOUND=4/4 QUOTE_ROWS=39 CAPTURE_BOUND=39/39 ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 C2=PASS exit=0`, also `--lane-only`; `build-spans.py --check` `STALE=0`; `quote-substance-check.py` `FAILURES=0` |

Re-measured: rows, theme absence, all 39 quotes and their offsets, anchors, census, and the entailment reads in section 4. Evidence-verified only: the counter's control scores and the inference-ground pass. The lane discloses that the CJK polarity leg is inert, so entailment rests on reading; I read the NIPH and Chinese entries against their captures (section 4) and found no overstatement. Grade **improved**.

## 3. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1: tool absent at base; at the tip 9/9 on my re-spelled probe plus the real capture, matched by an independent reader (19,682 characters, 8996); the forge scores 5/9 on the same probe |
| depth | improved | C2: three entries, 39 quotes, each located once in its form at the stated offset; anchors bound |
| coverage | improved | the three theme terms are absent from `corpus/knowledge` at base (git grep exit 1); three documents are new ground. S113 is a second carrier and earns no credit (agreed, section 4) |
| calibration | improved | the round-51 S120 offset `char 39411` is confirmed an offset of nothing (`word/document.xml` 1,379,262 characters; the sentence and `SRにおける` both `find` → -1; char 39411 is inside `w:rStyle` markup) and is re-located at 8996 in a named form; QUALITY 87–90 each cite a lesson row; one stale erratum range (section 6.1) |
| freshness | unchanged | no fetch; newest cache file 2026-10-24 23:26:57 -03 (`stat`); SOURCES rows are first opens of existing captures |
| adjacency | unchanged | the lane's connector seats report no sibling overlap. The closure did not re-read this independently and carries the lane's reading without upgrading it |

No axis is harmed. `git diff 00f8c7f5 f80a9a25 -- SCORECARD.md` is one hunk `@@ -2658,3 +2658,33 @@` with insertions only, and prior rows are untouched.

## 4. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `japanese-search-record-niph-form-r52.md` (S115) | admit | `.qcache/3a8b45977cd111e45e3980a5.raw` through the tool and through my independent reader | agree | 3.1 sentence once at 8996, 9020 and 9428 as stated. Section 7 at 19496/19521 asks for names only of outside experts and says they are in principle not published. `検索者` and `検索担当` occur 0 times in the text form, so the inference "the form does not make the searcher a field" holds. The `.txt` sidecar is not the text form (round 51 already showed 72,117 U+FFFD) |
| `chinese-prisma-s-reception-r52.md`, S113 no-credit judgment | admit, with no expansion credit for S113 | `453d492becd9a2f4632cb8dd.txt` (梅斯医学) vs SinoMed `42bac8830527d6f1bb125c49.txt` | agree | SinoMed has `作为“报告规范”的内在局限,并针对中文` and then only whitespace (tail `并针对中文数据库等本土化应用挑战提出实践建议` occurs 0 times); 梅斯医学 carries it. The record is the same article, so it counts as a second carrier; what it adds is that clause, exactly as the entry says |
| `japanese-prisma-item-wording-r40.md` (S116) | admit with the recheck re-cut | `e84bfe97808591d23fe3266f.txt` | agree | `検索者` 0; the staged full sentence occurs 0 times; `用いたフィルターや制限も含め，` at 641, once. The repair the lesson names is needed and was made |
| `search-log-fields-r36.md` | **reject** | `01f657b3d0ab045c494b3f92.txt` (key = sha256 of `https://doi.org/10.1186/s13643-020-01542-z`) | agree | 265 characters, `Client Challenge … A required part of this site couldn’t load`. `copied and pasted exactly as run` is in 0 of 2,549 `.txt` files; newest cache file is 2026-10-24. Neither conjunct of the flip is met |
| `grey-literature-and-chinese-search-record-r40.md` | **reject** | S130 `.qcache/bdff491a75c6abeda1d9c01d.raw` (OLE `d0cf11e0`, 243,929 B, key = sha256 of the gcpunion URL), decoded UTF-16LE; staged entry in `shokuknow/merge/chousa/…/grey-literature-and-chinese-search-record-r40.md` | agree on the decision, **disagree on one reason** | The decision is right on the grounds the row also gives: S133 and S111 are one URL (a second row would break the frozen by-document binding), and the document lies outside the round's frozen set. But the staged headline is "A Chinese regulator requires the search record to state whether grey literature was searched", a search-record field and so in province. Guideline currency is one of its `Unknown` bullets, not its spine. The source does carry the field: `应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题` occurs once in the UTF-16LE decode. "Already carried by `chinese-search-record-r39`" is also weak, because S109 is not the regulator. Routed (section 6.2) |
| SOURCES row S115 (newly written) | admit | as row 1 | agree | the headline quote `SRにおける文献検索期間について明記する。` is 1 whitespace word and 21 characters (≤25 words), located once at char 8996, the row's first anchor; all five anchor offsets are located quote offsets |
| SOURCES row S114 (newly written) | admit | `cacddf3bbf780a4c7582bb17.txt` | agree | the headline `明确说明每一项来源 的 检索或查询日期` (≤25 words) occurs once at 1707, its anchor offset. Tier A is scoped to "what this journal page states", not an attributed translation |
| quarantine slice (S120, one row on a theme URL) | verdict `present`, chars 8996/9020/9428 | NIPH `.raw` | agree | all three sentences occur once at those offsets in the tool form, and 8996 is reproduced by my independent reader. The round-51 `char 39411` is an offset of nothing, as Mistakes row 2 says |

Eight items: three admits, two rejects, two new rows and the quarantine verdict. All eight decisions agree. One reject reason is disputed and routed.

## 5. Trend verdicts

- **expansion: improved.** SOURCES grew 112 → 116 with four mined rows, and three documents sit on ground the base did not hold (the theme terms are absent at base). A new capability row (OOXML capture text form) is shown running on a real capture and on my own packages.
- **quality: improved.** The staged material was corrected on adoption, and each correction is checkable: the S125 title strings appear 0 times, the joined example string has `count=0`, and the S116 sentence has 0 occurrences, so the recheck was re-cut. The tool's refusal contract covers non-Word, escaping and missing targets, as my probe shows. The counters' weaknesses are reported, not hidden. No admitted entry failed my re-check (39/39 quotes, 39/39 offsets).
- **discernment: improved.** The non-author re-opening agrees with every sampled admit and reject (8/8 decisions). The one disputed reason, province framing on the grey-literature reject, changes no decision and is routed for a lesson, not left unlearned.

## 6. Routed defects and notes for the lane

1. **Stale erratum range (corrections sweep).** `corpus/lessons/round-52.md:153` and the SCORECARD round-52 verdict intro say `claims-erratum.md` E1–E4, while the erratum carries E1–E6 (E5 in-round narrowing, E6 unbounded span-builder reader). Append a correction naming E5–E6. Do not rewrite.
2. **Grey-literature r40 refusal reason.** Restate the reason as "S133 duplicates the S111 URL; outside the frozen by-document set". The headline is a search-record field (in province), and S130's UTF-16LE decode carries `是否检索灰色文献` once. Before any re-stage, define a text form for OLE `.doc` captures (UTF-16LE decode is not a defined form) and decide the regulator field record on its own source, with currency kept as an Unknown.
3. **Representation variance in the next frozen C1-style counter** (lane finding, now independently confirmed). A namespace prefix other than `w:`, single-quoted attributes, `CDATA`, comments and non-self-closing break elements separate the landed tool (9/9) from the forge (5/9) on my probe. Fold them into the frozen counter, not a post-freeze supplement.
4. **Still open from round 51:** adopter twin-id `held` label and refusal ordering (routed 2), and the anchored `correction:` check (routed 4). Both were built in scratch and not landed, so they stay on the queue.
5. **Inference-ground CJK polarity leg is inert** (lane's W2 finding). Add a red-before fixture on a negated CJK bullet.
6. Status-neutral: a W1 seat wrote `p.out`/`p.err` at the fleet root and a W2 seat wrote four control outputs into the lane root through relative redirects. Both were disclosed, moved or removed, and never committed.

SHONEN boxes: all four are `[~]`. For the operator: boxes 1–3 look checkable by a non-author from committed bytes. The Gates rows and QUALITY 87–90 resolve; the end-to-end task is logged with a receipt; I ran `python3 tools/capture-text.py <raw> --locate '<quote>'` without oral context. Box 4 (province fit) rests on lane-dispatched seats. I assert no `[x]` here; promotion is operator-owned.

## 7. Probe sources (closure scratch, reproduced for re-run)

`/tmp/r52close/c1probe.py` (`python3 c1probe.py <tool> <workdir>` prints one `<case>=PASS|FAIL` line per case and `PROBE=n/9`):

```python
import os, subprocess, sys, zipfile, secrets
TOOL, WD = sys.argv[1], sys.argv[2]; os.makedirs(WD, exist_ok=True)
WNS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MCNS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
def rels(target, prefix=""):
    p = (prefix + ":") if prefix else ""; x = (":" + prefix) if prefix else ""
    return (f"<?xml version='1.0' encoding='UTF-8'?>\n<{p}Relationships xmlns{x}=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            f"<{p}Relationship Target='{target}' Id='rX' Type='{RT}'></{p}Relationship></{p}Relationships>")
def pkg(name, members):
    path = os.path.join(WD, name)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for k, v in members.items(): z.writestr(k, v)
    return path
def run(path, *a):
    r = subprocess.run([sys.executable, TOOL, path, *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
tok = secrets.token_hex(3); res = []
doc1 = (f"<?xml version='1.0' encoding='UTF-8' standalone='yes'?><q:document xmlns:q='{WNS}' xmlns:m='{MCNS}'><q:body>"
        f"<q:p><q:pPr><q:tabs><q:tab q:val='left' q:pos='720'></q:tab></q:tabs></q:pPr>"
        f"<q:r><q:t xml:space='preserve'>A{tok} &amp; </q:t></q:r><!-- c --><q:r><q:t><![CDATA[<b>]]></q:t><q:tab></q:tab><q:t>C</q:t></q:r></q:p>"
        f"<q:p><q:r><q:delText>GONE</q:delText><q:instrText> PAGE </q:instrText><q:t>D</q:t><q:br></q:br><q:t>E</q:t><q:cr/></q:r></q:p>"
        f"<q:p><q:r><m:AlternateContent><m:Choice Requires='wps'><q:t>F</q:t></m:Choice><m:Fallback><q:t>NOPE</q:t></m:Fallback></m:AlternateContent></q:r></q:p>"
        f"<q:tbl><q:tr><q:tc><q:p><q:r><q:t>G&#x3042;</q:t></q:r></q:p></q:tc></q:tr></q:tbl></q:body></q:document>")
exp1 = f"A{tok} & <b>\tC\nD\nE\n\nF\nGあ\n"; mem = f"docs/{tok}/main.xml"
p1 = pkg(f"{tok}-1.zip", {"_rels/.rels": rels("/" + mem, prefix="r"), mem: doc1,
     "word/document.xml": f"<w:document xmlns:w='{WNS}'><w:body><w:p><w:r><w:t>DECOY</w:t></w:r></w:p></w:body></w:document>"})
rc, out, err = run(p1); res.append(("spelling+form", rc == 0 and out == exp1))
rc, out, err = run(p1, "--locate", "Gあ"); res.append(("locate", rc == 0 and out.strip() == f"LOCATED count=1 offset={exp1.index('Gあ')}"))
rc, out, err = run(p1, "--locate", "\n"); res.append(("locate-multi", rc == 1 and out.strip().startswith("LOCATED count=6 ")))
rc, out, err = run(p1, "--locate", "DECOY"); res.append(("locate-absent", rc == 1 and out.strip() == "LOCATED count=0 offset=-1"))
np_ = os.path.join(WD, f"{tok}-plain.docx"); open(np_, "w").write("not a zip")
for label, path in [("refuse-notzip", np_), ("refuse-norels", pkg(f"{tok}-2.zip", {"word/document.xml": doc1})),
    ("refuse-missing-target", pkg(f"{tok}-3.zip", {"_rels/.rels": rels("word/nothere.xml"), "word/document.xml": doc1})),
    ("refuse-nonword", pkg(f"{tok}-4.zip", {"_rels/.rels": rels("xl/workbook.xml"), "xl/workbook.xml": "<workbook xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'/>"})),
    ("refuse-escape", pkg(f"{tok}-5.zip", {"_rels/.rels": rels("../x.xml"), "word/document.xml": doc1}))]:
    rc, out, err = run(path); res.append((label, rc == 2 and out == "" and err.startswith("REFUSED")))
for k, ok in res: print(f"{k}={'PASS' if ok else 'FAIL'}")
print(f"PROBE={sum(ok for _, ok in res)}/{len(res)}")
```

`/tmp/r52close/indep.py` (`python3 indep.py <raw> <quote>...` prints the main part, the text-form length and `count find quote` per quote):

```python
import sys, zipfile
from xml.dom import minidom
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"; MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
z = zipfile.ZipFile(sys.argv[1]); rels = minidom.parseString(z.read("_rels/.rels"))
tgt = [r.getAttribute("Target").lstrip("/") for r in rels.getElementsByTagNameNS("*", "Relationship") if r.getAttribute("Type").endswith("/officeDocument")][0]
d = minidom.parseString(z.read(tgt)); out = []
def walk(n):
    for c in n.childNodes:
        if c.nodeType != c.ELEMENT_NODE: continue
        if c.namespaceURI == MC and c.localName == "Fallback": continue
        if c.namespaceURI == W and c.localName in ("tab", "br", "cr") and c.parentNode.namespaceURI == W and c.parentNode.localName == "r":
            out.append({"tab": "\t", "br": "\n", "cr": "\n"}[c.localName])
        if c.namespaceURI == W and c.localName == "t":
            out.append("".join(x.data for x in c.childNodes if x.nodeType in (x.TEXT_NODE, x.CDATA_SECTION_NODE))); continue
        walk(c)
        if c.namespaceURI == W and c.localName == "p": out.append("\n")
walk(d.documentElement); t = "".join(out); print(tgt, len(t))
for q in sys.argv[2:]: print(t.count(q), t.find(q), q)
```
