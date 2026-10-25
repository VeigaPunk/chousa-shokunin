# Quarantine hand-check — chousa register row S086

Row: `absent-defect-register.md:41` — `chousa | round1 | S086 | payload-absent | https://www.ncpssd.cn/`, two quoted spans; register note: "cited source, companion URLs and local artifacts were all checked; the quote is in none of them".
Slice: `assimilation/quarantine-slice` line 5: `S086  payload-absent`.

## Verdict: present — the `payload-absent` candidate is falsified by local byte evidence

Both quoted spans occur verbatim in the campaign's own capture of the row's
companion URL, the NSSD FAQ page named in the lane gate block
(`SOURCES-PROPOSED.md:119`, `URL: https://www.ncpssd.cn/ (help page:
https://ncpssd.org/service/help?mainTitle=%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)`).
They are absent only from the cited homepage capture — a different page.
"Present" here means present in local captured copies; no live fetch was made
(L0 `8d77e6c1` open), so nothing is claimed about the page's current state.

## Capture evidence (local, byte-exact)

- Help page capture — key `c4e1446a42d0a709c34097be` =
  sha256("https://ncpssd.org/service/help?mainTitle=%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98")[:24].
  `.qcache/c4e1446a42d0a709c34097be.raw` and `.txt` are byte-identical:
  45,308 bytes, sha256 `f5f72a942233a45daa1dc68305448df276b744584a2352e72c19a1fb6c2e099c`
  — matches the gate's "help page fetched, HTTP 200, 45,308 bytes".
  - Q1 `我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务`
    at byte offset 27523, inside FAQ item 7 `如何下载电子全文？` (line 318).
  - Q2 `我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`
    at byte offset 26676, inside FAQ item 4 `谁有权限使用网站上的资源？` (line 318).
- Cited homepage capture — key `76914d78c20094f677dea77d` =
  sha256("https://www.ncpssd.cn/")[:24]. `.raw` 197,752 bytes sha256
  `60c746513b7f13ea78e0d94f18a6a0a079674e2b84b795bb262d0f0683db0f93`,
  `.txt` 15,270 bytes sha256 `7a4ef1386800f55a520f003d16260e4237d2464dbfb3c274380714717269b2dd`
  — matches gate "homepage fetched, HTTP 200, 197,752 bytes". Neither quote occurs
  (grep -F: 0 hits); expected — the homepage does not serve the FAQ body.
- Qcache sweep: `grep -lF Q1` and `grep -lF Q2` over all of `.qcache/` return
  only `c4e1446a42d0a709c34097be.{raw,txt}` — the payload exists in exactly one
  capture, the companion help page.
- Lane-local artifacts: `kotodama/round11/.scratch/ncpssd_home.html`
  (197,752 B, sha256 `60c7…0f93`) is byte-identical to the homepage capture —
  no quotes. `kotodama/round6/.scratch/ncpssd.html` (143,829 B, sha256
  `8ecce8c1177c930ea1a757cb92297b7f0909cdfb12177085d473bb8c85574a32`) — no quotes.
- Register/lint rows: `quote-lint-full-v5.json` binds both ABSENT verdicts to
  lane `chousa`, `round1`, id `S086`, `binding: "id"`, url `https://www.ncpssd.cn/`
  (entries ~lines 1026/1038); `census-adjudication.json:469,481` repeats them.

## Why the census said ABSENT anyway

The row's cited URL is the homepage; the quotes live on the companion help URL
the gate block itself names. The campaign's own cache already held that page
(`.qcache/c4e1446a…`), so "companion URLs … were all checked; the quote is in
none of them" is contradicted by the campaign's own bytes: the companion
capture existed and was not matched. Identity note: the lint binds by row id,
not URL — under the current `SOURCES-PROPOSED.md` this content sits at S091
while S086 is the openstd row (chousa `ID-REMAP.md` is round-scoped: staged
round1 S086 → lane S089, staged S088 → S091). The verdict above is keyed to
the row's cited URL and quotes, as instructed.

## Commands run (all read-only, local)

- `grep -n "S086" absent-defect-register.md` → row at line 41.
- `python3`: sha256(url)[:24] → `76914d78…` (homepage), `c4e1446a…` (help page).
- `grep -o -b -F "$Q" .qcache/<key>.{txt,raw}` → Q1@27523, Q2@26676 in
  `c4e1446a…`; zero hits in `76914d78…`.
- `grep -l -F "$Q" .qcache/*` → only `c4e1446a42d0a709c34097be.{raw,txt}`.
- `sha256sum` on both captures and both kotodama scratch files (digests above).
- `awk 'NR==318' c4e1446a….txt` → numbered FAQ items 1,2,4,5,7 in one HTML
  blob; context slices at both offsets show items 4 and 7 wrapping the quotes.
- Frozen claim read at `4bbd234` (`corpus/evidence/round48/claims.md`); R48-C1
  counters (`c1-count.py`, `mutation-check.py`) are plumbing fixtures, not
  touched here.

## Bearing on the round-48 milestone

This row is a verified false positive in the register's fabrication class: the
quotes are findable in the campaign cache the census claimed to have checked.
That weakens any precision/precision-floor story built on `payload-absent`
meaning "quote is in none of them" — for S086 the defect is the checker's
companion-URL coverage/binding, not the lane's quote. Residual risk: presence
is established against 2026-10-23 captures only; whether the live FAQ still
serves this text is out of scope (no fetch, per L0). One w1 member
(Attack26) reached the same verdict on the same capture; this check
re-derived it independently with digests and a full-qcache sweep.
