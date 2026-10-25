ATTACKS: C1 operability — misses rate of the landed polarity probe on a fresh held-out set of 12 genuine flips (no W1 body reused)
VERDICT: overclaim

seat: L1Chousa47.HeldOutB (critic, leaf) · 2026-10-25 · item: in /tmp write 12 one-bullet JUNK entries, each quoting a phrase from spans/S901-1.txt or S902-1.txt and asserting its OPPOSITE in natural academic English (vary distance, wording, implicit negators `lacks`/`absent`, `un-` forms); run the landed tool; report kills k/12 with codes and every survivor classified by why it passed. Do not reuse W1 CritC1Survivors bodies. bounds: leaf; only this file written; scratch `/tmp/chousa-r47w2-HeldOutB/` deleted at close; no fetch, no install.

## 0. Landed tool, run context

```
$ git -C …/chousa-shokunin rev-parse HEAD
1fc5ed193ad48a482402c862f4e4cc47e46d5b2d
$ python3 tools/inference-ground.py --entry <body> --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r47w2-HeldOutB
```

Bodies hb01–hb12.md under /tmp/chousa-r47w2-HeldOutB/bodies/ (deleted at close). Each has one `#### Inference` bullet, cites `S901`/`S902`, quotes a span phrase verbatim (grounded: tokens=1 grounded=1 on every body), and asserts the opposite. All 12 are genuine flips: hb01/05 assert recording against `no revision is recorded`; hb02/03/04/06/11/12 deny frozen against `release ships a frozen pool`; hb09/10 deny dated against `archived copy is dated at build`; hb07 flips 7,572 (answers_named_source) to "lack any source"; hb08 flips 1,582 (answers_without_archive_key) to "bound to an archive key".

## 1. Result — kills 4/12, survivors 8/12 (MISS rate 67%)

```
=== hb01.md ===  GROUND: PASS  EXIT=0      survivor
=== hb02.md ===  FINDING INF_POLARITY_FLIP bullet=1 token='release ships a frozen pool / frozen'  EXIT=1   KILL
=== hb03.md ===  GROUND: PASS  EXIT=0      survivor
=== hb04.md ===  FINDING INF_POLARITY_FLIP bullet=1 token='release ships a frozen pool / unfrozen'  EXIT=1   KILL
=== hb05.md ===  GROUND: PASS  EXIT=0      survivor
=== hb06.md ===  GROUND: PASS  EXIT=0      survivor
=== hb07.md ===  GROUND: PASS  EXIT=0      survivor
=== hb08.md ===  FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key figures/answers_without_archive_key'  EXIT=1   KILL
=== hb09.md ===  FINDING INF_POLARITY_FLIP bullet=1 token='archived copy is dated at build / undated' ; token='… / build'  EXIT=1   KILL
=== hb10.md ===  GROUND: PASS  EXIT=0      survivor
=== hb11.md ===  GROUND: PASS  EXIT=0      survivor
=== hb12.md ===  GROUND: PASS  EXIT=0      survivor
```

Kill codes: 4/4 are `INF_POLARITY_FLIP`; no body died of ungrounded/uncited (all tokens grounded). Miss rate 8/12.

## 2. Survivors, classified by why they passed (all refute the frozen claim's class)

| body | flip | ground of pass (tools/inference-ground.py) |
|---|---|---|
| hb01 | `no revision is recorded` → "every change is logged" | P1/P2 match by 5-letter stem (`:321`, `:331`); "logged" shares no stem with scope {revision, recorded} — different-stem synonym. |
| hb03 | `release ships a frozen pool` → "the pool changes, so frozenness is absent" | implicit negator `absent` sits AFTER the stem word; P2 reads only the 3 words before (`:336`). "frozenness" stem `froz` has a clean before-window. |
| hb05 | `no revision is recorded` → "changes are recorded, not merely counted" | P1 refuses only with NO negator in 3-before/2-after; `not` at 2-after counts as the negator (`:334`) — double-negation-style pass. |
| hb06 | `release ships a frozen pool` → "It is not the case that …" | `not` is ~7 words before `frozen`, outside the 3-word window (`:333`); all stem-word windows clean. |
| hb07 | 7,572 → "lack any source" | figure leg reads the next 4 words (`:392`); `lack` is at word 5+ → no mismatch. Key answers_named_source is affirmative, so a clean window is expected. |
| hb10 | `archived copy is dated at build` → "carries no timestamp" | different-stem antonym ("timestamp" vs "dated"); `no` outside every stem-word window. |
| hb11 | `release ships a frozen pool` → "the pages are mutable" | pure semantic antonym; zero stem overlap with {release, ships, frozen, pool}. |
| hb12 | `release ships a frozen pool` → "never … frozen" | `never` sits before `frozen` but outside the 3-word window (filler "at any moment after release"). |

## 3. What this shows

- The probe's declared promise (docstring rule 5; claims.md C1) is a **windowed stem-sharing negator mismatch** + a 4-word figure-next-4 check. Within exactly that predicate, the tool behaves as written (kill codes are clean; refinements work: `lacks`-before and `un-` forms are now caught — hb02, hb04, hb09).
- As an operability capability ("refuses polarity flips", D7 class "narrowed to polarity"), the claim overclaims: a fresh set of natural flips passes at 8/12. All 8 survivors are ordinary academic English, no contrived double-negation tricks except hb05.
- The axis writing in claims.md/SCORECARD should keep the Named-limit sentence (`:55-58`, `:64`) — every survivor falls inside it. Nothing here requires changing the frozen predicate, fixtures, floor or target.

## 4. Commands run (verbatim decisive output above)

`git rev-parse HEAD`; 12 × `python3 tools/inference-ground.py --entry hbNN.md --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r47w2-HeldOutB`. No install, no fetch. Scratch deleted at close.
