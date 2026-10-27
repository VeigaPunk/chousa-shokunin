# R53DraftCorrections — round-52 routed defects 1 and 2, drafted append-only

seat: `R53DraftCorrections` (chousa round 53, wave 1) · date 2026-10-26
lane HEAD when read: `6365f15b64b89d1ad1ac66fe7d7b81c92e74d90f`
Read first: `corpus/evidence/round53/claims.md` (C1 and C2 frozen). I propose no change to a predicate, target, counter or control; nothing below touches either claim. Routed items: `corpus/lessons/round-52-verifier-spotcheck.md:92` (defect 1) and `:93` (defect 2).
Scratch `/fast/scratch/hyaku/chousa-r53/R53DraftCorrections` (`TMPDIR` set there, removed at the end); no network; no counter run; the only file written is this report.

## 1. Defect 1 — the stale erratum range (`E1–E4` for round 52)

### 1.1 Every place

```
$ grep -n 'E1–E4' corpus/lessons/round-52.md SCORECARD.md LOG.md
corpus/lessons/round-52.md:153:`corpus/evidence/round52/claims-erratum.md` E1–E4: the C1 supplement (post-freeze, reported beside the frozen counter), four tool changes outside the frozen predicate (non-Word main parts, size bound, root-escaping targets, element clearing), the reader divergence on an External relationship (named, not changed), and the frozen C2 counter's named limits.
SCORECARD.md:2664:Claims frozen in `corpus/evidence/round52/claims.md` at `37468eadd8d098e80289b2f31a22de3872d4a1f6` after scoring their do-nothing controls; post-freeze disclosures `corpus/evidence/round52/claims-erratum.md` E1–E4. After-measurement: …
$ grep -c 'E1–E4' LOG.md
0
```

Two places, one token each (`line.count('E1\u2013E4')` = 1 on both, U+2013 en dash, checked byte-exact with `in` on the literal). An ASCII-hyphen variant sweep (`grep -rn 'E1-E4' SCORECARD.md LOG.md corpus/ README.md SKILL.md`) gives one hit, `SKILL.md:133`, and it is a round-**51** statement (`corpus/evidence/round51/claims-erratum.md`) — see §3.2, not a round-52 place.

### 1.2 The real range

`grep -n '^#\|^\*\*E[0-9]'` matched only the heading, because the bullets begin `- **E1 —`; the sweep that works:

```
$ grep -n '^- \*\*E[0-9]' corpus/evidence/round52/claims-erratum.md
7:- **E1 — C1 supplement (post-freeze, not the claim's rule).** …
14:- **E2 — tool changes after the candidate `804a4537` (outside the frozen predicate).** …
27:- **E3 — named, not changed: the two readers diverge on an External officeDocument relationship listed …
32:- **E4 — named limits of the frozen C2 counter (W1 `R52CritForgeC2`).** …
36:- **E5 — in-round narrowing after W2 (outside the frozen counters).** …
40:- **E6 — named, not changed: the frozen span builder's reader is unbounded.** …
```

Six entries, E1–E6. The range is not the only defect: the prose at `round-52.md:153` enumerates E1–E4's *content* (supplement, tool changes, reader divergence, C2 limits) and therefore discloses nothing of E5 (the in-round narrowing that made the manifest 39 rows) or E6 (`build-spans.py`'s unbounded reader). A range-only edit would still leave those two undisclosed, which is why the draft below names them.

### 1.3 The form I matched

`SCORECARD.md:2622` `## Round 51 pointer corrections (append-only; no row above is edited)`; its preamble: "Each line names the row's line number, the bare pointer it prints and the committed non-empty file it meant"; sample `SCORECARD.md:2629` `correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py`. The lane's other idiom (`corpus/evidence/round50/stale-count-check.py:21`, `correction:.*superseded by`) closes a stale `LOG.md` line and does not fit a range token.

### 1.4 Draft — lane path `SCORECARD.md`, appended as a new section after the round-52 verdict (line 2664 is never rewritten)

```markdown
## Round 52 pointer corrections (append-only; no row above is edited)

correction: SCORECARD.md:2664 E1–E4 -> corpus/evidence/round52/claims-erratum.md (the range is E1–E6: E5 in-round narrowing, E6 unbounded span-builder reader)
correction: corpus/lessons/round-52.md:153 E1–E4 -> corpus/evidence/round52/claims-erratum.md (the range is E1–E6: E5 in-round narrowing, E6 unbounded span-builder reader)
```

### 1.5 What a reader consumes (finding, not a patch)

Tested against the only machine reader of this form, `corpus/evidence/round51/c3-count.py:41` `CORR = re.compile(r"^correction: SCORECARD\.md:(\d+) (\S+) -> (\S+)")`:

```
line 1 -> ('2664', 'E1–E4', 'corpus/evidence/round52/claims-erratum.md')  real(g3)= True   (4,255 B file)
line 1 with target 'E1–E6' -> ('2664', 'E1–E4', 'E1–E6')                  real(g3)= False
lesson line ('correction: corpus/lessons/round-52.md:153 …')             -> None
```

So: (a) the lesson line is prose-only — the regex hardcodes the `SCORECARD.md:` prefix; (b) the erratum path as target parses and passes `real()` (`c3-count.py:105-118` requires `real(root / tgt)`), but the resolver only consults corrections for a *dangling path-like pointer in a `## Capabilities` row's third cell or an indented `SHONEN.md` line* (`scorecard_rows`/`shonen_lines`), and line 2664 is verdict prose outside any Capabilities section (`grep -c 'E1' SHONEN.md` → 0). Neither correction is consumed by any lane reader today; the deliverable is the audit trail, and the L1 decides whether to add a reader.

## 2. Defect 2 — the grey-literature-r40 refusal reason

### 2.1 "S133 duplicates the S111 URL" — verified, one URL, one key

```
$ python3 (regex over SOURCES.append.md, first URL per row, sha256[:24])
line 36 S111 url=https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3  key=453d492becd9a2f4632cb8dd
line 58 S133 url=https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3  key=453d492becd9a2f4632cb8dd
$ grep -n '^\| S111 ' corpus/SOURCES.md (line 121)  url=https://www.sinomed.ac.cn/article.do?ui=2026335073  key=42bac8830527d6f1bb125c49
$ lane row S113 (corpus/SOURCES.md:123)             url=https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3  key=453d492becd9a2f4632cb8dd
```

The staged pair is one page; the lane already bound that page as **S113**, while lane **S111** is a different document (SinoMed). §2.5.

### 2.2 The closure's decode evidence — verified

```
$ python3: b=open('.qcache/bdff491a75c6abeda1d9c01d.raw','rb').read(); t=b.decode('utf-16le','replace')
bytes 243929 magic d0cf11e0a1b11ae1
chars 121964 FFFD 887
quote 是否检索灰色文献 count 1 find 57497
ctx '被排除。\r2.文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。\r3.文献筛选：…'
灰色文献 count 7 · 检索策略 count 11
$ sidecar .qcache/bdff491a75c6abeda1d9c01d.txt: chars 241510, 是否检索灰色文献 count 0, 灰色文献 count 0
```

Once, at decode offset 57497, inside the guideline's report-writing rule `2.文献检索策略` — a requirement on what the *search record* must state, so the headline is in province. The `.txt` sidecar carries neither string, matching `round-52.md:64`. The decode is not a defined text form (the closure's own §6.2 warning), so I mint no manifest quote from it; the offset is a decode offset, not a span offset.

### 2.3 Where currency sits in the staged entry

`knowledge/corpus/knowledge/grey-literature-and-chinese-search-record-r40.md` (read-only package): line 2 is the headline `# A Chinese regulator requires the search record to state whether grey literature was searched`; line 8 is the `recheck:` line naming `是否检索灰色文献等关键问题`; the currency doubt is an `#### Unknown` bullet at line 72, `- **Whether the NMPA guideline is still the current one was not checked.**`. So the round-52 cell `**out of province for its spine** (a regulator instrument's currency)` mislocates the spine: the spine is the field requirement, currency is one Unknown bullet.

### 2.4 Draft — lane path `corpus/lessons/round-53.md` (Gate row for this entry; the round-52 header's seven columns are `staged entry | documents (S-ids) | capture on disk (key, size) | province fit | decision | reason | flip`)

```markdown
| `grey-literature-and-chinese-search-record-r40.md` | S130, S131, S133 | S130 `bdff491a75c6abeda1d9c01d` (`.raw` 243,929 B OLE `.doc`; UTF-16LE decode 121,964 chars, 887 U+FFFD, `是否检索灰色文献` once at 57497 — a decode, not a defined text form; `.txt` sidecar 241,510 chars carries neither string); S131 `27d4865f201e99c1fed9f79b` (`.txt` 1,673 chars); S133 `453d492becd9a2f4632cb8dd` = staged S111's key | **in province**: a search-record field — the report must state whether grey literature was searched (`是否检索灰色文献等关键问题`, S130 decode 57497) | **refuse** | S133 duplicates the S111 URL; outside the frozen by-document set. Staged `SOURCES.append.md:36` and `:58` carry one URL, `…/guideline/show_article.do?id=23e481c0052069d3`, one key `453d492becd9a2f4632cb8dd`, so a second row would give two lane rows for one page and break `exactly one lane Registry row whose FIRST source-cell URL is the document's URL`; the 2019 NMPA guideline is outside round 53's frozen by-document set. Currency is the entry's own `Unknown` bullet (line 72), not its spine | unchanged as a refusal: the S133 duplicate stays out; currency is settled by the owning lane on its own source, kept as an `Unknown` |
```

### 2.5 Numbering caveat in the routed sentence (finding)

The Gate table's `documents (S-ids)` column uses **staged** ids throughout — `round-52.md:60` maps staged `S111, S112` to lane `S113, S114` — so "S133 duplicates the S111 URL" is correct *inside that convention*. Read with lane ids it is false and misleading: lane S111 (`corpus/SOURCES.md:121`) is the SinoMed record (key `42bac8830527d6f1bb125c49`), and the round-52 flip cell's "S133 is dropped in favour of the S111 row" then points at the wrong document. Recommend the lesson write `staged S111 (lane S113)` once, in the reason cell, so the sentence survives both conventions:

```markdown
S133 duplicates staged S111's URL (lane row S113); outside the frozen by-document set.
```

## 3. Out of scope, seen, and deliberately not touched

1. `corpus/lessons/round-52-verifier-spotcheck.md:92` itself prints `E1–E4` — it is quoting what the two places say, so correcting it would falsify the closure's description. Left alone.
2. Adjacent, a different round: `SKILL.md:133` states round-51 errata as `E1-E4` (ASCII hyphen), while `corpus/evidence/round51/claims-erratum.md` carries `## E1`…`## E5` (lines 5, 31, 35, 39, 43 — five). Not a round-52 statement; reported, not drafted.
3. Seven tracked process reports print the round-52 stale range and are append-only wave artifacts, not product statements: `.ufo/waves/round-52/w2/` `R52W2ReviewLesson.md:79`, `R52W2ReviewReadme.md:34`, `R52W2ConnCrossEntry.md:7`, `R52W2DraftLogEntry.md:32`, `R52W2ReopenRowS116.md:39`, `R52W2MutSupplement.md:4`, `R52W2DraftScorecardVerdict.md:95`. No correction drafted for them; naming them here is the sweep's completeness record.
4. No production file, no other seat's report, no git index or jj state touched; no counter run (both are the claim seats' ground); no install needed, so no tool recorded.

VERDICT: drafted two append-only `correction:` lines (SCORECARD.md:2664 and corpus/lessons/round-52.md:153, both `E1–E4 -> claims-erratum.md`, real range E1–E6) and the round-53 Gate row restoring the grey-literature-r40 refusal to its real ground (one URL, key `453d492becd9a2f4632cb8dd`, outside the frozen set; headline in province) after verifying `是否检索灰色文献` once at UTF-16LE decode offset 57497 — and found that no lane reader consumes either correction line and that the routed sentence's `S111` collides with the lane's SinoMed S111.
