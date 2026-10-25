# ReopenS101 — round 49 wave 2 (FALSIFY): lane row S101, journal data-specification copy (OLE .doc)

Seat: chousa lane, leaf. Item attacked: lane row S101 `…/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc` (`corpus/SOURCES.md:111`), its 5 `spans.tsv` rows, and every S101-citing sentence of `corpus/knowledge/citation-count-semantics-r37.md`. Tooling: RULES.md read; nothing installed (none needed). Scratch `TMPDIR=/dev/shm/chousa-r49-ReopenS101` created for the counter and deleted (verified absent). No production/sibling/git/jj/fleet write, no network. Lane tip `87e93353d0…`. Pin check after peers began editing the shared worktree: the S101 registry row and its five `spans.tsv` rows are byte-identical at `git show master:` and in the worktree (`diff` → `S101_ROW_IDENTICAL`, `S101_SPANS_IDENTICAL`); the concurrent edits touch S096/S103 rows and the entry's S103 sentences only, and the entry's S101 sentences are byte-identical at tip and worktree.

## 1. Every S101 span row, recomputed from the capture (script + observed output)

```
python3 - <<'PY'
import hashlib,re,pathlib
C=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache');E=pathlib.Path('corpus/evidence/round49')
U='https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc'
k=hashlib.sha256(U.encode()).hexdigest()[:24];raw=(C/(k+'.raw')).read_bytes();form=raw.decode('utf-16le','replace')
print('KEY',k,'DIGEST.raw',hashlib.sha256(raw).hexdigest(),'DIGEST.txt',hashlib.sha256((C/(k+'.txt')).read_bytes()).hexdigest())
ent=open('corpus/knowledge/citation-count-semantics-r37.md',encoding='utf-8').read();les=open('corpus/lessons/round-49.md',encoding='utf-8').read()
A=[int(x) for x in re.findall(r'char (\d+)',open('corpus/SOURCES.md',encoding='utf-8').read().split('| S101 |')[1].split('\n')[0])]
Q=set()
for l in open(E/'spans.tsv',encoding='utf-8'):
    if not l.startswith('S101\t'):continue
    _,u,sha,off,sf,q,e=l.rstrip('\n').split('\t');off=int(off);sp=(E/sf).read_text(encoding='utf-8')
    o=[m.start() for m in re.finditer(re.escape(q),form)];Q|=set(o)
    print(sf,'off',off,'span',len(sp),'q',len(q),'slice',form[off:off+len(sp)]==sp,'bytes',form[off:off+len(sp)].encode()==(E/sf).read_bytes(),
          'qcount',len(o),'qoff',o,'in_span',q in sp,'span>q',len(sp)>len(q),'entry',q in ent,'lesson',q in les,'words',len(q.split()))
print('ANCHOR',A,'==QUOTEOFFS',set(A)==Q,'fffd',form.count('\ufffd'),'chars',len(form),'units',len(raw)//2)
PY
```
Observed:
```
KEY 6dc68fd6b32ce9c8dfcebce8 DIGEST.raw 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3 DIGEST.txt d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112
spans/S101-1.txt off 11166 span 144 q 25 slice True bytes True qcount 1 qoff [11205] in_span True span>q True entry True lesson True words 1
spans/S101-2.txt off 11166 span 97 q 13 slice True bytes True qcount 1 qoff [11170] in_span True span>q True entry True lesson True words 1
spans/S101-3.txt off 12081 span 171 q 11 slice True bytes True qcount 1 qoff [12161] in_span True span>q True entry True lesson True words 1
spans/S101-4.txt off 11945 span 103 q 55 slice True bytes True qcount 1 qoff [11993] in_span True span>q True entry True lesson True words 3
spans/S101-5.txt off 34370 span 100 q 16 slice True bytes True qcount 1 qoff [34374] in_span True span>q True entry True lesson True words 2
ANCHOR [11170, 11205, 11993, 12161, 34374] ==QUOTEOFFS True fffd 263 chars 64512 units 64512
```
Reading: key recomputed `6dc68fd6b32ce9c8dfcebce8`; recorded digest is the `.raw`'s, so the form is the whole-file UTF-16LE decode (64512 chars = 64512 code units → no surrogate pairs, so "char" is unambiguous; the 263 U+FFFD are OLE binary runs starting at 15499, none inside a span). All five rows are exact slices (str and UTF-8 bytes), each quote occurs exactly once, sits inside its span, the span is longer, and the quote is in the entry and the lesson, ≤25 words / ≤160 chars. The `.txt` sidecar is a lossy UTF-8 decode of the binary (head `efbfbd efbfbd 11 e0 a1 b1 1a`, 14486 U+FFFD) and contains **none** of the five quotes; its digest is not the recorded one, and the anchor cell discloses the `.raw` form — no form ambiguity.

## 2. Registry row `corpus/SOURCES.md:111` — anchor / teaches / scope

Header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (11 cells, `ROW_RE` parses it); URL occurs once in the registry, 0 times at `BASE_REV`; `mined`, `opened 2026-10-25`, `used-by` names the entry.

- **anchor** "section 11 (文献标志码), section 14 (参考文献) and the parameter table …; located quotes char 11170, char 11205, char 11993, char 12161, char 34374": set-equal to the five computed quote offsets, none missing or extra. (Anchor `char N` are *quote* offsets; `spans.tsv.offset` is the *span start* — 11170 vs 11166 — different objects, both correct.) Sections exist: §11 title @10902 / §11.6 @11166; §14 title @11924; §15 "期刊基本参数(Serial parameters)" @33945 with 15.7 the `*参考文献格式` legend @34370.
- **teaches** "nine prescribed elements including 文献类型及载体类型标志": §14.2 "参考文献著录项目" @12049 lists a. 主要责任者, b. 文献题名, c. 文献类型及载体类型标志 @12161, d. 其他责任者, e. 版本, f. 出版项, g. 文献出处或电子文献的可获得地址, h. 文献起止页码, i. 文献标准编号, then `\r14.3` — exactly a–i, nine (§1.1 @1310–1590 repeats the same nine). The word 九 occurs 0 times; the count is a count of the enumeration, verifiable.
- **teaches** "section 14 recommends the GB/T 7714 顺序编码制 or 作者-出版年制 formats while the parameter table refers to ISO 690": §14.1 @11945 "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用…作者-出版年制。" (推荐 = recommends, so "not defers" holds); §15.7 @34370 "参考文献格式，参照ISO 690，…". Holds.
- **teaches** "a separate 文献标志码 A-E classifies each article by content for the purposes of 文献的统计和期刊评价": §11.6 @11166 "为便于文献的统计和期刊评价，确定文献的检索范围，提高检索结果的适用性，每一篇文章或资料应根据其内容性质标识一个文献标志码。本规范共设置以下五种：" + A 基础性理论与应用研究 / B 应用性技术成果报告 / C 业务指导与技术管理性文章 / D 一般动态性信息 / E. Holds (capture says 文章或资料).
- **scope** "the data specification whose fields and type identifiers underlie Chinese journal evaluation and citation statistics": 文献的统计和期刊评价 @11176/11179; 参考文献 "是对期刊论文进行统计和分析的重要信息源之一" @11979; and the capture itself says 引文统计 @5322 (§1.4 "为了减少外文刊名引用不规范所造成的引文统计及链接误差") and @25455 — so "citation statistics" is carried by the capture, not inferred.
- Adjacent (not an asked cell): the source cell's "copy hosted by 哈尔滨工业大学" is not in the capture (`哈尔滨` count 0) — it rests on the URL host `jc.hit.edu.cn`. The colophon @35890–36380 reads "CAJ-CD B/T 1-2006 / 中国学术期刊(光盘版)检索与评价数据规范 / 中国学术期刊(光盘版)编辑委员会 制定 … 印发 … 1999年1月第1版 2006年6月第7次印刷", consistent with the title and unused by the row.

## 3. `citation-count-semantics-r37.md` sentences citing S101

- `:5` "sections 11 and 14 (OLE .doc; UTF-16LE text of the raw capture)" — **narrower**: the bullet it heads also quotes §15.7 @34374, which the line does not name (the registry anchor does).
- Obs ¶2 "It assigns each article a 文献标志码 — … — whose stated purpose begins 为便于文献的统计和期刊评价" — **supported** @11166–11230; "each article" narrows 每一篇文章或资料 (the quote itself carries it).
- Obs ¶2 "its reference elements include 文献类型及载体类型标志" — **supported** @12161 (§14.2 c).
- Obs ¶2 "for reference format it says 本规范推荐采用GB/T 7714…作者-出版年制。 (it recommends, rather than defers to, the GB/T 7714 formats; a later parameter table reads 参考文献格式，参照ISO 690)" — **supported** @11945–12047 and @34370/34383; "later" is true (§15 after §14).
- Inf ¶4 "S101 sets a per-article code for statistics and evaluation … and recommends a reference format" — **supported** (same offsets; the rest is marked Inference, and §15.6 @34334 "文章总篇数，为发表在本期中具有文献标志码的文章的总和,据此计算载文量" carries the code→count link).
- Unknown "Whether the specification copy (S101) is the version in force …" — **supported as open, narrower than the capture**: the copy self-identifies CAJ-CD B/T 1-2006 and a 2006 7th printing @35890–36380; unused, so "in force" correctly stays open but the self-identification is available.
- Unknown "the register quote that put 'GB/T 7714' into the parameter-table sentence is absent as written; the capture says ISO 690 there and GB/T 7714 in section 14" — **supported, with an omission**: §15.7 has GB/T 7714 count 0, ISO 690 @34383; GB/T 7714 @12013/12040 in §14.1 — but §14.4 @13249 also says "参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以'.'结束", so §14 is not ISO-free and the ISO/GB contrast is thinner than the capture (W1 `GroundS102.md` q3: register string 0 occurrences — the absent-as-written verdict itself holds).

## 4. Context consistency (quote vs surrounding capture)

Measured: ±80-char window clipped at bare CR; `CR_in_span=False`, `LF_in_span=False` for all five; left/right = 39/80, 4/80, 80/80, 48/0, 4/80 (char before span start is `\r` for rows 1,2,4,5). The post-freeze CR clip therefore cannot corrupt these rows for `Path.read_text`'s universal-newline read, and every span is still an exact slice.

- S101-1/2 (11.6): span carries the purpose clause, the requirement and the head of the A–E list; "stated purpose begins" is exact (the clause continues "，确定文献的检索范围，提高检索结果的适用性"). Consistent.
- S101-3 (14.2 c): span starts mid-word ("…论文集主编、学位申报人…" → "主编、学位申报人…"), cutting item a. in half; it shows b–g and the quote is item c. "elements include" is supported, but h/i are outside the span, so the teaches "nine" cannot be re-derived from this span alone (it is derivable @12220–12300). Minor span-start defect.
- S101-4 (14.1): span is exactly the quoted sentence, 0 right context (next char `\r`) — nothing suppressed.
- S101-5 (15.7): the span *does* carry "，采用1位字母：n——顺序编码制（Numeric references method）；d——作者-出版年制（First element and date method）。", showing the parameter's letters select the same two methods §14.1 names; with §14.4's ISO 690/690-2, the ISO/GB split is provenance, not conflict. No quote is reversed against its context; the entry's framing is thinner than its own span, and it labels the "ISO-versus-GB/T reading" as the staged one.

## Cross-checks run

Frozen counter, `TMPDIR` set, lane checkout: `CAPTURE_BOUND=28/28`, `ANCHOR_BOUND=8/8`, `QUARANTINE_VERDICTS=5/5 (S082,S084,S086,S095,S096)`, `C2=PASS`, `EXIT=0` (also `BOUND=8/9 REFUSED=1 REF_ID_UNBOUND=0 QUOTES_IN_SPAN/ENTRY/LESSON=28/28`). Its anchor leg recomputes quote offsets as `offset+span.find(quote)` and requires every `char N` in that set — the S101 anchor is genuinely checked.

## Risks / calibration notes (none fatal to the row)

1. Entry source line `:5` omits §15.7 although the bullet quotes it (narrower, not false).
2. Unknown's ISO/GB contrast omits §14.4's "参照ISO 690及ISO 690-2" and the copy's CAJ-CD B/T 1-2006 self-id.
3. S101-3's span starts mid-word; teaches "nine" is span-external (verified @12049–12300).
4. Source cell's "hosted by 哈尔滨工业大学" is URL-derived, not capture text (0 hits for 哈尔滨).
5. W1 seat titles are crossed: `GroundS101.md` grounds the zcmu doc (lane S100) under "lane S101", and `GroundS102.md` grounds this hit.edu.cn doc under "lane S102". Landed row and lesson table are correct.

VERDICT: lane row S101 (journal data-specification OLE .doc) — holds — all five span rows recompute as exact UTF-16LE `.raw` slices with once-only quotes at the five anchor offsets, and every S101-citing sentence of `citation-count-semantics-r37.md` is supported by the capture (two narrownesses: the `sections 11 and 14` source line omits the §15.7 it quotes, and the ISO/GB contrast omits §14.4's ISO 690 reference); no quote is reversed against its context.
