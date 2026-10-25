# Round 48 hand-check — chousa absent-defect row ordinal 5

## Scope and selection

Read the local campaign register at `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (Rows, lines 37–42). Restricting to `chousa`, the five rows in source order are S077 (round1), S080 (round1), S082 (round1), S084 (round1), **S086 (round1)**. The selected row is S086, cited URL `https://www.ncpssd.cn/`, with two quotes. This selection follows source rows as ordered in the register, not lexical sorting of the IDs or the later row remap.

Identity caution: chousa `ID-REMAP.md` lines 5–22 says staged round1 original S086 became lane S089; it is round-scoped. This check retains register identity `round1/S086`, and treats S089 only as the lane's mapped row—not a substitute identity.

## Hand-check result

- Quote 1 — `我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务`: **PRESENT** in the local campaign capture. Anchor: campaign `.qcache/c4e1446a42d0a709c34097be.txt:318`, FAQ item 7 (`如何下载电子全文？`), where the quoted sentence begins verbatim. The captured HTML is likewise in `.qcache/c4e1446a42d0a709c34097be.raw:318`.
- Quote 2 — `我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`: **PRESENT** in the same local capture. Anchor: `.qcache/c4e1446a42d0a709c34097be.txt:318`, FAQ item 4 (`谁有权限使用网站上的资源？`), verbatim.

These establish presence for both quoted spans in a local captured copy of the cited FAQ page. The campaign's S086 row labels both spans `ABSENT`; that candidate verdict is falsified by this captured payload. No live fetch was made. This does not establish whether the page remains unchanged now.

## Corroboration and limits

The lane's `chousa/CHANNELS.md:35` records the NSSD FAQ anchor as items 3, 4 and 7 and notes that the FAQ body requires the `mainTitle` query parameter. `SOURCES-PROPOSED.md:44` places that source under mapped S091; this is not the selected row. These lane notes corroborate the relevant item numbering, but the verbatim verdict above rests on the local campaign cache, not those summaries.

`quote-lint-full-v5.json` records round1/chousa/S086 twice as `ABSENT`, each with `binding: id` and `url: https://www.ncpssd.cn/`; the register reproduces those candidates. The available local campaign captures show the cited text in the FAQ capture. The homepage-oriented cache `.qcache/76914d78c20094f677dea77d.txt` does not contain the FAQ body; its absence there is not contrary evidence because it is a different page. No source-level distinction or version mismatch was inferred beyond these observed records.

## Verdict

**Present (both quotes); register candidate is contradicted by available campaign capture.** Evidence: local captured FAQ `.qcache/c4e1446a42d0a709c34097be.txt:318`; exact anchors are FAQ items 4 and 7. This is not a live-current-source adjudication.

## Commands / observed output

- `find /home/vgpnk/Projects -name '*absent-defect*'` located the campaign register under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/`.
- Read register lines 37–42: five chousa source rows begin S077, S080, S082, S084, S086; S086 contains the two quoted spans.
- `python3` inspection of `quote-lint-full-v5.json`: emitted two `ABSENT` findings for lane chousa, round1, S086, both `binding: id`.
- `grep -rl` across local `.qcache`: found both target phrases in `.qcache/c4e1446a42d0a709c34097be.raw` and `.txt`; reading `.txt:318` showed FAQ items 4 and 7 with both exact sentences.
- No install, network request, or adoption edit.
