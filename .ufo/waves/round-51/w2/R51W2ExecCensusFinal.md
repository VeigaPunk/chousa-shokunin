# R51W2ExecCensusFinal — census and registry integrity at the tip

Leaf seat: census/registry integrity only (C1/C2/C3 numerics are other w2 seats). Tip read `72566c8` = assignment tip
`4436e27` + wave-2 spec (`git merge-base --is-ancestor 4436e279b91d8… HEAD` exit 0). UTC clock `2026-10-26`, one day past
the round's `2026-10-25`; both clocks exercised. Nothing installed; commands in
`/home/vgpnk/Projects/shokunin/chousa-shokunin` unless stated.

## 1. Fleet census and validate (lane root)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
VALIDATE_EXIT=0      W04 lines=5      E-lines=0
$ ... validate --root ... chousa --today 2026-10-25 → same five W04 + ok, EXIT=0
$ ... census --root /home/vgpnk/Projects/shokunin chousa
chousa	rows 112	tier.A 98	tier.B 9	tier.C 5	status.mined 88	status.queued 19	status.rejected 5
FLEET rows 112 tier.A 98 tier.B 9 tier.C 5 tier.invalid 0 · status.queued 19 mined 88 rejected 5
FLEET status.invalid 0 FLEET missing 0 CENSUS_EXIT=0
```

W04 is pre-existing: validate over the base (`--file` on `git show 9ec1751:corpus/SOURCES.md`, `--today
2026-10-19`) prints the same five ids/URLs and no sixth; that run's E08/E11 flood is a `--file` artifact
(paths resolve outside the lane; cut-off predates later rows), evidencing the W04 set only. The `--today
2026-10-25` run is clean, so the six new rows are not future-dated on either clock.
## 2. Frozen manual one-liners (lane root)

```
rows 112 · malformed (NF!=13) 0 · tier A=98 B=9 C=5 · status mined=88 queued=19 rejected=5
duplicate ids (no output) · enum/tier-inflation (no output) · dangling used-by (no output)
[ -e ] on the three cited entry files → OK ×3
```

Manual and script counts agree exactly; no malformed row, duplicate id, enum/A+community violation or dangling `used-by` — including the new rows' three targets.
## 3. Rows 106 → 112; S001–S106 unchanged

N computed: base last row line is S106 at **116** (`awk -F'|' … {n++;last=i;lastline=NR} END{print n,last,lastline}`
over `git show 9ec1751:corpus/SOURCES.md` → `106 S106 116`); tip S106 is line 116, S107 opens 117, S112 closes 122.

```
$ diff <(sed -n 1,116p base-sources.md) <(sed -n 1,116p corpus/SOURCES.md); echo $?               → 0
$ diff <(grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' base-sources.md) \
       <(grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md | sed -n 1,106p); echo $? → 0
ids contiguous last=112 count=112 · no row matching ^| S11[3-9]
staged S125 URL among lane URLs → False · lane rows containing "niph" → []
```

S001–S106 are byte-identical to base by prefix and row projection; the delta is six appended rows, no id
reused, none burned (pre-refusal scratch S113 did not land; refused staged S125 consumed none).
## 4. Every new row re-opened at registry level

Key `sha256(url)[:24]` (c2-count.py:114), form `read_text(encoding="utf-8", errors="replace")` (:121).

```
id   key                       .txt  claimed  decoded(text-mode)  URL occurrences in SOURCES.md
S107 7194acc65a18f6555e4b8893  yes   21216    21216               1
S108 62be15a474e866e4bef6c9d5  yes   39676    39676               1
S109 fd468a36d78ff156b6200946  yes   52208    52208               1
S110 c7266931a1731db3ff6ae77d  yes   50952    50952               1
S111 42bac8830527d6f1bb125c49  yes   1675     1675                1
S112 34fcefc159bf2ebbd1e09540  yes   25811    25811               1
```

Every new URL is unique in-file (count 1 ⇒ no cross-row duplicate; matches zero E04/no W04 for S107–S112);
every declared count is exact in the counter's form; the `char N` cells are real quote offsets —
`env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py` → `C2=PASS`,
`ANCHOR_BOUND=6/6`, `CAPTURE_BOUND=61/61`, `QUOTE_ROWS=61 ON_BOUND=61/61`, exit 0.

Two form facts a later reviewer should not re-derive:
- `spans.tsv`'s `offset` is the **span-file start**, not the quote offset: the quote sits at `offset +
  span.find(quote)`, uniformly **+80** (80 chars leading context), composed at c2-count.py:206-211. Read as
  absolute quote offsets, all 61 rows look off by 80.
- S111 is the only new capture with CR bytes (390; 2065 characters under `read_bytes().decode('utf-8')`).
  Its `1675 characters` and anchor offsets (695, 934, 1138, 1078, 1366) are text-mode values (`text.find` of
  `来源出版物： 中国循证医学杂志 卷：26 期：4` = 695; byte-decode 896) — self-consistent with the frozen
  form. S112's "40 glyphs lost at chars 101–140" holds (`t.count('\ufffd')` → 40, occupying 101–140).
## 5. Renumber map and used-by reciprocity

Checked by URL identity, not prose (staged rows from read-only `…/shokuknow/merge/chousa/SOURCES.append.md`):

```
S109→S107 SAME URL · S110→S108 SAME URL · S116→S109 SAME URL
S117→S110 SAME URL · S119→S111 SAME URL · S126→S112 SAME URL
```

All six hold by document. Reciprocity holds both ways: `japanese-search-record-r38.md` → {S107,S108},
`chinese-search-record-r39.md` → {S109,S110,S111}, `…-amendment-2026-10-23.md` → {S112} — exactly the rows whose
`used-by` names each entry. No entry mentions an id above S112 (`grep -nE '\bS(11[3-9]|1[2-9][0-9])\b'` over the
three → NONE); no `mined` row carries `used-by = —` anywhere.

## 6. What breaks — two staged-id references in the lesson's Gate

Prose-scope, `corpus/lessons/round-51.md`; the rows are clean. The renumber map is line 39; these sentences do not use it:
- `:60` "Admitted as narrowed: … (S126 only …)". S126 is **staged**; the admitted row is S112 and no lane row S126
  exists (registry stops at S112), so resolving `S126` against `corpus/SOURCES.md` hits nothing.
- `:69` "`453d492becd9a2f4632cb8dd` (= S111's document)". S111 here is **staged** (medsci.cn 解读 page, key `453d492…`);
  lane row S111 is the SinoMed record `…/article.do?ui=2026335073`, key `42bac883…` — different URL and capture, same
  article. The table repeats the collision ("S133 and S111 hash to one key").

The risk is concrete: the row layer promises an id resolves to one URL and one capture, so a seat told to "re-open
S111's document" from `:69` opens the SinoMed page and gets a text differing from the printed hash. The search log
already disambiguates (`SOURCES.md:295` "… in the package's numbering"), so the fix is one phrase per sentence — no
registry, counter or predicate change; the `:77-83` quarantine ids are prefixed `register S104 …` and are not this defect.
## 7. Not mine, observed

Working tree: ` M .ufo/waves/round-51/w1/R51DraftSkillGates.md`, untracked `w2.ready`, `w2.ready.dispatched`, `w2/`. The modified
w1 report is not mine and I did not open it; authorisation is the sentinel's call. This seat wrote only this report; scratch
`/dev/shm/chousa-r51-R51W2ExecCensusFinal/` deleted.

VERDICT: attacked the census and registry at the tip — validate exit 0 with only the five pre-existing W04, census 112 rows
agreeing with every manual one-liner (0 malformed, 0 duplicate ids, 0 enum/tier-inflation, 0 dangling `used-by`), S001–S106
byte-identical to base through its last row line 116 with six appended rows S107–S112 whose URLs are unique, keys resolve,
counts and anchor offsets hold in the frozen counter's form (`ANCHOR_BOUND=6/6`, `C2=PASS`), and the staged→lane map holds by
URL with S125 correctly id-less — all hold; the only break is two staged-id references at `corpus/lessons/round-51.md:60` and
`:69`, prose-only.
