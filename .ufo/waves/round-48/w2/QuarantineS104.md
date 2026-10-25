# QuarantineS104 — hand-check of chousa round3 `S104` (`payload-absent`)

**Verdict: PRESENT-in-source, ABSENT-AS-WRITTEN in the cached extraction — the
`payload-absent`/fabrication classification is a checker artifact, not a
defect.** The flagged string is the full sentence inside the gate block's own
*negative disclosure* ("the sentence in full … is **not contiguous in any
automated extraction**"). The harvester (`QUOTE_SPAN_RE`) grabbed the
disclosed sentence as a literal quote; the layout-mode cached text cannot
contain it contiguously — which is exactly what the note states. Re-extracting
the same captured PDF with `pdftotext -raw` recovers the sentence contiguous
(modulo line-wrap) at byte 19030. The only true writing deviation is a
two-codepoint terminator normalization (`。` written where the source prints
`．` U+FF0E ×2).

## Register row (frozen)

`quarantine-slice` line 11: `S104   payload-absent`

`absent-defect-register.md` line 47:
`| chousa | round3 | S104 | payload-absent | https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja | このプロセスに際して，誰が検索を行ったのか，その日時，使用した検索式を同時に記録しておくことが望ましい。これにより，研究の透明性を保ち，他者が同様の検索を再現できるようになる。 |`

Quote: 88 chars / 264 UTF-8 bytes, sha256 prefix `cb026b814f12c1d3`.

## Lane SOURCES row and gate block

Census-time id `S104` (quote-lint-full-v5.json, chousa/round3/S104, 3
findings: 2× folded/whitespace + 1× ABSENT). At `d9583b5a` the row was `S098`;
at HEAD (`lanes/chousa/round3/SOURCES-PROPOSED.md:71`) the same jstage row is
`S109`, gate block `#### Gate — S109` lines 79-93 — id drift, same URL+row.
ID-REMAP line 70 (`S104→S107`) tracks a different renumbering; URL+quote pin
the row unambiguously.

Gate block, lines 80-88 (verbatim):
```
URL: https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
Opened: 2026-10-23 (HTTP 200, 713,922 bytes; text extracted with pdftotext, 36,968 bytes)
Quote — section 7 …: "その日時，使用した検索式を同時に記録しておく"   <- declared contiguous run (present, exact)
Quote — section 7 …: "が同様の検索を再現できるようになる"             <- declared contiguous run (present, exact)
Quote — running foot, p.120: "日健教誌 第 32 巻 第2 号 2024 年"        <- census: folded/whitespace ✓
**Column note.** … the sentence in full — "このプロセスに際して…ようになる。" — is **not contiguous
in any automated extraction** … Only the contiguous runs are quoted above … stated … as prose, not as a quotation.
```
So the lane explicitly did **not** claim the full sentence as a quote; the
census harvested it anyway (sentence inside `— "…" —` on line 88 lacks any
SWEEP_HINT phrase → classified `literal`).

## On-disk captures (only evidence used; no fetch)

qcache key `sha256(url)[:24]` = `7194acc65a18f6555e4b8893`:

- `….pdf` = `….raw`, 713,922 B, sha256 `9315274a275172fe1cadacb8871264647211e50c07431e7fb127502554918d69` — HTTP-200 capture identical to gate attestation (713,922 B).
- `….txt`, 36,968 B, sha256 `05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f` — `pdftotext -layout` output (fetch() line ~480), matches gate attestation.

The journal sets sentence-final `．` (U+FF0E) everywhere: `．`×138, `。`×0,
`，`×259 in the extraction — the register's `。`×2 is the writer's
normalization, absent under all 11 census folds (TYPO lacks `．→。`).

Fragment positions in `….txt` (layout, byte offsets — interleaved):
start `27343` (left col, line 235), continuations `19989`/`20158`/`20327`
(right col, lines 184-186) — sentence wraps left-column-bottom →
right-column-top on journal p.121; each fragment verified present.

`pdftotext -raw` of the same `.pdf` (29,013 B): sentence at byte
**19030**, chars 7299/7320/7346/7372 separated only by `\n` —
`match(raw, q．variant)` = `no-whitespace` fold hit.

## Reproduced check (cache + local re-extract only)

```
ql.match(layout_txt, quote)          -> None      # census ABSENT reproduces
ql.match(layout_txt, quote with ．)  -> None      # interleave, not punctuation, blocks it
ql.match(layout_txt, 'その日時，使用した検索式を同時に記録しておく') -> exact
ql.match(layout_txt, 'が同様の検索を再現できるようになる')          -> exact
ql.match(layout_txt, '日健教誌 第 32 巻 第2 号 2024 年')           -> whitespace
ql.match(raw_txt,  quote)            -> None      # 。 vs ． only
ql.match(raw_txt,  quote with ．)    -> no-whitespace   # PRESENT
```

Companions: none generated (`_pdf/` URL, not `_article/`; `paper` kind, no
sibling filenames) — "companion URLs checked" is vacuous here. Local artifact
`merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38.md`
(4,914 B, sha256 `37d6ac65…`) contains only the contiguous-run recheck
fragment (line 7), as designed.

## Reason

The row is not a fabrication: every declared contiguous quote verifies
verbatim in the capture, and the "absent" sentence is verbatim-recoverable
from the captured source under a column-order-preserving extraction plus
whitespace fold and one terminator-glyph normalization (`．→。`). Two
independent check-side artifacts produced the ABSENT: (a) harvesting a
quoted example inside a negative disclosure as a `literal` quote; (b)
layout-mode interleaving, which the lane disclosed. Residual write-side
defect is minor: the disclosure's example normalizes `．`→`。` and the
id the register cites (`S104`) no longer matches HEAD (`S109`). For C1: this
row does not stand as a true `payload-absent` instance — if the predicate
needs the row to be a real fabrication, S104 counts against it; the defect
register row is a false positive of the fabrication class. Fix direction:
treat gate-disclosed non-contiguous spans as prose (skip `literal`), and/or
add a `．`/`。` typographic fold; the row itself needs no correction.
