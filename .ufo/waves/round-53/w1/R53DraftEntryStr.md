# R53DraftEntryStr — lane entry draft: the PRISMA authors' tracking-record commentary, re-grounded by document

seat: R53DraftEntryStr (scribe, chousa lane), round 53 wave 1, 2026-10-26
lane repo: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (my only write is this report)
scratch: `/fast/scratch/hyaku/chousa-r53/R53DraftEntryStr` (removed at exit; receipts below)
tool installs: none (pacman paused host-wide; no `uv`/`npx` call made). No network, no fetch (L0 `8d77e6c1` open).
sources: the staged entry `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/search-tracking-record-r40.md`
and the on-disk capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0ae65ac01b93119d3c2f3fed.{txt,raw,pdf}`.

## 1. Capture identity and what the draft rests on

- `.txt` sidecar (the text form the frozen C2 counter and `build-spans.py` read): 27,737 bytes, 27,659 characters, 5 form feeds —
  `wc -c` on the file plus `len(open(..., encoding='utf-8').read())`.
- `.raw` and `.pdf` are the same bytes: sha256 `c2aa0e12d45f33d01739952b858259fc97c14ab43be618cf865fcb5eededaf91`, 252,991 bytes each;
  the `.txt` sha256 is `1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d`.
- The staged body ids are dropped. The package rows they pointed at (`merge/chousa/SOURCES.append.md:19`, `:39`, `:55`) name the NDL
  WARP FAQ, the climate-fever paper and the NMPA `上市药品临床安全性文献评价指导原则（试行）`; this lane's same-numbered rows name
  other documents — `corpus/SOURCES.md:104` (S094) is the COLING claim-evidence paper, `corpus/SOURCES.md:124` (S114) is the
  chinagp.net Chinese PRISMA 2020 checklist page — and the lane has no row at the third number (highest id S116). Keeping those
  tokens would have mis-cited all three, so the draft names lane files by path instead.
- The staged ground's "round-1 note" has no lane text. `grep -rn -i 'jmla\|common questions' corpus/knowledge` from the lane root
  prints one line, `corpus/knowledge/search-log-method-r39.md:3` (the JMLA 2018 search-log method paper, lane id S078), and no file
  naming this FAQs paper; the ground line points at that file as the lane's standing search-log statement.
- `tracking record` (the C2 NEW_GROUND term) sits inside the located quote at char 447; `grep -rl 'Column [12]' corpus/knowledge | wc -l`
  prints `0`, so the column allocation is new ground as well.

## 2. The re-cut the seat asked for

The staged recheck quote joins two physical lines of the `.txt`: `PRISMA-S also recommends` (char 1288) and the next line's
`reporting the number of records identified from each information source.` (char 1320). The joined 96-character string occurs **0**
times in the text form:

```
python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0ae65ac01b93119d3c2f3fed.txt',encoding='utf-8').read(); print(t.count('PRISMA-S also recommends reporting the number of records identified from each information source'))"
0
```

The draft quotes the second line alone (char 1320, 72 characters, 10 words) and says so in the entry. The staged Column-2 quote
(`should be reported in Column 2`) fails the same way — 0 occurrences; the sentence breaks after `should be reported` (char 6355) —
and is replaced by the two line pieces at char 6355 and char 6544. A third staged quote, `the recommendation to report search
strategies for all databases, registries, and websites that were searched` (109 characters), also occurs 0 times and was not used.

## 3. Validation actually run (scratch mock root, the lane's own tools, nothing written to the lane)

`S=/fast/scratch/hyaku/chousa-r53/R53DraftEntryStr`; mock lane root `$S/mock` with `corpus/evidence/round53/quotes.tsv` (27 rows, `id url quote entry`) and a copy of the draft at
`corpus/knowledge/search-tracking-record-r40.md`; quotes read from the real `.txt`.

```
python3 corpus/evidence/round53/build-spans.py --root $S/mock --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
QUOTE S117 char 447 spans/S117-1.txt   (… 27 lines)
SPANS_ROWS=27 WRITTEN=27            exit 0; every quote accepted exactly once, offsets
                                    447 401 485 1605 1320 1288 9058 9183 6355 6544 6893 7694 13633 14417 10646 11685
                                    12842 15089 17488 17083 17114 14231 19789 20115 20387 8863 8993
python3 corpus/evidence/round53/build-spans.py --root $S/mock --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache --check
SPANS_ROWS=27 STALE=0               exit 0
python3 corpus/evidence/round51/quote-substance-check.py $S/mock/corpus/evidence/round53/spans.tsv
IDS=1 QUOTES=27 FAILURES=0          exit 0
python3 tools/inference-ground.py --entry $S/mock/corpus/knowledge/search-tracking-record-r40.md \
  --spans $S/mock/corpus/evidence/round53/spans.tsv --counts $S/counts.json --registry corpus/SOURCES.md
GROUND entry=search-tracking-record-r40.md section=1 bullets=6 tokens=12 grounded=12
GROUND: PASS                        exit 0
```

Checked on the draft text itself: the C2 source-line regex (the `^source:\s*S117\s+—\s+https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061(\s|$)` pattern at `c2-count.py:183`) matches `True`;
the only `S###` token is `S117`; `tracking record` is present; the QUALITY-10 placeholder probe (dollar-brace template slots, `TODO`,
`TBD`, `LANE_HASH`) returns nothing; `recheck:` starts with `365d`; the headings are `#`, `#### Observation`, `#### Inference`,
`#### Unknown`; every quote lies on one line of the `.txt` and occurs there exactly once (the builder refuses otherwise).

## 4. The entry

```markdown corpus/knowledge/search-tracking-record-r40.md
# A tracking record is routed by source: the PRISMA authors' commentary splits each source's count over two flow-diagram columns and leaves per-source detail to supplementary materials

source: S117 — https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061 — the title line (char 447) under the standfirst (char 401), the byline (char 485), the abstract's per-source count sentence (char 1320), the column allocation (char 6355, char 6544, char 6893, char 7694), the per-database-in-diagram sentence (char 10646), the supplementary-materials sentences (char 11685, char 14231) and the same-search passage (char 19789, char 20115, char 20387); J Med Libr Assoc 2022;110(2):253-257, doi 10.5195/jmla.2022.1449; capture `.qcache/0ae65ac01b93119d3c2f3fed.txt` read as UTF-8, 27,659 characters (27,737 bytes)
verified-at: 2026-10-26 — every quoted phrase re-located on one line of the read-only `.txt` sidecar at its stated offset, count 1 each; `.raw` and `.pdf` carry the same bytes (sha256 `c2aa0e12d45f33d01739952b858259fc97c14ab43be618cf865fcb5eededaf91`, 252,991 bytes); no fetch made (L0 `8d77e6c1` open)
recheck: 365d — from the lane root, `python3 corpus/evidence/round53/build-spans.py --check` prints `SPANS_ROWS=n STALE=0`; then re-download the PDF and confirm char 1320 still reads `reporting the number of records identified from each information source.`
ground: what a tracking record counts and where each identification route's records are placed in the PRISMA 2020 flow diagram; the lane's standing statement on a search log is `corpus/knowledge/search-log-method-r39.md` — `grep -rn -i 'jmla\|common questions' corpus/knowledge` from the lane root prints that file's `source:` line and nothing else, so the staged ground's "round-1 note" has no lane text to point at; no `corpus/knowledge` file names a flow-diagram column (`grep -rl 'Column [12]' corpus/knowledge | wc -l` prints `0`)
adopted: round 53 from the campaign package merge/chousa/ (staged `knowledge/corpus/knowledge/search-tracking-record-r40.md`)

#### Observation

- **The document is the two search-reporting authors' own commentary, and its title is about tracking records.** `PRISMA 2020 and PRISMA-S: common questions on` (char 401) is followed by `tracking records and the flow diagram` (char 447); the byline is `Melissa L. Rethlefsen, AHIP; Matthew J. Page` (char 485), and the abstract closes on the review process: `flow diagram and tracking records through the systematic review process` (char 1605).
- **The per-source count is stated as a recommendation in the abstract.** `PRISMA-S also recommends` (char 1288) is the abstract's last clause, and the next line carries its object: `reporting the number of records identified from each information source.` (char 1320). The sentence as the staged entry quoted it crosses that line break and occurs 0 times in this text form, so the entry quotes the second line alone.
- **The body makes the per-source count a property of the diagram.** It is expected that `records retrieved from each information source should be` (char 9058) `tracked, which aligns with PRISMA-S’s guidelines.` (char 9183).
- **The two columns are allocated by route.** Records identified from websites, organizations, `citation searching, and other methods should be reported` (char 6355) `in Column 2. The flow diagram template also suggests` (char 6544) an overall number for `databases and registers in Column 1.` (char 6893). Column 2 `represents the “Additional records identified through` (char 7694) other sources — the PRISMA 2009 box, with what the paper calls major improvements to tracking.
- **A citation index counts as a database, and the column follows the team's choice.** `Citation indexes are indeed databases and can be included` (char 13633) in Column 1, and a team may use both columns and `combine them in Column 1 in the flow diagram.` (char 14417). `PRISMA-S does recommend that, if space is available,` (char 10646) individual sources appear in the diagram; where there is no room, `records per individual information source should go in the` (char 11685) supplementary materials.
- **Google Scholar is both kinds of source; Google is an additional source only.** `Google Scholar is both a database and a citation index` (char 12842); Google is neither a bibliographic database nor a citation index and is `reported in Column 2.` (char 15089).
- **Counting every source is best practice, and a central count is easier to produce.** `Best practice is to count all records identified (by` (char 17488) hand or by other means; `When records are all centrally` (char 17083) `tracked, regardless of source, it is easier to produce this` (char 17114) data. `records identified per search in the supplementary` (char 14231) materials.
- **An update search is one data point, and the two documents' styles sit close together.** `PRISMA-S treats all results from the same search,` (char 19789) and with an update the total is combined `update, as a single data point [3]. In the PRISMA 2020` (char 20115), read `per database across the lifespan of the systematic review` (char 20387). `PRISMA-S was released slightly before PRISMA 2020, so` (char 8863) `the styles do not entirely align, but they are compatible` (char 8993).

#### Inference

- **A tracking record is routed, so the lane's sweep keeps a route per source.** `S117` puts `citation searching, and other methods should be reported` in one column and `databases and registers in Column 1.` in the other, so a total is a sum over routes and a record that carries only one number understates the columns it has to reconcile against.
- **The count is per source, which is what makes a sweep re-runnable.** `S117` has `records retrieved from each information source should be` `tracked, which aligns with PRISMA-S’s guidelines.`, and the lane's search-log entry `corpus/knowledge/search-log-method-r39.md` holds the log as a document the searcher updates; the pair gives a tally one unit (one source) and one home.
- **Per-source rows are the record; the diagram may carry a category total.** `S117` has `records identified per search in the supplementary` and puts `records per individual information source should go in the` supplementary materials where the diagram has no room, so a lane search log keeps one row per source even where a published diagram shows a category.
- **A re-run appends to the same source's row.** `S117` reads `update, as a single data point [3]. In the PRISMA 2020` and combines the total `per database across the lifespan of the systematic review`, so the lane's sweep keeps one row per source and adds its search points to that row.
- **The allocation is a reporting split, and copy-versus-URL is a different question.** `S117`'s Column 2 `represents the “Additional records identified through` other sources; whether the cited text sits in a copy this lane can open is the question `corpus/knowledge/exempt-hop-audit-r32.md` keeps, so this entry reads the columns as reporting and leaves verifiability there.
- **The paper's authority is explanatory, so its statements are practice and recommendation, not item text.** `S117` opens as `COMMENTARY` and says `PRISMA-S also recommends`, then reports `Best practice is to count all records identified (by` hand or by other means; a lane reading of it is therefore a reading of the authors' explanation of PRISMA 2020 and PRISMA-S.

#### Unknown

- **The item text of PRISMA-S was not read, and the paper carries no field list.** Sweep from the lane root: `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0ae65ac01b93119d3c2f3fed.txt',encoding='utf-8').read().lower();print([t.count(w) for w in ('requires','standard','recommends','field','checklist','chinese','japanese','commentary')])"` prints `[0, 0, 3, 0, 0, 0, 0, 2]`. The paper `recommends` and reports practice; it carries no item list and no field-level specification, and it names no Chinese or Japanese source.
- **The commentary's other questions were opened and not analysed.** The reports-not-retrieved boxes, the studies-versus-reports distinction and the 1,000-record ceiling on Google and Google Scholar (`Reports not retrieved` occurs once in the text form) are in the capture and no claim here rests on them.
- **Staged material corrected on adoption.** The staged recheck sentence crosses a line break, so the joined form occurs 0 times and the entry quotes the line at char 1320; the staged column sentence `should be reported in Column 2` does not exist in this text form (0 occurrences) and is replaced by the two line pieces at char 6355 and char 6544; the staged ground's "round-1 note" has no lane file (the grep above); the staged body ids are dropped — in the package they named the NDL WARP FAQ, the climate-fever paper and the NMPA 上市药品临床安全性文献评价指导原则（试行）, while this lane's rows at two of those numbers name the COLING claim-evidence paper and the Chinese PRISMA 2020 checklist page, and the lane holds no row at the third, so keeping the tokens would have mis-cited.
- **Whether the paper binds anyone was not established.** It is a commentary whose text says `PRISMA-S also recommends`; authority beyond explanation is outside this capture, and no standard wording is attributed to it here.
```

## 5. QUOTE machine lines (every quote the entry uses)

```
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	tracking records and the flow diagram	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA 2020 and PRISMA-S: common questions on	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Melissa L. Rethlefsen, AHIP; Matthew J. Page	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	flow diagram and tracking records through the systematic review process	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	reporting the number of records identified from each information source.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S also recommends	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	records retrieved from each information source should be	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	tracked, which aligns with PRISMA-S’s guidelines.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	citation searching, and other methods should be reported	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	in Column 2. The flow diagram template also suggests	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	databases and registers in Column 1.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	represents the “Additional records identified through	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Citation indexes are indeed databases and can be included	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	combine them in Column 1 in the flow diagram.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S does recommend that, if space is available,	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	records per individual information source should go in the	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Google Scholar is both a database and a citation index	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	reported in Column 2.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Best practice is to count all records identified (by	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	When records are all centrally	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	tracked, regardless of source, it is easier to produce this	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	records identified per search in the supplementary	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S treats all results from the same search,	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	update, as a single data point [3]. In the PRISMA 2020	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	per database across the lifespan of the systematic review	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S was released slightly before PRISMA 2020, so	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	the styles do not entirely align, but they are compatible	corpus/knowledge/search-tracking-record-r40.md
```

## 6. What the L1 still owes before the C2 counter can pass on this entry

1. A Registry row `S117` in `corpus/SOURCES.md`: first source cell the URL above, `mined`, opened 2026-10-26, `used-by` naming
   `corpus/knowledge/search-tracking-record-r40.md`, and an `anchor` cell whose `char N` values come from the 27 offsets above.
2. The 27 rows appended to `corpus/evidence/round53/quotes.tsv` (`entry` cell = the lane path), then `build-spans.py` without
   `--check` to write `spans.tsv` and `spans/`; C2 needs every row inside its span file, inside the entry and inside the lesson.
3. The same 27 quotes inside `corpus/lessons/round-53.md` — the lesson is the fourth carrier of each quote row.
4. `corpus/knowledge/search-tracking-record-r40.md` written from the block in section 4; this seat wrote no lane file.

## 7. Limits and out-of-scope

- The C2 counter was not run: it reads lane bytes (entry, lesson, registry, spans) that this seat may not write, and its `BOUND` leg
  needs the Registry row the L1 has not added. A draft is not a measurement.
- `tools/capture-text.py` refuses this capture (`REFUSED not a zip`, exit 2, tested twice): the `.raw` is a PDF, so the text form
  used throughout is the `.txt` sidecar, the form the seat spec and `build-spans.form_texts` both define.
- The paper's other questions (reports-not-retrieved boxes, studies versus reports, the 1,000-record ceiling) were opened and not
  analysed; no claim here rests on them.
- No tool installed; no pacman transaction attempted; `shokuknow`, the fleet root and sibling lanes were read only.

VERDICT: drafted and machine-validated the S117 entry for `corpus/knowledge/search-tracking-record-r40.md` by document — 27 located
one-line quotes, all accepted exactly once by the lane's span builder (`SPANS_ROWS=27 STALE=0`), `inference-ground` PASS on 6/6
bullets and 12/12 tokens, substance check 0 failures — re-cut the wrapped staged recheck quote to char 1320 and said so, and dropped
the staged body ids S094 S114 S130 because they name other documents at this lane's numbers.
