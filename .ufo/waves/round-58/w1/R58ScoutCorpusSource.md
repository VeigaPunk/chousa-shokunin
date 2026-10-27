# R58ScoutCorpusSource — S101 source registration and admissibility of the round-58 fresh opening

Seat: R58ScoutCorpusSource (scout, leaf). Lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin.
Freeze commit 9e73a03; claim base b13ca7b5; HEAD 5da0a63 (two commits past freeze; diff is
round-58 controls + s101-open.txt only). No fetch performed; no lane file written.

## Question

Why is re-opening the lane-owned S101 capture this round an admissible *fresh* source opening,
given the registration and the round-54/round-57 history?

## S101 source registration (corpus/SOURCES.md:111)

Row `| S101 |`, 11 cells. Document: 《中国学术期刊(光盘版)检索与评价数据规范(修订本)》,
copy hosted by 哈尔滨工业大学, URL https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc,
tier B, status `mined`, opened 2026-10-25, refresh 180d, used-by (base) `corpus/knowledge/citation-count-semantics-r37.md`.
Anchor cell still reads "…15.7 parameter table (UTF-16LE text of the raw .doc capture); located
quotes char 11170, char 11205, char 11993, char 12161, char 13247, char 34374" — the form label
and offsets the round-54 lesson later found undefined (see below).

## Original opening evidence

- Round 49 (corpus/lessons/round-49.md:92-100, accessed 2026-10-25, captures written 2026-10-23,
  campaign cache, no fetch): S101 opened with 6 quotes at chars 11170/11205/11993/12161/13247/34374
  of a whole-file UTF-16LE decode of the .doc, capture key 6dc68fd6b32ce9c8dfcebce8, sha256 prefix 6063a3aff7a4….
- Round 54 (corpus/lessons/round-54.md): Mistakes row 2 — that UTF-16LE decode is an *undefined*
  text form (263 U+FFFD, 243 0x0B, binary preamble); every old offset lands elsewhere in the
  defined form (S101 11170→11972 … 34374→25123). Nine anchored `correction:` lines in
  SCORECARD.md "Round 54 pointer corrections" (lines 2743-2748 for S101) re-point the six quotes
  into `corpus/evidence/round54/S101-text-form.txt` (the OLE defined form), verified 9/9 by the
  round-54 spot-check. The S101 leg of the staged r37 draft was **refused** with flip: "a span
  builder that reads an OLE .doc through tools/capture-text.py, and the four quotes re-located in
  that form". Quarantine register S096 (= lane S101 by URL) was then read in the defined OLE form
  (27,012 characters, 0 U+FFFD) and judged absent-as-written for its elided splice.
- Round 57 (corpus/lessons/round-57.md): the capture was stored lane-owned at f9736a3 (L1 re-fetch
  pass 1, under egress approval); refetch.tsv rows 19/66 record S101 attempt 1 and 2 both rc=0,
  HTTP 200, raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`
  (REPRODUCED). The lesson's id-space note binds register S096 → lane S101 by URL with key
  sha256(url)[:24] = `6dc68fd6b32ce9c8dfcebce8`. Attempt-3 addendum hand-check: S096's quote
  family `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` is verbatim PRESENT.

## This round's frozen opening

claims.md C2 freezes: raw key 6dc68fd6b32ce9c8dfcebce8, sha256 6063a3aff7…, defined form made by
pinned tools/capture-text.py (sha256 2c0140bc…), builder pinned 1ed2650a…, 12 quotes frozen in
corpus/evidence/round58/c2/quotes.tsv (+ in c2-count.py). quotes.tsv exists at freeze commit
(`git cat-file -e 9e73a03:corpus/evidence/round58/c2/quotes.tsv` → 0). Opening record
corpus/evidence/round58/s101-open.txt was pinned pre-dispatch at 5da0a63 ("round-58: pin S101
opening and frozen C2 baseline").

## My reproduction (scratch only; evidence, read-only on lane)

Command: `python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > $SCRATCH/s101-form.txt`
Observed: length 27,012 characters; U+FFFD 0; 0x0B 0; `cmp` vs corpus/evidence/round54/S101-text-form.txt
→ identical (ROUND54_FORM_IDENTICAL), so the defined form has been byte-stable since round 54.
All 12 frozen quotes occur exactly once, at the s101-open.txt offsets: 315, 330, 590, 683, 734,
781, 797, 838, 965, 993, 1460, 11723. Line-start anchors: 3 (meets the counter's ≥3 floor).
Tool pins verified by sha256sum: tools/capture-text.py = 2c0140bc…, tools/build-spans.py = 1ed2650a….
`git cat-file -e b13ca7b5:corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` → 0 (capture present at claim base).

## Why the re-opening is admissible as a fresh source opening

1. **No fetch; lane-owned committed bytes.** The source is the committed capture, present at the
   claim base and REPRODUCED under round-57's authorized refetch. Lane topology forbids live
   egress (L0 open); every prior opening of S101 (rounds 49, 54, 57) likewise read lane-held bytes.
2. **A new, authoritative text form — not a reuse of the old anchors.** The round-49/54 "opening"
   was in a decode no lane command prints and which round 54 proved undefined; its six offsets are
   superseded by SCORECARD corrections. Round 58 is the first opening in the defined OLE form
   (pinned capture-text.py), executed under the exact flip condition round 54 attached to its
   refusal ("span builder … through tools/capture-text.py, and the … quotes re-located in that
   form"). Re-opening the same bytes in the sanctioned defined form is the lane's standing
   re-opening pattern, not post-hoc widening: claims.md froze the source, form-maker, digest and
   12 quotes before wave data, and s101-open.txt pinned the located offsets pre-dispatch.
3. **New ground, disjoint quote content.** The 12 quotes cover the GB3469 single-letter alphabet,
   double-letter suggestion, carrier identifiers (MT, OL), the [type/carrier] notation and the
   document-code distinction — none of the six round-49 quote strings. Base grep:
   `git grep -c '载体类型标识' b13ca7b5 -- corpus/knowledge` → rc=1 (0 hits); traditional form
   `載体类型标识` also rc=1. The counter's NEW_GROUND leg holds on the honest base.
4. **Binding and causal separation are frozen and verified.** c2-count.py binds every row to the
   URL, raw digest and exact offsets in the defined form; builder/capture-text pins verified
   above; C2 is independent of C1's tool change.
5. **Scope discipline.** The claim is scoped to the source's located text, not present-day
   standards validity — consistent with the lane's text-presence vs. entailment vs. truth rule.

## Findings (observations, not fixes — frozen predicates are findings-only)

- c2-count.py's NEW_GROUND grep searches the base for the *traditional* form `載体类型标识` while
  requiring the *simplified* `载体类型标识` in the entry. At the actual base both forms are absent
  (rc=1 each), so the leg is satisfied on honest bytes; but a future base containing only the
  simplified form would pass this leg while ground pre-existed (form-mismatch latent mask).
- SOURCES.md:111's anchor cell still carries the old "(UTF-16LE text of the raw .doc capture)"
  label and the six round-49 offsets; only the SCORECARD correction lines carry the re-pointed
  defined-form offsets. The registry cell text was left unchanged by round 54 (its record).
- HEAD 5da0a63 sits two commits past the freeze commit; the intervening diff touches only
  round-58 controls and s101-open.txt. Working tree clean apart from untracked .ufo/waves/round-58/.

## Unrun checks

- Full `c2-count.py` battery (executor surface; not run by this scout seat).
- Any live fetch (forbidden; L0 open).

VERDICT: the round-58 re-opening of the S101 lane-owned capture survives as an admissible fresh
source opening — same committed bytes as rounds 49/54/57, but first opening in the pinned
capture-text.py defined form under round 54's sanctioned flip, with a frozen, reproduced,
disjoint 12-quote set; no evidence of frozen-predicate alteration or unauthorized egress found.
