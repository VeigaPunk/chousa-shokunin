# GroundS097 — re-ground staged row S088 (lane id S097) on capture 167e9db7dde3c998838e3469

Seat: GroundS097 (scribe). Wave: chousa-r49-w1. Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin.
Scope: re-ground the J-STAGE publisher page row S088→S097 by document, draft the Gate block,
per-claim verdicts for the staged entry, and the anchor cell. No files written outside this
report; no scratch dir created; no tool installed (RULES.md read: /home/vgpnk/.omp/agent/RULES.md:1-14;
no install needed — python3 only).

## 1. Commands run and observed output

(a) Capture identity — key matches sha256(full URL)[:24]:

```
$ python3 - <<'EOF'
import hashlib
url = 'https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja'
print(hashlib.sha256(url.encode()).hexdigest()[:24])
EOF
167e9db7dde3c998838e3469
```

(b) File type/encoding (both forms are UTF-8; the .raw is NOT UTF-16LE, so the .txt is the
clean text form and the .raw is the HTML form):

```
$ file .../167e9db7dde3c998838e3469.txt .../167e9db7dde3c998838e3469.raw
...txt: Unicode text, UTF-8 text, with CRLF, LF line terminators
...raw: HTML document, Unicode text, UTF-8 text, with very long lines (723), with CRLF, LF line terminators
$ stat -c '%n %s bytes mtime=%y' .../167e9db7dde3c998838e3469.txt
...txt 15656 bytes mtime=2026-10-23 20:33:32.773205668 -0300
```

(c) Quote location, uniqueness, and fit (in the .txt form; each quote also unique in the .raw):

```
$ python3 - <<'EOF'
txt = open('.../167e9db7dde3c998838e3469.txt', encoding='utf-8').read()
raw = open('.../167e9db7dde3c998838e3469.raw', encoding='utf-8').read()
cands = {
 'A': 'DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。',
 'B': 'J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます。',
 'C': '引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます。'}
for n,q in cands.items():
    print(n, 'len', len(q), 'words', len(q.split()),
          'txt count/first/last', txt.count(q), txt.find(q), txt.rfind(q),
          'raw count/first', raw.count(q), raw.find(q))
EOF
A len 49 words 1 txt count/first/last 1 2607 2607 raw count/first 1 26949
B len 40 words 1 txt count/first/last 1 2804 2804 raw count/first 1 27702
C len 55 words 1 txt count/first/last 1 2789 2789 raw count/first 1 27687
```

Each quote: ≤25 whitespace words, ≤160 characters, occurs EXACTLY ONCE in each form.
Form used for offsets: `.txt` (clean text; quote bytes are identical in `.raw`).

(d) Absent-defect register — no row names this URL:

```
$ grep -n 'jstage\.jst\.go\.jp/static/pages/ForPublishers/TAB2' .../absent-defect-register.md
(no matches)
$ grep -ni 'jstage' .../absent-defect-register.md
(only rows for OTHER URLs: S065 jstage result/global, S084 jstage .../FAQs/TAB2/-char/ja, S104 jstage article/kenkokyoiku — none is this URL)
```

(e) Supporting terms for the registry row's extra clauses (sections 11 and 14):

```
"Portico" txt count 5 first 5457; "iThenticate" count 1 first 6346
```

## 2. Draft Gate block for lane row S097

- row: S097 (staged S088, renumbered)
- URL: https://www.jstage.jst.go.jp/static/pages/ForPublishers/TAB2/-char/ja
- capture: .qcache/167e9db7dde3c998838e3469.txt (text form; also .raw)
- access date: 2026-10-25
- sections read: 1 (DOI登録機能), 2 (引用・被引用文献リンク機能), 11 (ダークアーカイブ), 14 (J-STAGE類似性チェックサービス)
- located quotes (verbatim, byte-exact from the capture .txt):

  | # | section | quote | chars | words | .txt offset | .raw offset |
  |---|---|---|---|---|---|---|---|
  | Q1 | 1. DOI登録機能 | DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。 | 49 | 1 | 2607 | 26949 |
  | Q2 | 2. 引用・被引用文献リンク機能 | J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます。 | 40 | 1 | 2804 | 27702 |
  | Q3 | 2. 引用・被引用文献リンク機能 | 引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます。 | 55 | 1 | 2789 | 27687 |

  Q3 is the middle clause of the sentence at .txt line 589; the full sentence adds the
  qualifier "J-STAGEが連携している外部サービスに登録されている" before it and the
  PubMed/CAS clause after it.

## 3. Per-claim verdicts (claims in the staged entry resting on S088)

Entry: merge/chousa/knowledge/corpus/knowledge/aggregator-vs-source-r36.md (source line 5 names
S088; sections 1, 2, 11, 14).

1. "J-STAGE states that DOI links to citation and cited-by works are created 'from a few days
   to two weeks after' the article is published" (Observation bullet 3) — **supported** by Q2
   (also Q3). Narrower in one respect: the capture restricts the delayed DOI-link creation to
   citations/cited-works registered in the external services J-STAGE links to
   ("J-STAGEが連携している外部サービスに登録されている引用文献および被引用文献には、…数日～2週間後にDOIによるリンクが作成されます", .txt line 589), and states the links are *displayed* already when the article is published ("J-STAGEで記事が公開されると、引用文献および被引用文献へのリンクが表示されます", same line). The registry row S097 teaches cell already carries this qualifier ("for works registered in the external services J-STAGE links to"); the entry's Observation paraphrase omits it.
2. "a DOI can only be used as a URL 1 to a few days after publication" (Observation bullet 3)
   — **supported** by Q1: "DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。" (section 1 note, .txt line 565). "can only" is the entry's framing of "usable only after 1 day–a few days"; the capture's fact is the delay.
3. Inference bullet: "it may be evidence that the index is two weeks behind" — **supported** by Q2 (the 数日～2週間 window).
4. Registry row S097's extra clauses (not in the entry): Portico dark archive (section 11, "Portico" at .txt offset 5457) and iThenticate similarity screening (section 14, "iThenticate" at .txt offset 6346) — **present** in the same capture.

No claim resting on S088 is not supported by the capture.

## 4. Draft anchor cell for row S097

`1. DOI登録機能 char 2607; 2. 引用・被引用文献リンク機能 char 2804` (offsets = Q1/Q2 quote offsets in the .txt form; section headings as on the page; Q3 shares section 2, offset 2789).

## 5. Limits

- Access date 2026-10-25 is today's date; capture mtime is 2026-10-23 (no live fetch; L0 8d77e6c1 open).
- Quotes are unique substrings; no paraphrase was used; nothing was invented.

VERDICT: Re-grounded S088→S097 by document with three byte-exact, exactly-once quotes (text form offsets 2607/2789/2804, raw 26949/27687/27702); both timed claims and the temporal-blind-spot inference are supported (one scope qualifier noted), no register row names the URL, and the Gate/anchor draft is delivered.
