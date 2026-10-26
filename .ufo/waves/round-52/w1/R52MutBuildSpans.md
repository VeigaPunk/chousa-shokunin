# R52MutBuildSpans — mutation test of the C2 capture binding (builder docx form)

Seat: R52MutBuildSpans (leaf; no subagent dispatch). Godspeed framing: batched parallel tool calls,
no clarifying questions. No tool installs performed (read `~/.omp/agent/RULES.md` first; pacman
paused host-wide; nothing was needed). `TMPDIR=/fast/scratch/hyaku/chousa-r52/R52MutBuildSpans`
for every run; scratch removed at finish.

## Setup (evidence)

- Scratch root `S=/fast/scratch/hyaku/chousa-r52/R52MutBuildSpans`; `ev/` holds copies of
  `corpus/evidence/round52/build-spans.py` and `c2-count.py` from the lane (copied byte-identical;
  sha256 `1732615412cf604f6af1bab983cafeeece953aa0344b7449729fea93bd144443` matches the lane file).
  `c2-count.py` imports `build-spans.py` from its own directory, so `ev/build-spans.py` is the
  mutated builder for the mutant-counter leg; the real lane `c2-count.py --root S/lane` is the
  unmutated frozen counter (lane `LANE`/git context intact; the scratch lane root supplies the
  spans manifest — the other C2 legs fail only for the absent scratch registry/entries, which is
  irrelevant to the binding leg).
- Capture: NIPH `https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx`; cache key
  `sha256(url)[:24]=3a8b45977cd111e45e3980a5`; `.raw` 178056 bytes, first bytes `PK\x03\x04`;
  main part `word/document.xml` via `_rels/.rels` rId1 (Type ends `/officeDocument`).
  `python3 tools/capture-text.py <raw>` yields the text form; builder `docx_text` agrees:
  both 19682 chars, equal strings.
- Quotes (located with `capture-text.py <raw> --locate`; each exactly once; no tab/newline;
  ≤25 whitespace words, ≤160 chars). Machine rows (planned lane id S115, entry path as in the
  staged C2 entry):

```
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	PRISMA(Preferred Reporting Items for Systematic Reviews and Meta-Analyses)声明	corpus/knowledge/japanese-search-record-niph-form-r52.md
```

  `LOCATED count=1 offset=8996 / 9257 / 9408` respectively.
- Baseline (pristine builder): `QUOTE S115 char 8996 spans/S115-1.txt`, `char 9408 …-2`,
  `char 9257 …-3`; `SPANS_ROWS=3 WRITTEN=3`; mutant-counter replicate: `CAPTURE_BOUND=3/3`;
  frozen counter: `CAPTURE_BOUND=3/3`.

## Mutants (smallest behavior-bearing point in `raw_form`/`docx_text`)

- **M1 — always UTF-16LE**: `raw_form` drops the `PK\x03\x04` branch; always
  `b.decode("utf-16le", errors="replace")`.
- **M2 — Fallback not skipped**: deletes `if el.tag == _FALLBACK: return`; the walk descends into
  `mc:Fallback` subtrees (60 in document.xml; 19 hold text in VML textboxes, e.g. `目標値に到達`).
- **M3 — instrText emitted**: `w:t` check widened to `el.tag in (_W+"t", _W+"instrText")`
  (50 `w:instrText`; TOC + PAGEREF field codes).
- **M4 — no newline at w:p**: deletes the `w:p`-end `out.append("\n")` (1240 `w:p`).

## Results

| mutant | builder | mutant-counter CAPTURE_BOUND | frozen-counter CAPTURE_BOUND | verdict |
| --- | --- | --- | --- | --- |
| M1 | exit 1, refused all 3 (`3a8b…raw:0x`) | n/a (no spans) | n/a | **KILLED — builder refusal** |
| M2 | exit 0, `char 8996/9408/9257` (identical to pristine) | 3/3 | 3/3 | **SURVIVES both counters** |
| M3 | exit 0, `char 10293/10705/10554` | 3/3 | 0/3 | killed only by frozen counter (offset drift) |
| M4 | exit 0, `char 8477/8859/8710` | 3/3 | 0/3 | killed only by frozen counter (offset drift) |

Evidence text: M2 text form length 19787 (>19682; first diff from pristine at char 12318 — the
first non-empty Fallback insertion — every span window ends ≤9417); M3 length 20979; M4 length
18463 = 19682 − 1219 removed paragraph newlines.

## Why M2 survives; quote that kills it

- M2 survives because all three chosen quotes lie in section 3.1/3.2 prose (offsets 8996–9408)
  **before** all non-empty `mc:Fallback` content (first insertion at 12318), so the mutant form is
  identical in every span window and at every quote offset; neither the mutant counter nor the
  frozen counter sees the fallback emission (both 3/3).
- Killer quote: `目標値に到達` — exactly once in the pristine form (offset 13246, pristine builder
  builds: exit 0, `QUOTE S115 char 13246`); under M2 it is emitted from *both* the Choice textbox
  and the Fallback VML textbox (count 2), so the builder refuses:
  `build-spans: refused S115: quote not exactly once in any form (…3a8b…raw:2x): '目標値に到達'`
  (exit 1). Representable in quotes.tsv (no tab/newline).
- M3/M4 also survive their own mutant counters: every `w:instrText` insertion borders a tab or a
  paragraph boundary, and M4 only removes `\n`, so no **representable** quote (quotes.tsv is
  tab/newline-separated) can change a quote's occurrence count under M3/M4. Killer quotes exist but
  are unrepresentable: `【目次】\n\n0. 要旨` (count 0 under M3) and
  `文献検索期間\n\n2015年1月から2018年10月まで` (count 0 under M4; both count 1 in pristine);
  feeding either into quotes.tsv yields a parse error (exit 2, `need 4 non-empty tab cells`).
  The frozen counter catches M3/M4 only by offset drift (CAPTURE_BOUND=0/3) — i.e. the quotes sit
  after early removed/inserted characters.

## VERDICT: Attacked the C2 capture binding through the builder's docx form with 4 mutants.
M1 killed by builder refusal; M2 (Fallback not skipped) is the surviving mutant — the chosen quotes
avoid the mutated construct, and `目標値に到達` (exactly-once pristine, 2x under M2) kills it; M3/M4
survive their own mutant counters and are caught only by the frozen counter's offset drift, with no
representable killer quote (quotes.tsv cannot carry tab/newline-bearing quotes).
