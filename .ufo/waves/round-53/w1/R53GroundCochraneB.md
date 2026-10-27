# R53GroundCochraneB — second pass on staged S193 → planned lane S121

Seat: independent B-pass on the Cochrane Handbook chapter-4 capture only (document
`https://training.cochrane.org/handbook/current/chapter-04`). I did not open
`.ufo/waves/round-53/w1/R53GroundCochraneA.md` or any other seat's report, and I read no
sibling lane. Lane repo read-only; the only file I write is this report. No install, no
network, no lane/source mutation. Scratch `/fast/scratch/hyaku/chousa-r53/R53GroundCochraneB`
(TMPDIR set for every command; scripts `sweep.py`, `locate.py` lived there and were removed).

Frozen inputs read first: `corpus/evidence/round53/claims.md` (C2 binds staged S193 to entry
`corpus/knowledge/western-instrument-alignment-r50.md`), `c2-count.py` (DOCS pair
`(E_WIA, "S193", COCHRANE)`; `COCHRANE = "https://training.cochrane.org/handbook/current/chapter-04"`),
`build-spans.py` (`IN_HEADER = id,url,quote,entry`; `CONTEXT = 80`; picks the first text form in
which the quote occurs **exactly once**).

## 1. Capture identity (both forms, digests re-derived)

```
$ C=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
$ sha256sum $C/c9d1e74c3ac8d9eb332c9770.txt $C/c9d1e74c3ac8d9eb332c9770.raw
722d3ce9b16486e8f7246670c37511b959abe427dc31304234e3ab12e665d97c  .../c9d1e74c3ac8d9eb332c9770.txt
813ef2234d7616b40ac072f3f35558fc4ad46f051802aa2970d5cecc9616570c  .../c9d1e74c3ac8d9eb332c9770.raw
$ wc -c .../c9d1e74c3ac8d9eb332c9770.txt        → 211326 bytes
  (python len(text) = 210708 chars, 1465 LF, 0 CR, longest line 3211 chars → no hard wrapping)
$ python3 -c 'hashlib.sha256("https://training.cochrane.org/handbook/current/chapter-04")…[:24]'
c9d1e74c3ac8d9eb332c9770      # cache key matches the URL, so this is that URL's capture
```

The document's own stamp, as the two forms carry it:

| element | evidence |
|---|---|
| title | `<title>Chapter 4: Searching for and selecting studies \| Cochrane</title>` — raw byte 884; body heading `Chapter 4: Searching for and selecting studies` txt line 301; collation line `Cochrane Handbook for Systematic Reviews of Interventions` txt line 265 (also 210) |
| edition / date | txt line 559, the collation's own citation: `… Chapter 4: Searching for and selecting studies [last updated March 2025]. In: Higgins JP, … Cochrane Handbook for Systematic Reviews of Interventions version 6.5.1 Cochrane, 2025. Available from cochrane.org/handbook .` — `version 6.5.1` count 1, `last updated March 2025` count 1, `Cochrane, 2025` count 1 |
| host | capture URL host `training.cochrane.org`; the page's own canonical link (raw byte 255) is `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04` |
| author | txt line 548 = the 11 chapter authors ending `; on behalf of the Cochrane Information Retrieval Methods Group`, repeated in §4.7 `Authors:` txt line 988; group name count 3 |
| site footer | `Copyright © 2026 The Cochrane Collaboration` at txt offset 209472 — the footer year (2026) is **not** the edition year (2025); do not quote it as the version |

Host finding (matters for the counter): the **same document is in the cache under two URLs**.
`sha256("https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04")[:24]
= 14aaa168a5cb4d833ca78b0b`, and `14aaa168a5cb4d833ca78b0b.txt` / `.raw` are **byte-identical**
to `c9d1e74c3ac8d9eb332c9770.txt` / `.raw` (both digests above, verified with `sha256sum` on all
four files). Staged package carries the document twice for this reason: row `S083` cites the
`www.cochrane.org` URL, row `S193` cites the `training.cochrane.org` URL
(`merge/chousa/SOURCES.append.md` lines 8 and 118). C2 keys the capture by the **training** URL
(`c2-count.py` `COCHRANE`), so the lane Registry row for S121 must carry the training URL, or
`form_text()` cannot find the capture and `CAPTURE_BOUND` cannot pass.

## 2. Negative sweeps (`text.count`, .txt form read as UTF-8, case-sensitive unless `ci` shown)

```
$ python3 sweep.py     # chars=210708 lines=1465 CR=0 maxline=3211; ref boundary = 2nd "4.8 References" at 144865
tracking record            cs=2   ci=2   prose=1   refs=1
each information source    cs=0   ci=0   prose=0   refs=0
information sources        cs=1   ci=1   prose=1   refs=0
number of records          cs=2   ci=2   prose=2   refs=0
PRISMA-S                   cs=11  ci=11  prose=8   refs=3
PRISMA 2020                cs=10  ci=10  prose=7   refs=3
information specialist     cs=23  ci=51  prose=22  refs=1
librarian                  cs=29  ci=37  prose=15  refs=14
unpublished                cs=43  ci=44  prose=21  refs=22
grey literature            cs=4   ci=5   prose=3   refs=1
检索                        cs=0   ci=0   prose=0   refs=0
检索策略                     cs=0   ci=0   prose=0   refs=0
检索日期                     cs=0   ci=0   prose=0   refs=0
灰色文献                     cs=0   ci=0   prose=0   refs=0
未发表                      cs=0   ci=0   prose=0   refs=0
PRISMA                     cs=31  ci=31  prose=24  refs=7
数据库                       cs=0   ci=0   prose=0   refs=0
```

Also counted: `PRISMA-ScR` = 0; `search record` = 0 and `search records` = 0 (the document never
uses the theme's own phrase; it says `tracking records` twice — once in prose, once in the
JMLA reference); `Rethlefsen et al 2021` = 6; `Rethlefsen and Page 2022` = 1; `Creative Commons`
= 0; `©` = 1 (the site footer only).

**Absent terms, so any entry sentence resting on them carries this sweep**: every CJK term in the
brief is 0 — `检索`, `检索策略`, `检索日期`, `灰色文献`, `未发表`, `数据库` — and every Han
codepoint in the file (8 chars, 6 unique) sits inside the language menu at offsets 253–263
(`繁體中文` / `简体中文`). The chapter is an English-only document; a claim that it "names the
Chinese term" or "has no Chinese vocabulary" is trivially true and must not be offered as a
finding. `each information source` is absent (0) although `information sources` occurs once —
quote PRISMA-S's wording with `information sources`, never `each information source`.

## 3. Located quotes (10; each occurs exactly once in the .txt form, lies on one line)

```
$ python3 locate.py
S121-A 4.KP   off=5587    occ=1 w=19 c=143 line=550  oneline=True
S121-I 4.2.1  off=13471   occ=1 w=12 c=76  line=577  oneline=True
S121-J 4.3.2  off=36552   occ=1 w=17 c=119 line=631  oneline=True
S121-B 4.3.5  off=52712   occ=1 w=17 c=116 line=655  oneline=True
S121-H 4.5    off=114096  occ=1 w=22 c=152 line=914  oneline=True
S121-C 4.5    off=114690  occ=1 w=17 c=121 line=914  oneline=True
S121-D 4.5    off=115755  occ=1 w=17 c=102 line=916  oneline=True
S121-E 4.5    off=116711  occ=1 w=22 c=143 line=917  oneline=True
S121-F 4.5    off=118144  occ=1 w=18 c=106 line=919  oneline=True
S121-G 4.8    off=193214  occ=1 w=13 c=83  line=1214 oneline=True
```

Section bodies (heading offsets, body occurrence, not the table of contents): §4.2.1 at 9897,
§4.3.2 at 35426, §4.3.5 at 52572, §4.5 at 111858, §4.6 at 120988, §4.8 at 144865. A sits in the
`Key Points` block (before §4.1 at 7717); all others fall inside the section named above.

Machine lines (tab-separated; staged-id = planned lane id; entry is lane-relative; drop the
leading `QUOTE` cell to obtain the `id,url,quote,entry` rows `build-spans.py` expects. Any subset
of ≥3 works mechanically — but paste into the entry **and** the lesson exactly the rows you keep,
and give the registry row only `char N` values that are offsets of kept rows):

```
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Review authors should work closely, from the start of the protocol, with an experienced medical/healthcare librarian or information specialist.	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	and that the reporting aligns with the current reporting guidance for PRISMA	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	The term ‘grey literature’ is often used to refer to reports published outside of traditional commercial publishing.	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	provides enough detail and specific examples for systematic review authors to report search methods and information sources in a clear, reproducible way	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Further PRISMA-related guidance has been published relating to tracking records and completion of the PRISMA flow diagram	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	together with the search set numbers and the total number of records retrieved by each search strategy	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Documenting the searching of sources other than databases, including the search terms used, is also required if searches are to be reproducible	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	It is particularly important to save locally or file print copies of any information found on the internet	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram	corpus/knowledge/western-instrument-alignment-r50.md
```

What each is for: **I** is the staged entry's alignment sentence in the document's own words
(§4.2.1 role bullet); **J** is its unpublished-studies/bias sentence (§4.3.2); **C** is the chapter
naming *tracking records* as PRISMA-related guidance (§4.5) and **G** is the chapter's own
reference-list entry for the JMLA PRISMA 2020/PRISMA-S common-questions paper (§4.8, staged S134 /
lane-side entry `search-tracking-record-r40.md`) — the two documents bind to each other inside one
reference list, which is the theme continuation by document; **H** is PRISMA-S used as a reporting
instrument for `information sources`; **D/E/F** are the chapter's search-record reporting duties
(set numbers and per-strategy record totals, non-database sources, local copies); **B** is the
grey-literature definition (§4.3.5); **A** carries the entry term `information specialist`.

## 4. Binding notes the frozen counter will check (derived from `c2-count.py`, not patched)

- `source:` line in the entry must match `^source:\s*S121\s+—\s+https://training\.cochrane\.org/handbook/current/chapter-04(\s|$)`
  (em dash U+2014, no trailing `/`); the staged entry's current `source: S193 — …` and
  `source: S195 — …` lines are exactly what `REF_ID_UNBOUND` refuses.
- Registry row (11 cells, `corpus/SOURCES.md` §Registry): col1 first source-cell URL =
  the training URL; `status = mined`; `opened = 2026-10-26`; `used-by` = exactly
  `corpus/knowledge/western-instrument-alignment-r50.md` (C2 builds `citing` from the frozen DOCS
  pair, so naming any second entry fails the equality); the row must be new since
  `5b5501…8b8c3e`.
- `anchor` cell: `char N` values must all be offsets of quote rows kept for S121. Suggested text
  (keeps A/I/J/C/D offsets): `§4.2.1 the information-specialist role bullet, §4.3.2 the
  unpublished-studies paragraph, §4.5 Documenting and reporting the search process; capture .txt
  read as UTF-8, 210708 characters; char 5587, char 13471, char 36552, char 114690, char 115755`.
- Entry term gate: at BASE_REV no `corpus/knowledge` file holds the three terms — checked for my
  term: `git -C chousa-shokunin grep -l -e "tracking record" -e "information specialist"
  -e "质量控制指南" 5b5501…8b8c3e -- corpus/knowledge` → exit 1, no output. The entry must carry
  `information specialist`, which quote A does.
- No `S###` token in any existing entry except a bound id: S121 is bound; S193/S195 tokens from the
  staged text must not survive.

## 5. Findings against what the staged entry rests on (reported, not patched)

1. **The alignment sentence is real but its subject is the role, not the chapter's own method.**
   `and that the reporting aligns with the current reporting guidance for PRISMA` (offset 13471) is
   one bullet in §4.2.1's list of what the information specialist ensures for Cochrane protocols
   and reviews; the full bullet also carries `and PRISMA-S ( Rethlefsen et al 2021 )`. The words
   `alignment` (0) and `reporting guideline` (0) do not occur; `aligns` occurs once (this bullet),
   and `reporting guidance` occurs once (same bullet). The entry's "explicit
   instrument-to-instrument statement" is therefore defensible only if attributed to the role
   bullet; as a statement about the chapter or about the review's own reporting it is not what the
   document says.
2. **The reverse-direction sentence exists and must not be conflated with (1).** At offset 114578:
   `This brings the PRISMA 2020 guidance more into line with Cochrane standards for reporting of
   search strategies.` — PRISMA 2020 moving toward Cochrane, not Cochrane toward PRISMA. A reading
   that cites both as one alignment claim would be wrong.
3. **The §4.3.2 bias framing is verbatim:** `Finding out about unpublished studies, and including
   their results in a systematic review when eligible and appropriate` … `is important for
   minimizing bias.` — with the citation `( Cook et al 1993 )` between the two spans (quote J cuts
   before it); and the section's opening
   sentence, `Initiatives to provide access to ongoing studies and unpublished data constitute a
   fast-moving field ( Isojarvi et al 2018 ).` (offset 35599, `fast-moving field` count 2).
4. **`PRISMA still counts 0` in the staged entry is about the Chinese guideline, not this
   capture** — this capture counts PRISMA 31 (24 prose / 7 reference list). I did not open the
   Chinese document, so I neither confirm nor contradict that count; it stays outside this seat.
5. **Document-internal twin:** the chapter's reference list holds the S117 JMLA paper (quote G,
   offset 193214) and `Rethlefsen et al 2021` six times; that is the strongest single link from S121
   to the theme entry `search-tracking-record-r40.md`, and it is a reference-list fact, not a
   statement of alignment.

## 6. Limits I did not cross

- Builder limit found while checking the forms: `raw_form()` in `build-spans.py` decodes a non-zip
  `.raw` as UTF-16LE; on this capture (UTF-8 HTML, 372,430 bytes) it yields 186,215 chars of
  mojibake and contains none of the quotes. Every S121 quote must therefore be unique in the
  `.txt` form — mine are (all `occ=1`), so the builder picks the `.txt` form and the digest above.
  A quote that occurred twice in `.txt` would send the builder to the mojibake form and be refused.
- I did not run `c2-count.py`, `build-spans.py`, or the adopter: no entry, spans.tsv, or registry
  row exists yet, so any such run measures the before-state, not this seat's material.
- I did not fetch the live page; the only evidence is the on-disk capture (L0 `8d77e6c1` open).
- The 210,708-char figure is the `.txt` form; the brief's 210,708 matches. The `.raw` is 372,430
  bytes and is not a quote source.

VERDICT: attacked staged S193 against its capture — identity (version 6.5.1, chapter last updated
March 2025, 11 authors + IRMG, training/`www` twin URLs byte-identical) and claim binding hold,
with the alignment sentence confirmed only as an §4.2.1 role bullet and the reverse-direction
PRISMA-2020 sentence flagged against conflation; 10 quotes located once each in the .txt form
(offsets above), CJK sweeps all 0 (8 Han chars, all in the language menu), and `each information
source` absent.
