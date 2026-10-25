# R51GroundJahbsA — re-ground staged S126 (JAHBS 38(1) 2023, step 7)

Target: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`
Lane target path: `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`
Capture: `.qcache/34fcefc159bf2ebbd1e09540.txt` (+ `.raw`), URL `https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf`.
**Form used throughout: the `.txt` read as UTF-8, 25811 characters** (`len(open(p,encoding='utf-8').read())`).

## 1. Capture identity (observed)

```
$ sha256sum 34fcefc159bf2ebbd1e09540.pdf 34fcefc159bf2ebbd1e09540.raw 34fcefc159bf2ebbd1e09540.txt
fe6eae45a1b0efb6bf0f9c5047cf2e0982410f985cb825d5e8c3cd6f393c67a1  ...pdf
fe6eae45a1b0efb6bf0f9c5047cf2e0982410f985cb825d5e8c3cd6f393c67a1  ...raw   (7787275 bytes, starts b'%PDF-1.4')
065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b  ...txt   (25811 chars)
$ ls -la .../34fcefc159bf2ebbd1e09540.*   → pdf/raw/txt mtime Oct 23 20:40
```
`.raw` and `.pdf` are byte-identical; the `.txt` is a two-column text extraction whose reading order interleaves
left/right column lines. Page markers (10) span pages 60–69, matching the staged citation.

## 2. The staged "step 7" attribution is correct — structural proof

Heading offsets in the `.txt`: `７．検索戦略を立案する` at 5258 (the 14-step list) and **10242** (the body heading);
`８．含める研究を選択する` at 5285 / **12588**; `６．レビュープロトコルへ…` at 5220 / **11023**.
Page markers: `…60－69  63` at 8822, `64 剱持・岡…` at 11372 → the body step-7 heading (10242) is on **p.63**, and the
row that carries the section-6 heading is column-interleaved:

```
'６．レビュープロトコルをレジストリへ登録する            PsycINFO などの専門データベースを検索すること'
```

i.e. left column = §6, right column = step 7. The Ovid/dates sentence sits in that **right column** (11229–11450), between
the step-7 and step-8 headings → it is inside step 7, not §6. The second sentence (`検索が終了した後は…`, 12105–12200) is in
step 7's p.64 right column, which runs on until the step-8 heading at 12588. **Staged placement: supported.**

## 3. Located quotes (each exactly once in the stated form)

- **11229** `検索した文献データベース名，Ovid などのプロバ` — supports: the record carries *the database name searched*
  and *a provider name, with Ovid as the example*. Does **not** support a requirement verb, a date, or a named provider list.
- **11289** `イダー名，検索の開始日と終了日を記載することで，` — supports: provider name (tail) + **search start and end
  dates** to be recorded. Does **not** support per-database dates, a date format, or a mandatory verb.
- **11348** `最新の結果を反映しているかどうか，更新がされて` — supports: the **currency rationale** — whether the newest
  results are reflected and whether the search has been updated. Does **not** support "latest *work*" (`最新の研究` appears
  nowhere) or an obligation to update.
- **11450** `いるかどうかの評価がしやすくなる８）。` — supports: the sentence's force is *evaluability* ("makes evaluation
  easier"), a cited recommendation (ref. 8), not a stated requirement.
- **10473** `使用するデータベースについて詳細に報告する` — the neighbouring sentence carries the only `必要がある` about
  databases: *reporting which databases were used in detail*. Does **not** support the three named fields as such.
- **12105** `検索が終了した後は，検索したデータベース名，` — supports: a second, separate step-7 sentence that lists the
  record as **database name + date searched + keywords and search formula + number of hits**.
- **12179** `検索した日，検索キーワードと検索式，検索件数を` — supports those three extra fields (absent from the staged entry).
- **10184** `表の資料や抄録を含めるかなど）を明記することが` — supports: `検索期間` **is** named with a requirement verb
  (`求められている`, PRISMA-P items, §5 protocol). This is where "must" can legitimately be grounded.
- **11805** `どを，あらかじめ記載する必要がある３）。その他に` — supports: in step 7 itself, `完全な検索式と言語制限や
  検索期間` must be stated in the protocol (`必要がある`).
- **158** `システマティックレビューとメタアナリシスの実施方法` — supports: the **article** is a methods article. Does
  **not** support "methods journal" or "peer-reviewed".

### Machine lines

```
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した文献データベース名，Ovid などのプロバ	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	イダー名，検索の開始日と終了日を記載することで，	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	最新の結果を反映しているかどうか，更新がされて	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	いるかどうかの評価がしやすくなる８）。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	使用するデータベースについて詳細に報告する	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索が終了した後は，検索したデータベース名，	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した日，検索キーワードと検索式，検索件数を	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	表の資料や抄録を含めるかなど）を明記することが	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	どを，あらかじめ記載する必要がある３）。その他に	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	システマティックレビューとメタアナリシスの実施方法	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

## 4. Staged claims about S126 that the capture does not carry

1. **"A peer-reviewed Japanese methods journal"** — the capture never says this journal is peer-reviewed. All three
   `査読` occurrences are elsewhere: 5982 `PRISMA 声明の準拠を求める査読付き雑誌` (generic, about journals requiring PRISMA);
   13481/13558 `査読者から「検索式は専門の司書に相談したか」` (the authors' *prior* submission, journal unnamed). `peer`,
   `ピアレビュー` = 0 occurrences. Venue is 日本保健医療行動科学会雑誌 (a health-behavioural-science society journal), so
   "methods **journal**" mis-describes the *journal*; only the *article* is methods (quote at 158).
2. **"The record must carry …" / "requires the database, the provider and the window"** — the three-field sentence has no
   requirement verb; its force is `記載することで…評価がしやすくなる` (11450). The only requirement verbs nearby attach to
   *reporting databases in detail* (10473 `必要がある`) and to `検索期間` in the protocol (10184 `求められている`, 11805
   `必要がある`). "must" is an upgrade of the staged sentence; it is groundable only via 10184/11805, which the entry does not cite.
3. **"whether the results reflect the latest work"** — capture says `最新の結果` (latest *results*), not `最新の研究`.
4. **Fields the capture carries and the entry omits**: `検索した日`, `検索キーワードと検索式`, `検索件数` (12105/12179), and
   the stated purpose `再現性を担保する` with the fields shown `後に論文中または付録等で` (step 7, p.64 right column).
5. **Attribution flag for the integrator (not resolved here)**: the entry's Inference says "a per-database date (the Japanese
   form)". S126 step 7 itself carries `検索した日` per database searched (12179). I did not open S125, so I do not rule on the
   S125 side; the integrating seat should decide whether the per-database date belongs to S126, S125, or both.
6. **Citation form**: capture mastheads read `38（1），2023` and `60－69` with U+FF0D (`0xff0d`), `60－69` occurring 10 times;
   the staged ASCII `38(1)` / `60–69` is a normalisation, not a mismatch of substance. Page span 60–69 confirmed by the
   ten page markers.
7. **Q12 (searcher identity)**: `検索者` = 0 occurrences in the `.txt`. This supports the staged "the searcher's identity
   appears in neither" **as term-absence in this text form only** — a PDF extraction can drop text, so absence here is not a
   statement by the document.
8. **Recheck string**: `検索の開始日と終了日を記載することで` occurs exactly once, at 11294 — the staged `recheck:` string
   is a valid pin for this document. The `recheck` also pins `SRにおける文献検索期間について明記する`, which is **not** in this
   capture (`SRにおける文献検索期間` = 0); it belongs to S125 and cannot be checked from S126.
9. **14-step procedure**: supported — the list at 5016–5459 has exactly 14 numbered items. Note the list's item 14 is
   `14．論文へまとめる` while the body heading (21656) is `14．論文へのまとめ`; harmless, but the entry should not quote a
   single form as if it were the only one.

## 5. Commands run (all read-only; no scratch dir created, nothing to delete)

```
$ python3 -c "len(t)"                                          → 25811
$ python3 … t.count(q) for every quote above                   → 1 for each (single occurrence)
$ python3 … t.find(q)                                          → offsets printed in §3
$ python3 … [m.start() for m in re.finditer('７．検索戦略を立案する',t)] → [5258, 10242]
$ python3 … re.finditer('\x0c',t)                              → page markers 3007,5470,8822,11372,14703,15511,16818,19148,21910,25810
$ python3 … t.count('検索者') → 0 ; t.count('査読') → 3 ; t.count('peer') → 0 ; t.count('60－69') → 10
```
No file under `chousa-shokunin`, `shokuknow`, or the fleet repo was modified. No pacman/install action taken (none needed).

VERDICT: attacked the staged S126 claims against the on-disk `.txt` — step-7 placement, the database/provider/window trio and
the currency rationale all hold verbatim, while "peer-reviewed methods journal", the "must/requires" force, "latest work", and
the omission of `検索した日`/keywords/hits are staged claims the capture does not carry.
