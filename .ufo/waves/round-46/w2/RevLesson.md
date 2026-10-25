# RevLesson — round-46 lesson audit (`## Mistakes`, `## Gate`)

seat: reviewer (leaf). Scope: `corpus/lessons/round-46.md` only. No lane production
file, index or jj state touched; scratch `/tmp/chousa-r46w2-RevLesson` removed.

## Target identity (the record moved twice while this seat ran)

| state | sha256 of `corpus/lessons/round-46.md` | note |
|---|---|---|
| `d09fc8e7` (claim landing) | — file absent | `git cat-file -p d09fc8e7:corpus/lessons/round-46.md` → `fatal: path … does not exist` |
| `3807537` (wave-2 setup) | `1749b0cc453f2a4c…` | 12 mistake rows; lesson added here, not in the landing commit (r44 `b603302`, r45 `5e8c7ad` carried theirs at landing) |
| `e50b388` (HEAD at 07:41) | same file, 14 rows | rows 13–14 + `### Named limits` added |
| worktree 07:39–07:41 | `83449da77674f7a5…` | edited live; `git status` also `M c1-count.py`, `M c2-count.py`, `M tools/inference-ground.py` |

Audited bytes = `e50b388` plus the live worktree; row numbers below are the live ones.

## `## Mistakes` — 14 rows, checklist per row

Requirement: class present · evidence pointer resolves · captured-by names a
criterion or `none` · fix shown able to fail (a command or receipt exists).

| row | class | captured-by | evidence pointer | fix shown able to fail |
|---|---|---|---|---|
| 1 | yes | `none at freeze` | `MutC1Junk` Row F (`:103`), `SentScopeAudit` F1/F2, `CritC1Attack` §5 | **verified by me** — see probes |
| 2 | yes | “the critic” (seat, not a criterion) | `CritC1Attack` §2 (`:52`), `ReviewerC1Tool` HIGH | receipt exists (`§2 exits 0`) but demonstrates the retained limit, not that the reporting fix is detectable |
| 3 | yes | “the code reviewer” | `ReviewerC1Tool` HIGH ×2 | **verified by me** — 3 forged numeral bullets exit 1 |
| 4 | yes | “the mutation-tester” | `MutC2Forge` (fenced/pyc/HTML) | receipt exists, but it contains an unmentioned 7th block `SKILL-7pipe … REGISTERED=71/71 C2=PASS exit=0` (`c2-controls.txt:50-56`) while the row says “forges refused” |
| 5 | yes | **MISSING** | `SentScopeAudit` F3 ×3 | **verified by me** — absolute + `../` manifests both exit 1 |
| 6 | yes | seat + sweep | `ScribeGateBlock` Findings 5; its digest `31c9836b942a00ba…` ≠ committed copy `c02c6f3dcc42fa06…` | **MISSING** (no `cmp`/sweep receipt committed) |
| 7 | yes | `none` (named limit) | `ReviewerC3Spans:78` — but that report has no “defect 1” label | no checker: the row itself says “the counter still cannot” |
| 8 | yes | source-opening seats | `ReviewOpenS089` X1, `ReviewOpenS086` | **MISSING** (no grep/receipt for the absent staged string) |
| 9 | yes | **MISSING** | `ReviewerC3Spans` “5” unresolvable (unnumbered bullets; item is `:97`); `ScribeEntryAmend` (c) `:108`; `CritC3Inference` I2 | **MISSING** |
| 10 | yes | **MISSING** | `ReviewerC2Set:37` (68/13) | **FAILS** — see H2 |
| 11 | yes | **MISSING** | `ReviewOpenS086:125` (M1) | **FAILS** — see H3 |
| 12 | yes | **MISSING** | `ScoutInheritedTree`, `ConnectSiblings` §8 | **MISSING** (“value-neutrality measured” names no file) |
| 13 | yes | **MISSING** | `ExecCounterRun` F1 `:64` | **MISPOINTED** — the real-tool `CANARY=pass` is `controls/c1-before.txt:8`, not `controls/c1-controls.txt`, which has 3 blocks (always-pass, cite-only, name-oracle) |
| 14 | yes | **MISSING** | `ExecCounterRun` | none by design (declared named limit) |

Counts: class 14/14 · captured-by 7/14 (missing 5, 9, 10, 11, 12, 13, 14) ·
evidence label present 14/14 (5 anchors imprecise/unresolvable: 7, 9, 6 digest, 13
location, 1 “point 5” resolves only to §5) · shown-able absent 5/14 (6, 8, 9, 12,
14), substantive 2 failures (10, 11), 1 uncheckable (7), 1 mispointed (13).

### H1 (high) — row 10's fix receipt is not the committed receipt, and the cell points at a section that does not exist

Row 10 (`:103-109`): “the receipt now carries three labelled trees (A: freeze
tree, B: base + the whole round-46 dir, C: bare base) … the three trees print
three different denominators.” `controls/c2-before.txt` has **two** trees and no
“tree C”; tree B is labelled “the bare base tree … (no round-46 counters)” yet
prints `ENTRY_POINTS=71 (tools=7 counters=50 named=69) REGISTERED=55/71
UNREGISTERED=16`. **No tree prints 68/13.** `SCORECARD.md:2460` also cites
“`controls/c2-before.txt` tree C” for 68/13 — a pointer to a nonexistent section.
(`ReviewerC2Set:37` measured 68/13 on the bare commit, but no committed receipt
carries it.)

### H2 (high) — row 11: the numbers are wrong and the “before” state exists in no committed tree

Row 11 (`:110-116`): “a span is 194–196 chars against 16–56 for its quote …
`--check` re-derives 11/11”. Measured at `e50b388`: span lengths are
`176,183,183,193,198,198,202,204,206,215` (**176–215**), quote lengths
`16,19,23,23,33,38,38,42,44,46,55` (**16–55**). `build-spans.py --check` prints
`SPANS_ROWS=11 STALE=0`, exit 0 (not `11/11`). The cited before-state (“every span
file was byte-identical to its quote”, `ReviewOpenS086` M1, lengths
23,46,44,16,19,38,23,38,55,42,33) is contradicted by the only trees that carry
spans: `d09fc8e7` and `3a3bc7a` both have `spans/S085-1.txt` = 183 bytes with
`offset 2280` (= quote offset 2360 − 80). Context was present from the first
commit, so row 11's evidence claim and its 194–196 figure cannot be reproduced.

### M1 (medium) — the record's C2 after-value is stale by one

Lesson `:27-28` and `SCORECARD.md:2460` say after = `ENTRY_POINTS=72 …
REGISTERED=72/72`. Committed `corpus/evidence/round46/measure-after.txt` and the
live run both print `ENTRY_POINTS=73 (tools=8 counters=50 named=71)
REGISTERED=73/73 UNREGISTERED=0 C2=PASS`, exit 0. Cause: the round-46 SCORECARD
section itself names `corpus/evidence/round46/build-spans.py`, which leg C then
picks up (+1 named). The kill rule (`UNREGISTERED>0`, `ENTRY_POINTS<71`) is still
met, so the verdict stands; the number a reader would re-measure does not.

### L (low) — row 6's fix claim is not verifiable

`ScribeGateBlock` Findings 5 records the lane copy as `cmp`-identical with sha256
`31c9836b942a00ba…`; the committed copy is `c02c6f3dcc42fa06021f03868fd2595964bedf42c81ed3b01a47835a284a4c12`.
No `cmp` output is committed, and the fleet sweep now prints
`M .ufo/state/chousa.report-baseline` (a chousa-named path, not round-46), so
“no chousa/round-46 path” is true only of round-46 paths.

## `## Gate` — five rows S085–S089

Each row was checked for URL, access date and a ≤25-word quote located in the
named capture (quote offsets are the lesson's own `char N` values; captures are
the five `.qcache` files named in the claim).

| row | URL | quotes, word counts | offsets verified as exact occurrences |
|---|---|---|---|
| S085 | https://fever.ai/dataset/fever.html | 5, 6 | 2360, 1271 ✓ |
| S086 | https://aclanthology.org/N18-1074.pdf | 7, 3, 4 | 15269, 42011, 20847 ✓ |
| S087 | https://zenodo.org/api/records/4925954 | 1+1, 1+1 (JSON fragments) | 171, 4929 ✓ |
| S088 | https://fever.ai/dataset/averitec.html | 7, 10 | 3929, 2904 ✓ |
| S089 | https://arxiv.org/html/2505.17978v2 | 4, 5 (curly apostrophe held) | 3022, 7137 ✓ |

All 11 quotes are verbatim at their stated offsets (longest quote 10 words); no
row exceeds 25 words. **Access date: present only collectively** — `Rows added
(opened 2026-10-25, …)` at `:238`, one date for all five, not per row. The five
`corpus/SOURCES.md:96-100` rows each carry `2026-10-25`, so the fact is checkable,
but the Gate row itself records no per-row date (element missing per row).

Gate's surrounding numbers verified: freeze registry 84 rows (`c2f0e9d`), after
89 rows (`d09fc8e7`), ids `S001`–`S089` contiguous (no gap), quarantine claim
correct — `quarantine-check.py slice` lists `S116 round4 payload-absent
https://aclanthology.org/N18-1074.pdf 3`.

## Probes I ran (verbatim decisive lines)

```
$ git -C … archive HEAD | tar -x -C /tmp/chousa-r46w2-RevLesson
$ python3 corpus/evidence/round46/c1-count.py
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS            exit=0
$ printf ' ' >> …/positive-a.md; python3 …/c1-count.py
FIXTURES_CHANGED=positive-a.md / C1=FAIL                                 exit=1
$ python3 …/c1-count.py --tool ./stub2.py      # import sys; sys.exit(2)
POSITIVE_PASS=0/3 / JUNK_KILLED=0/3 / C1=FAIL                            exit=1
$ python3 tools/inference-ground.py --entry case-s020.md --spans … --registry corpus/SOURCES.md
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='2,013'                     exit=1
   (same for '1,534' S005 and '2,018' S086; S085 control token grounds, exit 0)
$ python3 tools/inference-ground.py --entry case-escape.md --spans escape.tsv
FINDING INF_UNGROUNDED bullet=1 token=''                                 exit=1
   (manifest rows with absolute and ../../../tmp span_file, both refused)
$ python3 corpus/evidence/round46/build-spans.py --check
SPANS_ROWS=11 STALE=0                                                    exit=0
$ python3 corpus/evidence/round46/c2-count.py --list | tail -4
ENTRY_POINTS=73 (tools=8 counters=50 named=71) / GATES_ROWS=35 /
REGISTERED=73/73 / UNREGISTERED=0 / C2=PASS                              exit=0
$ python3 tools/inference-ground.py --entry <both admitted entries> …
GROUND: PASS (7/7 and 5/5)                                               exit=0
```

Row 1's fix and row 3's and row 5's fixes therefore hold as declared. Row 13's
CANARY fix exists in the live counter (`c1-count.py:94-101`) and the name-oracle
control is recorded (`c1-controls.txt:22 CANARY=fail C1=FAIL`).

## Residual risk / gaps

- The record is still moving: three production files are `M` in the worktree while
  this audit ran; a re-audit against a later commit may find rows 13–14 rewritten.
- “same five W04” in the Gate was not re-run (`measure-after.txt` prints one W04
  line, `S075`); census re-derivation belongs to `RevCensus`.
- Row 3's “27 of 86 rows carry a 4-digit URL run” was not recounted; the
  forged-bullet behaviour itself was verified.
- `ReviewOpenS086` M1's span measurement cannot be reproduced from any commit;
  I did not decide whether the report or its tree description is at fault — the
  lesson row is defective either way.
