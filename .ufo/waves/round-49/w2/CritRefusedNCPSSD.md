# CritRefusedNCPSSD — round 49 w2 (FALSIFY): the refused NCPSSD homepage row

Seat: CritRefusedNCPSSD (leaf; no subagents/background jobs; no network; no install — RULES.md
read, pacman paused, nothing needed). Read-only on lane and campaign cache; my only write is this
report. Scratch `/dev/shm/chousa-r49-CritRefusedNCPSSD` (TMPDIR exported for counters), deleted.
Objects read at tip `87e9335`: `corpus/lessons/round-49.md:131` (`refused-doc` row), `:115-118`
(register S086 verdict), `corpus/knowledge/aggregator-vs-source-r36.md:89-93` (NCPSSD Unknown
bullet). Both lesson lines and the bullet are byte-identical in the working tree, where they now
sit at `:133` and `:117-120` (two S096 span rows added); the entry's Observation/Inference is being
rewritten by another seat while I ran, so I quote the tip bytes and say where they moved.

## Capture identity — the two-URL premise is exact
```
sha256('https://www.ncpssd.cn/')[:24]                                  -> 76914d78c20094f677dea77d
sha256('https://ncpssd.org/service/help?mainTitle=常见问题')[:24]      -> c4e1446a42d0a709c34097be
grep -lF "谁有权限使用网站上的资源" .qcache/*.txt .qcache/*.raw
c4e1446a42d0a709c34097be.txt / .raw        # exactly one capture carries the FAQ body
```
Same institution on the help capture: `国家哲学社会科学文献中心` ×5, `中国社会科学院` ×5, `cass.org.cn` ×2;
the access-model text is only on the `常见问题` help page — "a different URL" is exact.

## Register S086 — absent from the cited capture, present in the companion
```
homepage (txt 15270 B, raw 197752 B): q1 0 / q2 0; 注册用户 0; 在线阅读 0; 免费 0; 全文下载 0; 仅对 0
help capture, byte-read + utf-8-sig, CRLF preserved (41495 chars): q2 find 24872 c1; q1 find 25269 c1
  q2 ctx: 4. 谁有权限使用网站上的资源？ …我们的网站是面向全社会，公益的，您注册成功后，可进行使用。
  q1 ctx: 7. 如何下载电子全文？ …我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务，外文期刊、古籍仅提供在线阅读服务…
help capture, text-mode open(encoding='utf-8-sig'), universal newlines (40831 chars): q2 24556; q1 24953
```
`round-49.md:117`'s "offsets 24872 and 25269" reproduces only under a CRLF-preserving byte decode
(text mode shifts both −316) and is unmapped to its quotes (q2@24872 item 4, q1@25269 item 7).

## The homepage capture is not "only a header and the builder line"
```
homepage .txt: 2249 lines, 569 non-blank, 7943 chars
中文期刊 82/241 | 外文期刊 84/249 | 集刊 88/263 | 外文图书 90/269 | 版权声明 123/425
在线咨询 127/437 | 使用指南 129/445 | 常见问题 131/453 | E-mail 2193/7700 | APP 2215/7807
请 登录 注册 110 c1 | 中国社会科学院图书馆承建 168 c1 | 公益 7388 c1 (= PubScholar公益学术平台 nav item)
```
Counterexample to `:131`'s reason: the bound capture carries the five-category 资源 navigation,
four 导航 blocks, search field labels, article listings and the footer (address, 邮编, 3 QR
blocks). The staged row's **own** anchor cell names "the site's 登录/注册 header and **资源
navigation**" (`merge/chousa/SOURCES.append.md:16`), so the reason omits content the staged row
did claim from this capture; the only 公益 is an external nav item, not a statement about NCPSSD.
The homepage links to `/service/help?mainTitle=使用指南` (`raw: service/help` ×3) and embeds no
FAQ body (`谁有权限` 0, `如何下载电子全文` 0, `我们的网站现有` 0 in raw), so even the raw form
cannot ground the staged claims.

## The Unknown bullet's "free" leg is an inference, not capture content
```
help capture: 免费 0 | 收费 0 | 费用 0 | 付费 0 | 公益 1 | 注册成功后 1
```
`aggregator-vs-source-r36.md:89-93` says the staged claims "(free after registration; full-text
download for registered users only; foreign journals and 古籍 online-reading only) **are in** its
help-page capture". Claims 2 and 3 track item 7's sentence (its 中文期刊论文 scope glossed as
"full-text"); claim 1 is stated nowhere — the page calls the site `公益的` and usable after
registration, never 免费. The bullet presents an inference as capture content and gives no capture
key, offset or URL (the key is two hops away in the lesson), so it is not re-openable from the entry.

## Refusal leg and verdict line sit outside every gate (probed on a scratch copy)
```
python3 corpus/evidence/round49/c2-count.py   (git archive 87e9335 -> scratch root)
BOUND=8/9 (min 7) REFUSED=1 ... QUARANTINE_VERDICTS=5/5 (S082,S084,S086,S095,S096)  C2=PASS exit 0
S086 verdict flipped to `fabricated`                                        -> C2=PASS
Unknown bullet + "NCPSSD holds 40 million records and is free for every visitor"
                                          -> C2=PASS; tools/inference-ground.py -> GROUND: PASS
```
`blocked` fires only when a fabricated/unverifiable register URL is also *bound*; the refused URL
never is. `REF_ID_UNBOUND`/`ANCHOR_BOUND`/`QUOTES_IN_*` are blind to a claim naming no `S###`, URL
or `char N`; `inference-ground.py` reads `#### Inference` only. This is declared scope
(`claims.md:58`: REFUSED = "no lane row, no `source:` line, and a `refused-doc` line naming its
URL"), not a violation — but it means both lines are human-checked only, and this report is that check.

## Answers
1. **Was refusing right?** Yes for what the row teaches. The staged entry itself attributes the
   access model to "its help" (`merge/chousa/.../aggregator-vs-source-r36.md:7,33-37`), and the
   staged row is a two-URL composite (homepage header+nav **plus** help items 3,4,7) that a
   one-URL registry row cannot represent; the statements occur in no homepage capture form.
2. **Could it have been bound narrowed?** Only on facts the staged `teaches` cell does not teach
   and no entry uses: `中国社会科学院图书馆承建` (char 168) and the 资源 nav (char 241+) — both
   unique. That is a re-scope to an identity/nav fact off the derived-index theme and would leave
   the access model exactly as ungrounded. The flip (help-page row) is the right route; note its
   capture is already on disk (`c4e1446a…`, both quotes verbatim), so the flip needs no fetch.
3. **`refused-doc` line accurate?** Cell 1 yes (staged S091 = the homepage URL; absent from
   `renumber.tsv`; no lane row; `REFUSED=1`). Decision yes. **Reason no** (section above). Flip
   cell valid. No namespace collision: lane `S086` is the FEVER row (`corpus/SOURCES.md:96`), so
   "register S086" cannot be misread as a lane row.
4. **Register S086 verdict line accurate?** Yes on substance: absent from the cited capture, both
   quotes verbatim in `c4e1446a…`, "Not fabricated" verified. Two calibration gaps: offsets are
   decode-dependent and unmapped to their quotes; and the register's own evidence cell — "companion
   URLs and local artifacts were all checked; the quote is in none of them"
   (`absent-defect-register.md:41`) — is **false**, which the line corrects by stating the presence
   but never names. Round-48 wrote `present` (`round-48.md:46`), round-49 writes
   `absent-as-written`; the scoping clause makes them consistent but does not reconcile the words.
5. **Any NCPSSD claim left in the entry?** Yes — the three staged claims plus the provenance
   assertion, all inside `#### Unknown` (89-93), unchanged by the concurrent rewrite. None in
   Observation/Inference, none in a `source:` line, no registry row, no span. The `adopted:` line
   (11) points to the Gate, so the refusal itself is disclosed.

## Smallest safe corrections (not applied; neither file is mine)
- `:131` reason → "carries no access-model statement; of the staged row's anchors only the
  登录/注册 header (char 110) and 承建 (char 168) occur; the 资源 navigation (char 241+) is
  present but states no access model."
- `:117-118` → name the decode ("byte read, utf-8-sig, CRLF preserved"), map the offsets
  (q2@24872 item 4, q1@25269 item 7), and say the register's companion-URL cell is false while
  its cited-URL verdict stands.
- `aggregator-vs-source-r36.md:89-93` → mark "free" as inferred and quote its basis
  (`我们的网站是面向全社会，公益的，您注册成功后，可进行使用。`; 免费 does not occur), and carry
  `c4e1446a42d0a709c34097be` + the two offsets so the assertion is re-openable.

## Axes and concurrent state
Calibration only: the reason cell overstates the capture's emptiness and the Unknown bullet
promotes an inference to capture content; both are human-checked, neither is gated. Operability
and depth are unaffected (refusal needs no tool; the eight bound rows carry the theme, `C2=PASS`
at the tip). Disclosure: while I ran, another seat modified the entry, `quotes.tsv`, `spans.tsv`,
several span files and the lesson; the live counter at write time is `QUOTE_ROWS=31 …
ANCHOR_BOUND=6/8 INFERENCE_GROUNDED=1/2 C2=FAIL` (real exit 1) — that seat's in-flight state, not
this seat's finding; the tip `87e9335` passes. Scratch deleted.

VERDICT: refusal of the staged NCPSSD homepage row — partly — the refusal and the register verdict hold (the access-model text is in no homepage capture; both quotes are verbatim in the help capture at 24872/25269), but the recorded reason ("only a 登录/注册 header and the builder line") is false against a 2,249-line capture that carries the 资源 navigation the staged row itself named, and the entry's Unknown bullet presents an inferred "free after registration" as help-capture content that no gate can see.
