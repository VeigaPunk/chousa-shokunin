# W2 hand-check — register row S088 (chousa, round2)

## Verdict: **absent-as-written** (quote refused as written; source content present in full)

## Row under check
- Quarantine slice line 6: `S088   payload-absent`
- Register row (`shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:42`):
  `chousa | round2 | S088 | payload-absent | https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf`
- Quote (94 chars): `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）ＭＴ / 磁盘（ｄｉｓｋ）ＤＫ / 光盘（ＣＤ－ＲＯＭ）ＣＤ / 联机网络（ｏｎｌｉｎｅ）ＯＬ / 缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）ＭＭ`

## SOURCES binding (id-renumber note)
The same URL+quote now sits at lane id **S093** (`lanes/chousa/round2/SOURCES-PROPOSED.md:45`,
gate block lines 38–46); register "S088" is the pre-rebind id. Gate line 45 is the exact
register quote. Gate line 46 itself warns: "this copy renders Latin letters in fullwidth".

## On-disk captures checked (read-only; none fetched)
```
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/
  0f33243fd7ac2fe88b85c1ba.pdf   6,209,520 B  sha256 cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41  (PDF 1.7, 45 pages, GB/T 7714—2025)
  0f33243fd7ac2fe88b85c1ba.raw identical sha256 (same PDF bytes)
  0f33243fd7ac2fe88b85c1ba.txt   190,614 B / 83,061 chars  sha256 13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f  (pdftotext -layout render)
```

## Commands run and observed output
1. `pdftotext -layout` (poppler 26.08.0) on the cached PDF → 190,614 B, sha256
   `13a34aa9…1182f` — **byte-identical to the cached .txt** (the capture is the layout render).
2. `pdftotext` (raw mode) → 166,687 B, sha256 `94e00b96…f174cd050`.
3. Match attempts vs both renders — all **-1**:
   exact; NFKC-folded; NFKC + whitespace-collapse; newline-variant (` / `→`\n`); space-variant.
4. Aggressive fold `[\s/／]+ → ''` on both sides: **match at folded offset 38572** — the quote's
   entire token sequence sits contiguously in the table block.
5. Component-term hits (layout render): 磁带@59025, 磁盘@59073, 光盘@59116, 联机网络@59161,
   缩微资料@59201(+4822 foreword), codes ＭＴ@59063, ＤＫ@59108, ＣＤ@59119/59153, ＯＬ@59166+,
   ＭＭ@59243 — all inside one block, char 58854–59243 (byte offset ~128,850).

## What the capture actually reads (chars 58891–59243, page 29, 表Ａ．２ 电子资源载体和标识代码）
```
    电子资源的载体类型                          载体类型标识代码
    磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）                     ＭＴ
       磁盘（ｄｉｓｋ）                           ＤＫ
     光盘（ＣＤ－ＲＯＭ）                           ＣＤ
     联机网络（ｏｎｌｉｎｅ）                         ＯＬ
缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）                 ＭＭ
```
Raw-mode render interleaves cells (`ＭＴ\nＤＫ\nＣＤ\nＯＬ\n` separated from names) — still no
single-line `…ＭＴ / …ＤＫ / …` form.

## Reason
The five name→code pairs of 表Ａ．２ are present **verbatim, including the fullwidth Latin**, but
as a two-column table; the register quote is a single-line ` / `-joined linearization that no
extraction of this PDF produces. Longest contiguous verbatim run vs the quote is
`联机网络`+context ≈26/94 chars (matches the frozen round-42 verdict at
`corpus/evidence/round42/quarantine-verdicts.tsv:7`, which called the same 83,061-char capture
absent with a 26-char longest run). One correction to that record's phrasing: it says the
rendering does not reproduce "its full-width media-type characters" — they **are** reproduced;
what is not reproduced is the column layout, and the ` / ` separators are the gate's own
linearization convention, never literal text. So: not fabricated, not unverifiable —
**absent-as-written**; correct resolution is to quote the table rows as rendered (or annotate
the linearization), per the round-42 flip condition.

## Confidence / remaining unknowns
High — byte-identical re-render of the cited PDF plus three match modes. No live fetch
performed (L0 open); no companion URLs exist for this row. C1 note: this row is a rendering
mismatch the census correctly flagged ABSENT, but its "in none of them" phrasing overstates —
the cited content is fully on disk under a documented fold; a polarity/precision counter that
scores `payload-absent` rows as quote-refusals remains accurate here.
