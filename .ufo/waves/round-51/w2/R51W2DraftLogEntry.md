# R51W2DraftLogEntry — draft of the round-51 LOG.md entry

Seat R51W2DraftLogEntry, round 51 wave 2, leaf (no dispatch). Read-only on the lane; the only file
I wrote is this report. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip
`4436e279b91d8d68fd439c9095695035fbeeab74` (freeze `d603f6f0…`, base `9ec1751a…`, adopter v2
`cf642c66`). No fetch; L0 `8d77e6c1` open. No install, no scratch root (nothing written outside this report).

## 1. Shape read (Round 50 entry)

    $ grep -n '^## Round 5' LOG.md  → 370:## Round 5 — verify-sweeps (goal wave)
                                      1809:## Round 50 — 2026-10-25 (adopter self-test; Chinese …)
    $ wc -l LOG.md → 1821 LOG.md

The Round 50 entry is: heading; a freeze paragraph naming `claims.md`, the control receipts, the
candidate/before-measurement and the disclosure file; one bullet per claim with its counter's literal
tail; a `Frontier / SOURCES` bullet; `Mistakes mined`; `Post-freeze tool changes`; `Waves`;
`Inherited`. The draft keeps that order and cites commits and counter tails, not prose numerals.

## 2. Counters at the tip (each run by me, `env -u ASSIMILATE_CITES`)

    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py | tail -2
    LEGS=5/5
    C1=PASS                                  # rc=0
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py | tail -2
    SUPPLEMENT_LEGS=6/6
    C1_SUPPLEMENT=PASS                       # rc=0
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py | tail -4
    QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
    QUARANTINE_BLOCKED_ADOPTED=0
    C2=PASS                                  # rc=0; earlier line: BOUND=6/7 (min 5) REFUSED=1
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py | tail -4
    CAP_ROWS=36 (base 36)
    POINTERS=74 (base 74)
    RESOLVED_BY_CORRECTION=4
    DANGLING=0
    C3=PASS                                  # rc=0

Before-states, from the filed receipts: `controls/c1-lane-before.txt` → `LEGS=1/5 / C1=FAIL / exit=1`;
`controls/c1-before.txt` → tool-before `1/5` (:1-7), echo `2/5` (:10-16), const `1/5` (:19-25),
flag-noop `2/5` (:28-34); `controls/c2-before.txt` → `ENTRIES=0/3 BOUND=0/7 REFUSED=0`;
`controls/c3-before-erratum.txt` → `DANGLING=5 / C3=FAIL / exit=1`.

## 3. Attack evidence used by the draft

    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py | tail -2
    LEGS=5/5
    C1=PASS
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --tool corpus/evidence/round51/controls/forge-dirname.py | tail -2   # from c1-supplement-controls.txt
    SUPPLEMENT_LEGS=1/6
    C1_SUPPLEMENT=FAIL
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/echo-tool.py | tail -2
    LEGS=2/5
    C1=FAIL
    $ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --tool corpus/evidence/round51/controls/echo-tool.py | tail -2
    SUPPLEMENT_LEGS=0/6
    C1_SUPPLEMENT=FAIL

`controls/c1-supplement-controls.txt` also files `tool-candidate1.py` at `LEGS=5/5 C1=PASS` +
`SUPPLEMENT_LEGS=3/6`, const `1/5`/`0/6`, flag-noop `2/5`/`1/6`, real tool supplement `6/6`.
`git show cf642c66 -- corpus/evidence/round51/controls/echo-tool.py` shows the delegation target
moving from the lane tool to `controls/tool-before.py` (E4) — that is why the echo control reads
`2/5` now, while lesson row 8 records the pre-fix `5/5`.

    $ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   → 112
    $ awk 'NR>1 && NF' corpus/evidence/round51/spans.tsv | wc -l             → 61
    $ git log --oneline -1 4436e27 → round-51: adopt the Japanese/Chinese search-record theme by document …
    $ git show cf642c66 --stat -- SCORECARD.md SHONEN.md → 9 +, 2 +- (four `correction:` lines at SCORECARD.md:2626-2629; SHONEN.md:10 path)
    $ python3 -c '…swarm-registry…' → w1 48 members, w2 41 members; w1-spec roles {scribe 22, executor 12, critic 4, scout 3, reviewer 2, connector 2, mutation-tester 1, sentinel 1, simplifier 1}
    $ ls .ufo/waves/round-51/w1/*.md | wc -l → 48   ;   w2 reports on disk at draft time: 25 (wave running)

Quarantine verdicts (lesson `### Quarantine slice`; `R51ExecQuarantine.md:109`): 2 `present` (S111,
S120), 4 `absent-as-written` (S104, S105, S112, S114), 0 `fabricated`/`unverifiable`. Refused document: staged S125, the NIPH `.docx` (`c2h.niph.go.jp/…/Reporting_Format_Jap_202404.docx`), capture form only.

## 4. Draft — intended lane path `LOG.md`, appended after line 1821

```LOG.md
## Round 51 — 2026-10-25 (a falsify wave on three frozen claims; the Japanese/Chinese search-record theme bound by document)

Claims froze at `d603f6f00f78d64f123d3aed2dd9f8701547a4ba` in `corpus/evidence/round51/claims.md` (base `9ec1751a…`, lane tip `4436e279…`) after the do-nothing controls were scored: `corpus/evidence/round51/controls/c1-lane-before.txt` → `LEGS=1/5 C1=FAIL exit=1`; `controls/c1-before.txt` → tool-before `1/5`, echo `2/5`, const `1/5`, flag-noop `2/5`; `controls/c2-before.txt` → `ENTRIES=0/3 BOUND=0/7 C2=FAIL`; `controls/c3-before-erratum.txt` → `DANGLING=5 C3=FAIL`. Disclosures: `corpus/evidence/round51/claims-erratum.md` E1 (the C3 extractor stripped a leading dot, so three existing `.ufo/…` paths read as drift; the before-count is 5, not the 8 of the first run, and no seat had scored) and E2-E4 in `corpus/lessons/round-51.md` `## Disclosed post-freeze changes`. No fetch; L0 `8d77e6c1` open.

- **C1 operability (capability extension, plumbing)**: `tools/assimilate-rows.py` v2 (`cf642c66`) draws a document id only from a `source:` line on header lines, substitutes and cites per entry, lists body-only ids in `bodyonly.tsv` and clashes in `bodyclash.tsv`, takes a registry or staged cell's identity after the escaped-pipe rewrite, refuses a registry with no `## Registry` heading or with an `S###` row outside it, and refuses a `source:` id that is neither staged nor a registry row; `--cites all`/`ASSIMILATE_CITES` keep the round-50 all-token behaviour. `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py` → `LEGS=5/5` `C1=PASS` exit 0 (was `LEGS=1/5`); `python3 corpus/evidence/round51/c1-supplement.py` → `SUPPLEMENT_LEGS=6/6` `C1_SUPPLEMENT=PASS`. The frozen counter still cannot see the behaviours: `controls/forge-dirname.py`, 94 lines that read the work directory's name out of `--out` and print canned shapes, scores `LEGS=5/5 C1=PASS` and `1/6` on the supplement; `controls/tool-candidate1.py` scores `5/5` and `3/6`; the four do-nothing controls stay at `2/5`, `1/5`, `2/5` and `0/6`, `0/6`, `1/6`.
- **C2 depth (sourced, ground)**: three entries — `corpus/knowledge/japanese-search-record-r38.md`, `corpus/knowledge/chinese-search-record-r39.md`, `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` — on six bound documents S107-S112 (staged S109/S110/S116/S117/S119/S126 → S107/S108/S109/S110/S111/S112), with a 61-row quote manifest `corpus/evidence/round51/spans.tsv` derived by `build-spans.py` from `quotes.tsv` and every quote also in the citing entry and in the lesson. `python3 corpus/evidence/round51/c2-count.py` → `BOUND=6/7 (min 5) REFUSED=1`, `QUOTE_ROWS=61 ON_BOUND=61/61`, `CAPTURE_BOUND=61/61`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=6/6`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_VERDICTS=6/6`, `C2=PASS` exit 0 (was `C2=FAIL`). The seventh staged document, a national institute's 記載様式 `.docx` (staged S125), was opened and refused: its text exists only in the DEFLATE member `word/document.xml`, the cache's `.txt` is 168952 characters of zip bytes (72117 U+FFFD) in which none of its phrases occur, and no quote can be bound in either form the counters read; the lesson carries the `refused-doc` line with its flip. Controls: the staged entries unchanged → `BOUND=0/7 REF_ID_UNBOUND=30 C2=FAIL`; adopter-rewritten entries with an append block but no quotes → `BOUND=7/7 QUOTE_ROWS=0 C2=FAIL`.
- **C3 calibration (plumbing)**: four append-only `correction:` lines at `SCORECARD.md:2626-2629` (rows printing `measure/final/`, `measure-l1/c1-s36361.json`, `measure-l1/c2-s36371.json`, `c1-supplement.py`) and one `SHONEN.md:10` line (bare `round25-meta-differential.log` → `corpus/evidence/round25-meta-differential.log`), both at `cf642c66`. `python3 corpus/evidence/round51/c3-count.py` → `CAP_ROWS=36 (base 36)`, `POINTERS=74 (base 74)`, `RESOLVED_BY_CORRECTION=4`, `DANGLING=0`, `C3=PASS` (was `DANGLING=5`). Controls: blanket correction line `DANGLING=5`; dangling rows deleted `CAP_ROWS=32`; zero-byte files at the pointer names `DANGLING=5` — all `C3=FAIL`; a DOTPATH control passes at the tip counter and prints `DANGLING=4 C3=FAIL` at the pre-erratum one.
- **Gate (lesson `## Gate`)**: three admits — the two search-record entries and the dated amendment (S126 only). Seven other staged entries in the neighbourhood were reviewed: four refused (`search-log-fields-r36.md`, its PRISMA-S capture a 267-character challenge page; `chinese-search-log-r37.md`, superseded by S111/S112; `grey-literature-and-chinese-search-record-r40.md`, out of province and one page carried by two ids; `grey-literature-and-chinese-search-record-r41.md`, no located quote), three `admit-later` (`search-tracking-record-r40.md`, `chinese-search-log-r37-amendment-2026-10-23.md`, `japanese-prisma-item-wording-r40.md`). Quarantine: all six theme-URL register rows hand-checked — 2 `present` (S111, S120), 4 `absent-as-written` (S104, S105, S112, S114), 0 `fabricated`, 0 `unverifiable`; no verdict blocks a bound document, and S114's `学科分类号`/`主题词`, which exist only in an HTML comment, are quoted nowhere. Collision check: 25 collisions under the 0-3-space pattern (3 identity, 22 numbering).
- **Frontier / SOURCES**: 106 → 112 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 112; A +5 S107-S110/S112, B +1 S111), no old row touched; census exit 0 at both ends with the same five W04 (lesson `## Census`). QUALITY 81-86 (nonce-generated counter inputs; `source:`-only citation; pointer resolution; receipt revision pins; random work-directory names and pinned-base controls; a tokenizer positive control). `SKILL.md` `assimilate-rows` row replaced, `chousa round-51 counters and checks` row added, one `correction:` line for the round-50 gate row. `corpus/README.md` `## Round51 coverage and frontier` (credit per document, not per entry or journal) plus one `correction:` line for the `istic` filename drift. `receipt-check.py`, `open-items-age.py` and `measure-r50-at-tip.txt` (round-50 receipt re-measured at `1d7aba0`, zero differing lines) landed.
- **Mistakes mined (lesson, 8 rows)**: an unpinned round-50 receipt and a gate row naming the candidate; a counter recognising its own literal DIFF lines; the adopter's default flip breaking both earlier one-shot counters (`round49` `2/3`, `round50` `3/5`); five dangling self-assessment pointers with no criterion to resolve them; the C3 tokenizer's leading dot; the `istic` filename drift absent from the coverage row; a receipt tally whose printed command prints `0`; and the C1 counter's fixed work-directory names, colliding id draws and inherited environment.
- **Post-freeze tool changes**: E1 above; E2 the frozen C1 counter can hang on a first-two-draw collision (1/401 per run; the supplement draws distinct ids); E3 it inherits an ambient `ASSIMILATE_CITES` (the supplement removes it; run the frozen counter with `env -u`); E4 the shipped echo and const controls delegated to the lane tool — they now delegate to `controls/tool-before.py`, so at the tip `echo-tool.py` scores `LEGS=2/5` and `SUPPLEMENT_LEGS=0/6`; v2 `cf642c66` as above. Not done, named: the zip-member capture form (`R51ExecCaptureForm`) and the `MutAdopter` survivors MUT04/MUT06.
- **Waves**: W1 48 seats (scribe 22, executor 12, critic 4, scout 3, reviewer 2, connector 2, mutation-tester 1, sentinel 1, simplifier 1), 48 reports filed. W2 41 seats (reviewer 12, critic 10, executor 8, mutation-tester 3, scribe 3, connector 2, scout 2, sentinel 1); report count to be filled at closure. The L1 wrote both specs (`gen-w1-spec.py`, `gen-w2-spec.py`) and the validated dispatches. No tool installs.
- **Inherited**: the round-50 routed defects are closed or disposed as `corpus/lessons/round-51.md` `## Spot-check intake` records — the revision pin via `measure-r50-at-tip.txt` and the `SKILL.md` correction, the nonce form by the round-51 counter and the supplement, seat names by `name-collision-check.py` before each `.ready`, the coverage-row drift by the README correction.
```

## 5. Findings

1. All three counters and the supplement reproduce at the tip with the values quoted above; the C1
   supplement is the only artefact separating the real tool (`6/6`) from forge (`1/6`) and v1 (`3/6`).
2. `claims.md`'s C3 Before bullet still says `DANGLING=8`; the erratum's 5 is the quoted before-count,
   so the entry's 5 must be read against `claims-erratum.md:19-23` — both numbers are filed, neither
   edited.
3. `corpus/evidence/round51/measure-after.txt` does not exist in the tree at `4436e27` (the directory
   holds `measure-r50-at-tip.txt` only). The draft therefore cites the counters and control receipts
   directly; if the L1 lands a round-51 after-measurement at closure, the freeze paragraph should name
   it the way the Round 50 entry names `round50/measure-after.txt`.
4. Lesson row 8's "at the tip it scored `LEGS=5/5`" for the echo control describes the pre-`cf642c66`
   delegation; measured now (`--tool controls/echo-tool.py`) it is `LEGS=2/5`, `SUPPLEMENT_LEGS=0/6`,
   and the `cf642c66` diff shows the delegation target changing. The draft states both.
5. `python3 corpus/evidence/round51/open-items-age.py .ufo/waves/round-51/w1/R51SentScope.md --round 51`
   prints `OPEN_ITEMS_AGE=FAIL` — the checker wants the round report's operator line, which no wave
   seat report carries, so the draft makes no PASS claim for it.
6. `python3 corpus/evidence/round51/receipt-check.py` prints `CHECKS=0 OK=0 FAILS=0
   RECEIPT_CHECK=PASS` with no arguments on this tree, so the draft asserts the file landed and what
   QUALITY 84 requires, not a scan hit count; W2 was still running at draft time (25 of 41 reports on
   disk), so the draft leaves W2's report count to closure. Every other count in it was read or run
   above.

## 6. Out of scope

No product, counter, lesson, SCORECARD, SHONEN, SKILL or README edit; no commit, no index or jj
operation; no campaign tool run; no network. This report is the only file written.

VERDICT: attacked the LOG/entry writing surface — re-ran the three frozen counters and the supplement at `4436e27` (`LEGS=5/5`, `SUPPLEMENT_LEGS=6/6`, `C2=PASS BOUND=6/7 REFUSED=1`, `C3=PASS DANGLING=0`), re-ran the forge and echo controls (5/5 vs 1/6; 2/5 vs 0/6), and grounded every sentence of the draft in a commit, a control receipt or a lesson section; found four drafting hazards (the claims/erratum 8-vs-5 split, no round-51 `measure-after.txt`, the echo 5/5 reading, an unfinished W2) and one check that does not pass as filed (`open-items-age.py` on a wave report), all handled in the draft.
