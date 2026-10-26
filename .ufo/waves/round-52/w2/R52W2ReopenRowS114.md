# R52W2ReopenRowS114 — falsify Registry row S114 (中国全科医学 PRISMA2020 条目清单)

Attack target: Registry row `S114` in `corpus/SOURCES.md` (line 124), capture re-opened read-only
at `…/.qcache/cacddf3bbf780a4c7582bb17.txt` (key `cacddf3bbf780a4c7582bb17` = sha256(url)[:24]), URL
https://www.chinagp.net/CN/column/item185.shtml. Every cell checked against the capture; the row's
anchors and the citing entry's char offsets re-derived with `text.find` on the same text form the
manifest uses.

## 1. Capture identity and text form

```
$ python3 - <<'EOF'
import hashlib
print(hashlib.sha256('https://www.chinagp.net/CN/column/item185.shtml'.encode()).hexdigest()[:24])
EOF
cacddf3bbf780a4c7582bb17
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/cacddf3bbf780a4c7582bb17.txt
b1c3cd6a5c22b97fd44c6c35367292a57c299fe19b5eb6c0b9c156bb3abe24f0  …/cacddf3bbf780a4c7582bb17.txt
```
The manifest `capture_sha256` for every S114 span equals that digest (`spans.tsv` col 3 =
`b1c3cd6a…`). Capture file: 11,676 bytes; strict UTF-8 decode succeeds; `open(…, encoding='utf-8').read()`
(universal newlines, CRLF→LF) = **6179 characters** — matching the row's `6179 characters` and the
entry's `6,179 characters`. `build-spans.py` reads the `.txt` with the same `read_text`, so the offset
contract uses this form.

## 2. Span manifest is self-consistent (canonical check)

```
$ python3 corpus/evidence/round52/build-spans.py --check --root /home/vgpnk/Projects/shokunin/chousa-shokunin
SPANS_ROWS=38 STALE=0
```
No stale/extra/orphan row or span file. Then I re-derived every S114 span against the capture: each
span file is the exact slice `form[offset:offset+len(span)]`, with the quote found at span position 80
(span 1 is clamped: offset 0, quote at 16):

| span | start | find(quote) | quote@spanpos | slice_eq |
|---|---|---|---|---|
| S114-1 | 0 | 16 | 16 | True |
| S114-2 | 840 | 920 | 80 | True |
| S114-3 | 1570 | 1650 | 80 | True |
| S114-4 | 1627 | 1707 | 80 | True |
| S114-5 | 1705 | 1785 | 80 | True |
| S114-6 | 5450 | 5530 | 80 | True |
| S114-7 | 5614 | 5694 | 80 | True |
| S114-8 | 5664 | 5744 | 80 | True |
| S114-9 | 6041 | 6121 | 80 | True |

Convention note: `spans.tsv` offset = quote offset − CONTEXT(80) (clamped at 0); the Registry anchor's
`char N` = the quote's absolute offset, i.e. start + 80. The +80 delta between the row's anchors and
the manifest starts is the documented builder rule, not a defect.

## 3. Cell-by-cell verdicts (all against the re-opened capture)

- **source (title/URL) — HOLD.** The row's first and only URL is `https://www.chinagp.net/CN/column/item185.shtml`; key matches. Capture text contains the site header/footer (`《中国全科医学》编辑部`, 冀ICP备12018774号-6), title `中国全科医学 报告清单` (char 16), table head `P RISMA2020 条目清单` (char 920; the inner space is in the capture), credit `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.` (char 5530) + `BMJ 2021;372:n71. doi: 10.1136/bmj.n71` (char 5694), `发布日期：2023-01-31` (char 5744), footer `网站版权 © 《中国全科医学》编辑部` (char 6121).
- **kind = docs — HOLD.** Rendered page text.
- **tier = A — HOLD.** Scope is precisely "what this journal page states … as the page shows them"; for that scope the page is primary. (A is argued by scope: the row makes no claim about PRISMA 2020 itself beyond what this page displays.)
- **scope — HOLD.** Items 6 and 7 exist verbatim: item 6 `信息来源` = `详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。` + `明确说明每一项来源 的 检索或查询日期`; item 7 `检索策略` = `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。` The "no translator named" clause verified: `翻译`, `译`, `translat`, `Translation` each occur 0 times.
- **anchor — HOLD.** `char 1650, 1707, 1785, 5530` equal `text.find` of quotes 3–6 on the 6179-char form (table above); each is a located quote of S114 occurring exactly once (build check refuses duplicates; all 9 are count-1).
- **teaches — HOLD.** Every clause is carried by the capture: table `报告清单` present; item 6 信息来源 and item 7 检索策略 rows present; credit line present; 发布日期 2023-01-31 present; text-form size 6179 chars accurate; four anchors accurate.
- **status = mined / opened 2026-10-26 / recheck 180d — HOLD.** Conventions match neighbor rows S113/S115/S116 (`mined`, same date, `180d`) and older rows (`mined` + `on-release`/`90d`/`365d` recheck styles). Entry line 6 also states `recheck: 180d`.
- **used-by — HOLD.** `grep -ln '^source: S114 ' corpus/knowledge/*.md` returns exactly one file: `corpus/knowledge/chinese-prisma-s-reception-r52.md` — identical to the row's used-by cell. No other knowledge file mentions S114 (grep across `corpus/knowledge/` excluding that entry: no matches).

## 4. Citing entry entailment (chinese-prisma-s-reception-r52.md)

All S114-cited offsets re-located and match: char 16, 920, 1650, 1707, 1785, 5530, 5694, 5744,
6121. Zero-counts claimed in the entry (`翻译`/`译`/`translat` 0; unspaced item-6/7 strings 0) all
confirmed. Inferences (item 6 dates each source; item 7 covers fewer source classes than item 6; page
is a hosted copy, not an attributed translation) follow from the capture text; the contrast with the
Japanese checklist entry is a cross-entry comparison, not a row claim.

## 5. Findings

No defect found in any cell of S114. The only anomaly any reviewer would meet — row anchors vs
`spans.tsv` starts differing by exactly 80 — is the builder's `start = off − CONTEXT` rule (clamped for
span 1), and the canonical `--check` passes. The row survives a non-author re-open.

VERDICT: ATTACKED Registry row S114 (capture re-open, every cell, anchors, used-by, citing-entry entailment) — no defect; row holds as authored.
