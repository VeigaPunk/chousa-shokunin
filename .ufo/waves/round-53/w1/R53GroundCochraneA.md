# R53GroundCochraneA — re-ground staged S193 → planned lane S121

seat: R53GroundCochraneA (scribe, leaf member — no subagent dispatch)
read first: `corpus/evidence/round53/claims.md` (frozen at `a6ff732`). No predicate, target, counter or control was proposed changed; everything below is reported.
scope: the Cochrane Handbook chapter 4 capture and the staged entry `western-instrument-alignment-r50.md` (`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/…`) plus its staged row in `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:118`.
writes: this file only. scratch `TMPDIR=/fast/scratch/hyaku/chousa-r53/R53GroundCochraneA` (removed at exit). No git/jj mutation anywhere; no lane, fleet or shokuknow file touched.

## 1. The capture and its text form

```
$ ls -la /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ | grep c9d1e74c3ac8d9eb332c9770
-rw-r--r-- 1 vgpnk vgpnk 372430 Oct 24 22:05 c9d1e74c3ac8d9eb332c9770.raw
-rw-r--r-- 1 vgpnk vgpnk 211326 Oct 24 22:05 c9d1e74c3ac8d9eb332c9770.txt
```

python3 read of the `.txt` (UTF-8, whole file):

```
chars 210708 fffd 0
lines 1466
```

210,708 characters — the seat spec's figure — and **0 U+FFFD**. The raw: `raw chars 371804 fffd 0` (371,804 chars in 372,430 bytes, multibyte; 0 U+FFFD).

The raw is **HTML, not a PDF**: `<!DOCTYPE html>`, `<meta name="Generator" content="Drupal 11 …">`, `<title>Chapter 4: Searching for and selecting studies | Cochrane</title>`. `command -v pdftotext` → `/usr/bin/pdftotext` (installed, unused — no PDF here). Fidelity was therefore checked by re-stripping the raw independently (drop `script|style|noscript`, drop tags, `html.unescape`, collapse whitespace):

```
stripped chars 208474
1 Chapter 4: Searching for and selecting studies [last updated March 2025]
1 the reporting aligns with the current reporting guidance for PRISMA
1 Initiatives to provide access to ongoing studies and unpublished data constitute a fast-moving field
1 Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate
sentences sampled 40 missing 0
title match raw: True
```

Verdict on the text form: **faithful**. Each of the four target sentences occurs exactly once in the independently stripped raw, and 40/40 randomly sampled `.txt` sentences occur in it; the 210,708 vs 208,474 gap is whitespace/normalisation, not content. Two structural facts a span builder must know: (a) section headings appear **twice** (table-of-contents at 3885/4092, body at 9895/35424), so a heading string is never a unique quote (`count=2` for both `4.2.1 Role of the information specialist/librarian` and `4.3.2 Ongoing studies and unpublished data sources`); (b) the `.txt` carries page chrome — its tail is the cookie-consent banner (`We'd like to set cookies …`).

Section offsets in the `.txt` form: §4.2.1 body 9895–14288, §4.3.2 35424–44279, §4.5 111856–120985, §4.8 references 144863–end.

## 2. Claim-by-claim verdicts (every entry sentence that rests on this document)

| # | entry lines | claim (first 80 chars) | verdict | located evidence (`.txt` offsets) |
|---|---|---|---|---|
| 1 | :2 | `source: S193 — https://training.cochrane.org/handbook/current/chapter-04 — §4.2.1 Role of the information specialist…` | located, with a URL-identity caveat (F1) | headings at 9895 and 35424; both within the page whose canonical is the `www.cochrane.org` URL |
| 2 | :15-18 | `The **western** one … makes an explicit instrument-to-instrument statement in §4.2.1: the reporting …` | located-narrower | 13480 + 13592. The clause is scoped to *Cochrane* protocols/reviews/updates: "ensuring that the conduct of Cochrane protocols, reviews and updates meets the requirements set out in … (MECIR) relating to searching activities for reviews, and that the reporting aligns with the current reporting guidance for PRISMA … and PRISMA-S". The chapter never uses the word "instrument" (0 occurrences), so "instrument-to-instrument" is the entry's characterisation, not the document's wording (F3) |
| 3 | :18-19 | `In §4.3.2 it treats unpublished studies as a **bias** question rather than a reporting one — finding out about…` | located (bias clause) | 36552 + 36693, inside §4.3.2 (35424–44279): "Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate … is important for minimizing bias" |
| 4 | :18-19 | `… rather than a reporting one` | absent as an explicit sentence (inference, structurally supported) | no sentence in §4.3.2 frames the *reporting* of unpublished studies: its 10 "report" hits (37664, 37708, 39609, 40354, 41412, 41839, 42080, 42433, 43360, 43386) are CSRs, bias research and trial re-publication. Reporting lives in §4.5 (111856), which names PRISMA-S (113967/114035) and mentions "unpublished" only in a passing archival warning (118260) (F4) |
| 5 | :21-23 | `and notes that initiatives giving access to ongoing studies and unpublished data constitute a fast-moving field.` | located | 35599, inside §4.3.2 |
| 6 | :55-57 | `The handbook treats unpublished studies as a source of **bias** and folds them into the search as a matter of bias…` | located (bias), located-narrower ("folds them into the search") | 36552/36693; §4.3.2 is a subsection of §4.3 "Sources to search" (17785), so the folding is by section placement, and the section then defers detail to an un-captured supplement (F6) |
| 7 | :79-80 | `Whether the handbook's alignment statement still stands in the edition after version 6.5.1, whose chapter was last…` | located — version/date stamp | 7432 `Chapter 4: Searching for and selecting studies [last updated March 2025]`; 7633 `Interventions version 6.5.1 Cochrane, 2025` (both in the citation block at the chapter head) |
| 8 | :6 | `ground: … the western research-methods literature the Chinese sources cite only in translation, and what it says…` | absent in this document | the chapter makes no statement about Chinese sources or translation; this ground line rests on other corpus entries, not on this capture |
| 9 | :5 | `recheck: 180d — re-open the chapter and confirm the alignment sentence and the unpublished-studies sentence still read…` | procedural (not a document claim); its two targets are locatable today | alignment at 13480, unpublished/bias at 36552; `verified-at: 2026-10-24` matches the capture mtime (Oct 24 22:05) |

Also carried by the staged row (`SOURCES.append.md:118`, 11 cells, 1,551 chars, no truncation — the ellipsis visible in a `cut` view was my display only): cell 6 repeats claims 2–5 plus "an explicit **instrument-to-instrument alignment**" → same verdicts (located-narrower), and cell 5's anchor (`§4.2.1 … and §4.3.2 …; Handbook version 6.5.1, chapter last updated March 2025`) → located. The row's trailing clause ("because it does not name PRISMA-S at all") rests on S195, not on this capture.

Claims in the entry that do **not** rest on this document (not scored here): the S195/`指标 4`/`PRISMA counts 0` sentences (:25-34), "never names PRISMA-S at all" (:42-43), the PRISMA-S depth sentence (:45-48), 灰色文献 counts (:58), and "the PRISMA-S paper and the handbook chapter were already in place" (:66-67).

Located PRISMA-S / PRISMA 2020 inventory as asked: `PRISMA-S` at 13592 (§4.2.1), 96410, 97545, 98951, 100036 (§4.4.8), 113823+113842 and 114035 (§4.5), plus two §4.8 reference lines; `PRISMA 2020` at 96438, 98895, 99169, 99777 (§4.4.8), 114266, 114594, 114881 (§4.5), plus three §4.8 reference lines.

## 3. Machine lines

Every quote below: exactly once in the `.txt` form, on one line, ≤25 whitespace words, ≤160 characters, copied byte-exact (offsets in §2 and F5).

```
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Chapter 4: Searching for and selecting studies [last updated March 2025]	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Interventions version 6.5.1 Cochrane, 2025	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	the reporting aligns with the current reporting guidance for PRISMA ( Page et al 2021b , Page et al 2021a )	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	PRISMA-S ( Rethlefsen et al 2021 )	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Medical/healthcare librarians and information specialists have an integral role in the production of Cochrane reviews	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Initiatives to provide access to ongoing studies and unpublished data constitute a fast-moving field	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Review authors should therefore consult a medical/healthcare librarian or information specialist for current advice	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	It is important to identify ongoing studies, so that when a review is updated these can be assessed for possible inclusion	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	is important for minimizing bias	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	addresses the reporting of search strategies in systematic reviews	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram	corpus/knowledge/western-instrument-alignment-r50.md
```

(Quote 12 is the chapter's own reference-list line at 193214 — see F5.)

## 4. Findings routed to the L1 (reported, nothing patched)

- **F1 — the cited URL is not the served page's canonical.** The raw carries `<link rel="canonical" href="https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04" />`; the string `training.cochrane.org` occurs 8× in the raw but only as reference links (e.g. 154381, 154647, 200698, 201778), never as the document's own identity, and the chapter's self-citation says "Available from cochrane.org/handbook". The lane has seen this exact one-hop redirect before: `.ufo/waves/round-25/build/SrcCochraneUpdate.md:3` recorded training→www for chapter-iv. Effect on C2: binding keys on the recorded URL, so the row still binds; a recheck that follows the redirect lands on the canonical page (same chapter, same version stamp). Disclosure only.
- **F2 — the same chapter is staged twice.** `SOURCES.append.md:8` stages `| S083 | Cochrane Handbook …, Chapter 4 … — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04 …` scoped to §4.5 / MECIR Box 4.5.a (C36) and Box 4.4.g (C37) — the same document as S193 under the canonical URL. The lane registry's `S083` is a *different* document (AVeriTeC, `corpus/SOURCES.md:93`), so the two id spaces have diverged. Consequence for the expansion credit rule ("per document, not per entry"): if both staged rows land, the lane holds two registry rows for one chapter. The entry under judgement cites S193/S121, which is the correct one for §4.2.1/§4.3.2.
- **F3 — "instrument-to-instrument" is not the document's word.** `grep -c` equivalent over the `.txt`: `instrument` = **0** occurrences. The alignment sentence aligns *reporting* with PRISMA/PRISMA-S inside a MECIR *conduct* sentence for Cochrane reviews. The Gate should credit the alignment as located and the phrase "instrument-to-instrument" as the entry's own characterisation.
- **F4 — the "rather than a reporting one" contrast is inference.** §4.3.2 contains no reporting frame for unpublished studies; §4.5 is where reporting is discussed (and it names PRISMA-S at 113967/114035). The entry's reading is structurally sound but is not a sentence of the chapter; a Gate that demands a located quote for that clause cannot get one.
- **F5 — depth cross-link the L1 can use.** The chapter's reference list at 193214 reads `PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram` — the JMLA paper that planned S117 (`search-tracking-record-r40.md`) is to rest on. The planned S117 and S121 documents are therefore tied together by one located line in S121's own capture; usable in the round-53 lesson, and a cheap second quote for the S117 entry's cross-reference.
- **F6 — §4.3.2 defers its detail off-capture.** At 35478: `For further details on this topic, please refer to Section 1.2 of the online Technical Supplement and its subsections.` That supplement is not in `.qcache`, so no deeper ongoing-studies claim can be grounded from this round.
- **F7 — the `.txt` is page-level, not article-only.** The text form includes site chrome (cookie banner at the tail); span building must anchor inside the chapter body, and a span that runs to EOF would swallow navigation text.
- **F8 — counter state read (read-only).** `python3 corpus/evidence/round53/c2-count.py --lane-only` → `EXIT=1`, last lines `BOUND=0/5 (min 3) REFUSED=0 … QUARANTINE_BLOCKED_ADOPTED=0` / `C2=FAIL`. Expected at wave 1: nothing of C2 has landed. Independently confirmed the C2 base-line preconditions at `5b55013`: `git grep -c "<term>" 5b55013 -- corpus/knowledge | wc -l` → `0` for `tracking record`, `information specialist`, `质量控制指南`, `training.cochrane`; 75 files under `corpus/knowledge` at BASE; `corpus/knowledge/western-instrument-alignment-r50.md` **absent** from the lane (staged only). Planned lane id `S121` is free: registry max id is `S116`, `grep -c "^| S121 |" corpus/SOURCES.md` → `0`, so the REAL leg's S117–S121 remap is the next five ids.

## 5. Out of scope

S195 and the Chinese-guideline half of the entry (`指标 4`, `PRISMA counts 0`, 灰色文献 counts, the "never names PRISMA-S" premise) — other seats' documents; the entry's PRISMA-S depth sentence; the recheck calendar arithmetic; the C1 adopter and its counter. No production file, entry, row, lesson or span file was written; the L1 integrates.

## 6. Limits

No network and no live fetch (capture-only, L0 `8d77e6c1` open). The offsets are offsets into the `.txt` sidecar, which is what `build-spans.py` slices; the `.raw` is HTML and cannot host them. The 40-sentence fidelity sample is a sample, not an exhaustive diff. `pdftotext` exists but is irrelevant to an HTML capture.

VERDICT: attacked staged S193 (Cochrane Handbook ch.4) against the 9 claim units of `western-instrument-alignment-r50.md` — 6 located (2 of them narrower: Cochrane-scoped MECIR/PRISMA alignment; section-placement "folds into the search"), 1 located-narrower with 0 occurrences of "instrument", 1 absent-as-sentence (the "rather than a reporting one" contrast, inference-only), 1 absent-in-document (the translation ground line), 0 contradicted; text form faithful with 0 U+FFFD; C2 still `FAIL` lane-only (nothing landed), and the chapter's own reference list already names the tracking-record paper (off 193214).
