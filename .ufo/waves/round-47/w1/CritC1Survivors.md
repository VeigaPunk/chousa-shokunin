# CritC1Survivors — polarity-flip bodies the landed probe accepts (R47-C1, operability)

seat: L1Chousa47.CritC1Survivors (critic, leaf) · 2026-10-25 · item: build the strongest polarity-flip bodies `tools/inference-ground.py` (rule 5, `INF_POLARITY_FLIP`) ACCEPTS over `corpus/fixtures/inference-ground-r47/` — (1) different-stem synonym/antonym, (2) flip word 4+ words from its negator, (3) double negation, (4) flip in a second bullet that quotes nothing, (5) figure flip with `without` 5+ words after the numeral, (6) re-create round-46 `v7-strongest.md`; state the narrowest true sentence; rule on "stem-sharing polarity flip" vs "entailment". bounds: leaf; only this file written; scratch `/tmp/chousa-r47-CritC1Survivors/` deleted; no fetch, no install, no lane production file touched.

## 0. Bytes attacked

```
$ git log --oneline -1            → a15610a round-47: C1 polarity probe in tools/inference-ground.py (INF_POLARITY_FLIP)
$ sha256sum tools/inference-ground.py ; git cat-file -p a15610a:tools/inference-ground.py | sha256sum
8899e7868ffb66fd0d58162342a20a2ab6f3a0e1aee7d0d5b36aa1b7fd7a0a40  (worktree == a15610a)
$ python3 corpus/evidence/round47/c1-count.py
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS   EXIT=0
```
Every run below: `python3 tools/inference-ground.py --entry <body> --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r47-CritC1Survivors`. Each body has one `#### Inference` section; the bullet text is quoted below.

## 1. Results — 12 survivors (exit 0), 2 bounds (exit 1)

| # | body (sha256[:16]) | Inference bullet (flip in **bold**) | result |
|---|---|---|---|
| 1 | `b1-synonym` 44aa55aea242a50f | Because `no revision is recorded`, **every sentence is edited** after publication (`S901`). | `tokens=1 grounded=1 GROUND: PASS` EXIT=0 |
| 1b | `b1b-prefix` a4e4dfe672a4bd4d | Since `the release ships a frozen pool`, the pool is **unfrozen** and changes after release (`S901`). | PASS EXIT=0 |
| 2 | `b2-far` e0565194f81dfdd9 | Although `the release ships a frozen pool`, the pool is **not**, by any reading of it, **frozen** (`S901`). | PASS EXIT=0 |
| 2b | `b2b-after` 5761af9f40187de4 | `the release ships a frozen pool` is said, but the pool **frozen** at release is a claim that **does not hold** (`S901`). | PASS EXIT=0 |
| 3 | `b3-double` 837e8d41f9abbbed | Because `no revision is recorded`, there is **no** sentence that is **not revised** after publication (`S901`). | PASS EXIT=0 |
| 3b | `b3b-after` dd3d6f008db13cf7 | Because `no revision is recorded`, every sentence **is revised, not merely recorded**, after publication (`S901`). | PASS EXIT=0 |
| 4a | `b4a-second-figure` e0a3feca8f5381d0 | bullet 1 = `positive-negation-kept` text; bullet 2: **Every sentence is revised after publication** across the 7,572 sourced answers (`S901`). | `bullets=2 tokens=2 grounded=2` PASS EXIT=0 |
| 4b | `b4b-second-otherquote` ea809091268c34b8 | bullet 1 as 4a; bullet 2: **Every sentence is revised after publication**, and `the archived copy is dated at build` (`S902`). | PASS EXIT=0 |
| 4c (bound) | `b4c-second-bare` 961ca5bedc31a962 | bullet 1 as 4a; bullet 2: Every sentence is revised after publication (`S901`). | `FINDING INF_UNGROUNDED bullet=2` EXIT=1 |
| 5 | `b5-figure-far` 3ee161d2d627dde3 | 7,572 answers, as the manifest counts them, are **without any source**, so the corpus cannot bind them (`S902`). | PASS EXIT=0 |
| 5b | `b5b-figure-noise` 9a7be240ea51468b | 1,582 sourced answers, **no fewer**, **carry an archive key**, so their citations are bound (`S902`). | PASS EXIT=0 |
| 5c | `b5c-figure-lack` bb968ef8d447c604 | 7,572 answers **lack a source**, so the corpus cannot bind them (`S902`). | PASS EXIT=0 |
| 5d (bound) | `b5d-figure-near` 034d68d2327b93aa | 7,572 answers are **without** any source, … (`S902`). | `FINDING INF_POLARITY_FLIP bullet=1 token='7,572 / counts key answers_named_source'` EXIT=1 |
| 7 | `b7-combined` 4f2f25ef211e219e | v7's three inversions rebuilt only from surviving forms (1, 1b, 5, 5b, 3 across 3 bullets) | `bullets=3 tokens=5 grounded=5 GROUND: PASS` EXIT=0 |
| 8 | `b8-spanfigure` (scratch manifest +S903 span `the manifest lists 7,572 answers that name a source`) | 7,572 answers **name no source**, … (`S903`). | PASS EXIT=0 with the r47 counts **and** with `--counts /dev/null` |

Item (4) as literally posed (a second bullet that quotes nothing at all) dies on rule 3 (`INF_UNGROUNDED`, 4c). It survives as soon as that bullet carries any grounding token whose stems differ from the flip word: a counts figure (4a) or another span's phrase (4b). The probe compares a bullet's words only against that bullet's own tokens (`:411`, `:417`), so the bullet-1 quote never constrains bullet 2.

## 2. v7-strongest re-created — it now exits 1, polarity included

I re-created the file from the two-section block in `round-46/w2/CritC1D7.md` §1. My sha256 is `578d19ac2c675b72…` and the round-46 file was `1234254cdc3c086c…`, so the round-46 file held bytes the report did not print. Byte identity is not established; the Inference text is verbatim.
```
[r47 fixtures]  bullets=2 tokens=8 grounded=4
FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revised'
FINDING INF_POLARITY_FLIP bullet=1 token='7,572 / counts key answers_named_source'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='78.7%'          (78.7 is absent from the r47 counts.json)
FINDING INF_UNCITED bullet=2 · INF_TOKEN_NOT_IN_SPAN bullet=2 ×3 ('independently re-verified…', 'no revision is recorded', '4,137')   EXIT=1
[r46 fixtures]  as above, plus FINDING INF_POLARITY_FLIP bullet=1 token='78.7% / counts key archive_share_percent'; no 78.7 token finding   EXIT=1
[r46 tool blob 3018b1d2 from 3807537, r46 fixtures]  bullets=1 tokens=5 grounded=5 GROUND: PASS   EXIT=0
```
Isolation: with bullet 1 only (`v7-b1only` f1dc8d4e5b785619) against the r46 fixtures, the result is **exactly three `INF_POLARITY_FLIP` and nothing else**, EXIT=1. The polarity probe kills v7 on its own, and the second section dies separately on the round-46 parser fixes. Repairing v7's bullet to use surviving forms (`edited`, plus `, as the manifest counts them,` / `, by the same manifest,` padding before `name no` / `without`) gives `v7-repaired` 1ac44f4253dfd751: **PASS EXIT=0** on the r46 fixtures, and on the r47 fixtures only `78.7%`-not-in-span. The round-46 strongest body is dead as written and alive after a three-word edit.

## 3. Mechanism (`tools/inference-ground.py`)

- `:295` `before, after = uw[j-3:j], uw[j+1:j+3]`: the windows count negators and never resolve scope. P1 accepts any negator in the window, including a second one (3) or an unrelated one (3b). P2 looks only *before* the word (2, 2b).
- `:222` `NEG_WORDS` is 11 closed-class words plus `n't`. Negative verbs (`lack`), affixes (`un-`), and quantifier flips (`every`/`no fewer`) are invisible (1b, 5b, 5c). `:242` `stem = w[:5]`: different-stem antonyms are invisible (1).
- `:342` `nxt = words(...)[:4]`: the figure leg is a 4-word window; a negator at word 5+ is missed (5), and any negator inside it satisfies a negative key (5b).
- `:414-424`: a figure found in cited span text sets `ok` before the counts branch, so `figure_flip` never runs on it (8).
- **The figure leg is unreachable on real lane entries.** `SKILL.md:70` and `corpus/evidence/round47/c3-count.py:174` both run entries with `--counts /dev/null`, so `figure_flip` fires only on fixtures. On every lane entry the C1 probe is P1/P2 phrase legs only.

## 4. Narrowest TRUE sentence of what the probe refuses

> For each 2+-word quoted phrase that a bullet's cited span carries, it refuses the bullet only in two cases. If the span negates the phrase (a negator inside it, or among the 3 span words before it), it refuses when some unquoted bullet word shares a 5-letter prefix with a 4+-letter content word after the phrase's negator and has none of the 11 `NEG_WORDS` (or an `n't` form) among its 3 preceding or 2 following words. If the span does not negate the phrase, it refuses when such a prefix-sharing word has one of those negators among its 3 preceding words. Separately, for a 3+-digit figure or percentage that only `counts.json` grounds, under keys of one polarity, it refuses when the presence of a negator in the next 4 words disagrees with a `no`/`not`/`none`/`without` key segment. That last leg is never exercised by the lane's entry runs, which pass `--counts /dev/null`.

It counts negator tokens in fixed windows; it does not compute polarity. A second negator, an unrelated negator, a negative verb or affix, a quantifier flip, a different stem, a different bullet, or a span-grounded figure all pass (§1).

## 5. Wording ruling — SCORECARD / SKILL / QUALITY

- **"entailment" must not appear as the capability.** `SCORECARD.md:2484` planned "an ENTAILMENT leg"; what landed is a lexical windowed negator-count probe. If the round-47 row says entailment, or says the D7 class is closed, it overclaims: `b7-combined` is a full D7 body that passes.
- **"stem-sharing polarity flip" is necessary but still too broad.** The scribe's capability draft (`ScribeC1Rows.md:76`, "stem-sharing flips only; a synonym or different-stem antonym still passes") implies every stem-sharing flip is refused. Bodies 2, 2b, 3, 3b share the stem (`frozen`, `revised`) and pass. The draft QUALITY 67 limit (`ScribeC1Rows.md:63-65`, "only sees a flip that shares a five-letter stem … inside its word window") has the same false converse: 3 and 3b are inside the window and pass. The SKILL limits cell names windows but omits the in-window miscounts, `lack`/`un-`, the per-bullet scope, the span-grounded figure skip, and the `/dev/null` counts in the lane's own runs.
- Smallest safe wording, with no predicate, counter, fixture, floor or target changed: "refuses a **windowed stem-sharing negator mismatch** (`INF_POLARITY_FLIP`): a quoted span phrase whose stem reappears in the bullet with the opposite negator count in a 3-before/2-after window, or a counts-manifest figure whose next 4 words disagree with its key; **not entailment** — double or unrelated negators in the window, negative verbs/affixes, different stems, flips in another bullet, and span-grounded figures pass, and lane entries run with `--counts /dev/null`, so the figure leg is fixture-only." Apply the same clause to the tool docstring's Named limit (`:45-48`) and to `claims.md:62` as a lesson note, not a claim edit (the claim is frozen).

## 6. Axes and corrections

- **operability (C1):** the claim verifies as declared (`C1=PASS`, §0), and its three junk fixtures are the easiest members of the class. The D7 class stays open, and §1 gives 12 accepted flips. The cheapest real tightenings, as round-48 candidates and not this claim: (a) **parity**, so an even negator count in the window reads as affirmed (kills 3, 3b, 5b); (b) apply P2's window on both sides (kills 2b); (c) run `figure_flip` on span-grounded figures too (kills 8); (d) add `lack`/`lacks`/`absent`/`fails`/`un`+stem to the negation lexicon (kills 1b, 5c); (e) check every bullet's unquoted words against the whole entry's grounded phrases (kills 4a, 4b). Each needs the false-positive leg (`LabC1FalsePos`) re-run.
- **calibration:** the rows must name the window and the `/dev/null` reachability gap (§3, §5). Calling the figure leg a lane capability is false until an entry run passes a real counts manifest.
- **depth:** a C3 entry passing rule 5 is not evidence that its inference follows. The adoption closure still needs a reader on every Inference bullet.

Commands run: `git log`, `sha256sum`, `git cat-file -p a15610a:… | sha256sum`, `git cat-file -p 3807537:tools/inference-ground.py`, `python3 corpus/evidence/round47/c1-count.py`, 20 `inference-ground.py` runs (outputs above), `grep -n` over the tool, `SKILL.md`, `SCORECARD.md`, `claims.md`, `c3-count.py`, and `ScribeC1Rows.md`. No install, no fetch. Scratch removed at close.
