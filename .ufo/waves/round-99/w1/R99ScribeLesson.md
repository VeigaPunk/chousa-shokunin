# R99ScribeLesson — round-99 lesson scribe: Gate/Mistakes/LOG drafts + falsification findings

Seat: `R99ScribeLesson` (wave `w1`, lane `chousa`, round 99). Attacked tree: F `d41f4cd8b857c6de683e7be5c5e8125b32763a8e`
(clone at `/fast/scratch/hyaku/chousa-r99/R99ScribeLesson/repo`, obtained by
`git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin repo` then
`git -C repo checkout -q d41f4cd8b857c6de683e7be5c5e8125b32763a8e`). Base `47ed34fa785288837f84cde9db15c41300854a78`.
All batteries were run against the clone, never against the live lane. Scratch deleted on exit.

Deliverables written (this seat's own paths only):

- `.ufo/waves/round-99/w1/R99ScribeLesson-lesson-draft.md` — the round-99 lesson `## Gate` + `## Mistakes` draft.
- `.ufo/waves/round-99/w1/R99ScribeLesson-log-draft.md` — the LOG.md round-99 entry draft.
- `.ufo/waves/round-99/w1/R99ScribeLesson-*.txt` — every receipt cited below (20 files).

## Behavior — what the round's own instruments do at F

All measurements re-run by this seat, not taken from the lane's committed receipts.

| instrument | command | observed | exit |
|---|---|---|---|
| C1 battery at F | `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>` | `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5` / `CHALLENGE_CONTROLS_R99=PASS` | 0 |
| C1 battery with the BASE tool | `… --tool <base tool> --no-oracles` | `NEG_REFUSED=0/7 … PROD_REFUSED=0/4 … CHALLENGE_CONTROLS_R99=FAIL` | 1 |
| C2 gate-records | `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md` | `GATE_RECORDS files=1 records=25 ok=25 fail=0` | 0 |
| C2 metadata | `bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-rates-r99.md --root .` | `METADATA_COMPLETE=1/1` / `RESEARCH_GATE: CLEAN` | 0 |
| C2 search re-run | `python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .` | `rev_match=4/4` / `SEARCH_RERUN: CLEAN` | 0 |
| C2 controls at F | `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` | `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0 BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2` / `ENTRY_CONTROLS_R99=PASS` | 0 |

Receipts: `R99ScribeLesson-battery-at-F.txt`, `R99ScribeLesson-base-battery-at-F.txt`,
`R99ScribeLesson-entry-controls-at-F.txt`, `R99ScribeLesson-c2-base-vs-fixed.txt`.

## Gates — the lesson's `## Gate` bullets, each quote located by this seat

Each bullet below was checked against the committed capture bytes, not against the lane's draft. Quotes were located by
this seat's own script (`R99ScribeLesson-quotes-located.txt`), which normalizes exactly as `tools/gate-records.py` does
(curly quotes → straight, whitespace collapsed) and re-locates every quote in its capture; it also checks that each
S236 quote is inside the record's `abstractText` field, not merely in the capture.

| id | URL | fetch time | decision | located quote (≤25 words) | where located |
|---|---|---|---|---|---|
| S232 | `https://peerj.com/articles/1364/` | 2026-11-09T04:00:32Z | reject (403, curl rc 22) | — no bytes, no capture | `corpus/evidence/round57/refetch.tsv:204` |
| S233 | `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727` | 2026-11-09T04:00:33Z | admit, tier A | "A total of 15 studies met the criteria for inclusion in the primary quantitative analysis." (15 words) | `corpus/captures/4b70901ad80c513f0c2f750c.txt` line 910 |
| S234 | `https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z` | 2026-11-09T04:00:33Z | reject (route: http 200 challenge page) | — no document text; the body is a challenge page | `corpus/captures/b90988847e704a08aabc8321.txt` line 8 ("Client Challenge"), line 14 ("A required part of this site couldn't load.") |
| S235 | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML` | 2026-11-09T04:00:42Z | reject (500, curl rc 22) | — no bytes, no capture | `corpus/evidence/round57/refetch.tsv:207` |
| S236 | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json` | 2026-11-09T04:01:07Z | admit, tier B | "We carried out a systematic review, meta-analysis and meta-regression of quotation errors, taking account of differences between studies in error ascertainment." (21 words, `abstractText`) | `corpus/captures/405a0054e1f6dbd1854a3618.txt` (one-line JSON), field `abstractText` |

Web-search query (one, the session's search tool, 2026-11-09):
`Jergas Baethge 2015 Quotation accuracy in medical journal articles systematic review meta-analysis PeerJ`
(committed at `corpus/SOURCES.md:432`).

S236 identity re-checked by this seat from the capture's JSON: `pmid` 26528420, `doi` 10.7717/peerj.1364, `pubYear` 2015,
`journalInfo.journal.title` PeerJ, `journalInfo.volume` 3 — the five fields kill rule K3 names
(`R99ScribeLesson-quotes-located.txt`).

## Touched surfaces

Read only: `.ufo/waves/round-99/claims.{md,json}`, `plans/round-99.md`, `corpus/lessons/round-98.md`,
`corpus/lessons/round-98-verifier-spotcheck.md`, `corpus/evidence/round99/egress-approval.md`,
`corpus/evidence/round57/refetch.tsv` rows S230–S236, the captures those rows name, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `corpus/knowledge/quotation-error-rates-r99.md`, `tools/gate-records.py`,
`tools/research-gate.sh`, `tools/search-rerun.py`, `tools/quarantine-check.py`,
`corpus/evidence/round99/challenge-controls-r99.py`, `corpus/evidence/round99/entry-controls-r99.py`,
`corpus/evidence/round98/gate-records-challenge-200.txt`.

Written (this seat's own paths only): the three files named under Deliverables plus the 20 `R99ScribeLesson-*.txt`
receipts in the same directory. No production file, no lane file, no fleet-root file was written. No git/jj mutation, no
commit, no push, no network fetch (every URL in the round was re-read from committed bytes only), no `sudo`, no sysctl, no
service restart.

## Findings

### F1 — the C2 controls' NUMBERS leg accepts a Do-cell number that is NOT printed in its warrant (the check is a substring test)

The entry-controls NUMBERS leg extracts each number from a Do cell and asks `n in wtext`, where `wtext` is the
concatenated warrant text (`corpus/evidence/round99/entry-controls-r99.py:104`, `nums_ok += n in wtext`; the number
regex is line 40, `NUM = re.compile(r"[0-9]+(?:[.,][0-9]+)*%?")`). It never asks whether the number is *printed* as a
token. A number that is only a **suffix** of a warrant's number therefore passes.

Exact commands (each run in a scratch copy of the F clone, `entry-controls-r99.py --root .`):

```
# forgery A: row 7 Do cell, warrant G11
sed-equivalent edit: "64.8% of content errors were major" -> "8% of content errors were major"
CASE NUMBERS 6/6 PASS
ENTRY_CONTROLS_R99=PASS
    exit=0

# forgery B: row 1 Do cell, warrant J2
edit: "total quotation errors at 25.4% and major ones at 11,9%" -> "… at 5.4% and major ones at 11,9%"
CASE NUMBERS 6/6 PASS
ENTRY_CONTROLS_R99=PASS
    exit=0

# forgery C: row 7 Do cell, warrant G11
edit: "64.8% of content errors were major" -> "2% of content errors were major"
CASE NUMBERS 6/6 PASS
ENTRY_CONTROLS_R99=PASS
    exit=0

# control: a number that is a substring of no warrant number
edit: "64.8% …" -> "63.8% …"
CASE NUMBERS 5/6 FAIL
ENTRY_CONTROLS_R99=FAIL
    exit=1
```

Receipt: `R99ScribeLesson-c2-numbers-substring.txt`.

The boundary is exactly the substring relation: `63.8%` is refused, `8%` / `2%` / `5.4%` are accepted. This does **not**
make C2's sentence false — the landed entry's own Do-cell numbers are all printed in their warrants (checked
independently: `28`, `25.4%`, `11,9%`, `14.5%` in row 1's J1/J2/J5/G10; `6.7%` in row 5's J3; `64.8%` in row 7's G11; the
two word-numbers `one sixth` (row 3, warrant J4) and `about half` (row 5, warrant G7) are also printed — see
`R99ScribeLesson-do-cell-numbers.txt`). It is a **control gap**: the C2 kill rule K2 ("a Do-cell number not printed in
that row's own warrant quotes") is not enforced by the shipped control for a number that is a suffix of a printed one.
A forger can state "8% of content errors were major" where the source says 64.8% and the whole control suite still
passes. Fix direction: make the leg match the number as a token (word-boundary or `\b`/negative-lookaround on the
percent form), not as a bare substring, and add the word-number forms ("one sixth", "about half") to what it counts —
the leg's regex `[0-9]+(?:[.,][0-9]+)*%?` sees no digits at all in "less than one sixth", so those two Do-cell numbers
are never checked (same receipt, `R99ScribeLesson-do-cell-numbers.txt`: 6 digit-number tokens counted across 8 Do
cells).

### F2 — QUALITY 229's lexical floor, run at F, still does not see S234's page (the assigned candidate, confirmed)

`corpus/QUALITY.md` 229's check, run verbatim against the F clone:

```
for k in $(/usr/bin/grep -ohE 'capture=corpus/captures/[0-9a-f]{24}\.txt' corpus/knowledge/*.md corpus/lessons/*.md | cut -d= -f2 | sort -u);
do /usr/bin/grep -lE 'Checking your browser|Cookies must be enabled|Just a moment|reCAPTCHA' "$k"; done
loop_rc=1     # printed nothing
```

Two independent reasons the criterion misses the round's own new challenge page:

1. **Scope.** The loop visits only captures *cited by a GATE-RECORD in `corpus/knowledge` or `corpus/lessons`* — 28
   captures at F. S234's capture is cited by **no** GATE-RECORD anywhere (the only reference is `corpus/SOURCES.md:246`,
   prose), so the loop never opens it. (`R99ScribeLesson-quality229-at-F.txt`; the cited set is
   `R99ScribeLesson-quality229-at-F.txt`, header; S234's key `b90988847e704a08aabc8321` is absent from it.)
2. **Vocabulary.** Even applied to the file directly, the four wordings do not match: `/usr/bin/grep -lE
   'Checking your browser|Cookies must be enabled|Just a moment|reCAPTCHA' corpus/captures/b90988847e704a08aabc8321.txt`
   → `grep_rc=1`, no output. The page says "Client Challenge" and "A required part of this site couldn't load." — and
   the *round-98 witness form* of the same check (over every stored capture) lists four challenge captures
   (`0954149536…`, `58725f5e…`, `b5b8d050…`, `ff9013bd…`) and **not** S234's
   (`R99ScribeLesson-quality229-witness.txt`).

So QUALITY 229's check, as written, cannot detect the round's new challenge page; the F gate can
(`CASE PROD S234 rc=1 verdict=CHALLENGE PASS`, `corpus/evidence/round99/after/c1-all.txt` line 15, vs the base tool's
`CASE PROD S234 rc=0 verdict=OK FAIL`, `corpus/evidence/round99/before/c1-base.txt` line 16). The lesson's Mistakes row 1
cites this, and the receipt line that shows the fix able to fail is the same `after/c1-all.txt` line 15.

### F3 — the round-98 challenge receipt no longer reproduces under F

`corpus/evidence/round98/gate-records-challenge-200.txt` is a committed file that carries a GATE-RECORD line quoting
S230's reCAPTCHA page, and its text records the base tool's verdict `S230 OK` (exit 0). Under F the same file prints
`S230 FAIL CHALLENGE` (exit 1):

```
$ python3 -B tools/gate-records.py verify --root . corpus/evidence/round98/gate-records-challenge-200.txt
GATE_RECORD corpus/evidence/round98/gate-records-challenge-200.txt:5 S230 FAIL CHALLENGE
GATE_RECORDS files=1 records=1 ok=0 fail=1     rc=1
$ python3 -B <base tool> verify --root . corpus/evidence/round98/gate-records-challenge-200.txt
GATE_RECORD corpus/evidence/round98/gate-records-challenge-200.txt:5 S230 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0     rc=0
```

Receipt: `R99ScribeLesson-round98-receipt-under-F.txt`. This is a *verdict flip on a committed file* — the only one in
the whole repo (see F4). It is not a defect in the fix (the flip is the fix working as intended), but the round-98
receipt is now a stale statement of what the tool does, and QUALITY 229 cites that file as its evidence. Worth a note
in the lesson's Gate or a routed defect: either amend the receipt with the F verdict or state that it records the base
tool.

### F4 — repo-wide, the F tool changes 91 committed files' output, and the battery's HARM leg covers 25

A sweep of every committed file containing a tool-parsed GATE-RECORD line (657 files) compared F's output to the base
tool's, file by file:

```
total files with tool-parsed GATE-RECORD lines: 657
setup errors: 0 | identical: 566
OK under base -> FAIL under F (verdict flips): 1
    corpus/evidence/round98/gate-records-challenge-200.txt
already-FAIL, extra code appended: 90
    .ufo/waves/round-85/... .ufo/waves/round-86/... .ufo/waves/round-87/... (forge fixtures, e.g.
    .ufo/waves/round-87/w1/receipts/R87ExecForge/f5/neg-tabb.md)
```

Receipt: `R99ScribeLesson-verdict-change-class.txt`.

The 90 "extra code appended" files are all round-85/86/87 *forge fixtures* under `.ufo/waves/` — they already failed
under the base tool (for `REFETCH`, `CAPTURE_SHA`, `QUOTE_ABSENT`, …), and F adds `CHALLENGE` to their code list because
their captures are the lane's old cookie-wall pages. Their recorded receipts therefore under-state the code list under F.
No verdict flips there; only the one in F3.

The battery's HARM leg covers 25 files — the `corpus/knowledge` + `corpus/lessons` files with a GATE-RECORD line — and
all 25 are byte-identical under F and base (`HARM_SAME=25/25`). I checked the leg's file-selection regex against the
tool's own parse predicate over the whole repo: the leg's `^\s*GATE-RECORD\s` misses 14 lines the tool *does* parse
(BOM/ZWSP-prefixed records and one bare `GATE-RECORD`), all in `.ufo/waves/round-83…87` forge fixtures
(`R99ScribeLesson-harm-gap-scan-repo.txt`) — none in `corpus/knowledge` or `corpus/lessons`, so the HARM=25/25 figure is
not weakened. But the leg's file set is narrower than the tool's parse set, which is why a repo-wide sweep was needed to
find F3 at all.

### F5 — QUALITY 230's check (the lane's own new criterion, `corpus/QUALITY.md` working tree) is vacuous in one direction and
silent in another

The live lane's working tree adds QUALITY 230, whose check is
`python3 -B tools/gate-records.py verify --root . corpus/knowledge/*.md corpus/lessons/*.md | /usr/bin/grep -c 'FAIL.*CHALLENGE'`
printing 0. Three measurements:

```
# (a) the real tree, fixed tool:      0    grep_rc=1   (the intended "no challenge record" reading)
# (b) the gate never runs at all:      0    grep_rc=1   (--root /nonexistent-root → gate exit 2, stdout empty)
# (c) the BASE (unfixed) tool:        0    grep_rc=1   (the pre-fix tool also prints 0)
```

Receipts: `R99ScribeLesson-quality230-vacuity.txt`, `R99ScribeLesson-quality230-base-vs-fixed.txt`,
`R99ScribeLesson-quality230-discriminating.txt`. The check does discriminate in the useful direction: with a planted
challenge record in a scratch knowledge file it prints 1 (exit 0), so it is not vacuous overall — but (b) shows it prints
0 when its subject never ran, and (c) shows it prints 0 under the tool that has no CHALLENGE code at all, so it cannot
tell "the fix is present" from "the gate is broken". A criterion whose check cannot fail on a broken subject is the same
shape as QUALITY 229's (a lexical floor that passes), which is what QUALITY 230 was written to replace. Recommend the
criterion also pin the gate's own summary line (e.g. require `GATE_RECORDS … ok=N fail=0` and a non-zero record count)
so that a gate that exits 2 is a failure, not a pass.

### F6 — named limits (c) and (b) of C1 hold; one detail confirmed exactly

Measured directly against `tools/gate-records.py` at F
(`R99ScribeLesson-named-limit-c.txt`, `R99ScribeLesson-boundary-200.txt`):

- limit (c) "no NFKC, so full-width letters or a zero-width character inside a marker pass" — **confirmed**: full-width
  `Ｊｕｓｔ　ａ　ｍｏｍｅｎｔ` → `is_challenge=False`; `just a\u200bmoment` → `False`; `just a moment` → `True`. The
  curly-apostrophe case is *not* a pass (`A required part of this site couldn’t load.` → `True`) because the tool
  normalizes U+2019 → `'` before matching — the S234 capture's own apostrophe is U+2019 and it still trips the marker.
- limit (b)/(a) the 200-word bound — **confirmed at the boundary**: a page of exactly 200 words containing
  "just a moment" → `is_challenge=True`; 201 words → `False`. A marker split across a newline still matches
  (normalization collapses whitespace); a marker with a zero-width space inside it does not.
- The `SHORT` POS fixture is **28** words, not the "30-word page" the claim's and the battery's docstrings say
  (`R99ScribeLesson-short-fixture-words.txt`: `norm(SHORT).split()` = 28). A cosmetic number in two docstrings, but it is
  a stated count that does not match the bytes.

### F7 — the C2 decision table's word-numbers are outside what the control counts

Row 3's Do cell states "less than **one sixth** of all quotation problems" and row 5's states "source errors counted as
minor in **about half** the studies". Both are numbers; the control's NUM regex sees no digits in either, so
`NUMBERS=6/6` counts six of the eight numbers the Do cells state (`R99ScribeLesson-do-cell-numbers.txt`). The two
word-numbers *are* printed in their warrants (J4, G7), so the entry is right and the control is blind — the same shape as
F1, and the reason a fix for F1 should also cover word-numbers.

## Out of scope (noted, not attacked)

- The `merge/chousa/` assimilation surface and `considerthese/` — not this round's claims.
- The round-98 spot-check's routed survivor R32 (verify-line whitespace) — carried to round 100 by the plan, not this
  round's instrument.
- `tools/quarantine-check.py`'s separate `INTERSTITIAL_MARKERS` (19 markers, 6 of which the new `CHALLENGE_MARKERS`
  shares): it classifies the S234 and S230 captures as `interstitial` but the S229 cookie-wall captures as `page`, because
  it scans only the first 4,000 characters and lacks "cookies must be enabled". Two marker lists now exist in the lane
  with different coverage; the new one is the stricter of the two on the observed captures
  (`R99ScribeLesson-quarantine-check.txt`). Recorded as a fact for the L1, not as a defect claim.

## Findings summary

| # | kind | where | one line |
|---|---|---|---|
| F1 | control gap | `corpus/evidence/round99/entry-controls-r99.py:104` | the NUMBERS leg substring-tests Do-cell numbers, so `64.8%` → `8%` and `25.4%` → `5.4%` pass with `ENTRY_CONTROLS_R99=PASS`; K2 is not enforced for a number that is a suffix of a printed one |
| F2 | confirmed candidate | `corpus/QUALITY.md:1436-1439` | QUALITY 229's check at F prints nothing and cannot open S234's capture (not in its cited set) nor match its wording |
| F3 | stale receipt | `corpus/evidence/round98/gate-records-challenge-200.txt:5` | the round-98 receipt records `S230 OK`; under F the same file prints `S230 FAIL CHALLENGE` (exit 1) — the repo's only verdict flip |
| F4 | coverage | `corpus/evidence/round99/challenge-controls-r99.py` `harm_files()` | HARM covers 25 corpus files; 91 other committed files' output changes (90 gain a code) |
| F5 | criterion gap | `corpus/QUALITY.md` QUALITY 230 (live working tree) | its check prints 0 when the gate never ran and 0 under the base tool, so it cannot tell "fixed" from "broken" |
| F6 | confirmed limit | `tools/gate-records.py` (F) | limits (a)/(b)/(c) hold exactly; the `SHORT` POS fixture is 28 words, not "30" as two docstrings say |
| F7 | control gap | `corpus/evidence/round99/entry-controls-r99.py` NUM regex | the two word-numbers in Do cells ("one sixth", "about half") are never counted, so `NUMBERS=6/6` covers six of eight |

## Claims touched — verdicts

This seat is the lesson scribe, not a claim judge; the frozen claims' predicates were re-run for the lesson's Gate
section and are recorded above, but no verdict is claimed on C1 or C2 by this seat.

VERDICT: R99ScribeLesson C1 n/a — the lesson scribe re-ran the C1 battery and its gate at F (PASS, `NEG_REFUSED=7/7 … ORACLES_REJECTED=5/5`) and drafted the Gate/Mistakes text; judgment on C1's wording is left to the attack seats.

VERDICT: R99ScribeLesson C2 n/a — the lesson scribe re-ran the four C2 counting commands at F (all pass, `records=25 ok=25`, `METADATA_COMPLETE=1/1`, `rev_match=4/4`, `ENTRY_CONTROLS_R99=PASS`) and located all 23 quotes in their captures; judgment on C2's wording is left to the attack seats.
