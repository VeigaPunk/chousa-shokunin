# ReviewS086Ratio

Seat: leaf reviewer. No subagent. No production edit. No network. No tool install.
Axes: operability (one interpreter, the digested capture, no reroute), calibration (published 4/46 and 2/29, bound not retuned), depth (independent longest-run, not the counter's printout).
Milestone: Round 43 absent-class split. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Recommendation only. Not an admission.

## Verdict

Published figures match. Independent recompute of S086's two quotes against the committed text capture, after NFKC and whitespace collapse, is **4/46** and **2/29**.

Max ratio is 4/46 = 0.08695652173913043, below the frozen 1/2 bound, so the row stays `not-carried`. The bound was not retuned.

## Identity

`git rev-parse HEAD` printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
`git log -1 --format='%H %s' 737f40b6aa8f37ffe2269db370fd6d65a720d9a8` printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8 round-43: split the absent class and adopt one locally re-opened search-log entry`.
`git merge-base --is-ancestor 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 HEAD` exited 0.
`python3 --version` printed `Python 3.14.8`. `sys.executable` printed `/usr/bin/python3`.
`git status --porcelain` on the round-42 verdict, examine receipt, and digest paths printed no lines.

Quotes were taken from the register data row, not from the published fractions. Register line 41, lane cell `` `chousa` ``, id `S086`, URL `https://www.ncpssd.cn/`:

- quote 1: `我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务`
- quote 2: `我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`

`sha256("https://www.ncpssd.cn/")[:24]` is `76914d78c20094f677dea77d`. That is the file named in `corpus/evidence/round42/receipts/examine.txt` lines 11–12 and in `corpus/evidence/round42/receipts/digests.txt` line 16. Slash-stripped and `http://` variants hash to keys whose `.txt` files do not exist. No same-identity reroute.

Capture bytes: 15270. SHA-256 `7a4ef1386800f55a520f003d16260e4237d2464dbfb3c274380714717269b2dd`, equal to the digest line. Register SHA-256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, equal to digests line 4. Quote SHA-256 prefixes `6c0f0f6bb827` and `e5dcf110a0ab` equal the examine receipt's quote hashes. The `.qcache` path is not a shokuknow git blob (`git ls-files --error-unmatch` exited 1). Identity is the digest, and the digest matches.

`Path.read_text` (universal newlines, the mode `cache_doc` uses) yields 7943 characters. That is the "7943-char capture" in `corpus/evidence/round42/quarantine-verdicts.tsv` line 6. Raw decode keeps 1745 CR characters (9688 chars). After NFKC and whitespace collapse the two readings are equal, length 4088. The ratios do not depend on which reading is used.

## Independent recompute

Normalization, as frozen: `re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()`. NFKC changes only U+FF0C FULLWIDTH COMMA to U+002C (quote 1 index 29; quote 2 indices 11, 15, 22). Lengths stay 46 and 29. The measured runs do not include those commas.

Longest contiguous common run was not taken from `tools/absent-split.py`. Three algorithms were run on the collapsed capture before any lane function was imported:

- binary search on window length, confirmed by `str.find`
- DP with the document as the outer axis (the lane DP iterates the quote outside)
- `difflib.SequenceMatcher(..., autojunk=False).find_longest_match`

Stdout of that run, verbatim:

```
S086_LINES 1
LINE 41 NCELLS 9
  CELL0=''
  CELL1='`chousa`'
  CELL2='round1'
  CELL3='S086'
  CELL4='`payload-absent`'
  CELL5='https://www.ncpssd.cn/'
  CELL6='`我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务`<br>`我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`'
  CELL7='cited source, companion URLs and local artifacts were all checked; the quote is in none of them'
  CELL8=''
URL 'https://www.ncpssd.cn/'
NQUOTES 2
CACHE_KEY 76914d78c20094f677dea77d
VARIANT_KEYS
  'https://www.ncpssd.cn/' -> 76914d78c20094f677dea77d exists=True
  'https://www.ncpssd.cn' -> 7bfc2f473eb8790cdafedbb7 exists=False
  'http://www.ncpssd.cn/' -> 3bd9b498c52670921f95ef5d exists=False
CAPTURE_BYTES 15270
CAPTURE_SHA256 7a4ef1386800f55a520f003d16260e4237d2464dbfb3c274380714717269b2dd
RAW_EXISTS True RAW_BYTES 197752
RAW_SHA256 60c746513b7f13ea78e0d94f18a6a0a079674e2b84b795bb262d0f0683db0f93
RAW_HEAD b'\r\n\r\n\r\n\r\n\r\n    <!'
UTF8_STRICT ok chars 9688 newlines 2249
DOC_NFKC_WS_LEN 4088
NFKC_CHANGED_DOC True
--- QUOTE 1
RAW_LEN 46 FOLDED_LEN 46
NFKC_EQ_RAW False
NFKC_CHAR_CHANGES [(29, '0xff0c', '0x2c')] n 1
MEMBERSHIP 4/46 SPAN 中文期刊
DP_DOC_OUTER 4/46
DIFFLIB 4/46 SPAN 中文期刊
EXACT_IN_DOC False
EXACT_IN_RAW_BODY False
ALL_MAX_SPANS [(17, '中文期刊'), (30, '外文期刊')]
--- QUOTE 2
RAW_LEN 29 FOLDED_LEN 29
NFKC_EQ_RAW False
NFKC_CHAR_CHANGES [(11, '0xff0c', '0x2c'), (15, '0xff0c', '0x2c'), (22, '0xff0c', '0x2c')] n 3
MEMBERSHIP 2/29 SPAN 我们
DP_DOC_OUTER 2/29
DIFFLIB 2/29 SPAN 我们
EXACT_IN_DOC False
EXACT_IN_RAW_BODY False
ALL_MAX_SPANS [(0, '我们'), (3, '网站'), (6, '面向'), (9, '社会'), (12, '公益'), (17, '注册'), (26, '使用')]
TAGSTRIP_DOC_LEN 4088
TAGSTRIP_Q1 4/46 SPAN 中文期刊 EXACT False
TAGSTRIP_Q2 2/29 SPAN 我们 EXACT False
UNESCAPE_CHANGED False
UNESCAPE_Q1 4/46 EXACT False
UNESCAPE_Q2 2/29 EXACT False
CJK_CHARS_IN_CAPTURE 2677 UNIQUE 553
```

A second run on the text-mode body (7943 chars), the capture the tools actually read, printed:

```
NO_COLLAPSE_NFKC_ONLY q1 (4, '中文期刊')
NO_COLLAPSE_NFKC_ONLY q2 (2, '我们')
RAW_NO_NORM q1 (4, '中文期刊')
RAW_NO_NORM q2 (2, '我们')
PROD_longest_run q1 4/46
PROD_longest_run q2 2/29
Q1_SHA12 6c0f0f6bb827
Q2_SHA12 e5dcf110a0ab
```

`中文期刊` is contiguous in the raw `.txt`, not a join across whitespace. First context: `'\n 帮助 \n \n\n \n 中文期刊 \n\n 外文期刊 \n\n '`. Collapsing whitespace does not create the run of 4, and skipping NFKC does not change it.

Cross-check after the independent result, not instead of it: `c2-count.py`'s `nfkc_ws` document equals the independent collapsed document, and its `longest_run` returns the same fractions. Stdout:

```
DOC_EQUAL_C2 True DOC_LEN 4088
TEXTMODE_CHARS 7943 FILE_BYTES 15270
FILE_SHA256 7a4ef1386800f55a520f003d16260e4237d2464dbfb3c274380714717269b2dd
Q1 independent=4/46 c2=4/46 span='中文期刊' match_published=True
Q1_SPAN_OFFSETS [93, 247, 2433]
Q2 independent=2/29 c2=2/29 span='我们' match_published=True
Q2_SPAN_OFFSETS [87, 214, 4026]
MAX_RATIO 4/46 0.08695652173913043 BOUND 0.5 CLASS not-carried
FIGURES_MATCH True
```

`corpus/evidence/round43/absent-split.tsv` line 4 is `S086	not-carried	4	46	0.086957	2`. `f"{4/46:.6f}"` is `0.086957`. The sixth decimal is rounding, not a different fraction. Quote 2's 2/29 is the other published figure; the TSV stores only the row maximum.

Neither quote is an exact substring of the capture. The page does contain CJK navigation labels (`中文期刊`, `外文期刊`, `我们`). It does not contain `我们的网站`, `全文下载`, `在线阅读`, `注册用户`, or `可进行使用`.

No fetch was performed.

## Findings by severity

No actionable defect in this seat's scope. The published 4/46 and 2/29 match an independent recompute of the committed capture.

Checked, and not a miss:

- Operability: one runtime, `/usr/bin/python3` 3.14.8, at measured commit `737f40b6`. Capture key is the register URL's sha256 prefix. The slash-stripped URL is a different key and has no file. Text-mode length 7943 and file SHA-256 match the round-42 verdict and digest.
- Calibration: both quotes match the published fractions. Row maximum 4/46 is below 1/2, so R43-SPLIT labels the row `not-carried`, which is the TSV label. The bound was not moved to absorb the row.
- Depth: three algorithms agree with each other before the lane DP is consulted. The lane DP, called afterwards, agrees. The runs survive without whitespace collapse and without NFKC. Tag strip and HTML unescape do not change them. The 4-character spans are real navigation labels, not a DP off-by-one.

There is no resume path and no continuity preflight in this recompute. Nothing in the lane tree, the git index, or `/home/vgpnk/Projects/shokuknow` was written. A failed preflight does not arise; mutation count on those trees is zero.

## Residual risk and verification gaps

- The sibling `.raw` (197752 bytes, SHA-256 `60c746513b7f13ea78e0d94f18a6a0a079674e2b84b795bb262d0f0683db0f93`) is not the capture the rule reads. Against that raw response, after the same NFKC and whitespace collapse, the runs are **5/46** (span `,外文期刊`) and **2/29**. Still below 1/2. The quoted sentences are absent from the raw response as well (`我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务`, `仅对网站注册用户`, `全文下载服务`, `外文期刊、古籍`, `可进行使用`, `公益的` are all absent). This does not contradict 4/46 on the `.txt`. It is recorded so a later reader does not treat the raw file as the published denominator.
- Live-web truth was not checked. `corpus/evidence/round43/claims.md` does not claim it. No fetch was run, so this seat cannot say the site lacks the sentences today.
- This seat did not execute `c2-count.py` or `absent-split.py` as scoring commands. It called `longest_run` only after the independent result, on S086 alone. Full-table agreement is outside this report.
- The `.qcache` file is not a git blob. Continuity is the round-42 digest, which matches the bytes read. A later un-digested replacement of that path would not be visible to git.
