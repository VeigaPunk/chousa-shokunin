# GroundS101 — W1 re-ground of staged row S100/lane S101 (zcmu CNKI .doc capture)

Seat: GroundS101, leaf — no subagents, no background jobs.
Tooling: nothing installed/updated (no tool needed; RULES.md read, no install record required).
Scratch: none created (no /tmp/chousa-r49-GroundS101); nothing to delete.

## Files opened (evidence pointers)
- /home/vgpnk/.omp/agent/RULES.md:1-14 — tooling directive; no install performed.
- staged entry .../merge/chousa/knowledge/corpus/knowledge/citation-count-semantics-r37.md:4,14-18 — source line S100 (URL below, "document read 2026-10-23"); Observation bullet 1 carries the two quotes.
- capture `.raw` b539a80218080da56a75b624.raw — 801,280 bytes; `file`: "Composite Document File V2 Document, Little Endian, Os: Windows, Version 6.1, Code page: 936, Author: Administrator, Template: Normal.dotm ... Number of Pages: 5, Number of Words: 132, Number of Characters: 757".
- capture `.txt` b539a80218080da56a75b624.txt — 1,406,840 bytes; `read` rejects it ("Cannot read binary ... not valid UTF-8"); python `decode('utf-8', errors='replace')` yields 308,430 U+FFFD replacement chars → lossy sidecar confirmed.
- absent-defect-register.md:45 — register row S095 (`chousa`/round2) three quotes.
- round-48.md:50 — round-48 Gate verdict for register S095: `absent-as-written`, pointer QuarantineS095.md ("one quote is present, two are punctuation/word-form misquotes in the OLE document; the .txt sidecar was a lossy binary decode").

## Decode command (exact, observed output)
python3 (eval cell):
```
raw = open(raw_path,'rb').read(); raw_dec = raw.decode('utf-16le', errors='replace')
txt = open(txt_path,'rb').read().decode('utf-8', errors='replace')
print(len(raw), len(raw_dec), len(txt))      # 801280 400543 762306
print(txt.count('\ufffd'))                    # 308430
```
Exact-match scan results on `raw_dec` (count / first offset / length):
| string | count | first | len |
|---|---|---|---|
| 中国知网他引频次查询方法说明 | 1 | 1280 | 14 |
| 中国知网他引频次的查询需要使用《中国引文数据库》 | 1 | 1296 | 24 |
| same + 。 | 1 | 1296 | 25 |
| 关于自引的说明 | 1 | 1423 | 7 |
| 关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引 | 1 | 1423 | 47 |
| same + 。 | 1 | 1423 | 48 |
| 他引频次具体查询方法如下 | 1 | 1473 | 12 |
| 成功登录《中国引文数据库》后，可按“题名”、“作者”、“单位”等方式查询需要检索的文献 | 1 | 1587 | 43 |
Whitespace-tolerant regex (any `\s*` between chars) for the two register misses: None. `.txt` sidecar exact scan: all three register quotes find() == -1.

## Gate block draft (lane row S101 = staged S100)
- URL: https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc
- Access date: 2026-10-25 (capture mtime 2026-10-23 20:36).
- G1: 「中国知网他引频次的查询需要使用《中国引文数据库》。」 — 25 chars, 0 whitespace words; EXACTLY ONCE in .raw UTF-16LE decode @ char 1296.
- G2: 「关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引。」 — 48 chars, 0 whitespace words; EXACTLY ONCE @ char 1423.
- Form: both located in `.raw` decoded UTF-16LE (`errors='replace'`); `.txt` is the lossy sidecar and contains none.

## Anchor cell draft
| section | char offset |
|---|---|
| 中国知网他引频次查询方法说明 (title) | 1280 |
| 中国知网他引频次的查询需要使用《中国引文数据库》。 | 1296 |
| 关于自引的说明 | 1423 |
| 他引频次具体查询方法如下 | 1473 |
| 成功登录《中国引文数据库》后，可按“题名”、“作者”、“单位”等方式查询需要检索的文献 | 1587 |

## Claim-by-claim support (claims resting on this row only)
1. CNKI 他引频次 query note — 他引频次 needs 中国引文数据库: **supported** (substance) — capture reads 「中国知网他引频次的查询需要使用《中国引文数据库》。」 @1296. The entry/register inline string without 《》 is count=0, so the entry's quoted form is a punctuation-truncated rendering (missing book-title marks and trailing 。); byte-exact capture text is G1.
2. Self-citation rule 关于自引的说明 「对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引」: **supported verbatim** — G2 @1423, exactly once (heading + body contiguous).
3. Entry title attribution "The CNKI document titled 中国知网他引频次查询方法说明": **supported** — title @1280.
Claims resting on S101/S102/S103 (hit.edu.cn; tego-shoten PDF; um.edu.mo PDF) untouched here.

## Register row S095 re-check (chousa slice; campaign id — distinct from lane own-work S095)
- Quote 1 「中国知网他引频次的查询需要使用中国引文数据库」: count=0 in raw-dec → **absent-as-written** (capture carries 《》+。; substance present).
- Quote 2 「关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引」: count=1 @1423 → **present** verbatim.
- Quote 3 「成功登录中国引文数据库后，可按题名作者单位等方式查询需要检索的文献」: count=0 → **absent-as-written** (capture reads 成功登录《中国引文数据库》后，可按“题名”、“作者”、“单位”等方式查询需要检索的文献 @1587: 《》 plus “”-quoting and 、 separators; substance present).
My verdict: **absent-as-written** (quote-precision failure on 2/3; 1/3 verbatim; all three substances present — not fabricated; nothing unreachable). Confirms round-48's recorded verdict (round-48.md:50). No `unreachable` involved.

No production file, sibling report, git/jj state, or fleet repo touched — only write: this report.

VERDICT: Re-grounded staged S100→lane S101 (zcmu CNKI .doc) via .raw UTF-16LE decode — Gate quotes G1 @1296 and G2 @1423 exact-once; self-citation rule supported verbatim, 他引频次/中国引文数据库 note supported in substance (register string misses 《}); register row S095 re-confirmed absent-as-written (2/3 quotes punctuation-form misquotes, not fabrication).
