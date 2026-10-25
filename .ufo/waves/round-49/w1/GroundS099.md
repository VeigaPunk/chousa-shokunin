# GroundS099 — round 49 w1, row S091/S099 re-grounding (NCPSSD homepage)

Seat: GroundS099 (chousa, leaf — no subagents, no background jobs). No network; on-disk captures only.
No tool install was performed (RULES.md read; pacman transactions paused host-wide; none needed).

## Capture used (binding URL = homepage)

- `.../.qcache/76914d78c20094f677dea77d.txt` — Unicode text, UTF-8 (with CRLF/LF), 15,270 bytes
  → 7,943 chars decoded (`open(...,encoding='utf-8')`). This is the canonical text form:
  `file` reports the `.raw` as "JavaScript source ... UTF-8", not UTF-16LE, so the `.txt` is not a lossy decode.
- FAQ companion capture `.../.qcache/c4e1446a42d0a709c34097be.txt` — UTF-8 with BOM, 45,308 bytes
  → 41,495 chars decoded as utf-8-sig. Used only to adjudicate the register row; it cannot ground row S099 spans.

## Gate block draft — lane row S099 (numbered from staged S091)

- URL: `https://www.ncpssd.cn/` (homepage; renumber.tsv maps S091 → S099, action append)
- Access date: 2026-10-25 (the capture's own page date reads `2026年10月24日 星期六`, txt line 54)
- Quotes (each ≤25 whitespace words, ≤160 chars, each occurs EXACTLY ONCE in the .txt form):

| # | quote (byte-exact) | form | offset `text.find` | count |
|---|---|---|---|---|
| Q1 | 中国社会科学院图书馆承建 | .txt | 168 | 1 |
| Q2 | 请 登录 注册 | .txt | 110 | 1 |

- Verification command (observed output):
  `python3 - <<'EOF'` → `Q1 codepoints: ['0x4e2d',...]` (12 CJK glyphs, no spaces) → `Q1 find/count: 168 1`;
  `Q2 codepoints: ['0x8bf7','0x20','0x767b','0x5f55','0x20','0x6ce8','0x518c']` (ASCII U+0020 spaces)
  → `Q2 find/count: 110 1`. `承建 count 1 | 注册 count 1 | 登录 count 1`. Fullwidth-space variants: none (count still 1).
- Anchor cell draft: `首页头部“您好/登录注册”区 — char 110`; `首页机构署名“中国社会科学院图书馆承建” — char 168`.

## Support verdicts for the staged entry's claims (capture = homepage .txt)

| claim (entry Observation / append row S099) | verdict | evidence |
|---|---|---|
| built/operated by CASS Library | **supported** (built) / **narrower** (operated) | Q1 `中国社会科学院图书馆承建`; operation not literally stated on homepage — only affiliation signals (承建, footer `E-mail： ncpssd@cass.org.cn`, txt line 2193) |
| free after registration | **not supported** | Q2 shows only a 登录/注册 header (`请 登录 注册`, char 110); no free/公益 statement about NCPSSD on homepage. The only `公益` occurrence (char 7388) is the external-resource nav item `PubScholar公益学术平台`, not a claim about NCPSSD |
| full-text download only for registered users | **not supported** | no `全文下载`/`注册用户` span on homepage; the only `下载` (char 7810) is footer `扫一扫下载APP` (app download), not article full-text policy |
| foreign journals and 古籍 online-reading only | **not supported** | homepage 资源 nav lists categories `中文期刊 / 外文期刊 / 古籍 / 集刊 / 外文图书` (txt lines 82-92, 1579-1589) but states no reading/download restriction; the only `阅读` (char 6535) is an article title `阅读史视域下…` |

Note: the staged entry already attributes the access-model statements to the help page ("its help states…"), which is a different capture
(`c4e1446a42d0a709c34097be`) and cannot ground this row. This row therefore supports only Q1/Q2-level facts; the access-model spans
remain ungrounded at this row.

## Absent-defect register row S086 (chousa slice) — re-check

- Register cites `https://www.ncpssd.cn/` with quotes:
  1. `我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务`
  2. `我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`
- My own re-check against the homepage capture (observed):
  `'我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务' -> -1 count 0`;
  `'我们的网站是面向全社会，公益的，您注册成功后，可进行使用。' -> -1 count 0`; fragments `仅对网站注册用户/仅提供在线阅读服务/面向全社会/注册成功后` all count 0.
- Companion FAQ capture (observed): quote 2 at offset 24872, quote 1 at offset 25269, each count 1 (utf-8-sig decode).
- **Verdict: absent-as-written** for the cited homepage capture — the spans are not in the named source's capture. **Not fabricated**: both
  strings occur verbatim in the companion help-page capture (offsets 24872/25269), consistent with round-48's Gate-table verdict (present,
  pointer `QuarantineS086.md` → FAQ capture). `unreachable` does not apply (capture exists and was opened).

## Other findings

- Staged append S099 sources cell says "read 2026-10-23", but the homepage capture's own date is `2026年10月24日 星期六`
  (txt line 54): the row's read-date is one day older than the captured page date — flag for recordkeeping calibration.
- No /tmp scratch was created (`/tmp/chousa-r49-GroundS099` does not exist); nothing to clean.

VERDICT: re-grounded staged row S091/S099 against the homepage capture — Q1/Q2 quotes located (chars 168/110, each unique), built-by-CASS supported, access-model claims not supported by this capture; register S086 re-checked absent-as-written on the homepage but not fabricated (present verbatim in FAQ capture).
