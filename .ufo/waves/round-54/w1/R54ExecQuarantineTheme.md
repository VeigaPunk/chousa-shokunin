# R54ExecQuarantineTheme — hand-check of the three quarantine rows on theme URLs

Seat: leaf executor (no subagent dispatched). Read-only: register, qcache captures and lane are read; only this file written. No network; every reading is from on-disk capture bytes. Offsets are `text.find` on `pathlib.Path(...).read_text(encoding="utf-8", errors="replace")`, the convention `c2-count.py` / `build-spans.py` use — that folds CRLF, so the SAMR sidecar is 3,591 chars there and 4,468 newline-preserving; the lesson's offsets (1029/1048) and mine agree under the lane convention only.

```
$ grep -n '`chousa`' …/absent-defect-register.md | grep -E 'S080|S088|S096'
38:| `chousa` | round1 | S080 | `payload-absent` | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507…
42:| `chousa` | round2 | S088 | `payload-absent` | https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9…
46:| `chousa` | round2 | S096 | `payload-absent` | https://jc.hit.edu.cn/_upload/article/files/f7/54/7119…
```
Replaying the brief's filter with `c2-count.py`'s own `url_of`/`DOCS`/`ALIASES` logic gives
`{'S080': …std.samr…, 'S088': …xuebaobangong…, 'S096': …jc.hit…}` — exactly three, no fourth.

## Verdict lines (for the lesson; re-derived this round, not copied)

register `S080` (round1) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — verdict: absent-as-written — the joined line `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` count=0 (also 0 whitespace-free, 0 NFKC-folded) while its parts are present, each on its own line: `标准号` 1@1327 (line 366), `发布日期` 1@1354 (line 370), `实施日期` 1@1382 (line 376), `发布 于 2025-12-02` 1@1029, `实施 于 2026-07-01` 1@1048, values `GB/T 7714-2025` 2@1239, `2025-12-02` 2@1034, `2026-07-01` 2@1053; `标准号：`/`发布日期：`/`实施日期：` count=0 in `.txt` and `.raw`; the page renders `<dt …name>标准号</dt><dd …value>GB/T 7714-2025</dd>`

register `S088` (round2) — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — verdict: absent-as-written — the slash-joined carrier list count=0 exact and 0 whitespace-free (the sidecar holds no ASCII `/` at all: count 0); its five rows are separate lines of 表Ａ．２ (caption 1@58955), each label exactly once — `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）`@59025, `磁盘（ｄｉｓｋ）`@59073, `光盘（ＣＤ－ＲＯＭ）`@59116, `联机网络（ｏｎｌｉｎｅ）`@59161, `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）`@59201 — codes in a second column (ＭＴ@59063, ＤＫ@59108, ＣＤ@59119); whitespace-free the five label+code pairs are contiguous, count 1 at 34,917

register `S096` (round2) — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — verdict: absent-as-written — in the defined OLE text form (27,012 chars, 0 U+FFFD) q2 `根据GB3469规定，以单字母方式标识以下各种参考文献类型` is verbatim once @336 (one line) and once @337 in the LibreOffice export, while q1 (96 chars) and q3 (36 chars) count=0 in all four forms; the document's own list has `出版项（出版地、出版者、出版年）`@223 (register drops both 、) and its 15.7 line has `参考文献格式，参照ISO 690`@25,123 (register substitutes GB/T 7714, which sits elsewhere at 12,800)

## Row S080 — SAMR record (`adf6ba934e813b2c326fa150`)

```
.txt  6,626 B  sha256 4e46154f4a841d17…  3,591 chars (.raw 76,252 B  sha256 a7b868be292a4c00…, HTML)
L366 ' 标准号 '   L367 ' GB/T 7714-2025 '   L370 ' 发布日期 '   L371 ' 2025-12-02 '
L376 ' 实施日期 ' L378 ' 2026-07-01'        fullwidth '：' in .txt: 6, first inside 采标情况
raw DOM: <dt class="basicInfo-item name">标准号</dt><dd class="basicInfo-item value">GB/T 7714-2025</dd>
```
Companion check (the register's reason cell says companions were checked too): the openstd record for the same standard — `b9ca2a4fdf9455867534f144` (`http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14`, theme document S122) — carries `标准号：GB/T 7714-2025` once @13,300, but its dates are colon-less divs (`发布日期`@16,016 / `2025-12-02`@16,105; `实施日期`@16,219 / `2026-07-01`@16,321). Across all 2,549 `.txt` sidecars in the qcache the joined string is in 0 files, `发布日期：2025-12-02` in 0, `实施日期：2026-07-01` in 0. Material present, rendering synthesized → absent-as-written (not fabricated, not unverifiable).

## Row S088 — JMU PDF (`0f33243fd7ac2fe88b85c1ba`)

```
.pdf 6,209,520 B sha256 cb3ffbf5013e7a3a… (identical to .raw)
.txt   190,614 B sha256 13a34aa9bb107eef…  83,061 chars
$ pdftotext -layout -enc UTF-8 <raw> out.txt  → sha256 13a34aa9bb107eef… (byte-identical)
L1375 '    电子资源的载体类型                          载体类型标识代码'
L1376 '    磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）                     ＭＴ'
L1380 '缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）                 ＭＭ'
```
Whole quote count=0; with whitespace removed the five label+code pairs *are* contiguous once
(offset 34,917), so the ` / ` join is the only synthesized part — and it cannot occur, since the
sidecar's ASCII `/` count is 0 (fullwidth `／` is present 887×, but that is a different byte
sequence). Longest verbatim run with the register string: 25 chars. UTF-8 byte search for the
joined string in `.pdf`/`.raw`: 0. → absent-as-written.

## Row S096 — HIT data specification (`6dc68fd6b32ce9c8dfcebce8`)

The `.txt` sidecar is a lossy binary re-decode, so nothing is decidable from it: 157,816 B /
128,416 chars with **14,486 U+FFFD**, 14 CJK chars, 0 hits for `主要责任者`. `.raw` is OLE CFB
(`d0cf11e0a1b11ae1`, 129,024 B, sha256 `6063a3aff7a4081e…`). Both required renderings, this round:

```
$ TMPDIR=$S python3 tools/capture-text.py <raw> > hit-def.txt    # exit 0, 47,356 B
  27,012 chars, 0 U+FFFD, sha256 a8e3e7ad213b6ec5…  (byte-identical to corpus/evidence/round54/S101-text-form.txt)
$ soffice -env:UserInstallation=file://$S/prof --headless --convert-to 'txt:Text (encoded):UTF8' <hit.doc>
  hit.txt 27,009 chars, 0 U+FFFD, sha256 340216d56a2302b2…
$ python3 tools/capture-text.py --locate '根据GB3469规定，…参考文献类型' <raw>
LOCATED count=1 offset=336
Q1 (96) def=0 LO=0 sidecar=0 raw-utf16le=0 | parts: 主要责任者 17@56, 文献题名 18@147,
   文献类型及载体类型标志 1@12963 (1.1 item c reads …类型标识@162), 其他责任者 5@184,
   版本（初版省略） 1@203, 出版项（出版地出版者出版年） 0 (doc: …（出版地、出版者、出版年）@223),
   文献出处或电子文献的可获得地址 2@250, 文献起止页码 4@276, 文献标准编号(ISBN，ISSN，……) 1@293
Q2 (29) def=1@336 LO=1@337 sidecar=0 raw-utf16le=1@byte 3232
Q3 (36) def=0 LO=0 sidecar=0 raw-utf16le=0 | doc 15.7 @25,119: '15.7参考文献格式，参照ISO 690，采用1位字母：
   n——顺序编码制（Numeric references method）；d——作者-出版年制（First element and date method）。'
```
Q2 is verbatim once on one line; Q1 and Q3 are splices (the `…` markers replace the `a.`–`i.`
enumerators and the doc's separators; Q3 also swaps ISO 690 → GB/T 7714). Material present →
absent-as-written, which supersedes round 42's `unverifiable` (that rested on never rendering it).

## Earlier lesson that already gave each row a verdict

```
S080  corpus/evidence/round42/quarantine-verdicts.tsv:3  -> absent             (round-42.md §Adjudication)
      corpus/lessons/round-48.md:43                     -> absent-as-written  (.ufo/waves/round-48/w2/QuarantineS080.md)
S088  corpus/evidence/round42/quarantine-verdicts.tsv:7  -> absent
      corpus/lessons/round-48.md:47                     -> absent-as-written  (.ufo/waves/round-48/w2/QuarantineS088.md)
S096  corpus/evidence/round42/quarantine-verdicts.tsv:11 -> unverifiable       (round-42.md:73, with the unrendered binaries)
      corpus/lessons/round-48.md:51                     -> absent-as-written  (.ufo/waves/round-48/w2/QuarantineS096.md)
      corpus/lessons/round-48-verifier-spotcheck.md:63  -> agree (q2 at byte 3232; q1/q3 absent under every fold)
      corpus/lessons/round-49.md:124                    -> absent-as-written  (re-check, "q2 is verbatim")
```
Round 43's `not-carried S080 … S088` (`round-43-verifier-spotcheck.md:60`) is the absent-split
tool's class, not a verdict; round-44/46/49 `S080`/`S088` hits are lane-id-space rows.

## Precision notes (reported, not patched — neither the register nor the lesson is mine)

1. `round-48.md:43` calls S080's fields "three **Japanese** data values"; S080 is the Chinese SAMR
   record (标准号/发布日期/实施日期). Pointer file `QuarantineS080.md` is correct; verdict unaffected.
2. The round-54 lesson's S096 line lists only the absent pieces — it should record that q2 is
   verbatim once @336, else the row reads as if nothing matched.
3. S088's lesson/round-48 wording "not in any extraction" misses that whitespace-free the five
   pairs are contiguous @34,917; only the ` / ` join is synthesized.
4. `标准号：GB/T 7714-2025` does occur once @13,300 — on the openstd companion (S122), a different
   document. It must not be quoted as S121 text.

## Risk / blocker

- `tools/capture-text.py` in the worktree is **not** the candidate blob: `git diff 8a7d0f1 --
  tools/capture-text.py` shows one uncommitted hunk (Prc `cb_grpprl` bounds check); worktree
  sha256 `e7e381b675353e85…` vs committed `fd0ed3f58565b781…`. On the HIT `.raw` both emit a
  byte-identical defined form (`cmp` clean), so the evidence holds either way — but C1 names
  8a7d0f1, so the L1 should confirm which blob the counter hashes.
- Read-only counter observation (not my verdict): `c2-count.py --lane-only` and full
  `c2-count.py` both exit 0 on the current tree — `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`,
  `QUARANTINE_BLOCKED_ADOPTED=0`, `CAPTURE_BOUND=33/33`, `C2=PASS` — consuming the lesson's
  pre-existing verdict lines, which are identical to mine.

## Housekeeping

No installs or upgrades (pacman paused host-wide; nothing needed): `pdftotext 26.08.0`, `LibreOffice 26.8.1.1`, `qpdf 12.4.2`, `Python 3.14.8` were already present. LibreOffice used a private `-env:UserInstallation=file://$S/prof`; `pgrep -u $USER -f "UserInstallation=file://$S"` returned nothing (exit 1) afterwards and no `soffice.bin` remained. Scratch `/fast/scratch/hyaku/chousa-r54/R54ExecQuarantineTheme` removed at the end.

VERDICT: attacked the three theme-URL quarantine rows from capture bytes — S080 absent-as-written (joined colon line 0×, labels 1@1327/1354/1382), S088 absent-as-written (slash-joined 0×, five 表Ａ．２ cells 1× each at 59025/59073/59116/59161/59201), S096 absent-as-written in the defined OLE form (q2 verbatim 1@336, q1/q3 spliced, `.txt` sidecar 14,486 U+FFFD unusable); all three agree with the lesson's existing lines, none is fabricated or unverifiable, so C2's kill rule on this slice is not tripped.
