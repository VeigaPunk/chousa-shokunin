# GroundIsticRecheck — round 50 / w1: the ISTIC repeat-commission provision and the page's silences

seat: `GroundIsticRecheck` (leaf, no dispatch) · lane `chousa-shokunin` @ `775417271bcae0ff642133f32b2d5388b1b2339b` (read-only)
target: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/001287c436f0e6b1d166ae8d.{txt,raw}`
url: `https://chaxin.las.ac.cn/service/citation-search`
entry this feeds: `corpus/knowledge/istic-citation-verification-r39.md` — staged id **S118** (`SOURCES.append.md:43`), planned lane id **S104**
network: none used; L0 `8d77e6c1` open. Every byte below is the on-disk capture.

## 1. Capture identity

| form | bytes | chars | sha256 |
|---|---|---|---|
| `.txt` | 5,599 | 2,288 (112 lines) | `67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db` |
| `.raw` | 352,066 | 346,919 (UTF-8, `<meta charset="utf-8">`) | `203b16907c2c953e49bb71310df2a5fd761d3f1798115ceb2ad6881cd01c17c5` |

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://chaxin.las.ac.cn/service/citation-search').hexdigest()[:24])"
001287c436f0e6b1d166ae8d
$ stat -c '%n %s %y' 001287c436f0e6b1d166ae8d.txt 001287c436f0e6b1d166ae8d.raw
…001287c436f0e6b1d166ae8d.txt 5599 2026-10-23 20:39:42.391724932 -0300
…001287c436f0e6b1d166ae8d.raw 352066 2026-10-23 20:39:42.388556450 -0300
```
- Key = `sha256(url)[:24]`, matches. Both forms carry the same mtime, which agrees with the staged entry's `page read 2026-10-23`.
- The `.txt` is the page text (0 `<`, 112 lines); the `.raw` is the HTML. **Form used for every quote below: the `.txt` read as UTF-8.**
- Freshness: this capture is 2 days old at 2026-10-25; the newest `.txt` in the cache is `2026-10-24 23:26:57`, so freshness is bounded by L0, not by this seat.
- **Page-scoped, not service-scoped, by measurement.** Every `https?://…chaxin\.las\.ac\.cn…` URL referenced in the staged package and the lane tree (walked over all `.md`) is one URL — this one — and its key has `.txt`+`.raw` on disk. The cache holds no sibling page of this service, so a service-wide silence claim is unsupported by on-disk evidence and I make none.

## 2. The provision, re-grounded

The staged sentence ("a repeat commission within two years on the same requirements may reuse the previous result, provided the earlier result is supplied; the same data is then not re-charged") sits inside a **scope heading the entry drops**. `.txt` 684–884, read in order:

- `684` **`2.针对中国科学院用户：`** — the heading; everything to `884` is a concession *for CAS users*, under `收费说明` → `优惠措施`.
- `684–735` `（1）引用检索费：3元/次（1-200次），2元/次（200次以上）` — a CAS-only price.
- `735–810` the provision itself (Q2): **four conditions** — CAS user (`2.`), `2年内` repeated commissions, `检索要求相同`, and `用户在提供上次检索结果同时`.
- **Waived:** `本次检索可免去相同数据的费用` — `可` makes it discretionary, and what is waived is the *same data's fee*, not the search.
- **Retained:** `但要收取本次检索的开库费、复核费和证明费` — database-opening fee, review fee, certification fee.
- `849–872` (Q3) a **second** CAS route: the user may search `SCI、EI、ISTP` themselves and bring a printout `一周之内` old for `复核` (5 元/篇 收录, 20 元/篇 引用). This is the page's only *recency* bound on a retrieval, and the entry does not have it.
- **Not stated anywhere in the slice:** that the previous result is reissued as the new report; that the repeat result is re-verified against a named index state; any index snapshot, index version or retrieval date.
- `[INFERENCE]` The retained `复核费` implies the earlier result is **re-reviewed**, not re-issued unchanged; the page never uses the word 复用 or says the report is reused. "May reuse the previous result" is therefore stronger than the text — the text's mechanism is a fee waiver for identical data plus a paid review.

## 3. Located quotes (`.txt` read as UTF-8; 1-based line; `text.find` offset)

| # | quote (byte-exact) | off | line | chars | ws | txt | raw |
|---|---|---|---|---|---|---|---|
| Q1 | `2.针对中国科学院用户：` | 684 | 69 | 12 | 1 | 1 | 1 |
| Q2 | `对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用，但要收取本次检索的开库费、复核费和证明费。` | 735 | 69 | 75 | 1 | 1 | 1 |
| Q3 | `将一周之内的网络检索结果打印后到我中心进行复核` | 849 | 69 | 23 | 1 | 1 | 1 |
| Q4 | `通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况` | 211 | 56 | 56 | 1 | 1 | 1 |
| Q5 | `按合作者排除自引标准统计他引次数` | 549 | 67 | 16 | 1 | 1 | 1 |
| Q6 | `附言：报告号，开票类型` | 1078 | 75 | 11 | 1 | 1 | 1 |
| Q7 | `03 完成并审核 报告 06 出具正式报 告并存档` | 380 | 59 | 25 | 6 | 1 | 0 |

```
$ python3 - <<'PY'   # per quote: find() offset / line / chars / ws-words / txt.count / raw.count
Q1 684/69/12/1/1/1   Q2 735/69/75/1/1/1   Q3 849/69/23/1/1/1   Q4 211/56/56/1/1/1
Q5 549/67/16/1/1/1   Q6 1078/75/11/1/1/1  Q7 380/59/25/6/1/0
PY
```
(same run as §3's table, columns compacted for width)
All seven: exactly once in the `.txt`, ≤25 whitespace words, ≤160 chars, no newline. Q7 is the byte-exact repair of the staged entry's `"03 完成并审核报告 06 出具正式报告并存档"` (`txt=0 raw=0`, measured) and is **already emitted by `GroundIsticA`** — do not double-emit it.

## 4. Machine lines

```
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	2.针对中国科学院用户：	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用，但要收取本次检索的开库费、复核费和证明费。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	将一周之内的网络检索结果打印后到我中心进行复核	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	按合作者排除自引标准统计他引次数	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	附言：报告号，开票类型	corpus/knowledge/istic-citation-verification-r39.md
```
`staged-id` = the round-50 staged package row (`merge/chousa/SOURCES.append.md:43`, file sha256 `a6dec4a0…aa696`); the planned lane id is `S104` (lane max is `S103`, no `S104` row). All six bind to the `.txt` form, which `corpus/evidence/round50/build-spans.py:55-65` tries first as UTF-8 — so the `.raw`-decoded-as-UTF-16LE hazard (`GroundIsticA` F8) does not bite them. At least one `char N` in the lane row's `anchor` cell can be any of `684 / 735 / 849 / 211 / 549 / 1078`.

## 5. Silence sweep (the negative claim carries this)

```
$ python3 - <<'PY'   # str.count per term, whole .txt (2,288 chars) and whole .raw (346,919 chars)
term            TXT  RAW          term            TXT  RAW
版本               0    0          编号               0    0
快照               0    0          单号               0    0
数据库版本            0    0          流水号              0    0
日期               0    0          检索时间             0    0
更新               0    0          snapshot           0    0
报告号              1    1          version            0    0
PY
```
- **The five assigned terms are absent from both forms.** The `.txt` was read whole (2,288 chars), so the sweep is exhaustive for the page text, not a sample.
- **The page's only temporal bindings are durations, not dates:** `2年` @739 (the provision window), `一周` @850 (CAS self-search recency), `5个工作日` @1483, `2个工作日` @1531, `4小时` @1624 (turnaround and cancellation). The other `年` hits (@1361, @1403) describe the *paper list's* 年、卷、页码 fields. A `\d{4}[-年/]\d{1,2}` scan of the `.txt` returns `[]`.
- **Identifier-shaped hits, classified:** `报告号` @1078 is real but it is the payment-memo field (`用途：检索费` / `附言：报告号，开票类型`), i.e. a billing key for an issued report, not a retrieval-run id and not a binding to an index state.
- **The `.raw` bundle does carry version-shaped and date-shaped tokens, and none of them is the index's:** `tailwindcss v3.4.17` @1401 and `normalize.css v5.0.0` @16142 (CSS licence banners), `ionicons…?v=3.0.0` @19612 ×5 (font-face URLs), Nuxt `buildId:"c9a7dd8c-…"` @346813 and `/_nuxt/builds/meta/c9a7dd8c-….json`, and `appCode=<14-digit timestamp><suffix>` @232 in a third-party `ai.kuaijing.cn` iframe src. These name the **site build and a vendor app**, not SCI/SSCI/EI/ESI/CSCD state. They live in `<script>`/`<style>`, which is why the text form drops them.
- **Province note (shape only):** the `.raw` client runtime config carries a field labelled `APP_AUTH_SECRET` @346744. Its value is **not** reproduced here (PROVINCE: secret values → kagi, shape-only here). It is served to the browser, so it is public rather than leaked, but it is secret-shaped and must not be pasted into any entry, lesson or span.
- **Verdict of the sweep:** the negative claim survives only in this scoped form — *the service's own statements name no index snapshot, no index version, no retrieval date and no retrieval-run identifier; the page bounds two retrievals by duration (2 years between repeat commissions, 1 week on a CAS user's own printout) and names one report number for billing.* An unscoped "the page names no version and no date" would be false of the raw bytes.

## 6. What the staged entry gets wrong (for the L1 to fix; I changed nothing)

- **D1 — scope dropped.** The entry states the repeat provision unconditionally; the page puts it under `2.针对中国科学院用户：` (Q1). As written, a non-CAS reader would believe they hold the concession.
- **D2 — mechanism overstated.** "May reuse the previous result" → the page waives the *same data's fee* (`可免去`, discretionary) and still charges 开库费、复核费、证明费 (Q2). `[INFERENCE]` the retained review fee means re-review, not reissue.
- **D3 — misnamed.** The entry calls it "a recheck mechanism". The page's words are `多次委托` under `优惠措施`; it describes no recheck of a previous *report*. (`复核` in Q3 is a review of a *user-supplied* search.)
- **D4 — the sibling route is missing.** Q3 gives a second CAS path (own search within one week → paid 复核). It is the page's only recency bound and the entry's Unknown section needs it, because it is the one place the page says anything about how fresh a retrieval may be.
- **D5 — the page gives two database lists.** 服务介绍: `SCI、SSCI、EI、ESI、CSCD` (Q4, with `等`). CAS self-search path: `SCI、EI、ISTP`. `ISTP` occurs nowhere else in either form. The entry's "from SCI, SSCI, EI, ESI and CSCD" is right for the service and incomplete for the page.
- **D6 — already reported by `GroundIsticA`** (workflow quote not byte-exact, fees retained, English gloss inside quotation marks); Q7 is the repair, and I do not re-emit it.

## 7. Integration notes

- **Wave id convention is inconsistent, measured:** `GroundIsticA` emits `S118` for this page; `GroundSxuScope` emits `S105` (planned) while `GroundSxuDefn` emits `S124` and `S135` (staged) for the *same* sxu PDF; `GroundSeuB` emits `S106` (planned). The L1 must collapse by URL, not by id, or one document will land as three rows.
- The staged entry's `source:` line and the lane row must both re-key to `S104 — https://chaxin.las.ac.cn/service/citation-search`, and the anchor cell must carry one of the offsets in §4.

## 8. Limits

- `tools/quote-reopen.py` fetches live registry URLs (`tools/quote-reopen.py:1-20`), so criterion 25's tool cannot run under L0 `8d77e6c1`. The `VERBATIM` evidence here is a local `str.find`/`str.count` on the capture — a different instrument, recorded as a tool limit, not relabelled as `QUOTE_REOPEN`.
- "The page says X" always means "the capture dated 2026-10-23 says X"; the live page was not fetched.
- The `.txt` is a derived form. Q5 and Q7 are text-form-only in part (`raw=0`) because the raw splits them across `<td>`/`<tspan>` nodes; the span slice is the `.txt` slice either way.
- I did not run `c2-count.py` or `build-spans.py`: the lane entry, `spans.tsv` and `corpus/lessons/round-50.md` do not exist yet, so there is nothing for them to read on this leg. State observation, not a verdict on the frozen counter.

## 9. Tooling and scratch

No install, no upgrade, no pacman transaction (host-wide pause respected); nothing was installed, so nothing to record. Scratch `/dev/shm/chousa-r50-GroundIsticRecheck/` (one long-line dump) created and deleted. Only write: this report.

VERDICT: attacked the staged S118 repeat-commission sentence against the capture — the provision is a CAS-only concession under `2.针对中国科学院用户：` @684 that waives the same-data fee @735 (`可免去`, discretionary) while retaining 开库费、复核费、证明费 and adds a second one-week recency route @849, so "may reuse the previous result" is refuted as overstatement; the silence claim survives only when scoped, since 版本/快照/数据库版本/日期/更新 are 0 in both forms while the raw carries front-end versions and a Nuxt buildId, and the page's only temporal bindings are durations (2年, 一周, 5/2 工作日, 4小时).
