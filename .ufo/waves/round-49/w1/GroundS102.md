# GroundS102 — round 49 wave 1 — re-ground staged row S101 (lane S102)

Seat: chousa lane, leaf member (no subagents, no network, no live fetch). Only write: this report. Scratch `/tmp/chousa-r49-GroundS102/` deleted after.

## Capture identification
- URL: `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`
- qcache prefix `sha256(url)[:24]` = `6dc68fd6b32ce9c8dfcebce8` → `.raw` (129024 B; sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`) and `.txt` (157816 B).
- `head -c 64 <capture>.raw | xxd` → `d0cf 11e0 a1b1 1ae1` = OLE compound (.doc). `head -c 64 <capture>.txt | xxd` → runs of `efbfbd` (UTF-8 U+FFFD); whole-file UTF-8 decode yields 14486 replacement chars → the `.txt` sidecar is a lossy decode and unusable.
- Form used: `.raw` whole-file UTF-16LE decode → 64512 chars, 263 replacement chars (only trailing OLE directory garbage). `python3 -c "open('/tmp/…/decoded.txt','w').write(open(path,'rb').read().decode('utf-16-le'))"`.
- Document title (decoded): `中国学术期刊(光盘版)检索与评价数据规范\x0b（修订本）` @1295; §11 `11中图分类号(CLC number)与文献标志码(Document code)` @10902; §14 `14 参考文献(References)` @11924.

## Gate block draft (lane S102)
- URL: as above; access date: 2026-10-25; form: `.raw` decoded UTF-16LE.
- Quotes (each `count==1` in this form; offsets are `text.find()` character offsets; copied byte-exact):

| # | quote | offset | chars | ws words |
|---|---|---|---|---|---|
| Q1 | `为便于文献的统计和期刊评价，确定文献的检索范围，提高检索结果的适用性，每一篇文章或资料应根据其内容性质标识一个文献标志码。` | 11170 | 61 | 1 |
| Q2 | `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。` | 11993 | 55 | 3 |
| Q3 | `c. 文献类型及载体类型标志；\x0bd. 其他责任者(译者、校注、校点、校勘者等)；\x0be. 版本(初版省略)；\x0bf. 出版项(出版地、出版者、出版年)；\x0bg. 文献出处或电子文献的可获得地址；\x0bh. 文献起止页码；\x0bi. 文献标准编号(ISBN,ISSN,…)。` | 12158 | 129 | 14 |

- `anchor` cell draft: `11．6 char 11170 · 14．1 char 11993 · 14．2 char 12049 · 14．3 char 12288 · 1．2．1 char 1610 · 15．7 char 34374` (section names + quote offsets).

## Staged-entry (r37) claims resting on this row vs capture
1. Source line "sections 11 and 14" — **supported** (§11 @10902, §14 @11924).
2. "nine prescribed reference elements including 文献类型及载体类型标志 and 文献出处或电子文献的可获得地址" — **supported**: §14.2 著录项目 list @12049 contains exactly items a–i (nine, in order; `re.findall(r'([a-i])\.\s', …)` = a,b,c,d,e,f,g,h,i); item c = `文献类型及载体类型标志` verbatim (Q3), item g = `文献出处或电子文献的可获得地址` verbatim (Q3). (Note §1.1 item c spells the variant `文献类型及载体类型标识` @1464; the entry's exact phrase matches §14.2.)
3. "classifies each article by a 文献标志码 (A–E) whose stated purpose is …为便于文献的统计和期刊评价…确定文献的检索范围，提高检索结果的适用性" — **supported**: Q1 @11170 (purpose sentence, verbatim), five codes `A——基础性理论与应用研究 … E——文件、资料…` @11208–11365.
4. "reference format itself is deferred to GB/T 7714" — **supported with nuance**: §14.1 (Q2 @11993) says 本规范推荐采用 (recommends) GB/T 7714's 顺序编码制/作者-出版年制 formats — instruction, not "deferred" wholesale. Separately §15.7 @34374 (serial-parameter letter codes) reads `参考文献格式，参照ISO 690，采用1位字母：n——顺序编码制（Numeric references method）；d——作者-出版年制（First element and date method）。` — the entry's GB/T claim is correct for the reference-format section.
5. Inference bullet (nine elements, document-type code, carrier code, resolvable address; A–E selection as declared counting/evaluation decision) — **supported**: same quotes plus §14.3.1 letter codes @12292 (`M C N J D R S P G K`, `Z`, 双字母 `DB CP EB`), §14.3.4 carrier codes @12596 (`磁带(magnetic tape)——MT，磁盘(disk)——DK，光盘(CD-ROM)——CD，联机网络(online)——OL`, `[文献类型标志/载体类型标志]`), and §15.6 @34334 `文章总篇数，为发表在本期中具有文献标志码的文章的总和,据此计算载文量。` (counting driven by 文献标志码-bearing articles).

## Register row S096 re-check (chousa round-2 slice, same URL)
Re-checked the register row's three quotes myself against the capture:
- q1 `主要责任者…文献题名；文献类型及载体类型标志；其他责任者…版本（初版省略）；出版项（出版地出版者出版年）；文献出处或电子文献的可获得地址；文献起止页码；文献标准编号(ISBN，ISSN，……)` — **0 occurrences**. absent-as-written: splices §14.2 wording (`文献类型及载体类型标志`, halfwidth parens) with §1.1 punctuation (fullwidth parens, `ISBN，ISSN，……`), drops the `、` separators in `出版地出版者出版年`.
- q2 `根据GB3469规定，以单字母方式标识以下各种参考文献类型` — **present, exact** @1616 (§1.2.1; §14.3.1 instead reads `根据 GB 3469规定` with a space).
- q3 `参考文献格式，参照 GB/T 7714，采用…顺序编码制；作者-出版年制` — **0 occurrences**. absent-as-written: takes §15.7's frame (`参考文献格式，参照…采用…顺序编码制；作者-出版年制`) and substitutes `GB/T 7714` for the capture's `ISO 690`; `参照 GB/T 7714` occurs nowhere verbatim.
- Own verdict: **absent-as-written** (q2 present; q1/q3 absent as written due to punctuation/splice/standard-swap; content genuine — not fabricated). Verdict matches round-48 Gate table. `unverifiable` not applicable: capture is present on disk.

## Notes
- No tool installed or updated (RULES.md read; none needed). No git/jj/fleet writes; no campaign tools run.
- Commands with observed outputs: `head -c 64 … | xxd` (magic/replacement runs), Python `decode('utf-16-le')`, `str.find`/`str.count` for every quote (counts: Q1/Q2/Q3 = 1; register q1/q3 = 0; q2 = 1).

VERDICT: Re-grounded staged row S101 (lane S102) against its on-disk OLE capture — Gate block drafted with three exactly-once quotes (offsets 11170/11993/12158); all r37 entry claims resting on this row adjudicated supported (GB/T-deferral nuance noted); register S096 re-checked: q2 present, q1/q3 absent-as-written — own verdict absent-as-written, consistent with round 48.
