# R54ExecInfStaged — inference-ground findings on the two staged round-54 entries

seat: R54ExecInfStaged · scope: run `tools/inference-ground.py` on the two staged entries and give the
drafting seat one groundable candidate phrase per Inference bullet · only file written is this report.

## 1. The seat command, verbatim (both entries exit 1)

```
$ python3 .../chousa-shokunin/tools/inference-ground.py --entry .../merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r3{6,7}.md --spans /dev/null --counts /dev/null --registry .../chousa-shokunin/corpus/SOURCES.md --root /fast/scratch/hyaku/chousa-r54/R54ExecInfStaged/root
GROUND entry=source-type-taxonomy-r36.md section=1 bullets=4 tokens=4 grounded=0
GROUND: FAIL        (exit 1)
GROUND entry=source-type-taxonomy-r37.md section=1 bullets=4 tokens=4 grounded=0
GROUND: FAIL        (exit 1)
```

The 20 `FINDING` lines the tool printed are listed per bullet in §2's *finding* column, with the offending
token quoted there; every one of the 8 bullets carries `INF_UNCITED`.

**All 8 bullets are `INF_UNCITED`**: rule 2 wants a source id *inside the bullet* — `ID_RE` reads bullet text
only, and the staged bullets carry no `S###` token (the ids sit in the `source:` header lines, which the tool
never reads). A drafted bullet must name its id inline; the landed entries do (r36: `` `S121` ``/`` `S122` `` once
each; r37: `(S123)` six times).

## 2. Candidate phrase per bullet

Each candidate occurs **exactly once** in its capture's `.txt` form, **on one line**, is ≥2 words / ≥4 CJK
chars (the tool's `has_two_words` floor), ≤25 whitespace words and ≤160 chars, and is byte-exact. Capture key
= first 24 hex of sha256(url).

| entry | bullet (first 60 chars) | finding | candidate phrase | capture key | offset |
|---|---|---|---|---|---|
| r36 | "The Chinese standard is the PRC's counterpart to the lane's " | INF_UNCITED + INF_UNGROUNDED | `本标准非等效采用ISO国际标准：ISO 690:2021。` | `adf6ba934e813b2c326fa150` | 1797 |
| r36 | "That is a precise and useful shape for the lane's tiering: a" | INF_UNCITED; INF_TOKEN_NOT_IN_SPAN ×3 ('the identity, status and adoption basis of the Chinese citation standard', 'the document-type taxonomy the standard prescribes', '403') | `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` | `b9ca2a4fdf9455867534f144` | 15188 |
| r36 | "A **type** taxonomy and the lane's **tier** rule are differe" | INF_UNCITED + INF_UNGROUNDED | `中国标准分类号` | `adf6ba934e813b2c326fa150` | 1507 |
| r36 | "The version pivot is the sharpest available lesson for the l" | INF_UNCITED; INF_TOKEN_NOT_IN_SPAN '2026' | `代替了以下标准` | `adf6ba934e813b2c326fa150` | 1110 |
| r37 | "**The scope clause is the most useful thing in the standard " | INF_UNCITED; INF_TOKEN_NOT_IN_SPAN '7714','2025' | `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献` | `0f33243fd7ac2fe88b85c1ba` | 5602 |
| r37 | "**A type taxonomy and the lane's tier rule are different axe" | INF_UNCITED + INF_UNGROUNDED | `文献类型标识、文献载体标识应按照附录Ａ` | `0f33243fd7ac2fe88b85c1ba` | 11542 |
| r37 | "**The identifier taxonomy is what makes a citation machine-c" | INF_UNCITED + INF_UNGROUNDED | `电子资源既应著录文献类型标识` | `0f33243fd7ac2fe88b85c1ba` | 11564 |
| r37 | "**Two consecutive standards, two scopes, one continuity.** T" | INF_UNCITED; INF_TOKEN_NOT_IN_SPAN '7714','2025' | `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` | `0f33243fd7ac2fe88b85c1ba` | 4736 |

Measured: every row `n=1 crossNL=False has_two_words=True`; chars 29/47/7/7/32/19/14/28, lines
468/491/407/291/166/361/361/132. The `quotes.tsv` rows (`id⇥url⇥quote⇥entry`) are these candidates with their
own row's entry (r36 → `corpus/knowledge/source-type-taxonomy-r36.md`, r37 → `…-r37.md`) and the URL of their
capture key. **Round trip**: the eight candidates were fed to the lane's own
`corpus/evidence/round54/build-spans.py` (scratch copies only); a drafted pair of entries — each bullet carrying
its candidate in backticks plus its lane id inline — then ran through the real tool:
`GROUND entry=…r36.md section=1 bullets=4 tokens=4 grounded=4 / GROUND: PASS`, and the same for r37.

## 3. Three falsified hazards for the drafting seat

**H1 — ASCII `7714`/`2025` in an r37 bullet can never ground from S123.** The JMU PDF renders its digits
fullwidth: ASCII `7714` count **0**, fullwidth `７７１４` count **55** in `0f33243fd7ac2fe88b85c1ba.txt`. A bullet
writing `GB/T 7714-2025` in prose yields tokens `7714` and `2025` no S123 span carries —
`FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='7714'` / `token='2025'`, `GROUND: FAIL`. The fullwidth rendering
*does* ground when a span carries it: the PDF's own `ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》`
(char 3602) passes `GROUND: PASS`.

**H2 — the numeral `403` has no carrier anywhere.** `403` count **0** in all three theme `.txt` forms. Across
the 2,549-file cache, 194 `.txt` captures contain `403` and 19 contain `7714`, but none of those 19 carries the
standard's type-table markers (`文献类型标识`, `载体标识`, `缩微资料`, `附录Ａ`, `舆图` all 0) — the reseller's
reproduction is not in the cache, so the staged r36 bullet 2's "HTTP 403 this round" describes a fetch the cache
does not hold. A bullet keeping `403` fails: `FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='403'`.

**H3 — r36 bullet 3's exclusion list is not in r36's own two captures, and one term is mistranslated.**
`图书馆员 / 文献目录编制者 / 索引编制者` each count **0** in the SAMR record (`adf6ba93…`) and **0** in the openstd
page (`b9ca2a4f…`), and **1** each in the JMU PDF (S123, r37's source) — so the staged r36 bullet 3 asserts the
list while citing only S085/S086; the `中国标准分类号` cell (S121, char 1507) is what r36's own captures carry, and
the list belongs to r37. Separately, the staged bullet reads "excludes librarians, **bibliophiles** and indexers",
but the capture's second term is `文献目录编制者` (bibliographic *catalogue* compilers); `文献爱好者` (bibliophiles)
occurs **0** times. The landed r37 renders it correctly.

## 4. Counter-level findings (frozen `c2-count.py` logic, applied to the staged texts)

**F1 — the staged `source:` headers name ids the lane already uses.** `S085` = FEVER dataset release page,
`S086` = the FEVER NAACL paper, `S093` = climate-fever. On the staged headers `REF_ID_UNBOUND = 3` (S085, S086,
S093; S101 counts as held-ok), so the counter's `unb == 0` fails: the staged ids must be re-bound to the lane's
new rows **S121** (SAMR record), **S122** (openstd notice), **S123** (JMU PDF) — which is what the landed rows do.

**F2 — adopting the held S101 citation needs its `used-by` widened.** The staged r37 carries `source: S101 —
https://jc.hit.edu.cn/…/1f6f2731-….doc`, and S101's row today reads `used-by:
corpus/knowledge/citation-count-semantics-r37.md` only; the counter's held check requires the citing entry to be
in S101's `used-by`, so that cell must also name `corpus/knowledge/source-type-taxonomy-r37.md`. (The landed r37
drops the HIT citation — `HELD_CITED=-`, `HELD_BAD=0` — which also satisfies the claim: the HIT document is
optional, "optionally the HIT data specification".)

**F3 — a quote row for a held id breaks the manifest.** The counter's ok-condition includes `on_bound == n`.
With the lane's 33 rows all bound, `on_bound = 33 == n = 33`; one added S101 row gives `on_bound = 33 != n = 34`,
so the counter fails. Held documents must not carry quote rows.

**F4 — the HIT `.doc`'s `.txt` sidecar carries no Chinese.** In `6dc68fd6b32ce9c8dfcebce8.txt`: `可获得地址`
n=0, `文献标志码` n=0, **14,486 U+FFFD**. The usable text is the `.raw` UTF-16LE decode (`可获得地址` n=2 at 1540,
`文献标志码` n=14 at 10922) — what `build-spans.raw_form` produces, and what the lane's `S101-text-form.txt`
(27,012 chars, 0 U+FFFD, from `tools/capture-text.py`) records.

**F5 — quarantine slice re-check (register rows on theme URLs).** Re-read against the register's own payload
strings, all three are **absent-as-written** (the landed lesson already carries that verdict): **S080** (SAMR) the
joined `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` occurs **0** times (`标准号：` itself 0
times), the three values being separate cells (`发布 于 2025-12-02` char 1029, `实施 于 2026-07-01` char 1048,
each once); **S088** (JMU) the slash-joined carrier list occurs **0** times, its five rows being separate lines
of 表Ａ．２ (`磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）` 59025 … `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` 59201,
each once; the register's payload is itself fullwidth `ＭＴ / ＤＫ`, joining name+code without the capture's column
padding, so it occurs neither way); **S096** (HIT) in the defined OLE form the `…`-elided splice occurs **0**
times and its third piece `参考文献格式，参照 GB/T 7714，采用` is **not** in the capture, whose parameter table
reads `参考文献格式，参照ISO 690` — yet one register sub-piece *is* verbatim present,
`根据GB3469规定，以单字母方式标识以下各种参考文献类型` (raw-UTF-16LE char 1616; OLE-form char 336 — the two forms carry
different offsets), so the row is absent-as-written rather than wholly absent.

## 5. Lane state, and the frozen claims

The lane has already landed drafts and rows: with the lane's own round-54 manifest both entries pass the tool
(`GROUND: PASS`, tokens 6 and 11, all grounded) and the frozen counter reads `C2=PASS` (`ENTRIES=2/2
BOUND=3/3 REF_ID_UNBOUND=0 QUOTE_ROWS=33 ON_BOUND=33/33 SPAN_IDS=3/3 QUOTES_IN_SPAN=33/33
QUOTES_IN_ENTRY=33/33 QUOTES_IN_LESSON=33/33 QUOTE_SHORT=33/33 SPAN_CONTEXT=33/33 CAPTURE_BOUND=33/33
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=3/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0`). The staged texts analysed above are the campaign's versions, not the landed
ones; the differences a drafter must preserve are §1's inline-id rule and §3's three hazards.

No frozen predicate, target, counter or control was changed or proposed for change. The staged texts were read
read-only from `merge/chousa/`; every capture came from the on-disk `.qcache`; no network was used. Tooling: no
install was needed (Python 3 stdlib only; the HIT `.doc` text came from the lane's own `tools/capture-text.py`
candidate). Scratch under `/fast/scratch/hyaku/chousa-r54/R54ExecInfStaged/` was removed on exit; no lane file
other than this report was written.

VERDICT: ran `inference-ground.py` on both staged entries (8/8 bullets `INF_UNCITED`, 12 token findings) and
supplied 8 groundable candidate phrases — one per bullet, each n=1 / one line / byte-exact, with capture key and
offset — which round-trip to `GROUND: PASS` on a drafted pair, and falsified three drafting hazards (ASCII
`7714`/`2025` ungroundable from the fullwidth JMU PDF, `403` with no carrier, r36 bullet 3's exclusion list absent
from r36's own two captures) plus five counter-level constraints (staged ids unbound, held `used-by`, no held
quote rows, HIT `.txt` unusable, the three quarantine verdicts).
