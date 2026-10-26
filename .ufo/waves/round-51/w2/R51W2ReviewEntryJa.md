# R51W2ReviewEntryJa — attack on `corpus/knowledge/japanese-search-record-r38.md` against QUALITY 1–86 and PROVINCE

Seat: `R51W2ReviewEntryJa` (leaf reviewer, `/skill:godspeed`). Date: 2026-10-25.
Boundaries: read-only on lane, fleet and `/home/vgpnk/Projects/shokuknow`; no scratch directory created; no tool installed or upgraded (`/home/vgpnk/.omp/agent/RULES.md` read, pacman guard respected); no network or live fetch (L0 `8d77e6c1` open).
Decode form (QUALITY 76): every `char N` below indexes the on-disk capture's `.txt` read as UTF-8 (`7194acc65a18f6555e4b8893.txt` for S107, 21,216 chars, sha256 `05c7ee9fe9e55461…`; `62be15a474e866e4bef6c9d5.txt` for S108, 39,676 chars, sha256 `960da5cf632dbd27…`).

## 1. Commands & observed outputs

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ grep -o 'S[0-9]\{3\}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/japanese-search-record-r38.md | sort | uniq -c
     11 S107
     13 S108
$ cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print([ja.count(w) for w in ['標準','規格','JIS']], [cn.count(w) for w in ['標準','規格','JIS']])" && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print([ja.count(w) for w in ['失敗','エラー','未実施','不完全','中断','実行でき']], [cn.count(w) for w in ['失敗','エラー','未実施','不完全','中断','実行でき']])" && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print([ja.count(w) for w in ['履歴','エクスポート','書き出し','出力','保存']], [cn.count(w) for w in ['履歴','エクスポート','書き出し','出力','保存']])" && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print([ja.count(w) for w in ['改訂']], [cn.count(w) for w in ['改訂']])"
[0, 0, 0] [0, 0, 0]
[0, 0, 0, 0, 0, 0] [0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0] [0, 0, 0, 0, 0]
[0] [0]
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ bash tools/research-gate.sh verify-metadata corpus/knowledge/japanese-search-record-r38.md --root . --as-of 2026-10-25 --registry corpus/SOURCES.md
META entry=japanese-search-record-r38.md source=present verified_at=dated recheck=scheduled due=2027-10-25 freshness=current verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
$ python3 tools/inference-ground.py --entry corpus/knowledge/japanese-search-record-r38.md --spans corpus/evidence/round51/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/japanese-search-record-r38.md section=1 bullets=4 tokens=10 grounded=10
GROUND: PASS
$ python3 corpus/evidence/round29/prose-check.py corpus/knowledge/japanese-search-record-r38.md
FILE corpus/knowledge/japanese-search-record-r38.md | digit-glued tokens: 0 | custody vocabulary: 0 | TOTAL hits=0 files=1
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py | tail -n 6
SUBSTANCE=PASS
ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
```

## 2. Applicable QUALITY criteria (1–86) vs `corpus/knowledge/japanese-search-record-r38.md`

- **Q6 (Provenance trio first) — MEETS (`:3-6`, `corpus/SOURCES.md:117-118`), with one recheck-runnability defect under Q13/Q57 below:**
  - `source:` lines (`:3-4`) name `S107` and `S108`, both `mined` (`opened: 2026-10-25`) in `corpus/SOURCES.md:117-118` with `used-by: corpus/knowledge/japanese-search-record-r38.md`, exact URLs, section/item anchors, capture paths, character counts, sha256 prefixes and `char` offsets.
  - `verified-at:` (`:5`) gives ISO date `2026-10-25` plus what was checked (`both captures re-read from the campaign cache; every quote below re-located with text.find; no fetch — L0 8d77e6c1 open`).
  - `recheck:` (`:6`) starts with cadence `365d` (`verify-metadata` → `recheck=scheduled due=2027-10-25 verdict=clean`).
- **Q13 & Q57 (`recheck:` command runnable as written; no live fetch under open L0 `8d77e6c1`) — FAILS (`:6`, `:28-30`):**
  - `:6` reads: `recheck: 365d — re-download both and confirm その日時，使用した検索式を同時に記録しておく (char 10234) and 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。 (char 4409) are unchanged, and re-run the four sweeps in #### Unknown (ran 2026-10-25)`.
  - **Defect 1a (`:6`):** `recheck:` is English prose ("re-download both and confirm … and re-run the four sweeps in `#### Unknown`"), not a directly runnable shell command, and "re-download both" instructs a live network fetch while L0 `8d77e6c1` is open (`:5`).
  - **Defect 1b (`:27-30`):** Only the first `#### Unknown` bullet (`:27`) carries a runnable command (`cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache && python3 -c "…"`). Bullets 2–4 (`:28-30`) write `Sweep: the same two-file command over ['失敗',…]`, `['履歴',…]`, and `['改訂']` — prose substitutions that a reader must manually splice into `:27`'s command. Reconstructed and run above, all four print their stated `[0, …]` outputs and both `:6` quotes sit at `10234` and `4409`.
- **Q1, Q2, Q30, Q72, Q76 (Falsifiable claims; exact anchors; quotes name location & decode form) — FAILS on two off-by-one/off-by-11 offsets in `:12` (`:3-4,12-16,27-31` otherwise MEET):**
  - Both `source:` lines (`:3-4`) state the decode form (`capture .qcache/….txt read as UTF-8`).
  - **Defect 2 (`:12`):** Bullet 1 of `#### Observation` writes:
    ``the copy reads `このプロセスに際して，誰が検索を行ったの` at the foot of the left column (char 13721) and continues at the head of the right column `か，その日時，使用した検索式を同時に記録しておく` (char 10234) `とが望ましい．` ``
    Measured in `7194acc65a18f6555e4b8893.txt` (UTF-8):
    ```
    $ python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); print(t.find('このプロセスに際して，誰が検索を行ったの'), t.find('誰が検索を行ったの'), t.find('か，その日時，使用した検索式を同時に記録しておく'), t.find('その日時，使用した検索式を同時に記録しておく'), t.find('とが望ましい．'))"
    13710 13721 10232 10234 10301
    ```
    `このプロセスに際して，誰が検索を行ったの` starts at **char 13710** (`13721` is the offset of the shorter substring `誰が検索を行ったの`), `か，その日時，使用した検索式を同時に記録しておく` starts at **char 10232** (`10234` is `その日時，…` without `か，`), and `とが望ましい．` starts at **char 10301** (no offset printed next to the backticked quote; only `望ましい, char 10303` is given). `corpus/lessons/round-51.md:97-100,108-110` records the true offsets (`10232`, `10234`, `10301`, `13710`, `13721`), proving `:12` attached the shorter substrings' offsets to the longer spans.
  - All other located quotes in `:3-4,12-16,27,30,31` match `t.find(q)` with `t.count(q) == 1`:
    S107: `10303` (`望ましい`), `10314` (`研究の透明性を保ち，他者`), `10370` (`が同様の検索を再現できるようになる`), `12666` (`PRISMA は，日本語を含め`), `12732` (`言語に翻訳されている`), `12807` (`報告すべき内容のチェックリストも付録されてい`), `12873` (`るため，使いやすさという点でも考慮されている．`), `17398` (`本健康教育学会誌にもシステマティックレビューの投`), `18441` (`PRISMA-ScR`).
    S108: `809` (`機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)`), `1498` (`更新版であれば更新した旨を記載する`), `3966` (`全てのデータベース`), `4124` (`それぞれのデータベース毎に最後に検索した日の日付を記載する。`), `4192` (`それぞれの情報源が最後に調べられた`), `4211` (`ハンドサーチの有無を記載する。`), `4311` (`検索戦略`), `4409` (`検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。`), `36834` (`検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。`), `36844` (`実際に使用した`), `36859` (`同等の詳細なもの`).
- **Q3, Q8, Q66, Q67, Q69, Q79 (Observation / Inference / Unknown separation; support states; CJK inference grounding; no polarity flip) — FAILS on one overstatement in `:20` (`:10-31` otherwise MEET):**
  - `tools/inference-ground.py` passes (`bullets=4 tokens=10 grounded=10`, exit 0). Lane pointers in `:22-23` (`corpus/README.md:390-391`, `SKILL.md:482-487`, `corpus/knowledge/chain-resolution-r3.md:145-147`) were opened and match what `:22-23` states.
  - **Defect 3 (`:20`):** Inference bullet 1 quotes `実際に使用した` or `同等の詳細なもの` (`36834`) and then concludes: `— the rule is about what was typed, not a reconstruction of it (S108).` That clause carries over the unnarrowed staged wording (`R51GroundJaohfaA.md:60`, `R51ReviewProvince.md:63`) and contradicts `もしくはそれと同等の詳細なものであること` ("or something of equivalent detail"), which explicitly permits an equivalent-detail reconstruction.
- **Q4, Q5 (Append-only errata; rejections kept) — MEETS (`:7,31`):**
  - The four staged errors (p.121 / `1次情報の「収集」` anchor, unsourced PRISMA-S/Cochrane sentence, body-only staged id `S105`, and unspaced `(V)-4`/`(V)-5`) are explicitly recorded and explained in `:7` and `:31` rather than silently dropped.
- **Q7 (Scoped tier) — FAILS on S108's tier in `corpus/SOURCES.md:118` and on `:16`:**
  - **Defect 4 (`:16`, `corpus/SOURCES.md:118`):** In `merge/chousa/SOURCES.append.md:34-35`, both staged S109 and S110 were `tier: B` (`R51ExecAdopt.md:43`); `corpus/SOURCES.md:117-118` upgraded both S107 and S108 to `tier: A`. S108 is an industry trade association's notification manual (`一般社団法人 健康食品産業協議会`) for functional-foods filings, not a primary research-method standard (`:27` itself states `Neither copy is a national or academic standard… S108 is an industry body's 留意点`). And Observation bullet 5 (`:16`, **What this copy is.**) is carrier/edition metadata (title, association + three cooperating bodies, running header `2026年6月5日 第２版` at chars 142, 28260, 35891) that belongs in `SOURCES.md` provenance (`:4`), not as a method observation (`R51ReviewProvince.md:57`).
- **Q9, Q37, Q74 (Counts carry their command and reconcile) — FAILS on uncommanded adjacent-word counts in `:16,27-28,30-31`:**
  - The four negative-sweep arrays in `:27-30` carry a command (`:27`), and `:3-4` character counts (`21,216`, `39,676`) match `len(open(...).read())`.
  - **Defect 5 (`:16,27-28,30-31`):** Prose counts in `:16` (`chars 142, 28260 and 35891`), `:27` (`The four ガイドライン hits in S107 … S108's two`), `:28` (`アクセス (5 in S107, 1 in S108)` and `検索でき (3 in S107, 0 in S108)`), `:30` (`S108's 更新 hits`), and `:31` (`char 297 and one other occurrence`, `PRISMA-S occurs once … Cochrane occurs as a database name`) carry no counting command in the entry. All were verified exact by command:
    ```
    $ cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print({w:(ja.count(w),cn.count(w)) for w in ['ガイドライン','アクセス','検索でき','PRISMA-S','1 次情報の「収集」','2026年6月5日 第２版']})"
    {'ガイドライン': (4, 2), 'アクセス': (5, 1), '検索でき': (3, 0), 'PRISMA-S': (1, 0), '1 次情報の「収集」': (2, 0), '2026年6月5日 第２版': (0, 3)}
    ```
- **Q10, Q23, Q26 (No placeholders; no digit-glued/custody prose; no unbacked `live`) — MEETS (`:1-31`):**
  - `prose-check.py` prints `TOTAL hits=0`; `grep -nwi live` and template-slot `grep` both return 0 hits (`rc=1`).
- **Q25, Q59 (Quarantine register rows named with capture form) — MEETS (`corpus/lessons/round-51.md:77-80`):**
  - Register rows `S104` (S107 URL, two-column split) and `S105` (S108 URL, two-column interleave + English splice) are both re-verified `absent-as-written` in `corpus/lessons/round-51.md:77-80`.
- **Q77, Q82 (No body-only S-ids; `source:` ids only) — MEETS (`:3-4,12-23,27-28,30`):**
  - `grep -o 'S[0-9]\{3\}'` returns `11 S107` and `13 S108` only; staged body-only `S105` was replaced by `corpus/knowledge/chain-resolution-r3.md` (`:7,23,31`).

## 3. Province check (`PROVINCE.md:3-17`)

- **Core entry (`:1-15,18-26,28-31`):** **IN PROVINCE** (`search-strategy taxonomy` and `claim-vs-source verification`, `PROVINCE.md:6-7`). Recording who searched, when, and with what expression (`S107:12`), listing databases with per-database last-search dates and hand-searching presence/method (`S108:14`), filing searcher/words/expression on attachment `(V) -5` (`S108:15`), and contrasting reporting rules with what `verify-sweeps` and `verify-chain` can check (`:20-23`) are reusable deep-research method. Zero spillover into `kasegi`, `kengaku`, `kumitate`, or `kagi`.
- **Regulatory/carrier drift (`:16`, and phrasing in `:27`):** Observation bullet 5 (`:16`, **What this copy is.**) states the functional-foods notification title (`機能性表示食品制度の届出資料…`), the trade association (`一般社団法人 健康食品産業協議会`), its three cooperating industry associations, and the running header offsets (`142, 28260, 35891`). That bullet states no search-method fact — it is document-carrier / regulatory-context provenance already carried on `:4` (`source: S108`) and `corpus/SOURCES.md:118`. Unknown bullet 1 (`:27`) uses the same carrier facts properly to bound scope (`Neither copy is a national or academic standard`).

## 4. Verdict & exact lines to cut / narrow

- **Recommendation:** **`admit-with-narrowing`** (the C2 counter is frozen at `C2=PASS`; any edit to `:16` must preserve the located quote `機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)` on `:4` or `:27` so `QUOTES_IN_ENTRY=61/61` in `c2-count.py` stays green).
- **Exact lines to cut or narrow in `corpus/knowledge/japanese-search-record-r38.md`:**
  1. **Cut `:16`** (Observation bullet 5, `- **What this copy is.** …`, regulatory/carrier provenance duplicating `:4`) after moving its located title string `機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)` (char 809) into `:4` or `:27`.
  2. **Narrow `:6` (`recheck:`)** from `"re-download both and confirm …"` to a placement-independent local command over the cached `.txt` files (or state that live re-download is gated on L0 `8d77e6c1` closing) and make the four sweep lists in `:27-30` one self-contained command.
  3. **Fix `:12` offsets** from `(char 13721)` → `(char 13710; 誰が検索を行ったの at char 13721)`, from `(char 10234)` → `(char 10232; その日時，使用した検索式を同時に記録しておく at char 10234)`, and add `(char 10301)` after `` `とが望ましい．` ``.
  4. **Cut the tail of `:20`** (`— the rule is about what was typed, not a reconstruction of it (S108).`) and replace with `— the rule accepts either the exact string run or an equivalent-detail statement of it (S108).`
  5. **Add the counting command to `:28`** for the adjacent-word counts (`ガイドライン`, `アクセス`, `検索でき`).

VERDICT: Attacked `corpus/knowledge/japanese-search-record-r38.md` against QUALITY 1–86 and PROVINCE — `c2-count.py` (61/61), `inference-ground.py` (4/4 bullets, 10/10 tokens), `verify-metadata` (CLEAN), `prose-check.py` (0 hits), S-id hygiene (`11 S107`, `13 S108`, 0 body-only ids) and all 4 negative sweeps (`[0,0,0]`, `[0,0,0,0,0,0]`, `[0,0,0,0,0]`, `[0]`) hold; recommend **admit-with-narrowing** to cut Observation bullet 5 (`:16`, carrier/regulatory metadata), fix two substring-vs-span char offsets in `:12` (`13721`→`13710`, `10234`→`10232`, add `10301`), cut the `:20` overstatement `"not a reconstruction of it"` (contradicting `もしくはそれと同等の詳細なもの` at char 36834), and replace `:6`/`28-30`'s prose `re-download` / `"the same two-file command"` with runnable local commands.
