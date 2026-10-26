# R52W2ExecInfRegression — attack: the `inference-ground` leg that carries C2's kill rule

Seat R52W2ExecInfRegression (leaf; no subagents). Lane HEAD `d1d972cf285515ae1de824ce9f1086d26f627662` (`e769c037…` ancestor: `merge-base --is-ancestor` → YES). Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ExecInfRegression` (TMPDIR there, removed on exit). No tool installed or upgraded; `pacman` untouched per the host-wide pause.

**Attacked → result.** (1) tool identity and the three earlier counters that read it — unchanged, all exit 0; (2) the tool on the three landed entries — 3/3 PASS, 24/24 tokens grounded; (3) the polarity channel's *reach* on those 24 tokens — **20 have no polarity window at all**; (4) one Inference bullet per entry rewritten to assert the opposite while keeping its quoted CJK phrase — **all three still print `GROUND: PASS`, exit 0, zero findings**; (5) the same inversion made reachable by a Latin carrier in the same entry file — fires, so the hole is the channel, not the harness; (6) three further inversions (mixed-token period claim, negated-span privacy sentence, translator verdict) — all pass; (7) the regression fixtures — **not one CJK character in r46/r47/r48**, and both mutation directions still bite on Latin; (8) the counts figure channel under `--counts /dev/null` — dead this round.

## 1. Tool identity; earlier counters that read it

```
$ sha256sum tools/inference-ground.py
33d4a37f3f7a5ce87862d0a354b3058ed5c579c5491b9e5d3ec6610a8e962b6d
$ git -C <lane> diff --stat 00f8c7f5… HEAD -- tools/inference-ground.py     → (empty)
$ git -C <lane> log -1 --format='%H %ad %s' -- tools/inference-ground.py
74794db07e1b383d5c3e96ad5122fd158a541271 Sun Oct 25 18:56:14 2026 -0300 round-50: … CJK grounding fix …
$ round46/c1-count.py → exit=0  JUNK_KILLED=3/3  CANARY=pass  C1=PASS
$ round47/c1-count.py → exit=0  R46_COUNTER=pass  R46_ENTRIES=2/2  C1=PASS
$ round48/c1-count.py → exit=0  PRECISION_GATE=PASS  LEGACY_R47=PASS  C1=PASS
```

## 2. The tool on the three new entries (round-52 manifest, `--json` per entry to scratch)

```
$ python3 tools/inference-ground.py --entry corpus/knowledge/<e>.md --spans corpus/evidence/round52/spans.tsv \
    --counts /dev/null --registry corpus/SOURCES.md --root <lane> --json <scratch>/<e>.json
japanese-search-record-niph-form-r52  section=1 bullets=5 tokens=9 grounded=9  GROUND: PASS exit=0
japanese-prisma-item-wording-r40      section=1 bullets=3 tokens=7 grounded=7  GROUND: PASS exit=0
chinese-prisma-s-reception-r52        section=1 bullets=4 tokens=8 grounded=8  GROUND: PASS exit=0
$ python3 corpus/evidence/round52/c2-count.py → exit=0  ENTRIES=3/3 … SUBSTANCE=PASS … ANCHOR_BOUND=4/4 …
                                               INFERENCE_GROUNDED=3/3 … C2=PASS
```
The leg is `grounded += p.returncode == 0` over `ENTRIES = (E_NIPH, E_JPW, E_ZHR)` (`c2-count.py:64,231-238`): a pure function of the tool's exit code on those three paths.

## 3. Reach: how many of the 24 tokens the polarity channel can even see

Imported the tool as a module and evaluated `phrase_polarity(tok, span_texts(…))` per token (the first call `polarity_flips` makes; empty `stems` ⇒ it returns `[]` unconditionally):

```
TOTAL tokens=24  polarity-unreachable=20  polarity-reachable=4
  reachable: PRISMA(Preferred Reporting Items…)/niph-b2 → prism,prefe,repor,items,syste,revie,analy,meta
             From: Page MJ, McKenzie JE, Bossuyt…      → page,mcken,bossu,boutr,hoffm,mulro
             系统评价_Meta分析中…（PRISMA-S）解读_郑卿勇.pdf → meta,prism
             originalUrl=, linkOutUrl=,                 → origi,linko
```
The 20 unreachable: 15 pure-CJK tokens (no `[A-Za-z]` word ⇒ `words()` empty ⇒ no scope), 4 mixed tokens whose only Latin run is under four letters (`web`, `sr`) and is dropped by `content()`'s `len(w) >= 4`, and the numeral `2020` (numerals never reach `polarity_flips`). Confirmed empirically: `probes/p3-webfp.md` keeps r40 b2's true claim and adds "no Web site is dropped from the strategy item" — the negator sits directly before a mixed token's Latin run and still prints `GROUND: PASS exit=0`. All four reachable carriers are bibliographic strings — a credit line, an attachment filename, URL flags, the PRISMA expansion — **none is item wording**, which is what every Inference bullet in these entries concludes from.

## 4. The CJK polarity probe (one bullet per entry, quote byte-identical)

Scratch copies verified byte-identical to the lane files before editing (`sha256sum` equal), then one bullet rewritten:
niph b3 "is counted in the flow chart, not hidden" → "**must not appear** in the flow chart", tail "keeps the non-database route **out of** the counted sources"; r40 b1 "ask for sources, their dates and a strategy" → "ask for sources and a strategy, **and not for their dates**", tail "**no requirement to date any source**" (span: 日付を記載する); zhr b1 "**dates each source**" → "**does not date its sources**", tail "one date for the search, **not one per source**" (span: 明确说明每一项来源的检索或查询日期).

```
mutated japanese-search-record-niph-form-r52 → tokens=9 grounded=9  GROUND: PASS exit=0 findings []
mutated japanese-prisma-item-wording-r40     → tokens=7 grounded=7  GROUND: PASS exit=0 findings []
mutated chinese-prisma-s-reception-r52       → tokens=7 grounded=7  GROUND: PASS exit=0 findings []
```
`INF_POLARITY_FLIP` did **not** fire on any of the three. Three further inversions, each keeping its CJK quote:
`p1-mixed` (niph b1 → "need not carry a start or an end date"; span 明記する) PASS exit=0; `p2-negspan` (niph b4 → "publishes the names and affiliations"; span 公開しない) PASS exit=0; `p5-credit` (zhr b3 → "names its translator and is an authorised Chinese version") PASS exit=0, 8/8 grounded — p5 is the verdict the lesson's staged-correction row records as *dropped*, re-asserted.

## 5. Controls: harness and detector live; the channel is the hole

```
ctrl/latin-flip.md → FINDING INF_POLARITY_FLIP bullet=1 token='The form requires a search date… / require'
                     FINDING INF_POLARITY_FLIP … / date                          GROUND: FAIL exit=1
ctrl/cjk-flip.md   → GROUND: PASS exit=0
probes/p4-prisma.md ("…and this happens without PRISMA", CJK quotes kept, real niph file, real manifest)
  FINDING INF_POLARITY_FLIP bullet=2 token='PRISMA(Preferred Reporting Items… / prisma'
  FINDING INF_POLARITY_FLIP bullet=2 token='PRISMA(Preferred Reporting Items… / items'   GROUND: FAIL exit=1
```
Latin/CJK twins are structurally identical (span affirms a requirement, bullet says it is not required, quote retained): only the script of the carrier decides. Their whole source, so the scratch fixtures need not survive:

```
ctrl/spans/S200-1.txt : The form requires a search date for every source.
ctrl/spans/S201-1.txt : 本様式は各情報源の検索日を記載する。
ctrl/latin-flip.md    : - **The form does not require a search date.** `S200` says "The form requires a search
                        date for every source.", so a record need not date its sources.
ctrl/cjk-flip.md      : - **本様式は検索日を必須としない。** `S201` says "本様式は各情報源の検索日を記載する。", so a
                        record need not date its sources.
```


## 6. Why the regression set cannot see this class

Scan of `corpus/fixtures/inference-ground-r46` and `-r47` (`*.md`, `*.tsv`, `*.txt`) for any CJK codepoint → no output. Both mutation directions still bite, on Latin only (`--tool` on a scratch copy):

```
t_nopol.py (polarity_flips→[])      r47: POSITIVE_PASS=3/3 JUNK_KILLED=1/3 CANARY=fail C1=FAIL
                                    r48: PRECISION_GATE=PASS LEGACY_R47=FAIL C1=FAIL
t_alwaysflip.py (polarity_flips→hits) r47: POSITIVE_PASS=1/3 JUNK_KILLED=3/3 CANARY=fail C1=FAIL
                                    r48: CORRECT_BULLETS_PASS=0/12 PRECISION_GATE=FAIL C1=FAIL
```
The fixtures are sound and the counters discriminate — for the script they were written in.

## 7. The counts channel is unexercised this round

`c2-count.py:236` passes `--counts /dev/null`; `count_values(/dev/null) == set()`, `count_keys(/dev/null) == {}`, `figure_flip("1,582 records carry no archive bucket","1,582",set()) → False`. Criterion 67's figure clause cannot fire on any round-52 entry; no counts manifest for this theme exists.

## 8. What is disclosed, and what the disclosure does not reach

- `claims.md:114-115` — "the counter measures binding and presence, not entailment (the round-50/51 limit, restated before data)". Accurate; the honest ceiling of C2.
- `claims.md:111` (kill rule) — "any entry failing `inference-ground`" is listed among what fails C2. On these three entries nothing can fail this leg except a missing quote or an ungrounded token: §4's inverted entries pass it.
- `QUALITY.md:627-637` (66) — named limit: "correct tokens strung into an assertion of the opposite still pass". True.
- `QUALITY.md:643-661` (67) — its named limit lists "a different stem, a distant negator, or a second bullet" (`:655`), never the script; and its `Note on 66` at 661-663 says "its limit … now holds only outside criterion 67's windows". On this round's bytes that reassures vacuously: 20 of 24 tokens lie outside every window because the windows are built from `[a-z]` words, and the quotes the entries reason from are Chinese and Japanese.
- `grep -n 'inference\|GROUND\|grounded' corpus/lessons/round-52.md` → no output: the lesson never states this leg, so the round's own gate record cannot show that it is a presence check.
- `has_two_words` (tool:92-96) carries the limit as a code comment ("words() is Latin-only, so a CJK phrase never trips the polarity check"), added in round 50 to fix the *token count*; the docstring's "Named limit" paragraph (tool:56-62) does not repeat it.

**Blind spot, named.** The polarity channel is defined over a Latin word regex, so a claim whose carrier is a CJK phrase has no window at all — not a narrow one, none — and every round-52 Inference conclusion is built on such a phrase; criterion 67 cannot observe a CJK-carried reversal and criterion 66's fail-open is fully open for the claims this round lands. Secondary: a mixed token contributes only its Latin runs of ≥4 letters, so where the channel is reachable here it keys on incidental bibliographic strings, not on the entailment — an inversion near those strings would fire on a claim they do not carry, while inversions of the claims beside them pass.

## 9. Risk and disposition

No frozen predicate, counter, control or target is touched; `INFERENCE_GROUNDED=3/3` and `C2=PASS` reproduce at HEAD and this seat does not dispute them. The exposure is in how the round reads that leg: `claims.md:111` and the C2 tag invite a reader to take `GROUND: PASS` as a check on the inference, and `QUALITY.md:661-663` invites the same. Covering the reversal class for CJK needs either (a) `claims.md:111` stating the leg is presence-only for CJK-carried claims — a disclosure, no predicate change — or (b) post-freeze, a CJK fixture (the `ctrl/cjk-flip.md` shape, ≤10 lines) in a future counter's fixture set; adding one now would change a frozen counter, which this seat does not do. No production file written; every fixture used lives only in scratch and is reproduced in the blocks above.

VERDICT: Attacked the `inference-ground` leg of C2 and the three entries' entailment — tool and r46/r47/r48 counters intact (3× exit 0, 24/24 tokens grounded), but three CJK-carried Inference bullets reversed to the opposite of their quoted spans still print `GROUND: PASS` exit 0 with zero `INF_POLARITY_FLIP`, because 20 of 24 tokens have no polarity window and the same inversion fires only once its carrier is Latin; the leg is a presence check on exactly the claims this round lands, and `QUALITY.md:661-663`'s narrowing note does not reach them.
