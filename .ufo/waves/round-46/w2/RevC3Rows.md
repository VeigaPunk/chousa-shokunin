# RevC3Rows — S085–S089 judged for truth (round 46, wave 2, falsify)

Item: for each of the five new Registry rows, re-open the capture and confirm (a) the
`anchor` quote is contiguous and ≤25 words at the stated offset, (b) `source` names the
right document, (c) `kind`/`tier` are defensible under `CORPUS.md` (row contract) and
`QUALITY.md`, (d) `used-by` names an entry that really cites it. Bytes judged:
`corpus/SOURCES.md` at HEAD `e50b388` (sha256
`73cb81f31b22ed443efe11fbb0d7e9fbfa26ad8d0a3e327b5ae5ff50480ef9ce`); the commit under
attack is `d09fc8e7` (sha `38ca3bd2…05`), whose only row difference is the S088 anchor,
corrected by `3807537`. No fetch; captures read from the campaign cache. No installs.

## Commands and decisive output

Rows at `corpus/SOURCES.md:96–100` (`:95` is blank), 11 cells each:
`96 S085 11 · 97 S086 11 · 98 S087 11 · 99 S088 11 · 100 S089 11`.

Spans re-derived (`str.find`; span = `capture[offset:offset+len(span)]`; `offset` = quote
start − 80; `capture_sha256` = sha256 of the capture file). All eleven:
`sha_ok True  slice EXACT  qpos == offset+80`, lengths 176–215:

```
S085-1 2360 (183)  S085-2 1271 (206)          S086-1 15269 (204)
S086-2 42011 (176) S086-3 20847 (179)         S087-1 171 (198)
S087-2 4929 (183)  S088-1 3929 (198)          S088-2 2904 (215)
S089-1 3022 (202)  S089-2 7137 (193)
```

Anchor cells (`capture[off:off+len(q)] == q`, whitespace-token count):

```
S085 @2349 contiguous=True words=18    S085 @1271 contiguous=True words=6
S086 @6737 contiguous=True words=8     S086 @6784 contiguous=True words=2
S086 @20847 contiguous=True words=4    S087 @171 contiguous=True words=2
S087 @4929 contiguous=True words=2     S088 @3909 contiguous=True words=9
S088 @2891 contiguous=True words=2     S088 @2904 contiguous=True words=10
S089 @7084 contiguous=True words=13
```

`PYTHONDONTWRITEBYTECODE=1 python3 corpus/evidence/round46/c3-count.py` (and
`--lane-only`): `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11|skipped REF_ID_UNBOUND=0 REF_BOUND=2/2
C3=PASS` exit=0 both.

## Per-row verdict

| row | anchor | source | kind/tier | used-by | verdict |
|---|---|---|---|---|---|
| S085 | 2349+1271 contiguous, 18+6 w | FEVER Dataset page; `build 385 / Last updated: 2026-04-02` (4069) | `dataset` A, release page of the dataset (precedent S082) | base entry `source:` 3–5 + 5 body cites | **PASS** (nit F5) |
| S086 | 6737/6784/20847 contiguous, ≤8 w | same paper: title + 4 authors (0), `Proceedings of NAACL-HLT 2018, pages 809–819` (5079) | `paper` A | base entry `source:` 4 + body | **FAIL on `teaches`** (F1); rest passes |
| S087 | 171+4929 contiguous, 2 w | record `"id": 4925954`, `"doi": "10.5281/zenodo.4925954"`, title (0–370) | `dataset` A: record's `"resource_type": {"title": "Dataset"}` (1346) | base entry `source:` 5 + body | **PASS** (nit F4) |
| S088 | 3909/2891/2904 contiguous, ≤10 w | `AVeriTeC Dataset` head; `Michael Schlichtkrull, Zhijiang Guo, Andreas Vlachos` (1920–1969) | `dataset` A | amendment `source:` 3 + body | **PASS** on the four cells; three cells to change (F2/F3/F6) |
| S089 | 7084 contiguous, 13 w | title + `Rui Cao … Andreas Vlachos`; `arXiv:2505.17978v2 [cs.CL] 07 Oct 2025` (1845) | `paper` A | amendment `source:` 4 + body | **PASS**, no cell change |

Kind/tier basis: `CORPUS.md:91` enum (`dataset`, `paper` legal); `CORPUS.md:93` A =
"primary or authoritative for that scope (… original paper, maintainer statement …)".
S087's `dataset` is the record's own resource type, not an inference. `status: mined`
holds in all five (≥1 path in `used-by`, `CORPUS.md:103`). No other file under
`corpus/knowledge/` or `corpus/lessons/` cites S085–S089 (`grep`), matching `used-by`;
precedent S082 shows lessons are not counted as citers.

## Findings (new; the three wave-1 named items are not repeated)

**F1 MED — S086 `teaches` (line 97) misstates the comparator twice.**
`a super-annotator's exhaustive set`: `exhaustive` occurs **0** times in capture
`1c15b611118dee97e4105fcf.txt`; the capture's subject is plural — `annotated by
super-annotators: expert annotators with no suggested time restrictions` (19520),
`When compared against the super-annotators, all except two annotators achieved > 90%
precision` (21727) — and the comparator is `We compared the regular annotations against
this set of evidence and the precision/recall was 95.42% and 72.36% respectively`
(20384–20410). The row's own citer disclaims the word: base entry line 28, ``the word
"exhaustive" occurs 0 times in the S086 capture``, and declines to state more; its line
16 repeats it. Wave 1 split (`ReviewOpenS086.md:90` endorsed; `ScribeEntryBase.md:94–97`
called it a defect); the row landed with the phrase, and the row is my cell. The anchor
also cites no offset for the comparator it asserts; add 20403 (or 21727).

**F2 MED-LOW — S088 `scope` (line 99) says "each evidence item", the capture says 7 of 8.**
`answer_type` occurs 8 times, `cached_source_url` 7; the eighth is the Not-Enough-Evidence
answer at 9375 — `{ "answer": "No answer could be found.", "answer_type": "Unanswerable",
"source_url": "", "source_medium": "" }` — with no `cached_source_url`. The citing entry
records the same exception (`evidence-pool-versioning-r39-amendment-2026-10-23.md:11`:
"documented practice, not a schema invariant"), and wave 1 proposed the correction for the
entry (`ReviewOpenS088.md:87`); the fix stopped at the entry. `scope` is a topic
(`CORPUS.md:98`), so this is imprecision, not a false universal.

**F3 LOW — S088 `teaches` grounding.** "a citation is stored as a `source_url` together
with an archive link to that url" is evidenced by the cached gloss (3909) plus the
examples (`"source_url": "https://en.wikipedia.org/wiki/Hunter_Biden"` at 5063), not by a
`source_url` gloss: at 3865 the page says `source_url : The answer to the question.`, a
copy of `answer`'s gloss — a page defect. Add the example offset.

**F4 LOW — S087 `teaches` offset.** `(char 4929)` is the file-entry start
`"key": "wiki-pages.zip"`; the size token `1713485474` is at 4962. Cite 4962 for the byte
count. "a versioned concept doi" is grounded:
`"relations": {"version": [{"index": 0, "is_last": true, "parent": … "4925953"}]}` (1453).

**F5 LOW — S085 `teaches` word.** "a Wikipedia page title" vs the anchor's own
`Wikipedia URL` (2349); example values are titles (`"Oliver_Reed"`). Say `Wikipedia URL
(example values are page titles)`. The anchor's second quote has no offset; the Gate
record gives 1271 (`corpus/lessons/round-46.md:242`).

**F6 LOW — S088 `recheck 180d` vs S085 `365d`, contradictory reasons.** Both captures are
the same stamp (`build 385`, `last updated 2026-04-02`; S085@4069, S088@12698).
`round-46.md:238–239` gives S088 180d *"where the page is build-stamped"*; `:260` changes
S085 180d→365d *"a build-stamped page, not a living one"* — one property, opposite
cadences. 180d is not unprecedented (6 rows), so state the real difference (S088 describes
a corpus with successor releases) or align.

**F7 LOW — `corpus/SOURCES.md:95` is blank, splitting the registry table.** S084 is line
94, line 95 blank, S085–S089 at 96–100; the parent had S084 → blank → `## Paths`, so the
rows were appended after the blank. GFM ends the table there, so the five new rows render
outside it (the regex census is unaffected). Delete line 95.

Not re-reported: the `d09fc8e7` S088 anchor `char 2891: Our best estimate…` is wrong (2891
is `claim_date :`; the quote starts at 2904) — already found (`corpus/lessons/round-46.md:82–88`,
`ReviewOpenS088` seat) and corrected by `3807537`; I re-derived the corrected cell as
`contiguous=True` at both offsets. That correction is an in-place `anchor` edit, which
`CORPUS.md` rule 2 does not list among the in-place cells: a round-level question, not a
current row defect.

## Residual risk and verification gaps

- `c3-count.py` never checks a row's `anchor` cell (named limit, `round-46.md:86–87`);
  F1–F7 are manual and only as good as this re-read. Captures live outside the lane
  (`.qcache`, read-only); a re-run needs that path.
- S086's 6737 quote is a dehyphenated fragment; the row discloses the split and I confirmed
  both halves (6737, 6784). A stricter reader could demand one contiguous run; I do not.
- Document identity was verified by content (titles, ids, DOIs, version strings), not by
  fetching the URL; no network was used.
- If the round rules "exhaustive" an acceptable paraphrase of "search over the whole Wikipedia for every possible sentence", F1 reduces to the singular `a super-annotator's`.
