# R84ExecReopen — C2 K2 (located) fire-or-hold

Godspeed axes: locate (K2 capture/re-open evidence), size (word count), cost (3 GETs only).

Revision under test: `03bbb4580b39b442be69f998fae2db48d64b8c93` (scored landing; extracted via `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 03bbb4580b39b442be69f998fae2db48d64b8c93 | tar -x -C /fast/scratch/hyaku/chousa-r84/R84ExecReopen/tree`, exit 0; toplevel asserted `/home/vgpnk/Projects/shokunin/chousa-shokunin`).

Entry: `corpus/knowledge/search-transparency-reporting-r84.md` at landing rev (12 quotes, ## Located quotes).

## (1) Committed-capture check (whitespace collapsed, curly quotes folded to ASCII)

Captures (key = sha256(url)[:24], verified):
- S214 `a640b15abf781e5c583d7088.txt` (txt_sha256 4cbf8881…)
- S018 `248b43277f376e437a356909.txt` (0640edfc…)
- S023 `f5545a194c06ab421875b047.txt` (20dc0c3a…)

| qid | source | result | capture line |
|---|---|---|---|
| Q1 | S214 | FOUND | 17 |
| Q2 | S214 | FOUND | 18 |
| Q3 | S214 | FOUND | 19 |
| Q4 | S214 | FOUND | 20 |
| Q5 | S214 | FOUND | 54 |
| Q6 | S018 | FOUND | 76 (also 120, 198) |
| Q7 | S018 | FOUND | 76 (also 120, 198) |
| Q8 | S018 | FOUND | 76 (also 120, 198) |
| Q9 | S023 | FOUND | 10318 (also 13363) |
| Q10 | S023 | FOUND | 3256 (also 4164, 4720) |
| Q11 | S023 | FOUND | 11517 |
| Q12 | S023 | FOUND | 3246 |

Command: Python eval — read each capture, `html.unescape`, fold curly quotes (`"` `'`) to ASCII, `re.sub(r"\s+"," ",s)`, substring match per line then full-text spanning. Exit 0. Receipt: `.ufo/waves/round-84/w1/R84ExecReopen/capture-check.json`.
Shell cross-check: `grep -n "Specify all databases" …/a640b15abf781e5c583d7088.txt` → line 17, exit 0.

## (2) Re-open check — exactly three GETs (URLs with 2026-11-08T02:1x–02:2xZ refetch rows)

Commands (one GET per URL, into scratch; HTML bodies NOT copied to wave folder — receipts only):

```
curl -fsSL --compressed --max-time 20 -A 'Mozilla/5.0 (chousa r84 reopen)' https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf -o /fast/scratch/hyaku/chousa-r84/R84ExecReopen/S214.html
curl -fsSL --compressed --max-time 20 -A 'Mozilla/5.0 (chousa r84 reopen)' https://aclanthology.org/2026.acl-long.1430/ -o /fast/scratch/hyaku/chousa-r84/R84ExecReopen/S018.html
curl -fsSL --compressed --max-time 20 -A 'Mozilla/5.0 (chousa r84 reopen)' https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ -o /fast/scratch/hyaku/chousa-r84/R84ExecReopen/S023.html
```

Observed (curl `-w 'http=%{http_code} bytes=%{size_download}'`, exit 0 each):
- S214: HTTP 200, 67506 bytes, effective URL redirects to squarespace PDF (`PRISMA_2020_checklist.pdf`); file type PDF 1.7, 2 pages. Raw sha256 `2eedbd5452741f9615307a0bce21a8198c0597ce2a0a8a0fd7e140d64b08c625` — byte-identical to refetch row raw_sha256.
- S018: HTTP 200, 42629 bytes. Raw sha256 `2a812275e1a7fab8e7e91116965ad9a7397726e283e1cb0cdd45ec18d21a3322` — byte-identical to refetch row raw_sha256.
- S023: HTTP 200, 35432 download bytes (682788 bytes on disk after decompression). Raw sha256 `fb32e12fa9bee1379acc0cf921ba7e79a6b85bd46253d993db0898847b9870a1` — byte-identical to refetch row raw_sha256.

Processing: S214 PDF via `pdftotext -layout`; S018/S023 HTML tag-stripped (script/style dropped), `html.unescape`, whitespace collapsed, curly quotes folded. Receipt: `.ufo/waves/round-84/w1/R84ExecReopen/reopen-check.json`.

Re-open results — all FOUND, zero ABSENT:
- S214: Q1 FOUND, Q2 FOUND, Q3 FOUND, Q4 FOUND, Q5 FOUND (all in 9208-char extracted text)
- S018: Q6 FOUND, Q7 FOUND, Q8 FOUND (all in 13988-char stripped text)
- S023: Q9 FOUND, Q10 FOUND, Q11 FOUND, Q12 FOUND (all in 238043-char stripped text)

No quote is ABSENT on a 200 page → K2 does not fire on the re-open leg. No unreachable pages.

## (3) Word counts (`wc -w` and Python `split()` — identical)

| qid | words | in 8..25 |
|---|---|---|
| Q1 | 17 | yes |
| Q2 | 9 | yes |
| Q3 | 17 | yes |
| Q4 | 16 | yes |
| Q5 | 15 | yes |
| Q6 | 13 | yes |
| Q7 | 15 | yes |
| Q8 | 18 | yes |
| Q9 | 10 | yes |
| Q10 | 24 | yes |
| Q11 | 9 | yes |
| Q12 | 9 | yes |

Commands: `for i in 1..12; do wc -w < q$i.txt; done` (exit 0) and Python `len(q.split())` (exit 0). Receipt: `.ufo/waves/round-84/w1/R84ExecReopen/wordcounts.txt`. No quote outside 8..25.

## Verdict

K2 (located): all 12 quotes occur in their committed captures AND on the live re-opened pages (HTTP 200 ×3, raw hashes byte-identical to refetch rows). No ABSENT quote fires the kill rule; word counts all within 8..25.

VERDICT: R84ExecReopen C2 held — all 12 quotes FOUND in captures and on 200 re-opens, none triggers K2.
