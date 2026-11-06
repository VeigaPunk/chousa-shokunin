# R83ExecReopen — C1 kill rule K2 (located): fire-or-hold

Seat: leaf executor, round 83 wave 1. Rule under test: C1 **K2 (located)** of
`corpus/evidence/round83/claims.md`:

> a declared quote of the entry does not occur (whitespace-collapsed, curly quotes folded) in its committed
> capture, or occurs there but is absent from the live page when a non-author re-open gets HTTP 200 and
> tag-strips it. An unreachable re-open is recorded, not a kill.

**Result: K2 does not fire. C1 holds on K2.** 16/16 declared quotes occur in their committed captures
(committed `.txt` and committed `.raw`), and 16/16 occur on the live pages, which returned HTTP 200 and are
byte-identical to the committed raw captures.

## Bytes attacked

| item | value |
|---|---|
| landing revision | `81b81173f19d175e2b2a6b409b2a496d09d0b258` |
| current tip | `aca2a781ef2db375881c21bf407e153f786ac61f` |
| entry blob at both | `2461a2ec24f2febc93aad43019381e062bd7c1dd` (`git rev-parse <rev>:corpus/knowledge/appraisal-judgment-records-r83.md` at both revisions, identical; `git diff --stat` landing..tip on the file is empty) |
| entry lines / quotes | 73 lines, 16 rows under `## Located quotes` |

Tree at the landing revision extracted with
`git archive 81b8117… | tar -x -C /fast/scratch/hyaku/chousa-r83/R83ExecReopen`.

## 1. Committed captures

Command (receipt `R83ExecReopen/committed-locate.txt`):

```
python3 -B locate_quotes.py --root /fast/scratch/hyaku/chousa-r83/R83ExecReopen --json committed.json
```

Observed last line `SUMMARY quotes=16 found=16 absent=0`, `EXIT=0`.

| qid | S-id | capture | line | status | words |
|---|---|---|---|---|---|
| Q1 | S009 | `ea16817cb78993196ea1a095.txt` | 492 | FOUND | 23 |
| Q2 | S009 | `ea16817cb78993196ea1a095.txt` | 494 | FOUND | 24 |
| Q3 | S009 | `ea16817cb78993196ea1a095.txt` | 494 | FOUND | 21 |
| Q4 | S212 | `708022d401fd771fc59bd1d9.txt` | 611 | FOUND | 14 |
| Q5 | S212 | `708022d401fd771fc59bd1d9.txt` | 611 | FOUND | 20 |
| Q6 | S212 | `708022d401fd771fc59bd1d9.txt` | 611 | FOUND | 12 |
| Q7 | S212 | `708022d401fd771fc59bd1d9.txt` | 611 | FOUND | 24 |
| Q8 | S212 | `708022d401fd771fc59bd1d9.txt` | 615 | FOUND | 23 |
| Q9 | S212 | `708022d401fd771fc59bd1d9.txt` | 716 | FOUND | 20 |
| Q10 | S212 | `708022d401fd771fc59bd1d9.txt` | 716 | FOUND | 21 |
| Q11 | S213 | `963807d173af711593fd1c45.txt` | 544 | FOUND | 16 |
| Q12 | S213 | `963807d173af711593fd1c45.txt` | 601 | FOUND | 20 |
| Q13 | S213 | `963807d173af711593fd1c45.txt` | 602 | FOUND | 16 |
| Q14 | S213 | `963807d173af711593fd1c45.txt` | 602 | FOUND | 15 |
| Q15 | S213 | `963807d173af711593fd1c45.txt` | 593 | FOUND | 20 |
| Q16 | S213 | `963807d173af711593fd1c45.txt` | 601 | FOUND | 21 |

Line numbers are 1-based lines of the committed `.txt`; the full capture line for each quote is printed in
`R83ExecReopen/committed-detail.txt`. Every match lies **within one line** of the capture — no quote is
stitched across a paragraph break by the whitespace collapse.

Same quotes against the committed `.raw` through the same stripper (receipt `R83ExecReopen/raw-locate.txt`):
16/16 FOUND, `EXIT=0`.

Curly-quote folding is load-bearing for Q1, Q5, Q9, Q10 and Q15 (their captures carry `‘ ’` where the entry
has `'`); without the fold those five would read ABSENT. That is exactly the normalisation K2 names.

Capture integrity: the `.raw` and `.txt` sha256 of all three captures equal the `raw_sha256` / `txt_sha256`
columns of their `corpus/evidence/round57/refetch.tsv` rows (S009 `e01497f8…`/`3dfd10e5…`, S212
`60c8ba69…`/`3b57cb03…`, S213 `342b82c4…`/`f5dae335…`) — all six MATCH. The capture keys are
`sha256(url)[:24]` of the three registry URLs (`R83ExecReopen/parse-integrity.txt`: 3/3 MATCH), and the entry's
`verified-at` line names exactly those three keys.

## 2. Live re-open — three GETs, one per URL

```
curl -sS -L --compressed --max-time 20 -A 'Mozilla/5.0 (chousa r83 reopen)' -o <S-id>.html -w '%{http_code}' <url>
```

| S-id | URL | HTTP | bytes | body sha256 | vs committed `.raw` |
|---|---|---|---|---|---|
| S009 | `…/assessing-risk-bias-included-studies-c52-c60` | 200 | 82846 | `e01497f87315171ee56b35c64bb8cb468278a0744df4ae0f33e57ea3ad49e7c5` | BODY_IDENTICAL |
| S212 | `…/handbook/current/chapter-07` | 200 | 179334 | `60c8ba69b4417596b1b377345d77d9f9d3b70fda6ad6f383cf01a8cb6de4f31b` | BODY_IDENTICAL |
| S213 | `…/handbook/current/chapter-08` | 200 | 159403 | `342b82c4204bc1ba57b6c66c3acac523a5e055f375603d368a9688dcddae3527` | BODY_IDENTICAL |

Receipts: `R83ExecReopen/live-sha256.txt` (sha256 + byte counts), `R83ExecReopen/live-locate.txt`
(`SUMMARY quotes=16 found=16 absent=0`, `EXIT=0`), `R83ExecReopen/live-excerpts.txt` (70 chars of live context
around each quote), `R83ExecReopen/live.json`.

All three live bodies are **byte-identical** to the committed raw captures, so the "absent from the live page"
arm of K2 cannot be reached by page drift either: the pages have not changed since the 2026-11-06T20:53Z
capture. 16/16 quotes FOUND after tag-strip (script/style/noscript/template/title dropped, comments dropped,
entities unescaped by `HTMLParser(convert_charrefs=True)`), whitespace collapse and curly-quote fold.

Live line numbers in the stripped live text (1-based, from `live-locate.txt`): Q1–Q3 S009 line 368; Q4–Q8
S212 line 394; Q9–Q10 S212 line 404; Q11–Q16 S213 line 394. They differ from the committed-capture lines in
§1 because the two strippers space blocks differently; each is an internal line of its own artefact, and the
committed-capture line is the citable one.

Stripper validation: rendering the committed `.raw` through the same stripper reproduces the FOUND/ABSENT
verdict of the committed `.txt` for every quote in every source (`raw_vs_txt_agree=3/3`, `7/7`, `6/6` in
`live-locate.txt`), so the live check is not an artefact of a private stripper.

## 3. Word counts

`wc -w` and `python str.split()` agree on all 16 quotes (receipt `R83ExecReopen/word-counts.txt`,
`OUT_OF_RANGE=0`, `EXIT=0`). Range observed: 12 (Q6) to 24 (Q2, Q7). **None outside 8..25.**

## Verdict on K2

Neither arm fires:

- committed-capture arm: 16/16 present, in both the committed `.txt` and the committed `.raw`;
- live arm: three HTTP 200 re-opens, 16/16 present, bodies byte-identical to the committed captures.

C1 is not falsified by K2. (K1, K3 and K4 are outside this seat's assignment and were not scored.)

## Residuals (out of class for K2, listed separately)

1. **Q1 and Q3 also occur verbatim in S212's capture** (lines 618 and 620) — Handbook ch.7 reproduces the
   MECIR C54/C55 text inside its own paragraph. The declared source S009 contains both, so K2 is satisfied;
   but the `source` column is not exclusive for those two rows. A K3 reviewer reading "Q1 (S009)" should know
   the identical sentences also sit in S212, where the surrounding paragraph is the ch.7 warrant. Not a defect
   under K2.
2. **Q2 is source-exclusive** and differs from the S212 variant: S009 line 494 has
   `correspondence with investigator etc.).`; S212 line 620 has `correspondence with investigator, etc).` The
   entry quotes the S009 form and attributes it to S009 — correct.
3. **Live line numbers are not the capture line numbers.** The stripped live text puts each block on its own
   line (S009 368, S212 394/404, S213 394), so the live line numbers in `live-locate.txt` differ from the
   committed-capture lines in §1. Character offsets into the collapsed live text are in
   `R83ExecReopen/live-excerpts.txt`. Neither is a defect; the committed-capture line is the citable one.
4. The three quoted fragments in the entry's `## Limits` section (outside the declared table) were checked as a
   courtesy: `could be assessed by just one reviewer`, `unless there are clear suggestions of the opposite`
   (S212) and `the absence of information leads to concerns about there being a problem` (S213) are all FOUND
   in both the committed capture and the live page (`R83ExecReopen/extra-fragments.txt`). The entry's prose
   gloss "when a machine-learning tool is used" is grounded in the same S212 paragraph (line 622: "including
   machine learning systems designed to semi-automate risk-of-bias assessment").

## Deviations recorded

1. **curl flags.** The wave item prescribed `curl -fsSL --compressed --max-time 20 …`; I ran
   `curl -sS -L --compressed --max-time 20 -w '%{http_code}'`. `-f` was dropped deliberately so a non-2xx is
   *recorded* as a status instead of collapsing into a curl failure; `-L` kept. All three returned 200, so the
   two forms are behaviourally identical on this run.
2. **UA.** The wave item prescribed `-A 'Mozilla/5.0 (chousa r83 reopen)'`; the egress table's seat row says
   "same UA", i.e. the campaign UA in `tools/capture-fetch.py` (`Mozilla/5.0 (X11; Linux x86_64)
   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36`). The two instructions disagree; I
   followed the wave item. No content effect: all three bodies came back byte-identical to the committed
   captures.
3. **`--max-time`.** 20 s (wave item) rather than 15 s (egress table). The three GETs completed in 2.4 s wall
   in total; no request came near either limit.
4. **One GET per URL, no retries**, no POST, no cookies, no credentials, nothing written to `corpus/captures/`
   or `refetch.tsv`. The three `.html` bodies were kept in scratch only and deleted; only their sha256 and byte
   counts are receipts.

No pacman, no `uv tool`, no `npx`, no binary install: no tool was installed or upgraded for this seat.

## Scratch

`/fast/scratch/hyaku/chousa-r83/R83ExecReopen` (tree, three `.html`, per-quote scratch files) removed with
`rm -rf` before yield. Every receipt cited above was written to
`.ufo/waves/round-83/w1/R83ExecReopen/` first.

VERDICT: R83ExecReopen C1 held — K2 (located) does not fire: all 16 declared quotes occur in their committed captures (`.txt` and `.raw`) and on three HTTP 200 live re-opens whose bodies are byte-identical to the committed raw captures, with every quote 12–24 words.
