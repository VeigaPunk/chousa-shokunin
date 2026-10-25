# ReopenS099 — S099 (ERIC EJ1372738) re-opened and attacked
seat: ReopenS099 (leaf, wave 2 FALSIFY) · date: 2026-10-25
item attacked: lane row **S099** — `https://eric.ed.gov/?id=EJ1372738`, row `corpus/SOURCES.md:109`, 3 rows in
`corpus/evidence/round49/spans.tsv:12-14`, cited by `corpus/knowledge/aggregator-vs-source-r36.md:7,39-43,65-70,80`
lane rev read: `87e9335` (`git rev-parse master`); corpus/tools bytes identical to measured `4ce61fc5`
(`git diff --stat 4ce61fc5 master -- corpus/ tools/` → only `measure-after.txt`, 103 +). No network; only `.qcache`
captures. Scratch `/dev/shm/chousa-r49-ReopenS099`, deleted at the end.
## (1) capture key, file digest, form, exact slice, exactly-once
```
$ K=$(printf '%s' 'https://eric.ed.gov/?id=EJ1372738' | sha256sum | cut -c1-24); ls -la $K.*; sha256sum $K.*
key=32d1d24b24fce96d2a078ec0     .txt 2796 bytes   .raw 14258 bytes
410a6d926d3f724c834dadfa63535b7c85cd75366d0df99b03918b8dd65c36a4  32d1d24b24fce96d2a078ec0.raw
0288da6eab57c4284d44bef19694b0ab23ac0fbd47ab173f5ecd572a72cfeb7b  32d1d24b24fce96d2a078ec0.txt
```
`capture_sha256` in all three S099 rows is `0288da6e…` = the **.txt** digest → form = `.txt`, UTF-8 (the `.raw`
digest `410a6d92…` is not recorded, so the UTF-16LE path is correctly not taken). `/dev/shm/chousa-r49-ReopenS099/
verify_s099.py` decodes the form whose FILE digest equals the recorded one, translates newlines exactly as
`build-spans.form_texts`/`c2-count.form_text` do, then compares slice, raw-byte slice, multiplicity and anchors:
```
$ TMPDIR=/dev/shm/chousa-r49-ReopenS099 python3 verify_s099.py
key        sha256(url)[:24] = 32d1d24b24fce96d2a078ec0
form file  32d1d24b24fce96d2a078ec0.txt  bytes=2796  sha256=0288da6eab57c4284d44bef19694b0ab23ac0fbd47ab173f5ecd572a72cfeb7b
S099 rows  3
S099-1.txt: digest->.txt (utf-8)  offset=1155 len(span)=259 len(quote)=99 words=17
  form[offset:offset+len(span)] == span text -> True ; capture bytes[1225:1484] == span bytes -> True
  quote count in form = 1 ; quote in span = True ; span longer = True
S099-2.txt: offset=1403 len(span)=290 len(quote)=130 words=22
  form[offset:offset+len(span)] == span text -> True ; capture bytes[1473:1763] == span bytes -> True
  quote count in form = 1 ; quote in span = True ; span longer = True
S099-3.txt: offset=1614 len(span)=239 len(quote)=79 words=12
  form[offset:offset+len(span)] == span text -> True ; capture bytes[1684:1923] == span bytes -> True
  quote count in form = 1 ; quote in span = True ; span longer = True
ALL_STRUCTURAL_LEGS=PASS
```
Byte note: the .txt is CRLF (75 `\r\n`), so translated char offsets ≠ file byte offsets; `bytes[1225]` = translated
char `1155`, and all three spans sit inside line 104, so the byte slice also equals the LF-only span file. Both
readings hold. Form probe: the `.txt` is a tag-free extraction (`"<div"==0`, `"<script"==0`), so I checked the
quotes against the server-byte `.raw` (HTML, entity-escaped): `raw_html_count=3 txt_count=1` for each quote, raw
sites at 784/1769/9173, each preceded by `Students practiced the heuristic of &quot;lateral reading&quot;:`. The
extraction does not invent the text; the `.raw` carries it 3×, which is why the exactly-once rule is per form.
## (2) Registry row: `char N` anchors, `teaches`, `scope`
```
anchor cell: the abstract on ERIC record EJ1372738 (capture .txt); located quotes char 1235, char 1483, char 1694
anchor chars [1235, 1483, 1694] vs located quote starts [1235, 1483, 1694]
  char 1235: form[1235:1334] == quote -> True ; char 1483: True ; char 1694: True
```
All three `char N` are located quote offsets in the same translated-char space the frozen counter uses
(`c2-count.py:187-188`: `int(offset)+span.find(quote)` = `1155+80=1235`). The spans.tsv `offset` column is the
**span** start (quote at +80 = `CONTEXT`), not the quote start — the counter's own convention, not an anchor
defect; my recomputation reproduces all three anchors, and `build-spans.py` prints the same numbers.

`teaches` — carried by the capture (line 104, chars 1043-1977), clause by clause:
- "the heuristic taught is lateral reading - leaving an unfamiliar website … at hand" ← `Students practiced the heuristic of "lateral reading": leaving an unfamiliar website to search the open Web before investing attention in the site at hand.` (small narrowing: the abstract says students were taught "online evaluation strategies", plural, of which lateral reading is the one named; cell writes "open web" lower-case vs capture "open Web" — paraphrase in a non-quote cell.)
- "matched-control study (n=271 against n=228)" ← `…students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.`
- "experimental students grew significantly in their ability to judge the credibility of digital content" ← verbatim, same sentence.

`scope` — **one clause the capture does not carry: "APA paywalls the full text".** The record carries (a) a
*search-filter* checkbox `<input type="checkbox" name="ft" /> Full text available on ERIC` (raw[5850:6150] — a
site filter, not a statement about EJ1372738), (b) `Direct link` to `http://dx.doi.org/10.1037/edu0000740`
(raw[6950:7250]), (c) `order@apa.org` / `http://www.apa.org` in the publisher meta (raw[3900:4300],
raw[10550:10750]). Probe: `pdf mentions: []`, `ed.gov/fulltext: []`, `citation_pdf_url`/`citation_doi` meta none,
`paywall`/`Pay` 0 hits. So the capture shows *no full text attached to this record* and nothing about APA's access
model: "paywalls" is an unmarked outside-the-capture inference in a registry cell. The operative half, "scoped to
the statements in the abstract", is supported — the capture holds the abstract only, complete (934 chars, ends
`…make wise decisions about the information that darts across their screens.`, `t.count("…")==0`). "distinct from
the lane's held SIFT row S003" is lane bookkeeping and true (S003 = hapgood.us Caulfield). Everything else is
carried: title, `v114 n5 p893-909 Jul 2022`, the five authors, ERIC number.
## (3) Every entry sentence citing S099 (`aggregator-vs-source-r36.md`)
| line | sentence (abridged) | capture text | grade |
|---|---|---|---|
| 39 | "**Reading a source *about* the source (Western).**" | — | label, not a capture claim; "(Western)" is a lane grouping tag |
| 39-41 | "The ERIC abstract of a district-wide field study defines lateral reading as `leaving an unfamiliar website … at hand`" | title "A District-Wide Field Study…"; "In a study conducted across an urban school district… Students practiced the heuristic of \"lateral reading\": leaving an unfamiliar website…" | **supported** (the colon-gloss is the abstract's own definition) |
| 42 | "reports \"Using a matched control design, … regular classrooms.\"" | verbatim, chars 1483-1613 | **supported** |
| 43 | "says treatment students \"grew significantly in their ability to judge the credibility of digital content\"" | "A multilevel linear mixed model showed that students in experimental classrooms grew significantly…" (1694-1773) | **supported** — the abstract itself calls that group "treatment classrooms" in the preceding sentence, so "treatment students" is not a substitution |
| 65-67 | "S099 gives that kind of move a concrete, field-tested procedure" | "field-tested" ← "A District-Wide Field Study"/"across an urban school district"; but the abstract names a **heuristic**, never a procedure, and describes a curriculum ("six 50-minute lessons") | **narrower** — "concrete … procedure" is the lane's gloss |
| 68-70 | "…the one method here that produces evidence about a source from outside the source; S099 is read at abstract level only" | capture is the abstract page only | second clause **supported**; first is lane inference (section marked Inference) |
| 7 | "the abstract on ERIC record EJ1372738 — capture 2026-10-23, re-opened 2026-10-25" | capture mtime 2026-10-23, digest unchanged at re-open | **supported** |

No sentence attributes to S099 anything about citation indexes, reference lists or counts; S099 is used only for
the outside-the-source method, which is what the abstract carries.
## (4) Context of the quotes (lifted or not?)
Spans (80 chars each side) keep the framing sentence in every case:
- 1: `…professional fact checkers. Students practiced the heuristic of "lateral reading": [quote]. Professional development was provided…` — the entry reads it as the definition; the colon gloss is exactly that. **Consistent.**
- 2: `…six 50-minute lessons in a district-mandated government course. [quote] A multilevel linear mixed model showed…` — quoted whole, including "Using a matched control design". **Consistent.**
- 3: the quote is the tail of `A multilevel linear mixed model showed that students in experimental classrooms grew significantly…`; it omits its subject, but the entry supplies the correct one ("treatment students" = "students in experimental classrooms"). **Consistent, not lifted**; the only reading the abstract does not license is "field-tested *procedure*" (item 3).
## Post-freeze builder change, as it touches S099

`git diff fe740e78 4ce61fc5 -- corpus/evidence/round49/build-spans.py` adds one branch guarded by
`if fname.endswith(".raw")` (CR-clipping of raw-form context); the `.txt` path is byte-unchanged, so the erratum's
repair cannot move my row. Reproduction of the committed manifest from `quotes.tsv` with the post-freeze builder,
read-only (`--check` writes nothing), on a scratch copy; then the frozen counter from the lane checkout:
```
$ python3 corpus/evidence/round49/build-spans.py --root /dev/shm/chousa-r49-ReopenS099/root --check
SPANS_ROWS=28 STALE=0   exit=0
$ python3 corpus/evidence/round49/c2-count.py | tail -30
BOUND=8/9 (min 7) REFUSED=1   BOUND_IDS=S096,S097,S098,S099,S100,S101,S102,S103
QUOTE_ROWS=28 ON_BOUND=28/28   SPAN_IDS=8/8   QUOTES_IN_SPAN=28/28   QUOTES_IN_ENTRY=28/28
QUOTES_IN_LESSON=28/28   QUOTE_SHORT=28/28   SPAN_CONTEXT=28/28   CAPTURE_BOUND=28/28
ANCHOR_BOUND=8/8   INFERENCE_GROUNDED=2/2   QUARANTINE_VERDICTS=5/5   C2=PASS
```
`CAPTURE_BOUND=28/28` and `ANCHOR_BOUND=8/8` agree with my independent recomputation; S099 contributes 3/28 of the
capture leg and is inside the anchor leg.
## Findings, risks, calibration

- **Holds:** capture key, form selection, file digest, all three exact slices (text and byte level), exactly-once
  in the recorded form, quotes present verbatim in the server-byte `.raw` too, span longer than quote, all three
  anchors located, `teaches` fully carried, every quoted sentence supported, context not lifted, builder
  reproduces the manifest.
- **Defect (calibration, scope cell only):** "APA paywalls the full text" is not carried by the capture and is not
  marked as inference; the scoping it justifies is correct on the capture's own evidence (no full text attached),
  but the *reason* is unobservable from the opened source.
- **Defect (minor, entry wording):** "concrete, field-tested procedure" (`aggregator-vs-source-r36.md:65-66`) — the
  capture says *heuristic* and a classroom intervention.
- **Minor:** `teaches` "open web" vs capture "open Web"; `(Western)` is a lane label; the `.txt` form is a derived
  extraction, so its digest binds the extraction, not the server bytes — closed with the `.raw` check (3×
  verbatim), which the frozen counter does not require.
- **No blocker.** Nothing here changes a frozen predicate, target or counter.

`rm -rf /dev/shm/chousa-r49-ReopenS099` — scratch removed; no production file, index or jj state touched.
VERDICT: S099 (ERIC EJ1372738) — partly — every structural leg (key, digest, form, slice, exactly-once, anchors), the `teaches` cell and all quoted entry sentences hold against the capture, but the `scope` cell's "APA paywalls the full text" is not carried by the capture and the entry's "concrete, field-tested procedure" is a gloss on the abstract's "heuristic".
