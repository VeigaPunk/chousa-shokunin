# QuarantineS096 — hand-check of register row S096 (chousa, round2)

Frozen slice: `.ufo/waves/round-48/assimilation/quarantine-slice` line 10:
`S096   payload-absent`. Register row: `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:46`
→ `chousa | round2 | S096 | payload-absent` with 3 quoted spans and reason
"cited source, companion URLs and local artifacts were all checked; the quote is in none of them".

## Row resolution (reg-id → lane row → capture)

- Register `S096` (campaign id-space) = lane staged row **`S101`** (SOURCES-PROPOSED
  id-space): `round-45/assimilation/staged-map.tsv:21` maps
  `S101 → jc.hit.edu.cn/…/1f6f2731-….doc`, key `6dc68fd6b32ce9c8dfcebce8`, `capture_chars=128416`, `quarantine_reg_id=S096`, r42 verdict `unverifiable`.
- Lane SOURCES row: `shokuknow/lanes/chousa/round2/SOURCES-PROPOSED.md:33` (S101,
  中国学术期刊（光盘版）检索与评价数据规范, tier B) + Gate block at `:106-110` —
  "Opened: 2026-10-23 (HTTP 200, 129,024 bytes; text extracted locally)".
- On-disk captures (`.ufo/waves/corpus-expansion-1/.qcache/`):
  - `6dc68fd6b32ce9c8dfcebce8.raw` — 129,024 B, sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; `file`: Composite Document File V2 (Word .doc, code page 936, 18 pages).
  - `6dc68fd6b32ce9c8dfcebce8.txt` — 157,816 B, sha256 `d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112`.
    Verified: `.txt` ≡ `raw.decode('utf-8','replace').encode('utf-8')` — i.e. the
    "text" capture is a **lossy UTF-8 re-decode of the binary .doc, not text
    extraction**. 128,416 chars, 14,486 U+FFFD, ~14 stray CJK glyphs; none of
    `根据GB3469`, `GB/T 7714`, `ISBN`, `ISSN`, `ISO 690` occurs. This explains the
    register's "quote is in none of them" and r42's "never rendered to text".

## Quote checks against the raw capture (UTF-16LE byte offsets)

Quote 2 (verbatim **PRESENT**): `根据GB3469规定，以单字母方式标识以下各种参考文献类型`
→ `.raw` UTF-16LE byte offset **3232** (§1.2); a spaced second instance `根据 GB 3469规定…` @24618 (§14.3.1).

Quote 1 (**absent-as-written**, spliced paraphrase): register quotes
`主要责任者…文献题名；文献类型及载体类型标志；其他责任者…版本（初版省略）；出版项（出版地出版者出版年）；文献出处或电子文献的可获得地址；文献起止页码；文献标准编号(ISBN，ISSN，……)`.
The .doc carries TWO copies of the 9-item list (§1.1 @2640–3190 and §14.2 @24272–24600);
neither matches as written:
- §1.1 list uses `载体类型标识` (not `标志`), fullwidth `（初版省略）`, `（出版地、出版者、出版年）`, `(ISBN，ISSN，……)` @3146 — commas inside parens differ.
- §14.2 list uses `载体类型标志`, halfwidth `(初版省略)`, `(出版地、出版者、出版年)`, `(ISBN,ISSN,…)` @24534.
- The register mixes §14.2's `标志` with §1.1's fullwidth parens/ellipsis and drops
  list letters a.–i. and parentheticals behind `…`. No verbatim hit for the span or
  its 10-char prefix.

Quote 3 (**absent-as-written**, rewritten): register quotes
`参考文献格式，参照 GB/T 7714，采用…顺序编码制；作者-出版年制`. Actual text:
- §15.7 @68748: `参考文献格式，参照ISO 690，采用1位字母：n——顺序编码制（Numeric references method）；d——作者-出版年制（First element and date me…` — says **参照ISO 690**, not `参照 GB/T 7714`.
- §14.1 @23992: `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。` — GB/T 7714 + both styles, different wording, no `参考文献格式，参照`.
- `GB/T 7714` occurs @24000,24054,28724,61308; `顺序编码制` @24026,26114,67332,68802;
  `作者-出版年制` @24080,60894,60950,63708,64880,68874 — none yields the quoted span.
- The string `参考文献格式，` followed by `参照` never precedes `GB/T 7714` in the capture.

## Verdict

**absent-as-written — per-quote split: q2 PRESENT verbatim @3232; q1 & q3 absent-as-written but grounded.**

- Not `unverifiable`: a real local capture exists and decodes (UTF-16LE OLE stream);
  the r42 "binary office document never rendered" gap is resolved by byte-level
  UTF-16 search. The `.txt` artifact is proven to be mojibake of the `.raw`, so the
  original payload-absent finding was an encoding artifact of the check, not absence.
- Not `present` for the row: quotes 1 and 3 do not occur verbatim under any fold
  (also checked no-space/fullwidth variants above). Per the wave convention
  (w1/Attack24: `absent (verbatim)` + grounded substance), the row's defect
  descriptor is defensible for q1/q3 while its blanket reason "the quote is in none
  of them" is falsified by q2.
- No fabrication: every load-bearing clause is in the payload — 9-element list
  (24322–24560), `根据 GB 3469` type-identification rule (24618/3232),
  顺序编码制/作者-出版年制 recommendation (23992–24096), §15.7 format codes (68782–68880).
  The defects are transcription-level: mixed fullwidth/halfwidth punctuation,
  `标识`/`标志` variant, `参照ISO 690`→`GB/T 7714` standard-swap in q3, and elisions
  rendered as `…`/`——` rewrites.

## Commands run

- `grep -rn '1f6f2731-8c87-4812-b7e2-9fad0069d508' shokunin/chousa-shokunin shokuknow` → staged-map.tsv:21, qcache keys, lane files.
- `file`, `sha256sum`, `wc -c` on both captures (digests above).
- `python3`: `txt == raw.decode('utf-8','replace').encode('utf-8')` → True.
- `python3` `d.find(q.encode('utf-16-le'))` over `.raw` → offsets listed above;
  verbatim hits only for q2 and `GB 3469`-spaced variant.
- `python3` window decodes `d[o:o+n].decode('utf-16-le')` @2640–3200, 24272–24660, 23900–24160, 68660–68920 → texts quoted above.

## Residual gaps

- q1/q3 were checked against the UTF-16LE text stream only; Word fast-save or piece-table
  runs could hide additional plain-ASCII mirrors, though all needle hits above were
  found and no second encoding (gb18030/utf-8) produced hits.
- The `.doc` also contains a GBK-encoded OLE layer not separately searched; `strings -e l`
  coverage via the UTF-16 needle set is the operative check. No live fetch (L0 8d77e6c1 open).
- No installs used; no scratch files created under /tmp (all reads in place).
