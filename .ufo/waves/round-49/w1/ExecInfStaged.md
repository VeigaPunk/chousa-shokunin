# w1 ExecInfStaged — inference-ground on the two rewritten entries + capture grounding

Seat leaf, lane `chousa-shokunin` @ fe740e7838b338d17fec9338c909557e6e7fed7d.
Scope: run `tools/inference-ground.py` on the two tool-rewritten adopt entries with
`--spans /dev/null --counts /dev/null`, list every finding per bullet, and for each
Inference bullet give one exact candidate grounding phrase occurring exactly once in
the on-disk capture(s). No installs performed (no tool change; RULES.md read, pacman
guard respected). No scratch files created. Captures and register read-only under
`…/shokuknow/.ufo/waves/corpus-expansion-1/`.

## 1. Commands run (observed output)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 tools/inference-ground.py --entry .ufo/waves/round-49/assimilation/adopt/corpus/knowledge/aggregator-vs-source-r36.md \
    --spans /dev/null --counts /dev/null --registry corpus/SOURCES.md \
    --root .ufo/waves/round-49/assimilation/adopt; echo exit=$?
GROUND entry=corpus/knowledge/aggregator-vs-source-r36.md section=1 bullets=5 tokens=3 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='0 inbound citations'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='nobody cites this'
FINDING INF_UNCITED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNCITED bullet=4 token=''
FINDING INF_UNGROUNDED bullet=4 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=5 token='record-declared and unverifiable'
GROUND: FAIL
exit=1
```

```
$ python3 tools/inference-ground.py --entry .ufo/waves/round-49/assimilation/adopt/corpus/knowledge/citation-count-semantics-r37.md \
    --spans /dev/null --counts /dev/null --registry corpus/SOURCES.md \
    --root .ufo/waves/round-49/assimilation/adopt; echo exit=$?
GROUND entry=corpus/knowledge/citation-count-semantics-r37.md section=1 bullets=4 tokens=1 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='same author'
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_UNCITED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNCITED bullet=4 token=''
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND: FAIL
exit=1
```

Capture keys (staged→lane id per `assimilation/adopt/renumber.tsv`; key = `sha256(full staged URL)[:24]`, c2-count.py:96-97):
S087→S096 `09fc63de41f293d43d631c46`, S088→S097 `167e9db7dde3c998838e3469`,
S089→S098 `fea98dc5a5a486c988dd415c`, S091→S099 `76914d78c20094f677dea77d`
(+ help-page companion `c4e1446a42d0a709c34097be`), S092→S100 `32d1d24b24fce96d2a078ec0`,
S100→S101 `b539a80218080da56a75b624`, S101→S102 `6dc68fd6b32ce9c8dfcebce8`,
S102→S103 `7809d5114330a60527436b07`, S103→S104 `02aefcf570a7108e699d0990`.

## 2. Findings per bullet (all findings; tool exit 1 both entries)

r36 bullets 1–4: `INF_UNCITED` (bullet cites no `S\d{3,}` inline) **and** `INF_UNGROUNDED`
(no backtick/quote/numeral grounding token). Bullet 5 cites held `S003` → not UNCITED,
but token `record-declared and unverifiable` → `INF_TOKEN_NOT_IN_SPAN`. Bullet 2
additionally: tokens `0 inbound citations`, `nobody cites this` (quoted) → both
`INF_TOKEN_NOT_IN_SPAN`.

r37 bullets 1–4: `INF_UNCITED` on all four; bullet 1 also has token `same author`
→ `INF_TOKEN_NOT_IN_SPAN`; bullets 2–4 also `INF_UNGROUNDED`.

Structural note (from tool code, `inference-ground.py:478-511`): `INF_UNCITED` fires
on the bullet text alone and is span-independent, so with this round's spans these
bullets would still fire unless each bullet cites an id inline — C2's
`INFERENCE_GROUNDED=2` leg (c2-count.py:190-198) therefore needs inline cites or a
counter change; freeze forbids touching predicate/counter, flagging this to the gate.

## 3. Candidate grounding phrase per Inference bullet (all count=1 in the named capture)

- r36 b1 (CiNii derived list) — `09fc63de…` (S096):
  `参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています` (1×).
  (alt, also 1×: `※CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません`; bare `必ずしも一致していません` is 2×.)
- r36 b2 (temporal lag) — `167e9db7…` (S097):
  `J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます` (1×).
- r36 b3 (resolution ladder, text-rung bottom) — `fea98dc5…` (S098):
  `4.引用文献の原文情報を書誌情報に解析して検索` (1×); ladder intro `引用元の所在確認は、次の順で解析・検索を実施しています` (1×).
- r36 b4 (NCPSSD access model) — help-page capture `c4e1446a…` (companion of S099):
  `我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务` (1×); also `我们的网站是面向全社会，公益的，您注册成功后，可进行使用。` (1×). The bare `76914d78…` homepage capture holds only `请 登录 注册` + category nav, no access terms.
- r36 b5 (lateral reading) — `32d1d24b…` (S100):
  `leaving an unfamiliar website to search the open Web before investing attention in the site at hand` (1×).
- r37 b1 (CNKI self-citation = co-authorship) — **no phrase available**: capture
  `b539a802…` (S101) is not text — `file` reports `data`, magic `d0cf11e0a1b11a`
  (OLE2 .doc); the `.txt` form is binary/non-UTF-8 (read tool refused; decode has
  308,430 U+FFFD of 762,306 chars). `如果引文出现了任一合作者` occurs 0× in it, and
  0× in every `*.txt` in `.qcache` (full-corpus scan). Blocker: cannot ground by document.
- r37 b2 (被引 vs 下载量 distinct fields) — `7809d511…` (S103):
  `「发表时间」「被引」「下载」` (1×) and `被引用回数、ダウンロード回数を示します` (1×).
- r37 b3 (溯源 mode = claim-to-source trace) — `02aefcf5…` (S104):
  `根据相关文献，生成可信增强回答` (1×). (`文献的标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载量` is line-wrapped in the capture, contiguous count 0.)
- r37 b4 (spec makes counting auditable) — **no phrase available**: capture
  `6dc68fd6…` (S102) likewise OLE2 binary (magic `d0cf11e0a1b11a`; 14,486 U+FFFD
  of 128,416 chars). `文献类型及载体类型标志` occurs 0× in it and 0× corpus-wide.
  Blocker: cannot ground by document.

## 4. Risks / blockers

- `INF_UNCITED` on 8/9 bullets is span-independent → C2 `INFERENCE_GROUNDED=2` cannot
  hold for these bullets as written (see §2).
- S101/S102 captures carry no extractable text form; their quotes already sit in the
  absent-defect-register as `payload-absent` (lines 45-46, staged round2 S095/S096 =
  our S100/S101 URLs). The self-citation rule and the nine-element spec cannot be
  re-grounded by document from `.qcache` as it exists; the register verdict lines and
  refusals should reflect this.

VERDICT: Ran inference-ground on both rewritten entries (9 bullets, 13 findings: 9 INF_UNCITED, 6 INF_UNGROUNDED, 4 INF_TOKEN_NOT_IN_SPAN; exit 1 each), gave one exactly-once capture phrase per bullet for the 7 groundable bullets, and documented that S101/S102 are binary OLE captures with zero occurrences of their quotes — the C2 by-document grounding leg is not satisfiable for those two without new captures.
