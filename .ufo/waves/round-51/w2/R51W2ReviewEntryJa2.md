# R51W2ReviewEntryJa2 — QUALITY 1-86 / PROVINCE attack on the Japanese amendment entry

Target: `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` (28 lines; blob `5973a968403051e4b89981bf110db60d4fce88e4`, byte-identical at `4436e279b91d8d68fd439c9095695035fbeeab74` and at `HEAD=72566c84e4184846ff9cbc4c92bc33b8291bc53b`; `git diff 4436e27 HEAD -- <file>` and `git diff HEAD -- <file>` both empty). Bar: `corpus/QUALITY.md` 1-86 and `PROVINCE.md`. Tooling: `RULES.md` read; pacman paused host-wide, 0 installs. Scratch `/dev/shm/chousa-r51-R51W2ReviewEntryJa2` (removed). No fetch (L0 `8d77e6c1` open).
Capture form for every `char N` below: `.qcache/34fcefc159bf2ebbd1e09540.txt` read as UTF-8, `len=25811`, `sha256=065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b` (re-derived).

## 1. Required commands, observed output

```
$ grep -o 'S[0-9]\{3\}' corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md | sort | uniq -c
     15 S112
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/build-spans.py --check
SPANS_ROWS=61 STALE=0
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf').hexdigest()[:24])"
f3dbe2fe59a684b1b94cfadc
$ ls .../.qcache/f3dbe2fe59a684b1b94cfadc*   -> f3dbe2fe59a684b1b94cfadc.fail    $ cat ... -> rc=28
$ python3 -c "import hashlib;k=hashlib.sha256(b'https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf').hexdigest()[:24];t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/'+k+'.txt',encoding='utf-8').read();print(len(t),[t.count(w) for w in ('検索者','検索担当','ハンドサーチ','灰色文献')])"
25811 [0, 0, 0, 0]
$ bash tools/research-gate.sh verify-metadata corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md --root . --as-of 2026-10-25 --registry corpus/SOURCES.md
META entry=japanese-search-record-r38-amendment-2026-10-23.md source=present verified_at=dated recheck=scheduled due=2027-04-23 freshness=current verdict=clean
METADATA_COMPLETE=1/1 ; RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)   [rc=0]
$ python3 tools/inference-ground.py --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md --spans corpus/evidence/round51/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md section=1 bullets=5 tokens=8 grounded=8
GROUND: PASS
$ python3 corpus/evidence/round29/prose-check.py <entry>            -> TOTAL hits=0 files=1
$ python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round51/spans.tsv -> IDS=6 QUOTES=61 FAILURES=0
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py
ENTRIES=3/3 BOUND=6/7 (min 5) REFUSED=1 BOUND_IDS=S107,S108,S109,S110,S111,S112 REF_ID_UNBOUND=0 NEW_GROUND=3/3 QUOTE_ROWS=61 ON_BOUND=61/61 SPAN_IDS=6/6 (min 3 each) QUOTES_IN_SPAN=61/61 QUOTES_IN_ENTRY=61/61 QUOTES_IN_LESSON=61/61 QUOTE_SHORT=61/61 SPAN_CONTEXT=61/61 CAPTURE_BOUND=61/61 SUBSTANCE=PASS ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120) QUARANTINE_BLOCKED_ADOPTED=0 C2=PASS
$ cd .../.qcache && python3 -c "t=open('34fcefc159bf2ebbd1e09540.txt',encoding='utf-8').read();print('peer',t.count('peer'),'pia',t.count('ピア'),'chakujou',t.count('査読'),'offsets',[i for i in range(len(t)) if t.startswith('査読',i)]);print('title',t.find('システマティックレビューとメタアナリシスの実施方法'))"
peer 0 pia 0 chakujou 3 offsets [5982, 13481, 13558]
title 158
$ python3 -c "t=open('34fcefc159bf2ebbd1e09540.txt',encoding='utf-8').read();qs=['求められている。こうした適格基準は','ロトコルには完全な検索式と言語制限や検索期間な','どを，あらかじめ記載する必要がある','検索が終了した後は，検索したデータベース名，','検索した日，検索キーワードと検索式，検索件数を','で再現性を担保する。','Page MJ, McKenzie JE, Bossuyt PM, Boutron I,','The PRISMA 2020 statement an','372: n71, 2021'];print({q:(t.count(q),t.find(q)) for q in qs});print('footnote8',t.find('８）。',11450))"
{'求められている。こうした適格基準は': (1, 10208), 'ロトコルには完全な検索式と言語制限や検索期間な': (1, 11730), 'どを，あらかじめ記載する必要がある': (1, 11805), '検索が終了した後は，検索したデータベース名，': (1, 12105), '検索した日，検索キーワードと検索式，検索件数を': (1, 12179), 'で再現性を担保する。': (1, 12329), 'Page MJ, McKenzie JE, Bossuyt PM, Boutron I,': (1, 23997), 'The PRISMA 2020 statement an': (1, 24684), '372: n71, 2021': (1, 24893)}
footnote8 11466
$ grep -l -a 'jahbs' *.txt -> (none)    $ grep -l -a '日本保健医療行動科学会雑誌' *.txt -> 34fcefc159bf2ebbd1e09540.txt
```

## 2. Provenance trio (criteria 6, 13, 57, 76) — checked first

- `source:` `:3` — S112, URL, seven anchors; `corpus/SOURCES.md:122` is `mined`, tier `A`, `used-by` names exactly this entry. MEETS 6/7.
- `verified-at:` `:4` — ISO date 2026-10-25, states cache re-open + `text.find`; I re-located all seven body anchors (table §3). MEETS 6; criterion 57 is PARTIAL (D4: the capture is named by path/key/length but not by its sha256), and the title phrase in `:3` has no stated offset (manifest row 55 gives char 158).
- `recheck:` `:5` — `180d`, cwd stated ("from the lane root"), command runs (above). MEETS 6/13. The `then re-download` clause is a 180d fetch, not runnable now under L0 (named limit, same convention as `japanese-search-record-r38.md:6`).
- Metadata gate: `RESEARCH_GATE: CLEAN`, `due=2027-04-23`; `grep -nwi live <entry>` rc1 (no hit).

## 3. Quotes: location, form, uniqueness (criteria 20, 30, 66, 72, 76)

| quote | char | count in .txt | entry line | lesson line |
|---|---|---|---|---|
| `システマティックレビューとメタアナリシスの実施方法` | 158 | 1 | :3 | :150 |
| `検索の特徴（検索期間` | 10140 | 1 | :11,:19 | :151 |
| `検索期間，言語制限` | 10146 | 1 | :11,:16 | :152 |
| `検索した文献データベース名` | 11229 | 1 | :12,:17,:20 | :153 |
| `Ovid などのプロバ` | 11243 | 1 | :12 | :154 |
| `検索の開始日と終了日を記載することで` | 11294 | 1 | :5,:12,:16,:17 | :155 |
| `最新の結果を反映しているかどうか` | 11348 | 1 | :12,:18 | :156 |
| `評価がしやすくなる` | 11457 | 1 | :12,:18 | :157 |

All are `.txt`-UTF-8, exactly once, ≤25 whitespace words and ≤160 characters (longest 24 characters); the 8 S112 rows are `corpus/evidence/round51/spans.tsv:55-62`, each span start = quote−80, and `c2` prints `QUOTES_IN_SPAN=QUOTES_IN_ENTRY=QUOTES_IN_LESSON=CAPTURE_BOUND=61/61`, `SUBSTANCE=PASS`. I also re-derived every offset with `text.find` (all equal the stated `char`).

## 4. Criteria 1-86 (applicable; `:N` is the entry unless another file is named)

- **1** PARTIAL — claims falsifiable; D2 (title) and D6 (`:18` clause) are the unmarked cases.
- **2** FAIL — D1 (`:1`,`:11`), D3 (`:27`), D4 (`:3-4`); all other claims carry anchors.
- **3** PASS — `#### Observation` :9, `#### Inference` :14, `#### Unknown` :22; the `:28` adoption-correction bullet follows the base entry's convention.
- **4** PASS — no erratum for this entry (`claims-erratum.md` E1 is C3).
- **5** PASS — refused NIPH form kept with URL and flip at `corpus/lessons/round-51.md:54-56`; `:7`,`:26`; no staged id in the entry.
- **6** PASS — trio §2; used-by exact; gate clean.
- **7** PASS — tier A, scope covers; the scope's `peer-reviewed` is D1.
- **8** FAIL — `:19` states the copy limit ("one society journal's methods article, not a national standard") while the title generalises; D2.
- **9** FAIL — D1's phrase is restated at `corpus/README.md:1091` and `corpus/SOURCES.md:122`; no owning line closes it.
- **10** PASS — `grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH' <entry>` rc1 (`:1-28`).
- **13** PASS — cwd stated, command ran (`:5`); fetch half is 180d (named limit).
- **20** PASS — every quote re-located in the `.txt` form and the gutter splits are named (`:12`); the span files are exact slices (c2).
- **23** PASS — prose-check `hits=0` (`:1-28`).
- **25** PASS-by-substitute — quotes were re-opened from the committed capture (`build-spans` + `c2` `CAPTURE_BOUND=61/61`; `:11-12`), not by `tools/quote-reopen.py` (fetch; L0 open); no ABSENT/UNREACHABLE verdict exists to record.
- **26** FAIL — D1.
- **30** PASS — all 8 manifest quotes are in the Gate set and verbatim; `QUOTES_IN_LESSON=61/61`.
- **37** PASS — 25,811 is re-derived by the entry's own `#### Unknown` sweep (prints `len`).
- **54** n/a — no counter claim in the entry (the title's support-state breach is D2 under 8/1).
- **57** PARTIAL — D4: no capture sha256 in the entry (sibling `japanese-search-record-r38.md:3` cites one; manifest row 56 holds `065b889a…`).
- **59** PASS for the refusal class — `lesson:54-56` names the capture (key), the form (`.docx`, `word/document.xml`) and a located quote (`:88`); the entry's `:26` names the form but carries no offset (residual §7).
- **66** PASS — `GROUND: PASS` 8/8 (`:16-20`).
- **67** PASS — no `INF_POLARITY_FLIP` (`:16-20`); CJK polarity is the tool's named limit.
- **72** PASS — `FAILURES=0`; no hollow quote (`:11-12`).
- **76** PASS — `:3` names `.txt` read as UTF-8 and the length; all offsets index that form.
- **77 / 82** PASS — `15 S112` only; no body-only or staged id (`:3-28`).
- **79** PASS — CJK bullets grounded 8/8 (`:16-20`).
- **11-12, 14-19, 21-22, 24, 27-29, 31-36, 38-56, 58, 60-65, 68-71, 73-75, 78, 80-81, 83-86** n/a — round, counter, tool, wave-spec, receipt and self-assessment criteria; this record is a knowledge entry.

## 5. Findings (severity; evidence; exact cut)

**D1 HIGH — `peer-reviewed` and `methods journal` are unsupported (QUALITY 2, 8, 9, 26).** `:11` says "A peer-reviewed Japanese methods journal"; `:1` says "a methods journal"; `README.md:1091` repeats it; `SOURCES.md:122` scope says "peer-reviewed". Sweep over the capture: `peer` 0, `ピア` 0, `査読` 3 at `[5982, 13481, 13558]` — `査読付き雑誌` at 5982 is generic ("PRISMA 声明の準拠を求める査読付き雑誌"), and `専門の司書に相談したか` at 13543 is a reviewer's comment on the authors' prior submission; no cache capture names `jahbs` (`grep -l -a 'jahbs' *.txt` empty) and only `34fcefc…txt` contains the journal name. The title at char 158 shows the *article* is methods, in a health-behavioural-science society journal; `:19` itself says "one society journal's methods article". W1 found this before landing (`R51GroundJahbsA.md:75-79`) and the landing did not fix it. **Cut:** `:11` "A peer-reviewed Japanese methods journal" -> "A Japanese methods article in one society journal"; `:1` "a methods journal" -> "a methods article in a Japanese society journal"; `README.md:1091` "a peer-reviewed Japanese methods journal" -> "a Japanese methods article in one society journal"; `SOURCES.md:122` scope "peer-reviewed Japanese methods article" -> "Japanese methods article". (Criterion 9: close all three in the same landing.)

**D2 MEDIUM — the title reports one article as "The Japanese search record" (QUALITY 8, 1).** `:1` "The Japanese search record carries a stated 検索期間: a methods journal reports it as a PRISMA-P item ..." generalises the single source and contradicts `:19` "This copy is one society journal's methods article, not a national standard". Also "as a PRISMA-P item" compresses the source's "17 items ... e.g. 検索の特徴" (the Inference at `:16` more accurately says "protocol element"). **Cut:** replace the title with "A Japanese methods article reports 検索期間 among the PRISMA-P protocol items and names the database, the provider and the window as record fields".

**D3 MEDIUM — `Unknown` `:27` overstates what is unestablished and leaves the sentence's citation unswept (QUALITY 2, 8, 59).** The sentence "Whether the article's three fields are a requirement or a recommendation of its authors was not established ... it cites no journal rule or standards body in the sentence read" is too broad on the capture: (a) the step-7 sentence's footnote marker `８）` sits at 11466, and reference 8 (list at 23997 `Page MJ, ...`; title `The PRISMA 2020 statement an` at 24684; `372: n71, 2021` at 24893) is the PRISMA 2020 statement — the sentence does cite a reporting standard, so "no standards body" survives only on a narrow reading and the footnote is never swept; (b) the same step's protocol sentence at 11730 `ロトコルには完全な検索式と言語制限や検索期間な` + 11805 `どを，あらかじめ記載する必要がある` requires 検索期間 in the protocol, and the quoted PRISMA-P sentence closes `求められている。こうした適格基準は` at 10208 (inside span S112-3) — so the window's requirement *is* established, though the database/provider trio's step-7 sentence is advisory. W1 supplied the requirement offsets (`R51GroundJahbsA.md:80-83`); the landing did not use them. **Cut:** replace `:27` with "Whether the step-7 three-field sentence is a requirement or a recommendation of its authors was not established: its verb is 記載することで…評価がしやすくなる and its footnote 8 is the PRISMA 2020 statement (reference 8, char 23997); the same step separately requires 検索期間 in the protocol (`あらかじめ記載する必要がある`, char 11805)." **D3b (depth, not a bar breach):** the same step's post-search list — `検索が終了した後は，検索したデータベース名，` at 12105, `検索した日，検索キーワードと検索式，検索件数を` at 12179, purpose `で再現性を担保する。` at 12329 — is omitted, so `:17` "incomplete by this article's list" should read "incomplete by that sentence" unless these are added (they would be new manifest rows; next round).

**D4 LOW — no capture digest in the entry (QUALITY 57).** `:3-4` name the capture path/key and length but not its sha256; `japanese-search-record-r38.md:3` cites `sha256 05c7ee9f…`, and `spans.tsv` row 56 holds `065b889a…`. `:4` "every quoted phrase ... at its stated offset" is true of the seven body quotes but not the title phrase (`:3`, manifest char 158). **Fix:** append `sha256 065b889a97b0…` to `:3`; say "every body quote" or add `(char 158)` after the title.

**D5 LOW — wrong ordinal in `adopted:`.** `:7` calls the NIPH form "the staged entry's second document"; the staged file's source lines are S125 (NIPH) at line 4 and S126 (JAHBS) at line 5 — the NIPH form is the first, and the adopted S126 is the second. **Cut:** "second document" -> "other document (staged S125, its first source line)".

**D6 LOW — an unbacked lane clause.** `:18` "The stated rationale is currency, and it is the lane's own recheck." The article's rationale is a reader's currency check; the entry's `recheck:` (`:5`) re-verifies quotes at 180d, not whether search results are current. **Cut:** ", and it is the lane's own recheck".

**Holds (attacked, not broken).** (i) All seven anchors and all eight manifest quotes are exact and unique; `c2` and `quote-substance` pass. (ii) `:20` "the article does not name who ran the search" survives: `検索者`/`検索担当` are 0; `司書` (5×, e.g. 11965, 13543) is a *consultant/constraint*, and the `誰が行ったかを記載することが求めら` at 15099 is PRISMA's **文献選択** (literature selection), not search execution — so the suspected overreach is falsified, not a defect. (iii) `:12`'s gutter claim is right: the quote at 11243 ends the left line with `プロバ` and `イダー名` opens the right; the three fields and the currency reason are in one sentence. (iv) The translation sweep and the 検索者 sweep reproduce exactly. (v) `SUBSTANCE=PASS`, `GROUND: PASS`, metadata gate clean, `C2=PASS`.

## 6. Province (`PROVINCE.md:5-8`)

IN province: every bullet (`:11-12`, `:16-20`, `:24-28`) is search-strategy taxonomy / claim-vs-source verification (record fields, PRISMA-P protocol items, currency rationale) and the searcher negative. Zero biomedical, regulatory or product-description drift: the staged NIPH HTA submission rule is refused at `:7`,`:26` and the entry states "not a national standard" (`:19`). No out-of-province absorption.

## 7. Residual risk / verification gaps

- `recheck:`'s fetch half not executed (L0 open); only the on-disk half was run.
- The Gate's S120 docx offset is form-dependent: W1 receipts give 8936 (`R51GroundNiphA.md:40`), 9729 (`R51CritTheme.md:87`), 10247 (`R51ExecCaptureForm.md:83`), 39411 (`R51ExecQuarantine.md:73`, `lesson:88`) on different extractions. I read the `.raw` as a zip in memory and confirmed the entry's `:26` content claim (`SRにおける文献検索期間について明記する` present in the joined `<w:t>` runs, 160571 in my form), but a reader cannot reproduce the Gate's 39411 from the entry; the entry itself carries no offset.
- QUALITY 25's literal `quote-reopen.py` was not run this round; the substitute capture re-open is receipted by the span manifest/counter.
- The C2 counter measures binding/presence, not entailment (`claims.md` R51-C2 limit); D3b is prose depth, not a counter cell.
- I did not re-run the round's full no-harm battery or other seats' counters; this report is the entry's slice only.
- At report time the worktree carries uncommitted edits to `tools/assimilate-rows.py`, `corpus/evidence/round51/c1-supplement.py` and `controls/c1-supplement-controls.txt` (not made by this seat; the entry, `SOURCES.md`, `spans.tsv`, `quotes.tsv`, `README.md` and `lessons/round-51.md` are clean, so the C2/inference/metadata evidence binds those bytes).

VERDICT: attacked `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` against QUALITY 1-86 and PROVINCE — in province, `S112`×15 only, all eight quotes unique/exact, recheck `SPANS_ROWS=61 STALE=0`, `GROUND: PASS`, `C2=PASS`; the central PRISMA-P/window claims hold, so **admit-with-narrowing**: cut D1 (`peer-reviewed`, `methods journal`; mirror README:1091, SOURCES:122), D2 (title's general clause), D3 (`Unknown` :27 requirement/citation), and apply D4-D6 metadata/precision fixes; no predicate, target, counter or control is proposed changed.
