# R52DraftMistakes — draft `## Mistakes` rows for `corpus/lessons/round-52.md`

seat: R52DraftMistakes (scribe, round 52 wave 1) · date: 2026-10-26 · leaf member, no subagent dispatch
lane: /home/vgpnk/Projects/shokunin/chousa-shokunin (read-only for this seat except this file)
inputs read: `corpus/lessons/round-51.md`, `corpus/lessons/round-51-verifier-spotcheck.md`, `LOG.md:1823-1836`,
`corpus/QUALITY.md:800-808` (criterion 76), `corpus/evidence/round51/{c1-count.py,controls/forge-dirname.py}`,
`corpus/evidence/round52/{claims.md,c1-count.py,controls/*}`, `corpus/evidence/round50/decode-form-check.py`,
capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.{raw,txt}`
(key = `sha256("https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx")[:24]`, recomputed).
No network, no fetch, no install (pacman paused host-wide; nothing installed). Scratch
`/fast/scratch/hyaku/chousa-r52/R52DraftMistakes` (TMPDIR), removed at the end; every output below is pasted here.

## 1. Behaviour verified (item 1 — capture form before a refusal)

The round-51 refusal is in the lesson, not only in the report: `corpus/lessons/round-51.md:55` (the `.docx`'s text
"exists only inside the DEFLATE member `word/document.xml`"), `:57` (`refused this round for its capture form, not
for its source quality`, with the flip = a counter/builder that reads a zip member), and `:89`, the located-quote row
`SRにおける文献検索期間について明記する。  char 39411  form .raw unzipped → word/document.xml UTF-8  <url>`.

**Which criterion should have required a text form before the refusal:** **QUALITY 76** (`corpus/QUALITY.md:800`) is
the only criterion that names a capture form, and it did *not* bite: its check is name-based **per file**.
`python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-51.md` → `FORM_NAMED … DECODE_FORM=PASS`
rc=0, because line 8 names "`.txt` read as UTF-8"; the checker never opens the capture
(`corpus/evidence/round50/decode-form-check.py:9`, named limits: "one naming per file, not one per offset; … the
check cannot open the capture"). The row's form is a zip member no lane tool reproduces — so the refusal stood on a
reading nothing in the lane could re-run, which is exactly what criterion 76 exists to prevent. No criterion covers
it today (66 covers entries, not refusals) → proposed **87** in row A.

**The cheap member-strip form is wrong on this file** (`doc.xml` = `unzip -p <raw> word/document.xml`, 1464476 bytes;
`.txt` sidecar = 319599 bytes):

```
$ grep -o 'w:instrText' doc.xml | wc -l        → 100   (50 elements: 50 open + 50 close)
$ grep -o 'mc:Fallback'  doc.xml | wc -l       → 120   (60 elements: 60 open + 60 close)
$ grep -o '<w:tab w:' doc.xml | wc -l          → 13    (w:pPr/w:tabs tab stops)
$ grep -o '<w:tab/>'  doc.xml | wc -l          → 49    (run-level tabs: the only ones the rule emits)
```
naive member-strip (`corpus/evidence/round52/controls/naive-tool.py`) vs the lane rule (`tools/capture-text.py`):

```
good chars 19682   naive chars 21910            (ratio 1.11)
'PAGE'   naive 49  good 0      'REF ' naive 49  good 0      'TOC \' naive 1  good 0
tabs     naive 62  good 49     (13 tab stops become tab characters)
naive minus mc:Fallback   → 21805 (delta 105)
naive minus w:instrText   → 20613 (delta 1297)   both dropped → 20508 (delta 1402)
lines 797, distinct 668, lines occurring >1: 73   (e.g. '□ 追加的有用性が示されている' twice)
quote offset: good 8996 · naive 10319 · member XML find() = -1 (tags split the sentence)
```
So the reader one would write casually injects 1297 characters of field instructions (`PAGE`, `REF`, `TOC \`), 105
characters of `mc:Fallback` content and 13 phantom tabs on **real** data, duplicates 73 lines, and lands the quote at
an offset the lane form does not have. Cheap-form controls on the frozen round-52 counter (my runs):
`naive-tool.py` → `LEGS=4/9` `REAL=PASS … locate=(0, 1, 10319) chars=21910`; `cache-txt-tool.py` → `LEGS=0/9`;
`const-tool.py` → `LEGS=0/9`; the tool → `LEGS=9/9 C1=PASS` with `REAL=PASS … locate=(0, 1, 8996) chars=19682`.

## 2. Behaviour verified (item 2 — fixed names in the round-51 counter vs the round-52 one)

Round-51 counter (routed defect 1, spot-check `:100`): subtest directories are literals —
`corpus/evidence/round51/c1-count.py:141` `tmp / "s"`, `:158` `"s-all"`, `:167` `"d1"`, `:174` `"d2"`,
`:189-191` `"renamed-heading" | "no-heading" | "row-outside"`; the forge reads the name it is given
(`corpus/evidence/round51/controls/forge-dirname.py:29` `scene = out.parent.name`). My run:
```
$ python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py
REGISTRY_STRUCTURE=PASS 4/4 … LEGS=5/5  C1=PASS   rc=0
```
Round-52 counter has no fixed per-subtest names:
```
$ grep -nE '"(s|s-all|d1|d2|renamed-heading|no-heading|row-outside)"' corpus/evidence/round52/c1-count.py
(no subtest-directory match; the only literals are the leg labels at :57 `LEGS = ("PARAS", …)` and the :269 `gens` dict keyed by them — printed, never passed to the tool)
work = tempfile.mkdtemp(prefix="c1r52-", dir=a.work)   (:267)   rmtree in finally (:329)
files = work / (g.name() + ext)  :248-250   Gen.name() = 5-12 chars of [a-z0-9]  :77-78   ext ∈ {.raw,.docx,.bin,""}  :262
```
A dirname-keyed forge in the round-51 shape (scratch: record `argv[1]`, print a canned body keyed on
`Path(argv[1]).parent.name`, answer `--locate` with `count=1 offset=0`; ~20 lines, removed with the scratch) scores
`LEGS=0/9 C1=FAIL`, and the paths it was handed witness the randomness: 9 distinct inputs, all inside one `c1r52-gz2utrot` mkdtemp —
`47wubojwstt.bin · 4zr5g.bin · 5drczr1ko25.bin · 8sds0fo8f · cxdnvlxj.bin · d66xfa1.docx · sn5qsshyfvs.bin ·
zex680.raw` (+ the pinned capture). Residual limit: `REAL_RAW` is a fixed absolute path (`:46`), so a tool keyed on it
scores the REAL leg alone — measured `LEGS=1/9 C1=FAIL` (`REAL=PASS … locate=(0, 1, 0) chars=21`).

## 3. Behaviour verified (item 3 — r51 report/lesson vs spot-check §4/§6, LOG round-51)

Two calibration defects the spot-check did not catch, both in `corpus/lessons/round-51.md`:

1. **`:89` `char 39411` indexes nothing.** In the named form the sentence is split across runs, so
   `doc.xml.find('SRにおける文献検索期間について明記する')` = **-1**; the `w:t` concatenation (18478 chars, the number the
   spot-check `:85` quotes) gives **8417**; the round-52 form gives **8996** (the counter's own REAL line). Bytes
   `doc.xml[39380:39440]` = ` w:rsidRPr="003A0822"><w:rPr><w:rStyle w:val="a3"/><w:noProo…` — run properties.
   `round-51-verifier-spotcheck.md:85` accepted the row ("agree, with a note") after checking that the quote *exists*,
   not that the offset is its offset; §4's own `char 8997` shows the convention used elsewhere.
2. **`:87` and spot-check `:82` label the same kind of form `.raw` "decoded UTF-8" under two newline rules.**
   Capture `42bac8830527d6f1bb125c49.raw` (20142 bytes, 473 CRLF): `read_text` (universal newlines,
   17523 chars) puts `R-05;R-37;R348.3;R916.3` at **9034** and `学科分类号` at **8997** (the spot-check's number); a
   CRLF-preserving read (17996 chars) puts them at **9302** (the lesson's number) and 9264. Both rows say "UTF-8".
   Three further rows (`:79`, `:83`, `:85`) use `form DEINT` (a seat's de-interleave; disclosed at lesson `:8`) that
   no lane tool reproduces, so their offsets are not re-checkable either.
3. Consistent, not a defect: lesson `:55`'s numbers reproduce exactly — `.txt` 168952 characters, 72117 U+FFFD,
   0 occurrences of `検索`; the spot-check `:105` item 6 (`zero.txt` removed) holds — `ls corpus/evidence/round51/zero.txt`
   → No such file. `LOG.md:1828` ("its text exists only in a compressed zip member the frozen span pipeline cannot
   read") is accurate and matches the lesson; the round-51 frozen counter's own weakness is disclosed at lesson `:22`.
4. New this round, and it would land a wrong lesson: **criterion 76's check cannot name the round-52 form.** A probe
   lesson whose form line reads "the .raw read through `tools/capture-text.py` (a zip member decoded as UTF-8, LF
   only)" prints `FORM_MISSING … DECODE_FORM=FAIL`, rc=1 — `FORM_LINE` matches only `utf-8-sig`, `UTF-16LE`, or
   `.txt`…`UTF-8` (`corpus/evidence/round50/decode-form-check.py:14`). Row B.
5. New this round, claim-level: the frozen round-52 C1 **REAL leg is self-consistency only**
   (`c1-count.py:322-327`: `good = rc==0 and txt.count(QUOTE)==1 and loc == (0,1,txt.find(QUOTE))`), so it accepts the
   naive form (`REAL=PASS … chars=21910`) as readily as the correct one (`chars=19682`): the leg meant to ground "the
   `.docx` is readable in the lane form" cannot tell the two forms apart. Row D (supplement, not a predicate change).

## 4. Draft rows — `corpus/lessons/round-52.md` `## Mistakes` (for the L1 to append; not written here)

```markdown
| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. capture-form / ungated refusal: round 51 refused the NIPH `.docx` (staged S125) as unreadable in the two frozen forms while its text was readable from `word/document.xml`; the only capture-form criterion (76) checks a lesson's *file*, not each located row, so an ad-hoc form passed, and the obvious member-strip reading is wrong on this very file | `corpus/lessons/round-51.md:55,57,89` (refusal + flip + `form .raw unzipped → word/document.xml UTF-8`); `corpus/QUALITY.md:800` (76, whose own limit is "the check cannot open the capture"); `corpus/evidence/round52/controls/naive-tool.py` scored `LEGS=4/9` on the frozen round-52 counter (my run) | R52DraftMistakes, from the pinned `.raw` (`3a8b4597….raw`), sha9 `sha256(url)[:24]` recomputed | `tools/capture-text.py` (the `_rels/.rels` officeDocument part; `w:t` text; run-level tab/br/cr; newline per `w:p`; nothing from `mc:Fallback`/`w:delText`/`w:instrText`/`w:pPr/w:tabs`) + new criterion **87**: a capture-form refusal names a text form **a lane tool reproduces** and the command that prints it, per row. Shown able to fail: `python3 corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/naive-tool.py` → `LEGS=4/9 C1=FAIL` (`REVISIONS=FAIL text differs at 9`, `LAYOUT=FAIL`, `ALTCONTENT=FAIL`, `MAIN_PART=FAIL`, `REFUSE=FAIL norel not refused`) and `char-anchor-check.py corpus/lessons/round-51.md <cache>` → `ADHOC_FORM corpus/lessons/round-51.md:89 form='form .raw unzipped → word/document.xml UTF-8'` + `CHAR_ANCHORS rows=6 bad=5`, rc=1 |
| 2. calibration / criterion gap: criterion 76's check cannot name the round-52 text form, so a lesson that names the tool correctly reads `FORM_MISSING` and one that names `.txt`-shaped words passes — the check grades vocabulary, not readability | probe lesson in scratch, form line "the `.raw` read through `tools/capture-text.py` (a zip member decoded as UTF-8, LF only)", `python3 corpus/evidence/round50/decode-form-check.py <probe>` → `FORM_MISSING … DECODE_FORM=FAIL` rc=1; `corpus/evidence/round50/decode-form-check.py:14` matches only `utf-8-sig|UTF-16LE|.txt…UTF-8`; and the same checker prints `FORM_NAMED DECODE_FORM=PASS` for `corpus/lessons/round-51.md`, whose `:89` form no tool reproduces | R52DraftMistakes | extend `FORM_LINE` to the tool form (`.raw` through `capture-text.py`) and make the check per located row (quote, offset, form) rather than per file; the row-level version is `corpus/evidence/round52/controls/char-anchor-check.py` (§5). Shown able to fail: on `corpus/lessons/round-51.md` with the capture cache → `OFFSET_MISMATCH …:87 says char 9302, find()=9034, count=1 form=form .raw decoded UTF-8`, `ADHOC_FORM …:89`, `CHAR_ANCHORS rows=6 bad=5`, rc=1 |
| 3. vacuous/attribution: the frozen round-51 C1 counter's subtest directories are fixed names, so a forge that reads the name it is handed and prints canned shapes scores it full | `corpus/evidence/round51/c1-count.py:141,158,167,174,189-191`; `corpus/evidence/round51/controls/forge-dirname.py:29`; routed defect 1 at `corpus/lessons/round-51-verifier-spotcheck.md:100`; my run: `python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py` → `LEGS=5/5 C1=PASS` rc=0 | R52DraftMistakes (re-ran the frozen counter rather than citing its receipt) | the round-52 counter draws the mkdtemp and every file name from the nonce (`c1-count.py:267,248-250,77-78`). Shown able to fail: a dirname-keyed forge in the round-51 shape against it → `PARAS=FAIL … REFUSE=FAIL bytes not refused`, `LEGS=0/9 C1=FAIL`; the inputs it saw were 9 distinct random basenames in one `c1r52-gz2utrot` directory. Named residual: `REAL_RAW` is a fixed absolute path (`c1-count.py:46`), so a tool keyed on it scores `LEGS=1/9 C1=FAIL` — one leg, not the claim |
| 4. vacuous (claim leg): the frozen round-52 C1 `REAL` leg validates self-consistency, not the text form, so the naive member-strip reading passes the leg meant to prove the `.docx` is readable in the lane form | `corpus/evidence/round52/c1-count.py:322-327` (`good = rc==0 and txt.count(QUOTE)==1 and loc == (0,1,txt.find(QUOTE))`); my run with the naive control → `REAL=PASS rc=0 count=1 locate=(0, 1, 10319) chars=21910` against the tool's `chars=19682`; `corpus/evidence/round52/claims.md:46` states the leg as "holds … exactly once and `--locate` agrees" | R52DraftMistakes | post-freeze **supplement** (predicate untouched, disclosed in `corpus/evidence/round52/claims-erratum.md`): pin `chars=19682` and the offset `8996` for the pinned capture, as `c1-supplement.py` did in round 51. Shown able to fail: the same supplement over the naive control must print `REAL=FAIL chars=21910 locate=(0,1,10319)`; today the frozen leg prints `REAL=PASS` for it |
| 5. calibration: the round-51 lesson's `.docx` quote row records an offset that is the offset of nothing — the sentence is split across runs, so it has no contiguous occurrence in the named form at all | `corpus/lessons/round-51.md:89` `char 39411`; `find()` in `word/document.xml` = **-1**; `w:t` concatenation (18478 chars) = **8417**; round-52 form = **8996** (also the round-52 counter's `REAL … locate=(0, 1, 8996)`); bytes 39380-39440 are run properties; accepted without an offset check at `corpus/lessons/round-51-verifier-spotcheck.md:85` | R52DraftMistakes | offsets are checked per row against the named form: `corpus/evidence/round52/controls/char-anchor-check.py` (§5). Shown able to fail on the row that motivated it: the checker reports the row's form as `ADHOC_FORM` (rc=1) and, forced to the tool form, `find()=8996 ≠ 39411`; on the same file it also prints `OFFSET_MISMATCH …:87 says char 9302, find()=9034` |
| 6. calibration: `.raw` "decoded UTF-8" is two forms (universal newlines vs CRLF preserved) and round 51 used both under one label, so offsets in the same file differ by 268 | `corpus/lessons/round-51.md:87` `char 9302` (CRLF-preserving read, 17996 chars) vs `corpus/lessons/round-51-verifier-spotcheck.md:82` `char 8997` (universal-newline read, 17523 chars) on the same `42bac8830527d6f1bb125c49.raw` (20142 bytes, 473 CRLF); three rows `:79,83,85` use `form DEINT`, which no lane tool reproduces (disclosed at lesson `:8`) | R52DraftMistakes | name the newline rule in every form, and prefer the tool form, which is LF-only on the pinned capture (`python3 tools/capture-text.py <raw>` → 19682 chars, 0 CR). Shown able to fail: `python3 -c` over the two reads of that capture prints `universal chars 17523 find 9034` / `newline="" chars 17996 find 9302` — one label, two offsets |
```

## 5. Draft check (fix of rows 1, 2, 5) — intended lane path `corpus/evidence/round52/controls/char-anchor-check.py`

Run in scratch as written below; output is §3/§4's. Refuses an ad-hoc form; an HTML `.raw` is read as UTF-8 (the lane's form, `corpus/lessons/round-51.md:8`), a zip `.raw` only through the tool.

```python
#!/usr/bin/env python3
"""char-anchor-check — every located-quote row of a lesson must satisfy text.find(quote) == the
recorded `char N` in the ONE form the row names, and that form must be one a lane tool reproduces (the
capture `.txt` as UTF-8, or a zip `.raw` through tools/capture-text.py; an HTML `.raw` as UTF-8).
Row shape: QUOTE <TAB> char N <TAB> form ... <TAB> url   (as in corpus/lessons/round-5*.md)."""
import hashlib, pathlib, re, subprocess, sys
def key(url): return hashlib.sha256(url.encode()).hexdigest()[:24]

def main():
    argv = sys.argv[1:]; lesson, cache = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    tool = pathlib.Path(argv[argv.index("--capture-text") + 1]) if "--capture-text" in argv \
        else pathlib.Path(__file__).resolve().parents[1] / "tools" / "capture-text.py"
    bad = rows = 0
    for n, line in enumerate(lesson.read_text(encoding="utf-8").splitlines(), 1):
        c = line.split("\t")
        if len(c) < 4: continue
        m, url, form = re.fullmatch(r"char (\d+)", c[1].strip()), c[3].strip(), c[2].strip()
        if not m or not url.startswith("http"): continue
        rows += 1; want, quote = int(m.group(1)), c[0]
        txt, raw = cache / (key(url) + ".txt"), cache / (key(url) + ".raw")
        if form.startswith("form .txt"):
            got = txt.read_text(encoding="utf-8", errors="replace") if txt.is_file() else None
        elif form.startswith("form .raw") and "capture-text.py" in form:
            got = subprocess.run([sys.executable, str(tool), str(raw)], capture_output=True).stdout \
                .decode("utf-8", "replace") if raw.is_file() else None
        elif form.startswith("form .raw") and not (raw.is_file() and raw.read_bytes()[:2] == b"PK"):
            got = raw.read_text(encoding="utf-8", errors="replace") if raw.is_file() else None
        else:
            print(f"ADHOC_FORM {lesson}:{n} form={form!r} url={url}"); bad += 1; continue
        if got is None: print(f"CAPTURE_MISSING {lesson}:{n} {key(url)}"); bad += 1; continue
        found = got.find(quote)
        if found != want or got.count(quote) != 1:
            print(f"OFFSET_MISMATCH {lesson}:{n} says char {want}, find()={found}, "
                  f"count={got.count(quote)} form={form}"); bad += 1
    print(f"CHAR_ANCHORS rows={rows} bad={bad}")
    return 1 if bad else 0

sys.exit(main())
```

## 6. Gates run (each with its observed result)

| gate | command | observed |
|---|---|---|
| pinned capture key | `sha256(url)[:24]` in python | `3a8b45977cd111e45e3980a5` — both files present |
| member counts | `unzip -p <raw> word/document.xml > doc.xml; grep -o …` | 1464476 bytes; `w:instrText` 100 (50 elements), `mc:Fallback` 120 (60), run tabs 49, tab stops 13 |
| form comparison | `tools/capture-text.py <raw>` vs `controls/naive-tool.py <raw>` | 19682 vs 21910 chars; PAGE/REF 0 vs 49; tabs 49 vs 62; duplicates 73 lines |
| counter, real tool | `python3 corpus/evidence/round52/c1-count.py --work <scratch>/work` | `LEGS=9/9 C1=PASS`, `REAL=PASS … locate=(0, 1, 8996) chars=19682`, rc=0 |
| counter, controls | same, `--tool controls/{naive,cache-txt,const}-tool.py` | `LEGS=4/9`, `LEGS=0/9`, `LEGS=0/9` — matches `controls/` receipts |
| counter, dirname forge | same, `--tool <scratch>/forge-dirname-r52.py` | `LEGS=0/9 C1=FAIL`; 9 random inputs in `c1r52-gz2utrot` |
| counter, REAL-path forge | same, `--tool <scratch>/forge-realpath.py` | `LEGS=1/9 C1=FAIL` (`REAL=PASS … chars=21`) |
| r51 counter + r51 forge | `python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py` | `LEGS=5/5 C1=PASS` rc=0 |
| criterion 76 on the r51 lesson | `python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-51.md` | `FORM_NAMED … DECODE_FORM=PASS` rc=0 (passes despite row 1) |
| criterion 76 on the r52 form | same, on the scratch probe lesson | `FORM_MISSING … DECODE_FORM=FAIL` rc=1 |
| row-level anchors | `<scratch>/char-anchor-check.py corpus/lessons/round-51.md <cache>` | 3 × `ADHOC_FORM` (`:79,83,89`), `OFFSET_MISMATCH :87 says char 9302, find()=9034`, `CHAR_ANCHORS rows=6 bad=5`, rc=1 |
| offsets, all candidate forms | python `find()` over five readings | 39411: member -1, w:t 8417, tool 8996, `.txt` 0 occurrences, raw-UTF-16LE -1 |
| newline ambiguity | python over `42bac883…raw` both ways | 17523/9034/8997 vs 17996/9302/9264 |
| `.txt` sidecar | python read of `3a8b4597….txt` | 168952 chars, 72117 U+FFFD, `検索` 0 — lesson `:55` reproduces |

## 7. Touched surfaces

Written: this file only (`.ufo/waves/round-52/w1/R52DraftMistakes.md`). Created and removed:
`/fast/scratch/hyaku/chousa-r52/R52DraftMistakes/` (`doc.xml`, `good.txt`, `naive.txt`, `lesson-probe.md`,
`seen.txt`, `work/`, two falsifiers described at §2/§4 and the checker reproduced at §5). No lane or fleet file edited; no git/jj
command of any kind; no counter written; `chousa-shokunin/tools/` and `corpus/` untouched; no `/home/vgpnk/Projects/shokuknow`
write; no network; no install.

## 8. Out of scope (not done, deliberately)

- I did not append anything to `corpus/lessons/round-52.md` (it does not exist yet) — omission is the L1's.
- I did not re-run `c2-count.py`, `build-spans.py` or any C2 leg; the C2 first-falsifiers belong to other seats.
- I did not patch `decode-form-check.py`, `c1-count.py`, `capture-text.py` or the claim; rows 2, 4 and 6 are proposed
  as supplement/erratum work, and the predicate text is untouched.
- `form DEINT` (three round-51 rows) is flagged, not re-grounded: no de-interleave tool exists in the lane to replay.
- I did not test a `.docx` whose `/officeDocument` relationship points at a directory, nor a package with two such relationships.

## 9. Findings summary

1. The round-51 refusal had no criterion behind it: 76's check passes any file that names one form and cannot open
   the capture; the refusal's form is a zip member nothing reproduces.
2. The cheap form is measurably wrong on the pinned file (1297 chars of field instructions, 105 of Fallback,
   13 phantom tabs, 73 duplicated lines, offset 10319 vs 8996) — so "just strip the member" was not an option.
3. The fixed-name defect is fixed and falsified: r51 counter + forge 5/5; r52 counter + the same attack shape 0/9,
   with the residual fixed path costing one leg.
4. The r52 REAL leg validates self-consistency, so the naive reading passes the leg that is supposed to prove the
   `.docx` is readable in the lane form (supplement needed; predicate untouched).
5. Two round-51 calibration defects stand: `char 39411` (`round-51.md:89`) is no form's offset, and `.raw` "UTF-8"
   carries two newline conventions (`9302` vs `8997` in one file).

Artifacts: this report (rows in §4, checker in §5, gates in §6). Nothing else persists.

VERDICT: I drafted six `## Mistakes` rows and falsified each — the r51 docx refusal has no criterion behind it and its
cheap form is wrong on the real file (naive 21910 vs 19682 chars, 49 `PAGE`/49 `REF`/1 `TOC`, 73 duplicated lines), the
r52 counter has no fixed names (dirname forge 0/9 vs the r51 frozen counter's 5/5 for the same attack, residual fixed
path = 1/9), and the r51 lesson's `char 39411` is the offset of nothing (-1 in the named form, 8996 in the lane form).
